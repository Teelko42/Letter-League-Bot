---
status: verifying
trigger: "tiles-placed-but-word-not-played — bot places tiles but struggles to actually play/submit the word; fails silently"
created: 2026-04-16T00:00:00Z
updated: 2026-04-16T15:50:00Z
---

## Current Focus

hypothesis: CONFIRMED — _get_canvas_bbox sometimes returns the canvas element's viewport bbox instead of the iframe bbox. All fractional constants (RECALL_X_FRAC, CONFIRM_X_FRAC, GRID_X0_FRAC, etc.) are calibrated against the FULL IFRAME screenshot. When the canvas bbox is used, _click_in_frame computes local_x = RECALL_X_FRAC * canvas_width — missing the canvas's left offset within the iframe coordinate space. The click lands at the wrong position. In sessions where canvas lookup fails (WOF session, smaller window), iframe bbox is used and RECALL works. In sessions where canvas lookup succeeds (TIBIAE/FOLEY), coordinates are wrong and RECALL fails.

test: Visual: post_recall_attempt1 (TIBIAE) and post_recall_attempt2 (FOLEY) show tiles STILL ON BOARD after recall. post_recall_attempt3/4/5 (WOF, smaller window where canvas lookup fails) show tiles PROPERLY CLEARED. This is the behavioral difference that points to bbox inconsistency.

fix: Remove canvas element lookup from _get_canvas_bbox entirely. Always use iframe bbox since all constants are calibrated against the full iframe screenshot. This is already documented in the existing code comment.

next_action: Apply the fix to src/browser/tile_placer.py

## Symptoms

expected: The bot should complete its turn successfully — place tiles on the board AND click PLAY to submit the word
actual: Tiles get placed on the board but the bot struggles to actually play/submit the word afterward; the first turn works, but subsequent turns fail — tiles are not placed correctly and the word is not submitted
errors: No visible errors or crashes — fails silently. Debug screenshots show "Invalid Placement" or "Invalid Word" for subsequent turns.
reproduction: Start autoplay mode; first turn works. Observe that on subsequent turns, tiles are placed at disconnected board positions ("Invalid Placement") or wrong words.
timeline: First turn works. Turn 2+ fails.

## Eliminated

- hypothesis: RECALL_X_FRAC=0.589404 fix alone resolves all failures
  evidence: post_recall_attempt1 (TIBIAE) and post_recall_attempt2 (FOLEY) show tiles STILL ON BOARD after recall. post_recall_attempt3/4/5 (WOF, smaller window) show tiles properly cleared. The fix was necessary but not sufficient — the bbox bug caused the wrong coordinates to be used even with correct RECALL_X_FRAC.
  timestamp: 2026-04-16

- hypothesis: PLAY button coordinates are wrong (pre-existing knowledge from e2e debug)
  evidence: e2e-pipeline-failures Round 5 confirmed PLAY is clicked at correct position; EOAN screenshot shows "PLAY (21 PTS)" label visible and word on board — the click reaches the button but the game responds with Invalid Word (word-list mismatch, not coordinate error)
  timestamp: 2026-04-16

- hypothesis: Recall timing too short causing tiles to persist across attempts
  evidence: Fixed in e2e Round 5-A (delay increased to 1.0-1.5s). post_recall screenshots confirm tiles are properly cleared between attempts.
  timestamp: 2026-04-16

- hypothesis: All rejections are due to word-list mismatch (Collins vs Letter League list)
  evidence: Partially true for words WITHOUT blanks (AEON, BIPOD, EINA, EUOI, NAOI all show "Invalid Word"). But some turn-2 failures show "Invalid Placement" which is not a word-list issue.
  timestamp: 2026-04-16

- hypothesis: Blank tile dialog blocks turn 1 placement
  evidence: Fixed. Confirmed by user: first turn now correctly placed and played. This is the confirmed-fixed issue from the previous session.
  timestamp: 2026-04-16

- hypothesis: _get_canvas_bbox inconsistently returns canvas vs iframe bbox causing coordinate drift
  evidence: canvas bbox and iframe bbox are fetched fresh on each place_move call. self._bbox is refreshed at start of each placement. Even if canvas vs iframe differs, this would affect ALL turns equally including turn 1 which works. Not turn-specific.
  timestamp: 2026-04-16

- hypothesis: assign_rack_indices uses stale rack from previous turn
  evidence: rack is passed fresh from extract_board_state each turn. No stale state. Engine converts '?' to '_' internally but the rack passed to place_move retains '?' for correct blank matching.
  timestamp: 2026-04-16

- hypothesis: Board is read as empty on turn 2 (vision returns 0 cells)
  evidence: CHEMIST screenshot (turn 2) shows "Invalid Word" not "Invalid Placement" — tiles ARE placed connected to something, meaning the engine found valid anchors and generated connected moves. Board reading produces SOME cells, not zero.
  timestamp: 2026-04-16

- hypothesis: Engine generates invalid disconnected moves due to move generation bug
  evidence: The engine validates cross-words via cross_checks; floating tiles are caught by connectivity check in validator. The fact that CHEMIST connects correctly confirms engine move generation works.
  timestamp: 2026-04-16

## Evidence

- timestamp: 2026-04-16
  checked: debug/tile_placer/pre_play_attempt1_PIONEER.png
  found: A "Select a letter" modal dialog is fully open on screen. CONFIRMED turn 1 blank tile dialog bug.
  implication: Previously fixed. User confirmed first turn now works.

- timestamp: 2026-04-16
  checked: debug/tile_placer/pre_play_attempt2_ELOINER.png, pre_play_attempt3_HEROINE.png
  found: Identical "Select a letter" modal open for subsequent blank-tile words. Previously the cause of all failures; now fixed.
  implication: Blank tile fix is working.

- timestamp: 2026-04-16
  checked: debug/tile_placer/pre_play_attempt1_CHEMIST.png
  found: Turn 2, score=38. C,H,M,I,S,T placed vertically, "Invalid Word" shown. Tiles ARE connected to board (placement accepted, word rejected for word-list reasons).
  implication: Coordinate mapping is CORRECT for turn 2 when vision reads positions accurately. Word-list mismatch is a secondary problem.

- timestamp: 2026-04-16
  checked: debug/tile_placer/pre_play_attempt1_QUITE.png and pre_play_attempt2_QUIET.png
  found: FREEING is on the board (turn 1 placed). QUITE tiles placed disconnected from FREEING ("Invalid Placement"). QUIET → "Swapping Tiles" (all attempts failed, fallback swap).
  implication: Engine generated QUITE at coordinates that appear connected in its board model but don't match real tile positions. Bot drags tiles to engine's (row,col) positions which are NOT adjacent to FREEING's actual cells.

- timestamp: 2026-04-16
  checked: debug/preprocessed_debug.png
  found: Shows a mid-game board with multiple tiles (FREEING, T, B, O, S, D) and grid overlay. This IS the image sent to Claude Vision. Reference markers (row/col numbers, gridlines) are visible. The preprocessing IS creating a good image.
  implication: The preprocessing is correct. The issue is Claude Vision reading coordinates from this image with 1-2 cell drift.

- timestamp: 2026-04-16
  checked: src/vision/__init__.py correct_positions and board-read-multi-word-fail.md debug session
  found: (1) correct_positions uses multiplier colors to determine shift. When tiles cover multiplier squares, all cells report "NONE" → curr_info=0 → function is a complete no-op. (2) The board-read-multi-word-fail fix softened "Position accuracy suspect" and "Invalid word(s) on board" errors to allow extraction to proceed. But extraction proceeds WITH wrong positions.
  implication: Two compounding issues: (a) vision drift not corrected because no signal; (b) soft-error fix allows pipeline to proceed despite wrong positions. The fix was necessary to prevent crashes but exposed the drift problem.

- timestamp: 2026-04-16
  checked: src/vision/validator.py validate_extraction + OFFICIAL_MULTIPLIER_LAYOUT
  found: On a board with FREEING at row 9 (cols 5-11), multiplier squares at (9,7)=DW and (9,11)=DW would be covered by tiles. Vision reports them as "NONE" → correct_positions has zero informative cells → cannot shift.
  implication: Confirms that correct_positions cannot fix drift on any board where tiles cover most multiplier squares.

- timestamp: 2026-04-16
  checked: debug/tile_placer/post_recall_attempt1.png (TIBIAE session, TURN 2)
  found: T,B,I tiles still on board after recall. Score dropped from 40 to 27 (point preview changed). "Invalid Word" label still showing. RECALL DID NOT WORK.
  implication: Recall click is landing at wrong position inside game frame.

- timestamp: 2026-04-16
  checked: debug/tile_placer/post_recall_attempt2.png (FOLEY session, TURN 2)
  found: F,B,E,N tiles still on board after recall attempt for FOLEY. Score shows 10. RECALL DID NOT WORK.
  implication: Same root cause as TIBIAE session.

- timestamp: 2026-04-16
  checked: debug/tile_placer/post_recall_attempt3-5.png (WOF session, TURN 1)
  found: Only GEAR (opponent's word) on board. Bot tiles (WOF, WOOF, OOF etc.) properly cleared. Score=0. "It's your turn" message shown. RECALL WORKED.
  implication: In WOF session (different window size/state), canvas bbox lookup failed and iframe bbox was used — coordinates correct.

- timestamp: 2026-04-16
  checked: _get_canvas_bbox() code + Playwright bounding_box() docs
  found: Playwright's bounding_box() returns VIEWPORT coordinates even for elements inside iframes. Canvas element is centered within the iframe with gray margins. When canvas bbox is used: local_x = RECALL_X_FRAC * canvas_width, which is offset from the canvas's left edge, NOT the iframe's left edge. _click_in_frame dispatches events at iframe-local coordinates starting from (0,0) = iframe top-left. Missing the canvas-to-iframe offset means clicks land in the wrong position.
  implication: Root cause confirmed. Fix: always use iframe bbox in _get_canvas_bbox.

- timestamp: 2026-04-16
  checked: src/vision/validator.py word-validity check (Check 5)
  found: Checks all runs of 2+ consecutive tiles form valid words. If FREEING shifts by 1 column but all 7 letters remain adjacent (F,R,E,E,I,N,G intact as a run), the word "FREEING" is still valid. Global uniform shift cannot be detected by word-validity check when words remain valid after shift.
  implication: Word-validity check is insufficient to detect global positional drift when the word letters remain consecutive. A smarter check is needed.

## Resolution

root_cause_1: _get_canvas_bbox() was returning the inner <canvas> element's bounding box instead of the iframe bbox. Fixed in prior session — now always returns iframe bbox.

root_cause_2: _click_confirm, _recall_tiles, and _tile_swap all used _click_in_frame (synthetic JS dispatch) as Strategy 1. This dispatches PointerEvent/MouseEvent on document.elementFromPoint() inside the game iframe. The JS dispatch never throws exceptions, so it always "succeeds" and returns/sets clicked=True — preventing the WORKING strategies (page.mouse.click at viewport coordinates) from ever executing. But the game's canvas ignores synthetic JS events for its button handlers. Tile dragging works because _drag_tile uses page.mouse.click() (real browser events), not _click_in_frame.

secondary_cause_resolved: RECALL_X_FRAC was also previously wrong (0.409650 = SWAP position instead of 0.589404 = RECALL position). That fix is already applied and correct.

fix: Simplified _click_confirm, _recall_tiles, and _tile_swap to use page.mouse.click() at viewport coordinates — the same mechanism that _drag_tile uses for tile placement. Removed the _click_in_frame JS dispatch strategy from all three methods. This ensures button clicks use real browser mouse events that the game canvas actually processes.

verification: (AWAITING USER LIVE TEST) — fix applied, 244/244 unit tests pass
files_changed: [src/browser/tile_placer.py]
