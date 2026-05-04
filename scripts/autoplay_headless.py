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
                    board, rack = await extract_board_state(img_bytes, mode=mode, gaddag=gaddag)
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
            if moves:
                selected = await asyncio.to_thread(
                    difficulty_engine.select_move, moves, 100,
                )
                candidates = [selected]
                for m in moves:
                    if m is not selected and len(candidates) < 5:
                        candidates.append(m)
            else:
                candidates = []

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
                    board, rack = await extract_board_state(img_bytes, mode=mode, gaddag=gaddag)
                    moves = await asyncio.to_thread(find_all_moves, board, rack, gaddag, mode)
                    moves = rejected_words.filter_moves(moves)
                    if moves:
                        selected = await asyncio.to_thread(
                            difficulty_engine.select_move, moves, 100,
                        )
                        candidates = [selected] + [m for m in moves if m is not selected][:4]
                    else:
                        candidates = []
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
