"""Auto-debug loop: run autoplay headlessly, auto-fix crashes with Claude.

This tool wraps scripts/autoplay_headless.py in a retry loop. When the
headless run crashes (non-zero exit or an ERROR-level log line is observed),
the orchestrator:

  1. Collects a debug bundle:
       - Tail of logs/autoplay.log
       - The latest debug/tile_placer/*.png and debug/turn_detection/*.png
       - `git status` / `git diff --stat` relative to the last clean run
       - Exit code and the last ~80 stderr lines from the subprocess
  2. Writes the bundle to `logs/auto_debug_iter_{N}.md`
  3. Invokes the Claude CLI in headless mode (`claude -p ...`) scoped to the
     project directory, asks it to diagnose the failure and patch the code
     (no git commit), with tool access restricted to Read/Edit/Grep/Glob/Bash.
  4. Records the returned fix summary, waits a short backoff, relaunches the
     headless run, and repeats.

The loop stops when:
  - The headless run completes cleanly (exit 0) AND played at least
    --min-clean-turns turns, OR
  - --max-iterations is exceeded, OR
  - The same error signature is hit --repeat-limit times in a row
    (indicates the patches aren't helping — aborts to avoid thrashing).

Nothing is ever committed or pushed. The user reviews `git diff` at the end.

Usage:
    py -m scripts.auto_debug                  # default: 10 iter, 3 clean turns
    py -m scripts.auto_debug --max-iterations 5 --min-clean-turns 5
    py -m scripts.auto_debug --turns-per-run 10 --dry-run
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
AUTOPLAY_LOG = LOG_DIR / "autoplay.log"
ORCHESTRATOR_LOG = LOG_DIR / "auto_debug.log"

DEBUG_DIRS = [
    PROJECT_ROOT / "debug" / "tile_placer",
    PROJECT_ROOT / "debug" / "turn_detection",
    PROJECT_ROOT / "debug",
]

# Lines from the autoplay log we consider evidence of a failure that needs
# investigation even if the subprocess hasn't crashed. Matched case-insensitively.
ERROR_PATTERNS = [
    r"Traceback \(most recent call last\)",
    r"\| ERROR\s+\|",
    r"Vision failed twice",
    r"All words rejected",
    r"PlacementError",
    r"VisNError",
    r"Recall after PlacementError also failed",
    r"game did not transition after clicking",
    r"unrecoverable error",
]
ERROR_RE = re.compile("|".join(ERROR_PATTERNS), re.IGNORECASE)


@dataclass
class RunResult:
    exit_code: int
    duration_s: float
    stderr_tail: str
    error_lines: list[str]
    error_signature: str  # hash of the canonicalised top error — used for loop-guard
    clean_turns: int  # turns observed in the FULL run log (not just error window)
    reached_terminal_marker: bool  # saw "Reached max_turns" / "Game over" / "Stop requested"


def _log(msg: str) -> None:
    stamp = time.strftime("%H:%M:%S")
    line = f"[auto_debug {stamp}] {msg}"
    print(line, flush=True)
    with ORCHESTRATOR_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def _tail_lines(path: Path, n: int) -> list[str]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except OSError:
        return []
    return lines[-n:]


def _newest_files(dir_path: Path, n: int, since_mtime: float = 0.0) -> list[Path]:
    if not dir_path.exists() or not dir_path.is_dir():
        return []
    entries = [
        p for p in dir_path.iterdir()
        if p.is_file() and p.stat().st_mtime > since_mtime
    ]
    entries.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return entries[:n]


def _canonicalise_error(lines: list[str]) -> str:
    """Produce a stable hash of the error — strips timestamps & paths."""
    joined = "\n".join(lines[-40:])
    # Remove absolute paths, timestamps, hex addresses, and line numbers
    joined = re.sub(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}[.,]\d+", "", joined)
    joined = re.sub(r"\d{2}:\d{2}:\d{2}", "", joined)
    joined = re.sub(r"0x[0-9a-fA-F]+", "", joined)
    joined = re.sub(r":\d+\b", ":LINE", joined)
    joined = re.sub(r"[A-Z]:[\\/][\S]+?[\\/](src|scripts|tests)", r"\1", joined)
    return hashlib.sha1(joined.encode("utf-8", "replace")).hexdigest()[:12]


def _extract_error_lines(log_lines: list[str]) -> list[str]:
    """Return the block of consecutive log lines containing the most relevant error."""
    hits = [i for i, ln in enumerate(log_lines) if ERROR_RE.search(ln)]
    if not hits:
        return log_lines[-30:]
    start = max(0, hits[0] - 5)
    end = min(len(log_lines), hits[-1] + 20)
    return log_lines[start:end]


# Markers emitted by scripts/autoplay_headless.py — see _run() in that file.
_TURN_PLAYED_RE = re.compile(r"\| __main__:_run:\d+ \| Turn \d+: ")
_TERMINAL_RE = re.compile(
    r"Reached max_turns=|Game over after |Stop requested — exiting|Idle timeout — exiting"
)


def _count_clean_turns(log_lines: list[str]) -> tuple[int, bool]:
    """Scan the *full* per-run log slice for turn-completion markers.

    Returns (turn_count, saw_terminal_marker). A clean exit-0 run that played
    its full quota emits one "Turn N: ..." line per turn plus a terminal
    marker — the orchestrator's success heuristic must read these from the
    whole run, not the narrow error-region tail (which can be entirely
    consumed by a single slow turn's placement logging).
    """
    turn_count = 0
    saw_terminal = False
    for ln in log_lines:
        if _TURN_PLAYED_RE.search(ln):
            turn_count += 1
        if _TERMINAL_RE.search(ln):
            saw_terminal = True
    return turn_count, saw_terminal


def _run_autoplay(
    turns_per_run: int,
    mode: str,
    run_timeout_s: int,
    log_start_size: int,
) -> RunResult:
    """Spawn scripts.autoplay_headless as subprocess; capture stderr; return summary."""
    cmd = [
        sys.executable, "-m", "scripts.autoplay_headless",
        "--max-turns", str(turns_per_run),
        "--mode", mode,
    ]
    _log(f"launching: {' '.join(cmd)}  (timeout={run_timeout_s}s)")

    # Use a large ring buffer for stderr so we don't OOM on pathological runs
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    env.setdefault("PYTHONIOENCODING", "utf-8")

    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=run_timeout_s,
        )
        exit_code = proc.returncode
        stderr = proc.stderr or ""
    except subprocess.TimeoutExpired as exc:
        exit_code = -9
        stderr = (exc.stderr or "") + "\n[auto_debug] subprocess timeout — killed"
    duration = time.monotonic() - start

    stderr_lines = stderr.splitlines()
    stderr_tail = "\n".join(stderr_lines[-80:])

    # Slice the autoplay log from where this run began
    full_log = _tail_lines(AUTOPLAY_LOG, 5000)
    # Keep only lines written during this run (by size offset if possible)
    run_log: list[str]
    if AUTOPLAY_LOG.exists() and AUTOPLAY_LOG.stat().st_size >= log_start_size:
        try:
            with AUTOPLAY_LOG.open("r", encoding="utf-8", errors="replace") as f:
                f.seek(log_start_size)
                run_log = f.read().splitlines()
        except OSError:
            run_log = full_log
    else:
        run_log = full_log

    error_lines = _extract_error_lines(run_log)
    clean_turns, reached_terminal = _count_clean_turns(run_log)
    # Hashing stderr_tail + error_lines gives us a fingerprint resilient to
    # whichever sink caught the failure.
    signature = _canonicalise_error(error_lines + stderr_lines[-20:])

    return RunResult(
        exit_code=exit_code,
        duration_s=duration,
        stderr_tail=stderr_tail,
        error_lines=error_lines,
        error_signature=signature,
        clean_turns=clean_turns,
        reached_terminal_marker=reached_terminal,
    )


def _write_context_bundle(
    iteration: int,
    result: RunResult,
    run_start_time: float,
) -> Path:
    bundle = LOG_DIR / f"auto_debug_iter_{iteration:03d}.md"

    newest: list[Path] = []
    for d in DEBUG_DIRS:
        newest.extend(_newest_files(d, 3, since_mtime=run_start_time))
    # dedupe preserving order
    seen = set()
    newest_unique: list[Path] = []
    for p in newest:
        if p not in seen:
            newest_unique.append(p)
            seen.add(p)
    newest_unique = newest_unique[:6]

    git_status = _git("status", "--short")
    git_diff_stat = _git("diff", "--stat")

    parts = [
        f"# Auto-debug iteration {iteration}",
        "",
        f"- exit_code: `{result.exit_code}`",
        f"- duration: {result.duration_s:.1f}s",
        f"- error_signature: `{result.error_signature}`",
        "",
        "## Recent debug artifacts",
        *([f"- `{p.relative_to(PROJECT_ROOT).as_posix()}`" for p in newest_unique]
          or ["_(none produced during this run)_"]),
        "",
        "## Autoplay log — error region",
        "```",
        *[ln.rstrip() for ln in result.error_lines],
        "```",
        "",
        "## Subprocess stderr (tail)",
        "```",
        result.stderr_tail or "(empty)",
        "```",
        "",
        "## git status --short",
        "```",
        git_status or "(clean)",
        "```",
        "",
        "## git diff --stat",
        "```",
        git_diff_stat or "(no changes)",
        "```",
    ]
    bundle.write_text("\n".join(parts), encoding="utf-8")
    return bundle


def _git(*args: str) -> str:
    try:
        out = subprocess.run(
            ["git", *args],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=10,
        )
        return (out.stdout or "").strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        return ""


def _find_claude_cli() -> str | None:
    exe = shutil.which("claude") or shutil.which("claude.exe")
    return exe


PROMPT_TEMPLATE = """You are an autonomous debug agent for the Letter League Bot, a Python project
that plays Discord's Letter League activity using Playwright + a vision
pipeline + a GADDAG move engine.

A headless autoplay run just failed. Your job is to diagnose the root cause
and patch the code so the next run gets further. Work independently — do
NOT ask the user questions and do NOT create git commits.

## Ground rules
- Scope changes to `src/` and `scripts/` only.
- Prefer the smallest possible fix. If the root cause is unclear, add
  targeted logging/assertions rather than guessing.
- Never delete tests. Never disable safety checks to paper over the bug.
- Do not edit `.env`, `browser_data/`, `cache/`, `data/wordlist.txt`, or
  anything under `.planning/`.
- If the failure looks transient (network/browser glitch with no code
  smell), say so explicitly in your final message and make no edits.
- After editing, run the relevant tests if a quick subset exists
  (`py -m pytest tests/<file> -x -q`). Skip running the full suite.

## Context bundle
Read this file first — it has the error region, debug artifacts, git state:

    {bundle_path}

Key source areas (in order of likelihood for this class of failure):
- `src/browser/tile_placer.py` — placement, recall, verification
- `src/browser/turn_detector.py` — turn polling, game-over detection
- `src/browser/capture.py` — canvas screenshotting
- `src/browser/navigator.py` — activity iframe navigation
- `src/vision/__init__.py`, `src/vision/validator.py` — board extraction
- `scripts/autoplay_headless.py` — the headless runner (iteration {iteration})

## Output
End your turn with a short report (1 paragraph):
- Root cause hypothesis
- Files changed (or "no changes — transient failure")
- Why you believe the next run will do better

Iteration {iteration} of {max_iterations}. Previous error signature: `{signature}`."""


def _invoke_claude(
    claude_exe: str,
    bundle_path: Path,
    iteration: int,
    max_iterations: int,
    signature: str,
    timeout_s: int,
    dry_run: bool,
) -> tuple[bool, str]:
    prompt = PROMPT_TEMPLATE.format(
        bundle_path=bundle_path.as_posix(),
        iteration=iteration,
        max_iterations=max_iterations,
        signature=signature,
    )
    if dry_run:
        _log("--dry-run: would invoke claude with the following prompt:")
        print("-" * 60)
        print(prompt)
        print("-" * 60)
        return True, "(dry run)"

    cmd = [
        claude_exe,
        "-p", prompt,
        "--permission-mode", "acceptEdits",
        "--add-dir", str(PROJECT_ROOT),
        "--allowedTools", "Read", "Edit", "Write", "Grep", "Glob", "Bash",
    ]
    _log(f"invoking claude (timeout={timeout_s}s, acceptEdits)")
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired as exc:
        _log(f"claude invocation timed out after {timeout_s}s")
        return False, (exc.stdout or "") + (exc.stderr or "")
    ok = proc.returncode == 0
    out = (proc.stdout or "") + (("\n--- stderr ---\n" + proc.stderr) if proc.stderr else "")
    return ok, out


def main() -> int:
    p = argparse.ArgumentParser(description="Auto-debug loop for Letter League autoplay")
    p.add_argument("--max-iterations", type=int, default=10)
    p.add_argument("--turns-per-run", type=int, default=5,
                   help="--max-turns passed to autoplay_headless each iteration")
    p.add_argument("--min-clean-turns", type=int, default=3,
                   help="Run must survive at least this many turns cleanly to call the fix loop done")
    p.add_argument("--run-timeout", type=int, default=1800,
                   help="Per-run hard timeout in seconds (default 30 min)")
    p.add_argument("--claude-timeout", type=int, default=900,
                   help="Per-fix Claude invocation timeout in seconds")
    p.add_argument("--repeat-limit", type=int, default=3,
                   help="Abort if the same error signature repeats this many times")
    p.add_argument("--mode", choices=("wild", "classic"), default="wild")
    p.add_argument("--backoff", type=int, default=5,
                   help="Seconds to wait between a fix and the next run")
    p.add_argument("--dry-run", action="store_true",
                   help="Do everything except call claude — useful for sanity checks")
    args = p.parse_args()

    claude_exe = _find_claude_cli()
    if claude_exe is None and not args.dry_run:
        _log("ERROR: `claude` CLI not found on PATH. Install claude-code or pass --dry-run.")
        return 2
    if claude_exe:
        _log(f"using claude CLI at: {claude_exe}")

    # Fresh orchestrator log per run
    ORCHESTRATOR_LOG.write_text(f"auto_debug run started {time.strftime('%Y-%m-%d %H:%M:%S')}\n",
                                encoding="utf-8")

    last_signature: str | None = None
    repeat_count = 0

    for iteration in range(1, args.max_iterations + 1):
        _log(f"=== iteration {iteration}/{args.max_iterations} ===")
        log_start_size = AUTOPLAY_LOG.stat().st_size if AUTOPLAY_LOG.exists() else 0
        run_start_time = time.time()

        result = _run_autoplay(
            turns_per_run=args.turns_per_run,
            mode=args.mode,
            run_timeout_s=args.run_timeout,
            log_start_size=log_start_size,
        )

        _log(f"run finished: exit={result.exit_code}  "
             f"duration={result.duration_s:.1f}s  sig={result.error_signature}")

        if result.exit_code == 0:
            clean = result.clean_turns
            # A run that hit its --max-turns quota (or saw "Game over") is a
            # full success regardless of how many turn-lines fall inside the
            # narrow error-region tail. Tile placement logging can easily fill
            # 30 lines per turn, so the previous heuristic mis-classified
            # complete runs as partial.
            quota_reached = (
                args.turns_per_run > 0 and clean >= args.turns_per_run
            )
            if (
                result.reached_terminal_marker
                or quota_reached
                or clean >= args.min_clean_turns
            ):
                _log(
                    f"SUCCESS — clean exit, {clean} turns played"
                    f"{' (terminal marker seen)' if result.reached_terminal_marker else ''}"
                    f". Stopping."
                )
                return 0
            _log(f"Clean exit but only {clean} turns observed — treating as partial and continuing.")

        # Loop guard
        if last_signature == result.error_signature:
            repeat_count += 1
        else:
            repeat_count = 1
        last_signature = result.error_signature

        if repeat_count > args.repeat_limit:
            _log(f"ABORT — same error signature {result.error_signature} repeated "
                 f"{repeat_count} times. The patches aren't helping.")
            return 3

        bundle = _write_context_bundle(iteration, result, run_start_time)
        _log(f"wrote context bundle -> {bundle.as_posix()}")

        ok, out = _invoke_claude(
            claude_exe or "claude",
            bundle,
            iteration,
            args.max_iterations,
            result.error_signature,
            timeout_s=args.claude_timeout,
            dry_run=args.dry_run,
        )
        # Record the claude response for human review
        response_path = LOG_DIR / f"auto_debug_iter_{iteration:03d}_response.md"
        response_path.write_text(out, encoding="utf-8")
        _log(f"{'ok' if ok else 'FAIL'} — claude response -> {response_path.as_posix()}")

        if not ok and not args.dry_run:
            _log("claude returned non-zero; continuing anyway to let the next run expose state")

        _log(f"sleeping {args.backoff}s before next run")
        time.sleep(args.backoff)

    _log(f"max iterations ({args.max_iterations}) reached without a clean run. Giving up.")
    return 4


if __name__ == "__main__":
    sys.exit(main())
