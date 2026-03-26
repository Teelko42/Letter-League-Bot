---
phase: 07-tile-placement
plan: 02
subsystem: browser
tags: [patchright, tile-placement, acceptance-detection, retry-logic, tile-swap]

# Dependency graph
requires:
  - phase: 07-tile-placement-01
    provides: TilePlacer.place_tiles(), CoordMapper, PlacementError
  - phase: 06-turn-detection
    provides: classify_frame() for post-confirm acceptance detection

provides:
  - TilePlacer.place_move() — full public API: tiles -> confirm -> verify -> retry -> tile swap
  - TilePlacer._click_confirm() — teleport-click confirm button with jitter
  - TilePlacer._wait_for_acceptance() — 1-2s wait + classify_frame() acceptance check
  - TilePlacer._recall_tiles() — click recall/undo to return tiles to rack
  - TilePlacer._tile_swap() — tile swap fallback with warning log
  - CoordMapper.recall_btn_px() / swap_btn_px() — fractional coordinate helpers
  - TilePlacer and PlacementError exported from src.browser package

affects:
  - 08-orchestration (place_move() is the single call in the autonomous play loop)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "classify_frame() reused from Phase 6 for post-confirm turn-state detection — no new vision logic"
    - "Retry loop iterates moves[:MAX_WORD_RETRIES] — caller provides sorted move list, Plan 02 does not call engine"
    - "PlacementError caught per-move in place_move() — recall attempted, then continue to next candidate"
    - "Tile swap fallback after MAX_WORD_RETRIES=3 failures — sacrifices turn rather than blocking"

key-files:
  created: []
  modified:
    - src/browser/tile_placer.py
    - src/browser/__init__.py

key-decisions:
  - "place_move() receives list[Move] sorted best-first from caller — no engine coupling inside placer"
  - "Acceptance check reuses classify_frame() from Phase 6 — any state != my_turn means turn ended"
  - "MAX_WORD_RETRIES=3 before tile swap — balances retry cost vs turn loss"
  - "PlacementError caught per-attempt: recall attempted, then continue; final fallback is tile swap"

requirements-completed: [TILE-03]

# Metrics
duration: 2min
completed: 2026-03-26
---

# Phase 7 Plan 02: Tile Placement — Confirmation, Retry, and Tile Swap Summary

**Full placement pipeline: confirm button click, classify_frame()-based acceptance detection, per-word retry loop (up to 3 attempts), and tile swap fallback when all words fail**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-03-26T17:56:36Z
- **Completed:** 2026-03-26T17:58:33Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- `TilePlacer.place_move(moves, rack)` is the single public API for the autonomous play loop: drags tiles, clicks confirm, waits 1-2s, checks acceptance via `classify_frame()`, recalls on rejection, retries up to `MAX_WORD_RETRIES=3` times, then falls back to tile swap
- `TilePlacer._click_confirm()` clicks the confirm button with jitter using `page.mouse.click` (teleport, not drag — correct for button clicks)
- `TilePlacer._wait_for_acceptance()` waits `random.uniform(1.0, 2.0)` seconds then calls `classify_frame()` — returns True if state is not "my_turn" (turn ended = accepted), False if still "my_turn" (rejected)
- `TilePlacer._recall_tiles()` clicks the recall/undo button and waits `random.uniform(0.5, 1.0)` for animation
- `TilePlacer._tile_swap()` clicks the tile swap button as a last resort, logging a warning
- `CoordMapper` extended with `recall_btn_px()` and `swap_btn_px()` using `RECALL_X/Y_FRAC` and `SWAP_X/Y_FRAC` placeholder constants
- `TilePlacer` and `PlacementError` added to `src/browser/__init__.py` package exports
- `tile_placer.py` grows from 246 lines (Plan 01) to 578 lines — well above `min_lines: 250`

## Task Commits

Each task was committed atomically:

1. **Task 1: Add confirm, acceptance detection, retry loop, and tile swap to TilePlacer** - `7435a49` (feat)
2. **Task 2: Update browser package exports** - `c6e388f` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified

- `src/browser/tile_placer.py` — Extended with 5 new methods + 4 new constants + 2 new CoordMapper methods (578 lines total)
- `src/browser/__init__.py` — Added TilePlacer and PlacementError imports and __all__ entries

## Decisions Made

- `place_move()` receives `list[Move]` sorted best-first from caller — no engine coupling inside the placer; this keeps concerns separated
- Acceptance check reuses `classify_frame()` from Phase 6 — any state != "my_turn" means turn ended (accepted or game over both count as non-rejection)
- `MAX_WORD_RETRIES=3` before tile swap — balances turn efficiency (trying best words) vs not looping forever
- `PlacementError` caught per-attempt inside `place_move()`: recall attempted after drag failure, then continue to next candidate; final fallback is tile swap rather than raising

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None — all verification checks passed on first attempt.

## Self-Check: PASSED

- `src/browser/tile_placer.py` — FOUND (578 lines, > 250 minimum)
- `src/browser/__init__.py` — FOUND (contains TilePlacer import)
- Commit `7435a49` — FOUND (Task 1)
- Commit `c6e388f` — FOUND (Task 2)
- All 4 verification checks passed: package exports, TilePlacer methods, CoordMapper methods, existing exports

---
*Phase: 07-tile-placement*
*Completed: 2026-03-26*
