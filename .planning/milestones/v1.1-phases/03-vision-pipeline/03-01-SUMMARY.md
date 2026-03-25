---
phase: 03-vision-pipeline
plan: 01
subsystem: vision
tags: [opencv, pillow, numpy, image-processing, json-schema, claude-vision]

# Dependency graph
requires:
  - phase: 01-word-engine
    provides: MultiplierType enum and Board/Cell classes used in MULT_STR_TO_ENGINE and schema interfaces
provides:
  - VisNError class with INVALID_SCREENSHOT, EXTRACTION_FAILED, VALIDATION_FAILED typed error codes
  - BOARD_SCHEMA JSON schema dict compatible with Claude Vision output_config.format
  - OFFICIAL_MULTIPLIER_LAYOUT dict (110 non-NONE positions for the 19x27 board)
  - MULT_STR_TO_ENGINE mapping from schema strings to MultiplierType enum
  - preprocess_screenshot(img_bytes) -> bytes function (OpenCV crop + Pillow upscale)
affects: [03-02-extractor, 03-02-validator]

# Tech tracking
tech-stack:
  added: [opencv-python==4.13.0.92, Pillow==12.1.1, numpy==2.2.6]
  patterns:
    - OpenCV HSV color mask for board region detection (cv2.inRange + cv2.findContours + cv2.boundingRect)
    - Pillow BytesIO pipeline for in-memory image processing (no disk I/O)
    - Image.Resampling.LANCZOS for quality 2x upscaling (Pillow 12.x form)
    - Typed error codes as module-level string constants paired with a custom Exception class

key-files:
  created:
    - src/vision/__init__.py
    - src/vision/errors.py
    - src/vision/schema.py
    - src/vision/preprocessor.py
    - tests/vision/__init__.py
    - tests/vision/test_preprocessor.py
  modified: []

key-decisions:
  - "Installed opencv-python, Pillow, numpy via pip — were listed in STACK.md but not yet installed in the Python 3.10.4 environment (Rule 3 auto-fix)"
  - "OFFICIAL_MULTIPLIER_LAYOUT uses 110 deduplicated positions — plan had two duplicate entries for (17,1) and (17,25) in the DW section; Python dict deduplication handled this automatically"
  - "Board detection HSV range [15,20,160] to [35,80,240] is an initial estimate; must be empirically calibrated against real Letter League screenshots before production use"
  - "MULT_STR_TO_ENGINE maps all 5 multiplier strings to MultiplierType enum for direct use when populating Board from vision output"

patterns-established:
  - "Pattern: All vision pipeline source files use `from __future__ import annotations` (project convention)"
  - "Pattern: preprocess_screenshot raises VisNError(INVALID_SCREENSHOT) not ValueError — typed errors for the entire vision pipeline"
  - "Pattern: Test images built with PIL.Image.new + ImageDraw (no external fixtures), validated against HSV bounds before writing"

requirements-completed: [VISN-03, VISN-04]

# Metrics
duration: 3min
completed: 2026-03-24
---

# Phase 3 Plan 01: Vision Foundation Summary

**OpenCV HSV board detection with Pillow 2x LANCZOS upscale, JSON schema for Claude structured output, and typed VisNError codes for the 19x27 Letter League board**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-24T21:43:45Z
- **Completed:** 2026-03-24T21:46:24Z
- **Tasks:** 3
- **Files modified:** 6 created

## Accomplishments

- `src/vision/` package established with error types, schema, and preprocessor as the foundation for Plan 03-02's extractor and validator
- `BOARD_SCHEMA` JSON schema constrains Claude Vision output at the token level — eliminates JSON parse errors on the extraction path
- `preprocess_screenshot()` detects the board region via OpenCV HSV color masking, crops, upscales 2x with LANCZOS, and clamps to 1568px — all 5 unit tests pass with synthetic images

## Task Commits

Each task was committed atomically:

1. **Task 1: Create vision error types and JSON schema with multiplier layout** - `69ed230` (feat)
2. **Task 2: Implement image preprocessor with OpenCV board detection and Pillow upscale** - `662daa4` (feat)
3. **Task 3: Write preprocessor unit tests** - `5c7132b` (test)

## Files Created/Modified

- `src/vision/__init__.py` - Package init (public API added in Plan 03-02)
- `src/vision/errors.py` - VisNError class + INVALID_SCREENSHOT, EXTRACTION_FAILED, VALIDATION_FAILED constants
- `src/vision/schema.py` - BOARD_SCHEMA, OFFICIAL_MULTIPLIER_LAYOUT (110 positions), MULT_STR_TO_ENGINE
- `src/vision/preprocessor.py` - preprocess_screenshot() — OpenCV HSV detection, Pillow crop/upscale, 1568px clamp
- `tests/vision/__init__.py` - Empty test package init
- `tests/vision/test_preprocessor.py` - 5 unit tests using synthetic PIL images

## Decisions Made

- Used `from __future__ import annotations` in all source files (project convention)
- `OFFICIAL_MULTIPLIER_LAYOUT` contains 110 positions (deduplication of the plan's DW list which had two duplicate entries for (17,1) and (17,25))
- Board detection clamps to MIN_BOARD_AREA=10000px before accepting a contour as a board region
- No color/contrast adjustments in the preprocessor per CONTEXT.md decision

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Installed missing vision dependencies**
- **Found during:** Pre-execution environment check
- **Issue:** opencv-python, Pillow, and numpy were listed as "already in project stack" in RESEARCH.md but were not installed in the Python 3.10.4 environment used by this project
- **Fix:** `py -m pip install opencv-python Pillow numpy` — installed opencv-python==4.13.0.92, Pillow==12.1.1, numpy==2.2.6
- **Files modified:** None (environment-level change)
- **Verification:** `py -c "import cv2, numpy; from PIL import Image"` succeeded
- **Committed in:** N/A (pip install, not code change)

---

**Total deviations:** 1 auto-fixed (1 blocking dependency install)
**Impact on plan:** Required for the plan to execute at all. Zero scope creep.

## Issues Encountered

None — once dependencies were installed, all three tasks executed cleanly.

## User Setup Required

None - no external service configuration required. The installed packages (opencv-python, Pillow, numpy) are standard and require no API keys or dashboard configuration.

## Next Phase Readiness

- `src/vision/` package with all foundation types is ready for Plan 03-02
- Plan 03-02 can import `VisNError`, `BOARD_SCHEMA`, `OFFICIAL_MULTIPLIER_LAYOUT`, `MULT_STR_TO_ENGINE`, and `preprocess_screenshot` directly
- HSV range constants (`BOARD_HSV_LOWER`, `BOARD_HSV_UPPER`) in preprocessor.py need empirical calibration against real Letter League screenshots — this is expected and documented in the code with a TODO comment
- OFFICIAL_MULTIPLIER_LAYOUT positions are approximate and must be verified against real screenshots before multiplier validation (check 3 in validator) can be relied upon

## Self-Check: PASSED

All created files confirmed present on disk. All task commits verified in git log.

---
*Phase: 03-vision-pipeline*
*Completed: 2026-03-24*
