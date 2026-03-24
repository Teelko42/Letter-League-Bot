---
phase: 01-word-engine
plan: 04
subsystem: engine
tags: [move-generation, gaddag, algorithm, gordon-1994, blank-tiles, cross-checks, tdd, python]

# Dependency graph
requires:
  - phase: 01-word-engine/01-01
    provides: GADDAG data structure with SEPARATOR/TERMINAL markers, dict-based node graph
  - phase: 01-word-engine/01-02
    provides: Board with find_anchors, compute_cross_checks, compute_left_limit, place_tile
  - phase: 01-word-engine/01-03
    provides: score_move/score_word for Classic and Wild mode scoring of candidate moves

provides:
  - find_all_moves(): Gordon (1994) LeftPart/ExtendRight algorithm returning all valid placements
  - Blank tile handling with GADDAG-arc pruning (not blind 26-letter iteration)
  - Cross-check enforcement for perpendicular word validity
  - Move deduplication by (word, start_row, start_col, direction)
  - Moves ranked by score descending (WENG-05: first move is optimal)
  - GameEngine: stateful public API (find_moves, best_move, play_move, is_valid_word)
  - Multi-turn game state via play_move() updating board between turns
  - Classic and Wild mode support throughout full pipeline

affects:
  - Phase 2 (difficulty system — consumes GameEngine.find_moves and Move.score)
  - Phase 4 (Discord integration — consumes GameEngine as primary API)
  - All downstream phases that need word engine capabilities

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Gordon (1994) LeftPart/ExtendRight GADDAG traversal
    - Placed-position threading through recursive calls (left_placed + right_placed)
    - In-place rack mutation with pop/insert for O(1) backtracking
    - Blank tile GADDAG-arc pruning: iterate node.keys() not ALPHABET
    - TDD with RED/GREEN commits

key-files:
  created:
    - src/engine/moves.py
    - src/engine/__init__.py
    - tests/test_moves.py
    - tests/test_engine.py
  modified: []

key-decisions:
  - "Left-part placed positions threaded through _left_part and _extend_right as left_placed + right_placed — enables accurate start-position calculation in _build_move without board mutation"
  - "Blank tiles try only GADDAG-arc letters at current node (not all 26) — correctness + efficiency"
  - "_extend_right splits into public wrapper and _extend_right_inner to carry both left_placed and right_placed without changing the public signature"
  - "GameEngine wraps GADDAG+Board+find_all_moves — clean stateful API for downstream phases"
  - "play_move() only places from_rack=True tiles — existing board tiles unchanged"

patterns-established:
  - "Move generation is pure: board is never mutated during generation (temporary Cells for scoring)"
  - "Rack copy per anchor branch (list(rack)) isolates backtracking between anchor explorations"
  - "All 72 tests pass as the acceptance gate for Phase 1 completion"

requirements-completed: [WENG-02, WENG-05]

# Metrics
duration: 20min
completed: 2026-03-24
---

# Phase 1 Plan 04: Move Generation + GameEngine Summary

**Gordon (1994) LeftPart/ExtendRight move generation with blank-tile GADDAG pruning, cross-check enforcement, deduplication, score-ranked output, and stateful GameEngine public API**

## Performance

- **Duration:** ~20 min
- **Started:** 2026-03-24T02:06:26Z
- **Completed:** 2026-03-24T02:26:00Z
- **Tasks:** 2 (Task 1: moves.py TDD, Task 2: GameEngine + integration tests)
- **Files modified:** 4

## Accomplishments

- Implemented complete Gordon (1994) algorithm: LeftPart builds reversed-prefix by traversing GADDAG arcs left of anchor; ExtendRight places tiles rightward respecting cross-checks
- Blank tile ('_') optimization: at each GADDAG node, only tries letters with outgoing arcs (not all 26) — correctness + pruning in one step
- Tracked left-part and right-part placed positions separately and combined them in `_build_move` — solves accurate start-position calculation without board mutation
- GameEngine provides clean stateful API: `find_moves`, `best_move`, `play_move`, `is_valid_word`, `is_first_turn` — zero board coupling for callers
- 72 total tests passing across all modules (GADDAG, Board, Scoring, Moves, Engine)

## Task Commits

1. **Task 1 (RED): Failing move generation tests** — `fd13109` (test)
2. **Task 1 (GREEN): LeftPart/ExtendRight implementation** — `7ba59c4` (feat)
3. **Task 2: GameEngine + integration tests** — `0d16101` (feat)

**Plan metadata:** _(docs commit follows)_

## Files Created/Modified

- `src/engine/moves.py` — Gordon (1994) move generation: find_all_moves, LeftPart, ExtendRight, perpendicular gathering, deduplication; 633 lines
- `src/engine/__init__.py` — GameEngine public API class with stateful board management; 138 lines
- `tests/test_moves.py` — 12 move generation tests: empty board, extensions, prefix extension, cross-check validation, blank tiles, GADDAG pruning, no-moves, deduplication, sorting, rack tracking, perpendicular scoring; 254 lines
- `tests/test_engine.py` — 9 integration tests: init, word validation, find moves, best move, no moves, play move, second turn, multi-turn, Classic vs Wild; 247 lines

## Decisions Made

- **Placed-position threading**: Left-part rack tiles need their board positions tracked to correctly determine the start position of the word in `_build_move`. Threaded `left_placed` through `_left_part` into `_extend_right`, then combined with `right_placed` in `_build_move`. This keeps the board unmodified during generation (pure exploratory traversal).

- **_extend_right_inner pattern**: Public `_extend_right` wrapper takes `left_placed` and calls `_extend_right_inner` with `right_placed=[]` — keeps the public call signature clean while allowing inner recursion to carry both lists.

- **Rack copy per anchor**: Each anchor's exploration gets `list(rack)` — isolates backtracking between anchors. Within a single anchor's LeftPart/ExtendRight recursion, the rack is mutated in-place for efficiency.

- **Blank tile uses `list(node.keys())`**: At each GADDAG node, blank tries only keys that aren't SEPARATOR or TERMINAL. This is both correct (only valid continuations) and efficient (pruned from 26 to typically 3-8 options per node).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Restructured placed-position tracking to fix IndexError on board boundary**

- **Found during:** Task 1 initial implementation (first test run)
- **Issue:** First version of `_extend_right` only tracked `right_placed` (right-extension rack tiles) but `_build_move` tried to iterate `word_len` steps from the start position computed from those tiles only. Left-part letters contributed to `word` length but had no corresponding position entries, causing the iteration to go past board bounds (e.g., Cell (3,7) on a 7x7 board).
- **Fix:** Added `left_placed` parameter to `_left_part` tracking positions of left-part tiles as they're placed (computing position from anchor offset). Split `_extend_right` into public wrapper + `_extend_right_inner` carrying both `left_placed` and `right_placed`. `_build_move` receives both and combines them for accurate start-position and word iteration.
- **Files modified:** `src/engine/moves.py`
- **Verification:** All 12 move generation tests pass after fix
- **Committed in:** `7ba59c4` (part of GREEN commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 — Bug)
**Impact on plan:** Essential correctness fix. No scope creep. The architectural separation of left/right placed positions is actually cleaner than a single flat list.

## Issues Encountered

- Initial `_extend_right` implementation didn't track left-part tile positions, causing `_build_move` to iterate beyond board boundaries. Fixed by threading `left_placed` through the call chain and computing left-part positions from the anchor offset during `_left_part` recursion.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- `GameEngine` is fully functional: load wordlist, find all moves, rank by score, play moves, multi-turn support in Classic and Wild modes
- `find_all_moves` ready for consumption by Phase 2 (difficulty system) — returns moves with full `ScoreBreakdown` including perpendicular scores
- Phase 1 (Word Engine) is 100% complete: all 5 requirements (WENG-01 through WENG-05) covered
- No blockers for Phase 2

## Self-Check: PASSED

- `src/engine/moves.py` - FOUND
- `src/engine/__init__.py` - FOUND
- `tests/test_moves.py` - FOUND
- `tests/test_engine.py` - FOUND
- Commit `fd13109` (test RED) - FOUND
- Commit `7ba59c4` (feat GREEN moves) - FOUND
- Commit `0d16101` (feat engine) - FOUND
- All 72 tests pass: `72 passed in 0.74s`

---
*Phase: 01-word-engine*
*Completed: 2026-03-24*
