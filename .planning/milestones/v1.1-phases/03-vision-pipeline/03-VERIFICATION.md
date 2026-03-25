---
phase: 03-vision-pipeline
verified: 2026-03-24T22:15:00Z
status: human_needed
score: 10/10 must-haves verified
human_verification:
  - test: "Submit a real Letter League screenshot to extract_board_state() and inspect the returned Board"
    expected: "All placed tiles appear at their correct 0-indexed (row, col) positions matching what is visible in the screenshot"
    why_human: "Automated tests use synthetic images only. HSV detection range is an initial estimate that requires calibration against actual screenshots. We cannot verify accuracy of tile coordinate extraction without a real game screenshot."
  - test: "Submit a real Letter League screenshot and confirm the tile rack is correctly extracted"
    expected: "The returned rack list matches the letters visible in the rack strip at the bottom of the screenshot, including '?' for blank tiles"
    why_human: "Rack extraction depends on Claude Vision accurately parsing the rack region. Cannot verify correctness without a real screenshot."
  - test: "Submit a real screenshot and compare returned multiplier values against the visible board squares"
    expected: "Each cell's reported multiplier (DL/TL/DW/TW/NONE) matches the colored square visible on the board for that position"
    why_human: "OFFICIAL_MULTIPLIER_LAYOUT positions are documented as approximate estimates requiring empirical calibration. The layout comment in schema.py explicitly states: 'TODO: Verify against real Letter League screenshots'. Cannot verify positional accuracy programmatically."
  - test: "Submit a non-game screenshot (e.g. a desktop screenshot or blank image) to extract_board_state()"
    expected: "Function raises VisNError with code INVALID_SCREENSHOT within a few seconds"
    why_human: "HSV detection in preprocess_screenshot will gate most invalid images, but real-world behavior against diverse non-game inputs needs human confirmation."
---

# Phase 3: Vision Pipeline Verification Report

**Phase Goal:** The bot can reliably extract a complete, validated board state from a Letter League screenshot
**Verified:** 2026-03-24T22:15:00Z
**Status:** human_needed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | A JSON schema defines the board extraction format with board cells, bounding rect, rack, and multipliers | VERIFIED | `BOARD_SCHEMA` in `src/vision/schema.py`: type=object, required=['board','rack'], additionalProperties=False. Board has min_row/max_row/min_col/max_col/cells. Cell has row/col/letter/is_blank/multiplier enum ['NONE','DL','TL','DW','TW']. rack maxItems=7. All assertions pass programmatically. |
| 2 | The official 19x27 multiplier layout is hardcoded and can be looked up by (row, col) | VERIFIED | `OFFICIAL_MULTIPLIER_LAYOUT` in `src/vision/schema.py`: 110 entries (after deduplication). `MULT_STR_TO_ENGINE` maps all 5 strings to MultiplierType enum. Confirmed via `py -c` import check. |
| 3 | A raw screenshot is auto-cropped to the board region using color-based detection, upscaled 2x, and clamped to 1568px | VERIFIED | `preprocess_screenshot()` in `src/vision/preprocessor.py`: OpenCV HSV mask → findContours → boundingRect → Pillow crop → 2x LANCZOS resize → 1568px clamp → PNG bytes. All 5 unit tests pass with synthetic images (PNG output, upscale assertion, clamping, raises on missing board, raises on tiny area). |
| 4 | Invalid or non-game screenshots raise a typed VisNError with INVALID_SCREENSHOT code | VERIFIED | `preprocess_screenshot()` raises `VisNError(INVALID_SCREENSHOT, ...)` for: no contours found, largest contour area < MIN_BOARD_AREA (10000px). `VisNError` has `.code` and `.message` attributes, `__str__` formats as `[CODE] message`. Confirmed via `test_preprocess_raises_on_no_board` and `test_preprocess_raises_on_tiny_region` (both pass). |
| 5 | A preprocessed screenshot sent to Claude Vision API returns a structured JSON with board cells, bounding rect, rack, and multipliers | VERIFIED | `call_vision_api()` in `src/vision/extractor.py`: async, uses `output_config={"format":{"type":"json_schema","schema":BOARD_SCHEMA}}` with `claude-sonnet-4-6`. Returns `json.loads(response.content[0].text)`. Import check and function inspection confirm correct structure. |
| 6 | The tile rack is extracted alongside the board in a single API call | VERIFIED | `BOARD_SCHEMA` has `"rack"` as a required top-level field alongside `"board"`. Extractor sends a single API call returning both in one JSON. `extract_board_state` returns `(board, rack)` where `rack = data["rack"]`. |
| 7 | Extracted data passes four validation checks: valid letters, connectivity, multiplier layout match, rack count <= 7 | VERIFIED | `validate_extraction()` in `src/vision/validator.py`: Check 1 (A-Z via ALPHABET import), Check 2 (BFS flood-fill from first tile, floating = placed-visited), Check 3 (compare against OFFICIAL_MULTIPLIER_LAYOUT), Check 4 (len > 7 error, valid_rack_chars = ALPHABET + '?'). All 8 unit tests pass. |
| 8 | On validation failure, one retry is attempted with error context fed back to Claude | VERIFIED | `extract_board_state()` in `src/vision/__init__.py`: if errors non-empty, builds `retry_context = "\n".join(errors)`, logs warning, calls `call_vision_api(processed_bytes, retry_context=retry_context)`, re-validates. If errors still non-empty: raises `VisNError(VALIDATION_FAILED, ...)`. Retry header `"PREVIOUS ATTEMPT HAD ERRORS"` confirmed in extractor.py prompt construction. |
| 9 | The public extract_board_state function returns a populated Board + rack list or raises VisNError | VERIFIED | `extract_board_state(img_bytes, mode)` in `src/vision/__init__.py`: async, returns `tuple[Board, list[str]]`. Board constructed with `Board(rows=19, cols=27, multiplier_layout=_MULTIPLIER_LAYOUT_ENGINE)`, populated via `board.place_tile(row, col, letter, is_blank, mode)` for each cell. `inspect.iscoroutinefunction(extract_board_state)` confirmed True. |
| 10 | Unrecognizable screenshots return a VisNError with INVALID_SCREENSHOT code | VERIFIED | `preprocess_screenshot()` raises `VisNError(INVALID_SCREENSHOT)` on no-match or small area. This propagates through `extract_board_state()` without catching. `__all__` exports `VisNError, INVALID_SCREENSHOT, EXTRACTION_FAILED, VALIDATION_FAILED` for downstream consumers. |

**Score:** 10/10 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/vision/__init__.py` | `extract_board_state(img_bytes, mode)` public async API; `__all__` exports | VERIFIED | 140 lines. Async, returns `(Board, list[str])`. Imports from all pipeline modules. `_MULTIPLIER_LAYOUT_ENGINE` pre-computed at module load. Retry logic present. |
| `src/vision/errors.py` | `VisNError` class with typed error codes | VERIFIED | 21 lines. `VisNError(Exception)` with `.code`, `.message`. Three constants: `INVALID_SCREENSHOT`, `EXTRACTION_FAILED`, `VALIDATION_FAILED`. |
| `src/vision/schema.py` | `BOARD_SCHEMA` dict, `OFFICIAL_MULTIPLIER_LAYOUT` mapping, `MULT_STR_TO_ENGINE` mapping | VERIFIED | 196 lines. BOARD_SCHEMA passes structural assertions. OFFICIAL_MULTIPLIER_LAYOUT has 110 positions. MULT_STR_TO_ENGINE has all 5 keys. |
| `src/vision/preprocessor.py` | `preprocess_screenshot(img_bytes) -> bytes` | VERIFIED | 107 lines. OpenCV HSV detection, Pillow crop/resize, 1568px clamp, PNG output. Raises `VisNError(INVALID_SCREENSHOT)` on failure. |
| `src/vision/extractor.py` | `call_vision_api(img_bytes, retry_context)` async function | VERIFIED | 137 lines. Async, model=claude-sonnet-4-6, output_config json_schema, base64 encode, EXTRACTION_PROMPT constant (1341 chars), retry_context appended, latency + token logging. |
| `src/vision/validator.py` | `validate_extraction(data)` function returning list of error strings | VERIFIED | 94 lines. Four checks in sequence. BFS flood-fill for connectivity. Returns `list[str]`, empty = pass. |
| `tests/vision/__init__.py` | Empty test package init | VERIFIED | Present. |
| `tests/vision/test_preprocessor.py` | Unit tests for preprocessor edge cases | VERIFIED | 98 lines. 5 tests, all pass: PNG output, upscale, clamp, no-board error, tiny-area error. Synthetic PIL images, no external fixtures. |
| `tests/vision/test_validator.py` | Unit tests for all four validation checks | VERIFIED | 177 lines. 8 tests, all pass: valid passes, invalid letter, floating tile, connected word, single tile, multiplier mismatch, rack > 7, invalid rack tile. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `src/vision/preprocessor.py` | `src/vision/errors.py` | raises VisNError on detection failure | WIRED | `from src.vision.errors import INVALID_SCREENSHOT, VisNError` at line 9. Used at lines 57-60, 71-75, 79-84. |
| `src/vision/schema.py` | `src/engine/models.py` | MULT_STR_TO_ENGINE maps to MultiplierType | WIRED | `from src.engine.models import MultiplierType` at line 3. Used in `MULT_STR_TO_ENGINE` dict. |
| `src/vision/extractor.py` | `src/vision/schema.py` | imports BOARD_SCHEMA for output_config | WIRED | `from src.vision.schema import BOARD_SCHEMA` confirmed in extractor.py. Used in `output_config` dict at API call. |
| `src/vision/validator.py` | `src/vision/schema.py` | imports OFFICIAL_MULTIPLIER_LAYOUT for check 3 | WIRED | `from src.vision.schema import OFFICIAL_MULTIPLIER_LAYOUT` in validator.py line 6. Used in check 3 loop. |
| `src/vision/__init__.py` | `src/vision/preprocessor.py` | calls preprocess_screenshot in pipeline | WIRED | `from src.vision.preprocessor import preprocess_screenshot` confirmed. Called at pipeline step 1. |
| `src/vision/__init__.py` | `src/vision/extractor.py` | calls call_vision_api in pipeline | WIRED | `from src.vision.extractor import call_vision_api` confirmed. Called at step 2 and retry step 4. |
| `src/vision/__init__.py` | `src/vision/validator.py` | calls validate_extraction + retry on failure | WIRED | `from src.vision.validator import validate_extraction` confirmed. Called at step 3 and re-called after retry. |
| `src/vision/__init__.py` | `src/engine/board.py` | populates Board with extracted cells via place_tile | WIRED | `from src.engine.board import Board` confirmed. `Board(rows=19, cols=27, multiplier_layout=_MULTIPLIER_LAYOUT_ENGINE)` + `board.place_tile(...)` per cell. |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| VISN-01 | 03-02-PLAN.md | User can submit a screenshot and receive a structured board state extraction | SATISFIED | `extract_board_state()` returns `(Board, list[str])` representing grid cells, letters, positions. Board is a fully populated 19x27 `Board` object. |
| VISN-02 | 03-02-PLAN.md | User's tile rack is extracted alongside the board | SATISFIED | Single `call_vision_api` call returns `{"board": ..., "rack": [...]}`. `extract_board_state` returns rack as `list[str]`. |
| VISN-03 | 03-01-PLAN.md | Multiplier squares are detected and mapped to board positions | SATISFIED | `OFFICIAL_MULTIPLIER_LAYOUT` (110 positions) in schema.py. Validator check 3 compares each extracted cell's multiplier against the layout. Board populated with `_MULTIPLIER_LAYOUT_ENGINE`. NOTE: positions require empirical calibration against real screenshots — see human verification items. |
| VISN-04 | 03-01-PLAN.md | Screenshots are cropped to the board region and upscaled before API processing | SATISFIED | `preprocess_screenshot()`: OpenCV HSV detection → crop → 2x LANCZOS upscale → 1568px clamp → PNG bytes. 5 passing tests with synthetic images confirm behavior. |
| VISN-05 | 03-02-PLAN.md | Extracted board state is validated against engine constraints before being passed to the word engine | SATISFIED | `validate_extraction()` runs 4 checks: valid A-Z letters, BFS connectivity, multiplier layout match, rack <= 7 tiles. Single retry with error context. Raises `VisNError(VALIDATION_FAILED)` if validation fails after retry. 8 tests pass. |

All 5 VISN requirements satisfied programmatically. No orphaned requirements found — REQUIREMENTS.md maps all 5 VISN IDs to Phase 3, all 5 claimed by plans 03-01 and 03-02.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `src/vision/schema.py` | 59 | `TODO: Verify against real Letter League screenshots — update positions if needed` | Info | OFFICIAL_MULTIPLIER_LAYOUT positions are approximate. Multiplier validation (check 3) and Board construction use these positions. Calibration is required before multiplier data is reliable, but this is a known, documented limitation — not a code defect. |
| `src/vision/preprocessor.py` | 23-26 | `# HSV range for Letter League board background — needs empirical calibration` | Info | BOARD_HSV_LOWER/UPPER are initial estimates. Board detection may fail or produce incorrect crops on real screenshots. This is the core unknown for the phase. Known limitation explicitly documented in code. |

No blocker or warning severity anti-patterns found. Both items are info-level — they are expected calibration requirements, not stub implementations or missing logic. The code is fully implemented; the unknowns are empirical input data.

### Human Verification Required

#### 1. Real Screenshot Board Extraction

**Test:** Run `asyncio.run(extract_board_state(open("screenshot.png","rb").read()))` against an actual Letter League game screenshot.
**Expected:** Returns a `Board` object where `board.get_cell(row, col).letter` matches each tile visible on the screenshot, at their correct 0-indexed coordinates.
**Why human:** All automated tests use synthetic PIL images. The HSV range `[15,20,160]–[35,80,240]` is an initial estimate. Board detection accuracy and tile coordinate extraction correctness can only be confirmed with a real game screenshot.

#### 2. Tile Rack Extraction Accuracy

**Test:** Inspect the returned `rack` list from `extract_board_state()` against the tile rack visible in the screenshot.
**Expected:** Rack list contains the exact letters shown in the player's rack strip at the bottom of the screenshot. Blank tiles shown as `'?'`.
**Why human:** Claude Vision's ability to parse the rack region from a real Letter League screenshot cannot be verified without a real screenshot.

#### 3. Multiplier Position Accuracy

**Test:** Cross-reference the multiplier for a few known squares (e.g. TW corners) in the returned Board against the visual board.
**Expected:** Multiplier enum values on the Board match the colored squares visible on the actual game board.
**Why human:** `OFFICIAL_MULTIPLIER_LAYOUT` is documented as approximate. The code explicitly marks positions as needing verification. Positional accuracy requires visual comparison against a real board.

#### 4. Invalid Screenshot Rejection

**Test:** Pass a non-game image (e.g. a desktop screenshot) to `extract_board_state()`.
**Expected:** `VisNError` with `code == "INVALID_SCREENSHOT"` raised within 1-5 seconds (no API call made).
**Why human:** Confirms HSV detection correctly rejects non-game images in practice. The synthetic test only validates the code path; real-world rejection rate is unknown.

### Gaps Summary

No gaps blocking automated goal achievement. All 10 derived truths are verified at code level. All 9 artifacts exist and are substantive. All 8 key links are wired. All 5 VISN requirements are satisfied. The 13 tests (5 preprocessor + 8 validator) all pass, including full regression suite (107 tests, 0 failures).

The phase goal is architecturally complete. The single remaining uncertainty is empirical: whether the HSV board detection range and the approximate multiplier layout positions are accurate enough on real Letter League screenshots. This cannot be resolved without actual game screenshots and is correctly classified as human verification rather than a code gap.

---

_Verified: 2026-03-24T22:15:00Z_
_Verifier: Claude (gsd-verifier)_
