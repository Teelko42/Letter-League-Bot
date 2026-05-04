# Auto-debug iteration 1

- exit_code: `-9`
- duration: 2429.8s
- error_signature: `ec19b0598068`

## Recent debug artifacts
- `debug/tile_placer/post_recall_attempt2.png`
- `debug/tile_placer/pre_play_attempt2_LAGENA.png`
- `debug/tile_placer/post_recall_attempt1.png`
- `debug/turn_detection/frame_20260428_105220_621800_pre_start_attempt1.png`
- `debug/iframe_missing.png`
- `debug/preprocessed_debug.png`

## Autoplay log — error region
```
2026-04-28 10:57:07.935 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1399
2026-04-28 10:57:07.936 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'E' placement not verified — retrying with fresh jitter
2026-04-28 10:57:08.821 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103816 bytes (attempt 1)
2026-04-28 10:57:11.026 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102872 bytes (attempt 1)
2026-04-28 10:57:11.206 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1168
2026-04-28 10:57:11.208 | ERROR   | src.browser.tile_placer:place_move:1074 | Tile placement failed for 'RANULAE' (attempt 3): Tile 'E' at (9,19) failed to place after retry
2026-04-28 10:57:11.397 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 10:57:12.292 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103554 bytes (attempt 1)
2026-04-28 10:57:12.293 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.3, 789.5) (pass 1/10)
2026-04-28 10:57:16.639 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101884 bytes (attempt 1)
2026-04-28 10:57:16.796 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.1, 788.6) (pass 2/10)
2026-04-28 10:57:19.913 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102446 bytes (attempt 1)
2026-04-28 10:57:20.074 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.5, 788.7) (pass 3/10)
2026-04-28 10:57:22.626 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102587 bytes (attempt 1)
2026-04-28 10:57:22.911 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.2, 787.1) (pass 4/10)
2026-04-28 10:57:25.138 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101997 bytes (attempt 1)
2026-04-28 10:57:25.302 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.4, 789.1) (pass 5/10)
2026-04-28 10:57:27.384 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101867 bytes (attempt 1)
2026-04-28 10:57:27.544 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.5, 787.3) (pass 6/10)
2026-04-28 10:57:29.855 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102539 bytes (attempt 1)
2026-04-28 10:57:30.030 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.0, 788.6) (pass 7/10)
2026-04-28 10:57:32.563 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102267 bytes (attempt 1)
2026-04-28 10:57:32.785 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.6, 788.2) (pass 8/10)
2026-04-28 10:57:35.521 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101502 bytes (attempt 1)
2026-04-28 10:57:35.671 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.0, 788.1) (pass 9/10)
2026-04-28 10:57:37.535 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101581 bytes (attempt 1)
2026-04-28 10:57:37.662 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.3, 790.9) (pass 10/10)
2026-04-28 10:57:39.523 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101573 bytes (attempt 1)
2026-04-28 10:57:39.650 | INFO    | src.browser.tile_placer:_recall_tiles:891 | Recall complete after 10 click(s) — canvas stable
2026-04-28 10:57:40.516 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101878 bytes (attempt 1)
2026-04-28 10:57:40.520 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt3.png
2026-04-28 10:57:40.520 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 4/4: 'LACUNAE' (score=56)
2026-04-28 10:57:40.675 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 10:57:40.677 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 3) -> board (9,13) | src=(1145.3,832.8) dst=(1145.2,516.2)
2026-04-28 10:57:41.558 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101689 bytes (attempt 1)
2026-04-28 10:57:43.347 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114672 bytes (attempt 1)
2026-04-28 10:57:43.498 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 6.7996
2026-04-28 10:57:43.499 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,13)
2026-04-28 10:57:44.110 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,14) | src=(980.0,831.8) dst=(1199.0,512.8)
2026-04-28 10:57:44.923 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115407 bytes (attempt 1)
2026-04-28 10:57:46.602 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114520 bytes (attempt 1)
2026-04-28 10:57:46.725 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1791
2026-04-28 10:57:46.726 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,14)
2026-04-28 10:57:47.410 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'C' (slot 1) -> board (9,15) | src=(1032.8,828.8) dst=(1249.6,515.6)
2026-04-28 10:57:48.234 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115521 bytes (attempt 1)
2026-04-28 10:57:49.940 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115398 bytes (attempt 1)
2026-04-28 10:57:50.154 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.2076
2026-04-28 10:57:52.017 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115390 bytes (attempt 1)
2026-04-28 10:57:53.460 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114618 bytes (attempt 1)
2026-04-28 10:57:53.575 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.2620
2026-04-28 10:57:53.576 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'C' via keyboard press
2026-04-28 10:57:54.077 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'C' verified at (9,15)
2026-04-28 10:57:54.718 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 5) -> board (9,16) | src=(1258.6,828.9) dst=(1295.1,512.9)
2026-04-28 10:57:55.561 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114490 bytes (attempt 1)
2026-04-28 10:57:57.313 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114545 bytes (attempt 1)
2026-04-28 10:57:57.546 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.2892
2026-04-28 10:57:57.547 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,16)
2026-04-28 10:57:58.080 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 4) -> board (9,17) | src=(1202.6,833.3) dst=(1349.1,515.7)
2026-04-28 10:57:59.437 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114686 bytes (attempt 1)
2026-04-28 10:58:01.200 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114831 bytes (attempt 1)
2026-04-28 10:58:01.325 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.2605
2026-04-28 10:58:01.326 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,17)
2026-04-28 10:58:01.828 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (9,18) | src=(1311.7,831.7) dst=(1400.7,516.2)
2026-04-28 10:58:02.718 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114126 bytes (attempt 1)
2026-04-28 10:58:04.486 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114838 bytes (attempt 1)
2026-04-28 10:58:04.600 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1332
2026-04-28 10:58:04.601 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'A' placement not verified — retrying with fresh jitter
2026-04-28 10:58:05.422 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114660 bytes (attempt 1)
2026-04-28 10:58:07.152 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114961 bytes (attempt 1)
2026-04-28 10:58:07.263 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4057
2026-04-28 10:58:07.265 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,18)
2026-04-28 10:58:07.887 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 2) -> board (9,19) | src=(1092.5,830.8) dst=(1448.0,515.4)
2026-04-28 10:58:08.685 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114126 bytes (attempt 1)
2026-04-28 10:58:10.362 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115146 bytes (attempt 1)
2026-04-28 10:58:10.480 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1884
2026-04-28 10:58:10.481 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (9,19)
2026-04-28 10:58:11.338 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114690 bytes (attempt 1)
2026-04-28 10:58:11.343 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt4_LACUNAE.png
2026-04-28 10:58:11.942 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 10:58:11.943 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1149.3, 788.2)
2026-04-28 10:58:13.419 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114691 bytes (attempt 1)
2026-04-28 10:58:13.532 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 10:58:13.533 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 10:58:13.533 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1145.5, 786.3)
2026-04-28 10:58:14.939 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115306 bytes (attempt 1)
2026-04-28 10:58:15.056 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 10:58:16.661 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114627 bytes (attempt 1)
2026-04-28 10:58:16.772 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 10:58:16.773 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LACUNAE' rejected (attempt 4/4) — recalling tiles
2026-04-28 10:58:16.777 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'lacunae' (total: 78)
2026-04-28 10:58:17.639 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114540 bytes (attempt 1)
2026-04-28 10:58:17.641 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.3, 788.2) (pass 1/10)
2026-04-28 10:58:19.626 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114586 bytes (attempt 1)
2026-04-28 10:58:19.744 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.2, 788.6) (pass 2/10)
2026-04-28 10:58:21.740 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114091 bytes (attempt 1)
2026-04-28 10:58:21.899 | INFO    | src.browser.tile_placer:_recall_tiles:891 | Recall complete after 2 click(s) — canvas stable
2026-04-28 10:58:22.730 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114127 bytes (attempt 1)
2026-04-28 10:58:22.733 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt4.png
2026-04-28 10:58:22.734 | WARNING | src.browser.tile_placer:place_move:1130 | All 4 word attempt(s) failed — returning to caller for re-vision
2026-04-28 10:58:22.735 | WARNING | __main__:_run:193 | No move accepted (candidates=5) — re-vision + swap fallback
2026-04-28 10:58:26.291 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115446 bytes (attempt 1)
2026-04-28 10:58:26.291 | INFO    | src.vision:extract_board_state:125 | Vision pipeline start — mode=wild
2026-04-28 10:58:26.328 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,51) 1366×625 from 1545×731 canvas
2026-04-28 10:58:26.583 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-04-28 10:58:26.686 | INFO    | src.vision:extract_board_state:131 | Preprocessing complete — 360185 bytes
2026-04-28 10:58:26.687 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=False
2026-04-28 10:58:30.815 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=4.12s  input_tokens=2905  output_tokens=77
2026-04-28 10:58:30.816 | INFO    | src.vision:extract_board_state:137 | Extraction complete (first attempt)
2026-04-28 10:58:30.816 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,13)=?*[DW]
2026-04-28 10:58:30.817 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['A', 'E', 'N', 'U', 'L', 'A']
2026-04-28 10:58:30.818 | DEBUG   | src.vision.validator:correct_positions:92 | Position auto-correction skipped: insufficient evidence (matches=1, informative=1, threshold=2 or 50%)
2026-04-28 10:58:30.818 | INFO    | src.vision:extract_board_state:155 | Validation result — 1 error(s)
2026-04-28 10:58:30.819 | WARNING | src.vision:extract_board_state:181 | Validation failed (1 errors), retrying: ["Invalid letter '?' at (9, 13)"]
2026-04-28 10:58:30.819 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=True
2026-04-28 10:58:33.675 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=2.85s  input_tokens=2933  output_tokens=77
2026-04-28 10:58:33.676 | INFO    | src.vision:extract_board_state:187 | Extraction complete (retry)
2026-04-28 10:58:33.676 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,13)=A[DW]
2026-04-28 10:58:33.676 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['A', 'E', 'N', 'U', 'L', 'A']
2026-04-28 10:58:33.677 | DEBUG   | src.vision.validator:correct_positions:92 | Position auto-correction skipped: insufficient evidence (matches=1, informative=1, threshold=2 or 50%)
2026-04-28 10:58:33.677 | INFO    | src.vision:extract_board_state:234 | Validation result after retry — 0 error(s)
2026-04-28 10:58:33.679 | INFO    | src.vision:extract_board_state:328 | Vision pipeline complete — 7.39s  tiles=1  rack_size=6
2026-04-28 10:58:33.759 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 8 blacklisted candidate(s)
2026-04-28 10:58:33.763 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 1/3: 'ALANE' (score=24)
2026-04-28 10:58:33.921 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 10:58:33.922 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,11) | src=(979.6,829.0) dst=(1043.8,511.4)
2026-04-28 10:58:34.748 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114173 bytes (attempt 1)
2026-04-28 10:58:36.808 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115127 bytes (attempt 1)
2026-04-28 10:58:37.317 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1750
2026-04-28 10:58:37.318 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,11)
2026-04-28 10:58:37.901 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 4) -> board (9,12) | src=(1202.6,829.9) dst=(1095.0,515.4)
2026-04-28 10:58:38.896 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115619 bytes (attempt 1)
2026-04-28 10:58:40.846 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115623 bytes (attempt 1)
2026-04-28 10:58:40.992 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.0351
2026-04-28 10:58:40.993 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'L' placement not verified — retrying with fresh jitter
2026-04-28 10:58:41.888 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115592 bytes (attempt 1)
2026-04-28 10:58:43.668 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114603 bytes (attempt 1)
2026-04-28 10:58:43.819 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1264
2026-04-28 10:58:43.820 | ERROR   | src.browser.tile_placer:place_move:1074 | Tile placement failed for 'ALANE' (attempt 1): Tile 'L' at (9,12) failed to place after retry
2026-04-28 10:58:43.955 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 10:58:44.763 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115285 bytes (attempt 1)
2026-04-28 10:58:44.764 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.1, 788.4) (pass 1/10)
2026-04-28 10:58:46.781 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114617 bytes (attempt 1)
2026-04-28 10:58:47.351 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.2, 789.8) (pass 2/10)
2026-04-28 10:58:50.835 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114699 bytes (attempt 1)
2026-04-28 10:58:51.140 | INFO    | src.browser.tile_placer:_recall_tiles:891 | Recall complete after 2 click(s) — canvas stable
2026-04-28 10:58:52.333 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 115492 bytes (attempt 1)
2026-04-28 10:58:52.336 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-04-28 10:58:52.338 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 2/3: 'LAUAN' (score=14)
2026-04-28 10:58:52.526 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 10:58:52.527 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 4) -> board (8,12) | src=(1204.0,828.6) dst=(1093.3,477.6)
2026-04-28 10:58:53.478 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 114620 bytes (attempt 1)
2026-04-28 10:58:55.370 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101984 bytes (attempt 1)
2026-04-28 10:58:55.542 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 6.3221
2026-04-28 10:58:55.544 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (8,12)
2026-04-28 10:58:56.225 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (8,13) | src=(980.7,833.2) dst=(1147.2,483.3)
2026-04-28 10:58:57.094 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102550 bytes (attempt 1)
2026-04-28 10:58:58.962 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103786 bytes (attempt 1)
2026-04-28 10:58:59.138 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8974
2026-04-28 10:58:59.138 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (8,13)
2026-04-28 10:58:59.779 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 3) -> board (8,14) | src=(1148.5,831.1) dst=(1195.7,480.6)
2026-04-28 10:59:00.930 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103899 bytes (attempt 1)
2026-04-28 10:59:02.646 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102899 bytes (attempt 1)
2026-04-28 10:59:02.799 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1285
2026-04-28 10:59:02.800 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'U' placement not verified — retrying with fresh jitter
2026-04-28 10:59:04.383 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103542 bytes (attempt 1)
2026-04-28 10:59:06.137 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103602 bytes (attempt 1)
2026-04-28 10:59:06.324 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.2986
2026-04-28 10:59:06.325 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (8,14)
2026-04-28 10:59:06.827 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 5) -> board (8,15) | src=(1258.5,828.1) dst=(1249.7,481.3)
2026-04-28 10:59:07.701 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102859 bytes (attempt 1)
2026-04-28 10:59:09.563 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104214 bytes (attempt 1)
2026-04-28 10:59:09.700 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6012
2026-04-28 10:59:09.701 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (8,15)
2026-04-28 10:59:10.282 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 2) -> board (8,16) | src=(1090.3,830.4) dst=(1298.9,480.1)
2026-04-28 10:59:11.181 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104275 bytes (attempt 1)
2026-04-28 10:59:14.162 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104902 bytes (attempt 1)
2026-04-28 10:59:14.310 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.9831
2026-04-28 10:59:14.311 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (8,16)
2026-04-28 10:59:15.278 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104139 bytes (attempt 1)
2026-04-28 10:59:15.282 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt2_LAUAN.png
2026-04-28 10:59:15.930 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 10:59:15.931 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1143.9, 790.6)
2026-04-28 10:59:17.467 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103740 bytes (attempt 1)
2026-04-28 10:59:17.581 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 10:59:17.582 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 10:59:17.584 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1146.7, 787.8)
2026-04-28 10:59:19.374 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103964 bytes (attempt 1)
2026-04-28 10:59:19.494 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 10:59:20.973 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104549 bytes (attempt 1)
2026-04-28 10:59:21.108 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 10:59:21.111 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LAUAN' rejected (attempt 2/3) — recalling tiles
2026-04-28 10:59:21.115 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'lauan' (total: 79)
2026-04-28 10:59:22.329 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104498 bytes (attempt 1)
2026-04-28 10:59:22.330 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.8, 787.7) (pass 1/10)
2026-04-28 10:59:25.051 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102221 bytes (attempt 1)
2026-04-28 10:59:25.213 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.7, 790.3) (pass 2/10)
2026-04-28 10:59:27.186 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102055 bytes (attempt 1)
2026-04-28 10:59:27.330 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.4, 786.0) (pass 3/10)
2026-04-28 10:59:29.229 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102172 bytes (attempt 1)
2026-04-28 10:59:29.383 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.4, 787.9) (pass 4/10)
2026-04-28 10:59:31.273 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101417 bytes (attempt 1)
2026-04-28 10:59:31.423 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.5, 789.6) (pass 5/10)
2026-04-28 10:59:33.402 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102018 bytes (attempt 1)
2026-04-28 10:59:33.559 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.9, 790.1) (pass 6/10)
2026-04-28 10:59:35.453 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101953 bytes (attempt 1)
2026-04-28 10:59:35.598 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.2, 788.8) (pass 7/10)
2026-04-28 10:59:37.869 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102505 bytes (attempt 1)
2026-04-28 10:59:38.171 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.9, 786.2) (pass 8/10)
2026-04-28 10:59:40.206 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102671 bytes (attempt 1)
2026-04-28 10:59:40.493 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.8, 786.1) (pass 9/10)
2026-04-28 10:59:43.272 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102015 bytes (attempt 1)
2026-04-28 10:59:43.791 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.6, 790.8) (pass 10/10)
2026-04-28 10:59:45.753 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102327 bytes (attempt 1)
2026-04-28 10:59:45.900 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 10:59:46.804 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102627 bytes (attempt 1)
2026-04-28 10:59:46.808 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt2.png
2026-04-28 10:59:46.809 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 3/3: 'ULNAE' (score=14)
2026-04-28 10:59:46.948 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 10:59:46.948 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 3) -> board (8,11) | src=(1144.5,833.6) dst=(1047.2,481.1)
2026-04-28 10:59:47.898 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102426 bytes (attempt 1)
2026-04-28 10:59:49.815 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103842 bytes (attempt 1)
2026-04-28 10:59:50.077 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6528
2026-04-28 10:59:50.078 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (8,11)
2026-04-28 10:59:50.726 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 4) -> board (8,12) | src=(1204.2,832.9) dst=(1095.1,480.3)
2026-04-28 10:59:52.547 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103272 bytes (attempt 1)
2026-04-28 10:59:54.488 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106705 bytes (attempt 1)
2026-04-28 10:59:54.645 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.0866
2026-04-28 10:59:54.646 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (8,12)
2026-04-28 10:59:55.166 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 2) -> board (8,13) | src=(1090.6,828.9) dst=(1146.2,482.2)
2026-04-28 10:59:56.060 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106766 bytes (attempt 1)
2026-04-28 10:59:58.043 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107513 bytes (attempt 1)
2026-04-28 10:59:58.225 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4715
2026-04-28 10:59:58.226 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (8,13)
2026-04-28 10:59:58.682 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (8,14) | src=(978.7,830.6) dst=(1193.9,483.3)
2026-04-28 10:59:59.654 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106535 bytes (attempt 1)
2026-04-28 11:00:01.551 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 117797 bytes (attempt 1)
2026-04-28 11:00:01.721 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 6.3649
2026-04-28 11:00:01.722 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (8,14)
2026-04-28 11:00:02.203 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 1) -> board (8,15) | src=(1038.2,832.5) dst=(1246.1,479.7)
2026-04-28 11:00:03.040 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 118517 bytes (attempt 1)
2026-04-28 11:00:04.745 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107037 bytes (attempt 1)
2026-04-28 11:00:04.922 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 6.2877
2026-04-28 11:00:04.923 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (8,15)
2026-04-28 11:00:05.862 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107186 bytes (attempt 1)
2026-04-28 11:00:05.888 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt3_ULNAE.png
2026-04-28 11:00:06.706 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:00:06.707 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1148.5, 789.4)
2026-04-28 11:00:08.138 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106897 bytes (attempt 1)
2026-04-28 11:00:08.259 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:00:08.259 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:00:08.260 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1148.8, 785.9)
2026-04-28 11:00:09.705 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106387 bytes (attempt 1)
2026-04-28 11:00:09.884 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:00:11.543 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106423 bytes (attempt 1)
2026-04-28 11:00:11.665 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:00:11.665 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'ULNAE' rejected (attempt 3/3) — recalling tiles
2026-04-28 11:00:11.669 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'ulnae' (total: 80)
2026-04-28 11:00:12.883 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107365 bytes (attempt 1)
2026-04-28 11:00:12.884 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.7, 789.9) (pass 1/10)
2026-04-28 11:00:15.069 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102077 bytes (attempt 1)
2026-04-28 11:00:15.229 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.3, 789.6) (pass 2/10)
2026-04-28 11:00:17.023 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102210 bytes (attempt 1)
2026-04-28 11:00:17.177 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.1, 790.0) (pass 3/10)
2026-04-28 11:00:19.248 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102390 bytes (attempt 1)
2026-04-28 11:00:19.408 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.5, 787.7) (pass 4/10)
2026-04-28 11:00:22.709 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101966 bytes (attempt 1)
2026-04-28 11:00:22.922 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.1, 788.0) (pass 5/10)
2026-04-28 11:00:25.149 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102360 bytes (attempt 1)
2026-04-28 11:00:25.285 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.8, 789.9) (pass 6/10)
2026-04-28 11:00:27.564 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101915 bytes (attempt 1)
2026-04-28 11:00:27.730 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.6, 791.0) (pass 7/10)
2026-04-28 11:00:29.752 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102018 bytes (attempt 1)
2026-04-28 11:00:30.165 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.2, 786.5) (pass 8/10)
2026-04-28 11:00:32.742 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101369 bytes (attempt 1)
2026-04-28 11:00:32.938 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.5, 788.3) (pass 9/10)
2026-04-28 11:00:35.997 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102229 bytes (attempt 1)
2026-04-28 11:00:36.216 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.9, 789.2) (pass 10/10)
2026-04-28 11:00:39.558 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101513 bytes (attempt 1)
2026-04-28 11:00:39.731 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:00:40.595 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101615 bytes (attempt 1)
2026-04-28 11:00:40.598 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt3.png
2026-04-28 11:00:40.599 | WARNING | src.browser.tile_placer:place_move:1122 | All 3 word attempt(s) failed — performing tile swap fallback
2026-04-28 11:00:40.849 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:00:40.850 | WARNING | src.browser.tile_placer:_tile_swap:993 | Falling back to tile swap at (1008.4, 789.9) — no valid words accepted after 5 attempts
2026-04-28 11:00:40.906 | INFO    | __main__:_run:217 | Turn 1: no move accepted (swap/skip)
2026-04-28 11:00:44.471 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101639 bytes (attempt 1)
2026-04-28 11:00:44.588 | INFO    | src.browser.turn_detector:poll_turn:647 | Turn state changed: None -> my_turn
2026-04-28 11:00:44.705 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:00:45.524 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101185 bytes (attempt 1)
2026-04-28 11:00:46.451 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101664 bytes (attempt 1)
2026-04-28 11:00:46.452 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1284.6, 788.7) (pass 1/10)
2026-04-28 11:00:49.934 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101674 bytes (attempt 1)
2026-04-28 11:00:50.104 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1282.8, 788.9) (pass 2/10)
2026-04-28 11:00:52.052 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101546 bytes (attempt 1)
2026-04-28 11:00:52.214 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1288.3, 786.5) (pass 3/10)
2026-04-28 11:00:55.360 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101133 bytes (attempt 1)
2026-04-28 11:00:55.554 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1288.6, 789.9) (pass 4/10)
2026-04-28 11:00:57.828 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101487 bytes (attempt 1)
2026-04-28 11:00:57.996 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1282.8, 790.0) (pass 5/10)
2026-04-28 11:01:00.004 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101577 bytes (attempt 1)
2026-04-28 11:01:00.507 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1286.1, 788.5) (pass 6/10)
2026-04-28 11:01:02.614 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101352 bytes (attempt 1)
2026-04-28 11:01:02.798 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1284.3, 786.2) (pass 7/10)
2026-04-28 11:01:04.970 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101716 bytes (attempt 1)
2026-04-28 11:01:05.142 | INFO    | src.browser.tile_placer:clear_stale_placements:973 | Pre-turn recall complete after 7 click(s) — canvas stable
2026-04-28 11:01:09.539 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101154 bytes (attempt 1)
2026-04-28 11:01:09.540 | INFO    | src.vision:extract_board_state:125 | Vision pipeline start — mode=wild
2026-04-28 11:01:09.574 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,51) 1366×625 from 1545×731 canvas
2026-04-28 11:01:09.810 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-04-28 11:01:09.914 | INFO    | src.vision:extract_board_state:131 | Preprocessing complete — 307723 bytes
2026-04-28 11:01:09.915 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=False
2026-04-28 11:01:12.422 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=2.50s  input_tokens=2905  output_tokens=57
2026-04-28 11:01:12.423 | INFO    | src.vision:extract_board_state:137 | Extraction complete (first attempt)
2026-04-28 11:01:12.459 | DEBUG   | src.vision:_log_extracted_state:40 | Vision extracted 0 cells
2026-04-28 11:01:12.462 | INFO    | src.vision:extract_board_state:155 | Validation result — 0 error(s)
2026-04-28 11:01:12.556 | INFO    | src.vision:extract_board_state:328 | Vision pipeline complete — 3.02s  tiles=0  rack_size=7
2026-04-28 11:01:13.510 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 86 blacklisted candidate(s)
2026-04-28 11:01:13.536 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 1/1: 'RANULAE' (score=56)
2026-04-28 11:01:13.713 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:01:13.713 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'R' (slot 3) -> board (9,13) | src=(1145.9,828.4) dst=(1147.5,513.0)
2026-04-28 11:01:14.597 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101242 bytes (attempt 1)
2026-04-28 11:01:16.648 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109088 bytes (attempt 1)
2026-04-28 11:01:16.784 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8860
2026-04-28 11:01:18.108 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108140 bytes (attempt 1)
2026-04-28 11:01:19.547 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104949 bytes (attempt 1)
2026-04-28 11:01:19.675 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.4243
2026-04-28 11:01:19.676 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'R' via keyboard press
2026-04-28 11:01:20.180 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'R' verified at (9,13)
2026-04-28 11:01:20.703 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,14) | src=(980.1,830.7) dst=(1194.8,514.3)
2026-04-28 11:01:21.615 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107622 bytes (attempt 1)
2026-04-28 11:01:23.501 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103660 bytes (attempt 1)
2026-04-28 11:01:23.633 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.0454
2026-04-28 11:01:23.633 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,14)
2026-04-28 11:01:24.309 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,15) | src=(1033.9,828.9) dst=(1245.3,512.6)
2026-04-28 11:01:25.219 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111307 bytes (attempt 1)
2026-04-28 11:01:26.968 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108182 bytes (attempt 1)
2026-04-28 11:01:27.090 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8719
2026-04-28 11:01:27.090 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,15)
2026-04-28 11:01:27.571 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,16) | src=(1199.7,828.2) dst=(1300.2,513.1)
2026-04-28 11:01:28.380 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105754 bytes (attempt 1)
2026-04-28 11:01:30.159 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110248 bytes (attempt 1)
2026-04-28 11:01:30.295 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4835
2026-04-28 11:01:30.296 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,16)
2026-04-28 11:01:30.804 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,17) | src=(1090.0,828.7) dst=(1348.5,515.6)
2026-04-28 11:01:31.640 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111468 bytes (attempt 1)
2026-04-28 11:01:33.383 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108977 bytes (attempt 1)
2026-04-28 11:01:33.685 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5989
2026-04-28 11:01:33.686 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,17)
2026-04-28 11:01:34.237 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (9,18) | src=(1313.1,833.6) dst=(1401.5,514.6)
2026-04-28 11:01:35.013 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105912 bytes (attempt 1)
2026-04-28 11:01:38.136 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103797 bytes (attempt 1)
2026-04-28 11:01:38.272 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.1097
2026-04-28 11:01:38.274 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,18)
2026-04-28 11:01:38.829 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 5) -> board (9,19) | src=(1258.3,832.1) dst=(1448.7,511.0)
2026-04-28 11:01:39.659 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109434 bytes (attempt 1)
2026-04-28 11:01:41.480 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107666 bytes (attempt 1)
2026-04-28 11:01:41.597 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4657
2026-04-28 11:01:41.598 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (9,19)
2026-04-28 11:01:42.425 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111853 bytes (attempt 1)
2026-04-28 11:01:42.433 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt1_RANULAE.png
2026-04-28 11:01:43.368 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:01:43.369 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1147.3, 790.9)
2026-04-28 11:01:44.808 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110089 bytes (attempt 1)
2026-04-28 11:01:44.947 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:01:44.948 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:01:44.949 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1146.3, 787.0)
2026-04-28 11:01:46.562 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109630 bytes (attempt 1)
2026-04-28 11:01:46.681 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:01:48.164 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107802 bytes (attempt 1)
2026-04-28 11:01:48.272 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:01:48.273 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'RANULAE' rejected (attempt 1/1) — recalling tiles
2026-04-28 11:01:48.277 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'ranulae' (total: 81)
2026-04-28 11:01:49.330 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109242 bytes (attempt 1)
2026-04-28 11:01:49.331 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.9, 786.0) (pass 1/10)
2026-04-28 11:01:51.179 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103666 bytes (attempt 1)
2026-04-28 11:01:51.318 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.8, 786.3) (pass 2/10)
2026-04-28 11:01:53.573 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106572 bytes (attempt 1)
2026-04-28 11:01:53.805 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.7, 787.1) (pass 3/10)
2026-04-28 11:01:55.974 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109893 bytes (attempt 1)
2026-04-28 11:01:56.120 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.6, 787.3) (pass 4/10)
2026-04-28 11:01:58.127 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110329 bytes (attempt 1)
2026-04-28 11:01:58.410 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.7, 789.8) (pass 5/10)
2026-04-28 11:02:00.651 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111412 bytes (attempt 1)
2026-04-28 11:02:00.802 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.4, 788.7) (pass 6/10)
2026-04-28 11:02:03.673 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110887 bytes (attempt 1)
2026-04-28 11:02:03.865 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.1, 788.0) (pass 7/10)
2026-04-28 11:02:05.899 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104940 bytes (attempt 1)
2026-04-28 11:02:06.064 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.0, 790.6) (pass 8/10)
2026-04-28 11:02:08.516 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105141 bytes (attempt 1)
2026-04-28 11:02:08.727 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.3, 789.9) (pass 9/10)
2026-04-28 11:02:10.905 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109928 bytes (attempt 1)
2026-04-28 11:02:11.065 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.2, 789.9) (pass 10/10)
2026-04-28 11:02:14.954 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108233 bytes (attempt 1)
2026-04-28 11:02:15.221 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:02:16.827 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103235 bytes (attempt 1)
2026-04-28 11:02:16.830 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-04-28 11:02:16.832 | WARNING | src.browser.tile_placer:place_move:1130 | All 1 word attempt(s) failed — returning to caller for re-vision
2026-04-28 11:02:16.833 | WARNING | __main__:_run:193 | No move accepted (candidates=5) — re-vision + swap fallback
2026-04-28 11:02:20.416 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105503 bytes (attempt 1)
2026-04-28 11:02:20.417 | INFO    | src.vision:extract_board_state:125 | Vision pipeline start — mode=wild
2026-04-28 11:02:20.460 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,51) 1366×625 from 1545×731 canvas
2026-04-28 11:02:20.721 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-04-28 11:02:20.838 | INFO    | src.vision:extract_board_state:131 | Preprocessing complete — 315823 bytes
2026-04-28 11:02:20.839 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=False
2026-04-28 11:02:24.280 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=3.44s  input_tokens=2905  output_tokens=54
2026-04-28 11:02:24.281 | INFO    | src.vision:extract_board_state:137 | Extraction complete (first attempt)
2026-04-28 11:02:24.282 | DEBUG   | src.vision:_log_extracted_state:40 | Vision extracted 0 cells
2026-04-28 11:02:24.282 | INFO    | src.vision:extract_board_state:155 | Validation result — 0 error(s)
2026-04-28 11:02:24.283 | INFO    | src.vision:extract_board_state:328 | Vision pipeline complete — 3.87s  tiles=0  rack_size=7
2026-04-28 11:02:25.064 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 100 blacklisted candidate(s)
2026-04-28 11:02:25.100 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 1/5: 'ANNUAL' (score=24)
2026-04-28 11:02:25.419 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:02:25.420 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,11) | src=(982.1,828.2) dst=(1041.9,516.2)
2026-04-28 11:02:26.558 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109909 bytes (attempt 1)
2026-04-28 11:02:28.292 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105785 bytes (attempt 1)
2026-04-28 11:02:28.445 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3676
2026-04-28 11:02:28.446 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,11)
2026-04-28 11:02:29.088 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,12) | src=(1035.2,829.8) dst=(1098.1,510.6)
2026-04-28 11:02:30.185 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110106 bytes (attempt 1)
2026-04-28 11:02:32.019 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107557 bytes (attempt 1)
2026-04-28 11:02:32.164 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4779
2026-04-28 11:02:32.165 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,12)
2026-04-28 11:02:32.825 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 3) -> board (9,13) | src=(1144.9,831.7) dst=(1148.2,513.2)
2026-04-28 11:02:33.677 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105147 bytes (attempt 1)
2026-04-28 11:02:35.513 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110396 bytes (attempt 1)
2026-04-28 11:02:35.656 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5134
2026-04-28 11:02:37.105 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108005 bytes (attempt 1)
2026-04-28 11:02:38.421 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108690 bytes (attempt 1)
2026-04-28 11:02:38.947 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.4967
2026-04-28 11:02:38.948 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'N' via keyboard press
2026-04-28 11:02:39.457 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,13)
2026-04-28 11:02:40.172 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,14) | src=(1202.8,831.3) dst=(1195.6,513.6)
2026-04-28 11:02:41.231 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106178 bytes (attempt 1)
2026-04-28 11:02:42.902 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112186 bytes (attempt 1)
2026-04-28 11:02:43.038 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8033
2026-04-28 11:02:43.040 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,14)
2026-04-28 11:02:43.641 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (9,15) | src=(1314.9,828.6) dst=(1246.9,513.0)
2026-04-28 11:02:44.450 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110782 bytes (attempt 1)
2026-04-28 11:02:46.260 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104445 bytes (attempt 1)
2026-04-28 11:02:46.425 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.0117
2026-04-28 11:02:46.426 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,15)
2026-04-28 11:02:46.975 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,16) | src=(1089.1,832.2) dst=(1297.3,515.7)
2026-04-28 11:02:48.355 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110741 bytes (attempt 1)
2026-04-28 11:02:50.161 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105178 bytes (attempt 1)
2026-04-28 11:02:50.332 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5434
2026-04-28 11:02:50.333 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,16)
2026-04-28 11:02:51.201 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107019 bytes (attempt 1)
2026-04-28 11:02:51.205 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt1_ANNUAL.png
2026-04-28 11:02:52.130 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:02:52.130 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1146.5, 786.9)
2026-04-28 11:02:53.715 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106605 bytes (attempt 1)
2026-04-28 11:02:53.832 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:02:53.833 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:02:53.834 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1148.6, 789.9)
2026-04-28 11:02:55.379 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103822 bytes (attempt 1)
2026-04-28 11:02:55.507 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:02:56.995 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112100 bytes (attempt 1)
2026-04-28 11:02:57.140 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:02:57.141 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'ANNUAL' rejected (attempt 1/5) — recalling tiles
2026-04-28 11:02:57.151 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'annual' (total: 82)
2026-04-28 11:02:58.123 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111833 bytes (attempt 1)
2026-04-28 11:02:58.124 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.2, 788.7) (pass 1/10)
2026-04-28 11:03:00.050 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107181 bytes (attempt 1)
2026-04-28 11:03:00.223 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.6, 790.8) (pass 2/10)
2026-04-28 11:03:02.318 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111260 bytes (attempt 1)
2026-04-28 11:03:02.578 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.0, 786.1) (pass 3/10)
2026-04-28 11:03:04.687 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104741 bytes (attempt 1)
2026-04-28 11:03:04.869 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.2, 785.6) (pass 4/10)
2026-04-28 11:03:06.897 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106611 bytes (attempt 1)
2026-04-28 11:03:07.070 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.0, 787.3) (pass 5/10)
2026-04-28 11:03:09.425 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106896 bytes (attempt 1)
2026-04-28 11:03:09.574 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.4, 785.2) (pass 6/10)
2026-04-28 11:03:11.528 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109571 bytes (attempt 1)
2026-04-28 11:03:11.690 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.7, 786.9) (pass 7/10)
2026-04-28 11:03:13.618 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104508 bytes (attempt 1)
2026-04-28 11:03:13.766 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.7, 789.7) (pass 8/10)
2026-04-28 11:03:15.843 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110152 bytes (attempt 1)
2026-04-28 11:03:16.022 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.9, 789.0) (pass 9/10)
2026-04-28 11:03:17.996 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111113 bytes (attempt 1)
2026-04-28 11:03:18.165 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.4, 789.0) (pass 10/10)
2026-04-28 11:03:20.573 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111105 bytes (attempt 1)
2026-04-28 11:03:20.708 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:03:21.702 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104626 bytes (attempt 1)
2026-04-28 11:03:21.705 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-04-28 11:03:21.706 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 2/5: 'UNABLE' (score=24)
2026-04-28 11:03:21.856 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:03:21.856 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,10) | src=(1204.3,829.6) dst=(993.0,510.5)
2026-04-28 11:03:23.094 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105239 bytes (attempt 1)
2026-04-28 11:03:25.008 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109972 bytes (attempt 1)
2026-04-28 11:03:25.232 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4810
2026-04-28 11:03:25.232 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,10)
2026-04-28 11:03:25.743 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,11) | src=(1032.8,830.8) dst=(1047.3,515.7)
2026-04-28 11:03:26.612 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106320 bytes (attempt 1)
2026-04-28 11:03:28.449 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111598 bytes (attempt 1)
2026-04-28 11:03:28.608 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5519
2026-04-28 11:03:28.609 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,11)
2026-04-28 11:03:29.300 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(977.9,833.5) dst=(1094.4,511.1)
2026-04-28 11:03:30.415 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105620 bytes (attempt 1)
2026-04-28 11:03:32.283 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111011 bytes (attempt 1)
2026-04-28 11:03:32.464 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5484
2026-04-28 11:03:32.465 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:03:33.076 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'B' (slot 3) -> board (9,13) | src=(1147.9,833.5) dst=(1144.9,515.6)
2026-04-28 11:03:33.977 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110265 bytes (attempt 1)
2026-04-28 11:03:35.930 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105821 bytes (attempt 1)
2026-04-28 11:03:36.105 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4784
2026-04-28 11:03:37.502 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111441 bytes (attempt 1)
2026-04-28 11:03:39.565 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105959 bytes (attempt 1)
2026-04-28 11:03:39.707 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.3665
2026-04-28 11:03:39.708 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'B' via keyboard press
2026-04-28 11:03:40.219 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'B' verified at (9,13)
2026-04-28 11:03:40.738 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,14) | src=(1090.3,833.8) dst=(1199.4,515.1)
2026-04-28 11:03:41.627 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112090 bytes (attempt 1)
2026-04-28 11:03:43.424 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107035 bytes (attempt 1)
2026-04-28 11:03:43.576 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5635
2026-04-28 11:03:43.577 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,14)
2026-04-28 11:03:44.120 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 5) -> board (9,15) | src=(1259.1,829.1) dst=(1247.9,510.6)
2026-04-28 11:03:45.019 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104190 bytes (attempt 1)
2026-04-28 11:03:46.683 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110864 bytes (attempt 1)
2026-04-28 11:03:46.835 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.0857
2026-04-28 11:03:46.836 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (9,15)
2026-04-28 11:03:48.011 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110333 bytes (attempt 1)
2026-04-28 11:03:48.016 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt2_UNABLE.png
2026-04-28 11:03:48.612 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:03:48.613 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1143.8, 790.3)
2026-04-28 11:03:50.184 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105475 bytes (attempt 1)
2026-04-28 11:03:50.314 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:03:50.315 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:03:50.316 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1144.3, 789.0)
2026-04-28 11:03:51.818 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106101 bytes (attempt 1)
2026-04-28 11:03:51.956 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:03:53.379 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112018 bytes (attempt 1)
2026-04-28 11:03:53.499 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:03:53.500 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'UNABLE' rejected (attempt 2/5) — recalling tiles
2026-04-28 11:03:53.503 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'unable' (total: 83)
2026-04-28 11:03:54.330 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105885 bytes (attempt 1)
2026-04-28 11:03:54.331 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.5, 785.5) (pass 1/10)
2026-04-28 11:03:56.236 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109269 bytes (attempt 1)
2026-04-28 11:03:56.438 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.6, 787.4) (pass 2/10)
2026-04-28 11:03:58.293 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110514 bytes (attempt 1)
2026-04-28 11:03:58.520 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.3, 789.6) (pass 3/10)
2026-04-28 11:04:00.367 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107581 bytes (attempt 1)
2026-04-28 11:04:00.517 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.9, 790.4) (pass 4/10)
2026-04-28 11:04:02.638 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112144 bytes (attempt 1)
2026-04-28 11:04:02.838 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.3, 785.1) (pass 5/10)
2026-04-28 11:04:04.807 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110714 bytes (attempt 1)
2026-04-28 11:04:04.954 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.4, 788.5) (pass 6/10)
2026-04-28 11:04:06.983 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104225 bytes (attempt 1)
2026-04-28 11:04:07.156 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.0, 786.3) (pass 7/10)
2026-04-28 11:04:09.495 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108054 bytes (attempt 1)
2026-04-28 11:04:09.679 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.8, 790.8) (pass 8/10)
2026-04-28 11:04:11.750 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111932 bytes (attempt 1)
2026-04-28 11:04:11.907 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.4, 785.6) (pass 9/10)
2026-04-28 11:04:14.250 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110622 bytes (attempt 1)
2026-04-28 11:04:14.387 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.1, 789.8) (pass 10/10)
2026-04-28 11:04:17.450 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103931 bytes (attempt 1)
2026-04-28 11:04:17.604 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:04:18.720 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105137 bytes (attempt 1)
2026-04-28 11:04:18.723 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt2.png
2026-04-28 11:04:18.724 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 3/5: 'LANDAU' (score=24)
2026-04-28 11:04:18.850 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:04:18.851 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,11) | src=(1093.1,828.4) dst=(1047.1,514.3)
2026-04-28 11:04:19.725 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106782 bytes (attempt 1)
2026-04-28 11:04:22.254 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109066 bytes (attempt 1)
2026-04-28 11:04:22.405 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4403
2026-04-28 11:04:22.406 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,11)
2026-04-28 11:04:22.986 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(979.4,833.5) dst=(1096.4,511.3)
2026-04-28 11:04:23.902 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104580 bytes (attempt 1)
2026-04-28 11:04:26.568 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104054 bytes (attempt 1)
2026-04-28 11:04:26.729 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.2329
2026-04-28 11:04:26.729 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:04:27.196 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,13) | src=(1033.1,830.6) dst=(1144.5,516.1)
2026-04-28 11:04:27.998 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111095 bytes (attempt 1)
2026-04-28 11:04:29.699 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107774 bytes (attempt 1)
2026-04-28 11:04:29.842 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6295
2026-04-28 11:04:29.843 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,13)
2026-04-28 11:04:30.409 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'D' (slot 3) -> board (9,14) | src=(1143.2,829.8) dst=(1196.7,515.6)
2026-04-28 11:04:31.294 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103329 bytes (attempt 1)
2026-04-28 11:04:33.076 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110694 bytes (attempt 1)
2026-04-28 11:04:33.273 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6719
2026-04-28 11:04:34.687 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106945 bytes (attempt 1)
2026-04-28 11:04:36.003 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105672 bytes (attempt 1)
2026-04-28 11:04:36.153 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.2141
2026-04-28 11:04:36.153 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'D' via keyboard press
2026-04-28 11:04:36.668 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'D' verified at (9,14)
2026-04-28 11:04:37.148 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (9,15) | src=(1309.9,829.0) dst=(1245.6,516.0)
2026-04-28 11:04:37.979 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110423 bytes (attempt 1)
2026-04-28 11:04:39.959 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104026 bytes (attempt 1)
2026-04-28 11:04:40.149 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8617
2026-04-28 11:04:40.149 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,15)
2026-04-28 11:04:40.791 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,16) | src=(1198.6,829.0) dst=(1299.3,515.8)
2026-04-28 11:04:41.663 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109582 bytes (attempt 1)
2026-04-28 11:04:43.963 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109438 bytes (attempt 1)
2026-04-28 11:04:44.145 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3986
2026-04-28 11:04:44.146 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,16)
2026-04-28 11:04:44.970 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111179 bytes (attempt 1)
2026-04-28 11:04:44.973 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt3_LANDAU.png
2026-04-28 11:04:45.979 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:04:45.980 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1149.4, 788.5)
2026-04-28 11:04:47.517 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111454 bytes (attempt 1)
2026-04-28 11:04:47.631 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:04:47.632 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:04:47.632 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1146.2, 788.0)
2026-04-28 11:04:49.414 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109671 bytes (attempt 1)
2026-04-28 11:04:49.583 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:04:51.443 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111109 bytes (attempt 1)
2026-04-28 11:04:51.569 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:04:51.571 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LANDAU' rejected (attempt 3/5) — recalling tiles
2026-04-28 11:04:51.576 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'landau' (total: 84)
2026-04-28 11:04:52.437 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105488 bytes (attempt 1)
2026-04-28 11:04:52.438 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.5, 788.1) (pass 1/10)
2026-04-28 11:04:54.371 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107629 bytes (attempt 1)
2026-04-28 11:04:54.521 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.6, 788.0) (pass 2/10)
2026-04-28 11:04:56.932 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107705 bytes (attempt 1)
2026-04-28 11:04:57.112 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.9, 787.0) (pass 3/10)
2026-04-28 11:04:58.985 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109688 bytes (attempt 1)
2026-04-28 11:04:59.145 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.6, 791.0) (pass 4/10)
2026-04-28 11:05:01.669 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108992 bytes (attempt 1)
2026-04-28 11:05:01.893 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.3, 787.5) (pass 5/10)
2026-04-28 11:05:04.167 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105159 bytes (attempt 1)
2026-04-28 11:05:04.334 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.3, 787.7) (pass 6/10)
2026-04-28 11:05:06.519 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105697 bytes (attempt 1)
2026-04-28 11:05:06.840 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.7, 787.5) (pass 7/10)
2026-04-28 11:05:09.097 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107075 bytes (attempt 1)
2026-04-28 11:05:09.259 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.8, 785.4) (pass 8/10)
2026-04-28 11:05:11.273 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108428 bytes (attempt 1)
2026-04-28 11:05:11.469 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.7, 787.6) (pass 9/10)
2026-04-28 11:05:13.295 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111099 bytes (attempt 1)
2026-04-28 11:05:13.440 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.9, 786.6) (pass 10/10)
2026-04-28 11:05:15.752 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109506 bytes (attempt 1)
2026-04-28 11:05:15.907 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:05:16.686 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103414 bytes (attempt 1)
2026-04-28 11:05:16.690 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt3.png
2026-04-28 11:05:16.691 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 4/5: 'LANGUE' (score=24)
2026-04-28 11:05:16.813 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:05:16.813 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,11) | src=(1088.6,833.1) dst=(1042.7,512.8)
2026-04-28 11:05:17.623 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107593 bytes (attempt 1)
2026-04-28 11:05:19.611 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109581 bytes (attempt 1)
2026-04-28 11:05:19.761 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3610
2026-04-28 11:05:19.763 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,11)
2026-04-28 11:05:20.411 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(978.4,828.3) dst=(1094.6,513.0)
2026-04-28 11:05:21.248 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108586 bytes (attempt 1)
2026-04-28 11:05:22.923 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105283 bytes (attempt 1)
2026-04-28 11:05:23.077 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5145
2026-04-28 11:05:23.079 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:05:23.678 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,13) | src=(1034.9,829.8) dst=(1145.6,510.7)
2026-04-28 11:05:24.456 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105332 bytes (attempt 1)
2026-04-28 11:05:26.254 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110267 bytes (attempt 1)
2026-04-28 11:05:26.402 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5799
2026-04-28 11:05:26.402 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,13)
2026-04-28 11:05:26.980 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'G' (slot 3) -> board (9,14) | src=(1144.9,833.2) dst=(1195.9,513.5)
2026-04-28 11:05:28.109 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105416 bytes (attempt 1)
2026-04-28 11:05:29.930 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111043 bytes (attempt 1)
2026-04-28 11:05:30.072 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5828
2026-04-28 11:05:31.608 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108266 bytes (attempt 1)
2026-04-28 11:05:32.879 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108815 bytes (attempt 1)
2026-04-28 11:05:33.059 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.1267
2026-04-28 11:05:33.060 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'G' via keyboard press
2026-04-28 11:05:33.570 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'G' verified at (9,14)
2026-04-28 11:05:34.211 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,15) | src=(1201.3,832.2) dst=(1247.5,514.5)
2026-04-28 11:05:35.196 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111983 bytes (attempt 1)
2026-04-28 11:05:36.883 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105136 bytes (attempt 1)
2026-04-28 11:05:37.027 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8221
2026-04-28 11:05:37.027 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,15)
2026-04-28 11:05:37.632 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 5) -> board (9,16) | src=(1253.8,832.8) dst=(1300.4,513.4)
2026-04-28 11:05:38.507 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105170 bytes (attempt 1)
2026-04-28 11:05:40.280 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111077 bytes (attempt 1)
2026-04-28 11:05:40.440 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5169
2026-04-28 11:05:40.440 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (9,16)
2026-04-28 11:05:41.361 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110871 bytes (attempt 1)
2026-04-28 11:05:41.367 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt4_LANGUE.png
2026-04-28 11:05:42.069 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:05:42.070 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1145.7, 785.4)
2026-04-28 11:05:43.668 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104529 bytes (attempt 1)
2026-04-28 11:05:43.799 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:05:43.800 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:05:43.801 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1146.8, 786.0)
2026-04-28 11:05:45.282 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110294 bytes (attempt 1)
2026-04-28 11:05:45.391 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:05:46.889 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110049 bytes (attempt 1)
2026-04-28 11:05:47.014 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:05:47.015 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LANGUE' rejected (attempt 4/5) — recalling tiles
2026-04-28 11:05:47.019 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'langue' (total: 85)
2026-04-28 11:05:48.271 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110154 bytes (attempt 1)
2026-04-28 11:05:48.272 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.5, 788.5) (pass 1/10)
2026-04-28 11:05:50.466 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105300 bytes (attempt 1)
2026-04-28 11:05:50.638 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.4, 785.6) (pass 2/10)
2026-04-28 11:05:52.602 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104941 bytes (attempt 1)
2026-04-28 11:05:52.782 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.6, 787.1) (pass 3/10)
2026-04-28 11:05:54.802 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109336 bytes (attempt 1)
2026-04-28 11:05:55.070 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.6, 786.8) (pass 4/10)
2026-04-28 11:05:56.883 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111479 bytes (attempt 1)
2026-04-28 11:05:57.034 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.1, 786.2) (pass 5/10)
2026-04-28 11:05:58.966 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105079 bytes (attempt 1)
2026-04-28 11:05:59.124 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.3, 788.7) (pass 6/10)
2026-04-28 11:06:01.232 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109719 bytes (attempt 1)
2026-04-28 11:06:01.412 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.0, 786.6) (pass 7/10)
2026-04-28 11:06:03.391 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110795 bytes (attempt 1)
2026-04-28 11:06:03.554 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.4, 790.7) (pass 8/10)
2026-04-28 11:06:05.717 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103128 bytes (attempt 1)
2026-04-28 11:06:05.902 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.8, 788.4) (pass 9/10)
2026-04-28 11:06:08.296 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105079 bytes (attempt 1)
2026-04-28 11:06:08.461 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.5, 787.2) (pass 10/10)
2026-04-28 11:06:10.261 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110147 bytes (attempt 1)
2026-04-28 11:06:10.412 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:06:11.252 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109550 bytes (attempt 1)
2026-04-28 11:06:11.256 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt4.png
2026-04-28 11:06:11.257 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 5/5: 'LANATE' (score=24)
2026-04-28 11:06:11.384 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:06:11.384 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,11) | src=(1092.8,833.4) dst=(1045.3,512.4)
2026-04-28 11:06:12.283 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103913 bytes (attempt 1)
2026-04-28 11:06:14.079 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111267 bytes (attempt 1)
2026-04-28 11:06:14.260 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.0797
2026-04-28 11:06:14.261 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,11)
2026-04-28 11:06:14.946 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(981.8,827.9) dst=(1097.4,513.6)
2026-04-28 11:06:16.500 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103880 bytes (attempt 1)
2026-04-28 11:06:18.233 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111659 bytes (attempt 1)
2026-04-28 11:06:18.430 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.0526
2026-04-28 11:06:18.432 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:06:18.925 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,13) | src=(1036.4,833.6) dst=(1147.1,514.8)
2026-04-28 11:06:19.838 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110706 bytes (attempt 1)
2026-04-28 11:06:21.593 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105246 bytes (attempt 1)
2026-04-28 11:06:21.727 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.2956
2026-04-28 11:06:21.728 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,13)
2026-04-28 11:06:22.345 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (9,14) | src=(1310.8,828.1) dst=(1195.5,513.3)
2026-04-28 11:06:23.258 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110070 bytes (attempt 1)
2026-04-28 11:06:24.950 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110099 bytes (attempt 1)
2026-04-28 11:06:25.098 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.7335
2026-04-28 11:06:25.099 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,14)
2026-04-28 11:06:25.741 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'T' (slot 3) -> board (9,15) | src=(1144.5,832.2) dst=(1250.1,513.0)
2026-04-28 11:06:27.189 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104214 bytes (attempt 1)
2026-04-28 11:06:29.375 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110434 bytes (attempt 1)
2026-04-28 11:06:29.526 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.9974
2026-04-28 11:06:31.768 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109695 bytes (attempt 1)
2026-04-28 11:06:34.639 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111798 bytes (attempt 1)
2026-04-28 11:06:34.923 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.6656
2026-04-28 11:06:34.923 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'T' via keyboard press
2026-04-28 11:06:35.427 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'T' verified at (9,15)
2026-04-28 11:06:35.916 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 5) -> board (9,16) | src=(1257.7,831.7) dst=(1299.4,513.8)
2026-04-28 11:06:37.070 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110449 bytes (attempt 1)
2026-04-28 11:06:38.982 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104959 bytes (attempt 1)
2026-04-28 11:06:39.161 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4389
2026-04-28 11:06:39.162 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (9,16)
2026-04-28 11:06:40.151 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103364 bytes (attempt 1)
2026-04-28 11:06:40.155 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt5_LANATE.png
2026-04-28 11:06:40.948 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:06:40.949 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1144.0, 786.7)
2026-04-28 11:06:42.451 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106804 bytes (attempt 1)
2026-04-28 11:06:42.648 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:06:42.649 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:06:42.650 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1147.2, 787.5)
2026-04-28 11:06:44.185 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110817 bytes (attempt 1)
2026-04-28 11:06:44.309 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:06:45.758 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108114 bytes (attempt 1)
2026-04-28 11:06:45.881 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:06:45.881 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LANATE' rejected (attempt 5/5) — recalling tiles
2026-04-28 11:06:45.885 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'lanate' (total: 86)
2026-04-28 11:06:46.755 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110178 bytes (attempt 1)
2026-04-28 11:06:46.755 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.8, 790.9) (pass 1/10)
2026-04-28 11:06:48.761 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104466 bytes (attempt 1)
2026-04-28 11:06:49.222 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.0, 789.1) (pass 2/10)
2026-04-28 11:06:51.103 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106962 bytes (attempt 1)
2026-04-28 11:06:51.284 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.0, 790.5) (pass 3/10)
2026-04-28 11:06:53.518 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106405 bytes (attempt 1)
2026-04-28 11:06:53.677 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.0, 786.8) (pass 4/10)
2026-04-28 11:06:55.727 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108770 bytes (attempt 1)
2026-04-28 11:06:55.894 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.6, 788.9) (pass 5/10)
2026-04-28 11:06:57.957 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109654 bytes (attempt 1)
2026-04-28 11:06:58.159 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.9, 785.6) (pass 6/10)
2026-04-28 11:07:00.382 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110853 bytes (attempt 1)
2026-04-28 11:07:00.579 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.2, 788.8) (pass 7/10)
2026-04-28 11:07:03.215 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105873 bytes (attempt 1)
2026-04-28 11:07:03.421 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.3, 790.4) (pass 8/10)
2026-04-28 11:07:06.172 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105162 bytes (attempt 1)
2026-04-28 11:07:06.337 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.9, 786.9) (pass 9/10)
2026-04-28 11:07:08.350 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103761 bytes (attempt 1)
2026-04-28 11:07:08.525 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.4, 788.4) (pass 10/10)
2026-04-28 11:07:10.410 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109618 bytes (attempt 1)
2026-04-28 11:07:10.571 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:07:11.428 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111310 bytes (attempt 1)
2026-04-28 11:07:11.435 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt5.png
2026-04-28 11:07:11.435 | WARNING | src.browser.tile_placer:place_move:1122 | All 5 word attempt(s) failed — performing tile swap fallback
2026-04-28 11:07:11.579 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:07:11.580 | WARNING | src.browser.tile_placer:_tile_swap:993 | Falling back to tile swap at (1005.3, 790.5) — no valid words accepted after 5 attempts
2026-04-28 11:07:11.604 | INFO    | __main__:_run:217 | Turn 2: no move accepted (swap/skip)
2026-04-28 11:07:15.255 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110964 bytes (attempt 1)
2026-04-28 11:07:15.400 | INFO    | src.browser.turn_detector:poll_turn:647 | Turn state changed: None -> my_turn
2026-04-28 11:07:15.543 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:07:16.737 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107297 bytes (attempt 1)
2026-04-28 11:07:17.956 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109754 bytes (attempt 1)
2026-04-28 11:07:17.957 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1288.6, 786.7) (pass 1/10)
2026-04-28 11:07:20.300 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109881 bytes (attempt 1)
2026-04-28 11:07:20.591 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1283.4, 787.9) (pass 2/10)
2026-04-28 11:07:22.555 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109788 bytes (attempt 1)
2026-04-28 11:07:22.710 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1284.3, 790.9) (pass 3/10)
2026-04-28 11:07:24.848 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103379 bytes (attempt 1)
2026-04-28 11:07:25.034 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1287.8, 790.2) (pass 4/10)
2026-04-28 11:07:26.915 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105683 bytes (attempt 1)
2026-04-28 11:07:27.132 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1283.0, 790.3) (pass 5/10)
2026-04-28 11:07:29.103 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109423 bytes (attempt 1)
2026-04-28 11:07:29.290 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1285.3, 787.6) (pass 6/10)
2026-04-28 11:07:31.477 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109625 bytes (attempt 1)
2026-04-28 11:07:31.678 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1282.7, 787.6) (pass 7/10)
2026-04-28 11:07:33.599 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104358 bytes (attempt 1)
2026-04-28 11:07:33.839 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1285.9, 786.5) (pass 8/10)
2026-04-28 11:07:35.829 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105201 bytes (attempt 1)
2026-04-28 11:07:35.994 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1286.3, 787.0) (pass 9/10)
2026-04-28 11:07:37.905 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107208 bytes (attempt 1)
2026-04-28 11:07:38.068 | INFO    | src.browser.tile_placer:clear_stale_placements:973 | Pre-turn recall complete after 9 click(s) — canvas stable
2026-04-28 11:07:42.052 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108095 bytes (attempt 1)
2026-04-28 11:07:42.053 | INFO    | src.vision:extract_board_state:125 | Vision pipeline start — mode=wild
2026-04-28 11:07:42.099 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,51) 1366×625 from 1545×731 canvas
2026-04-28 11:07:42.343 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-04-28 11:07:42.472 | INFO    | src.vision:extract_board_state:131 | Preprocessing complete — 314791 bytes
2026-04-28 11:07:42.473 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=False
2026-04-28 11:07:46.752 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=4.28s  input_tokens=2905  output_tokens=78
2026-04-28 11:07:46.758 | INFO    | src.vision:extract_board_state:137 | Extraction complete (first attempt)
2026-04-28 11:07:46.758 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,13)=[DW]
2026-04-28 11:07:46.759 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['A', 'N', 'L', '?', 'U', 'E', 'A']
2026-04-28 11:07:46.759 | INFO    | src.vision:extract_board_state:155 | Validation result — 0 error(s)
2026-04-28 11:07:46.760 | INFO    | src.vision:extract_board_state:328 | Vision pipeline complete — 4.71s  tiles=0  rack_size=7
2026-04-28 11:07:48.134 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 160 blacklisted candidate(s)
2026-04-28 11:07:48.159 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 1/5: 'MANUAL' (score=24)
2026-04-28 11:07:48.303 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:07:48.304 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'M' (slot 3) -> board (9,11) | src=(1148.2,833.3) dst=(1043.6,515.0)
2026-04-28 11:07:49.189 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104788 bytes (attempt 1)
2026-04-28 11:07:50.919 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103825 bytes (attempt 1)
2026-04-28 11:07:51.051 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6879
2026-04-28 11:07:52.878 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104296 bytes (attempt 1)
2026-04-28 11:07:54.404 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108689 bytes (attempt 1)
2026-04-28 11:07:54.522 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.2742
2026-04-28 11:07:54.523 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'M' via keyboard press
2026-04-28 11:07:55.028 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'M' verified at (9,11)
2026-04-28 11:07:55.601 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(980.5,828.7) dst=(1094.5,512.0)
2026-04-28 11:07:56.378 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104769 bytes (attempt 1)
2026-04-28 11:07:58.083 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110260 bytes (attempt 1)
2026-04-28 11:07:58.209 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6336
2026-04-28 11:07:58.210 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:07:58.877 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,13) | src=(1032.5,832.0) dst=(1145.5,510.6)
2026-04-28 11:07:59.689 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109550 bytes (attempt 1)
2026-04-28 11:08:01.518 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105299 bytes (attempt 1)
2026-04-28 11:08:01.628 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3848
2026-04-28 11:08:01.629 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,13)
2026-04-28 11:08:02.228 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,14) | src=(1203.7,832.1) dst=(1197.1,514.1)
2026-04-28 11:08:02.991 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110525 bytes (attempt 1)
2026-04-28 11:08:05.183 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106028 bytes (attempt 1)
2026-04-28 11:08:05.309 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6717
2026-04-28 11:08:05.310 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,14)
2026-04-28 11:08:05.961 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (9,15) | src=(1313.2,830.2) dst=(1246.7,512.6)
2026-04-28 11:08:06.759 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105592 bytes (attempt 1)
2026-04-28 11:08:08.632 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110215 bytes (attempt 1)
2026-04-28 11:08:08.970 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4316
2026-04-28 11:08:08.971 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,15)
2026-04-28 11:08:09.387 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,16) | src=(1091.2,829.2) dst=(1295.4,515.4)
2026-04-28 11:08:10.302 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105456 bytes (attempt 1)
2026-04-28 11:08:12.152 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110727 bytes (attempt 1)
2026-04-28 11:08:12.284 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3382
2026-04-28 11:08:12.285 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,16)
2026-04-28 11:08:13.110 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109665 bytes (attempt 1)
2026-04-28 11:08:13.116 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt1_MANUAL.png
2026-04-28 11:08:13.858 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:08:13.858 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1147.3, 785.5)
2026-04-28 11:08:15.302 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104758 bytes (attempt 1)
2026-04-28 11:08:15.534 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:08:15.536 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:08:15.536 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1147.5, 786.2)
2026-04-28 11:08:17.099 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112085 bytes (attempt 1)
2026-04-28 11:08:17.202 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:08:18.613 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108894 bytes (attempt 1)
2026-04-28 11:08:18.774 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:08:18.774 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'MANUAL' rejected (attempt 1/5) — recalling tiles
2026-04-28 11:08:18.777 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'manual' (total: 87)
2026-04-28 11:08:19.544 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110395 bytes (attempt 1)
2026-04-28 11:08:19.545 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.6, 787.1) (pass 1/10)
2026-04-28 11:08:22.337 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111829 bytes (attempt 1)
2026-04-28 11:08:22.455 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.3, 790.2) (pass 2/10)
2026-04-28 11:08:24.340 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106252 bytes (attempt 1)
2026-04-28 11:08:24.527 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.8, 787.0) (pass 3/10)
2026-04-28 11:08:26.352 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111495 bytes (attempt 1)
2026-04-28 11:08:26.471 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.7, 787.3) (pass 4/10)
2026-04-28 11:08:28.442 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105706 bytes (attempt 1)
2026-04-28 11:08:29.291 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.5, 789.3) (pass 5/10)
2026-04-28 11:08:31.299 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104726 bytes (attempt 1)
2026-04-28 11:08:31.450 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.5, 786.0) (pass 6/10)
2026-04-28 11:08:33.438 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105053 bytes (attempt 1)
2026-04-28 11:08:33.573 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.9, 789.4) (pass 7/10)
2026-04-28 11:08:35.423 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109777 bytes (attempt 1)
2026-04-28 11:08:35.553 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.1, 785.9) (pass 8/10)
2026-04-28 11:08:37.575 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104859 bytes (attempt 1)
2026-04-28 11:08:37.702 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.4, 786.7) (pass 9/10)
2026-04-28 11:08:39.935 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105288 bytes (attempt 1)
2026-04-28 11:08:40.067 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.1, 790.9) (pass 10/10)
2026-04-28 11:08:42.071 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106398 bytes (attempt 1)
2026-04-28 11:08:42.228 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:08:43.003 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110016 bytes (attempt 1)
2026-04-28 11:08:43.010 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-04-28 11:08:43.010 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 2/5: 'LACUNE' (score=24)
2026-04-28 11:08:43.258 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:08:43.258 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,11) | src=(1091.6,828.7) dst=(1042.7,513.3)
2026-04-28 11:08:44.149 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110665 bytes (attempt 1)
2026-04-28 11:08:45.842 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106749 bytes (attempt 1)
2026-04-28 11:08:45.957 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3967
2026-04-28 11:08:45.958 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,11)
2026-04-28 11:08:46.659 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(980.7,830.5) dst=(1098.0,515.5)
2026-04-28 11:08:47.680 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109752 bytes (attempt 1)
2026-04-28 11:08:49.544 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108310 bytes (attempt 1)
2026-04-28 11:08:49.677 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4313
2026-04-28 11:08:49.677 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:08:50.111 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'C' (slot 3) -> board (9,13) | src=(1146.4,829.0) dst=(1147.7,516.3)
2026-04-28 11:08:51.068 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106491 bytes (attempt 1)
2026-04-28 11:08:53.007 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111578 bytes (attempt 1)
2026-04-28 11:08:53.136 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5713
2026-04-28 11:08:54.632 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109448 bytes (attempt 1)
2026-04-28 11:08:56.030 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107545 bytes (attempt 1)
2026-04-28 11:08:56.161 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.3245
2026-04-28 11:08:56.162 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'C' via keyboard press
2026-04-28 11:08:56.664 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'C' verified at (9,13)
2026-04-28 11:08:57.131 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,14) | src=(1203.4,827.9) dst=(1199.2,515.0)
2026-04-28 11:08:57.992 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110161 bytes (attempt 1)
2026-04-28 11:08:59.740 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109868 bytes (attempt 1)
2026-04-28 11:08:59.894 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5555
2026-04-28 11:08:59.895 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,14)
2026-04-28 11:09:00.382 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,15) | src=(1034.4,829.7) dst=(1247.8,513.3)
2026-04-28 11:09:01.345 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107171 bytes (attempt 1)
2026-04-28 11:09:03.122 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105445 bytes (attempt 1)
2026-04-28 11:09:03.289 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4517
2026-04-28 11:09:03.290 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,15)
2026-04-28 11:09:03.741 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 5) -> board (9,16) | src=(1259.1,831.3) dst=(1299.8,511.5)
2026-04-28 11:09:04.846 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112214 bytes (attempt 1)
2026-04-28 11:09:06.963 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110286 bytes (attempt 1)
2026-04-28 11:09:07.134 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4872
2026-04-28 11:09:07.135 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (9,16)
2026-04-28 11:09:08.162 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107481 bytes (attempt 1)
2026-04-28 11:09:08.167 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt2_LACUNE.png
2026-04-28 11:09:08.791 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:09:08.792 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1146.5, 787.4)
2026-04-28 11:09:10.546 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112406 bytes (attempt 1)
2026-04-28 11:09:10.700 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:09:10.701 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:09:10.701 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1147.6, 788.1)
2026-04-28 11:09:12.294 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107636 bytes (attempt 1)
2026-04-28 11:09:12.423 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:09:13.953 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110621 bytes (attempt 1)
2026-04-28 11:09:14.078 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:09:14.079 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LACUNE' rejected (attempt 2/5) — recalling tiles
2026-04-28 11:09:14.082 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'lacune' (total: 88)
2026-04-28 11:09:14.868 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106165 bytes (attempt 1)
2026-04-28 11:09:14.869 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.3, 786.0) (pass 1/10)
2026-04-28 11:09:16.848 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112788 bytes (attempt 1)
2026-04-28 11:09:17.013 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.5, 788.4) (pass 2/10)
2026-04-28 11:09:19.126 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110523 bytes (attempt 1)
2026-04-28 11:09:19.379 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.0, 788.8) (pass 3/10)
2026-04-28 11:09:21.468 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104242 bytes (attempt 1)
2026-04-28 11:09:21.621 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.3, 787.0) (pass 4/10)
2026-04-28 11:09:23.617 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110248 bytes (attempt 1)
2026-04-28 11:09:23.833 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.6, 790.1) (pass 5/10)
2026-04-28 11:09:25.811 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106188 bytes (attempt 1)
2026-04-28 11:09:25.951 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.3, 786.3) (pass 6/10)
2026-04-28 11:09:27.990 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105935 bytes (attempt 1)
2026-04-28 11:09:28.155 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.9, 785.1) (pass 7/10)
2026-04-28 11:09:30.083 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111360 bytes (attempt 1)
2026-04-28 11:09:30.266 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.5, 789.2) (pass 8/10)
2026-04-28 11:09:32.377 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106196 bytes (attempt 1)
2026-04-28 11:09:32.566 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.7, 790.1) (pass 9/10)
2026-04-28 11:09:34.510 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107973 bytes (attempt 1)
2026-04-28 11:09:34.666 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.4, 785.9) (pass 10/10)
2026-04-28 11:09:36.791 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110996 bytes (attempt 1)
2026-04-28 11:09:37.087 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:09:38.115 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110702 bytes (attempt 1)
2026-04-28 11:09:38.120 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt2.png
2026-04-28 11:09:38.121 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 3/5: 'LACUNA' (score=24)
2026-04-28 11:09:38.254 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:09:38.255 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,11) | src=(1088.0,829.8) dst=(1047.7,512.7)
2026-04-28 11:09:39.369 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112284 bytes (attempt 1)
2026-04-28 11:09:41.620 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111633 bytes (attempt 1)
2026-04-28 11:09:41.780 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8010
2026-04-28 11:09:41.781 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,11)
2026-04-28 11:09:42.374 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(983.0,833.0) dst=(1098.2,511.2)
2026-04-28 11:09:43.426 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109445 bytes (attempt 1)
2026-04-28 11:09:45.186 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105418 bytes (attempt 1)
2026-04-28 11:09:45.354 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6519
2026-04-28 11:09:45.355 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:09:45.784 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'C' (slot 3) -> board (9,13) | src=(1144.0,829.0) dst=(1146.8,516.3)
2026-04-28 11:09:46.606 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105372 bytes (attempt 1)
2026-04-28 11:09:48.285 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111885 bytes (attempt 1)
2026-04-28 11:09:48.432 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5996
2026-04-28 11:09:49.858 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108020 bytes (attempt 1)
2026-04-28 11:09:51.184 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108149 bytes (attempt 1)
2026-04-28 11:09:51.336 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.4333
2026-04-28 11:09:51.336 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'C' via keyboard press
2026-04-28 11:09:51.841 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'C' verified at (9,13)
2026-04-28 11:09:52.258 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,14) | src=(1198.9,832.9) dst=(1194.7,516.3)
2026-04-28 11:09:53.076 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105349 bytes (attempt 1)
2026-04-28 11:09:54.854 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110034 bytes (attempt 1)
2026-04-28 11:09:55.064 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.9181
2026-04-28 11:09:55.065 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,14)
2026-04-28 11:09:55.717 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,15) | src=(1036.0,830.7) dst=(1246.9,512.8)
2026-04-28 11:09:56.549 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106063 bytes (attempt 1)
2026-04-28 11:09:58.385 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110529 bytes (attempt 1)
2026-04-28 11:09:58.588 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4509
2026-04-28 11:09:58.590 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,15)
2026-04-28 11:09:59.207 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (9,16) | src=(1309.5,832.9) dst=(1297.3,510.7)
2026-04-28 11:10:00.160 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107586 bytes (attempt 1)
2026-04-28 11:10:02.456 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110664 bytes (attempt 1)
2026-04-28 11:10:02.594 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5234
2026-04-28 11:10:02.595 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,16)
2026-04-28 11:10:04.332 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105861 bytes (attempt 1)
2026-04-28 11:10:04.342 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt3_LACUNA.png
2026-04-28 11:10:05.609 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:10:05.610 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1146.6, 789.9)
2026-04-28 11:10:07.201 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112518 bytes (attempt 1)
2026-04-28 11:10:07.323 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:10:07.324 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:10:07.324 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1146.2, 787.6)
2026-04-28 11:10:08.725 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109465 bytes (attempt 1)
2026-04-28 11:10:08.854 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:10:10.780 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108905 bytes (attempt 1)
2026-04-28 11:10:11.045 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:10:11.046 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LACUNA' rejected (attempt 3/5) — recalling tiles
2026-04-28 11:10:11.049 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'lacuna' (total: 89)
2026-04-28 11:10:11.920 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109041 bytes (attempt 1)
2026-04-28 11:10:11.921 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.9, 785.7) (pass 1/10)
2026-04-28 11:10:13.856 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104485 bytes (attempt 1)
2026-04-28 11:10:13.995 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.3, 790.9) (pass 2/10)
2026-04-28 11:10:15.985 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110020 bytes (attempt 1)
2026-04-28 11:10:16.128 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.2, 786.2) (pass 3/10)
2026-04-28 11:10:18.482 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110947 bytes (attempt 1)
2026-04-28 11:10:18.619 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.9, 785.0) (pass 4/10)
2026-04-28 11:10:20.426 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104413 bytes (attempt 1)
2026-04-28 11:10:20.538 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.5, 789.7) (pass 5/10)
2026-04-28 11:10:22.490 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109996 bytes (attempt 1)
2026-04-28 11:10:22.620 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.4, 787.2) (pass 6/10)
2026-04-28 11:10:24.361 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104591 bytes (attempt 1)
2026-04-28 11:10:24.714 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.2, 790.4) (pass 7/10)
2026-04-28 11:10:26.562 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109035 bytes (attempt 1)
2026-04-28 11:10:26.694 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.4, 788.9) (pass 8/10)
2026-04-28 11:10:28.679 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111524 bytes (attempt 1)
2026-04-28 11:10:28.808 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.2, 788.1) (pass 9/10)
2026-04-28 11:10:30.817 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106101 bytes (attempt 1)
2026-04-28 11:10:30.939 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.3, 785.9) (pass 10/10)
2026-04-28 11:10:32.830 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110895 bytes (attempt 1)
2026-04-28 11:10:32.957 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:10:33.815 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110419 bytes (attempt 1)
2026-04-28 11:10:33.818 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt3.png
2026-04-28 11:10:33.819 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 4/5: 'LAGUNE' (score=24)
2026-04-28 11:10:33.939 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:10:33.940 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,11) | src=(1092.9,831.0) dst=(1044.5,513.3)
2026-04-28 11:10:35.113 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110305 bytes (attempt 1)
2026-04-28 11:10:37.187 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110682 bytes (attempt 1)
2026-04-28 11:10:37.394 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8794
2026-04-28 11:10:37.395 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,11)
2026-04-28 11:10:37.936 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(978.7,828.7) dst=(1095.2,512.5)
2026-04-28 11:10:38.805 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105982 bytes (attempt 1)
2026-04-28 11:10:40.492 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110911 bytes (attempt 1)
2026-04-28 11:10:40.617 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6131
2026-04-28 11:10:40.618 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:10:41.211 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'G' (slot 3) -> board (9,13) | src=(1147.9,830.0) dst=(1148.5,513.8)
2026-04-28 11:10:42.083 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107482 bytes (attempt 1)
2026-04-28 11:10:43.783 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105670 bytes (attempt 1)
2026-04-28 11:10:43.927 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4453
2026-04-28 11:10:45.313 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110320 bytes (attempt 1)
2026-04-28 11:10:46.532 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110053 bytes (attempt 1)
2026-04-28 11:10:46.643 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.4557
2026-04-28 11:10:46.644 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'G' via keyboard press
2026-04-28 11:10:47.149 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'G' verified at (9,13)
2026-04-28 11:10:47.833 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,14) | src=(1198.5,832.8) dst=(1197.0,511.1)
2026-04-28 11:10:48.684 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104731 bytes (attempt 1)
2026-04-28 11:10:50.401 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111974 bytes (attempt 1)
2026-04-28 11:10:50.514 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5244
2026-04-28 11:10:50.515 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,14)
2026-04-28 11:10:51.030 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,15) | src=(1035.6,828.3) dst=(1249.7,514.9)
2026-04-28 11:10:51.894 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111091 bytes (attempt 1)
2026-04-28 11:10:53.715 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103122 bytes (attempt 1)
2026-04-28 11:10:53.909 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.9448
2026-04-28 11:10:53.909 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,15)
2026-04-28 11:10:54.421 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 5) -> board (9,16) | src=(1253.7,829.1) dst=(1299.1,515.0)
2026-04-28 11:10:55.683 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105251 bytes (attempt 1)
2026-04-28 11:10:57.493 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104659 bytes (attempt 1)
2026-04-28 11:10:57.608 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3889
2026-04-28 11:10:57.609 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (9,16)
2026-04-28 11:10:58.412 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109461 bytes (attempt 1)
2026-04-28 11:10:58.417 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt4_LAGUNE.png
2026-04-28 11:10:59.156 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:10:59.157 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1149.1, 789.3)
2026-04-28 11:11:00.675 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111119 bytes (attempt 1)
2026-04-28 11:11:00.792 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:11:00.793 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:11:00.793 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1147.8, 786.6)
2026-04-28 11:11:02.438 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108399 bytes (attempt 1)
2026-04-28 11:11:02.560 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:11:04.347 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110975 bytes (attempt 1)
2026-04-28 11:11:04.480 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:11:04.481 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LAGUNE' rejected (attempt 4/5) — recalling tiles
2026-04-28 11:11:04.484 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'lagune' (total: 90)
2026-04-28 11:11:05.332 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110613 bytes (attempt 1)
2026-04-28 11:11:05.333 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.7, 785.2) (pass 1/10)
2026-04-28 11:11:07.300 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104376 bytes (attempt 1)
2026-04-28 11:11:07.420 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.8, 789.0) (pass 2/10)
2026-04-28 11:11:09.280 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109607 bytes (attempt 1)
2026-04-28 11:11:09.419 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.1, 788.6) (pass 3/10)
2026-04-28 11:11:11.276 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104468 bytes (attempt 1)
2026-04-28 11:11:11.405 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.2, 788.7) (pass 4/10)
2026-04-28 11:11:13.263 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108350 bytes (attempt 1)
2026-04-28 11:11:13.381 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.8, 786.7) (pass 5/10)
2026-04-28 11:11:15.686 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109043 bytes (attempt 1)
2026-04-28 11:11:15.843 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.8, 790.4) (pass 6/10)
2026-04-28 11:11:17.693 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104473 bytes (attempt 1)
2026-04-28 11:11:17.817 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.0, 786.7) (pass 7/10)
2026-04-28 11:11:19.909 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103507 bytes (attempt 1)
2026-04-28 11:11:20.032 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.6, 788.4) (pass 8/10)
2026-04-28 11:11:22.122 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108840 bytes (attempt 1)
2026-04-28 11:11:22.290 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.4, 788.5) (pass 9/10)
2026-04-28 11:11:24.367 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109834 bytes (attempt 1)
2026-04-28 11:11:24.516 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.6, 788.5) (pass 10/10)
2026-04-28 11:11:26.452 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105028 bytes (attempt 1)
2026-04-28 11:11:26.586 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:11:28.093 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103546 bytes (attempt 1)
2026-04-28 11:11:28.096 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt4.png
2026-04-28 11:11:28.097 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 5/5: 'LAGUNA' (score=24)
2026-04-28 11:11:28.274 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:11:28.275 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,11) | src=(1088.7,832.5) dst=(1045.2,510.6)
2026-04-28 11:11:29.052 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104865 bytes (attempt 1)
2026-04-28 11:11:30.844 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109982 bytes (attempt 1)
2026-04-28 11:11:30.961 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.7638
2026-04-28 11:11:30.961 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,11)
2026-04-28 11:11:31.387 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(980.5,829.4) dst=(1097.1,516.3)
2026-04-28 11:11:32.242 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111587 bytes (attempt 1)
2026-04-28 11:11:33.975 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109747 bytes (attempt 1)
2026-04-28 11:11:34.088 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5882
2026-04-28 11:11:34.088 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:11:34.722 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'G' (slot 3) -> board (9,13) | src=(1145.6,833.1) dst=(1143.5,512.4)
2026-04-28 11:11:35.594 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104997 bytes (attempt 1)
2026-04-28 11:11:37.249 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110559 bytes (attempt 1)
2026-04-28 11:11:37.388 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6963
2026-04-28 11:11:39.258 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106975 bytes (attempt 1)
2026-04-28 11:11:40.956 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105670 bytes (attempt 1)
2026-04-28 11:11:41.084 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.4440
2026-04-28 11:11:41.085 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'G' via keyboard press
2026-04-28 11:11:41.599 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'G' verified at (9,13)
2026-04-28 11:11:42.084 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,14) | src=(1202.5,829.9) dst=(1195.2,515.3)
2026-04-28 11:11:43.017 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109073 bytes (attempt 1)
2026-04-28 11:11:44.720 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104703 bytes (attempt 1)
2026-04-28 11:11:44.878 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3513
2026-04-28 11:11:44.878 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,14)
2026-04-28 11:11:45.467 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,15) | src=(1033.0,832.2) dst=(1247.5,512.9)
2026-04-28 11:11:46.367 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110211 bytes (attempt 1)
2026-04-28 11:11:48.493 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106359 bytes (attempt 1)
2026-04-28 11:11:48.648 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3601
2026-04-28 11:11:48.649 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,15)
2026-04-28 11:11:49.118 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (9,16) | src=(1309.3,833.7) dst=(1298.8,512.4)
2026-04-28 11:11:49.933 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105806 bytes (attempt 1)
2026-04-28 11:11:51.657 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109460 bytes (attempt 1)
2026-04-28 11:11:51.808 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5906
2026-04-28 11:11:51.809 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,16)
2026-04-28 11:11:52.675 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110417 bytes (attempt 1)
2026-04-28 11:11:52.679 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt5_LAGUNA.png
2026-04-28 11:11:53.449 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:11:53.450 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1145.6, 785.7)
2026-04-28 11:11:54.911 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103706 bytes (attempt 1)
2026-04-28 11:11:55.039 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:11:55.039 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:11:55.040 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1149.0, 786.4)
2026-04-28 11:11:56.571 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105325 bytes (attempt 1)
2026-04-28 11:11:56.694 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:11:58.166 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111340 bytes (attempt 1)
2026-04-28 11:11:58.289 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:11:58.290 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LAGUNA' rejected (attempt 5/5) — recalling tiles
2026-04-28 11:11:58.293 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'laguna' (total: 91)
2026-04-28 11:11:59.583 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111600 bytes (attempt 1)
2026-04-28 11:11:59.583 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.8, 789.2) (pass 1/10)
2026-04-28 11:12:01.875 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103174 bytes (attempt 1)
2026-04-28 11:12:02.063 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.8, 789.8) (pass 2/10)
2026-04-28 11:12:04.096 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106395 bytes (attempt 1)
2026-04-28 11:12:04.271 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.2, 787.7) (pass 3/10)
2026-04-28 11:12:06.271 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110259 bytes (attempt 1)
2026-04-28 11:12:06.447 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.8, 790.5) (pass 4/10)
2026-04-28 11:12:09.818 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110408 bytes (attempt 1)
2026-04-28 11:12:10.147 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.2, 790.0) (pass 5/10)
2026-04-28 11:12:12.210 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106020 bytes (attempt 1)
2026-04-28 11:12:12.401 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.2, 789.5) (pass 6/10)
2026-04-28 11:12:14.386 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111694 bytes (attempt 1)
2026-04-28 11:12:14.821 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.6, 790.8) (pass 7/10)
2026-04-28 11:12:19.076 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109146 bytes (attempt 1)
2026-04-28 11:12:19.345 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.6, 787.4) (pass 8/10)
2026-04-28 11:12:21.172 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111699 bytes (attempt 1)
2026-04-28 11:12:21.345 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.8, 790.2) (pass 9/10)
2026-04-28 11:12:23.633 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110405 bytes (attempt 1)
2026-04-28 11:12:23.827 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.2, 790.6) (pass 10/10)
2026-04-28 11:12:25.999 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111032 bytes (attempt 1)
2026-04-28 11:12:26.164 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:12:27.050 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109985 bytes (attempt 1)
2026-04-28 11:12:27.053 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt5.png
2026-04-28 11:12:27.054 | WARNING | src.browser.tile_placer:place_move:1130 | All 5 word attempt(s) failed — returning to caller for re-vision
2026-04-28 11:12:27.055 | WARNING | __main__:_run:193 | No move accepted (candidates=5) — re-vision + swap fallback
2026-04-28 11:12:30.601 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104790 bytes (attempt 1)
2026-04-28 11:12:30.602 | INFO    | src.vision:extract_board_state:125 | Vision pipeline start — mode=wild
2026-04-28 11:12:30.647 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,51) 1366×625 from 1545×731 canvas
2026-04-28 11:12:30.925 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-04-28 11:12:31.036 | INFO    | src.vision:extract_board_state:131 | Preprocessing complete — 314526 bytes
2026-04-28 11:12:31.037 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=False
2026-04-28 11:12:34.162 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=3.12s  input_tokens=2905  output_tokens=78
2026-04-28 11:12:34.163 | INFO    | src.vision:extract_board_state:137 | Extraction complete (first attempt)
2026-04-28 11:12:34.164 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,13)=[DW]
2026-04-28 11:12:34.164 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['A', 'N', 'L', '?', 'U', 'E', 'A']
2026-04-28 11:12:34.165 | INFO    | src.vision:extract_board_state:155 | Validation result — 0 error(s)
2026-04-28 11:12:34.166 | INFO    | src.vision:extract_board_state:328 | Vision pipeline complete — 3.56s  tiles=0  rack_size=7
2026-04-28 11:12:34.892 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 220 blacklisted candidate(s)
2026-04-28 11:12:34.915 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 1/5: 'NEURAL' (score=24)
2026-04-28 11:12:35.033 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:12:35.034 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,10) | src=(1033.0,829.8) dst=(997.0,511.1)
2026-04-28 11:12:35.863 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105214 bytes (attempt 1)
2026-04-28 11:12:37.640 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109286 bytes (attempt 1)
2026-04-28 11:12:37.790 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5743
2026-04-28 11:12:37.791 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,10)
2026-04-28 11:12:38.494 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 5) -> board (9,11) | src=(1257.7,829.6) dst=(1042.8,514.8)
2026-04-28 11:12:39.368 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104694 bytes (attempt 1)
2026-04-28 11:12:41.125 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110439 bytes (attempt 1)
2026-04-28 11:12:41.325 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.7575
2026-04-28 11:12:41.326 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (9,11)
2026-04-28 11:12:41.866 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,12) | src=(1202.2,828.7) dst=(1092.7,516.1)
2026-04-28 11:12:42.695 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104948 bytes (attempt 1)
2026-04-28 11:12:44.450 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111748 bytes (attempt 1)
2026-04-28 11:12:44.591 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5218
2026-04-28 11:12:44.592 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,12)
2026-04-28 11:12:45.158 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'R' (slot 3) -> board (9,13) | src=(1147.0,832.9) dst=(1143.3,515.3)
2026-04-28 11:12:46.039 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109669 bytes (attempt 1)
2026-04-28 11:12:47.802 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105831 bytes (attempt 1)
2026-04-28 11:12:47.950 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3542
2026-04-28 11:12:49.319 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109858 bytes (attempt 1)
2026-04-28 11:12:50.643 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110154 bytes (attempt 1)
2026-04-28 11:12:50.794 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.4311
2026-04-28 11:12:50.795 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'R' via keyboard press
2026-04-28 11:12:51.310 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'R' verified at (9,13)
2026-04-28 11:12:51.976 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,14) | src=(977.5,829.0) dst=(1195.0,516.0)
2026-04-28 11:12:52.922 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105891 bytes (attempt 1)
2026-04-28 11:12:54.700 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112326 bytes (attempt 1)
2026-04-28 11:12:54.848 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4285
2026-04-28 11:12:54.849 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,14)
2026-04-28 11:12:55.539 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,15) | src=(1092.5,831.7) dst=(1250.1,510.4)
2026-04-28 11:12:56.647 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108152 bytes (attempt 1)
2026-04-28 11:12:58.467 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111588 bytes (attempt 1)
2026-04-28 11:12:58.629 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5271
2026-04-28 11:12:58.630 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,15)
2026-04-28 11:12:59.562 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105365 bytes (attempt 1)
2026-04-28 11:12:59.566 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt1_NEURAL.png
2026-04-28 11:13:00.366 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:13:00.367 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1149.3, 789.8)
2026-04-28 11:13:02.002 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106592 bytes (attempt 1)
2026-04-28 11:13:02.241 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:13:02.242 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:13:02.242 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1148.9, 790.0)
2026-04-28 11:13:03.832 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110921 bytes (attempt 1)
2026-04-28 11:13:03.954 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:13:08.852 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111796 bytes (attempt 1)
2026-04-28 11:13:08.973 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:13:08.976 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'NEURAL' rejected (attempt 1/5) — recalling tiles
2026-04-28 11:13:08.981 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'neural' (total: 92)
2026-04-28 11:13:10.122 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105790 bytes (attempt 1)
2026-04-28 11:13:10.122 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.6, 787.3) (pass 1/10)
2026-04-28 11:13:12.239 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107727 bytes (attempt 1)
2026-04-28 11:13:12.402 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.1, 785.3) (pass 2/10)
2026-04-28 11:13:14.476 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110214 bytes (attempt 1)
2026-04-28 11:13:14.619 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.8, 789.5) (pass 3/10)
2026-04-28 11:13:17.180 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111800 bytes (attempt 1)
2026-04-28 11:13:18.327 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.2, 785.8) (pass 4/10)
2026-04-28 11:13:21.207 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110219 bytes (attempt 1)
2026-04-28 11:13:21.392 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.5, 788.5) (pass 5/10)
2026-04-28 11:13:23.412 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105518 bytes (attempt 1)
2026-04-28 11:13:23.603 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.4, 789.1) (pass 6/10)
2026-04-28 11:13:26.364 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 112009 bytes (attempt 1)
2026-04-28 11:13:26.526 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.4, 785.1) (pass 7/10)
2026-04-28 11:13:28.566 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104120 bytes (attempt 1)
2026-04-28 11:13:28.723 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.7, 790.9) (pass 8/10)
2026-04-28 11:13:30.675 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110155 bytes (attempt 1)
2026-04-28 11:13:30.852 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.5, 787.8) (pass 9/10)
2026-04-28 11:13:32.765 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111820 bytes (attempt 1)
2026-04-28 11:13:32.896 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.9, 788.3) (pass 10/10)
2026-04-28 11:13:34.843 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105839 bytes (attempt 1)
2026-04-28 11:13:34.970 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:13:35.898 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109393 bytes (attempt 1)
2026-04-28 11:13:35.902 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-04-28 11:13:35.903 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 2/5: 'LAGENA' (score=24)
2026-04-28 11:13:36.073 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:13:36.074 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,11) | src=(1088.0,828.1) dst=(1044.5,514.0)
2026-04-28 11:13:36.885 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110309 bytes (attempt 1)
2026-04-28 11:13:38.910 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104217 bytes (attempt 1)
2026-04-28 11:13:39.024 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.9110
2026-04-28 11:13:39.025 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,11)
2026-04-28 11:13:39.493 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(979.7,830.5) dst=(1097.6,514.3)
2026-04-28 11:13:40.618 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110793 bytes (attempt 1)
2026-04-28 11:13:43.114 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104237 bytes (attempt 1)
2026-04-28 11:13:43.395 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.9748
2026-04-28 11:13:43.396 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:13:43.875 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'G' (slot 3) -> board (9,13) | src=(1144.0,832.2) dst=(1146.7,515.2)
2026-04-28 11:13:44.811 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110922 bytes (attempt 1)
2026-04-28 11:13:46.622 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105982 bytes (attempt 1)
2026-04-28 11:13:46.769 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.2212
2026-04-28 11:13:48.153 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105553 bytes (attempt 1)
2026-04-28 11:13:49.377 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105298 bytes (attempt 1)
2026-04-28 11:13:49.534 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.2550
2026-04-28 11:13:49.535 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'G' via keyboard press
2026-04-28 11:13:50.037 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'G' verified at (9,13)
2026-04-28 11:13:50.707 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 5) -> board (9,14) | src=(1253.8,831.9) dst=(1196.3,514.9)
2026-04-28 11:13:51.742 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108699 bytes (attempt 1)
2026-04-28 11:13:53.414 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103576 bytes (attempt 1)
2026-04-28 11:13:53.534 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.9888
2026-04-28 11:13:53.535 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (9,14)
2026-04-28 11:13:53.979 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,15) | src=(1033.2,829.4) dst=(1244.4,511.1)
2026-04-28 11:13:54.765 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104129 bytes (attempt 1)
2026-04-28 11:13:56.670 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110335 bytes (attempt 1)
2026-04-28 11:13:57.040 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8681
2026-04-28 11:13:57.041 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,15)
2026-04-28 11:13:57.556 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (9,16) | src=(1312.1,829.8) dst=(1296.7,513.5)
2026-04-28 11:13:58.492 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103935 bytes (attempt 1)
2026-04-28 11:14:00.545 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110530 bytes (attempt 1)
2026-04-28 11:14:00.678 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.9020
2026-04-28 11:14:00.679 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,16)
2026-04-28 11:14:01.546 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111122 bytes (attempt 1)
2026-04-28 11:14:01.550 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt2_LAGENA.png
2026-04-28 11:14:02.373 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:14:02.373 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1144.5, 790.6)
2026-04-28 11:14:03.838 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104288 bytes (attempt 1)
2026-04-28 11:14:03.964 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 11:14:03.964 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 11:14:03.965 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1148.1, 789.3)
2026-04-28 11:14:05.474 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111169 bytes (attempt 1)
2026-04-28 11:14:05.583 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 11:14:07.085 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108473 bytes (attempt 1)
2026-04-28 11:14:07.201 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 11:14:07.202 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LAGENA' rejected (attempt 2/5) — recalling tiles
2026-04-28 11:14:07.205 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'lagena' (total: 93)
2026-04-28 11:14:08.098 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110338 bytes (attempt 1)
2026-04-28 11:14:08.100 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.1, 789.1) (pass 1/10)
2026-04-28 11:14:09.963 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105719 bytes (attempt 1)
2026-04-28 11:14:10.226 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.6, 788.3) (pass 2/10)
2026-04-28 11:14:12.089 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110332 bytes (attempt 1)
2026-04-28 11:14:12.219 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.0, 790.1) (pass 3/10)
2026-04-28 11:14:14.411 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105630 bytes (attempt 1)
2026-04-28 11:14:14.589 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.9, 790.1) (pass 4/10)
2026-04-28 11:14:16.644 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105357 bytes (attempt 1)
2026-04-28 11:14:16.805 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.4, 785.9) (pass 5/10)
2026-04-28 11:14:18.827 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 106733 bytes (attempt 1)
2026-04-28 11:14:19.019 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.9, 790.3) (pass 6/10)
2026-04-28 11:14:21.159 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109025 bytes (attempt 1)
2026-04-28 11:14:21.327 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.6, 789.6) (pass 7/10)
2026-04-28 11:14:23.316 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 111393 bytes (attempt 1)
2026-04-28 11:14:23.451 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.7, 785.9) (pass 8/10)
2026-04-28 11:14:25.252 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105280 bytes (attempt 1)
2026-04-28 11:14:25.407 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.6, 788.7) (pass 9/10)
2026-04-28 11:14:27.632 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105803 bytes (attempt 1)
2026-04-28 11:14:27.755 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.2, 788.1) (pass 10/10)
2026-04-28 11:14:30.152 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110656 bytes (attempt 1)
2026-04-28 11:14:30.427 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 11:14:31.280 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108779 bytes (attempt 1)
2026-04-28 11:14:31.289 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt2.png
2026-04-28 11:14:31.290 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 3/5: 'LAUNCE' (score=24)
2026-04-28 11:14:31.482 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:14:31.482 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 2) -> board (9,11) | src=(1093.7,831.3) dst=(1044.4,515.4)
2026-04-28 11:14:32.383 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110084 bytes (attempt 1)
2026-04-28 11:14:34.100 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105779 bytes (attempt 1)
2026-04-28 11:14:34.255 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.4780
2026-04-28 11:14:34.256 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (9,11)
2026-04-28 11:14:34.726 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 0) -> board (9,12) | src=(977.2,831.0) dst=(1095.5,511.3)
2026-04-28 11:14:35.780 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 105630 bytes (attempt 1)
2026-04-28 11:14:37.552 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109668 bytes (attempt 1)
2026-04-28 11:14:37.730 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.5357
2026-04-28 11:14:37.731 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (9,12)
2026-04-28 11:14:38.295 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'U' (slot 4) -> board (9,13) | src=(1200.5,830.4) dst=(1144.7,511.1)
2026-04-28 11:14:39.294 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104779 bytes (attempt 1)
2026-04-28 11:14:41.164 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108715 bytes (attempt 1)
2026-04-28 11:14:41.314 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6312
2026-04-28 11:14:41.315 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'U' verified at (9,13)
2026-04-28 11:14:41.937 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 1) -> board (9,14) | src=(1037.5,829.0) dst=(1198.1,511.0)
2026-04-28 11:14:43.156 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 104079 bytes (attempt 1)
2026-04-28 11:14:44.870 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101687 bytes (attempt 1)
2026-04-28 11:14:44.993 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8597
2026-04-28 11:14:44.994 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (9,14)
2026-04-28 11:14:45.506 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'C' (slot 3) -> board (9,15) | src=(1145.7,831.6) dst=(1245.7,515.1)
2026-04-28 11:14:46.312 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 101818 bytes (attempt 1)
2026-04-28 11:14:48.031 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 103816 bytes (attempt 1)
2026-04-28 11:14:48.194 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8334
2026-04-28 11:18:22.850 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:38 | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 3 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank', 'https://879863686565621790.discordsays.com/?instance_id=i-1498713407573197022-gc-1486201751353819208-1486201752477761590&location_id=gc-1486201751353819208-1486201752477761590&launch_id=1498713407573197022&referrer_id=undefined&custom_id=undefined&discord_proxy_ticket=faux-proxy-ticket&guild_id=1486201751353819208&channel_id=1486201752477761590&frame_id=3b267e7b-874e-4da1-add9-3f1eb1eda617&platform=desktop']
2026-04-28 11:18:23.636 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:46 | Viewport screenshot saved -> debug\iframe_missing.png
2026-04-28 11:18:23.637 | WARNING | __main__:_run:211 | Re-vision retry failed: Locator.screenshot: Timeout 29857ms exceeded.
Call log:
  - taking element screenshot
  - waiting for fonts to load...

2026-04-28 11:18:23.638 | INFO    | __main__:_run:217 | Turn 3: no move accepted (swap/skip)
2026-04-28 11:18:23.796 | INFO    | src.browser.capture:capture_canvas:113 | Activity iframe verified visible
2026-04-28 11:24:55.691 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 14691 bytes (attempt 1)
2026-04-28 11:24:55.775 | INFO    | src.browser.turn_detector:poll_turn:633 | Turn state: game_over before gameplay detected — treating as loading screen, waiting
2026-04-28 11:25:01.585 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 14691 bytes (attempt 1)
2026-04-28 11:25:06.985 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 14691 bytes (attempt 1)
2026-04-28 11:25:12.033 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 14691 bytes (attempt 1)
2026-04-28 11:25:17.766 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 102815 bytes (attempt 1)
2026-04-28 11:25:17.896 | INFO    | src.browser.turn_detector:poll_turn:647 | Turn state changed: game_over -> my_turn
2026-04-28 11:25:18.048 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:25:19.104 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:38 | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-04-28 11:25:19.338 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:46 | Viewport screenshot saved -> debug\iframe_missing.png
2026-04-28 11:25:19.339 | WARNING | src.browser.tile_placer:clear_stale_placements:937 | clear_stale_placements: dialog probe failed (Locator.screenshot: Element is not attached to the DOM
Call log:
  - taking element screenshot
  - waiting for fonts to load...
  - fonts loaded
  - attempting scroll into view action
    - waiting for element to be stable
) — continuing to recall
2026-04-28 11:25:49.396 | WARNING | src.browser.capture:capture_canvas:115 | Activity iframe not visible after 30s
2026-04-28 11:26:19.740 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:38 | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-04-28 11:26:20.060 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:46 | Viewport screenshot saved -> debug\iframe_missing.png
2026-04-28 11:26:20.060 | WARNING | src.browser.tile_placer:clear_stale_placements:949 | clear_stale_placements: capture failed (Locator.screenshot: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")
) — aborting
2026-04-28 11:26:50.079 | WARNING | src.browser.capture:capture_canvas:115 | Activity iframe not visible after 30s
2026-04-28 11:27:23.115 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:38 | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-04-28 11:27:23.426 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:46 | Viewport screenshot saved -> debug\iframe_missing.png
2026-04-28 11:27:23.427 | WARNING | __main__:_run:161 | Vision attempt 1 failed: Locator.screenshot: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

2026-04-28 11:27:53.447 | WARNING | src.browser.capture:capture_canvas:115 | Activity iframe not visible after 30s
2026-04-28 11:28:26.466 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:38 | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-04-28 11:28:26.735 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:46 | Viewport screenshot saved -> debug\iframe_missing.png
2026-04-28 11:28:26.736 | WARNING | __main__:_run:161 | Vision attempt 2 failed: Locator.screenshot: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

2026-04-28 11:28:26.736 | ERROR   | __main__:_run:163 | Vision failed twice — skipping turn
2026-04-28 11:28:56.754 | WARNING | src.browser.capture:capture_canvas:115 | Activity iframe not visible after 30s
2026-04-28 11:29:29.785 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:38 | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-04-28 11:29:30.037 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:46 | Viewport screenshot saved -> debug\iframe_missing.png
2026-04-28 11:29:30.038 | WARNING | src.browser.turn_detector:poll_turn:615 | capture_canvas failed (1/5, retry in 1.0s): Locator.screenshot: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

2026-04-28 11:30:01.052 | WARNING | src.browser.capture:capture_canvas:115 | Activity iframe not visible after 30s
2026-04-28 11:30:34.084 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:38 | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-04-28 11:30:34.400 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:46 | Viewport screenshot saved -> debug\iframe_missing.png
2026-04-28 11:30:34.401 | WARNING | src.browser.turn_detector:poll_turn:615 | capture_canvas failed (2/5, retry in 2.0s): Locator.screenshot: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

2026-04-28 11:31:06.422 | WARNING | src.browser.capture:capture_canvas:115 | Activity iframe not visible after 30s
```

## Subprocess stderr (tail)
```
[32m11:14:10[0m | [1mINFO   [0m | Clicking recall button at (1285.6, 788.3) (pass 2/10)
[32m11:14:12[0m | [1mINFO   [0m | Clicking recall button at (1284.0, 790.1) (pass 3/10)
[32m11:14:14[0m | [1mINFO   [0m | Clicking recall button at (1287.9, 790.1) (pass 4/10)
[32m11:14:16[0m | [1mINFO   [0m | Clicking recall button at (1287.4, 785.9) (pass 5/10)
[32m11:14:19[0m | [1mINFO   [0m | Clicking recall button at (1286.9, 790.3) (pass 6/10)
[32m11:14:21[0m | [1mINFO   [0m | Clicking recall button at (1287.6, 789.6) (pass 7/10)
[32m11:14:23[0m | [1mINFO   [0m | Clicking recall button at (1287.7, 785.9) (pass 8/10)
[32m11:14:25[0m | [1mINFO   [0m | Clicking recall button at (1288.6, 788.7) (pass 9/10)
[32m11:14:27[0m | [1mINFO   [0m | Clicking recall button at (1283.2, 788.1) (pass 10/10)
[32m11:14:30[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m11:14:31[0m | [1mINFO   [0m | Word attempt 3/5: 'LAUNCE' (score=24)
[32m11:14:31[0m | [1mINFO   [0m | Placing tile 'L' (slot 2) -> board (9,11) | src=(1093.7,831.3) dst=(1044.4,515.4)
[32m11:14:34[0m | [1mINFO   [0m | Tile 'L' verified at (9,11)
[32m11:14:34[0m | [1mINFO   [0m | Placing tile 'A' (slot 0) -> board (9,12) | src=(977.2,831.0) dst=(1095.5,511.3)
[32m11:14:37[0m | [1mINFO   [0m | Tile 'A' verified at (9,12)
[32m11:14:38[0m | [1mINFO   [0m | Placing tile 'U' (slot 4) -> board (9,13) | src=(1200.5,830.4) dst=(1144.7,511.1)
[32m11:14:41[0m | [1mINFO   [0m | Tile 'U' verified at (9,13)
[32m11:14:41[0m | [1mINFO   [0m | Placing tile 'N' (slot 1) -> board (9,14) | src=(1037.5,829.0) dst=(1198.1,511.0)
[32m11:14:44[0m | [1mINFO   [0m | Tile 'N' verified at (9,14)
[32m11:14:45[0m | [1mINFO   [0m | Placing tile 'C' (slot 3) -> board (9,15) | src=(1145.7,831.6) dst=(1245.7,515.1)
[32m11:18:22[0m | [33m[1mWARNING[0m | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 3 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank', 'https://879863686565621790.discordsays.com/?instance_id=i-1498713407573197022-gc-1486201751353819208-1486201752477761590&location_id=gc-1486201751353819208-1486201752477761590&launch_id=1498713407573197022&referrer_id=undefined&custom_id=undefined&discord_proxy_ticket=faux-proxy-ticket&guild_id=1486201751353819208&channel_id=1486201752477761590&frame_id=3b267e7b-874e-4da1-add9-3f1eb1eda617&platform=desktop']
[32m11:18:23[0m | [33m[1mWARNING[0m | Viewport screenshot saved -> debug\iframe_missing.png
[32m11:18:23[0m | [33m[1mWARNING[0m | Re-vision retry failed: Locator.screenshot: Timeout 29857ms exceeded.
Call log:
  - taking element screenshot
  - waiting for fonts to load...

[32m11:18:23[0m | [1mINFO   [0m | Turn 3: no move accepted (swap/skip)
[32m11:18:23[0m | [1mINFO   [0m | Activity iframe verified visible
[32m11:24:55[0m | [1mINFO   [0m | Turn state: game_over before gameplay detected — treating as loading screen, waiting
[32m11:25:17[0m | [1mINFO   [0m | Turn state changed: game_over -> my_turn
[32m11:25:19[0m | [33m[1mWARNING[0m | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
[32m11:25:19[0m | [33m[1mWARNING[0m | Viewport screenshot saved -> debug\iframe_missing.png
[32m11:25:19[0m | [33m[1mWARNING[0m | clear_stale_placements: dialog probe failed (Locator.screenshot: Element is not attached to the DOM
Call log:
  - taking element screenshot
  - waiting for fonts to load...
  - fonts loaded
  - attempting scroll into view action
    - waiting for element to be stable
) — continuing to recall
[32m11:25:49[0m | [33m[1mWARNING[0m | Activity iframe not visible after 30s
[32m11:26:19[0m | [33m[1mWARNING[0m | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
[32m11:26:20[0m | [33m[1mWARNING[0m | Viewport screenshot saved -> debug\iframe_missing.png
[32m11:26:20[0m | [33m[1mWARNING[0m | clear_stale_placements: capture failed (Locator.screenshot: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")
) — aborting
[32m11:26:50[0m | [33m[1mWARNING[0m | Activity iframe not visible after 30s
[32m11:27:23[0m | [33m[1mWARNING[0m | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
[32m11:27:23[0m | [33m[1mWARNING[0m | Viewport screenshot saved -> debug\iframe_missing.png
[32m11:27:23[0m | [33m[1mWARNING[0m | Vision attempt 1 failed: Locator.screenshot: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

[32m11:27:53[0m | [33m[1mWARNING[0m | Activity iframe not visible after 30s
[32m11:28:26[0m | [33m[1mWARNING[0m | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
[32m11:28:26[0m | [33m[1mWARNING[0m | Viewport screenshot saved -> debug\iframe_missing.png
[32m11:28:26[0m | [33m[1mWARNING[0m | Vision attempt 2 failed: Locator.screenshot: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

[32m11:28:26[0m | [31m[1mERROR  [0m | Vision failed twice — skipping turn
[32m11:28:56[0m | [33m[1mWARNING[0m | Activity iframe not visible after 30s
[32m11:29:29[0m | [33m[1mWARNING[0m | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
[32m11:29:30[0m | [33m[1mWARNING[0m | Viewport screenshot saved -> debug\iframe_missing.png
[32m11:29:30[0m | [33m[1mWARNING[0m | capture_canvas failed (1/5, retry in 1.0s): Locator.screenshot: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

[32m11:30:01[0m | [33m[1mWARNING[0m | Activity iframe not visible after 30s
[32m11:30:34[0m | [33m[1mWARNING[0m | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
[32m11:30:34[0m | [33m[1mWARNING[0m | Viewport screenshot saved -> debug\iframe_missing.png
[32m11:30:34[0m | [33m[1mWARNING[0m | capture_canvas failed (2/5, retry in 2.0s): Locator.screenshot: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

[32m11:31:06[0m | [33m[1mWARNING[0m | Activity iframe not visible after 30s

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
?? debug/tile_placer/pre_play_attempt1_DAMNS.png
?? debug/tile_placer/pre_play_attempt1_DOG.png
?? debug/tile_placer/pre_play_attempt1_EL.png
?? debug/tile_placer/pre_play_attempt1_FAKE.png
?? debug/tile_placer/pre_play_attempt1_FIBERS.png
?? debug/tile_placer/pre_play_attempt1_FIZ.png
?? debug/tile_placer/pre_play_attempt1_FORKY.png
?? debug/tile_placer/pre_play_attempt1_GINZO.png
?? debug/tile_placer/pre_play_attempt1_GOOD.png
?? debug/tile_placer/pre_play_attempt1_GOOGOL.png
?? debug/tile_placer/pre_play_attempt1_GOOLD.png
?? debug/tile_placer/pre_play_attempt1_HINGED.png
?? debug/tile_placer/pre_play_attempt1_ID.png
?? debug/tile_placer/pre_play_attempt1_JIAO.png
?? debug/tile_placer/pre_play_attempt1_JOEY.png
?? debug/tile_placer/pre_play_attempt1_JOINT.png
?? debug/tile_placer/pre_play_attempt1_JOINTS.png
?? debug/tile_placer/pre_play_attempt1_LEG.png
?? debug/tile_placer/pre_play_attempt1_LOGO.png
?? debug/tile_placer/pre_play_attempt1_MANUAL.png
?? debug/tile_placer/pre_play_attempt1_NEURAL.png
?? debug/tile_placer/pre_play_attempt1_OI.png
?? debug/tile_placer/pre_play_attempt1_OUTVIE.png
?? debug/tile_placer/pre_play_attempt1_PODGIEST.png
?? debug/tile_placer/pre_play_attempt1_PORTAGE.png
?? debug/tile_placer/pre_play_attempt1_QUIMS.png
?? debug/tile_placer/pre_play_attempt1_RANULAE.png
?? debug/tile_placer/pre_play_attempt1_ST.png
?? debug/tile_placer/pre_play_attempt1_TIN.png
?? debug/tile_placer/pre_play_attempt1_TOLA.png
?? debug/tile_placer/pre_play_attempt1_TOWELING.png
?? debug/tile_placer/pre_play_attempt1_VIAE.png
?? debug/tile_placer/pre_play_attempt1_VICAR.png
?? debug/tile_placer/pre_play_attempt1_VITEX.png
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
?? debug/tile_placer/pre_play_attempt2_COZ.png
?? debug/tile_placer/pre_play_attempt2_DI.png
?? debug/tile_placer/pre_play_attempt2_DITTY.png
?? debug/tile_placer/pre_play_attempt2_DOGGO.png
?? debug/tile_placer/pre_play_attempt2_FLAUTA.png
?? debug/tile_placer/pre_play_attempt2_GAZON.png
?? debug/tile_placer/pre_play_attempt2_GLOAT.png
?? debug/tile_placer/pre_play_attempt2_GOOLD.png
?? debug/tile_placer/pre_play_attempt2_INBYE.png
?? debug/tile_placer/pre_play_attempt2_IO.png
?? debug/tile_placer/pre_play_attempt2_KEEF.png
?? debug/tile_placer/pre_play_attempt2_KINARA.png
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
?? debug/tile_placer/pre_play_attempt2_ORAD.png
?? debug/tile_placer/pre_play_attempt2_OUTVIE.png
?? debug/tile_placer/pre_play_attempt2_POZ.png
?? debug/tile_placer/pre_play_attempt2_TAJINE.png
?? debug/tile_placer/pre_play_attempt2_TO.png
?? debug/tile_placer/pre_play_attempt2_TOWNLET.png
?? debug/tile_placer/pre_play_attempt2_TOXINS.png
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
?? debug/tile_placer/pre_play_attempt3_EXEAT.png
?? debug/tile_placer/pre_play_attempt3_FAKE.png
?? debug/tile_placer/pre_play_attempt3_FAUCAL.png
?? debug/tile_placer/pre_play_attempt3_GEL.png
?? debug/tile_placer/pre_play_attempt3_GI.png
?? debug/tile_placer/pre_play_attempt3_GOOGOL.png
?? debug/tile_placer/pre_play_attempt3_GOOLD.png
?? debug/tile_placer/pre_play_attempt3_HIELD.png
?? debug/tile_placer/pre_play_attempt3_JOEY.png
?? debug/tile_placer/pre_play_attempt3_KRONA.png
?? debug/tile_placer/pre_play_attempt3_LACUNA.png
?? debug/tile_placer/pre_play_attempt3_LANDAU.png
?? debug/tile_placer/pre_play_attempt3_LOD.png
?? debug/tile_placer/pre_play_attempt3_LOTO.png
?? debug/tile_placer/pre_play_attempt3_NABI.png
?? debug/tile_placer/pre_play_attempt3_NOT.png
?? debug/tile_placer/pre_play_attempt3_OF.png
?? debug/tile_placer/pre_play_attempt3_OUTVIE.png
?? debug/tile_placer/pre_play_attempt3_PORTAGE.png
?? debug/tile_placer/pre_play_attempt3_POZ.png
?? debug/tile_placer/pre_play_attempt3_QI.png
?? debug/tile_placer/pre_play_attempt3_ROAD.png
?? debug/tile_placer/pre_play_attempt3_SOZ.png
?? debug/tile_placer/pre_play_attempt3_TAJ.png
?? debug/tile_placer/pre_play_attempt3_TOWNLET.png
?? debug/tile_placer/pre_play_attempt3_TOXIN.png
?? debug/tile_placer/pre_play_attempt3_ULNAE.png
?? debug/tile_placer/pre_play_attempt3_VIE.png
?? debug/tile_placer/pre_play_attempt3_WELTING.png
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
?? debug/tile_placer/pre_play_attempt4_CARIBE.png
?? debug/tile_placer/pre_play_attempt4_CERIA.png
?? debug/tile_placer/pre_play_attempt4_DOL.png
?? debug/tile_placer/pre_play_attempt4_DOR.png
?? debug/tile_placer/pre_play_attempt4_DOTAL.png
?? debug/tile_placer/pre_play_attempt4_FAUNAL.png
?? debug/tile_placer/pre_play_attempt4_GLOWER.png
?? debug/tile_placer/pre_play_attempt4_GOLD.png
?? debug/tile_placer/pre_play_attempt4_GONG.png
?? debug/tile_placer/pre_play_attempt4_GOOLD.png
?? debug/tile_placer/pre_play_attempt4_JAILED.png
?? debug/tile_placer/pre_play_attempt4_KEEF.png
?? debug/tile_placer/pre_play_attempt4_LACUNAE.png
?? debug/tile_placer/pre_play_attempt4_LAGUNE.png
?? debug/tile_placer/pre_play_attempt4_LANGUE.png
?? debug/tile_placer/pre_play_attempt4_MOZO.png
?? debug/tile_placer/pre_play_attempt4_NUBIA.png
?? debug/tile_placer/pre_play_attempt4_OUTVIE.png
?? debug/tile_placer/pre_play_attempt4_PORTAGE.png
?? debug/tile_placer/pre_play_attempt4_RACIER.png
?? debug/tile_placer/pre_play_attempt4_TON.png
?? debug/tile_placer/pre_play_attempt4_VIA.png
?? debug/tile_placer/pre_play_attempt4_VITAE.png
?? debug/tile_placer/pre_play_attempt4_WIGLET.png
?? debug/tile_placer/pre_play_attempt4_ZIN.png
?? debug/tile_placer/pre_play_attempt4_ZO.png
?? debug/tile_placer/pre_play_attempt4_ZOO.png
?? debug/tile_placer/pre_play_attempt4_ZOS.png
?? debug/tile_placer/pre_play_attempt5_AREIC.png
?? debug/tile_placer/pre_play_attempt5_AZO.png
?? debug/tile_placer/pre_play_attempt5_BARIC.png
?? debug/tile_placer/pre_play_attempt5_BI.png
?? debug/tile_placer/pre_play_attempt5_BITTY.png
?? debug/tile_placer/pre_play_attempt5_EA.png
?? debug/tile_placer/pre_play_attempt5_EVITE.png
?? debug/tile_placer/pre_play_attempt5_FACULA.png
?? debug/tile_placer/pre_play_attempt5_FANGO.png
?? debug/tile_placer/pre_play_attempt5_FON.png
?? debug/tile_placer/pre_play_attempt5_GALOOT.png
?? debug/tile_placer/pre_play_attempt5_GOD.png
?? debug/tile_placer/pre_play_attempt5_GOLD.png
?? debug/tile_placer/pre_play_attempt5_JOINED.png
?? debug/tile_placer/pre_play_attempt5_KEEF.png
?? debug/tile_placer/pre_play_attempt5_LAGUNA.png
?? debug/tile_placer/pre_play_attempt5_LANATE.png
?? debug/tile_placer/pre_play_attempt5_NAB.png
?? debug/tile_placer/pre_play_attempt5_NABI.png
?? debug/tile_placer/pre_play_attempt5_NIB.png
?? debug/tile_placer/pre_play_attempt5_NOWL.png
?? debug/tile_placer/pre_play_attempt5_NY.png
?? debug/tile_placer/pre_play_attempt5_OUTVIE.png
?? debug/tile_placer/pre_play_attempt5_TOGA.png
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
?? logs/
?? scripts/auto_debug.py
?? scripts/autoplay_headless.py
?? src/engine/rejected_words.py
```

## git diff --stat
```
debug/preprocessed_debug.png               | Bin 371628 -> 314526 bytes
 debug/tile_placer/post_recall_attempt1.png | Bin 117178 -> 109393 bytes
 debug/tile_placer/post_recall_attempt2.png | Bin 120237 -> 108779 bytes
 debug/tile_placer/post_recall_attempt3.png | Bin 119929 -> 110419 bytes
 debug/tile_placer/post_recall_attempt4.png | Bin 119657 -> 103546 bytes
 debug/tile_placer/post_recall_attempt5.png | Bin 120024 -> 109985 bytes
 src/bot/autoplay_cog.py                    |  39 +++-
 src/browser/capture.py                     |  71 +++++-
 src/browser/tile_placer.py                 | 340 +++++++++++++++++++++++++----
 src/browser/turn_detector.py               | 191 +++++++++++++++-
 src/vision/__init__.py                     | 127 ++++++++---
 tests/test_tile_placer.py                  |  79 ++++++-
 12 files changed, 739 insertions(+), 108 deletions(-)
```