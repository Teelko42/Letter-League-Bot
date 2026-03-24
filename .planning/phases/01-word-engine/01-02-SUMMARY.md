---
phase: 01-word-engine
plan: 02
subsystem: engine
tags: [board, python, tdd, anchors, cross-checks, left-limits, move-generation, precomputation]

# Dependency graph
requires:
  - phase: 01-01
    provides: "Cell and MultiplierType dataclasses from models.py; GADDAG.is_valid_word() for cross-check validation"
provides:
  - "Board class: configurable grid (default 19x27) with multiplier layout, classic/wild tile placement"
  - "find_anchors(): direction-independent anchor square detection, center anchor on empty board"
  - "compute_cross_checks(): direction-dependent cross-check letter sets using GADDAG validation"
  - "_gather_perpendicular(): helper to collect contiguous perpendicular tiles for cross-check formation"
  - "compute_left_limit(): LeftPart algorithm left-extent constraint capped at rack_size-1"
affects:
  - 01-03-scoring
  - 01-04-move-gen

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Anchor-based move generation preparation: empty cells adjacent to occupied cells are anchors"
    - "Direction-dependent cross-checks: H validates vertical perps (gather up/down), V validates horizontal perps (gather left/right)"
    - "Left-limit cap: min(empty cells before anchor, rack_size - 1) — prevents LeftPart over-extension"

key-files:
  created:
    - src/engine/board.py
    - tests/test_board.py
  modified: []

key-decisions:
  - "Anchors are direction-independent: same set for H and V — direction parameter exists for API consistency only"
  - "Cross-checks are direction-dependent: H cross-checks validate vertical perpendicular words; V validates horizontal"
  - "TYPE_CHECKING guard for GADDAG import in board.py: avoids circular import; runtime uses string annotation"
  - "left_limit returns 0 immediately if adjacent cell is occupied: existing tile chain is a forced prefix, not an extension opportunity"

patterns-established:
  - "Board methods accept direction parameter for API uniformity even when not used (find_anchors)"
  - "Perpendicular word formed as prefix + candidate_letter + suffix; validated with gaddag.is_valid_word()"

requirements-completed:
  - WENG-02

# Metrics
duration: 2min
completed: 2026-03-24
---

# Phase 1 Plan 02: Board State and Precomputation Summary

**Board class with configurable 19x27 grid, classic/wild tile placement, anchor square detection, direction-dependent GADDAG-backed cross-check sets, and LeftPart left-limit computation — all verified with 20 TDD tests**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-03-24T02:00:37Z
- **Completed:** 2026-03-24T02:02:51Z
- **Tasks:** 2
- **Files modified:** 2 created

## Accomplishments

- Board initializes as a configurable grid (default 19x27) with multiplier layout dict — no hardcoded positions; layout provided as configuration per CONTEXT.md spec
- Tile placement supports classic mode (no bonding) and wild mode (bonds the square multiplier permanently to the tile for future scoring turns)
- Anchor squares correctly identified as empty cells adjacent to occupied cells; empty board returns center cell as the sole synthetic anchor for the first move
- Cross-check sets computed per empty cell using GADDAG validation — H mode gathers tiles above/below (validates vertical perps), V mode gathers tiles left/right (validates horizontal perps); cells with no perpendicular tiles receive the full 26-letter set
- Left-limit computation for LeftPart algorithm: scans before anchor, stops at occupied cell (returns 0 immediately), capped at rack_size - 1

## Task Commits

Each task was committed atomically:

1. **Task 1: Board state management and tile placement (TDD)** - `ab67542` (feat)
2. **Task 2: Anchor squares, cross-checks, and left-limit precomputation** - `ab67542` (feat — included in same commit as full Board class implementation)

**Plan metadata:** _(this commit)_

_Note: Tasks 1 and 2 were implemented together in board.py as a single cohesive class. Tests for both tasks were written first (RED), then the full implementation was committed GREEN. Both task done-criteria verified before commit._

## Files Created/Modified

- `src/engine/board.py` - Board class: grid initialization, get_cell/place_tile/is_empty/center, find_anchors, compute_cross_checks, _gather_perpendicular, compute_left_limit
- `tests/test_board.py` - 20 TDD tests: 9 board state tests (Task 1) + 11 precomputation tests (Task 2)

## Decisions Made

- **Anchors are direction-independent:** The plan specifies "direction parameter exists for API consistency" — find_anchors returns the same set regardless of 'H' or 'V'. Confirmed by test_anchors_direction_independent.
- **TYPE_CHECKING guard for GADDAG import:** board.py uses `if TYPE_CHECKING` to import GADDAG and a string annotation at runtime, avoiding circular imports (gaddag.py does not import board.py, but keeping the pattern consistent with the project).
- **left_limit returns 0 on adjacent occupied cell:** When scanning left and immediately hitting an occupied tile, there is zero room for LeftPart extension — the existing tiles form a forced prefix handled separately by move generation. Returning 0 early is both correct and efficient.

## Deviations from Plan

None — plan executed exactly as written.

The plan specified separate RED→GREEN cycles for Tasks 1 and 2. Both tasks were written as failing tests first (confirmed by import error on missing board.py), then board.py was implemented with all methods. Since tasks share a single file and the implementation is cohesive, a single implementation commit is appropriate and matches the plan's `files_modified` list.

## Issues Encountered

- Python is not on PATH on this Windows machine; used full path `/c/Users/Ninja/AppData/Local/Programs/Python/Python310/python.exe` for all test runs. This matches the known environment from plan 01-01 and does not affect the engine code.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Board is ready for consumption by plan 01-03 (scoring) and plan 01-04 (move generation)
- compute_cross_checks requires a GADDAG instance — plan 01-04 will call this during move generation setup
- No blockers for plan 01-03 (scoring engine)

## Self-Check: PASSED

- FOUND: src/engine/board.py
- FOUND: tests/test_board.py
- FOUND: .planning/phases/01-word-engine/01-02-SUMMARY.md
- FOUND: commit ab67542
- 20/20 tests passing

---
*Phase: 01-word-engine*
*Completed: 2026-03-24*
