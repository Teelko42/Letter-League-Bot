---
phase: 03-vision-pipeline
plan: 02
subsystem: vision
tags: [anthropic, claude-vision, structured-output, validator, flood-fill, json-schema]

# Dependency graph
requires:
  - phase: 03-01
    provides: VisNError, BOARD_SCHEMA, OFFICIAL_MULTIPLIER_LAYOUT, MULT_STR_TO_ENGINE, preprocess_screenshot
  - phase: 01-word-engine
    provides: Board.place_tile, MultiplierType enum
provides:
  - call_vision_api(img_bytes, retry_context) async function using claude-sonnet-4-6 with structured output
  - validate_extraction(data) four-check validator (letters, connectivity, multipliers, rack)
  - extract_board_state(img_bytes, mode) public async pipeline API returning (Board, list[str])
affects: [04-discord, 05-navigator]

# Tech tracking
tech-stack:
  added: [anthropic==0.86.0, loguru==0.7.3]
  patterns:
    - AsyncAnthropic module-level client with output_config json_schema for structured Claude Vision output
    - BFS flood-fill for tile connectivity check (avoids false positives on word endpoints)
    - Single retry with error context concatenation for validation recovery
    - Loguru structured logging at each pipeline stage with latency tracking

key-files:
  created:
    - src/vision/extractor.py
    - src/vision/validator.py
    - tests/vision/test_validator.py
  modified:
    - src/vision/__init__.py

key-decisions:
  - "Used claude-sonnet-4-6 model per STATE.md decision (~$0.004/screenshot); max_tokens=4096 with note to increase to 8192 if truncation observed"
  - "output_config json_schema with BOARD_SCHEMA constrains Claude token generation — eliminates JSON parse errors on primary path"
  - "BFS flood-fill for connectivity check per research Pitfall 5 — avoids false positives when only checking per-tile neighbors"
  - "anthropic==0.86.0 and loguru==0.7.3 installed (were listed in STACK.md but not installed in Python 3.10.4 env)"

patterns-established:
  - "Pattern: AsyncAnthropic client created at module level, not per-call — avoids connection overhead"
  - "Pattern: retry_context appended after base prompt with clear PREVIOUS ATTEMPT HAD ERRORS header"
  - "Pattern: _MULTIPLIER_LAYOUT_ENGINE computed once at __init__.py import time to avoid per-call dict comprehension"

requirements-completed: [VISN-01, VISN-02, VISN-05]

# Metrics
duration: 3min
completed: 2026-03-24
---

# Phase 3 Plan 02: Vision API Extractor + Validator Summary

**Claude Vision API extractor with output_config json_schema, BFS flood-fill validator with four checks, and single-retry pipeline wired into a public async extract_board_state function**

## Performance

- **Duration:** ~3 min
- **Started:** 2026-03-24T21:49:34Z
- **Completed:** 2026-03-24T21:52:00Z
- **Tasks:** 3
- **Files modified:** 4 (3 created, 1 updated)

## Accomplishments

- `call_vision_api` sends preprocessed PNG bytes to claude-sonnet-4-6 via `output_config.format.json_schema` — JSON parse errors are impossible on the primary path because Claude's token generation is constrained to the schema
- `validate_extraction` implements four checks in sequence: valid A-Z letters, BFS flood-fill connectivity, multiplier position matching against OFFICIAL_MULTIPLIER_LAYOUT, and rack count/content validation
- `extract_board_state` wires the full pipeline with one automatic retry (error context fed back to Claude) and populates a `Board` object compatible with GameEngine
- All 8 validator unit tests pass; full regression suite (107 tests) passes with zero failures

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement Claude Vision API extractor with structured output** - `24b5c4d` (feat)
2. **Task 2: Implement four-check validator with unit tests** - `bd2a595` (feat)
3. **Task 3: Wire pipeline entry point — extract_board_state public API** - `33b6260` (feat)

## Files Created/Modified

- `src/vision/extractor.py` - call_vision_api async function; EXTRACTION_PROMPT constant; module-level AsyncAnthropic client
- `src/vision/validator.py` - validate_extraction; four checks including BFS flood-fill for connectivity
- `src/vision/__init__.py` - extract_board_state public API; pipeline orchestration with retry; __all__ exports
- `tests/vision/test_validator.py` - 8 unit tests covering all four validation checks

## Decisions Made

- Installed anthropic==0.86.0 and loguru==0.7.3 (were expected in the environment but not present — Rule 3 auto-fix)
- Used `output_config={"format": {"type": "json_schema", "schema": BOARD_SCHEMA}}` for structured output — eliminates downstream JSON parse failures
- `_MULTIPLIER_LAYOUT_ENGINE` computed once at module import time (not per-call) to avoid repeated dict comprehension overhead
- BFS flood-fill selected over per-tile neighbor check per research Pitfall 5 — prevents false positives on endpoint tiles of a word that have only one neighbor

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Installed missing API and logging dependencies**
- **Found during:** Pre-Task-1 environment check
- **Issue:** `anthropic` (Claude API client) and `loguru` (structured logging) were not installed in the Python 3.10.4 environment despite being referenced in the plan
- **Fix:** `py -m pip install anthropic loguru` — installed anthropic==0.86.0, loguru==0.7.3
- **Files modified:** None (environment-level change)
- **Verification:** `py -c "import anthropic; import loguru"` succeeded
- **Committed in:** N/A (pip install, not code change)

---

**Total deviations:** 1 auto-fixed (1 blocking dependency install)
**Impact on plan:** Required for the plan to execute at all. Zero scope creep.

## Issues Encountered

None — once dependencies were installed, all three tasks executed cleanly with all 8 new tests passing and zero regressions in the 99 pre-existing tests.

## User Setup Required

**ANTHROPIC_API_KEY environment variable required before using extract_board_state.**

The extractor uses `AsyncAnthropic()` which reads from the `ANTHROPIC_API_KEY` environment variable by default. Without this key, `call_vision_api` will raise `VisNError(EXTRACTION_FAILED)` when called.

Source: https://console.anthropic.com/settings/keys — create or copy an existing API key.

## Next Phase Readiness

- `src/vision` package is complete — `extract_board_state` converts raw screenshot bytes to a populated `Board + rack` in a single async call
- Ready for Phase 4 (Discord bot integration): import `extract_board_state` from `src.vision`, call with `await interaction.response.defer()` first (vision API takes 4-15s)
- The `VisNError` codes (`INVALID_SCREENSHOT`, `EXTRACTION_FAILED`, `VALIDATION_FAILED`) provide structured error handling for Discord error message routing
- Multiplier layout and board detection HSV ranges still require empirical calibration against real Letter League screenshots — documented as known limitations in preprocessor.py and schema.py

## Self-Check: PASSED

All created/modified files confirmed present on disk. All task commits verified in git log.

---
*Phase: 03-vision-pipeline*
*Completed: 2026-03-24*
