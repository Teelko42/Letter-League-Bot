---
phase: 01-word-engine
plan: 03
subsystem: engine
tags: [scoring, classic-mode, wild-mode, bingo, multipliers, tdd, python]

# Dependency graph
requires:
  - phase: 01-word-engine/01-01
    provides: Cell, MultiplierType, ScoreBreakdown data models and TILE_VALUES

provides:
  - score_word(): pure function scoring a single word in Classic or Wild mode
  - score_move(): full move scorer including perp words, bingo, and ScoreBreakdown
  - Classic mode: multipliers apply only to newly placed tiles on placement turn
  - Wild mode: bonded multipliers apply to all tiles in word every turn (permanent)
  - Bingo bonus (x2 main word) when all rack tiles consumed

affects:
  - 01-04 (move generation — uses score_move to rank candidate moves)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Pure function scoring — accepts cells and positions as parameters, no Board dependency
    - Mode-parametric scoring — single score_word handles both Classic and Wild via mode argument
    - TDD with RED/GREEN/REFACTOR commits

key-files:
  created:
    - src/engine/scoring.py
    - tests/test_scoring.py
  modified: []

key-decisions:
  - "score_word/score_move accept cells+positions as params, not Board — keeps scoring pure and testable"
  - "Wild mode uses bonded_multiplier (set by Board.place_tile), Classic uses square_multiplier filtered by newly_placed_positions"
  - "Wild stacking is multiplicative: DW+DW=x4, TW+DW=x6 (per research recommendation for open question #1)"
  - "Bingo multiplier applied to main word only — Letter League rule, NOT Scrabble +50"
  - "Blank tiles: always 0 pts, even with bonded DL/TL in Wild mode (0 * multiplier = 0)"

patterns-established:
  - "Scoring is stateless: all needed state passed as arguments, no globals or Board references"
  - "score_word returns (letter_sum, word_multiplier) tuple — caller controls how to combine"
  - "Perpendicular words each scored independently via score_word, then summed in score_move"

requirements-completed: [WENG-03, WENG-04]

# Metrics
duration: 8min
completed: 2026-03-24
---

# Phase 1 Plan 03: Scoring Engine Summary

**Classic and Wild mode scoring engine with mode-parametric multiplier logic, multiplicative Wild stacking, Letter League bingo bonus, and independent perpendicular word scoring**

## Performance

- **Duration:** ~8 min
- **Started:** 2026-03-24T01:54:00Z
- **Completed:** 2026-03-24T02:02:56Z
- **Tasks:** 2 (Task 1: Classic TDD, Task 2: Wild TDD)
- **Files modified:** 2

## Accomplishments

- Implemented `score_word()` — pure function scoring a single word with full Classic/Wild multiplier semantics
- Implemented `score_move()` — complete move scorer: main word, perpendicular words, bingo bonus, ScoreBreakdown
- 22 tests covering all multiplier combinations, blank tiles, bingo, perpendicular scoring, and Classic vs Wild distinction
- Full TDD cycle: failing tests committed first, then implementation to green

## Task Commits

Each task was committed atomically:

1. **Task 1 (RED): Classic and Wild failing tests** - `bac4a28` (test)
2. **Task 2 (GREEN): Scoring implementation** - `bcffead` (feat)

**Plan metadata:** _(docs commit follows)_

_Note: Tasks 1 and 2 shared files — tests written first (RED), implementation added to pass all 22 tests (GREEN)_

## Files Created/Modified

- `src/engine/scoring.py` — scoring engine with `score_word()` and `score_move()`; 149 lines
- `tests/test_scoring.py` — 22 tests across Classic and Wild modes; 270 lines

## Decisions Made

- **Pure function design**: `score_word` and `score_move` accept `cells` + `newly_placed_positions` as parameters — no Board import, fully testable in isolation without board dependency
- **Wild uses `bonded_multiplier`**: Classic reads `cell.square_multiplier` filtered by `newly_placed_positions`; Wild reads `cell.bonded_multiplier` for all cells. This cleanly separates the two modes
- **Multiplicative stacking for Wild**: DW+DW=x4, TW+DW=x6. Mirrors research recommendation (open question #1 resolution)
- **Bingo fires on `tiles_from_rack == rack_size`**: rack-size-agnostic, works for any rack size (7 default, 4, etc.)

## Deviations from Plan

None - plan executed exactly as written. Both tasks (Classic TDD, Wild TDD) were implemented in a single coherent pass since the implementation naturally covered both modes together. All 22 tests pass, all plan truths verified.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `score_move()` is ready for consumption by Plan 04 (move generation) to rank candidate moves
- `score_word()` can be used independently if perpendicular word scoring needs isolated testing
- No blockers for 01-04

## Self-Check: PASSED

- `src/engine/scoring.py` - FOUND
- `tests/test_scoring.py` - FOUND
- `.planning/phases/01-word-engine/01-03-SUMMARY.md` - FOUND
- Commit `bac4a28` (test RED) - FOUND
- Commit `bcffead` (feat GREEN) - FOUND
- All 22 tests pass

---
*Phase: 01-word-engine*
*Completed: 2026-03-24*
