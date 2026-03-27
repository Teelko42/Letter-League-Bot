---
phase: 07-tile-placement
verified: 2026-03-26T18:15:00Z
status: human_needed
score: 9/9 must-haves verified
human_verification:
  - test: "Run calibrate_placement.py with a live game screenshot, update fractional constants in tile_placer.py, then observe bot placing a 3-5 letter word"
    expected: "Each rack tile drags from the correct rack slot to the correct board cell with human-like pacing (1-3s between tiles)"
    why_human: "Fractional constants are calibrated PLACEHOLDER values — accuracy of coordinate mapping cannot be verified without a live game canvas at known resolution"
  - test: "After placing a valid word and clicking confirm, observe the game UI for the confirmation result"
    expected: "Tiles remain on board and score updates (word accepted); if rejected, bot recalls tiles and tries next word"
    why_human: "classify_frame acceptance detection depends on live visual state; cannot verify correct board state diff programmatically without running against real game"
  - test: "Trigger a word rejection scenario (e.g., intentionally place an invalid word) and verify the retry loop"
    expected: "Bot recalls tiles, logs rejection, then attempts next candidate move (up to 3 tries), then falls back to tile swap"
    why_human: "Retry flow requires live game feedback (rejection signal from classify_frame); cannot simulate without running patchright against live Discord"
---

# Phase 7: Tile Placement Verification Report

**Phase Goal:** The bot translates a chosen word move into a sequence of pixel clicks that correctly places tiles on the board and submits the play via the game UI
**Verified:** 2026-03-26T18:15:00Z
**Status:** human_needed (all automated checks passed; 3 items require live game observation)
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | CoordMapper computes board cell pixel coordinates from canvas bounding box and fractional constants | VERIFIED | `board_cell_px(0,0)` on bbox `{x:0,y:0,w:1000,h:600}` returns `(30.0, 12.0)` matching `GRID_X0_FRAC*1000, GRID_Y0_FRAC*600`; formula verified programmatically |
| 2 | CoordMapper computes rack tile pixel coordinates from canvas bounding box and fractional constants | VERIFIED | `rack_tile_px(0)` returns `(150.0, 552.0)` matching `RACK_X0_FRAC*1000, RACK_Y_FRAC*600`; confirmed programmatically |
| 3 | TilePlacer drags tiles from rack slots to board cells using page.mouse.down/move/up sequence | VERIFIED | `_drag_tile` at lines 261-285 executes `mouse.move -> mouse.down -> asyncio.sleep(0.05) -> mouse.move(steps=10) -> mouse.up` exactly as specified |
| 4 | Each tile placement is verified via screenshot pixel-diff with one retry on failure | VERIFIED | `_verify_placement` at lines 287-316 uses `capture_canvas` + OpenCV mean absolute diff > 1.0; retry logic at lines 388-406 |
| 5 | Rack tile selection uses leftmost-available-duplicate matching with blank tile ('?') handling | VERIFIED | `assign_rack_indices(['A','B','A','C'], [TileUse(0,0,'A',False,True), TileUse(0,1,'A',False,True)])` returns `[0, 2]`; blank handling confirmed at line 198 |
| 6 | Human-like jitter (+/-3px) and delay (1-3s) applied to every drag action | VERIFIED | `jitter()` at lines 150-167 applies `random.uniform(-px, px)`; inter-tile delay `random.uniform(1.0, 3.0)` at line 417; all drag calls use jitter (lines 366, 367, 397, 398) |
| 7 | After all tiles are placed, the bot clicks the confirm button at its fractional canvas position | VERIFIED | `_click_confirm` at lines 421-432 calls `jitter(*mapper.confirm_btn_px())` then `page.mouse.click`; wired in `place_move` at line 548 |
| 8 | The bot detects acceptance (turn ended) vs rejection (still my turn) via classify_frame after 1-2s wait | VERIFIED | `_wait_for_acceptance` at lines 434-452: `asyncio.sleep(random.uniform(1.0, 2.0))`, captures screenshot, calls `classify_frame()`, returns `state != "my_turn"` |
| 9 | On rejection, the bot clears placed tiles and retries; after 3 failed attempts, falls back to tile swap | VERIFIED | `place_move` at lines 486-578: iterates `moves[:MAX_WORD_RETRIES]` (3), calls `_recall_tiles` on rejection (line 568), falls through to `_tile_swap` (line 577) when all attempts exhausted |

**Score:** 9/9 truths verified

### Required Artifacts

| Artifact | Min Lines | Actual Lines | Status | Details |
|----------|-----------|--------------|--------|---------|
| `src/browser/tile_placer.py` | 250 (Plan 02) | 578 | VERIFIED | Contains CoordMapper (5 methods), TilePlacer (8 methods), assign_rack_indices, jitter, PlacementError |
| `scripts/calibrate_placement.py` | 40 (Plan 01) | 167 | VERIFIED | Interactive OpenCV calibration tool; computes and prints 9 fractional constants as paste-ready Python block |
| `src/browser/__init__.py` | contains "TilePlacer" | — | VERIFIED | Line 7: `from src.browser.tile_placer import TilePlacer, PlacementError`; both in `__all__` |

### Key Link Verification

| From | To | Via | Pattern | Status | Details |
|------|----|-----|---------|--------|---------|
| `src/browser/tile_placer.py` | `src/browser/capture.py` | import capture_canvas for per-tile verification screenshots | `from src\.browser\.capture import capture_canvas` | WIRED | Line 11: direct top-level import; used at lines 301, 382, 396, 449 |
| `src/browser/tile_placer.py` | `src/engine/models.py` | import Move, TileUse for type annotations and rack_tiles_consumed() | `from src\.engine\.models import` | WIRED | Line 15: TYPE_CHECKING guard for Move, TileUse; runtime import at line 344; `move.rack_tiles_consumed()` at line 349 |
| `src/browser/tile_placer.py` | `src/browser/turn_detector.py` | import classify_frame for post-confirm acceptance detection | `from src\.browser\.turn_detector import classify_frame` | WIRED | Line 12: direct top-level import; used at line 450 inside `_wait_for_acceptance` |
| `src/browser/__init__.py` | `src/browser/tile_placer.py` | re-exports TilePlacer and PlacementError | `from src\.browser\.tile_placer import` | WIRED | Line 7: import confirmed; both names in `__all__` (lines 18-19); package import test passed |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| TILE-01 | 07-01-PLAN.md | Bot computes pixel coordinates for board cells and rack tiles from canvas bounding box | SATISFIED | `CoordMapper.board_cell_px()` and `rack_tile_px()` verified programmatically; no hardcoded absolute coords — all fractional |
| TILE-02 | 07-01-PLAN.md | Bot clicks rack tiles and board cells to place a chosen word move | SATISFIED | `TilePlacer.place_tiles()` at lines 322-419 executes full drag sequence: rack slot -> board cell for all `move.rack_tiles_consumed()` tiles |
| TILE-03 | 07-02-PLAN.md | Bot confirms word placement via the game's UI confirmation mechanism | SATISFIED | `place_move()` at lines 486-578 implements full confirm -> accept/reject -> retry -> tile swap pipeline; `_click_confirm` clicks confirm button; `_wait_for_acceptance` uses `classify_frame` |

No orphaned requirements: TILE-01, TILE-02, TILE-03 are the only requirements mapped to Phase 7 in REQUIREMENTS.md (traceability table, lines 83-85). All three are claimed and satisfied.

### Anti-Patterns Found

| File | Lines | Pattern | Severity | Impact |
|------|-------|---------|----------|--------|
| `src/browser/tile_placer.py` | 21, 35-38 | PLACEHOLDER comment on fractional constants | INFO (by design) | GRID, RACK, CONFIRM constants on lines 24-32 are labeled placeholder pending live calibration; RECALL/SWAP constants on lines 35-38 also placeholder. The `calibrate_placement.py` script is the operator's tool to replace these. This is intentional per PLAN 01 Task 1 specification and Success Criterion #1 — not a stub. |

No empty implementations, no console.log-only handlers, no `return null`/`return {}` stubs found.

### Human Verification Required

#### 1. Coordinate Accuracy After Calibration

**Test:** Run `python scripts/calibrate_placement.py <screenshot.png>` with a live game screenshot. Update the printed constants into `src/browser/tile_placer.py`. Then trigger `place_tiles()` for a known word.
**Expected:** Rack tiles drag from the correct slot positions to the correct board cells; tiles land visibly on the board without missing target cells.
**Why human:** Fractional constants are still PLACEHOLDER values (lines 24-32, 35-38). The coordinate math is verified correct but the actual numeric values depend on live canvas geometry measurements. Accuracy requires operator calibration first.

#### 2. Confirm Click and Acceptance Detection

**Test:** Place a valid word, observe the confirm button click, and watch for game response (score update or word-rejected indicator).
**Expected:** `_click_confirm` hits the confirm button; `_wait_for_acceptance` correctly returns True (turn ended) or False (still my_turn) based on the live visual state.
**Why human:** `classify_frame` wraps a trained HSV/visual classifier. Whether it correctly distinguishes "accepted" from "rejected" in the post-confirm UI state requires live game observation. Cannot simulate this without running patchright against Discord.

#### 3. Rejection Recovery and Tile Swap Fallback

**Test:** Force a rejection scenario (play an invalid word or a word rejected by the game). Observe the retry loop. If all 3 attempts fail, observe tile swap.
**Expected:** Bot calls `_recall_tiles` after each rejection, tries the next candidate word, and falls back to `_tile_swap` after 3 failures. No hang or uncaught exception.
**Why human:** The retry flow depends on `classify_frame` returning `"my_turn"` on rejection — requires live game feedback. Tile swap correctness also depends on SWAP button coordinates being calibrated.

### Gaps Summary

No gaps. All 9 observable truths are verified. All 3 artifacts pass all three levels (exists, substantive, wired). All 4 key links are wired. All 3 requirements (TILE-01, TILE-02, TILE-03) are satisfied with implementation evidence.

The PLACEHOLDER fractional constants are informational only — they are an explicit design decision in both PLAN files. The `calibrate_placement.py` tool delivers the means to replace them. This does not block the goal since the coordinate math is correct and the calibration workflow is complete.

Three items are flagged for human verification because they require live game execution (patchright driving Discord) to confirm: coordinate accuracy post-calibration, confirm acceptance detection, and the rejection retry loop.

---

_Verified: 2026-03-26T18:15:00Z_
_Verifier: Claude (gsd-verifier)_
