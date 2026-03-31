---
phase: 08-autonomous-game-loop
plan: 02
subsystem: bot
tags: [discord, cog, asyncio, browser, game-loop, pytest, mocking]

requires:
  - phase: 08-autonomous-game-loop
    plan: 01
    provides: "AutoPlayPhase, LoopState, build_turn_embed, build_swap_embed, build_gameover_embed"
  - phase: 05-browser-foundation
    provides: "BrowserSession, navigate_to_activity, capture_canvas"
  - phase: 06-turn-detection
    provides: "poll_turn, preflight_check, classify_frame"
  - phase: 07-tile-placement
    provides: "TilePlacer, PlacementError"
  - phase: 03-vision-pipeline
    provides: "extract_board_state"
  - phase: 01-word-engine
    provides: "find_all_moves, Move"

provides:
  - "AutoPlayCog with /autoplay start|stop|status slash commands via app_commands.Group"
  - "Autonomous game loop as asyncio.create_task (non-blocking discord.py event loop)"
  - "Vision pipeline retry (once) then skip-cycle on second failure"
  - "_attempt_reconnect with 3 attempts and 5/15/30s exponential backoff"
  - "Browser crash recovery via BrowserSession relaunch"
  - "Tile swap fallback when find_all_moves returns empty list"
  - "cog_unload cancels orphaned loop tasks"
  - "AutoPlayCog registered in bot.py setup_hook"

affects:
  - "Phase 08 complete — bot can play Letter League games end-to-end autonomously"

tech-stack:
  added:
    - pytest-asyncio 1.3.0 (async test support)
  patterns:
    - "app_commands.Group subcommands: /autoplay start|stop|status as group children"
    - "asyncio.create_task for non-blocking game loop on discord.py's event loop"
    - "asyncio.to_thread for CPU-bound find_all_moves and select_move offloading"
    - "Exponential backoff reconnection with RECONNECT_DELAYS = [5, 15, 30]"
    - "TDD: test callbacks via app_commands.Command.callback (not direct invocation)"
    - "State pre-initialization pattern for loop tests: set cog._state before _run_game_loop"

key-files:
  created:
    - src/bot/autoplay_cog.py
    - tests/test_autoplay_cog.py
  modified:
    - src/bot/bot.py

key-decisions:
  - "Access slash command handlers in tests via command.callback(cog, interaction) — app_commands.Command wraps the method and is not directly callable"
  - "Tests that call _run_game_loop directly must pre-set cog._state — normally set by autoplay_start before task creation"
  - "Game loop assert self._state is not None guards against misuse; loop callers must initialize state first"
  - "find_all_moves uses asyncio.to_thread (CPU-bound GADDAG search); select_move also offloaded the same way"
  - "RECONNECT_DELAYS = [5, 15, 30] — three attempts with increasing backoff before RuntimeError"

requirements-completed:
  - LOOP-01
  - LOOP-02
  - LOOP-03
  - LOOP-04
  - BROW-03

duration: 5min
completed: 2026-03-31
---

# Phase 8 Plan 02: AutoPlayCog — Autonomous Game Loop Summary

**AutoPlayCog wiring all Phase 5-7 subsystems into a self-sustaining Discord-controlled game loop: /autoplay start|stop|status commands, async task-based loop, reconnection resilience, and 11 unit tests with fully mocked browser/vision/engine subsystems**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-03-31T22:28:19Z
- **Completed:** 2026-03-31T22:33:15Z
- **Tasks:** 2
- **Files modified:** 3 (2 created, 1 modified, 1 test created)

## Accomplishments

- Created `src/bot/autoplay_cog.py` — full AutoPlayCog with:
  - `/autoplay start`: launches BrowserSession, navigates to activity, spawns game loop task
  - `/autoplay stop`: signals stop event, transitions to STOPPING phase
  - `/autoplay status`: reports phase, turn count, and formatted uptime
  - `_run_game_loop`: async task with poll_turn → capture → vision → move gen → place → embed cycle
  - `_attempt_reconnect`: 3 retries with 5/15/30s backoff
  - `cog_unload`: cancels orphaned task on bot reload/shutdown
- Updated `src/bot/bot.py` — `AutoPlayCog` registered in `setup_hook` after `AdvisorCog`
- Created `tests/test_autoplay_cog.py` — 11 unit tests covering all cog behaviors with mocked subsystems

## Task Commits

Each task was committed atomically:

1. **Task 1: Build AutoPlayCog with game loop, reconnection, and slash commands** — `33ca777` (feat)
2. **Task 2: Unit tests for AutoPlayCog with mocked subsystems** — `542008c` (test)

## Files Created/Modified

- `src/bot/autoplay_cog.py` — AutoPlayCog (236 lines): commands, loop, reconnection, cleanup
- `src/bot/bot.py` — Added AutoPlayCog registration in setup_hook
- `tests/test_autoplay_cog.py` — 11 tests: guard logic, task creation, stop/status, swap, reconnect, game-over, vision retry, cog unload

## Decisions Made

- `app_commands.Command` wraps slash handlers and is not directly callable — tests access `command.callback(cog, interaction)` to invoke the handler
- Tests calling `_run_game_loop` directly must pre-initialize `cog._state` — mirrors what `autoplay_start` does before task creation
- `find_all_moves` and `select_move` both wrapped in `asyncio.to_thread` — both are CPU-bound and must not block discord.py's event loop
- `RECONNECT_DELAYS = [5, 15, 30]` (3 attempts with backoff) as specified in BROW-03

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 2 - Missing Critical Functionality] Pre-set cog._state for loop tests**
- **Found during:** Task 2 (test_swap_on_no_moves, test_game_over_stops_loop, test_vision_retry_then_skip)
- **Issue:** `_run_game_loop` contains `assert self._state is not None` — normally set by `autoplay_start` before task creation. Tests calling the loop coroutine directly failed this assertion.
- **Fix:** Added `cog._state = LoopState(phase=AutoPlayPhase.STARTING, channel_id=42)` setup in each loop test before calling `_run_game_loop`. This correctly mirrors the production call sequence.
- **Files modified:** tests/test_autoplay_cog.py

**2. [Rule 1 - Bug] Use command.callback() for slash command tests**
- **Found during:** Task 2 (test_start_guard — first test run)
- **Issue:** Calling `await cog.autoplay_start(interaction)` raised `TypeError: 'Command' object is not callable` — discord.py wraps decorated methods in an `app_commands.Command` object.
- **Fix:** All slash command invocations changed to `await cog.autoplay_start.callback(cog, interaction)` pattern. This is the correct way to test app_commands handlers without going through discord.py's full dispatch machinery.
- **Files modified:** tests/test_autoplay_cog.py

## User Setup Required

The `VOICE_CHANNEL_URL` environment variable must be set before invoking `/autoplay start`. The bot reads it at command time and errors clearly if missing:

```
VOICE_CHANNEL_URL=https://discord.com/channels/SERVER_ID/CHANNEL_ID
```

## Issues Encountered

- pytest-asyncio not installed — installed via pip before running tests. No code changes required.

## Next Phase Readiness

- Phase 8 is complete. The bot now has full autonomous play capability end-to-end.
- All 124 project tests pass.

---
*Phase: 08-autonomous-game-loop*
*Completed: 2026-03-31*

## Self-Check: PASSED

- FOUND: src/bot/autoplay_cog.py
- FOUND: src/bot/bot.py (updated)
- FOUND: tests/test_autoplay_cog.py
- FOUND: .planning/phases/08-autonomous-game-loop/08-02-SUMMARY.md
