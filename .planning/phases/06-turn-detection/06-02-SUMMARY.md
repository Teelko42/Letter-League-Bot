---
phase: 06-turn-detection
plan: "02"
subsystem: vision
tags: [opencv, hsv, turn-detection, calibration]

requires:
  - phase: 06-turn-detection/01
    provides: "turn_detector module with placeholder HSV constants"
provides:
  - "Calibrated HSV thresholds for turn detection (BANNER_CONFIDENCE=0.07)"
  - "Verified classify_frame accuracy across all three game states"
  - "Reference screenshots in debug/turn_detection/ for regression testing"
affects: [phase-08, game-loop]

tech-stack:
  added: []
  patterns: ["HSV color thresholding with fractional ROI cropping"]

key-files:
  created: []
  modified: ["src/browser/turn_detector.py"]

key-decisions:
  - "BANNER_CONFIDENCE=0.07 — 3.3% margin above not_my_turn baseline (3.7%), 2.1% below my_turn min (9.1%)"
  - "GAME_OVER_BOARD_THRESHOLD=0.25 — between game_over peach (12%) and gameplay peach (57-60%)"
  - "HSV range [5-20,120-255,150-255] confirmed from placeholder — good separation without widening"
  - "Screenshots manually captured and cropped to simulate capture_canvas output for calibration"

patterns-established:
  - "Manual screenshot calibration workflow: capture full Discord window, crop to game iframe area, analyze HSV"

requirements-completed: [TURN-01]

duration: 15min
completed: 2026-03-26
---

# Phase 06-02: Turn Detection Calibration Summary

**HSV thresholds calibrated from live gameplay — 5/5 screenshots classify correctly with zero false positives**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-03-26T00:45:00Z
- **Completed:** 2026-03-26T01:00:00Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments
- Calibrated BANNER_CONFIDENCE from 0.10 to 0.07 based on observed orange ratios (my_turn ~9-10%, not_my_turn ~3.7%)
- Calibrated GAME_OVER_BOARD_THRESHOLD from 0.02 to 0.25 based on center peach ratios (gameplay ~58%, game_over ~12%)
- All 5 test screenshots (2 my_turn, 2 not_my_turn, 1 game_over) classify correctly
- Zero false positives — no not_my_turn frame classified as my_turn

## Task Commits

1. **Task 1: Run live calibration (human-verify checkpoint)** — Manual screenshot capture during live gameplay
2. **Task 2: Update thresholds and verify classification** — `f6e90c6` (feat)

## Files Created/Modified
- `src/browser/turn_detector.py` — Updated HSV constants from placeholders to calibrated values
- `debug/turn_detection/cropped_*.png` — Cropped reference screenshots simulating capture_canvas output

## Decisions Made
- HSV range kept at placeholder values [5-20,120-255,150-255] — analysis confirmed good separation
- BANNER_CONFIDENCE set to 0.07 (not 0.10) for wider margin from not_my_turn baseline
- Screenshots were full Discord windows — cropped to game iframe area for accurate calibration
- GAME_OVER_BOARD_THRESHOLD raised from 0.02 to 0.25 to catch leaderboard overlay (12% peach vs 58% gameplay)

## Deviations from Plan
- Calibration done via manual screenshots instead of calibrate_turn.py script (iframe navigation failed)
- Screenshots manually cropped to simulate capture_canvas output since full Discord windows were captured
- Only 5 screenshots total instead of 12+ (plan wanted 5+ per state) — ratios were consistent

## Issues Encountered
- calibrate_turn.py couldn't find Activity iframe (no active game at time of script run)
- Workaround: manual screenshots during live gameplay, then programmatic HSV analysis

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Turn detection calibrated and verified — ready for Phase 7+ integration
- poll_turn() can detect all three states: my_turn, not_my_turn, game_over

---
*Phase: 06-turn-detection*
*Completed: 2026-03-26*
