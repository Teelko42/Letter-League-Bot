# Letter League Bot - Remaining Testing Report

**Date:** 2026-04-02
**Current test count:** 124 test functions across 10 test files
**Current coverage:** Engine and Difficulty subsystems are well-tested; Browser and Bot subsystems have significant gaps.

---

## Table of Contents

1. [Current Test Coverage Summary](#1-current-test-coverage-summary)
2. [What's Already Tested](#2-whats-already-tested)
3. [Remaining Tests: Browser Subsystem](#3-remaining-tests-browser-subsystem)
4. [Remaining Tests: Bot Subsystem](#4-remaining-tests-bot-subsystem)
5. [Remaining Tests: Vision Subsystem](#5-remaining-tests-vision-subsystem)
6. [Remaining Tests: Misc Gaps](#6-remaining-tests-misc-gaps)
7. [Recommended Testing Order](#7-recommended-testing-order)
8. [Appendix: File-by-File Status](#appendix-file-by-file-status)

---

## 1. Current Test Coverage Summary

| Subsystem | Source Files | Source Lines | Tests | Status |
|-----------|-------------|-------------|-------|--------|
| Engine | 7 files | ~1,544 | 72 | Well covered |
| Difficulty | 3 files | ~175 | 22 | Well covered |
| Vision | 5 files | ~607 | 13 | Partial (preprocessor + validator only) |
| Bot | 6 files | ~1,134 | 17 | Partial (autoplay_cog + formatter only) |
| Browser | 5 files | ~1,330 | 0 | **Not tested** |

---

## 2. What's Already Tested

These files have dedicated test coverage and do **not** need additional work:

| Test File | Tests | What It Covers |
|-----------|-------|----------------|
| `test_board.py` | 20 | Board dimensions, multiplier layout, tile ops, anchors, cross-checks, left-limits |
| `test_gaddag.py` | 9 | GADDAG build, word lookup, case handling, pickle cache roundtrip & invalidation |
| `test_moves.py` | 12 | Move generation: empty board, extensions, cross-word validation, blanks, dedup |
| `test_scoring.py` | 22 | Classic/Wild scoring: multipliers, blanks, perpendicular words, bingo bonus |
| `test_engine.py` | 9 | GameEngine init, find_moves, best_move, play_move, multi-turn, mode switching |
| `test_difficulty.py` | 22 | FrequencyIndex + DifficultyEngine: 0-100% range, word freq, OOV, strategy variation |
| `test_autoplay_cog.py` | 11 | AutoPlayCog slash commands, game loop, reconnection, vision retries (all mocked) |
| `test_autoplay_formatter.py` | 6 | Turn/swap/game-over embeds, LoopState defaults, AutoPlayPhase members |
| `vision/test_preprocessor.py` | 5 | PNG output, upscale, max-edge clamping, invalid screenshot |
| `vision/test_validator.py` | 8 | Valid extraction, invalid letters, floating tiles, connectivity, multiplier mismatches |

---

## 3. Remaining Tests: Browser Subsystem

The browser subsystem has **zero tests** and accounts for ~1,330 lines. These are the highest-priority gaps.

---

### 3.1 CoordMapper (file: `src/browser/tile_placer.py`, lines 56-143)

**What it does:** Converts board grid coordinates and rack slot indices into pixel positions using fractional constants relative to a canvas bounding box.

**Why it's testable without a browser:** Pure math -- takes a bbox dict, returns pixel coordinates. No Playwright dependency.

**Tests to write** (file: `tests/test_coord_mapper.py`):

- [ ] **Step 1:** `test_board_cell_px_origin` -- Pass a known bbox (e.g. `{"x": 0, "y": 0, "width": 1000, "height": 800}`), call `board_cell_px(0, 0)`, and assert the result matches `GRID_X0_FRAC * 1000` and `GRID_Y0_FRAC * 800`.
- [ ] **Step 2:** `test_board_cell_px_offset` -- Call `board_cell_px(7, 7)` (center of board) and verify it equals `(bbox.x + (GRID_X0_FRAC + 7 * CELL_W_FRAC) * width, ...)`.
- [ ] **Step 3:** `test_board_cell_px_with_nonzero_bbox_origin` -- Use a bbox with `x=100, y=50` to verify the offset is added.
- [ ] **Step 4:** `test_rack_tile_px_slot_0` -- Call `rack_tile_px(0)`, verify it returns rack origin.
- [ ] **Step 5:** `test_rack_tile_px_slot_6` -- Call `rack_tile_px(6)` (last slot), verify spacing.
- [ ] **Step 6:** `test_confirm_btn_px` -- Call `confirm_btn_px()`, verify expected coordinates.
- [ ] **Step 7:** `test_recall_btn_px` -- Call `recall_btn_px()`, verify expected coordinates.
- [ ] **Step 8:** `test_swap_btn_px` -- Call `swap_btn_px()`, verify expected coordinates.
- [ ] **Step 9:** `test_none_bbox_raises` -- Pass `bbox=None`, expect `PlacementError`.

---

### 3.2 assign_rack_indices (file: `src/browser/tile_placer.py`, lines 171-213)

**What it does:** Maps TileUse objects to rack slot positions. Pure function, no browser dependency.

**Tests to write** (add to `tests/test_coord_mapper.py` or `tests/test_tile_placer_utils.py`):

- [ ] **Step 1:** `test_assign_simple_unique_letters` -- Rack `['A', 'B', 'C']`, tiles using A and C -> indices `[0, 2]`.
- [ ] **Step 2:** `test_assign_duplicate_letters` -- Rack `['A', 'A', 'B']`, two tiles needing A -> indices `[0, 1]` (greedy left-to-right).
- [ ] **Step 3:** `test_assign_blank_tile` -- Rack `['A', '?', 'B']`, tile with `is_blank=True` -> matches `'?'` at index 1.
- [ ] **Step 4:** `test_assign_missing_letter_raises` -- Rack `['A', 'B']`, tile needing C -> `ValueError`.
- [ ] **Step 5:** `test_assign_empty_rack_tiles` -- Empty `rack_tiles` list -> empty result.

---

### 3.3 jitter (file: `src/browser/tile_placer.py`, lines 151-168)

**What it does:** Adds random pixel jitter to coordinates. Pure function.

**Tests to write:**

- [ ] **Step 1:** `test_jitter_within_bounds` -- Call `jitter(100.0, 200.0, px=5)` many times, assert result is always within `[95, 105]` x `[195, 205]`.
- [ ] **Step 2:** `test_jitter_zero_px` -- Call `jitter(100.0, 200.0, px=0)`, assert exact coordinates returned.

---

### 3.4 TilePlacer (file: `src/browser/tile_placer.py`, lines 221-596)

**What it does:** Orchestrates drag-and-drop tile placement with screenshot verification and retry logic.

**Why mocking is needed:** All methods use `self._page.mouse` and `capture_canvas()`. Must mock Playwright.

**Tests to write** (file: `tests/test_tile_placer.py`):

- [ ] **Step 1:** `test_place_tiles_calls_drag_in_order` -- Mock `_drag_tile`, `_verify_placement` (returns True), `_get_canvas_bbox`. Call `place_tiles()` with a 3-tile horizontal move. Assert drags happen in left-to-right column order.
- [ ] **Step 2:** `test_place_tiles_vertical_order` -- Same as above but vertical move. Assert drags happen top-to-bottom.
- [ ] **Step 3:** `test_place_tiles_retry_on_verification_failure` -- Mock `_verify_placement` to fail once then succeed. Verify drag is called twice for that tile.
- [ ] **Step 4:** `test_place_tiles_raises_after_retry_failure` -- Mock `_verify_placement` to always fail. Expect `PlacementError`.
- [ ] **Step 5:** `test_place_tiles_no_rack_tiles_skips` -- Pass a move with no rack tiles consumed. Verify no drags happen.
- [ ] **Step 6:** `test_place_move_accepted_first_try` -- Mock `place_tiles` + `_click_confirm` + `_wait_for_acceptance` (returns True). Assert returns True.
- [ ] **Step 7:** `test_place_move_rejected_then_accepted` -- First word rejected, second accepted. Assert recall is called, returns True.
- [ ] **Step 8:** `test_place_move_all_rejected_tile_swap` -- All words rejected. Assert `_tile_swap` called, returns False.
- [ ] **Step 9:** `test_place_move_placement_error_continues` -- First move raises PlacementError. Assert recall attempted, moves to next word.
- [ ] **Step 10:** `test_get_canvas_bbox_canvas_found` -- Mock iframe locator returning valid bbox. Assert bbox returned.
- [ ] **Step 11:** `test_get_canvas_bbox_fallback_to_iframe` -- Canvas locator raises, iframe locator returns bbox. Assert fallback works.
- [ ] **Step 12:** `test_get_canvas_bbox_both_fail` -- Both locators return None. Expect `PlacementError`.

---

### 3.5 turn_detector (file: `src/browser/turn_detector.py`)

**What it does:** Classifies game screenshots as "my_turn", "not_my_turn", or "game_over" using HSV color analysis. Also has `poll_turn()` which loops capture + classify.

**Tests to write** (file: `tests/test_turn_detector.py`):

For the pure functions (`classify_frame`, `_is_my_turn`, `_is_game_over`):

- [ ] **Step 1:** `test_classify_frame_my_turn` -- Create a synthetic image with an orange banner in the top 15%. Encode as PNG bytes. Call `classify_frame()`. Assert returns `"my_turn"`.
- [ ] **Step 2:** `test_classify_frame_not_my_turn` -- Create an image with a non-orange top region and visible board peach in center. Assert returns `"not_my_turn"`.
- [ ] **Step 3:** `test_classify_frame_game_over` -- Create an image with no orange banner AND low peach ratio in center. Assert returns `"game_over"`.
- [ ] **Step 4:** `test_classify_frame_invalid_bytes` -- Pass corrupt/empty bytes. Assert returns a safe default (not a crash).
- [ ] **Step 5:** `test_is_my_turn_above_threshold` -- Verify orange pixel ratio above `BANNER_CONFIDENCE` (0.07) triggers True.
- [ ] **Step 6:** `test_is_my_turn_below_threshold` -- Verify ratio below threshold triggers False.

For `poll_turn()` (requires mocking `capture_canvas`):

- [ ] **Step 7:** `test_poll_turn_returns_my_turn_immediately` -- Mock `capture_canvas` to return a "my_turn" image. Assert `poll_turn()` returns `"my_turn"` quickly.
- [ ] **Step 8:** `test_poll_turn_game_over_detected` -- Mock capture to return game-over image. Assert returns `"game_over"`.
- [ ] **Step 9:** `test_poll_turn_slow_polling_after_idle` -- Mock capture to always return "not_my_turn". Verify it switches to slow polling interval after `IDLE_THRESHOLD_S`.

For `preflight_check()`:

- [ ] **Step 10:** `test_preflight_check_passes` -- Mock capture returning a valid game image. Assert returns True.
- [ ] **Step 11:** `test_preflight_check_fails_blank` -- Mock capture returning blank/black image. Assert returns False.

---

### 3.6 capture.py (file: `src/browser/capture.py`)

**What it does:** `capture_canvas()` takes a Playwright page, finds the game iframe, and screenshots it. `is_non_blank()` checks if screenshot bytes contain actual content.

**Tests to write** (file: `tests/test_capture.py`):

For `is_non_blank()` (pure function, no browser needed):

- [ ] **Step 1:** `test_is_non_blank_colorful_image` -- Create a numpy array with varied pixel values, encode to PNG bytes. Assert returns True.
- [ ] **Step 2:** `test_is_non_blank_solid_black` -- Create an all-zeros image. Assert returns False.
- [ ] **Step 3:** `test_is_non_blank_solid_white` -- Create an all-255 image. Assert returns False (std dev = 0).
- [ ] **Step 4:** `test_is_non_blank_empty_bytes` -- Pass `b""`. Assert returns False.
- [ ] **Step 5:** `test_is_non_blank_corrupt_bytes` -- Pass random non-image bytes. Assert returns False (no crash).

For `capture_canvas()` (requires mocking Playwright):

- [ ] **Step 6:** `test_capture_canvas_returns_png_bytes` -- Mock page iframe locator to return screenshot bytes. Assert returned bytes start with PNG header.
- [ ] **Step 7:** `test_capture_canvas_retries_on_blank` -- Mock first capture as blank, second as valid. Assert retry logic works.
- [ ] **Step 8:** `test_capture_canvas_raises_after_max_retries` -- Mock all captures as blank. Assert raises after retry limit.

---

### 3.7 navigator.py (file: `src/browser/navigator.py`)

**What it does:** Navigates Playwright to a Discord voice channel, opens the Activity shelf, selects Letter League, and returns the activity iframe.

**Tests to write** (file: `tests/test_navigator.py`):

- [ ] **Step 1:** `test_navigate_success` -- Mock page.goto, click selectors, wait_for_selector. Assert returns a frame object.
- [ ] **Step 2:** `test_navigate_retries_on_timeout` -- Mock first attempt to raise TimeoutError, second to succeed. Assert retries.
- [ ] **Step 3:** `test_navigate_raises_after_max_retries` -- Mock all attempts to fail. Assert raises after `max_retries`.
- [ ] **Step 4:** `test_navigate_invalid_channel_url` -- Pass a malformed URL. Assert appropriate error.

---

### 3.8 session.py (file: `src/browser/session.py`)

**What it does:** Manages Playwright browser lifecycle -- first-run login, session validation, and session expiry detection.

**Tests to write** (file: `tests/test_session.py`):

- [ ] **Step 1:** `test_session_start_creates_context` -- Mock patchright. Call `start()`. Assert browser context created with profile dir.
- [ ] **Step 2:** `test_session_stop_closes_resources` -- Call `stop()`. Assert browser and playwright are closed.
- [ ] **Step 3:** `test_session_validates_login` -- Mock `wait_for_selector` to find guild nav. Assert session validated.
- [ ] **Step 4:** `test_session_expired_exits` -- Mock `wait_for_selector` to timeout. Assert clean exit behavior.

---

## 4. Remaining Tests: Bot Subsystem

---

### 4.1 AdvisorCog (file: `src/bot/cog.py`)

**What it does:** Handles `/analyze`, `/setdifficulty`, `/setmode` slash commands. The `/analyze` command runs the full vision -> engine -> difficulty pipeline.

**Tests to write** (file: `tests/test_advisor_cog.py`):

- [ ] **Step 1:** `test_analyze_rejects_oversized_attachment` -- Mock attachment with `size > 10_000_000`. Assert error embed sent.
- [ ] **Step 2:** `test_analyze_rejects_wrong_content_type` -- Mock attachment with `content_type="text/plain"`. Assert error embed sent.
- [ ] **Step 3:** `test_analyze_success_returns_top_3` -- Mock vision pipeline + engine to return 5 moves. Assert success embed contains top 3.
- [ ] **Step 4:** `test_analyze_no_moves_returns_no_moves_embed` -- Mock engine to return empty list. Assert `build_no_moves_embed` called.
- [ ] **Step 5:** `test_analyze_vision_error_returns_error_embed` -- Mock `extract_board_state` to raise `VisNError`. Assert error embed sent.
- [ ] **Step 6:** `test_analyze_unexpected_error_returns_generic_error` -- Mock engine to raise RuntimeError. Assert generic error embed.
- [ ] **Step 7:** `test_analyze_with_difficulty_below_100` -- Set channel difficulty to 50. Assert `difficulty_engine.select_move` called.
- [ ] **Step 8:** `test_setdifficulty_updates_channel_state` -- Call `setdifficulty(strength=75)`. Assert `channel_store.set_difficulty` called with correct args.
- [ ] **Step 9:** `test_setmode_updates_channel_state` -- Call `setmode(mode="classic")`. Assert `channel_store.set_mode` called.
- [ ] **Step 10:** `test_analyze_defers_response` -- Assert `interaction.response.defer(ephemeral=True)` called first.

---

### 4.2 ChannelStore (file: `src/bot/channel_state.py`)

**What it does:** Simple in-memory key-value store for per-channel settings (difficulty, mode).

**Tests to write** (file: `tests/test_channel_state.py`):

- [ ] **Step 1:** `test_get_creates_default_state` -- Call `store.get(12345)`. Assert returns `ChannelState(difficulty=100, mode="wild")`.
- [ ] **Step 2:** `test_get_same_channel_returns_same_object` -- Call `get(123)` twice. Assert same object (not a copy).
- [ ] **Step 3:** `test_set_difficulty_updates_and_returns` -- Call `set_difficulty(123, 50)`. Assert returned state has `difficulty=50`.
- [ ] **Step 4:** `test_set_mode_updates_and_returns` -- Call `set_mode(123, "classic")`. Assert returned state has `mode="classic"`.
- [ ] **Step 5:** `test_separate_channels_isolated` -- Set difficulty for channel 1, verify channel 2 still has default.

---

### 4.3 LetterLeagueBot (file: `src/bot/bot.py`)

**What it does:** discord.py Bot subclass. Loads GADDAG and DifficultyEngine in `setup_hook`. Syncs slash commands.

**Tests to write** (file: `tests/test_bot_init.py`):

- [ ] **Step 1:** `test_bot_init_stores_paths` -- Create bot with custom paths. Assert `wordlist_path` and `cache_path` stored.
- [ ] **Step 2:** `test_setup_hook_loads_gaddag` -- Mock GADDAG constructor. Call `setup_hook()`. Assert `self.gaddag` is set.
- [ ] **Step 3:** `test_setup_hook_loads_difficulty_engine` -- Assert `self.difficulty_engine` is set after `setup_hook()`.
- [ ] **Step 4:** `test_setup_hook_missing_wordlist_raises` -- Pass nonexistent wordlist path. Assert raises during `setup_hook()`.
- [ ] **Step 5:** `test_bot_creates_channel_store` -- Assert `self.channel_store` is a `ChannelStore` instance.

---

## 5. Remaining Tests: Vision Subsystem

---

### 5.1 Vision Extractor (file: `src/vision/extractor.py`)

**What it does:** Calls Claude Vision API with a screenshot, sends a structured prompt, and parses the JSON response into board state.

**Tests to write** (file: `tests/vision/test_extractor.py`):

- [ ] **Step 1:** `test_call_vision_api_success` -- Mock `anthropic.AsyncAnthropic().messages.create` to return a valid JSON response. Assert returned dict has expected keys.
- [ ] **Step 2:** `test_call_vision_api_retry_context_appended` -- Pass `retry_context="bad cells"`. Assert the prompt sent includes the error context string.
- [ ] **Step 3:** `test_call_vision_api_api_error_raises_visnerror` -- Mock API to raise `anthropic.APIError`. Assert `VisNError` with code `EXTRACTION_FAILED`.
- [ ] **Step 4:** `test_call_vision_api_unexpected_error_raises_visnerror` -- Mock API to raise `RuntimeError`. Assert `VisNError` raised.
- [ ] **Step 5:** `test_call_vision_api_logs_latency` -- Mock API. Assert logger output contains latency and token counts.

---

### 5.2 Vision Schema (file: `src/vision/schema.py`)

**What it does:** Defines Pydantic schemas for board extraction and the official multiplier layout constant.

**Tests to write** (file: `tests/vision/test_schema.py`):

- [ ] **Step 1:** `test_board_schema_valid_json_roundtrip` -- Create a valid board dict matching the schema. Assert it validates without error.
- [ ] **Step 2:** `test_board_schema_rejects_invalid_letter` -- Provide a cell with `letter: "1"`. Assert validation rejects it.
- [ ] **Step 3:** `test_official_multiplier_layout_dimensions` -- Assert `OFFICIAL_MULTIPLIER_LAYOUT` is 15x15 (or whatever the board size is).
- [ ] **Step 4:** `test_official_multiplier_layout_symmetry` -- Assert the layout is symmetric (standard Scrabble-style symmetry).

---

### 5.3 Vision Pipeline Integration (file: `src/vision/__init__.py`)

**What it does:** `extract_board_state()` chains preprocessor -> extractor -> validator with retry logic.

**Tests to write** (file: `tests/vision/test_pipeline.py`):

- [ ] **Step 1:** `test_pipeline_success_end_to_end` -- Mock `call_vision_api` to return valid data. Assert returns `(board, rack)` tuple.
- [ ] **Step 2:** `test_pipeline_retries_on_validation_failure` -- Mock first extraction to fail validation, second to pass. Assert API called twice.
- [ ] **Step 3:** `test_pipeline_raises_after_max_retries` -- Mock all extractions to fail validation. Assert raises `VisNError`.
- [ ] **Step 4:** `test_pipeline_preprocessor_called_first` -- Mock preprocessor. Assert image bytes are preprocessed before API call.

---

## 6. Remaining Tests: Misc Gaps

---

### 6.1 Vision Errors (file: `src/vision/errors.py`)

Low priority -- simple exception class. Optional tests:

- [ ] `test_visnerror_stores_code_and_message` -- Assert `VisNError(code, msg).code == code` and `.message == msg`.

---

### 6.2 Engine Models (file: `src/engine/models.py`)

Low priority -- frozen dataclasses. Indirectly tested everywhere. Optional tests:

- [ ] `test_move_rack_tiles_consumed` -- Create a Move, call `rack_tiles_consumed()`. Assert returns only TileUses with `from_rack=True`.

---

## 7. Recommended Testing Order

Work through these in order. Each step builds on the previous and increases confidence.

### Phase A: Pure Functions (no mocking needed)

These are the easiest wins -- no Playwright, no Discord, no API keys.

| Priority | What | File to Create | Estimated Tests |
|----------|------|---------------|----------------|
| A1 | CoordMapper | `tests/test_coord_mapper.py` | 9 |
| A2 | assign_rack_indices | (same file or `test_tile_placer_utils.py`) | 5 |
| A3 | jitter | (same file) | 2 |
| A4 | is_non_blank | `tests/test_capture.py` | 5 |
| A5 | ChannelStore | `tests/test_channel_state.py` | 5 |
| **Total** | | | **26** |

### Phase B: Mocked Subsystem Tests

These require `unittest.mock` but no external services.

| Priority | What | File to Create | Estimated Tests |
|----------|------|---------------|----------------|
| B1 | TilePlacer | `tests/test_tile_placer.py` | 12 |
| B2 | turn_detector (classify_frame) | `tests/test_turn_detector.py` | 11 |
| B3 | AdvisorCog | `tests/test_advisor_cog.py` | 10 |
| B4 | Vision extractor | `tests/vision/test_extractor.py` | 5 |
| B5 | Vision pipeline | `tests/vision/test_pipeline.py` | 4 |
| **Total** | | | **42** |

### Phase C: Infrastructure & Edge Cases

Lower priority -- fills remaining gaps.

| Priority | What | File to Create | Estimated Tests |
|----------|------|---------------|----------------|
| C1 | capture_canvas | `tests/test_capture.py` (append) | 3 |
| C2 | navigator | `tests/test_navigator.py` | 4 |
| C3 | BrowserSession | `tests/test_session.py` | 4 |
| C4 | LetterLeagueBot init | `tests/test_bot_init.py` | 5 |
| C5 | Vision schema | `tests/vision/test_schema.py` | 4 |
| C6 | Vision errors + engine models | inline in existing files | 2 |
| **Total** | | | **22** |

---

### Summary

| Phase | Tests to Write | Difficulty | Dependencies |
|-------|---------------|------------|--------------|
| **A** (Pure Functions) | 26 | Easy | None |
| **B** (Mocked Subsystems) | 42 | Medium | unittest.mock, pytest-asyncio |
| **C** (Infrastructure) | 22 | Medium-Hard | Mocking Playwright, discord.py, Anthropic |
| **Grand Total** | **90** | | |

After completing all phases, the project will have **~214 total tests** covering every module.

---

## Appendix: File-by-File Status

| Source File | Lines | Has Tests? | Test File | Remaining Work |
|------------|-------|-----------|-----------|----------------|
| `src/engine/__init__.py` | 138 | Yes | `test_engine.py` | None |
| `src/engine/board.py` | 306 | Yes | `test_board.py` | None |
| `src/engine/gaddag.py` | 170 | Yes | `test_gaddag.py` | None |
| `src/engine/models.py` | 100 | Indirect | (used everywhere) | Optional: `rack_tiles_consumed()` |
| `src/engine/moves.py` | 647 | Yes | `test_moves.py` | None |
| `src/engine/scoring.py` | 149 | Yes | `test_scoring.py` | None |
| `src/engine/tiles.py` | 34 | Indirect | (used everywhere) | None |
| `src/difficulty/__init__.py` | 6 | Yes | `test_difficulty.py` | None |
| `src/difficulty/engine.py` | 95 | Yes | `test_difficulty.py` | None |
| `src/difficulty/frequency.py` | 74 | Indirect | `test_difficulty.py` | None |
| `src/vision/__init__.py` | 139 | No | -- | Phase B5 |
| `src/vision/errors.py` | 20 | Indirect | (used in validator) | Optional |
| `src/vision/extractor.py` | 144 | No | -- | Phase B4 |
| `src/vision/preprocessor.py` | 122 | Yes | `test_preprocessor.py` | None |
| `src/vision/schema.py` | 225 | Indirect | (used in validator) | Phase C5 |
| `src/vision/validator.py` | 96 | Yes | `test_validator.py` | None |
| `src/bot/__init__.py` | 3 | -- | -- | N/A |
| `src/bot/autoplay_cog.py` | 332 | Yes | `test_autoplay_cog.py` | None |
| `src/bot/autoplay_state.py` | 39 | Yes | `test_autoplay_formatter.py` | None |
| `src/bot/bot.py` | 140 | No | -- | Phase C4 |
| `src/bot/channel_state.py` | 67 | No | -- | Phase A5 |
| `src/bot/cog.py` | 233 | No | -- | Phase B3 |
| `src/bot/formatter.py` | 320 | Yes | `test_autoplay_formatter.py` | None |
| `src/browser/__init__.py` | 20 | -- | -- | N/A |
| `src/browser/capture.py` | 91 | No | -- | Phase A4 + C1 |
| `src/browser/navigator.py` | 252 | No | -- | Phase C2 |
| `src/browser/session.py` | 125 | No | -- | Phase C3 |
| `src/browser/tile_placer.py` | 596 | No | -- | Phase A1-A3 + B1 |
| `src/browser/turn_detector.py` | 266 | No | -- | Phase B2 |
