---
phase: 06-turn-detection
plan: "01"
subsystem: browser
tags: [opencv, hsv, polling, turn-detection, calibration, asyncio]

# Dependency graph
requires:
  - phase: 05-browser-foundation
    provides: "capture_canvas(), BrowserSession, navigate_to_activity()"
  - phase: 03-vision-pipeline
    provides: "BOARD_HSV_LOWER/UPPER constants for game-over peach detection"

provides:
  - "TurnState Literal type (my_turn | not_my_turn | game_over)"
  - "classify_frame(img_bytes) — HSV banner + peach-ratio heuristic classification"
  - "poll_turn(page) — adaptive async polling loop returning on state change"
  - "preflight_check(page) — one-shot capture + classify + debug save"
  - "scripts/calibrate_turn.py — live HSV threshold discovery tool"

affects: [07-tile-placement, 08-game-loop]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Adaptive polling with fast/slow intervals and idle-threshold switchover"
    - "Quiet logging — only emit on state-change transitions"
    - "Exponential backoff on capture failure (base 1s, cap 30s)"
    - "Fractional ROI cropping (0.0–0.15 of height) rather than absolute pixel coords"
    - "game_over checked before my_turn to prevent infinite polling post-game"
    - "All HSV constants marked PLACEHOLDER for calibration in Plan 02"

key-files:
  created:
    - src/browser/turn_detector.py
    - scripts/calibrate_turn.py
  modified:
    - src/browser/__init__.py

key-decisions:
  - "Evaluate game_over before my_turn in classify_frame to prevent post-game infinite loop"
  - "Quiet logging pattern — only log on state-change, not every poll cycle"
  - "All HSV thresholds are placeholder values; Plan 02 calibrates from live screenshots"
  - "Calibration script imports same constants as detector so comparison is apples-to-apples"

patterns-established:
  - "TurnState: Literal type pattern — downstream phases import type directly from src.browser"
  - "Adaptive polling: fast interval until IDLE_THRESHOLD_S, then slow — snap back on change"

requirements-completed: [TURN-01]

# Metrics
duration: 2min
completed: 2026-03-26
---

# Phase 6 Plan 01: Turn Detector Module and Calibration Tooling Summary

**HSV-based orange banner turn detection with adaptive polling loop, game-over heuristic, and live calibration script — all HSV constants clearly marked as placeholders for Plan 02 calibration**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-03-26T05:23:09Z
- **Completed:** 2026-03-26T05:25:19Z
- **Tasks:** 2
- **Files modified:** 3

## Accomplishments

- Created `src/browser/turn_detector.py` with TurnState type, 6 functions (classify_frame, poll_turn, preflight_check, _is_my_turn, _is_game_over, _save_debug_screenshot) and adaptive polling loop
- Created `scripts/calibrate_turn.py` for live gameplay HSV threshold discovery, printing per-frame ROI stats and end-of-session suggested threshold ranges
- Updated `src/browser/__init__.py` to re-export TurnState, classify_frame, poll_turn, and preflight_check — downstream Phase 8 can import `from src.browser import poll_turn, TurnState`

## Task Commits

Each task was committed atomically:

1. **Task 1: Create turn detector module** - `4190954` (feat)
2. **Task 2: Create calibration script** - `73c4af2` (feat)

**Plan metadata:** (docs commit — see below)

## Files Created/Modified

- `src/browser/turn_detector.py` — TurnState type, classify_frame, poll_turn, preflight_check, plus internal helpers; all HSV constants marked PLACEHOLDER
- `scripts/calibrate_turn.py` — Interactive calibration loop: captures every 2s, prints banner ROI HSV stats (median/min/max), orange ratio vs threshold, centre peach ratio; accumulates session summary with suggested ranges on Ctrl+C
- `src/browser/__init__.py` — Added TurnState, classify_frame, poll_turn, preflight_check to imports and __all__

## Decisions Made

- game_over evaluated before my_turn in classify_frame — prevents infinite polling after the game ends (leaderboard overlay hides board centre peach, which is the game-over signal)
- Quiet logging pattern: only emit a log line when turn state changes, not on every poll cycle (per CONTEXT.md decisions)
- Fractional ROI constants (BANNER_ROI_FRAC) rather than absolute pixel coordinates — resolution-independent
- Calibration script imports the same BANNER_HSV_LOWER/UPPER/CONFIDENCE constants as the detector so reported ratios are directly comparable to the detector's decision boundary
- local imports of capture_canvas inside poll_turn and preflight_check to avoid circular import (src.browser.capture <-> src.browser.__init__)

## Deviations from Plan

None — plan executed exactly as written.

## Issues Encountered

None — all verification checks passed on first run.

## User Setup Required

None — no external service configuration required.

## Next Phase Readiness

- Turn detection structure is complete; Plan 02 only needs to run calibrate_turn.py during a live game to discover correct HSV values and update the PLACEHOLDER constants
- Package exports are live — `from src.browser import poll_turn, TurnState` works now
- All placeholders clearly marked so Plan 02 scope is clear: update 5 constants in turn_detector.py, re-run verification

---
*Phase: 06-turn-detection*
*Completed: 2026-03-26*

## Self-Check: PASSED

- FOUND: src/browser/turn_detector.py
- FOUND: scripts/calibrate_turn.py
- FOUND: .planning/phases/06-turn-detection/06-01-SUMMARY.md
- FOUND commit: 4190954 (Task 1)
- FOUND commit: 73c4af2 (Task 2)
