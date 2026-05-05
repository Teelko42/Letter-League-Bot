# Auto-debug iteration 2

- exit_code: `1`
- duration: 580.1s
- error_signature: `aa1407fbfcfb`

## Recent debug artifacts
- `debug/tile_placer/post_recall_attempt1.png`
- `debug/tile_placer/pre_play_attempt1_TAWIE.png`
- `debug/tile_placer/pre_play_attempt5_YEAN.png`
- `debug/iframe_missing.png`
- `debug/preprocessed_debug.png`

## Autoplay log — error region
```
2026-05-03 23:21:18.043 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.0609
2026-05-03 23:21:18.044 | WARNING | src.browser.tile_placer:place_tiles:703 | Tile 'U' placement not verified — retrying with fresh jitter
2026-05-03 23:21:18.953 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119820 bytes (attempt 1)
2026-05-03 23:21:20.950 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119800 bytes (attempt 1)
2026-05-03 23:21:21.062 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.0458
2026-05-03 23:21:21.063 | ERROR   | src.browser.tile_placer:place_move:1061 | Tile placement failed for 'OUTATE' (attempt 2): Tile 'U' at (8,16) failed to place after retry
2026-05-03 23:21:21.189 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:21:21.190 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1287.7, 750.5) (pass 1/9)
2026-05-03 23:21:21.990 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1287.0, 749.0) (pass 2/9)
2026-05-03 23:21:23.031 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1284.1, 751.8) (pass 3/9)
2026-05-03 23:21:23.809 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1284.2, 753.4) (pass 4/9)
2026-05-03 23:21:24.700 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1283.5, 750.7) (pass 5/9)
2026-05-03 23:21:25.558 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1286.5, 750.0) (pass 6/9)
2026-05-03 23:21:26.491 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1283.5, 749.1) (pass 7/9)
2026-05-03 23:21:27.258 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1287.3, 752.3) (pass 8/9)
2026-05-03 23:21:28.346 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1284.4, 748.0) (pass 9/9)
2026-05-03 23:21:30.025 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118591 bytes (attempt 1)
2026-05-03 23:21:30.029 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:849 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt2.png
2026-05-03 23:21:30.030 | INFO    | src.browser.tile_placer:place_move:1050 | Word attempt 3/5: 'YOUR' (score=22)
2026-05-03 23:21:30.206 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:21:30.207 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'Y' (slot 0) -> board (6,11) | src=(982.8,830.9) dst=(1043.9,391.3)
2026-05-03 23:21:31.251 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118586 bytes (attempt 1)
2026-05-03 23:21:33.500 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119873 bytes (attempt 1)
2026-05-03 23:21:33.628 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.6970
2026-05-03 23:21:33.629 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'Y' verified at (6,11)
2026-05-03 23:21:34.277 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'O' (slot 4) -> board (7,11) | src=(1202.7,830.1) dst=(1042.8,427.5)
2026-05-03 23:21:35.476 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119748 bytes (attempt 1)
2026-05-03 23:21:37.690 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119983 bytes (attempt 1)
2026-05-03 23:21:37.825 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.5605
2026-05-03 23:21:37.828 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'O' verified at (7,11)
2026-05-03 23:21:38.528 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'U' (slot 6) -> board (8,11) | src=(1314.1,827.2) dst=(1046.1,459.1)
2026-05-03 23:21:39.947 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119973 bytes (attempt 1)
2026-05-03 23:21:42.304 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120409 bytes (attempt 1)
2026-05-03 23:21:42.395 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.2767
2026-05-03 23:21:42.396 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'U' verified at (8,11)
2026-05-03 23:21:43.249 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120254 bytes (attempt 1)
2026-05-03 23:21:43.259 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:849 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt3_YOUR.png
2026-05-03 23:21:43.880 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:21:43.881 | INFO    | src.browser.tile_placer:_click_confirm:799 | Clicking confirm/PLAY button at (1145.2, 751.7)
2026-05-03 23:21:46.384 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120230 bytes (attempt 1)
2026-05-03 23:21:47.068 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:824 | Post-confirm poll 1/3: my_turn
2026-05-03 23:21:47.092 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:830 | Re-clicking PLAY (retry after 1 polls)
2026-05-03 23:21:47.098 | INFO    | src.browser.tile_placer:_click_confirm:799 | Clicking confirm/PLAY button at (1147.8, 748.8)
2026-05-03 23:21:48.961 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120195 bytes (attempt 1)
2026-05-03 23:21:49.055 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:824 | Post-confirm poll 2/3: my_turn
2026-05-03 23:21:51.273 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119904 bytes (attempt 1)
2026-05-03 23:21:51.332 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:824 | Post-confirm poll 3/3: my_turn
2026-05-03 23:21:51.333 | INFO    | src.browser.tile_placer:place_move:1101 | Word 'YOUR' rejected (attempt 3/5) — recalling tiles
2026-05-03 23:21:51.334 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'your' (total: 28)
2026-05-03 23:21:51.335 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1287.7, 752.2) (pass 1/5)
2026-05-03 23:21:52.116 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1285.8, 752.1) (pass 2/5)
2026-05-03 23:21:53.008 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1284.8, 751.1) (pass 3/5)
2026-05-03 23:21:53.818 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1283.8, 753.1) (pass 4/5)
2026-05-03 23:21:54.717 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1286.8, 750.3) (pass 5/5)
2026-05-03 23:21:56.211 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118719 bytes (attempt 1)
2026-05-03 23:21:56.212 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:849 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt3.png
2026-05-03 23:21:56.213 | INFO    | src.browser.tile_placer:place_move:1050 | Word attempt 4/5: 'YEAR' (score=22)
2026-05-03 23:21:56.270 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:21:56.270 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'Y' (slot 0) -> board (6,11) | src=(977.7,828.0) dst=(1042.4,388.2)
2026-05-03 23:21:56.834 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118341 bytes (attempt 1)
2026-05-03 23:21:59.105 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119573 bytes (attempt 1)
2026-05-03 23:21:59.275 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.7143
2026-05-03 23:21:59.276 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'Y' verified at (6,11)
2026-05-03 23:21:59.891 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'E' (slot 5) -> board (7,11) | src=(1253.8,826.7) dst=(1043.9,424.2)
2026-05-03 23:22:00.903 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119834 bytes (attempt 1)
2026-05-03 23:22:02.846 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119808 bytes (attempt 1)
2026-05-03 23:22:03.004 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.5485
2026-05-03 23:22:03.005 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'E' verified at (7,11)
2026-05-03 23:22:03.558 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'A' (slot 1) -> board (8,11) | src=(1037.4,830.1) dst=(1044.2,459.5)
2026-05-03 23:22:04.465 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119870 bytes (attempt 1)
2026-05-03 23:22:07.849 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119953 bytes (attempt 1)
2026-05-03 23:22:08.044 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.3131
2026-05-03 23:22:08.044 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'A' verified at (8,11)
2026-05-03 23:22:09.292 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120018 bytes (attempt 1)
2026-05-03 23:22:09.294 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:849 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt4_YEAR.png
2026-05-03 23:22:09.822 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:22:09.822 | INFO    | src.browser.tile_placer:_click_confirm:799 | Clicking confirm/PLAY button at (1148.4, 753.9)
2026-05-03 23:22:11.014 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119796 bytes (attempt 1)
2026-05-03 23:22:11.071 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:824 | Post-confirm poll 1/3: my_turn
2026-05-03 23:22:11.071 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:830 | Re-clicking PLAY (retry after 1 polls)
2026-05-03 23:22:11.071 | INFO    | src.browser.tile_placer:_click_confirm:799 | Clicking confirm/PLAY button at (1146.7, 749.3)
2026-05-03 23:22:12.279 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120120 bytes (attempt 1)
2026-05-03 23:22:12.331 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:824 | Post-confirm poll 2/3: my_turn
2026-05-03 23:22:13.499 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119896 bytes (attempt 1)
2026-05-03 23:22:13.548 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:824 | Post-confirm poll 3/3: my_turn
2026-05-03 23:22:13.549 | INFO    | src.browser.tile_placer:place_move:1101 | Word 'YEAR' rejected (attempt 4/5) — recalling tiles
2026-05-03 23:22:13.550 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'year' (total: 29)
2026-05-03 23:22:13.551 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1283.8, 752.2) (pass 1/5)
2026-05-03 23:22:14.319 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1285.0, 753.0) (pass 2/5)
2026-05-03 23:22:15.070 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1286.7, 749.0) (pass 3/5)
2026-05-03 23:22:15.929 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1285.8, 753.3) (pass 4/5)
2026-05-03 23:22:16.678 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1286.0, 750.3) (pass 5/5)
2026-05-03 23:22:18.197 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118701 bytes (attempt 1)
2026-05-03 23:22:18.198 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:849 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt4.png
2026-05-03 23:22:18.199 | INFO    | src.browser.tile_placer:place_move:1050 | Word attempt 5/5: 'YEAN' (score=22)
2026-05-03 23:22:18.253 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:22:18.253 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'Y' (slot 0) -> board (6,15) | src=(981.7,827.1) dst=(1247.4,388.4)
2026-05-03 23:22:18.830 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118432 bytes (attempt 1)
2026-05-03 23:22:20.516 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120180 bytes (attempt 1)
2026-05-03 23:22:20.658 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.8388
2026-05-03 23:22:20.660 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'Y' verified at (6,15)
2026-05-03 23:22:21.265 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'E' (slot 5) -> board (7,15) | src=(1258.4,826.5) dst=(1247.4,424.7)
2026-05-03 23:22:22.516 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119776 bytes (attempt 1)
2026-05-03 23:22:25.970 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120247 bytes (attempt 1)
2026-05-03 23:22:26.227 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 1.5555
2026-05-03 23:22:26.229 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'E' verified at (7,15)
2026-05-03 23:22:26.672 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'A' (slot 1) -> board (8,15) | src=(1037.6,826.6) dst=(1246.5,461.4)
2026-05-03 23:22:27.631 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120260 bytes (attempt 1)
2026-05-03 23:22:30.050 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120486 bytes (attempt 1)
2026-05-03 23:22:30.210 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.2561
2026-05-03 23:22:30.210 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'A' verified at (8,15)
2026-05-03 23:22:31.134 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120362 bytes (attempt 1)
2026-05-03 23:22:31.142 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:849 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt5_YEAN.png
2026-05-03 23:22:32.235 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:22:32.235 | INFO    | src.browser.tile_placer:_click_confirm:799 | Clicking confirm/PLAY button at (1146.6, 753.2)
2026-05-03 23:22:34.284 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 111290 bytes (attempt 1)
2026-05-03 23:22:34.540 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:824 | Post-confirm poll 1/3: not_my_turn
2026-05-03 23:22:34.541 | INFO    | src.browser.tile_placer:place_move:1092 | Word 'YEAN' accepted! (score=22, attempt 5/5)
2026-05-03 23:22:34.542 | INFO    | __main__:_run:267 | Turn 1: played 'YEAN' (score=22)
2026-05-03 23:22:38.330 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 108725 bytes (attempt 1)
2026-05-03 23:22:38.529 | INFO    | src.browser.turn_detector:poll_turn:648 | Turn state changed: None -> not_my_turn
2026-05-03 23:22:44.824 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119943 bytes (attempt 1)
2026-05-03 23:22:44.933 | INFO    | src.browser.turn_detector:poll_turn:648 | Turn state changed: not_my_turn -> my_turn
2026-05-03 23:22:45.091 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:22:45.970 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120529 bytes (attempt 1)
2026-05-03 23:22:46.009 | INFO    | src.browser.tile_placer:clear_stale_placements:958 | Pre-turn recall click at (1287.9, 751.3) (pass 1/4)
2026-05-03 23:22:47.055 | INFO    | src.browser.tile_placer:clear_stale_placements:958 | Pre-turn recall click at (1283.9, 751.2) (pass 2/4)
2026-05-03 23:22:48.014 | INFO    | src.browser.tile_placer:clear_stale_placements:958 | Pre-turn recall click at (1287.6, 753.9) (pass 3/4)
2026-05-03 23:22:48.948 | INFO    | src.browser.tile_placer:clear_stale_placements:958 | Pre-turn recall click at (1288.3, 748.5) (pass 4/4)
2026-05-03 23:22:54.721 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120686 bytes (attempt 1)
2026-05-03 23:22:54.722 | INFO    | src.vision:extract_board_state:148 | Vision pipeline start — mode=wild
2026-05-03 23:22:54.774 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,54) 1366×657 from 1545×768 canvas
2026-05-03 23:22:55.850 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-05-03 23:22:56.119 | INFO    | src.vision:extract_board_state:154 | Preprocessing complete — 376381 bytes
2026-05-03 23:22:56.120 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=False
2026-05-03 23:23:01.428 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=5.27s  input_tokens=2903  output_tokens=306
2026-05-03 23:23:01.428 | INFO    | src.vision:extract_board_state:160 | Extraction complete (first attempt)
2026-05-03 23:23:01.429 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (6,15)=I[DW] (7,15)=O[DW] (9,8)=R[DW] (9,9)=E[DL] (9,10)=E[DL] (9,11)=N*[TL] (9,12)=E[DL] (9,13)=N[DW] (9,14)=T[DL] (9,15)=T[DL]
2026-05-03 23:23:01.429 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['A', 'E', 'U', 'A', 'Y', 'T', 'W']
2026-05-03 23:23:01.429 | DEBUG   | src.vision.validator:correct_positions:92 | Position auto-correction skipped: insufficient evidence (matches=4, informative=10, threshold=2 or 50%)
2026-05-03 23:23:01.430 | DEBUG   | src.vision.validator:correct_positions_gaddag:317 | GADDAG position correction: no shift improves word validity (current 1/2 valid runs)
2026-05-03 23:23:01.435 | INFO    | src.vision:extract_board_state:179 | Validation result — 4 error(s)
2026-05-03 23:23:01.436 | WARNING | src.vision:extract_board_state:205 | Validation failed (4 errors), retrying: ["Floating tile 'I' at (6, 15) — not connected to other tiles", "Floating tile 'O' at (7, 15) — not connected to other tiles", 'Position accuracy suspect: 10/10 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.', "Invalid word(s) on board: 'REENENTT' at row 9 cols 8-15 — tile positions are likely off by 1. Re-count carefully from center star at (9,13)."]
2026-05-03 23:23:01.439 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=True
2026-05-03 23:23:09.401 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=7.96s  input_tokens=3050  output_tokens=160
2026-05-03 23:23:09.402 | INFO    | src.vision:extract_board_state:211 | Extraction complete (retry)
2026-05-03 23:23:09.403 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (6,15)=I[DW] (7,15)=O[NONE]
2026-05-03 23:23:09.404 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['A', 'E', 'U', 'A', 'Y', 'T', 'W']
2026-05-03 23:23:09.405 | INFO    | src.vision.validator:correct_positions_center_star:193 | Center star correction: shifting tiles by (+2, -2) to place a tile on (9,13) — multiplier score 2
2026-05-03 23:23:09.406 | INFO    | src.vision:extract_board_state:230 | Merged 9 cell(s) from first attempt that retry dropped: [('I', 6, 15), ('O', 7, 15), ('R', 9, 8), ('E', 9, 9), ('E', 9, 10), ('N', 9, 11), ('E', 9, 12), ('T', 9, 14), ('T', 9, 15)]
2026-05-03 23:23:09.407 | INFO    | src.vision:extract_board_state:259 | Validation result after retry — 3 error(s)
2026-05-03 23:23:09.409 | WARNING | src.vision:extract_board_state:289 | Removed 2 floating tile(s) to salvage extraction
2026-05-03 23:23:09.409 | WARNING | src.vision:extract_board_state:308 | Word validity check failed (1 word(s)) after retry — proceeding with best-effort extraction: ["Invalid word(s) on board: 'REENEOTT' at row 9 cols 8-15 — tile positions are likely off by 1. Re-count carefully from center star at (9,13)."]
2026-05-03 23:23:09.413 | INFO    | src.vision:extract_board_state:353 | Vision pipeline complete — 14.69s  tiles=9  rack_size=7
2026-05-03 23:23:09.647 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 75 blacklisted candidate(s)
2026-05-03 23:23:09.663 | INFO    | src.browser.tile_placer:place_move:1050 | Word attempt 1/5: 'TAWIE' (score=39)
2026-05-03 23:23:09.856 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:23:09.856 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'T' (slot 5) -> board (8,10) | src=(1254.5,830.0) dst=(992.2,458.8)
2026-05-03 23:23:11.369 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121424 bytes (attempt 1)
2026-05-03 23:23:13.583 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122198 bytes (attempt 1)
2026-05-03 23:23:13.694 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.9176
2026-05-03 23:23:13.695 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'T' verified at (8,10)
2026-05-03 23:23:14.145 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'A' (slot 0) -> board (8,11) | src=(978.6,830.2) dst=(1046.7,461.5)
2026-05-03 23:23:16.144 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121622 bytes (attempt 1)
2026-05-03 23:23:18.710 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122584 bytes (attempt 1)
2026-05-03 23:23:18.865 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 1.5279
2026-05-03 23:23:18.865 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'A' verified at (8,11)
2026-05-03 23:23:19.519 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'W' (slot 6) -> board (8,12) | src=(1313.3,829.0) dst=(1092.8,460.6)
2026-05-03 23:23:21.124 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122403 bytes (attempt 1)
2026-05-03 23:23:23.175 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 126313 bytes (attempt 1)
2026-05-03 23:23:23.288 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.5699
2026-05-03 23:23:23.288 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'W' verified at (8,12)
2026-05-03 23:23:23.794 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'E' (slot 1) -> board (8,14) | src=(1034.4,830.0) dst=(1198.8,459.9)
2026-05-03 23:23:24.799 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122240 bytes (attempt 1)
2026-05-03 23:23:27.511 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121843 bytes (attempt 1)
2026-05-03 23:23:27.656 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 1.6807
2026-05-03 23:23:27.657 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'E' verified at (8,14)
2026-05-03 23:23:28.780 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120849 bytes (attempt 1)
2026-05-03 23:23:28.797 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:849 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt1_TAWIE.png
2026-05-03 23:23:29.434 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:23:29.434 | INFO    | src.browser.tile_placer:_click_confirm:799 | Clicking confirm/PLAY button at (1145.1, 748.1)
2026-05-03 23:23:31.132 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121764 bytes (attempt 1)
2026-05-03 23:23:31.232 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:824 | Post-confirm poll 1/3: my_turn
2026-05-03 23:23:31.233 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:830 | Re-clicking PLAY (retry after 1 polls)
2026-05-03 23:23:31.233 | INFO    | src.browser.tile_placer:_click_confirm:799 | Clicking confirm/PLAY button at (1148.8, 749.2)
2026-05-03 23:23:33.021 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121377 bytes (attempt 1)
2026-05-03 23:23:33.186 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:824 | Post-confirm poll 2/3: my_turn
2026-05-03 23:23:35.054 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121492 bytes (attempt 1)
2026-05-03 23:23:35.204 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:824 | Post-confirm poll 3/3: my_turn
2026-05-03 23:23:35.204 | INFO    | src.browser.tile_placer:place_move:1101 | Word 'TAWIE' rejected (attempt 1/5) — recalling tiles
2026-05-03 23:23:35.208 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'tawie' (total: 30)
2026-05-03 23:23:35.215 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1287.6, 749.3) (pass 1/6)
2026-05-03 23:23:36.164 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1285.2, 752.8) (pass 2/6)
2026-05-03 23:23:37.171 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1283.7, 752.5) (pass 3/6)
2026-05-03 23:23:38.074 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1287.1, 753.4) (pass 4/6)
2026-05-03 23:23:39.908 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1288.0, 750.9) (pass 5/6)
2026-05-03 23:23:43.082 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1287.0, 748.9) (pass 6/6)
2026-05-03 23:23:45.194 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122690 bytes (attempt 1)
2026-05-03 23:23:45.208 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:849 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-05-03 23:23:45.212 | INFO    | src.browser.tile_placer:place_move:1050 | Word attempt 2/5: 'TAW' (score=31)
2026-05-03 23:23:45.541 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-03 23:23:45.541 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'T' (slot 5) -> board (10,10) | src=(1255.4,825.4) dst=(992.6,528.9)
2026-05-03 23:23:47.882 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 123025 bytes (attempt 1)
2026-05-03 23:23:52.100 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 124193 bytes (attempt 1)
2026-05-03 23:23:52.481 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.6580
2026-05-03 23:23:52.489 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'T' verified at (10,10)
2026-05-03 23:23:53.026 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'A' (slot 0) -> board (10,11) | src=(980.5,830.1) dst=(1046.6,526.9)
2026-05-03 23:23:54.012 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 124995 bytes (attempt 1)
2026-05-03 23:23:55.919 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 125010 bytes (attempt 1)
2026-05-03 23:23:56.056 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.4115
2026-05-03 23:23:56.057 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'A' verified at (10,11)
2026-05-03 23:23:56.528 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'W' (slot 6) -> board (10,12) | src=(1311.9,827.8) dst=(1097.7,531.8)
2026-05-03 23:24:16.848 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:38 | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-05-03 23:24:17.466 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:46 | Viewport screenshot saved -> debug\iframe_missing.png
2026-05-03 23:24:17.467 | WARNING | __main__:_run:222 | place_move raised: Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)
2026-05-03 23:24:17.469 | ERROR   | __main__:_run:224 | place_move hit iframe-dead error — re-navigating: Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)
2026-05-03 23:24:17.471 | WARNING | __main__:_recover_iframe:140 | Iframe dead (1/2) — re-navigating: Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)
2026-05-03 23:24:18.243 | INFO    | src.browser.navigator:_run_navigation:82 | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
2026-05-03 23:24:32.444 | INFO    | src.browser.navigator:_run_navigation:121 | Join Voice button found — clicking to join voice channel
2026-05-03 23:24:39.066 | INFO    | src.browser.navigator:_run_navigation:137 | Opened Activity shelf
2026-05-03 23:24:41.475 | INFO    | src.browser.navigator:_run_navigation:158 | Selected Letter League from shelf
2026-05-03 23:24:41.839 | INFO    | src.browser.navigator:_run_navigation:176 | No launcher button — game may already be launching
2026-05-03 23:25:43.274 | ERROR   | src.browser.navigator:_run_navigation:202 | Iframe wait timed out after 60s. Page frames (2): ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-05-03 23:25:43.275 | WARNING | src.browser.navigator:navigate_to_activity:53 | Navigation attempt 1/3 failed: Activity iframe did not appear within 60 seconds. Retrying in 3 seconds...
2026-05-03 23:25:47.991 | INFO    | src.browser.navigator:_run_navigation:82 | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
2026-05-03 23:25:54.334 | INFO    | src.browser.navigator:_run_navigation:121 | Join Voice button found — clicking to join voice channel
2026-05-03 23:26:04.510 | INFO    | src.browser.navigator:_run_navigation:137 | Opened Activity shelf
2026-05-03 23:26:10.677 | INFO    | src.browser.navigator:_run_navigation:158 | Selected Letter League from shelf
2026-05-03 23:26:11.607 | INFO    | src.browser.navigator:_run_navigation:176 | No launcher button — game may already be launching
2026-05-03 23:27:14.632 | ERROR   | src.browser.navigator:_run_navigation:202 | Iframe wait timed out after 60s. Page frames (2): ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-05-03 23:27:14.633 | WARNING | src.browser.navigator:navigate_to_activity:53 | Navigation attempt 2/3 failed: Activity iframe did not appear within 60 seconds. Retrying in 3 seconds...
2026-05-03 23:27:17.994 | INFO    | src.browser.navigator:_run_navigation:82 | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
2026-05-03 23:27:33.363 | INFO    | src.browser.navigator:_run_navigation:121 | Join Voice button found — clicking to join voice channel
2026-05-03 23:27:44.074 | INFO    | src.browser.navigator:_run_navigation:137 | Opened Activity shelf
2026-05-03 23:27:48.496 | INFO    | src.browser.navigator:_run_navigation:158 | Selected Letter League from shelf
2026-05-03 23:27:48.997 | INFO    | src.browser.navigator:_run_navigation:176 | No launcher button — game may already be launching
2026-05-03 23:28:50.352 | ERROR   | src.browser.navigator:_run_navigation:202 | Iframe wait timed out after 60s. Page frames (2): ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-05-03 23:28:50.353 | ERROR   | src.browser.navigator:navigate_to_activity:61 | Navigation failed after 3 attempts: Activity iframe did not appear within 60 seconds
2026-05-03 23:28:51.124 | ERROR   | __main__:main:297 | Headless autoplay crashed
Traceback (most recent call last):

  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\tasks.py", line 507, in wait_for
    return await fut
                 └ <coroutine object Locator.screenshot at 0x000002B492738C40>
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\site-packages\patchright\async_api\_generated.py", line 17057, in screenshot
    await self._impl_obj.screenshot(
          │    │         └ <function Locator.screenshot at 0x000002B49064FC40>
          │    └ <Locator frame=<Frame name= url='https://discord.com/channels/1486201751353819208/1486201752477761590'> selector='iframe[src*...
          └ <Locator frame=<Frame name= url='https://discord.com/channels/1486201751353819208/1486201752477761590'> selector='iframe[src*...
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\site-packages\patchright\_impl\_locator.py", line 492, in screenshot
    return await self._with_element(
                 │    └ <function Locator._with_element at 0x000002B49064DC60>
                 └ <Locator frame=<Frame name= url='https://discord.com/channels/1486201751353819208/1486201752477761590'> selector='iframe[src*...
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\site-packages\patchright\_impl\_locator.py", line 92, in _with_element
    handle = await self.element_handle(timeout=timeout)
                   │    │                      └ 30000
                   │    └ <function Locator.element_handle at 0x000002B49064EA20>
                   └ <Locator frame=<Frame name= url='https://discord.com/channels/1486201751353819208/1486201752477761590'> selector='iframe[src*...
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\site-packages\patchright\_impl\_locator.py", line 302, in element_handle
    handle = await self._frame.wait_for_selector(
                   │    │      └ <function Frame.wait_for_selector at 0x000002B49068CA40>
                   │    └ <Frame name= url='https://discord.com/channels/1486201751353819208/1486201752477761590'>
                   └ <Locator frame=<Frame name= url='https://discord.com/channels/1486201751353819208/1486201752477761590'> selector='iframe[src*...
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\site-packages\patchright\_impl\_frame.py", line 342, in wait_for_selector
    await self._channel.send(
          │    │        └ <function Channel.send at 0x000002B490560540>
          │    └ <patchright._impl._connection.Channel object at 0x000002B4906C3310>
          └ <Frame name= url='https://discord.com/channels/1486201751353819208/1486201752477761590'>
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\site-packages\patchright\_impl\_connection.py", line 52, in send
    return await self._connection.wrap_api_call(
                 │    │           └ <function Connection.wrap_api_call at 0x000002B490562840>
                 │    └ <patchright._impl._connection.Connection object at 0x000002B490569E80>
                 └ <patchright._impl._connection.Channel object at 0x000002B4906C3310>
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\site-packages\patchright\_impl\_connection.py", line 498, in wrap_api_call
    return await cb()
                 └ <function Channel.send.<locals>.<lambda> at 0x000002B4914A8A40>
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\site-packages\patchright\_impl\_connection.py", line 102, in _inner_send
    done, _ = await asyncio.wait(
                    │       └ <function wait at 0x000002B4AE5C16C0>
                    └ <module 'asyncio' from 'C:\\Users\\Ninja\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\asyncio\\__init__.py'>
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\tasks.py", line 451, in wait
    return await _wait(fs, timeout, return_when, loop)
                 │     │   │        │            └ <ProactorEventLoop running=False closed=True debug=False>
                 │     │   │        └ 'FIRST_COMPLETED'
                 │     │   └ None
                 │     └ {<Future pending>, <Future finished exception=TimeoutError('Timeout 30000ms exceeded.\nCall log:\n  2 × waiting for locator("...
                 └ <function _wait at 0x000002B4AE5C18A0>
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\tasks.py", line 537, in _wait
    await waiter
          └ <Future cancelled>

asyncio.exceptions.CancelledError


The above exception was the direct cause of the following exception:


Traceback (most recent call last):

  File "C:\Github\Letter-League-Bot\src\browser\capture.py", line 132, in capture_canvas
    screenshot_bytes: bytes = await asyncio.wait_for(
                                    │       └ <function wait_for at 0x000002B4AE5C1800>
                                    └ <module 'asyncio' from 'C:\\Users\\Ninja\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\asyncio\\__init__.py'>

  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\tasks.py", line 506, in wait_for
    async with timeouts.timeout(timeout):
               │        │       └ 20.0
               │        └ <function timeout at 0x000002B4AE5B7F60>
               └ <module 'asyncio.timeouts' from 'C:\\Users\\Ninja\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\asyncio\\timeouts.py'>
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\timeouts.py", line 116, in __aexit__
    raise TimeoutError from exc_val
                            └ CancelledError()

TimeoutError


During handling of the above exception, another exception occurred:


Traceback (most recent call last):

  File "C:\Github\Letter-League-Bot\scripts\autoplay_headless.py", line 220, in _run
    accepted = await placer.place_move(candidates, rack, swap_on_fail=False)
                     │      │          │           └ ['A', 'E', 'U', 'A', 'Y', 'T', 'W']
                     │      │          └ [Move(word='TAWIE', start_row=8, start_col=10, direction='H', tiles_used=[TileUse(row=8, col=10, letter='T', is_blank=False, ...
                     │      └ <function TilePlacer.place_move at 0x000002B4DD5E8720>
                     └ <src.browser.tile_placer.TilePlacer object at 0x000002B490935010>

  File "C:\Github\Letter-League-Bot\src\browser\tile_placer.py", line 1059, in place_move
    await self.place_tiles(move, rack)
          │    │           │     └ ['A', 'E', 'U', 'A', 'Y', 'T', 'W']
          │    │           └ Move(word='TAW', start_row=10, start_col=10, direction='H', tiles_used=[TileUse(row=10, col=10, letter='T', is_blank=False, f...
          │    └ <function TilePlacer.place_tiles at 0x000002B4DD5E8180>
          └ <src.browser.tile_placer.TilePlacer object at 0x000002B490935010>

  File "C:\Github\Letter-League-Bot\src\browser\tile_placer.py", line 697, in place_tiles
    before_bytes = await capture_canvas(self._page, render_wait=False)
                         │              │    └ <Page url='https://discord.com/channels/1486201751353819208/1486201752477761590'>
                         │              └ <src.browser.tile_placer.TilePlacer object at 0x000002B490935010>
                         └ <function capture_canvas at 0x000002B4D97A5440>

  File "C:\Github\Letter-League-Bot\src\browser\capture.py", line 142, in capture_canvas
    raise RuntimeError(

RuntimeError: Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)


During handling of the above exception, another exception occurred:


Traceback (most recent call last):

  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code

  File "C:\Github\Letter-League-Bot\scripts\autoplay_headless.py", line 305, in <module>
    sys.exit(main())
    │   │    └ <function main at 0x000002B4AEBE9760>
    │   └ <built-in function exit>
    └ <module 'sys' (built-in)>

> File "C:\Github\Letter-League-Bot\scripts\autoplay_headless.py", line 292, in main
    code = asyncio.run(_run(args.max_turns, args.mode))
           │       │   │    │    │          │    └ 'wild'
           │       │   │    │    │          └ Namespace(max_turns=5, mode='wild')
           │       │   │    │    └ 5
           │       │   │    └ Namespace(max_turns=5, mode='wild')
           │       │   └ <function _run at 0x000002B4AEBE9440>
           │       └ <function run at 0x000002B4AE565620>
           └ <module 'asyncio' from 'C:\\Users\\Ninja\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\asyncio\\__init__.py'>
```

## Subprocess stderr (tail)
```

  File "[32mC:\Github\Letter-League-Bot\src\browser\[0m[32m[1mcapture.py[0m", line [33m142[0m, in [35mcapture_canvas[0m
    [35m[1mraise[0m [1mRuntimeError[0m[1m([0m

[31m[1mRuntimeError[0m:[1m Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)[0m


[1mDuring handling of the above exception, another exception occurred:[0m


[33m[1mTraceback (most recent call last):[0m

  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code

  File "[32mC:\Github\Letter-League-Bot\scripts\[0m[32m[1mautoplay_headless.py[0m", line [33m305[0m, in [35m<module>[0m
    [1msys[0m[35m[1m.[0m[1mexit[0m[1m([0m[1mmain[0m[1m([0m[1m)[0m[1m)[0m
    [36m│   │    └ [0m[36m[1m<function main at 0x000002B4AEBE9760>[0m
    [36m│   └ [0m[36m[1m<built-in function exit>[0m
    [36m└ [0m[36m[1m<module 'sys' (built-in)>[0m

> File "[32mC:\Github\Letter-League-Bot\scripts\[0m[32m[1mautoplay_headless.py[0m", line [33m292[0m, in [35mmain[0m
    [1mcode[0m [35m[1m=[0m [1masyncio[0m[35m[1m.[0m[1mrun[0m[1m([0m[1m_run[0m[1m([0m[1margs[0m[35m[1m.[0m[1mmax_turns[0m[1m,[0m [1margs[0m[35m[1m.[0m[1mmode[0m[1m)[0m[1m)[0m
    [36m       │       │   │    │    │          │    └ [0m[36m[1m'wild'[0m
    [36m       │       │   │    │    │          └ [0m[36m[1mNamespace(max_turns=5, mode='wild')[0m
    [36m       │       │   │    │    └ [0m[36m[1m5[0m
    [36m       │       │   │    └ [0m[36m[1mNamespace(max_turns=5, mode='wild')[0m
    [36m       │       │   └ [0m[36m[1m<function _run at 0x000002B4AEBE9440>[0m
    [36m       │       └ [0m[36m[1m<function run at 0x000002B4AE565620>[0m
    [36m       └ [0m[36m[1m<module 'asyncio' from 'C:\\Users\\Ninja\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\asyncio\\__init__.py'>[0m

  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\runners.py", line 194, in run
    return runner.run(main)
           │      │   └ <coroutine object _run at 0x000002B4AE653930>
           │      └ <function Runner.run at 0x000002B4AE5C7EC0>
           └ <asyncio.runners.Runner object at 0x000002B4AEC54050>
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           │    │                        └ <Task finished name='Task-1' coro=<_run() done, defined at C:\Github\Letter-League-Bot\scripts\autoplay_headless.py:74> excep...
           │    └ None
           └ <asyncio.runners.Runner object at 0x000002B4AEC54050>
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\base_events.py", line 720, in run_until_complete
    return future.result()
           │      └ <method 'result' of '_asyncio.Task' objects>
           └ <Task finished name='Task-1' coro=<_run() done, defined at C:\Github\Letter-League-Bot\scripts\autoplay_headless.py:74> excep...

  File "[32mC:\Github\Letter-League-Bot\scripts\[0m[32m[1mautoplay_headless.py[0m", line [33m227[0m, in [35m_run[0m
    [35m[1mif[0m [35m[1mnot[0m [35m[1mawait[0m [1m_recover_iframe[0m[1m([0m[1mstr[0m[1m([0m[1mexc[0m[1m)[0m[1m)[0m[1m:[0m
    [36m             └ [0m[36m[1m<function _run.<locals>._recover_iframe at 0x000002B490A00EA0>[0m

  File "[32mC:\Github\Letter-League-Bot\scripts\[0m[32m[1mautoplay_headless.py[0m", line [33m145[0m, in [35m_recover_iframe[0m
    [35m[1mawait[0m [1mnavigate_to_activity[0m[1m([0m[1mpage[0m[1m,[0m [1mchannel_url[0m[1m)[0m
    [36m      │                    │     └ [0m[36m[1m'https://discord.com/channels/1486201751353819208/1486201752477761590'[0m
    [36m      │                    └ [0m[36m[1m<Page url='https://discord.com/channels/1486201751353819208/1486201752477761590'>[0m
    [36m      └ [0m[36m[1m<function navigate_to_activity at 0x000002B4DB874C20>[0m

  File "[32mC:\Github\Letter-League-Bot\src\browser\[0m[32m[1mnavigator.py[0m", line [33m65[0m, in [35mnavigate_to_activity[0m
    [35m[1mraise[0m [1mlast_exc[0m  [30m[1m# type: ignore[misc][0m
    [36m      └ [0m[36m[1mRuntimeError('Activity iframe did not appear within 60 seconds')[0m

  File "[32mC:\Github\Letter-League-Bot\src\browser\[0m[32m[1mnavigator.py[0m", line [33m46[0m, in [35mnavigate_to_activity[0m
    [35m[1mreturn[0m [35m[1mawait[0m [1masyncio[0m[35m[1m.[0m[1mwait_for[0m[1m([0m
    [36m             │       └ [0m[36m[1m<function wait_for at 0x000002B4AE5C1800>[0m
    [36m             └ [0m[36m[1m<module 'asyncio' from 'C:\\Users\\Ninja\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\asyncio\\__init__.py'>[0m

  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\tasks.py", line 507, in wait_for
    return await fut
                 └ <coroutine object _run_navigation at 0x000002B4909E6DA0>

  File "[32mC:\Github\Letter-League-Bot\src\browser\[0m[32m[1mnavigator.py[0m", line [33m211[0m, in [35m_run_navigation[0m
    [35m[1mraise[0m [1mRuntimeError[0m[1m([0m

[31m[1mRuntimeError[0m:[1m Activity iframe did not appear within 60 seconds[0m
[32m23:28:51[0m | [1mINFO   [0m | Headless autoplay finished in 561.8s
Future exception was never retrieved
future: <Future finished exception=TimeoutError('Timeout 30000ms exceeded.\nCall log:\n  2 × waiting for locator("iframe[src*=\\"discordsays.com\\"]")\n')>
patchright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

```

## git status --short
```
D TESTING_REPORT.md
 M data/rejected_words.txt
 M debug/iframe_missing.png
 M debug/preprocessed_debug.png
 M debug/tile_placer/post_recall_attempt1.png
 M debug/tile_placer/post_recall_attempt2.png
 M debug/tile_placer/post_recall_attempt3.png
 M debug/tile_placer/post_recall_attempt4.png
 M debug/tile_placer/post_recall_attempt5.png
 M logs/auto_debug.log
 M logs/auto_debug_iter_001.md
 M logs/auto_debug_iter_001_response.md
 M logs/autoplay.log
 M scripts/auto_debug.py
 M src/browser/navigator.py
?? debug/tile_placer/pre_play_attempt1_INEPTER.png
?? debug/tile_placer/pre_play_attempt1_OYE.png
?? debug/tile_placer/pre_play_attempt1_REPENT.png
?? debug/tile_placer/pre_play_attempt1_TAWIE.png
?? debug/tile_placer/pre_play_attempt1_TRECENTO.png
?? debug/tile_placer/pre_play_attempt1_TUTOY.png
?? debug/tile_placer/pre_play_attempt1_YET.png
?? debug/tile_placer/pre_play_attempt1_YETI.png
?? debug/tile_placer/pre_play_attempt1_YU.png
?? debug/tile_placer/pre_play_attempt2_AYE.png
?? debug/tile_placer/pre_play_attempt2_AYU.png
?? debug/tile_placer/pre_play_attempt2_OATY.png
?? debug/tile_placer/pre_play_attempt2_UEY.png
?? debug/tile_placer/pre_play_attempt2_YAE.png
?? debug/tile_placer/pre_play_attempt3_EYOT.png
?? debug/tile_placer/pre_play_attempt3_TAY.png
?? debug/tile_placer/pre_play_attempt3_TYE.png
?? debug/tile_placer/pre_play_attempt3_YE.png
?? debug/tile_placer/pre_play_attempt3_YOU.png
?? debug/tile_placer/pre_play_attempt3_YOUR.png
?? debug/tile_placer/pre_play_attempt4_OY.png
?? debug/tile_placer/pre_play_attempt4_UNITY.png
?? debug/tile_placer/pre_play_attempt4_YATE.png
?? debug/tile_placer/pre_play_attempt4_YEA.png
?? debug/tile_placer/pre_play_attempt4_YEAR.png
?? debug/tile_placer/pre_play_attempt4_YO.png
?? debug/tile_placer/pre_play_attempt5_AY.png
?? debug/tile_placer/pre_play_attempt5_OUTEAT.png
?? debug/tile_placer/pre_play_attempt5_TOEY.png
?? debug/tile_placer/pre_play_attempt5_TOY.png
?? debug/tile_placer/pre_play_attempt5_YA.png
?? debug/tile_placer/pre_play_attempt5_YEAN.png
?? debug/turn_detection/frame_20260503_223115_507963_pre_start_attempt1.png
?? logs/_autoplay_stderr.tmp
?? logs/auto_debug_journal.md
```

## git diff --stat
```
TESTING_REPORT.md                          |  409 ----
 data/rejected_words.txt                    |  317 +---
 debug/iframe_missing.png                   |  Bin 135250 -> 78713 bytes
 debug/preprocessed_debug.png               |  Bin 383175 -> 376381 bytes
 debug/tile_placer/post_recall_attempt1.png |  Bin 15698 -> 122690 bytes
 debug/tile_placer/post_recall_attempt2.png |  Bin 121791 -> 118591 bytes
 debug/tile_placer/post_recall_attempt3.png |  Bin 122711 -> 118719 bytes
 debug/tile_placer/post_recall_attempt4.png |  Bin 122785 -> 118701 bytes
 debug/tile_placer/post_recall_attempt5.png |  Bin 123531 -> 112122 bytes
 logs/auto_debug.log                        |   90 +-
 logs/auto_debug_iter_001.md                | 1940 ++-----------------
 logs/auto_debug_iter_001_response.md       |   10 +-
 logs/autoplay.log                          | 2785 ++++++++++++++++++++++++++++
 scripts/auto_debug.py                      |  420 ++++-
 src/browser/navigator.py                   |   44 +-
 15 files changed, 3434 insertions(+), 2581 deletions(-)
```