# Auto-debug iteration 6

- exit_code: `-9`
- duration: 3014.4s
- error_signature: `a0c59ed74500`

## Recent debug artifacts
- `debug/tile_placer/post_recall_attempt2.png`
- `debug/tile_placer/pre_play_attempt2_YEZ.png`
- `debug/tile_placer/post_recall_attempt1.png`
- `debug/turn_detection/frame_20260428_160630_875022_pre_start_attempt1.png`
- `debug/preprocessed_debug.png`

## Autoplay log — error region
```
2026-04-28 16:22:08.948 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1047
2026-04-28 16:22:08.949 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'S' placement not verified — retrying with fresh jitter
2026-04-28 16:22:09.815 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121972 bytes (attempt 1)
2026-04-28 16:22:11.581 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120880 bytes (attempt 1)
2026-04-28 16:22:11.712 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1337
2026-04-28 16:22:11.713 | ERROR   | src.browser.tile_placer:place_move:1074 | Tile placement failed for 'LEASINGS' (attempt 2): Tile 'S' at (7,16) failed to place after retry
2026-04-28 16:22:11.902 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:22:12.830 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122105 bytes (attempt 1)
2026-04-28 16:22:12.830 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.2, 753.2) (pass 1/10)
2026-04-28 16:22:15.323 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119800 bytes (attempt 1)
2026-04-28 16:22:15.492 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.9, 751.2) (pass 2/10)
2026-04-28 16:22:17.377 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119031 bytes (attempt 1)
2026-04-28 16:22:17.503 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.4, 749.6) (pass 3/10)
2026-04-28 16:22:19.509 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119295 bytes (attempt 1)
2026-04-28 16:22:19.667 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.3, 748.7) (pass 4/10)
2026-04-28 16:22:22.276 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120353 bytes (attempt 1)
2026-04-28 16:22:22.436 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.8, 751.2) (pass 5/10)
2026-04-28 16:22:24.655 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119705 bytes (attempt 1)
2026-04-28 16:22:24.777 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.7, 750.5) (pass 6/10)
2026-04-28 16:22:27.963 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120024 bytes (attempt 1)
2026-04-28 16:22:28.160 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.6, 748.5) (pass 7/10)
2026-04-28 16:22:30.218 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120007 bytes (attempt 1)
2026-04-28 16:22:30.664 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.2, 750.5) (pass 8/10)
2026-04-28 16:22:32.766 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119523 bytes (attempt 1)
2026-04-28 16:22:32.939 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.9, 748.3) (pass 9/10)
2026-04-28 16:22:35.655 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119595 bytes (attempt 1)
2026-04-28 16:22:35.906 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.9, 751.2) (pass 10/10)
2026-04-28 16:22:38.082 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119957 bytes (attempt 1)
2026-04-28 16:22:38.243 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 16:22:39.120 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119724 bytes (attempt 1)
2026-04-28 16:22:39.124 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt2.png
2026-04-28 16:22:39.124 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 3/5: 'LEADINGS' (score=88)
2026-04-28 16:22:39.292 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:22:39.292 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 5) -> board (4,16) | src=(1257.7,825.7) dst=(1297.2,320.7)
2026-04-28 16:22:40.165 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119900 bytes (attempt 1)
2026-04-28 16:22:42.128 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121270 bytes (attempt 1)
2026-04-28 16:22:42.248 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6469
2026-04-28 16:22:42.248 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (4,16)
2026-04-28 16:22:42.687 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 0) -> board (5,16) | src=(982.4,828.1) dst=(1294.8,354.8)
2026-04-28 16:22:43.645 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120484 bytes (attempt 1)
2026-04-28 16:22:45.571 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121247 bytes (attempt 1)
2026-04-28 16:22:45.696 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.0696
2026-04-28 16:22:45.697 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'E' placement not verified — retrying with fresh jitter
2026-04-28 16:22:46.506 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122093 bytes (attempt 1)
2026-04-28 16:22:48.442 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121329 bytes (attempt 1)
2026-04-28 16:22:48.554 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1804
2026-04-28 16:22:48.555 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (5,16)
2026-04-28 16:22:49.161 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (6,16) | src=(1313.2,829.2) dst=(1296.1,390.2)
2026-04-28 16:22:50.046 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121087 bytes (attempt 1)
2026-04-28 16:22:53.066 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120962 bytes (attempt 1)
2026-04-28 16:22:53.478 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.7600
2026-04-28 16:22:53.484 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (6,16)
2026-04-28 16:22:54.130 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'D' (slot 3) -> board (7,16) | src=(1146.7,827.7) dst=(1297.8,422.9)
2026-04-28 16:22:54.922 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120922 bytes (attempt 1)
2026-04-28 16:22:56.815 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122028 bytes (attempt 1)
2026-04-28 16:22:56.929 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.2099
2026-04-28 16:22:58.416 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121601 bytes (attempt 1)
2026-04-28 16:22:59.784 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120320 bytes (attempt 1)
2026-04-28 16:22:59.903 | DEBUG   | src.browser.tile_placer:_verify_dialog_dismissed:588 | Blank dialog dismiss pixel diff: 0.3466
2026-04-28 16:22:59.904 | INFO    | src.browser.tile_placer:_dismiss_blank_letter_dialog:483 | Blank dialog: dismissed 'D' via keyboard press
2026-04-28 16:23:00.420 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'D' verified at (7,16)
2026-04-28 16:23:00.877 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'I' (slot 1) -> board (8,16) | src=(1034.3,827.5) dst=(1299.9,458.4)
2026-04-28 16:23:01.902 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121829 bytes (attempt 1)
2026-04-28 16:23:03.724 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120755 bytes (attempt 1)
2026-04-28 16:23:03.862 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1711
2026-04-28 16:23:03.863 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'I' verified at (8,16)
2026-04-28 16:23:04.474 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'G' (slot 4) -> board (10,16) | src=(1200.5,830.8) dst=(1297.6,528.5)
2026-04-28 16:23:05.500 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121018 bytes (attempt 1)
2026-04-28 16:23:07.584 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120245 bytes (attempt 1)
2026-04-28 16:23:07.744 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.2771
2026-04-28 16:23:07.745 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'G' verified at (10,16)
2026-04-28 16:23:08.314 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'S' (slot 2) -> board (11,16) | src=(1088.2,829.5) dst=(1297.4,566.7)
2026-04-28 16:23:09.230 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121112 bytes (attempt 1)
2026-04-28 16:23:11.066 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121698 bytes (attempt 1)
2026-04-28 16:23:11.276 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6742
2026-04-28 16:23:11.277 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'S' verified at (11,16)
2026-04-28 16:23:12.214 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121645 bytes (attempt 1)
2026-04-28 16:23:12.221 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt3_LEADINGS.png
2026-04-28 16:23:13.095 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:23:13.095 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1149.7, 749.0)
2026-04-28 16:23:14.840 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122379 bytes (attempt 1)
2026-04-28 16:23:14.958 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: my_turn
2026-04-28 16:23:14.959 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:826 | Re-clicking PLAY (retry after 1 polls)
2026-04-28 16:23:14.960 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1147.7, 748.9)
2026-04-28 16:23:16.452 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122029 bytes (attempt 1)
2026-04-28 16:23:16.575 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 2/3: my_turn
2026-04-28 16:23:18.091 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121873 bytes (attempt 1)
2026-04-28 16:23:18.249 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 3/3: my_turn
2026-04-28 16:23:18.252 | INFO    | src.browser.tile_placer:place_move:1111 | Word 'LEADINGS' rejected (attempt 3/5) — recalling tiles
2026-04-28 16:23:18.255 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'leadings' (total: 217)
2026-04-28 16:23:19.131 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121639 bytes (attempt 1)
2026-04-28 16:23:19.132 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.9, 752.2) (pass 1/10)
2026-04-28 16:23:21.123 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119796 bytes (attempt 1)
2026-04-28 16:23:21.226 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.6, 753.5) (pass 2/10)
2026-04-28 16:23:23.007 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120138 bytes (attempt 1)
2026-04-28 16:23:23.137 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.7, 749.1) (pass 3/10)
2026-04-28 16:23:25.290 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119339 bytes (attempt 1)
2026-04-28 16:23:25.406 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.2, 751.8) (pass 4/10)
2026-04-28 16:23:27.574 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119151 bytes (attempt 1)
2026-04-28 16:23:27.689 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.1, 753.2) (pass 5/10)
2026-04-28 16:23:30.029 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119191 bytes (attempt 1)
2026-04-28 16:23:30.143 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.7, 749.6) (pass 6/10)
2026-04-28 16:23:32.057 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119644 bytes (attempt 1)
2026-04-28 16:23:32.195 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.6, 752.2) (pass 7/10)
2026-04-28 16:23:34.532 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119883 bytes (attempt 1)
2026-04-28 16:23:34.731 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.4, 750.8) (pass 8/10)
2026-04-28 16:23:36.738 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118862 bytes (attempt 1)
2026-04-28 16:23:36.869 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.7, 749.9) (pass 9/10)
2026-04-28 16:23:38.886 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120029 bytes (attempt 1)
2026-04-28 16:23:39.008 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.6, 752.2) (pass 10/10)
2026-04-28 16:23:40.940 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120024 bytes (attempt 1)
2026-04-28 16:23:41.096 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 16:23:41.959 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119829 bytes (attempt 1)
2026-04-28 16:23:41.962 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt3.png
2026-04-28 16:23:41.963 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 4/5: 'LEAVINGS' (score=88)
2026-04-28 16:23:42.083 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:23:42.084 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 5) -> board (4,16) | src=(1256.6,827.1) dst=(1298.6,320.9)
2026-04-28 16:23:43.307 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120018 bytes (attempt 1)
2026-04-28 16:23:45.136 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121069 bytes (attempt 1)
2026-04-28 16:23:45.269 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.0788
2026-04-28 16:23:45.270 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (4,16)
2026-04-28 16:23:45.743 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 0) -> board (5,16) | src=(980.0,827.4) dst=(1295.3,358.6)
2026-04-28 16:23:46.676 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121144 bytes (attempt 1)
2026-04-28 16:23:48.598 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121445 bytes (attempt 1)
2026-04-28 16:23:48.778 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1371
2026-04-28 16:23:48.779 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'E' placement not verified — retrying with fresh jitter
2026-04-28 16:23:49.686 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120721 bytes (attempt 1)
2026-04-28 16:23:51.560 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121107 bytes (attempt 1)
2026-04-28 16:23:51.816 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3438
2026-04-28 16:23:51.821 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (5,16)
2026-04-28 16:23:52.268 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (6,16) | src=(1310.2,829.3) dst=(1299.2,391.9)
2026-04-28 16:23:53.123 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121645 bytes (attempt 1)
2026-04-28 16:23:56.145 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120852 bytes (attempt 1)
2026-04-28 16:23:56.340 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.1524
2026-04-28 16:23:56.342 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (6,16)
2026-04-28 16:23:56.851 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'V' (slot 3) -> board (7,16) | src=(1145.0,830.9) dst=(1300.5,426.9)
2026-04-28 16:23:57.795 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119616 bytes (attempt 1)
2026-04-28 16:23:59.706 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120608 bytes (attempt 1)
2026-04-28 16:23:59.825 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1477
2026-04-28 16:23:59.826 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'V' placement not verified — retrying with fresh jitter
2026-04-28 16:24:00.650 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121201 bytes (attempt 1)
2026-04-28 16:24:02.953 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120658 bytes (attempt 1)
2026-04-28 16:24:03.074 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.0552
2026-04-28 16:24:03.075 | ERROR   | src.browser.tile_placer:place_move:1074 | Tile placement failed for 'LEAVINGS' (attempt 4): Tile 'V' at (7,16) failed to place after retry
2026-04-28 16:24:03.218 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:24:04.078 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120861 bytes (attempt 1)
2026-04-28 16:24:04.079 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.1, 752.5) (pass 1/10)
2026-04-28 16:24:06.498 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120075 bytes (attempt 1)
2026-04-28 16:24:06.620 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.0, 753.5) (pass 2/10)
2026-04-28 16:24:08.944 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120107 bytes (attempt 1)
2026-04-28 16:24:09.147 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.0, 752.3) (pass 3/10)
2026-04-28 16:24:10.981 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119878 bytes (attempt 1)
2026-04-28 16:24:11.120 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.0, 751.6) (pass 4/10)
2026-04-28 16:24:13.365 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119277 bytes (attempt 1)
2026-04-28 16:24:13.504 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.9, 748.0) (pass 5/10)
2026-04-28 16:24:15.586 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119327 bytes (attempt 1)
2026-04-28 16:24:15.709 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.1, 749.7) (pass 6/10)
2026-04-28 16:24:17.894 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120032 bytes (attempt 1)
2026-04-28 16:24:18.025 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.3, 753.3) (pass 7/10)
2026-04-28 16:24:19.981 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119829 bytes (attempt 1)
2026-04-28 16:24:20.101 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.2, 752.2) (pass 8/10)
2026-04-28 16:24:21.993 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119621 bytes (attempt 1)
2026-04-28 16:24:22.106 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.6, 749.2) (pass 9/10)
2026-04-28 16:24:23.962 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119863 bytes (attempt 1)
2026-04-28 16:24:24.085 | INFO    | src.browser.tile_placer:_recall_tiles:891 | Recall complete after 9 click(s) — canvas stable
2026-04-28 16:24:25.027 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120010 bytes (attempt 1)
2026-04-28 16:24:25.030 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt4.png
2026-04-28 16:24:25.032 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 5/5: 'EANLINGS' (score=80)
2026-04-28 16:24:25.198 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:24:25.198 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 0) -> board (7,16) | src=(979.1,829.9) dst=(1298.7,428.3)
2026-04-28 16:24:26.144 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119894 bytes (attempt 1)
2026-04-28 16:24:27.917 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120943 bytes (attempt 1)
2026-04-28 16:24:28.057 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1971
2026-04-28 16:24:28.058 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (7,16)
2026-04-28 16:24:28.672 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 6) -> board (8,16) | src=(1309.1,828.3) dst=(1298.1,462.7)
2026-04-28 16:24:29.768 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119942 bytes (attempt 1)
2026-04-28 16:24:31.523 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120051 bytes (attempt 1)
2026-04-28 16:24:31.652 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1626
2026-04-28 16:24:31.653 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'A' verified at (8,16)
2026-04-28 16:24:32.346 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 5) -> board (10,16) | src=(1256.0,828.1) dst=(1297.3,531.2)
2026-04-28 16:24:33.368 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119716 bytes (attempt 1)
2026-04-28 16:24:35.615 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120205 bytes (attempt 1)
2026-04-28 16:24:35.800 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3460
2026-04-28 16:24:35.801 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (10,16)
2026-04-28 16:24:36.466 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'I' (slot 1) -> board (11,16) | src=(1033.0,826.2) dst=(1300.2,563.9)
2026-04-28 16:24:37.838 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120258 bytes (attempt 1)
2026-04-28 16:24:39.626 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120040 bytes (attempt 1)
2026-04-28 16:24:39.738 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1399
2026-04-28 16:24:39.739 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'I' placement not verified — retrying with fresh jitter
2026-04-28 16:24:40.783 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120767 bytes (attempt 1)
2026-04-28 16:24:42.581 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120001 bytes (attempt 1)
2026-04-28 16:24:42.765 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.0758
2026-04-28 16:24:42.766 | ERROR   | src.browser.tile_placer:place_move:1074 | Tile placement failed for 'EANLINGS' (attempt 5): Tile 'I' at (11,16) failed to place after retry
2026-04-28 16:24:42.925 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:24:44.499 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120066 bytes (attempt 1)
2026-04-28 16:24:44.502 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.5, 750.1) (pass 1/10)
2026-04-28 16:24:46.594 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119733 bytes (attempt 1)
2026-04-28 16:24:46.715 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.5, 752.9) (pass 2/10)
2026-04-28 16:24:49.084 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119983 bytes (attempt 1)
2026-04-28 16:24:49.225 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.9, 751.6) (pass 3/10)
2026-04-28 16:24:51.345 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118910 bytes (attempt 1)
2026-04-28 16:24:51.496 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.7, 751.6) (pass 4/10)
2026-04-28 16:24:53.804 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120171 bytes (attempt 1)
2026-04-28 16:24:53.939 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.1, 749.8) (pass 5/10)
2026-04-28 16:24:56.390 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119699 bytes (attempt 1)
2026-04-28 16:24:56.625 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.0, 748.7) (pass 6/10)
2026-04-28 16:24:58.998 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120215 bytes (attempt 1)
2026-04-28 16:24:59.154 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.9, 752.0) (pass 7/10)
2026-04-28 16:25:01.184 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119255 bytes (attempt 1)
2026-04-28 16:25:01.302 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.5, 753.1) (pass 8/10)
2026-04-28 16:25:05.101 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119665 bytes (attempt 1)
2026-04-28 16:25:05.482 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.7, 748.9) (pass 9/10)
2026-04-28 16:25:08.409 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119940 bytes (attempt 1)
2026-04-28 16:25:08.533 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.9, 748.3) (pass 10/10)
2026-04-28 16:25:10.907 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119675 bytes (attempt 1)
2026-04-28 16:25:11.108 | WARNING | src.browser.tile_placer:_recall_tiles:899 | Recall hit cap (10 clicks) without stabilising
2026-04-28 16:25:12.343 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119718 bytes (attempt 1)
2026-04-28 16:25:12.348 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt5.png
2026-04-28 16:25:12.348 | WARNING | src.browser.tile_placer:place_move:1130 | All 5 word attempt(s) failed — returning to caller for re-vision
2026-04-28 16:25:12.351 | WARNING | __main__:_run:239 | No move accepted (candidates=5) — re-vision + swap fallback
2026-04-28 16:25:16.194 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119803 bytes (attempt 1)
2026-04-28 16:25:16.195 | INFO    | src.vision:extract_board_state:148 | Vision pipeline start — mode=wild
2026-04-28 16:25:16.262 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,54) 1366×657 from 1545×768 canvas
2026-04-28 16:25:16.606 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-04-28 16:25:16.840 | INFO    | src.vision:extract_board_state:154 | Preprocessing complete — 379135 bytes
2026-04-28 16:25:16.844 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=False
2026-04-28 16:25:21.706 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=4.85s  input_tokens=2903  output_tokens=253
2026-04-28 16:25:21.732 | INFO    | src.vision:extract_board_state:160 | Extraction complete (first attempt)
2026-04-28 16:25:21.733 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (7,17)=E[DL] (9,11)=P[DW] (9,12)=R[TL] (9,13)=O[DW] (9,14)=V[TL] (9,15)=E[DW] (9,16)=N[DL] (10,17)=D[DL]
2026-04-28 16:25:21.741 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['G', 'I', 'S', 'L', 'A', 'E']
2026-04-28 16:25:22.023 | INFO    | src.vision.validator:correct_positions:101 | Position auto-correction: shifting tiles by (-3, -1) — multiplier matches 2 → 4
2026-04-28 16:25:22.036 | INFO    | src.vision.validator:correct_positions_center_star:193 | Center star correction: shifting tiles by (+3, +1) to place a tile on (9,13) — multiplier score 4
2026-04-28 16:25:22.037 | INFO    | src.vision:extract_board_state:179 | Validation result — 3 error(s)
2026-04-28 16:25:22.118 | WARNING | src.vision:extract_board_state:205 | Validation failed (3 errors), retrying: ["Floating tile 'E' at (7, 17) — not connected to other tiles", "Floating tile 'D' at (10, 17) — not connected to other tiles", 'Position accuracy suspect: 6/8 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
2026-04-28 16:25:22.119 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=True
2026-04-28 16:25:27.529 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=5.31s  input_tokens=3000  output_tokens=252
2026-04-28 16:25:27.531 | INFO    | src.vision:extract_board_state:211 | Extraction complete (retry)
2026-04-28 16:25:27.531 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (7,16)=E[DL] (9,11)=P[DW] (9,12)=R[DL] (9,13)=O[DW] (9,14)=V[DL] (9,15)=E[DW] (9,16)=N[DL] (10,16)=D[TL]
2026-04-28 16:25:27.538 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['G', 'I', 'S', 'L', 'A', 'E']
2026-04-28 16:25:27.539 | INFO    | src.vision.validator:correct_positions:101 | Position auto-correction: shifting tiles by (-3, +0) — multiplier matches 3 → 4
2026-04-28 16:25:27.559 | DEBUG   | src.vision.validator:correct_positions_gaddag:317 | GADDAG position correction: no shift improves word validity (current 1/2 valid runs)
2026-04-28 16:25:27.561 | INFO    | src.vision:extract_board_state:230 | Merged 8 cell(s) from first attempt that retry dropped: [('E', 7, 17), ('P', 9, 11), ('R', 9, 12), ('O', 9, 13), ('V', 9, 14), ('E', 9, 15), ('N', 9, 16), ('D', 10, 17)]
2026-04-28 16:25:27.562 | INFO    | src.vision:extract_board_state:259 | Validation result after retry — 10 error(s)
2026-04-28 16:25:27.586 | WARNING | src.vision:extract_board_state:289 | Removed 8 floating tile(s) to salvage extraction
2026-04-28 16:25:27.587 | WARNING | src.vision:extract_board_state:308 | Word validity check failed (1 word(s)) after retry — proceeding with best-effort extraction: ["Invalid word(s) on board: 'ND' at col 16 rows 6-7 — tile positions are likely off by 1. Re-count carefully from center star at (9,13)."]
2026-04-28 16:25:27.588 | WARNING | src.vision:extract_board_state:319 | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 7/10 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
2026-04-28 16:25:27.615 | INFO    | src.vision:extract_board_state:353 | Vision pipeline complete — 11.42s  tiles=8  rack_size=6
2026-04-28 16:25:28.101 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 35 blacklisted candidate(s)
2026-04-28 16:25:28.107 | INFO    | src.browser.tile_placer:place_move:1063 | Word attempt 1/3: 'LIGASE' (score=42)
2026-04-28 16:25:28.242 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:25:28.243 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 3) -> board (2,18) | src=(1148.8,825.9) dst=(1397.3,254.2)
2026-04-28 16:25:29.520 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119263 bytes (attempt 1)
2026-04-28 16:25:31.394 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119823 bytes (attempt 1)
2026-04-28 16:25:31.550 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.7472
2026-04-28 16:25:31.553 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (2,18)
2026-04-28 16:25:31.997 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'I' (slot 1) -> board (3,18) | src=(1038.0,826.5) dst=(1399.6,286.6)
2026-04-28 16:25:33.072 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120499 bytes (attempt 1)
2026-04-28 16:25:34.912 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121844 bytes (attempt 1)
2026-04-28 16:25:35.059 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6882
2026-04-28 16:25:35.059 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'I' verified at (3,18)
2026-04-28 16:25:35.477 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'G' (slot 0) -> board (4,18) | src=(982.2,828.5) dst=(1397.9,323.4)
2026-04-28 16:25:36.362 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121602 bytes (attempt 1)
2026-04-28 16:25:39.412 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120796 bytes (attempt 1)
2026-04-28 16:25:39.546 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.8345
2026-04-28 16:25:39.547 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'G' verified at (4,18)
2026-04-28 16:25:39.963 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'A' (slot 4) -> board (5,18) | src=(1203.2,829.7) dst=(1398.2,356.4)
2026-04-28 16:25:40.741 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121826 bytes (attempt 1)
2026-04-28 16:25:42.614 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122602 bytes (attempt 1)
2026-04-28 16:25:42.774 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.0601
2026-04-28 16:25:42.775 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'A' placement not verified — retrying with fresh jitter
2026-04-28 16:25:43.758 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121872 bytes (attempt 1)
2026-04-28 16:25:45.723 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121437 bytes (attempt 1)
2026-04-28 16:25:45.857 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.0776
2026-04-28 16:25:45.858 | ERROR   | src.browser.tile_placer:place_move:1074 | Tile placement failed for 'LIGASE' (attempt 1): Tile 'A' at (5,18) failed to place after retry
2026-04-28 16:25:46.117 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:25:47.500 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121892 bytes (attempt 1)
2026-04-28 16:25:47.501 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.3, 750.1) (pass 1/10)
2026-04-28 16:25:50.153 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119522 bytes (attempt 1)
2026-04-28 16:25:50.866 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.9, 750.2) (pass 2/10)
2026-04-28 16:25:52.890 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120232 bytes (attempt 1)
2026-04-28 16:25:53.010 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1288.2, 749.4) (pass 3/10)
2026-04-28 16:25:55.563 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119086 bytes (attempt 1)
2026-04-28 16:25:56.252 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.0, 753.8) (pass 4/10)
2026-04-28 16:25:58.657 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119751 bytes (attempt 1)
2026-04-28 16:25:58.785 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.6, 751.6) (pass 5/10)
2026-04-28 16:26:00.626 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119741 bytes (attempt 1)
2026-04-28 16:26:00.739 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.8, 750.8) (pass 6/10)
2026-04-28 16:26:02.898 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119921 bytes (attempt 1)
2026-04-28 16:26:03.028 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.8, 752.6) (pass 7/10)
2026-04-28 16:26:04.922 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119957 bytes (attempt 1)
2026-04-28 16:26:05.029 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.8, 751.4) (pass 8/10)
2026-04-28 16:26:07.188 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119140 bytes (attempt 1)
2026-04-28 16:26:07.348 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.6, 753.4) (pass 9/10)
```

## Subprocess stderr (tail)
```
[32m16:32:39[0m | [1mINFO   [0m | Placing tile 'E' (slot 0) -> board (12,16) | src=(980.1,825.5) dst=(1297.6,599.6)
[32m16:32:41[0m | [1mINFO   [0m | Tile 'E' verified at (12,16)
[32m16:32:42[0m | [1mINFO   [0m | Placing tile 'S' (slot 3) -> board (13,16) | src=(1143.1,826.3) dst=(1300.6,630.6)
[32m16:32:45[0m | [1mINFO   [0m | Tile 'S' verified at (13,16)
[32m16:32:46[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.3, 751.2)
[32m16:32:48[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.0, 752.1)
[32m16:32:52[0m | [1mINFO   [0m | Word 'LINGOES' rejected (attempt 5/5) — recalling tiles
[32m16:32:52[0m | [1mINFO   [0m | Blacklisted rejected word 'lingoes' (total: 224)
[32m16:32:53[0m | [1mINFO   [0m | Clicking recall button at (1284.5, 752.7) (pass 1/10)
[32m16:32:55[0m | [1mINFO   [0m | Clicking recall button at (1284.2, 748.1) (pass 2/10)
[32m16:32:57[0m | [1mINFO   [0m | Clicking recall button at (1286.6, 751.8) (pass 3/10)
[32m16:33:00[0m | [1mINFO   [0m | Clicking recall button at (1286.5, 753.0) (pass 4/10)
[32m16:33:02[0m | [1mINFO   [0m | Clicking recall button at (1284.5, 751.7) (pass 5/10)
[32m16:33:04[0m | [1mINFO   [0m | Clicking recall button at (1286.6, 748.6) (pass 6/10)
[32m16:33:07[0m | [1mINFO   [0m | Clicking recall button at (1285.4, 749.1) (pass 7/10)
[32m16:33:10[0m | [1mINFO   [0m | Recall complete after 7 click(s) — canvas stable
[32m16:33:11[0m | [33m[1mWARNING[0m | All 5 word attempt(s) failed — returning to caller for re-vision
[32m16:33:11[0m | [33m[1mWARNING[0m | No move accepted (candidates=5) — re-vision + swap fallback
[32m16:33:15[0m | [1mINFO   [0m | Vision pipeline start — mode=wild
[32m16:33:15[0m | [1mINFO   [0m | Preprocessing complete — 378979 bytes
[32m16:33:15[0m | [1mINFO   [0m | Calling Claude Vision API — retry=False
[32m16:33:21[0m | [1mINFO   [0m | Claude Vision response received — latency=5.43s  input_tokens=2903  output_tokens=256
[32m16:33:21[0m | [1mINFO   [0m | Extraction complete (first attempt)
[32m16:33:21[0m | [1mINFO   [0m | Validation result — 3 error(s)
[32m16:33:21[0m | [33m[1mWARNING[0m | Validation failed (3 errors), retrying: ["Floating tile 'E' at (7, 16) — not connected to other tiles", "Floating tile 'D' at (11, 16) — not connected to other tiles", 'Position accuracy suspect: 6/8 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m16:33:21[0m | [1mINFO   [0m | Calling Claude Vision API — retry=True
[32m16:33:25[0m | [1mINFO   [0m | Claude Vision response received — latency=4.67s  input_tokens=3000  output_tokens=254
[32m16:33:25[0m | [1mINFO   [0m | Extraction complete (retry)
[32m16:33:25[0m | [1mINFO   [0m | Validation result after retry — 3 error(s)
[32m16:33:25[0m | [33m[1mWARNING[0m | Removed 2 floating tile(s) to salvage extraction
[32m16:33:25[0m | [33m[1mWARNING[0m | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 6/8 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m16:33:25[0m | [1mINFO   [0m | Vision pipeline complete — 10.54s  tiles=6  rack_size=7
[32m16:33:26[0m | [1mINFO   [0m | Word attempt 1/5: 'FEZ' (score=30)
[32m16:33:26[0m | [1mINFO   [0m | Placing tile 'F' (slot 5) -> board (8,15) | src=(1258.8,829.0) dst=(1247.3,459.8)
[32m16:33:29[0m | [1mINFO   [0m | Tile 'F' verified at (8,15)
[32m16:33:30[0m | [1mINFO   [0m | Placing tile 'Z' (slot 0) -> board (10,15) | src=(977.9,825.5) dst=(1245.5,527.5)
[32m16:33:33[0m | [1mINFO   [0m | Tile 'Z' verified at (10,15)
[32m16:33:36[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1144.3, 749.2)
[32m16:33:38[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1149.7, 748.2)
[32m16:33:41[0m | [1mINFO   [0m | Word 'FEZ' rejected (attempt 1/5) — recalling tiles
[32m16:33:41[0m | [1mINFO   [0m | Blacklisted rejected word 'fez' (total: 225)
[32m16:33:42[0m | [1mINFO   [0m | Clicking recall button at (1287.1, 752.0) (pass 1/10)
[32m16:33:45[0m | [1mINFO   [0m | Clicking recall button at (1287.0, 752.4) (pass 2/10)
[32m16:33:47[0m | [1mINFO   [0m | Clicking recall button at (1287.5, 749.3) (pass 3/10)
[32m16:33:49[0m | [1mINFO   [0m | Clicking recall button at (1282.9, 751.9) (pass 4/10)
[32m16:33:52[0m | [1mINFO   [0m | Clicking recall button at (1286.2, 753.9) (pass 5/10)
[32m16:33:54[0m | [1mINFO   [0m | Clicking recall button at (1285.5, 749.1) (pass 6/10)
[32m16:33:56[0m | [1mINFO   [0m | Clicking recall button at (1284.4, 748.1) (pass 7/10)
[32m16:33:59[0m | [1mINFO   [0m | Clicking recall button at (1284.7, 752.1) (pass 8/10)
[32m16:34:02[0m | [1mINFO   [0m | Clicking recall button at (1285.5, 753.8) (pass 9/10)
[32m16:34:04[0m | [1mINFO   [0m | Clicking recall button at (1283.1, 752.0) (pass 10/10)
[32m16:34:07[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m16:34:09[0m | [1mINFO   [0m | Word attempt 2/5: 'YEZ' (score=30)
[32m16:34:09[0m | [1mINFO   [0m | Placing tile 'Y' (slot 1) -> board (8,15) | src=(1032.8,827.5) dst=(1248.1,461.8)
[32m16:34:15[0m | [1mINFO   [0m | Tile 'Y' verified at (8,15)
[32m16:34:16[0m | [1mINFO   [0m | Placing tile 'Z' (slot 0) -> board (10,15) | src=(977.8,826.2) dst=(1250.0,526.8)
[32m16:34:21[0m | [1mINFO   [0m | Tile 'Z' verified at (10,15)
[32m16:34:23[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1148.0, 752.6)
[32m16:34:25[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1148.3, 751.2)
[32m16:34:29[0m | [1mINFO   [0m | Word 'YEZ' rejected (attempt 2/5) — recalling tiles
[32m16:34:29[0m | [1mINFO   [0m | Blacklisted rejected word 'yez' (total: 226)
[32m16:34:30[0m | [1mINFO   [0m | Clicking recall button at (1284.3, 749.3) (pass 1/10)
[32m16:34:32[0m | [1mINFO   [0m | Clicking recall button at (1283.0, 749.2) (pass 2/10)
[32m16:34:35[0m | [1mINFO   [0m | Clicking recall button at (1287.3, 751.1) (pass 3/10)
[32m16:34:38[0m | [1mINFO   [0m | Clicking recall button at (1287.1, 750.2) (pass 4/10)
[32m16:34:40[0m | [1mINFO   [0m | Clicking recall button at (1283.4, 752.0) (pass 5/10)
[32m16:34:42[0m | [1mINFO   [0m | Clicking recall button at (1287.1, 748.5) (pass 6/10)
[32m16:34:45[0m | [1mINFO   [0m | Clicking recall button at (1283.7, 749.9) (pass 7/10)
[32m16:34:47[0m | [1mINFO   [0m | Clicking recall button at (1283.0, 753.4) (pass 8/10)
[32m16:34:49[0m | [1mINFO   [0m | Clicking recall button at (1284.5, 748.4) (pass 9/10)
[32m16:34:51[0m | [1mINFO   [0m | Clicking recall button at (1286.5, 750.6) (pass 10/10)
[32m16:34:54[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m16:34:54[0m | [1mINFO   [0m | Word attempt 3/5: 'FYRD' (score=26)
[32m16:34:55[0m | [1mINFO   [0m | Placing tile 'F' (slot 5) -> board (10,15) | src=(1257.8,829.1) dst=(1248.6,531.7)
[32m16:34:58[0m | [1mINFO   [0m | Tile 'F' verified at (10,15)
[32m16:34:58[0m | [1mINFO   [0m | Placing tile 'Y' (slot 1) -> board (10,16) | src=(1036.7,827.3) dst=(1297.8,530.7)
[32m16:35:02[0m | [1mINFO   [0m | Tile 'Y' verified at (10,16)
[32m16:35:03[0m | [1mINFO   [0m | Placing tile 'R' (slot 2) -> board (10,17) | src=(1093.7,830.5) dst=(1348.9,526.8)

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
 M src/browser/navigator.py
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
?? debug/tile_placer/pre_play_attempt1_DEWIER.png
?? debug/tile_placer/pre_play_attempt1_DIG.png
?? debug/tile_placer/pre_play_attempt1_DIYA.png
?? debug/tile_placer/pre_play_attempt1_DOG.png
?? debug/tile_placer/pre_play_attempt1_EEN.png
?? debug/tile_placer/pre_play_attempt1_EL.png
?? debug/tile_placer/pre_play_attempt1_FAKE.png
?? debug/tile_placer/pre_play_attempt1_FEZ.png
?? debug/tile_placer/pre_play_attempt1_FIBERS.png
?? debug/tile_placer/pre_play_attempt1_FIZ.png
?? debug/tile_placer/pre_play_attempt1_FLEET.png
?? debug/tile_placer/pre_play_attempt1_FORKY.png
?? debug/tile_placer/pre_play_attempt1_FOUR.png
?? debug/tile_placer/pre_play_attempt1_FROG.png
?? debug/tile_placer/pre_play_attempt1_FUTURE.png
?? debug/tile_placer/pre_play_attempt1_FYCE.png
?? debug/tile_placer/pre_play_attempt1_GARNET.png
?? debug/tile_placer/pre_play_attempt1_GIF.png
?? debug/tile_placer/pre_play_attempt1_GIFT.png
?? debug/tile_placer/pre_play_attempt1_GINZO.png
?? debug/tile_placer/pre_play_attempt1_GOOD.png
?? debug/tile_placer/pre_play_attempt1_GOOGOL.png
?? debug/tile_placer/pre_play_attempt1_GOOLD.png
?? debug/tile_placer/pre_play_attempt1_GOWF.png
?? debug/tile_placer/pre_play_attempt1_GROW.png
?? debug/tile_placer/pre_play_attempt1_GRUNGY.png
?? debug/tile_placer/pre_play_attempt1_HAULING.png
?? debug/tile_placer/pre_play_attempt1_HINGED.png
?? debug/tile_placer/pre_play_attempt1_ID.png
?? debug/tile_placer/pre_play_attempt1_JIAO.png
?? debug/tile_placer/pre_play_attempt1_JOEY.png
?? debug/tile_placer/pre_play_attempt1_JOINT.png
?? debug/tile_placer/pre_play_attempt1_JOINTS.png
?? debug/tile_placer/pre_play_attempt1_KENDO.png
?? debug/tile_placer/pre_play_attempt1_KURU.png
?? debug/tile_placer/pre_play_attempt1_LANGUISH.png
?? debug/tile_placer/pre_play_attempt1_LEAK.png
?? debug/tile_placer/pre_play_attempt1_LEANINGS.png
?? debug/tile_placer/pre_play_attempt1_LEG.png
?? debug/tile_placer/pre_play_attempt1_LOGO.png
?? debug/tile_placer/pre_play_attempt1_MANUAL.png
?? debug/tile_placer/pre_play_attempt1_NAWAB.png
?? debug/tile_placer/pre_play_attempt1_NAY.png
?? debug/tile_placer/pre_play_attempt1_NEEDLE.png
?? debug/tile_placer/pre_play_attempt1_NEURAL.png
?? debug/tile_placer/pre_play_attempt1_OI.png
?? debug/tile_placer/pre_play_attempt1_OUTVIE.png
?? debug/tile_placer/pre_play_attempt1_PIX.png
?? debug/tile_placer/pre_play_attempt1_PIXEL.png
?? debug/tile_placer/pre_play_attempt1_PODGIEST.png
?? debug/tile_placer/pre_play_attempt1_PORTAGE.png
?? debug/tile_placer/pre_play_attempt1_PROVEN.png
?? debug/tile_placer/pre_play_attempt1_PUGH.png
?? debug/tile_placer/pre_play_attempt1_QUIMS.png
?? debug/tile_placer/pre_play_attempt1_RANULAE.png
?? debug/tile_placer/pre_play_attempt1_SPOILAGE.png
?? debug/tile_placer/pre_play_attempt1_ST.png
?? debug/tile_placer/pre_play_attempt1_TAG.png
?? debug/tile_placer/pre_play_attempt1_TARGE.png
?? debug/tile_placer/pre_play_attempt1_TIN.png
?? debug/tile_placer/pre_play_attempt1_TOLA.png
?? debug/tile_placer/pre_play_attempt1_TOWELING.png
?? debug/tile_placer/pre_play_attempt1_TOWERED.png
?? debug/tile_placer/pre_play_attempt1_TREW.png
?? debug/tile_placer/pre_play_attempt1_TUNNAGE.png
?? debug/tile_placer/pre_play_attempt1_UNREEL.png
?? debug/tile_placer/pre_play_attempt1_VALID.png
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
?? debug/tile_placer/pre_play_attempt2_ANENT.png
?? debug/tile_placer/pre_play_attempt2_AVE.png
?? debug/tile_placer/pre_play_attempt2_AXITE.png
?? debug/tile_placer/pre_play_attempt2_BORDEL.png
?? debug/tile_placer/pre_play_attempt2_BRIEFS.png
?? debug/tile_placer/pre_play_attempt2_CANULAE.png
?? debug/tile_placer/pre_play_attempt2_CARIBE.png
?? debug/tile_placer/pre_play_attempt2_CAULKED.png
?? debug/tile_placer/pre_play_attempt2_COZ.png
?? debug/tile_placer/pre_play_attempt2_DI.png
?? debug/tile_placer/pre_play_attempt2_DIF.png
?? debug/tile_placer/pre_play_attempt2_DITTY.png
?? debug/tile_placer/pre_play_attempt2_DOGGO.png
?? debug/tile_placer/pre_play_attempt2_EEL.png
?? debug/tile_placer/pre_play_attempt2_ENE.png
?? debug/tile_placer/pre_play_attempt2_FET.png
?? debug/tile_placer/pre_play_attempt2_FEW.png
?? debug/tile_placer/pre_play_attempt2_FLAUTA.png
?? debug/tile_placer/pre_play_attempt2_FLIT.png
?? debug/tile_placer/pre_play_attempt2_FUGU.png
?? debug/tile_placer/pre_play_attempt2_FUGUE.png
?? debug/tile_placer/pre_play_attempt2_GASOLINE.png
?? debug/tile_placer/pre_play_attempt2_GAZON.png
?? debug/tile_placer/pre_play_attempt2_GLOAT.png
?? debug/tile_placer/pre_play_attempt2_GOOLD.png
?? debug/tile_placer/pre_play_attempt2_GULPH.png
?? debug/tile_placer/pre_play_attempt2_GURNET.png
?? debug/tile_placer/pre_play_attempt2_HAULINGS.png
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
?? debug/tile_placer/pre_play_attempt2_LID.png
?? debug/tile_placer/pre_play_attempt2_LIFT.png
?? debug/tile_placer/pre_play_attempt2_LIG.png
?? debug/tile_placer/pre_play_attempt2_LOG.png
?? debug/tile_placer/pre_play_attempt2_LOTA.png
?? debug/tile_placer/pre_play_attempt2_MOZO.png
?? debug/tile_placer/pre_play_attempt2_NABI.png
?? debug/tile_placer/pre_play_attempt2_NENE.png
?? debug/tile_placer/pre_play_attempt2_NIB.png
?? debug/tile_placer/pre_play_attempt2_NIGHED.png
?? debug/tile_placer/pre_play_attempt2_NILGHAU.png
?? debug/tile_placer/pre_play_attempt2_NOGG.png
?? debug/tile_placer/pre_play_attempt2_NY.png
?? debug/tile_placer/pre_play_attempt2_ORAD.png
?? debug/tile_placer/pre_play_attempt2_OUTVIE.png
?? debug/tile_placer/pre_play_attempt2_POZ.png
?? debug/tile_placer/pre_play_attempt2_RUGGY.png
?? debug/tile_placer/pre_play_attempt2_SILAGE.png
?? debug/tile_placer/pre_play_attempt2_TAJINE.png
?? debug/tile_placer/pre_play_attempt2_TEF.png
?? debug/tile_placer/pre_play_attempt2_TO.png
?? debug/tile_placer/pre_play_attempt2_TOFU.png
?? debug/tile_placer/pre_play_attempt2_TOWNLET.png
?? debug/tile_placer/pre_play_attempt2_TOXINS.png
?? debug/tile_placer/pre_play_attempt2_TREF.png
?? debug/tile_placer/pre_play_attempt2_UNABLE.png
?? debug/tile_placer/pre_play_attempt2_UNRATE.png
?? debug/tile_placer/pre_play_attempt2_VELETA.png
?? debug/tile_placer/pre_play_attempt2_WINGLET.png
?? debug/tile_placer/pre_play_attempt2_YAGI.png
?? debug/tile_placer/pre_play_attempt2_YEZ.png
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
?? debug/tile_placer/pre_play_attempt3_DIV.png
?? debug/tile_placer/pre_play_attempt3_ENDUE.png
?? debug/tile_placer/pre_play_attempt3_EXEAT.png
?? debug/tile_placer/pre_play_attempt3_FAKE.png
?? debug/tile_placer/pre_play_attempt3_FAUCAL.png
?? debug/tile_placer/pre_play_attempt3_FEH.png
?? debug/tile_placer/pre_play_attempt3_FER.png
?? debug/tile_placer/pre_play_attempt3_FID.png
?? debug/tile_placer/pre_play_attempt3_FRUG.png
?? debug/tile_placer/pre_play_attempt3_FUG.png
?? debug/tile_placer/pre_play_attempt3_FUN.png
?? debug/tile_placer/pre_play_attempt3_FUR.png
?? debug/tile_placer/pre_play_attempt3_GEL.png
?? debug/tile_placer/pre_play_attempt3_GI.png
?? debug/tile_placer/pre_play_attempt3_GID.png
?? debug/tile_placer/pre_play_attempt3_GLAIVES.png
?? debug/tile_placer/pre_play_attempt3_GOALIES.png
?? debug/tile_placer/pre_play_attempt3_GOOGOL.png
?? debug/tile_placer/pre_play_attempt3_GOOLD.png
?? debug/tile_placer/pre_play_attempt3_GRACKLE.png
?? debug/tile_placer/pre_play_attempt3_HANGUL.png
?? debug/tile_placer/pre_play_attempt3_HIELD.png
?? debug/tile_placer/pre_play_attempt3_JOEY.png
?? debug/tile_placer/pre_play_attempt3_KRONA.png
?? debug/tile_placer/pre_play_attempt3_LACUNA.png
?? debug/tile_placer/pre_play_attempt3_LANDAU.png
?? debug/tile_placer/pre_play_attempt3_LEADINGS.png
?? debug/tile_placer/pre_play_attempt3_LEE.png
?? debug/tile_placer/pre_play_attempt3_LEK.png
?? debug/tile_placer/pre_play_attempt3_LEUGH.png
?? debug/tile_placer/pre_play_attempt3_LOD.png
?? debug/tile_placer/pre_play_attempt3_LOTO.png
?? debug/tile_placer/pre_play_attempt3_NABI.png
?? debug/tile_placer/pre_play_attempt3_NEG.png
?? debug/tile_placer/pre_play_attempt3_NOT.png
?? debug/tile_placer/pre_play_attempt3_NUDGE.png
?? debug/tile_placer/pre_play_attempt3_OF.png
?? debug/tile_placer/pre_play_attempt3_OUTVIE.png
?? debug/tile_placer/pre_play_attempt3_PORTAGE.png
?? debug/tile_placer/pre_play_attempt3_POZ.png
?? debug/tile_placer/pre_play_attempt3_QI.png
?? debug/tile_placer/pre_play_attempt3_REW.png
?? debug/tile_placer/pre_play_attempt3_ROAD.png
?? debug/tile_placer/pre_play_attempt3_RUNNEL.png
?? debug/tile_placer/pre_play_attempt3_SHAULING.png
?? debug/tile_placer/pre_play_attempt3_SOZ.png
?? debug/tile_placer/pre_play_attempt3_TAJ.png
?? debug/tile_placer/pre_play_attempt3_TOWNLET.png
?? debug/tile_placer/pre_play_attempt3_TOXIN.png
?? debug/tile_placer/pre_play_attempt3_ULNAE.png
?? debug/tile_placer/pre_play_attempt3_UNRENT.png
?? debug/tile_placer/pre_play_attempt3_VIE.png
?? debug/tile_placer/pre_play_attempt3_VIFDA.png
?? debug/tile_placer/pre_play_attempt3_WELTING.png
?? debug/tile_placer/pre_play_attempt3_WOF.png
?? debug/tile_placer/pre_play_attempt3_YAD.png
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
?? debug/tile_placer/pre_play_attempt4_DAY.png
?? debug/tile_placer/pre_play_attempt4_DOL.png
?? debug/tile_placer/pre_play_attempt4_DOR.png
?? debug/tile_placer/pre_play_attempt4_DOTAL.png
?? debug/tile_placer/pre_play_attempt4_FAUNAL.png
?? debug/tile_placer/pre_play_attempt4_FIL.png
?? debug/tile_placer/pre_play_attempt4_FROW.png
?? debug/tile_placer/pre_play_attempt4_FURY.png
?? debug/tile_placer/pre_play_attempt4_GAK.png
?? debug/tile_placer/pre_play_attempt4_GILD.png
?? debug/tile_placer/pre_play_attempt4_GLOWER.png
?? debug/tile_placer/pre_play_attempt4_GOLD.png
?? debug/tile_placer/pre_play_attempt4_GONG.png
?? debug/tile_placer/pre_play_attempt4_GOOLD.png
?? debug/tile_placer/pre_play_attempt4_HANGI.png
?? debug/tile_placer/pre_play_attempt4_HELE.png
?? debug/tile_placer/pre_play_attempt4_IF.png
?? debug/tile_placer/pre_play_attempt4_JAILED.png
?? debug/tile_placer/pre_play_attempt4_KEEF.png
?? debug/tile_placer/pre_play_attempt4_LACUNAE.png
?? debug/tile_placer/pre_play_attempt4_LAGUNE.png
?? debug/tile_placer/pre_play_attempt4_LANGUE.png
?? debug/tile_placer/pre_play_attempt4_LEU.png
?? debug/tile_placer/pre_play_attempt4_LINGA.png
?? debug/tile_placer/pre_play_attempt4_LIT.png
?? debug/tile_placer/pre_play_attempt4_LONGIES.png
?? debug/tile_placer/pre_play_attempt4_LUCKED.png
?? debug/tile_placer/pre_play_attempt4_MOZO.png
?? debug/tile_placer/pre_play_attempt4_NEAT.png
?? debug/tile_placer/pre_play_attempt4_NUBIA.png
?? debug/tile_placer/pre_play_attempt4_OUTVIE.png
?? debug/tile_placer/pre_play_attempt4_PORTAGE.png
?? debug/tile_placer/pre_play_attempt4_PROVENLY.png
?? debug/tile_placer/pre_play_attempt4_RACIER.png
?? debug/tile_placer/pre_play_attempt4_REF.png
?? debug/tile_placer/pre_play_attempt4_TERGA.png
?? debug/tile_placer/pre_play_attempt4_TON.png
?? debug/tile_placer/pre_play_attempt4_TURF.png
?? debug/tile_placer/pre_play_attempt4_TURK.png
?? debug/tile_placer/pre_play_attempt4_UNDEE.png
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
?? debug/tile_placer/pre_play_attempt5_AGE.png
?? debug/tile_placer/pre_play_attempt5_AREIC.png
?? debug/tile_placer/pre_play_attempt5_AZO.png
?? debug/tile_placer/pre_play_attempt5_BARIC.png
?? debug/tile_placer/pre_play_attempt5_BI.png
?? debug/tile_placer/pre_play_attempt5_BITTY.png
?? debug/tile_placer/pre_play_attempt5_CARLE.png
?? debug/tile_placer/pre_play_attempt5_DIT.png
?? debug/tile_placer/pre_play_attempt5_EA.png
?? debug/tile_placer/pre_play_attempt5_ETNA.png
?? debug/tile_placer/pre_play_attempt5_EVITE.png
?? debug/tile_placer/pre_play_attempt5_FACULA.png
?? debug/tile_placer/pre_play_attempt5_FANGO.png
?? debug/tile_placer/pre_play_attempt5_FEG.png
?? debug/tile_placer/pre_play_attempt5_FEU.png
?? debug/tile_placer/pre_play_attempt5_FON.png
?? debug/tile_placer/pre_play_attempt5_GALOOT.png
?? debug/tile_placer/pre_play_attempt5_GILT.png
?? debug/tile_placer/pre_play_attempt5_GLID.png
?? debug/tile_placer/pre_play_attempt5_GOD.png
?? debug/tile_placer/pre_play_attempt5_GOLD.png
?? debug/tile_placer/pre_play_attempt5_GREW.png
?? debug/tile_placer/pre_play_attempt5_HETE.png
?? debug/tile_placer/pre_play_attempt5_JOINED.png
?? debug/tile_placer/pre_play_attempt5_KEEF.png
?? debug/tile_placer/pre_play_attempt5_LACKED.png
?? debug/tile_placer/pre_play_attempt5_LAGUNA.png
?? debug/tile_placer/pre_play_attempt5_LANATE.png
?? debug/tile_placer/pre_play_attempt5_LAUGHING.png
?? debug/tile_placer/pre_play_attempt5_LINGOES.png
?? debug/tile_placer/pre_play_attempt5_LINGUA.png
?? debug/tile_placer/pre_play_attempt5_LUNGI.png
?? debug/tile_placer/pre_play_attempt5_NAB.png
?? debug/tile_placer/pre_play_attempt5_NABI.png
?? debug/tile_placer/pre_play_attempt5_NIB.png
?? debug/tile_placer/pre_play_attempt5_NOWL.png
?? debug/tile_placer/pre_play_attempt5_NY.png
?? debug/tile_placer/pre_play_attempt5_OUTVIE.png
?? debug/tile_placer/pre_play_attempt5_REFT.png
?? debug/tile_placer/pre_play_attempt5_TEW.png
?? debug/tile_placer/pre_play_attempt5_TIDY.png
?? debug/tile_placer/pre_play_attempt5_TOGA.png
?? debug/tile_placer/pre_play_attempt5_VID.png
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
?? debug/turn_detection/frame_20260428_144214_795442_pre_start_attempt1.png
?? debug/turn_detection/frame_20260428_151327_322704_pre_start_attempt1.png
?? debug/turn_detection/frame_20260428_160630_875022_pre_start_attempt1.png
?? logs/
?? scripts/auto_debug.py
?? scripts/autoplay_headless.py
?? src/engine/rejected_words.py
```

## git diff --stat
```
debug/preprocessed_debug.png               | Bin 371628 -> 378979 bytes
 debug/tile_placer/post_recall_attempt1.png | Bin 117178 -> 119462 bytes
 debug/tile_placer/post_recall_attempt2.png | Bin 120237 -> 119294 bytes
 debug/tile_placer/post_recall_attempt3.png | Bin 119929 -> 118487 bytes
 debug/tile_placer/post_recall_attempt4.png | Bin 119657 -> 119380 bytes
 debug/tile_placer/post_recall_attempt5.png | Bin 120024 -> 119569 bytes
 src/bot/autoplay_cog.py                    |  39 +++-
 src/browser/capture.py                     |  92 +++++++-
 src/browser/navigator.py                   |  17 +-
 src/browser/tile_placer.py                 | 340 +++++++++++++++++++++++++----
 src/browser/turn_detector.py               | 192 +++++++++++++++-
 src/vision/__init__.py                     | 152 ++++++++++---
 tests/test_tile_placer.py                  |  79 ++++++-
 13 files changed, 800 insertions(+), 111 deletions(-)
```