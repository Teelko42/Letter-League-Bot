# Auto-debug iteration 3

- exit_code: `-9`
- duration: 4195.8s
- error_signature: `4713a6f9b244`

## Recent debug artifacts
- `debug/tile_placer/pre_play_attempt2_RUGGY.png`
- `debug/tile_placer/post_recall_attempt1.png`
- `debug/tile_placer/pre_play_attempt1_GRUNGY.png`
- `debug/turn_detection/frame_20260428_133141_949567_pre_start_attempt1.png`
- `debug/turn_detection/frame_20260428_122307_048398_pre_start_attempt1.png`
- `debug/iframe_missing.png`

## Autoplay log — error region
```
2026-04-28 12:42:57.559 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.0815
2026-04-28 12:42:57.560 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'U' placement not verified — retrying with fresh jitter
2026-04-28 12:42:58.584 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 123733 bytes (attempt 1)
2026-04-28 12:43:00.494 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 123729 bytes (attempt 1)
2026-04-28 12:43:00.621 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.0035
2026-04-28 12:43:00.622 | ERROR   | src.browser.tile_placer:place_move:1074 | Tile placement failed for 'CURF' (attempt 5): Tile 'U' at (8,16) failed to place after retry
2026-04-28 12:43:00.781 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 12:43:01.656 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 123966 bytes (attempt 1)
2026-04-28 12:43:01.657 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.8, 753.4) (pass 1/10)
2026-04-28 12:43:03.688 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 124232 bytes (attempt 1)
2026-04-28 12:43:03.811 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.5, 752.7) (pass 2/10)
2026-04-28 12:43:05.752 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 123587 bytes (attempt 1)
2026-04-28 12:43:05.872 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.5, 752.9) (pass 3/10)
2026-04-28 12:43:07.730 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 124147 bytes (attempt 1)
2026-04-28 12:43:07.848 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.8, 753.9) (pass 4/10)
2026-04-28 12:43:09.919 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 123864 bytes (attempt 1)
2026-04-28 12:43:10.031 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.3, 753.5) (pass 5/10)
2026-04-28 12:43:12.007 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 123536 bytes (attempt 1)
2026-04-28 12:43:12.125 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.3, 751.9) (pass 6/10)
2026-04-28 12:43:14.154 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 123761 bytes (attempt 1)
2026-04-28 12:43:14.279 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.0, 748.0) (pass 7/10)
2026-04-28 12:43:16.128 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 123749 bytes (attempt 1)
2026-04-28 12:43:16.249 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.2, 752.9) (pass 8/10)
2026-04-28 12:43:18.189 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 123083 bytes (attempt 1)
2026-04-28 12:43:18.321 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.4, 751.1) (pass 9/10)
2026-04-28 12:43:20.261 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122972 bytes (attempt 1)
2026-04-28 12:43:20.385 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.4, 753.5) (pass 10/10)
2026-04-28 12:43:22.400 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122557 bytes (attempt 1)
2026-04-28 12:43:22.520 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 12:43:23.381 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122533 bytes (attempt 1)
2026-04-28 12:43:23.385 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt5.png
2026-04-28 12:43:23.386 | WARNING | src.browser.tile_placer:place_move:1122 | All 5 word attempt(s) failed — performing tile swap fallback
2026-04-28 12:43:23.508 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 12:43:23.509 | WARNING | src.browser.tile_placer:_tile_swap:993 | Falling back to tile swap at (1010.3, 751.6) — no valid words accepted after 5 attempts
2026-04-28 12:43:23.542 | INFO    | __main__:_run:270 | Turn 4: no move accepted (swap/skip)
2026-04-28 12:43:27.105 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121687 bytes (attempt 1)
2026-04-28 12:43:27.233 | INFO    | src.browser.turn_detector:poll_turn:648 | Turn state changed: None -> my_turn
2026-04-28 12:43:27.387 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 12:43:28.274 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122444 bytes (attempt 1)
2026-04-28 12:43:29.170 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121434 bytes (attempt 1)
2026-04-28 12:43:29.171 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1285.4, 752.8) (pass 1/10)
2026-04-28 12:43:31.286 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121613 bytes (attempt 1)
2026-04-28 12:43:31.444 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1286.7, 753.8) (pass 2/10)
2026-04-28 12:43:33.380 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121892 bytes (attempt 1)
2026-04-28 12:43:33.529 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1285.6, 753.7) (pass 3/10)
2026-04-28 12:43:35.563 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121717 bytes (attempt 1)
2026-04-28 12:43:35.730 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1285.4, 752.2) (pass 4/10)
2026-04-28 12:43:37.782 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122419 bytes (attempt 1)
2026-04-28 12:43:37.939 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1283.7, 752.4) (pass 5/10)
2026-04-28 12:43:39.959 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122385 bytes (attempt 1)
2026-04-28 12:43:40.084 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1283.1, 748.3) (pass 6/10)
2026-04-28 12:43:41.992 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122297 bytes (attempt 1)
2026-04-28 12:43:42.111 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1288.2, 753.7) (pass 7/10)
2026-04-28 12:43:44.106 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122666 bytes (attempt 1)
2026-04-28 12:43:44.648 | INFO    | src.browser.tile_placer:clear_stale_placements:973 | Pre-turn recall complete after 7 click(s) — canvas stable
2026-04-28 12:43:48.246 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122772 bytes (attempt 1)
2026-04-28 12:43:48.247 | INFO    | src.vision:extract_board_state:125 | Vision pipeline start — mode=wild
2026-04-28 12:43:48.318 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,54) 1366×657 from 1545×768 canvas
2026-04-28 12:43:48.598 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-04-28 12:43:48.772 | INFO    | src.vision:extract_board_state:131 | Preprocessing complete — 384264 bytes
2026-04-28 12:43:48.773 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=False
2026-04-28 12:43:54.257 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=5.48s  input_tokens=2903  output_tokens=306
2026-04-28 12:43:54.257 | INFO    | src.vision:extract_board_state:137 | Extraction complete (first attempt)
2026-04-28 12:43:54.258 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,12)=T*[DL] (9,13)=O[DW] (9,14)=W[DL] (9,15)=E[DL] (9,16)=R[DL] (9,17)=E[DL] (9,18)=D[DL] (10,12)=P[TL] (10,13)=I[DL] (10,14)=X[TL]
2026-04-28 12:43:54.259 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['Y', 'G', 'F', 'G', 'C', 'U', 'N']
2026-04-28 12:43:54.259 | DEBUG   | src.vision.validator:correct_positions:92 | Position auto-correction skipped: insufficient evidence (matches=4, informative=10, threshold=2 or 50%)
2026-04-28 12:43:54.260 | DEBUG   | src.vision.validator:correct_positions_gaddag:317 | GADDAG position correction: no shift improves word validity (current 3/5 valid runs)
2026-04-28 12:43:54.260 | INFO    | src.vision:extract_board_state:155 | Validation result — 2 error(s)
2026-04-28 12:43:54.262 | WARNING | src.vision:extract_board_state:181 | Validation failed (2 errors), retrying: ['Position accuracy suspect: 8/10 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.', "Invalid word(s) on board: 'TP' at col 12 rows 9-10, 'WX' at col 14 rows 9-10 — tile positions are likely off by 1. Re-count carefully from center star at (9,13)."]
2026-04-28 12:43:54.265 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=True
2026-04-28 12:44:00.605 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=6.34s  input_tokens=3022  output_tokens=306
2026-04-28 12:44:00.606 | INFO    | src.vision:extract_board_state:187 | Extraction complete (retry)
2026-04-28 12:44:00.609 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,12)=T*[TL] (9,13)=O[DW] (9,14)=W[TL] (9,15)=E[DL] (9,16)=R[DL] (9,17)=E[DL] (9,18)=D[DL] (10,11)=P[TL] (10,12)=I[DL] (10,13)=X[TL]
2026-04-28 12:44:00.609 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['Y', 'G', 'F', 'G', 'C', 'U', 'N']
2026-04-28 12:44:00.610 | DEBUG   | src.vision.validator:correct_positions:92 | Position auto-correction skipped: insufficient evidence (matches=4, informative=10, threshold=2 or 50%)
2026-04-28 12:44:00.610 | INFO    | src.vision:extract_board_state:205 | Merged 1 cell(s) from first attempt that retry dropped: [('X', 10, 14)]
2026-04-28 12:44:00.613 | INFO    | src.vision:extract_board_state:234 | Validation result after retry — 2 error(s)
2026-04-28 12:44:00.614 | WARNING | src.vision:extract_board_state:283 | Word validity check failed (1 word(s)) after retry — proceeding with best-effort extraction: ["Invalid word(s) on board: 'WX' at col 14 rows 9-10, 'PIXX' at row 10 cols 11-14 — tile positions are likely off by 1. Re-count carefully from center star at (9,13)."]
2026-04-28 12:44:00.615 | WARNING | src.vision:extract_board_state:294 | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 10/11 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
2026-04-28 12:44:00.637 | INFO    | src.vision:extract_board_state:328 | Vision pipeline complete — 12.39s  tiles=11  rack_size=7
2026-04-28 12:44:00.701 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 10 blacklisted candidate(s)
2026-04-28 12:44:00.704 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 1/5: 'GRUNGY' (score=22)
2026-04-28 12:44:00.857 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 12:44:00.858 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'G' (slot 1) -> board (8,16) | src=(1034.9,828.3) dst=(1295.0,460.2)
2026-04-28 12:44:01.858 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122445 bytes (attempt 1)
2026-04-28 12:44:03.619 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 125030 bytes (attempt 1)
2026-04-28 12:44:03.751 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.9669
2026-04-28 12:44:03.752 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'G' verified at (8,16)
2026-04-28 12:44:04.171 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 5) -> board (10,16) | src=(1259.3,827.4) dst=(1298.4,529.5)
2026-04-28 12:44:05.210 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 132224 bytes (attempt 1)
2026-04-28 12:44:06.973 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 126822 bytes (attempt 1)
2026-04-28 12:44:07.092 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6065
2026-04-28 12:44:07.092 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (10,16)
2026-04-28 12:44:07.538 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 6) -> board (11,16) | src=(1309.4,829.1) dst=(1299.1,561.5)
2026-04-28 12:44:08.478 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 125188 bytes (attempt 1)
2026-04-28 12:44:11.307 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 132449 bytes (attempt 1)
2026-04-28 12:44:11.598 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8062
2026-04-28 12:44:11.603 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (11,16)
2026-04-28 12:44:12.188 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'G' (slot 3) -> board (12,16) | src=(1148.0,830.8) dst=(1300.2,596.5)
2026-04-28 12:44:13.016 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 128807 bytes (attempt 1)
2026-04-28 12:44:14.736 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 124992 bytes (attempt 1)
2026-04-28 12:44:14.859 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.2283
2026-04-28 12:44:14.860 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'G' verified at (12,16)
2026-04-28 12:44:15.344 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'Y' (slot 0) -> board (13,16) | src=(980.2,828.8) dst=(1296.5,635.9)
2026-04-28 12:44:17.079 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 131495 bytes (attempt 1)
2026-04-28 12:44:18.928 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 125993 bytes (attempt 1)
2026-04-28 12:44:19.121 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6873
2026-04-28 12:44:19.122 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'Y' verified at (13,16)
2026-04-28 12:44:20.042 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 128135 bytes (attempt 1)
2026-04-28 12:44:20.047 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt1_GRUNGY.png
2026-04-28 12:44:21.186 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 12:44:21.187 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1148.4, 753.9)
2026-04-28 12:44:22.702 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121168 bytes (attempt 1)
2026-04-28 12:44:22.825 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 12:44:22.825 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 12:44:22.826 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1144.7, 750.0)
2026-04-28 12:44:24.318 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 120388 bytes (attempt 1)
2026-04-28 12:44:24.453 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 12:44:26.944 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 118698 bytes (attempt 1)
2026-04-28 12:44:27.057 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 12:44:27.058 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'GRUNGY' rejected (attempt 1/5) — recalling tiles
2026-04-28 12:44:27.061 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'grungy' (total: 148)
2026-04-28 12:44:27.870 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 119159 bytes (attempt 1)
2026-04-28 12:44:27.871 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.9, 753.7) (pass 1/10)
2026-04-28 12:44:29.961 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 119680 bytes (attempt 1)
2026-04-28 12:44:30.092 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.6, 749.4) (pass 2/10)
2026-04-28 12:44:32.063 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 119868 bytes (attempt 1)
2026-04-28 12:44:32.191 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.7, 749.4) (pass 3/10)
2026-04-28 12:44:34.234 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 120512 bytes (attempt 1)
2026-04-28 12:44:34.361 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.7, 750.6) (pass 4/10)
2026-04-28 12:44:36.257 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 119860 bytes (attempt 1)
2026-04-28 12:44:36.378 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.6, 752.4) (pass 5/10)
2026-04-28 12:44:38.169 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 119025 bytes (attempt 1)
2026-04-28 12:44:38.333 | INFO    | src.browser.tile_placer:_recall_tiles:891 | Recall complete after 5 click(s) — canvas stable
2026-04-28 12:44:39.162 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 119940 bytes (attempt 1)
2026-04-28 12:44:39.167 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-04-28 12:44:39.168 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 2/5: 'RUGGY' (score=20)
2026-04-28 12:44:39.472 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 12:44:39.472 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 5) -> board (10,16) | src=(1258.6,825.5) dst=(1295.5,527.6)
2026-04-28 12:44:40.317 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 119867 bytes (attempt 1)
2026-04-28 12:44:42.314 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 120618 bytes (attempt 1)
2026-04-28 12:44:42.447 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6381
2026-04-28 12:44:42.448 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (10,16)
2026-04-28 12:44:42.904 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'G' (slot 1) -> board (11,16) | src=(1037.9,827.8) dst=(1295.1,563.4)
2026-04-28 12:44:43.844 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121412 bytes (attempt 1)
2026-04-28 12:44:45.632 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121445 bytes (attempt 1)
2026-04-28 12:44:45.741 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.2476
2026-04-28 12:44:45.742 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'G' verified at (11,16)
2026-04-28 12:44:46.288 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'G' (slot 3) -> board (12,16) | src=(1147.1,831.1) dst=(1298.3,598.0)
2026-04-28 12:44:47.400 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121519 bytes (attempt 1)
2026-04-28 12:44:49.225 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121135 bytes (attempt 1)
2026-04-28 12:44:49.437 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5202
2026-04-28 12:44:49.438 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'G' verified at (12,16)
2026-04-28 12:44:49.901 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'Y' (slot 0) -> board (13,16) | src=(981.4,830.6) dst=(1298.9,634.9)
2026-04-28 12:44:50.716 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121040 bytes (attempt 1)
2026-04-28 12:44:52.560 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122232 bytes (attempt 1)
2026-04-28 12:44:52.749 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5944
2026-04-28 12:44:52.758 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'Y' verified at (13,16)
2026-04-28 12:44:53.967 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122572 bytes (attempt 1)
2026-04-28 12:44:53.974 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt2_RUGGY.png
2026-04-28 12:44:55.632 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 12:44:55.632 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1147.8, 751.3)
2026-04-28 12:44:56.812 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121943 bytes (attempt 1)
2026-04-28 12:44:56.855 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 12:44:56.856 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 12:44:56.856 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1147.5, 753.7)
2026-04-28 12:44:58.102 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122017 bytes (attempt 1)
2026-04-28 12:44:58.150 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 12:44:59.349 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 122374 bytes (attempt 1)
2026-04-28 12:44:59.393 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 12:44:59.394 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'RUGGY' rejected (attempt 2/5) — recalling tiles
2026-04-28 12:44:59.395 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'ruggy' (total: 149)
2026-04-28 12:44:59.981 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 121537 bytes (attempt 1)
2026-04-28 12:44:59.981 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.5, 751.3) (pass 1/10)
2026-04-28 12:45:01.697 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 119760 bytes (attempt 1)
2026-04-28 12:45:01.759 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.6, 750.1) (pass 2/10)
2026-04-28 12:45:03.806 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 119708 bytes (attempt 1)
2026-04-28 12:45:03.941 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.0, 751.9) (pass 3/10)
2026-04-28 13:00:09.068 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:38 | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 3 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank', 'https://879863686565621790.discordsays.com/?instance_id=i-1498736237178257519-gc-1486201751353819208-1486201752477761590&location_id=gc-1486201751353819208-1486201752477761590&launch_id=1498736237178257519&referrer_id=undefined&custom_id=undefined&discord_proxy_ticket=faux-proxy-ticket&guild_id=1486201751353819208&channel_id=1486201752477761590&frame_id=571842dc-d48a-44fd-885c-7165a2b25452&platform=desktop']
2026-04-28 13:00:09.574 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:46 | Viewport screenshot saved -> debug\iframe_missing.png
2026-04-28 13:00:09.574 | WARNING | __main__:_run:222 | place_move raised: Locator.screenshot: Timeout -873596ms exceeded.
Call log:
  - taking element screenshot

2026-04-28 13:00:09.575 | ERROR   | __main__:_run:224 | place_move hit iframe-dead error — re-navigating: Locator.screenshot: Timeout -873596ms exceeded.
Call log:
  - taking element screenshot

2026-04-28 13:00:09.576 | WARNING | __main__:_recover_iframe:140 | Iframe dead (1/2) — re-navigating: Locator.screenshot: Timeout -873596ms exceeded.
Call log:
  - taking element screenshot

2026-04-28 13:00:09.893 | INFO    | src.browser.navigator:_run_navigation:71 | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
2026-04-28 13:30:35.997 | INFO    | src.browser.navigator:_run_navigation:114 | No Join Voice button found — assuming already in voice channel
2026-04-28 13:30:52.334 | WARNING | src.browser.navigator:navigate_to_activity:42 | Navigation attempt 1/3 failed: Locator.wait_for: Timeout 15000ms exceeded.
Call log:
  - waiting for locator("button[aria-label=\"Start An Activity\"]") to be visible
  - waiting for locator("button[aria-label=\"Start An Activity\"]")
. Retrying in 3 seconds...
2026-04-28 13:30:56.839 | INFO    | src.browser.navigator:_run_navigation:71 | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
2026-04-28 13:31:11.287 | INFO    | src.browser.navigator:_run_navigation:110 | Join Voice button found — clicking to join voice channel
2026-04-28 13:31:23.353 | INFO    | src.browser.navigator:_run_navigation:126 | Opened Activity shelf
2026-04-28 13:31:26.246 | INFO    | src.browser.navigator:_run_navigation:147 | Selected Letter League from shelf
2026-04-28 13:31:26.793 | INFO    | src.browser.navigator:_run_navigation:154 | Clicked Play — launching activity
```

## Subprocess stderr (tail)
```
[32m12:44:00[0m | [33m[1mWARNING[0m | Word validity check failed (1 word(s)) after retry — proceeding with best-effort extraction: ["Invalid word(s) on board: 'WX' at col 14 rows 9-10, 'PIXX' at row 10 cols 11-14 — tile positions are likely off by 1. Re-count carefully from center star at (9,13)."]
[32m12:44:00[0m | [33m[1mWARNING[0m | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 10/11 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m12:44:00[0m | [1mINFO   [0m | Vision pipeline complete — 12.39s  tiles=11  rack_size=7
[32m12:44:00[0m | [1mINFO   [0m | Word attempt 1/5: 'GRUNGY' (score=22)
[32m12:44:00[0m | [1mINFO   [0m | Placing tile 'G' (slot 1) -> board (8,16) | src=(1034.9,828.3) dst=(1295.0,460.2)
[32m12:44:03[0m | [1mINFO   [0m | Tile 'G' verified at (8,16)
[32m12:44:04[0m | [1mINFO   [0m | Placing tile 'U' (slot 5) -> board (10,16) | src=(1259.3,827.4) dst=(1298.4,529.5)
[32m12:44:07[0m | [1mINFO   [0m | Tile 'U' verified at (10,16)
[32m12:44:07[0m | [1mINFO   [0m | Placing tile 'N' (slot 6) -> board (11,16) | src=(1309.4,829.1) dst=(1299.1,561.5)
[32m12:44:11[0m | [1mINFO   [0m | Tile 'N' verified at (11,16)
[32m12:44:12[0m | [1mINFO   [0m | Placing tile 'G' (slot 3) -> board (12,16) | src=(1148.0,830.8) dst=(1300.2,596.5)
[32m12:44:14[0m | [1mINFO   [0m | Tile 'G' verified at (12,16)
[32m12:44:15[0m | [1mINFO   [0m | Placing tile 'Y' (slot 0) -> board (13,16) | src=(980.2,828.8) dst=(1296.5,635.9)
[32m12:44:19[0m | [1mINFO   [0m | Tile 'Y' verified at (13,16)
[32m12:44:21[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1148.4, 753.9)
[32m12:44:22[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1144.7, 750.0)
[32m12:44:27[0m | [1mINFO   [0m | Word 'GRUNGY' rejected (attempt 1/5) — recalling tiles
[32m12:44:27[0m | [1mINFO   [0m | Blacklisted rejected word 'grungy' (total: 148)
[32m12:44:27[0m | [1mINFO   [0m | Clicking recall button at (1286.9, 753.7) (pass 1/10)
[32m12:44:30[0m | [1mINFO   [0m | Clicking recall button at (1283.6, 749.4) (pass 2/10)
[32m12:44:32[0m | [1mINFO   [0m | Clicking recall button at (1282.7, 749.4) (pass 3/10)
[32m12:44:34[0m | [1mINFO   [0m | Clicking recall button at (1282.7, 750.6) (pass 4/10)
[32m12:44:36[0m | [1mINFO   [0m | Clicking recall button at (1285.6, 752.4) (pass 5/10)
[32m12:44:38[0m | [1mINFO   [0m | Recall complete after 5 click(s) — canvas stable
[32m12:44:39[0m | [1mINFO   [0m | Word attempt 2/5: 'RUGGY' (score=20)
[32m12:44:39[0m | [1mINFO   [0m | Placing tile 'U' (slot 5) -> board (10,16) | src=(1258.6,825.5) dst=(1295.5,527.6)
[32m12:44:42[0m | [1mINFO   [0m | Tile 'U' verified at (10,16)
[32m12:44:42[0m | [1mINFO   [0m | Placing tile 'G' (slot 1) -> board (11,16) | src=(1037.9,827.8) dst=(1295.1,563.4)
[32m12:44:45[0m | [1mINFO   [0m | Tile 'G' verified at (11,16)
[32m12:44:46[0m | [1mINFO   [0m | Placing tile 'G' (slot 3) -> board (12,16) | src=(1147.1,831.1) dst=(1298.3,598.0)
[32m12:44:49[0m | [1mINFO   [0m | Tile 'G' verified at (12,16)
[32m12:44:49[0m | [1mINFO   [0m | Placing tile 'Y' (slot 0) -> board (13,16) | src=(981.4,830.6) dst=(1298.9,634.9)
[32m12:44:52[0m | [1mINFO   [0m | Tile 'Y' verified at (13,16)
[32m12:44:55[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.8, 751.3)
[32m12:44:56[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.5, 753.7)
[32m12:44:59[0m | [1mINFO   [0m | Word 'RUGGY' rejected (attempt 2/5) — recalling tiles
[32m12:44:59[0m | [1mINFO   [0m | Blacklisted rejected word 'ruggy' (total: 149)
[32m12:44:59[0m | [1mINFO   [0m | Clicking recall button at (1285.5, 751.3) (pass 1/10)
[32m12:45:01[0m | [1mINFO   [0m | Clicking recall button at (1287.6, 750.1) (pass 2/10)
[32m12:45:03[0m | [1mINFO   [0m | Clicking recall button at (1287.0, 751.9) (pass 3/10)
(node:38116) TimeoutNegativeWarning: -873596.0860000001 is a negative number.
Timeout duration was set to 1.
(Use `node --trace-warnings ...` to show where the warning was created)
[32m13:00:09[0m | [33m[1mWARNING[0m | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 3 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank', 'https://879863686565621790.discordsays.com/?instance_id=i-1498736237178257519-gc-1486201751353819208-1486201752477761590&location_id=gc-1486201751353819208-1486201752477761590&launch_id=1498736237178257519&referrer_id=undefined&custom_id=undefined&discord_proxy_ticket=faux-proxy-ticket&guild_id=1486201751353819208&channel_id=1486201752477761590&frame_id=571842dc-d48a-44fd-885c-7165a2b25452&platform=desktop']
[32m13:00:09[0m | [33m[1mWARNING[0m | Viewport screenshot saved -> debug\iframe_missing.png
[32m13:00:09[0m | [33m[1mWARNING[0m | place_move raised: Locator.screenshot: Timeout -873596ms exceeded.
Call log:
  - taking element screenshot

[32m13:00:09[0m | [31m[1mERROR  [0m | place_move hit iframe-dead error — re-navigating: Locator.screenshot: Timeout -873596ms exceeded.
Call log:
  - taking element screenshot

[32m13:00:09[0m | [33m[1mWARNING[0m | Iframe dead (1/2) — re-navigating: Locator.screenshot: Timeout -873596ms exceeded.
Call log:
  - taking element screenshot

[32m13:00:09[0m | [1mINFO   [0m | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
[32m13:30:35[0m | [1mINFO   [0m | No Join Voice button found — assuming already in voice channel
[32m13:30:52[0m | [33m[1mWARNING[0m | Navigation attempt 1/3 failed: Locator.wait_for: Timeout 15000ms exceeded.
Call log:
  - waiting for locator("button[aria-label=\"Start An Activity\"]") to be visible
  - waiting for locator("button[aria-label=\"Start An Activity\"]")
. Retrying in 3 seconds...
[32m13:30:56[0m | [1mINFO   [0m | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
[32m13:31:11[0m | [1mINFO   [0m | Join Voice button found — clicking to join voice channel
[32m13:31:23[0m | [1mINFO   [0m | Opened Activity shelf
[32m13:31:26[0m | [1mINFO   [0m | Selected Letter League from shelf
[32m13:31:26[0m | [1mINFO   [0m | Clicked Play — launching activity
[32m13:31:28[0m | [1mINFO   [0m | Activity iframe found: https://879863686565621790.discordsays.com/?instance_id=i-1498753513843593266-gc-1486201751353819208-1486201752477761590&location_id=gc-1486201751353819208-1486201752477761590&launch_id=1498753513843593266&referrer_id=undefined&custom_id=undefined&discord_proxy_ticket=faux-proxy-ticket&guild_id=1486201751353819208&channel_id=1486201752477761590&frame_id=cf000de2-96f0-4604-8eca-82d340aa335a&platform=desktop
[32m13:31:29[0m | [1mINFO   [0m | Chat panel already hidden
[32m13:31:29[0m | [1mINFO   [0m | Activity iframe verified visible
[32m13:31:41[0m | [1mINFO   [0m | ensure_game_started: lobby detected — clicking START GAME (attempt 1/4)
[32m13:31:42[0m | [1mINFO   [0m | Clicking START GAME button at iframe-relative (1347.2, 721.9) / page (1722.2, 833.9)
[32m13:31:48[0m | [1mINFO   [0m | Game started — initial state: my_turn
[32m13:31:53[0m | [1mINFO   [0m | ensure_game_started: game started — initial state: my_turn
[32m13:31:53[0m | [1mINFO   [0m | Reached max_turns=5 — exiting cleanly
[32m13:31:53[0m | [1mINFO   [0m | Headless autoplay finished in 4185.7s

[auto_debug] subprocess timeout — killed
```

## git status --short
```
M debug/preprocessed_debug.png
 M debug/tile_placer/post_recall_attempt1.png
 M debug/tile_placer/post_recall_attempt2.png
 M debug/tile_placer/post_recall_attempt3.png
 M debug/tile_placer/post_recall_attempt4.png
 M debug/tile_placer/post_recall_attempt5.png
 M src/bot/autoplay_cog.py
 M src/browser/capture.py
 M src/browser/tile_placer.py
 M src/browser/turn_detector.py
 M src/vision/__init__.py
 M tests/test_tile_placer.py
?? .claude/
?? data/rejected_words.txt
?? debug/iframe_missing.png
?? debug/menu_screen.png
?? debug/start_btn_probe_estimated.png
?? debug/start_btn_probe_existing.png
?? debug/start_btn_probe_rounded.png
?? debug/tile_placer/pre_play_attempt1_ACARI.png
?? debug/tile_placer/pre_play_attempt1_AFLOAT.png
?? debug/tile_placer/pre_play_attempt1_ALUMNAE.png
?? debug/tile_placer/pre_play_attempt1_ANNUAL.png
?? debug/tile_placer/pre_play_attempt1_ANORAK.png
?? debug/tile_placer/pre_play_attempt1_ARABIC.png
?? debug/tile_placer/pre_play_attempt1_BEANY.png
?? debug/tile_placer/pre_play_attempt1_BIN.png
?? debug/tile_placer/pre_play_attempt1_BITTY.png
?? debug/tile_placer/pre_play_attempt1_CAULKER.png
?? debug/tile_placer/pre_play_attempt1_DAMNS.png
?? debug/tile_placer/pre_play_attempt1_DOG.png
?? debug/tile_placer/pre_play_attempt1_EL.png
?? debug/tile_placer/pre_play_attempt1_FAKE.png
?? debug/tile_placer/pre_play_attempt1_FIBERS.png
?? debug/tile_placer/pre_play_attempt1_FIZ.png
?? debug/tile_placer/pre_play_attempt1_FORKY.png
?? debug/tile_placer/pre_play_attempt1_FOUR.png
?? debug/tile_placer/pre_play_attempt1_FROG.png
?? debug/tile_placer/pre_play_attempt1_FUTURE.png
?? debug/tile_placer/pre_play_attempt1_FYCE.png
?? debug/tile_placer/pre_play_attempt1_GINZO.png
?? debug/tile_placer/pre_play_attempt1_GOOD.png
?? debug/tile_placer/pre_play_attempt1_GOOGOL.png
?? debug/tile_placer/pre_play_attempt1_GOOLD.png
?? debug/tile_placer/pre_play_attempt1_GOWF.png
?? debug/tile_placer/pre_play_attempt1_GROW.png
?? debug/tile_placer/pre_play_attempt1_GRUNGY.png
?? debug/tile_placer/pre_play_attempt1_HINGED.png
?? debug/tile_placer/pre_play_attempt1_ID.png
?? debug/tile_placer/pre_play_attempt1_JIAO.png
?? debug/tile_placer/pre_play_attempt1_JOEY.png
?? debug/tile_placer/pre_play_attempt1_JOINT.png
?? debug/tile_placer/pre_play_attempt1_JOINTS.png
?? debug/tile_placer/pre_play_attempt1_KENDO.png
?? debug/tile_placer/pre_play_attempt1_KURU.png
?? debug/tile_placer/pre_play_attempt1_LEAK.png
?? debug/tile_placer/pre_play_attempt1_LEG.png
?? debug/tile_placer/pre_play_attempt1_LOGO.png
?? debug/tile_placer/pre_play_attempt1_MANUAL.png
?? debug/tile_placer/pre_play_attempt1_NEURAL.png
?? debug/tile_placer/pre_play_attempt1_OI.png
?? debug/tile_placer/pre_play_attempt1_OUTVIE.png
?? debug/tile_placer/pre_play_attempt1_PIX.png
?? debug/tile_placer/pre_play_attempt1_PIXEL.png
?? debug/tile_placer/pre_play_attempt1_PODGIEST.png
?? debug/tile_placer/pre_play_attempt1_PORTAGE.png
?? debug/tile_placer/pre_play_attempt1_QUIMS.png
?? debug/tile_placer/pre_play_attempt1_RANULAE.png
?? debug/tile_placer/pre_play_attempt1_ST.png
?? debug/tile_placer/pre_play_attempt1_TIN.png
?? debug/tile_placer/pre_play_attempt1_TOLA.png
?? debug/tile_placer/pre_play_attempt1_TOWELING.png
?? debug/tile_placer/pre_play_attempt1_TOWERED.png
?? debug/tile_placer/pre_play_attempt1_TREW.png
?? debug/tile_placer/pre_play_attempt1_VIAE.png
?? debug/tile_placer/pre_play_attempt1_VICAR.png
?? debug/tile_placer/pre_play_attempt1_VITEX.png
?? debug/tile_placer/pre_play_attempt1_WEFT.png
?? debug/tile_placer/pre_play_attempt1_WOE.png
?? debug/tile_placer/pre_play_attempt1_ZO.png
?? debug/tile_placer/pre_play_attempt1_ZONA.png
?? debug/tile_placer/pre_play_attempt1_ZOOM.png
?? debug/tile_placer/pre_play_attempt2_ACARI.png
?? debug/tile_placer/pre_play_attempt2_AIAIA.png
?? debug/tile_placer/pre_play_attempt2_AVE.png
?? debug/tile_placer/pre_play_attempt2_AXITE.png
?? debug/tile_placer/pre_play_attempt2_BORDEL.png
?? debug/tile_placer/pre_play_attempt2_BRIEFS.png
?? debug/tile_placer/pre_play_attempt2_CANULAE.png
?? debug/tile_placer/pre_play_attempt2_CARIBE.png
?? debug/tile_placer/pre_play_attempt2_CAULKED.png
?? debug/tile_placer/pre_play_attempt2_COZ.png
?? debug/tile_placer/pre_play_attempt2_DI.png
?? debug/tile_placer/pre_play_attempt2_DITTY.png
?? debug/tile_placer/pre_play_attempt2_DOGGO.png
?? debug/tile_placer/pre_play_attempt2_FET.png
?? debug/tile_placer/pre_play_attempt2_FEW.png
?? debug/tile_placer/pre_play_attempt2_FLAUTA.png
?? debug/tile_placer/pre_play_attempt2_FUGU.png
?? debug/tile_placer/pre_play_attempt2_FUGUE.png
?? debug/tile_placer/pre_play_attempt2_GAZON.png
?? debug/tile_placer/pre_play_attempt2_GLOAT.png
?? debug/tile_placer/pre_play_attempt2_GOOLD.png
?? debug/tile_placer/pre_play_attempt2_INBYE.png
?? debug/tile_placer/pre_play_attempt2_IO.png
?? debug/tile_placer/pre_play_attempt2_KEEF.png
?? debug/tile_placer/pre_play_attempt2_KINARA.png
?? debug/tile_placer/pre_play_attempt2_KUGEL.png
?? debug/tile_placer/pre_play_attempt2_KUTU.png
?? debug/tile_placer/pre_play_attempt2_LACKER.png
?? debug/tile_placer/pre_play_attempt2_LACUNE.png
?? debug/tile_placer/pre_play_attempt2_LAGENA.png
?? debug/tile_placer/pre_play_attempt2_LAUAN.png
?? debug/tile_placer/pre_play_attempt2_LI.png
?? debug/tile_placer/pre_play_attempt2_LIG.png
?? debug/tile_placer/pre_play_attempt2_LOG.png
?? debug/tile_placer/pre_play_attempt2_LOTA.png
?? debug/tile_placer/pre_play_attempt2_MOZO.png
?? debug/tile_placer/pre_play_attempt2_NABI.png
?? debug/tile_placer/pre_play_attempt2_NIB.png
?? debug/tile_placer/pre_play_attempt2_NIGHED.png
?? debug/tile_placer/pre_play_attempt2_NOGG.png
?? debug/tile_placer/pre_play_attempt2_NY.png
?? debug/tile_placer/pre_play_attempt2_ORAD.png
?? debug/tile_placer/pre_play_attempt2_OUTVIE.png
?? debug/tile_placer/pre_play_attempt2_POZ.png
?? debug/tile_placer/pre_play_attempt2_RUGGY.png
?? debug/tile_placer/pre_play_attempt2_TAJINE.png
?? debug/tile_placer/pre_play_attempt2_TEF.png
?? debug/tile_placer/pre_play_attempt2_TO.png
?? debug/tile_placer/pre_play_attempt2_TOFU.png
?? debug/tile_placer/pre_play_attempt2_TOWNLET.png
?? debug/tile_placer/pre_play_attempt2_TOXINS.png
?? debug/tile_placer/pre_play_attempt2_TREF.png
?? debug/tile_placer/pre_play_attempt2_UNABLE.png
?? debug/tile_placer/pre_play_attempt2_WINGLET.png
?? debug/tile_placer/pre_play_attempt2_ZONING.png
?? debug/tile_placer/pre_play_attempt2_ZOOT.png
?? debug/tile_placer/pre_play_attempt3_ACARI.png
?? debug/tile_placer/pre_play_attempt3_AGLOO.png
?? debug/tile_placer/pre_play_attempt3_ARABIC.png
?? debug/tile_placer/pre_play_attempt3_BEAN.png
?? debug/tile_placer/pre_play_attempt3_BI.png
?? debug/tile_placer/pre_play_attempt3_BIN.png
?? debug/tile_placer/pre_play_attempt3_BITTY.png
?? debug/tile_placer/pre_play_attempt3_BUNYA.png
?? debug/tile_placer/pre_play_attempt3_CALKED.png
?? debug/tile_placer/pre_play_attempt3_EXEAT.png
?? debug/tile_placer/pre_play_attempt3_FAKE.png
?? debug/tile_placer/pre_play_attempt3_FAUCAL.png
?? debug/tile_placer/pre_play_attempt3_FER.png
?? debug/tile_placer/pre_play_attempt3_FRUG.png
?? debug/tile_placer/pre_play_attempt3_FUG.png
?? debug/tile_placer/pre_play_attempt3_FUN.png
?? debug/tile_placer/pre_play_attempt3_FUR.png
?? debug/tile_placer/pre_play_attempt3_GEL.png
?? debug/tile_placer/pre_play_attempt3_GI.png
?? debug/tile_placer/pre_play_attempt3_GOOGOL.png
?? debug/tile_placer/pre_play_attempt3_GOOLD.png
?? debug/tile_placer/pre_play_attempt3_GRACKLE.png
?? debug/tile_placer/pre_play_attempt3_HIELD.png
?? debug/tile_placer/pre_play_attempt3_JOEY.png
?? debug/tile_placer/pre_play_attempt3_KRONA.png
?? debug/tile_placer/pre_play_attempt3_LACUNA.png
?? debug/tile_placer/pre_play_attempt3_LANDAU.png
?? debug/tile_placer/pre_play_attempt3_LEK.png
?? debug/tile_placer/pre_play_attempt3_LOD.png
?? debug/tile_placer/pre_play_attempt3_LOTO.png
?? debug/tile_placer/pre_play_attempt3_NABI.png
?? debug/tile_placer/pre_play_attempt3_NOT.png
?? debug/tile_placer/pre_play_attempt3_OF.png
?? debug/tile_placer/pre_play_attempt3_OUTVIE.png
?? debug/tile_placer/pre_play_attempt3_PORTAGE.png
?? debug/tile_placer/pre_play_attempt3_POZ.png
?? debug/tile_placer/pre_play_attempt3_QI.png
?? debug/tile_placer/pre_play_attempt3_REW.png
?? debug/tile_placer/pre_play_attempt3_ROAD.png
?? debug/tile_placer/pre_play_attempt3_SOZ.png
?? debug/tile_placer/pre_play_attempt3_TAJ.png
?? debug/tile_placer/pre_play_attempt3_TOWNLET.png
?? debug/tile_placer/pre_play_attempt3_TOXIN.png
?? debug/tile_placer/pre_play_attempt3_ULNAE.png
?? debug/tile_placer/pre_play_attempt3_VIE.png
?? debug/tile_placer/pre_play_attempt3_WELTING.png
?? debug/tile_placer/pre_play_attempt3_WOF.png
?? debug/tile_placer/pre_play_attempt3_ZAG.png
?? debug/tile_placer/pre_play_attempt3_ZIG.png
?? debug/tile_placer/pre_play_attempt3_ZO.png
?? debug/tile_placer/pre_play_attempt3_ZOOM.png
?? debug/tile_placer/pre_play_attempt4_ALOD.png
?? debug/tile_placer/pre_play_attempt4_AZON.png
?? debug/tile_placer/pre_play_attempt4_BANI.png
?? debug/tile_placer/pre_play_attempt4_BE.png
?? debug/tile_placer/pre_play_attempt4_BITTY.png
?? debug/tile_placer/pre_play_attempt4_BY.png
?? debug/tile_placer/pre_play_attempt4_CALKER.png
?? debug/tile_placer/pre_play_attempt4_CARIBE.png
?? debug/tile_placer/pre_play_attempt4_CERIA.png
?? debug/tile_placer/pre_play_attempt4_DOL.png
?? debug/tile_placer/pre_play_attempt4_DOR.png
?? debug/tile_placer/pre_play_attempt4_DOTAL.png
?? debug/tile_placer/pre_play_attempt4_FAUNAL.png
?? debug/tile_placer/pre_play_attempt4_FROW.png
?? debug/tile_placer/pre_play_attempt4_FURY.png
?? debug/tile_placer/pre_play_attempt4_GAK.png
?? debug/tile_placer/pre_play_attempt4_GLOWER.png
?? debug/tile_placer/pre_play_attempt4_GOLD.png
?? debug/tile_placer/pre_play_attempt4_GONG.png
?? debug/tile_placer/pre_play_attempt4_GOOLD.png
?? debug/tile_placer/pre_play_attempt4_JAILED.png
?? debug/tile_placer/pre_play_attempt4_KEEF.png
?? debug/tile_placer/pre_play_attempt4_LACUNAE.png
?? debug/tile_placer/pre_play_attempt4_LAGUNE.png
?? debug/tile_placer/pre_play_attempt4_LANGUE.png
?? debug/tile_placer/pre_play_attempt4_LUCKED.png
?? debug/tile_placer/pre_play_attempt4_MOZO.png
?? debug/tile_placer/pre_play_attempt4_NUBIA.png
?? debug/tile_placer/pre_play_attempt4_OUTVIE.png
?? debug/tile_placer/pre_play_attempt4_PORTAGE.png
?? debug/tile_placer/pre_play_attempt4_RACIER.png
?? debug/tile_placer/pre_play_attempt4_REF.png
?? debug/tile_placer/pre_play_attempt4_TON.png
?? debug/tile_placer/pre_play_attempt4_TURF.png
?? debug/tile_placer/pre_play_attempt4_TURK.png
?? debug/tile_placer/pre_play_attempt4_VIA.png
?? debug/tile_placer/pre_play_attempt4_VITAE.png
?? debug/tile_placer/pre_play_attempt4_WERT.png
?? debug/tile_placer/pre_play_attempt4_WET.png
?? debug/tile_placer/pre_play_attempt4_WIGLET.png
?? debug/tile_placer/pre_play_attempt4_WORT.png
?? debug/tile_placer/pre_play_attempt4_ZIN.png
?? debug/tile_placer/pre_play_attempt4_ZO.png
?? debug/tile_placer/pre_play_attempt4_ZOO.png
?? debug/tile_placer/pre_play_attempt4_ZOS.png
?? debug/tile_placer/pre_play_attempt5_ACKEE.png
?? debug/tile_placer/pre_play_attempt5_AREIC.png
?? debug/tile_placer/pre_play_attempt5_AZO.png
?? debug/tile_placer/pre_play_attempt5_BARIC.png
?? debug/tile_placer/pre_play_attempt5_BI.png
?? debug/tile_placer/pre_play_attempt5_BITTY.png
?? debug/tile_placer/pre_play_attempt5_CARLE.png
?? debug/tile_placer/pre_play_attempt5_EA.png
?? debug/tile_placer/pre_play_attempt5_EVITE.png
?? debug/tile_placer/pre_play_attempt5_FACULA.png
?? debug/tile_placer/pre_play_attempt5_FANGO.png
?? debug/tile_placer/pre_play_attempt5_FEG.png
?? debug/tile_placer/pre_play_attempt5_FEU.png
?? debug/tile_placer/pre_play_attempt5_FON.png
?? debug/tile_placer/pre_play_attempt5_GALOOT.png
?? debug/tile_placer/pre_play_attempt5_GOD.png
?? debug/tile_placer/pre_play_attempt5_GOLD.png
?? debug/tile_placer/pre_play_attempt5_GREW.png
?? debug/tile_placer/pre_play_attempt5_JOINED.png
?? debug/tile_placer/pre_play_attempt5_KEEF.png
?? debug/tile_placer/pre_play_attempt5_LACKED.png
?? debug/tile_placer/pre_play_attempt5_LAGUNA.png
?? debug/tile_placer/pre_play_attempt5_LANATE.png
?? debug/tile_placer/pre_play_attempt5_NAB.png
?? debug/tile_placer/pre_play_attempt5_NABI.png
?? debug/tile_placer/pre_play_attempt5_NIB.png
?? debug/tile_placer/pre_play_attempt5_NOWL.png
?? debug/tile_placer/pre_play_attempt5_NY.png
?? debug/tile_placer/pre_play_attempt5_OUTVIE.png
?? debug/tile_placer/pre_play_attempt5_REFT.png
?? debug/tile_placer/pre_play_attempt5_TEW.png
?? debug/tile_placer/pre_play_attempt5_TOGA.png
?? debug/tile_placer/pre_play_attempt5_WOG.png
?? debug/tile_placer/pre_play_attempt5_ZING.png
?? debug/tile_placer/pre_play_attempt5_ZO.png
?? debug/tile_placer/pre_play_attempt5_ZOOM.png
?? debug/tile_placer/pre_play_attempt5_ZOOT.png
?? debug/turn_detection/frame_20260421_150958_649938_preflight.png
?? debug/turn_detection/frame_20260421_162703_689039_pre_start_attempt1.png
?? debug/turn_detection/frame_20260421_163307_323588_pre_start_attempt1.png
?? debug/turn_detection/frame_20260421_164425_523549_pre_start_attempt1.png
?? debug/turn_detection/frame_20260421_165428_726286_pre_start_attempt1.png
?? debug/turn_detection/frame_20260421_174433_849089_pre_start_attempt1.png
?? debug/turn_detection/frame_20260421_180028_532026_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_101610_397574_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_104718_015726_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_114521_760256_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_135931_873495_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_141956_093101_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_154012_580127_preflight.png
?? debug/turn_detection/frame_20260423_154849_895818_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_161723_820145_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_170818_278622_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_171501_568210_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_174032_864806_pre_start_attempt1.png
?? debug/turn_detection/frame_20260423_174748_088829_pre_start_attempt1.png
?? debug/turn_detection/frame_20260428_105220_621800_pre_start_attempt1.png
?? debug/turn_detection/frame_20260428_113635_825402_preflight.png
?? debug/turn_detection/frame_20260428_113826_776417_pre_start_attempt1.png
?? debug/turn_detection/frame_20260428_122307_048398_pre_start_attempt1.png
?? debug/turn_detection/frame_20260428_133141_949567_pre_start_attempt1.png
?? logs/
?? scripts/auto_debug.py
?? scripts/autoplay_headless.py
?? src/engine/rejected_words.py
```

## git diff --stat
```
debug/preprocessed_debug.png               | Bin 371628 -> 384264 bytes
 debug/tile_placer/post_recall_attempt1.png | Bin 117178 -> 119940 bytes
 debug/tile_placer/post_recall_attempt2.png | Bin 120237 -> 122966 bytes
 debug/tile_placer/post_recall_attempt3.png | Bin 119929 -> 122491 bytes
 debug/tile_placer/post_recall_attempt4.png | Bin 119657 -> 122774 bytes
 debug/tile_placer/post_recall_attempt5.png | Bin 120024 -> 122533 bytes
 src/bot/autoplay_cog.py                    |  39 +++-
 src/browser/capture.py                     |  71 +++++-
 src/browser/tile_placer.py                 | 340 +++++++++++++++++++++++++----
 src/browser/turn_detector.py               | 192 +++++++++++++++-
 src/vision/__init__.py                     | 127 ++++++++---
 tests/test_tile_placer.py                  |  79 ++++++-
 12 files changed, 740 insertions(+), 108 deletions(-)
```