---
phase: 07-tile-placement
plan: 01
subsystem: browser
tags: [patchright, opencv, drag-and-drop, coordinate-mapping, calibration]

# Dependency graph
requires:
  - phase: 05-browser-foundation
    provides: patchright Page object and canvas iframe capture pipeline
  - phase: 06-turn-detection
    provides: capture_canvas() for per-tile verification screenshots
  - phase: 01-word-engine
    provides: Move and TileUse dataclasses for tile placement orchestration

provides:
  - CoordMapper class mapping board cell (row,col) and rack slot indices to viewport pixels via fractional constants
  - TilePlacer class executing drag-and-drop placements with per-tile pixel-diff verification and retry
  - assign_rack_indices() for leftmost-duplicate rack slot matching with blank tile ('?') support
  - jitter() helper adding +/-3px human-like noise to drag coordinates
  - PlacementError exception for all placement failure cases
  - scripts/calibrate_placement.py interactive tool for measuring fractional constants from live screenshots

affects:
  - 07-tile-placement-02 (confirmation, rejection recovery, retry logic built on TilePlacer)
  - 08-orchestration (TilePlacer.place_tiles() is the core action in the play loop)

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Fractional constants (FRAC suffix) for all pixel coordinates — resolution-independent, calibratable from any screenshot"
    - "TYPE_CHECKING guard for Move/TileUse imports — avoids circular imports at runtime"
    - "Local import of capture_canvas inside methods to avoid circular reference (same pattern as turn_detector.py)"
    - "Greedy left-to-right rack slot consumption via None-sentinel mutation of working copy"

key-files:
  created:
    - src/browser/tile_placer.py
    - scripts/calibrate_placement.py
  modified: []

key-decisions:
  - "All pixel coordinates expressed as fractions of canvas width/height — operator calibrates once from a live screenshot via calibrate_placement.py, then hardcodes constants in tile_placer.py"
  - "Pixel-diff threshold of 1.0 mean absolute difference for placement verification — conservative enough to detect any tile landing while ignoring render noise"
  - "One retry on placement failure before raising PlacementError — keeps automation moving without infinite loops"
  - "Human-like inter-tile delay of 1-3s (random.uniform) between placements — matches observed human pacing"
  - "Sort rack tiles by col (H) or row (V) before dragging — ensures word spells left-to-right / top-to-bottom as the game expects"

patterns-established:
  - "Fractional constants pattern: all UI coordinates as FRAC suffix floats multiplied by bbox width/height at call time"
  - "CoordMapper.board_cell_px/rack_tile_px: all coordinate math in one class, consumed by TilePlacer for testability"

requirements-completed: [TILE-01, TILE-02]

# Metrics
duration: 3min
completed: 2026-03-26
---

# Phase 7 Plan 01: Tile Placement — CoordMapper and TilePlacer Summary

**Resolution-independent drag-and-drop tile placement via fractional coordinate mapping, per-tile pixel-diff verification, and an interactive calibration script for measuring live game constants**

## Performance

- **Duration:** ~3 min
- **Started:** 2026-03-26T17:51:19Z
- **Completed:** 2026-03-26T17:54:04Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- CoordMapper translates board cell (row, col) and rack slot indices into viewport pixel coordinates using fractional constants relative to the canvas bounding box — works at any resolution
- TilePlacer orchestrates full drag-and-drop sequences: jittered source/target coordinates, per-tile before/after screenshot pixel-diff verification, one retry on failure, 1-3s human-like delays
- assign_rack_indices() greedily maps rack tiles to leftmost available slots with blank tile '?' support
- calibrate_placement.py interactive OpenCV tool lets operator click 6 reference points on a screenshot and prints all fractional constants as a ready-to-paste Python block

## Task Commits

Each task was committed atomically:

1. **Task 1: Create CoordMapper and core drag functions** - `4fc4d5b` (feat)
2. **Task 2: Create calibration script for fractional constants** - `c9e7172` (feat)

**Plan metadata:** (docs commit follows)

## Files Created/Modified
- `src/browser/tile_placer.py` — CoordMapper, TilePlacer, PlacementError, assign_rack_indices, jitter (246 lines)
- `scripts/calibrate_placement.py` — Interactive fractional-constant calibration tool (167 lines)

## Decisions Made
- All pixel coordinates expressed as fractions of canvas width/height; operator calibrates once from a live screenshot via `calibrate_placement.py`, then hardcodes constants
- Pixel-diff threshold of 1.0 mean absolute difference chosen as conservative threshold for placement verification (catches any tile landing without false positives from render noise)
- One retry on placement failure before raising `PlacementError` — keeps automation moving without infinite loops
- Human-like inter-tile delay 1–3s (`random.uniform`) between placements matches observed human pacing
- Rack tiles sorted by `col` ascending (H) or `row` ascending (V) before dragging — ensures word spells in board-natural order
- `TYPE_CHECKING` guard for `Move`/`TileUse` imports — avoids runtime circular imports; consistent with existing codebase pattern

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None — all 4 verification checks passed on first attempt.

## User Setup Required
Operator must run `python scripts/calibrate_placement.py <screenshot.png>` once with a live game screenshot to measure real fractional constants, then update the `PLACEHOLDER` values at the top of `src/browser/tile_placer.py`. Plan 02 will integrate confirmation and rejection recovery on top of this foundation.

## Next Phase Readiness
- `TilePlacer.place_tiles()` is ready for Plan 02 to wrap with confirmation-click, board-state diff verification, and rejection recovery logic
- Fractional constants in `tile_placer.py` are PLACEHOLDER values — must be calibrated from live screenshots before automated play will land tiles accurately
- `CoordMapper.confirm_btn_px()` is already implemented for Plan 02's confirmation step

---
*Phase: 07-tile-placement*
*Completed: 2026-03-26*
