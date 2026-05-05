"""Headless single-player autoplay runner — no Discord bot required.

Reproduces the core of AutoPlayCog._run_game_loop against a live Letter
League game that is already running in the browser profile. Intended as
the subject-under-test for scripts/auto_debug.py, which wraps it with an
automatic bug-fix loop.

Exit codes:
    0  clean exit (game over, idle timeout, or --max-turns reached)
    1  unrecoverable exception raised from the loop
    2  configuration error (missing env, missing wordlist)
    130 Ctrl+C

Environment:
    DISCORD_CHANNEL_URL   Full Discord channel URL where the activity is
                          running. Must already have a game started (or
                          be on the title screen; this script will click
                          START if needed).
    WORDLIST_PATH         Override default data/wordlist.txt location.
    GADDAG_CACHE_PATH     Override default cache/gaddag.pkl location.

Usage:
    py -m scripts.autoplay_headless [--max-turns N] [--mode wild|classic]
"""

from __future__ import annotations

import argparse
import asyncio
import os
import signal
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "autoplay.log"

DEFAULT_WORDLIST = PROJECT_ROOT / "data" / "wordlist.txt"
DEFAULT_GADDAG_CACHE = PROJECT_ROOT / "cache" / "gaddag.pkl"


def _configure_logging() -> None:
    logger.remove()
    logger.add(sys.stderr, level="INFO",
               format="<green>{time:HH:mm:ss}</green> | <level>{level:<7}</level> | {message}")
    logger.add(str(LOG_FILE), level="DEBUG", rotation="5 MB", retention=5,
               enqueue=True,
               format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<7} | {name}:{function}:{line} | {message}")


def _move_is_safe(move: "Move", known_tiles: dict[tuple[int, int], str]) -> bool:
    """Return True iff every existing-board tile this move uses is authoritative.

    A move's ``tiles_used`` mixes rack-placed tiles (from_rack=True) with the
    existing board tiles the word builds on (from_rack=False). When an
    existing-board tile_use sits at a position not in ``known_tiles`` it came
    from vision's view of an opponent tile we've never confirmed — and since
    vision drift on dense boards can place a tile 1-3 cells off, the engine
    is happily building a play through a phantom letter that isn't actually
    where it thinks. Letter League rejects such plays at submission time.

    Filtering preference (vs hard rejection): even risky moves are useful as
    fallbacks if no safe move exists, so callers should *order* candidates
    safe-first rather than dropping risky ones outright.
    """
    for t in move.tiles_used:
        if not t.from_rack and (t.row, t.col) not in known_tiles:
            return False
    return True


def _build_candidates(
    moves: list,
    known_tiles: dict[tuple[int, int], str],
    difficulty_engine,
    cap: int = 5,
) -> list:
    """Order moves into a place-move candidate list, preferring safe over risky.

    Within each safety tier the order is: highest-quality pick (per
    ``difficulty_engine.select_move``) first, then frequency-ordered fallbacks.

    Why difficulty=50 (balanced score+frequency): Letter League's live word
    list is materially smaller than a Scrabble GADDAG — it routinely rejects
    valid English (CLIMBED, UPCLIMBED, PAVONINE, NEVOID, KNAP) while
    accepting their common-word neighbours. Empirical: a pure-score primary
    (difficulty=100) loses turns to dictionary rejections; a pure-freq
    primary (difficulty=0) lands at 70% but scores poorly because it picks
    BE/HO/AH over ITALICIZE/ZOUNDS. Difficulty 50 blends the two — common
    words still get a strong boost, but among similarly-common candidates
    the higher-scoring play wins, so big anchor extensions (ITALICIZE-class)
    can rise back to the top when their frequency is decent. The fallback
    is freq-sorted regardless, so even after the primary is rejected the
    next attempt is still a common-word fallback.

    The returned list never exceeds ``cap`` items; the placer tries them in
    order up to MAX_WORD_RETRIES.
    """
    if not moves:
        return []

    safe = [m for m in moves if _move_is_safe(m, known_tiles)]
    risky = [m for m in moves if not _move_is_safe(m, known_tiles)]

    def _tier(pool: list) -> list:
        if not pool:
            return []
        primary = difficulty_engine.select_move(pool, 50)
        fallback = sorted(
            (m for m in pool if m is not primary),
            key=lambda m: difficulty_engine.freq.normalized(m.word),
            reverse=True,
        )
        return [primary] + fallback

    out: list = []
    for tier in (_tier(safe), _tier(risky)):
        for m in tier:
            if len(out) >= cap:
                break
            out.append(m)
        if len(out) >= cap:
            break
    return out


def _is_iframe_dead_error(exc: BaseException) -> bool:
    """Return True if exc looks like the activity iframe is gone.

    Playwright surfaces lost-iframe errors as ``Locator.screenshot: Timeout``
    with a "waiting for locator(...iframe...)" call log, or as
    ``Element is not attached to the DOM``. We match on those substrings —
    any other vision/network failure should not trigger re-navigation.
    """
    msg = str(exc)
    return (
        "discordsays.com" in msg
        or "iframe" in msg.lower()
        or "Element is not attached to the DOM" in msg
        or ("Locator.screenshot" in msg and "Timeout" in msg)
    )


async def _run(max_turns: int, mode: str) -> int:
    from src.browser.capture import capture_canvas, invalidate_iframe_cache
    from src.browser.navigator import navigate_to_activity
    from src.browser.session import BrowserSession
    from src.browser.tile_placer import TilePlacer
    from src.browser.turn_detector import (
        IframeDeadError,
        ensure_game_started,
        poll_turn,
    )
    from src.difficulty import DifficultyEngine
    from src.engine import rejected_words
    from src.engine.gaddag import GADDAG
    from src.engine.moves import find_all_moves
    from src.vision import extract_board_state

    channel_url = os.getenv("DISCORD_CHANNEL_URL") or os.getenv("VOICE_CHANNEL_URL")
    if not channel_url:
        logger.error("DISCORD_CHANNEL_URL (or VOICE_CHANNEL_URL) not set in environment/.env")
        return 2

    wordlist_path = Path(os.getenv("WORDLIST_PATH", str(DEFAULT_WORDLIST)))
    gaddag_cache = Path(os.getenv("GADDAG_CACHE_PATH", str(DEFAULT_GADDAG_CACHE)))
    if not wordlist_path.exists():
        logger.error("Wordlist not found at {}", wordlist_path)
        return 2

    logger.info("Loading GADDAG from {} (cache: {})", wordlist_path, gaddag_cache)
    gaddag_cache.parent.mkdir(parents=True, exist_ok=True)
    gaddag = await asyncio.to_thread(GADDAG.from_wordlist, wordlist_path, gaddag_cache)
    difficulty_engine = DifficultyEngine()
    logger.info("Engine ready. Mode={}, max_turns={}", mode, max_turns)

    stop_event = asyncio.Event()

    def _handle_sigint() -> None:
        logger.warning("SIGINT received — requesting stop")
        stop_event.set()

    loop = asyncio.get_running_loop()
    try:
        loop.add_signal_handler(signal.SIGINT, _handle_sigint)
    except (NotImplementedError, RuntimeError):
        pass  # Windows + ProactorEventLoop doesn't support add_signal_handler on Python <3.8

    session = BrowserSession()
    turn_count = 0
    # Authoritative record of (row, col) -> letter for tiles the bot has
    # successfully placed. Built from accepted Move.tiles_used after each
    # turn LL confirms. Passed to extract_board_state so the vision pipeline
    # can detect drift (vision sees our known tiles offset by some (dr, dc))
    # and authoritatively pin our cells in place. Without this the engine
    # can spend turns generating "valid" plays against a phantom board state
    # that LL then rejects because the tiles aren't actually where vision
    # thought they were.
    known_tiles: dict[tuple[int, int], str] = {}
    try:
        page = await session.start()
        logger.info("Browser up — navigating to {}", channel_url)
        await navigate_to_activity(page, channel_url)
        await ensure_game_started(page)
        placer = TilePlacer(page)

        iframe_recoveries = 0
        MAX_IFRAME_RECOVERIES = 2

        async def _recover_iframe(reason: str) -> bool:
            """Re-navigate to the activity. Returns False if recovery cap is hit."""
            nonlocal iframe_recoveries
            iframe_recoveries += 1
            if iframe_recoveries > MAX_IFRAME_RECOVERIES:
                logger.error(
                    "Iframe dead {} times — giving up: {}", iframe_recoveries, reason
                )
                return False
            logger.warning(
                "Iframe dead ({}/{}) — re-navigating: {}",
                iframe_recoveries, MAX_IFRAME_RECOVERIES, reason,
            )
            invalidate_iframe_cache()
            await navigate_to_activity(page, channel_url)
            await ensure_game_started(page)
            return True

        while not stop_event.is_set():
            if max_turns > 0 and turn_count >= max_turns:
                logger.info("Reached max_turns={} — exiting cleanly", max_turns)
                return 0

            try:
                turn_state = await poll_turn(page, stop_event=stop_event)
            except IframeDeadError as exc:
                if not await _recover_iframe(str(exc)):
                    return 1
                continue
            if turn_state == "stop_requested":
                logger.info("Stop requested — exiting")
                return 0
            if turn_state == "game_over":
                logger.info("Game over after {} turns", turn_count)
                return 0
            if turn_state == "idle_timeout":
                logger.warning("Idle timeout — exiting")
                return 0

            # Clear any stale uncommitted tiles on the board before reading it.
            # On turn 1 (or after a crash/manual intervention) the game may
            # already have tiles staged — they would pollute the vision read
            # AND get submitted as part of our move, triggering rejections.
            await placer.clear_stale_placements()

            # Vision with one retry
            board = None
            rack: list[str] = []
            iframe_dead_during_vision: Exception | None = None
            for attempt in range(2):
                try:
                    img_bytes = await capture_canvas(page)
                    board, rack = await extract_board_state(
                        img_bytes, mode=mode, gaddag=gaddag,
                        known_tiles=known_tiles,
                    )
                    iframe_dead_during_vision = None
                    break
                except Exception as exc:
                    logger.warning("Vision attempt {} failed: {}", attempt + 1, exc)
                    if _is_iframe_dead_error(exc):
                        iframe_dead_during_vision = exc
                        # Don't burn another 60s on a second attempt against
                        # a known-dead iframe — bail to the recovery path.
                        break
            if board is None:
                if iframe_dead_during_vision is not None:
                    logger.error(
                        "Vision failed with iframe-dead error — re-navigating: {}",
                        iframe_dead_during_vision,
                    )
                    if not await _recover_iframe(str(iframe_dead_during_vision)):
                        return 1
                    continue
                logger.error("Vision failed twice — skipping turn")
                continue

            moves = await asyncio.to_thread(find_all_moves, board, rack, gaddag, mode)
            moves = rejected_words.filter_moves(moves)
            # Order candidates safe-first: a move that hooks only through our
            # known anchors (or is rack-only) won't be invalidated by vision
            # drift on opponent tiles. Risky moves (depending on unverified
            # opponent positions) are still in the list as fallbacks. Within
            # each tier the existing freq-then-score logic still applies — see
            # _build_candidates for details.
            candidates = await asyncio.to_thread(
                _build_candidates, moves, known_tiles, difficulty_engine,
            )

            turn_count += 1
            try:
                accepted = await placer.place_move(candidates, rack, swap_on_fail=False)
            except Exception as exc:
                logger.warning("place_move raised: {}", exc)
                if _is_iframe_dead_error(exc):
                    logger.error(
                        "place_move hit iframe-dead error — re-navigating: {}", exc,
                    )
                    if not await _recover_iframe(str(exc)):
                        return 1
                    continue
                accepted = None

            if not accepted:
                # Cover both "all candidates rejected" and "no candidates
                # produced" — the latter happens when vision sees stuck tiles
                # on the board and a near-empty rack, so find_all_moves yields
                # zero moves. Without a terminal action the game stays on
                # my_turn forever; swap_on_fail=True forces SWAP as the last
                # resort so the turn actually ends.
                logger.warning(
                    "No move accepted (candidates={}) — re-vision + swap fallback",
                    len(candidates),
                )
                try:
                    img_bytes = await capture_canvas(page)
                    board, rack = await extract_board_state(
                        img_bytes, mode=mode, gaddag=gaddag,
                        known_tiles=known_tiles,
                    )
                    moves = await asyncio.to_thread(find_all_moves, board, rack, gaddag, mode)
                    moves = rejected_words.filter_moves(moves)
                    candidates = await asyncio.to_thread(
                        _build_candidates, moves, known_tiles, difficulty_engine,
                    )
                    accepted = await placer.place_move(candidates, rack, swap_on_fail=True)
                except Exception as exc:
                    logger.warning("Re-vision retry failed: {}", exc)
                    if _is_iframe_dead_error(exc):
                        logger.error(
                            "Re-vision hit iframe-dead error — re-navigating: {}", exc,
                        )
                        if not await _recover_iframe(str(exc)):
                            return 1
                        continue

            if accepted:
                logger.info("Turn {}: played '{}' (score={})",
                            turn_count, accepted.word, accepted.score)
                # Record every tile in the accepted play as ground truth —
                # both the rack tiles we just placed and any board tiles the
                # word built on. LL accepting the move proves vision's read
                # of those positions agreed with reality, so they're safe to
                # treat as anchors for subsequent turns.
                for t in accepted.tiles_used:
                    known_tiles[(t.row, t.col)] = t.letter
                logger.debug(
                    "Known-tile anchor set now {} tile(s)", len(known_tiles),
                )
            else:
                logger.info("Turn {}: no move accepted (swap/skip)", turn_count)

        return 0
    finally:
        try:
            await asyncio.wait_for(session.close(), timeout=5.0)
        except (Exception, asyncio.TimeoutError):
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Headless Letter League autoplay")
    parser.add_argument("--max-turns", type=int, default=0,
                        help="Exit cleanly after this many turns (0 = unlimited)")
    parser.add_argument("--mode", choices=("wild", "classic"), default="wild")
    args = parser.parse_args()

    _configure_logging()
    load_dotenv()

    start = time.monotonic()
    try:
        code = asyncio.run(_run(args.max_turns, args.mode))
    except KeyboardInterrupt:
        logger.warning("Interrupted — exiting")
        return 130
    except Exception:
        logger.exception("Headless autoplay crashed")
        return 1
    finally:
        logger.info("Headless autoplay finished in {:.1f}s", time.monotonic() - start)
    return code


if __name__ == "__main__":
    sys.exit(main())
