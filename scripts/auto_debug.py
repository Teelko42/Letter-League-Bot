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
import signal
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
JOURNAL_PATH = LOG_DIR / "auto_debug_journal.md"
AUTOPLAY_STDERR_TMP = LOG_DIR / "_autoplay_stderr.tmp"

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
    clean_turns: int  # all turn lines (placed + skipped) — kept for the journal
    placed_turns: int  # turns that actually committed a word
    skipped_turns: int  # turns that ended in swap/skip (success gate must NOT count these)
    reached_terminal_marker: bool  # saw "Reached max_turns" / "Game over" / "Stop requested"


def _log(msg: str) -> None:
    stamp = time.strftime("%H:%M:%S")
    line = f"[auto_debug {stamp}] {msg}"
    print(line, flush=True)
    with ORCHESTRATOR_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def _kill_process_tree(pid: int) -> None:
    """Best-effort kill of pid and all descendants.

    On Windows, subprocess.run(timeout=...) only signals the immediate child,
    so a wedged Playwright session (chromium + node helper) keeps the python
    parent's stdio pipes open and the timeout never returns. taskkill /T walks
    the whole tree by PID. On POSIX we kill the process group.
    """
    if os.name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                capture_output=True,
                timeout=15,
            )
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass
    else:
        try:
            pgid = os.getpgid(pid)
        except (ProcessLookupError, PermissionError):
            return
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(pgid, sig)
            except (ProcessLookupError, PermissionError, OSError):
                return
            time.sleep(1.5)


def _run_with_tree_kill(
    cmd: list[str],
    cwd: str,
    env: dict[str, str],
    timeout_s: int,
    stderr_file: Path,
) -> tuple[int, str, bool]:
    """Spawn cmd in its own process group; on timeout, kill the whole tree.

    stderr is redirected to ``stderr_file`` instead of a PIPE — long runs (loguru
    streams INFO to stderr per turn) would otherwise fill the 64KB pipe buffer
    and deadlock the child once the parent stops draining. Returns
    (exit_code, stderr_text, hit_timeout).
    """
    if os.name == "nt":
        popen_kwargs: dict[str, object] = {
            "creationflags": subprocess.CREATE_NEW_PROCESS_GROUP,
        }
    else:
        popen_kwargs = {"start_new_session": True}

    stderr_file.parent.mkdir(parents=True, exist_ok=True)
    if stderr_file.exists():
        stderr_file.unlink()

    with stderr_file.open("w", encoding="utf-8", errors="replace") as ferr:
        proc = subprocess.Popen(  # noqa: S603 — args are constructed locally
            cmd,
            cwd=cwd,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=ferr,
            **popen_kwargs,  # type: ignore[arg-type]
        )
        hit_timeout = False
        try:
            proc.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            hit_timeout = True
            _log(f"timeout — killing process tree pid={proc.pid}")
            _kill_process_tree(proc.pid)
            try:
                proc.wait(timeout=20)
            except subprocess.TimeoutExpired:
                _log(f"WARNING: process tree kill did not fully drain pid={proc.pid}")

    try:
        stderr_text = stderr_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        stderr_text = ""

    if hit_timeout:
        stderr_text += "\n[auto_debug] subprocess timeout — process tree killed"
        exit_code = -9
    else:
        exit_code = proc.returncode if proc.returncode is not None else -9

    return exit_code, stderr_text, hit_timeout


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
# Distinguish "actually placed a word" from "swap/skip" so the success gate
# can't be fooled by a run that exits cleanly while the bot is mostly skipping.
_TURN_LINE_RE = re.compile(r"\| __main__:_run:\d+ \| Turn \d+: ")
_TURN_PLACED_RE = re.compile(r"\| __main__:_run:\d+ \| Turn \d+: played ")
_TURN_SKIPPED_RE = re.compile(r"\| __main__:_run:\d+ \| Turn \d+: no move accepted")
_TERMINAL_RE = re.compile(
    r"Reached max_turns=|Game over after |Stop requested — exiting|Idle timeout — exiting"
)


def _count_clean_turns(log_lines: list[str]) -> tuple[int, int, int, bool]:
    """Scan the *full* per-run log slice for turn-completion markers.

    Returns (total_turns, placed_turns, skipped_turns, saw_terminal_marker).
    The success gate must compare against placed_turns, not total_turns —
    a bot that takes its turn but always swap/skips would otherwise be
    declared healthy. The user's bar is "place a word every turn".
    """
    total = 0
    placed = 0
    skipped = 0
    saw_terminal = False
    for ln in log_lines:
        if _TURN_PLACED_RE.search(ln):
            placed += 1
            total += 1
        elif _TURN_SKIPPED_RE.search(ln):
            skipped += 1
            total += 1
        elif _TURN_LINE_RE.search(ln):
            # Forward-compat: any new "Turn N:" variant we don't recognise.
            total += 1
        if _TERMINAL_RE.search(ln):
            saw_terminal = True
    return total, placed, skipped, saw_terminal


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

    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    env.setdefault("PYTHONIOENCODING", "utf-8")

    start = time.monotonic()
    exit_code, stderr, _hit_timeout = _run_with_tree_kill(
        cmd,
        cwd=str(PROJECT_ROOT),
        env=env,
        timeout_s=run_timeout_s,
        stderr_file=AUTOPLAY_STDERR_TMP,
    )
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
    total_turns, placed, skipped, reached_terminal = _count_clean_turns(run_log)
    # Hashing stderr_tail + error_lines gives us a fingerprint resilient to
    # whichever sink caught the failure.
    signature = _canonicalise_error(error_lines + stderr_lines[-20:])

    return RunResult(
        exit_code=exit_code,
        duration_s=duration,
        stderr_tail=stderr_tail,
        error_lines=error_lines,
        error_signature=signature,
        clean_turns=total_turns,
        placed_turns=placed,
        skipped_turns=skipped,
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
        f"- words placed: {result.placed_turns}",
        f"- turns skipped (swap/skip — these are FAILURES for the user goal): "
        f"{result.skipped_turns}",
        f"- terminal marker reached: {result.reached_terminal_marker}",
        "",
        "**User goal: the bot must place a word every turn.** A turn that ends in",
        "swap/skip means the placement pipeline failed (vision drift, retries",
        "exhausted, etc.) and the engine fell back to swap. The fix needs to make",
        "more turns end with a placed word, not just keep the run alive longer.",
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


def _dirty_py_files() -> set[str]:
    """Return repo-relative paths of modified or added .py files (uncommitted)."""
    out = _git("status", "--porcelain")
    files: set[str] = set()
    for line in out.splitlines():
        if len(line) < 4:
            continue
        # Porcelain format: XY <path>  (rename uses ' -> ', deletions start with D)
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1].strip()
        path = path.strip('"')
        if line[0] == "D" or line[1] == "D":
            continue
        if path.endswith(".py"):
            files.add(path.replace("\\", "/"))
    return files


def _changed_py_since(initial: set[str]) -> list[str]:
    """Files claude touched this session: dirty now but not dirty at startup."""
    return sorted(_dirty_py_files() - initial)


def _module_for(path: str) -> str | None:
    """Convert e.g. 'src/browser/tile_placer.py' -> 'src.browser.tile_placer'.

    Returns None for paths outside the importable tree (tests/, debug/, etc.)
    or for ``__init__.py`` files (importing those re-runs package init —
    fine for compile, brittle for import-smoke).
    """
    if not (path.startswith("src/") or path.startswith("scripts/")):
        return None
    if path.endswith("/__init__.py"):
        return None
    if not path.endswith(".py"):
        return None
    return path[:-3].replace("/", ".")


def _matching_test_files(changed: list[str]) -> list[str]:
    """For each src/<area>/<name>.py find tests/test_<name>.py or tests/<area>/test_<name>.py."""
    found: list[str] = []
    seen: set[str] = set()
    for f in changed:
        if not f.startswith("src/"):
            continue
        stem = Path(f).stem
        rel_parent = Path(f).parent
        try:
            sub = rel_parent.relative_to("src")
        except ValueError:
            sub = Path()
        candidates = [
            PROJECT_ROOT / "tests" / f"test_{stem}.py",
            PROJECT_ROOT / "tests" / sub / f"test_{stem}.py",
        ]
        for c in candidates:
            rel = c.relative_to(PROJECT_ROOT).as_posix()
            if c.exists() and rel not in seen:
                found.append(rel)
                seen.add(rel)
    return found


def _smoke_test_changed(changed: list[str]) -> tuple[bool, list[str]]:
    """Compile + import + targeted pytest gate on Claude's edits.

    Returns (ok, failure_summaries). ok=True when every step passed.
    Each failure summary is a short label + truncated stderr.
    """
    if not changed:
        return True, ["smoke: no .py files changed — skipped"]

    failures: list[str] = []
    env = os.environ.copy()
    env.setdefault("PYTHONPATH", str(PROJECT_ROOT))
    env.setdefault("PYTHONIOENCODING", "utf-8")

    # 1. py_compile: parser + bytecode-gen, catches syntax errors fast.
    for f in changed:
        proc = subprocess.run(
            [sys.executable, "-m", "py_compile", f],
            cwd=str(PROJECT_ROOT),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        if proc.returncode != 0:
            failures.append(f"py_compile {f}:\n{(proc.stderr or proc.stdout).strip()[-800:]}")

    if failures:
        return False, failures

    # 2. import: catches NameError/missing import/circular import that compile misses.
    for f in changed:
        mod = _module_for(f)
        if mod is None:
            continue
        proc = subprocess.run(
            [sys.executable, "-c", f"import {mod}"],
            cwd=str(PROJECT_ROOT),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        if proc.returncode != 0:
            failures.append(f"import {mod}:\n{(proc.stderr or proc.stdout).strip()[-800:]}")

    if failures:
        return False, failures

    # 3. matching tests, if any. -x stops on first failure to keep the loop tight.
    test_files = _matching_test_files(changed)
    if test_files:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", *test_files, "-x", "-q"],
            cwd=str(PROJECT_ROOT),
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=240,
        )
        if proc.returncode != 0:
            tail = ((proc.stdout or "") + "\n" + (proc.stderr or "")).strip()[-1500:]
            failures.append(f"pytest {' '.join(test_files)} failed:\n{tail}")

    return len(failures) == 0, failures or ["smoke: PASS"]


def _append_smoke_section_to_bundle(bundle: Path, failures: list[str], attempt: int) -> None:
    """Append a smoke-failure section to the iteration bundle so the retry sees it."""
    parts = [
        "",
        f"## Post-edit smoke gate FAILED (attempt {attempt})",
        "Your previous edit broke the smoke checks below. Read the failure",
        "output, fix the actual issue (don't paper over it by deleting the",
        "import or skipping the test), and end your turn.",
        "",
    ]
    for fail in failures:
        parts.append("```")
        parts.append(fail)
        parts.append("```")
        parts.append("")
    with bundle.open("a", encoding="utf-8") as f:
        f.write("\n".join(parts))


_HYPOTHESIS_RE = re.compile(
    r"\*?\*?root cause[^*\n:]*\*?\*?:?\s*(.+?)(?:\n\s*\n|\*\*Files|\*\*Why|\Z)",
    re.IGNORECASE | re.DOTALL,
)


def _extract_hypothesis(response_text: str) -> str:
    """Pull the 'root cause' sentence from a Claude response for the journal."""
    if not response_text.strip():
        return "(empty response — claude likely timed out)"
    m = _HYPOTHESIS_RE.search(response_text)
    if m:
        text = m.group(1).strip().lstrip("*: ").strip()
        return re.sub(r"\s+", " ", text)[:400]
    # Fallback: first non-empty paragraph
    paragraphs = [p.strip() for p in response_text.split("\n\n") if p.strip()]
    if not paragraphs:
        return "(no extractable hypothesis)"
    return re.sub(r"\s+", " ", paragraphs[0].lstrip("*: ").strip())[:400]


def _journal_excerpt(max_entries: int = 5) -> str:
    """Last N entries of the cross-iteration journal, or a placeholder."""
    if not JOURNAL_PATH.exists():
        return "_(none — this is iteration 1, or the journal was reset)_"
    try:
        text = JOURNAL_PATH.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "_(journal unreadable)_"
    # Entries start with "## Iter " — split, keep the last N.
    chunks = re.split(r"(?m)^(?=## Iter )", text)
    chunks = [c.strip() for c in chunks if c.strip().startswith("## Iter ")]
    if not chunks:
        return "_(journal empty)_"
    return "\n\n".join(chunks[-max_entries:])


def _journal_append(
    iteration: int,
    result: "RunResult",
    changed_files: list[str],
    hypothesis: str,
    smoke_status: str,
) -> None:
    """Append a structured per-iteration entry the next iteration's prompt will read."""
    JOURNAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not JOURNAL_PATH.exists():
        JOURNAL_PATH.write_text(
            "# Auto-debug journal\n\n"
            "Each entry summarises one fix attempt. Newer iterations should\n"
            "read this so they don't repeat or undo previous work.\n",
            encoding="utf-8",
        )
    files_line = ", ".join(changed_files) if changed_files else "(none)"
    parts = [
        "",
        f"## Iter {iteration} — sig {result.error_signature}",
        f"- exit: `{result.exit_code}`  duration: {result.duration_s:.0f}s  "
        f"placed: {result.placed_turns}  skipped: {result.skipped_turns}  "
        f"terminal_marker: {result.reached_terminal_marker}",
        f"- changed: {files_line}",
        f"- smoke: {smoke_status}",
        f"- hypothesis: {hypothesis}",
    ]
    with JOURNAL_PATH.open("a", encoding="utf-8") as f:
        f.write("\n".join(parts) + "\n")


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

## Previous attempts (read before editing)
The orchestrator records every prior fix attempt below. Do NOT re-apply a
fix that's already in place — read what's been tried, figure out what's
*new* about the current failure, and target that. If a previous hypothesis
turned out wrong, consider reverting it before patching elsewhere.

{journal_excerpt}

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
    journal_excerpt: str = "",
) -> tuple[bool, str]:
    prompt = PROMPT_TEMPLATE.format(
        bundle_path=bundle_path.as_posix(),
        iteration=iteration,
        max_iterations=max_iterations,
        signature=signature,
        journal_excerpt=journal_excerpt or "_(no prior attempts recorded)_",
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
    p.add_argument("--smoke-claude-timeout", type=int, default=600,
                   help="Claude invocation timeout for smoke-gate retries (focused task)")
    p.add_argument("--no-smoke-gate", action="store_true",
                   help="Disable post-edit compile/import/pytest gate (not recommended)")
    p.add_argument("--reset-journal", action="store_true",
                   help="Wipe logs/auto_debug_journal.md before starting (default: keep history)")
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

    if args.reset_journal and JOURNAL_PATH.exists():
        JOURNAL_PATH.unlink()
        _log("journal reset")

    # Snapshot pre-existing dirty .py files so the smoke gate only runs on
    # files claude actually touches this session (not the user's stash).
    initial_dirty = _dirty_py_files()
    if initial_dirty:
        _log(f"pre-existing dirty .py files (excluded from smoke): {sorted(initial_dirty)}")

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
             f"duration={result.duration_s:.1f}s  sig={result.error_signature}  "
             f"placed={result.placed_turns}  skipped={result.skipped_turns}  "
             f"terminal={result.reached_terminal_marker}")

        if result.exit_code == 0:
            placed = result.placed_turns
            skipped = result.skipped_turns
            # The user's bar is "place a word every turn without fault." A
            # run that exits cleanly but mostly skipped is NOT a success —
            # it's the exact failure mode we're trying to fix. The gate must
            # compare placed_turns against min_clean_turns and never let
            # skip-heavy runs slip through.
            #
            # Skip ratio guard: even hitting min_clean_turns in placements
            # doesn't count if more than 1/3 of total turns were skipped —
            # that signals the bot still has a placement reliability bug.
            total = placed + skipped
            skip_ratio = (skipped / total) if total else 0.0
            quota_reached = (
                args.turns_per_run > 0 and placed >= args.turns_per_run
            )
            placement_healthy = (
                placed >= args.min_clean_turns and skip_ratio <= 0.33
            )
            if quota_reached or placement_healthy:
                _log(
                    f"SUCCESS — clean exit, {placed} placed / {skipped} skipped"
                    f"{' (terminal marker seen)' if result.reached_terminal_marker else ''}"
                    f". Stopping."
                )
                return 0
            reason: str
            if placed < args.min_clean_turns:
                reason = f"only {placed} word(s) placed (need >= {args.min_clean_turns})"
            else:
                reason = f"skip ratio {skip_ratio:.0%} too high (placed={placed}, skipped={skipped})"
            _log(f"Clean exit but {reason} — treating as partial and continuing.")

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

        journal_excerpt = _journal_excerpt(max_entries=5)

        ok, out = _invoke_claude(
            claude_exe or "claude",
            bundle,
            iteration,
            args.max_iterations,
            result.error_signature,
            timeout_s=args.claude_timeout,
            dry_run=args.dry_run,
            journal_excerpt=journal_excerpt,
        )
        # Record the claude response for human review
        response_path = LOG_DIR / f"auto_debug_iter_{iteration:03d}_response.md"
        response_path.write_text(out, encoding="utf-8")
        _log(f"{'ok' if ok else 'FAIL'} — claude response -> {response_path.as_posix()}")

        if not ok and not args.dry_run:
            _log("claude returned non-zero; continuing anyway to let the next run expose state")

        # ── Post-edit smoke gate ──────────────────────────────────────────────
        # Compile + import + matching pytest on whatever .py files claude touched
        # this session. If the gate fails, re-invoke claude once with the failure
        # appended to the bundle. We don't skip the next autoplay run on smoke
        # failure: a broken import causes autoplay to exit in seconds (not 30 min)
        # so the next iteration just sees the same error and tries again, with the
        # journal entry below telling claude what already went wrong.
        smoke_status = "skipped (--no-smoke-gate)"
        if args.dry_run:
            smoke_status = "skipped (--dry-run)"
        elif args.no_smoke_gate:
            pass
        else:
            changed = _changed_py_since(initial_dirty)
            _log(f"smoke gate: {len(changed)} claude-touched .py file(s)")
            smoke_ok, summary = _smoke_test_changed(changed)
            if smoke_ok:
                smoke_status = "PASS" if changed else "PASS (no changes)"
                _log(f"smoke: {smoke_status}")
            else:
                _log(f"smoke: FAIL — {len(summary)} issue(s); re-invoking claude")
                _append_smoke_section_to_bundle(bundle, summary, attempt=1)
                _ok2, out2 = _invoke_claude(
                    claude_exe or "claude",
                    bundle,
                    iteration,
                    args.max_iterations,
                    result.error_signature,
                    timeout_s=args.smoke_claude_timeout,
                    dry_run=False,
                    journal_excerpt=journal_excerpt,
                )
                retry_path = LOG_DIR / f"auto_debug_iter_{iteration:03d}_smoke_retry.md"
                retry_path.write_text(out2, encoding="utf-8")
                _log(f"smoke retry claude response -> {retry_path.as_posix()}")
                changed = _changed_py_since(initial_dirty)
                smoke_ok2, summary2 = _smoke_test_changed(changed)
                if smoke_ok2:
                    smoke_status = "PASS (after 1 retry)"
                    _log("smoke: PASS after retry")
                else:
                    head = summary2[0].splitlines()[0] if summary2 else "unknown"
                    smoke_status = f"FAIL after retry: {head}"
                    _log("smoke still failing — next iteration will see it via journal + autoplay log")

        # ── Journal this iteration so the next prompt sees what happened ──────
        hypothesis = _extract_hypothesis(out)
        changed_now = _changed_py_since(initial_dirty)
        _journal_append(iteration, result, changed_now, hypothesis, smoke_status)

        _log(f"sleeping {args.backoff}s before next run")
        time.sleep(args.backoff)

    _log(f"max iterations ({args.max_iterations}) reached without a clean run. Giving up.")
    return 4


if __name__ == "__main__":
    sys.exit(main())
