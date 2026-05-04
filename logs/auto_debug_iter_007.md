# Auto-debug iteration 7

- exit_code: `0`
- duration: 1439.0s
- error_signature: `dec71d3cf183`

## Recent debug artifacts
- `debug/tile_placer/post_recall_attempt5.png`
- `debug/tile_placer/pre_play_attempt5_EQUID.png`
- `debug/tile_placer/post_recall_attempt4.png`
- `debug/turn_detection/frame_20260428_164116_835181_pre_start_attempt1.png`
- `debug/preprocessed_debug.png`

## Autoplay log — error region
```
2026-04-28 16:45:43.519 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.0635
2026-04-28 16:45:43.520 | WARNING | src.browser.tile_placer:place_tiles:703 | Tile 'O' placement not verified — retrying with fresh jitter
2026-04-28 16:45:46.202 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121088 bytes (attempt 1)
2026-04-28 16:45:49.384 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120611 bytes (attempt 1)
2026-04-28 16:45:50.248 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.0728
2026-04-28 16:45:50.249 | ERROR   | src.browser.tile_placer:place_move:1078 | Tile placement failed for 'BODGE' (attempt 4): Tile 'O' at (8,16) failed to place after retry
2026-04-28 16:45:50.458 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:45:51.362 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120611 bytes (attempt 1)
2026-04-28 16:45:51.364 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1283.9, 751.6) (pass 1/10)
2026-04-28 16:45:53.502 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119798 bytes (attempt 1)
2026-04-28 16:45:53.710 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1283.2, 750.5) (pass 2/10)
2026-04-28 16:45:56.572 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119339 bytes (attempt 1)
2026-04-28 16:45:56.730 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1284.1, 750.9) (pass 3/10)
2026-04-28 16:46:00.444 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119056 bytes (attempt 1)
2026-04-28 16:46:00.631 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1285.9, 751.1) (pass 4/10)
2026-04-28 16:46:02.667 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119795 bytes (attempt 1)
2026-04-28 16:46:02.816 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1286.8, 748.2) (pass 5/10)
2026-04-28 16:46:04.927 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119381 bytes (attempt 1)
2026-04-28 16:46:05.255 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1284.5, 750.6) (pass 6/10)
2026-04-28 16:46:07.158 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 117812 bytes (attempt 1)
2026-04-28 16:46:07.330 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1287.8, 750.9) (pass 7/10)
2026-04-28 16:46:09.300 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118673 bytes (attempt 1)
2026-04-28 16:46:09.492 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1283.2, 752.8) (pass 8/10)
2026-04-28 16:46:11.618 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118468 bytes (attempt 1)
2026-04-28 16:46:11.839 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1286.2, 751.0) (pass 9/10)
2026-04-28 16:46:14.148 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118467 bytes (attempt 1)
2026-04-28 16:46:14.316 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1283.7, 753.8) (pass 10/10)
2026-04-28 16:46:16.698 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118493 bytes (attempt 1)
2026-04-28 16:46:16.848 | WARNING | src.browser.tile_placer:_recall_tiles:903 | Recall hit cap (10 clicks) without stabilising
2026-04-28 16:46:17.857 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 117764 bytes (attempt 1)
2026-04-28 16:46:17.861 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:849 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt4.png
2026-04-28 16:46:17.862 | INFO    | src.browser.tile_placer:place_move:1067 | Word attempt 5/5: 'GAMBADE' (score=30)
2026-04-28 16:46:17.999 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:46:18.000 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'G' (slot 1) -> board (4,16) | src=(1037.4,826.1) dst=(1300.4,321.4)
2026-04-28 16:46:18.930 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118147 bytes (attempt 1)
2026-04-28 16:46:20.925 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119793 bytes (attempt 1)
2026-04-28 16:46:21.110 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.6616
2026-04-28 16:46:21.111 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'G' verified at (4,16)
2026-04-28 16:46:21.732 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'A' (slot 3) -> board (5,16) | src=(1148.6,827.1) dst=(1296.0,353.8)
2026-04-28 16:46:22.661 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120398 bytes (attempt 1)
2026-04-28 16:46:24.559 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120959 bytes (attempt 1)
2026-04-28 16:46:24.707 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.1972
2026-04-28 16:46:24.707 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'A' verified at (5,16)
2026-04-28 16:46:25.311 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'M' (slot 2) -> board (6,16) | src=(1088.8,826.5) dst=(1299.5,390.0)
2026-04-28 16:46:26.233 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120928 bytes (attempt 1)
2026-04-28 16:46:28.039 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119837 bytes (attempt 1)
2026-04-28 16:46:28.190 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.5522
2026-04-28 16:46:28.190 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'M' verified at (6,16)
2026-04-28 16:46:28.652 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'B' (slot 5) -> board (7,16) | src=(1257.0,826.1) dst=(1299.8,427.4)
2026-04-28 16:46:29.610 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119706 bytes (attempt 1)
2026-04-28 16:46:31.472 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120580 bytes (attempt 1)
2026-04-28 16:46:31.624 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.8158
2026-04-28 16:46:31.625 | INFO    | src.browser.tile_placer:place_tiles:730 | Tile 'B' verified at (7,16)
2026-04-28 16:46:32.297 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'A' (slot 4) -> board (8,16) | src=(1200.6,827.3) dst=(1299.8,461.5)
2026-04-28 16:46:33.223 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121100 bytes (attempt 1)
2026-04-28 16:46:35.126 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121543 bytes (attempt 1)
2026-04-28 16:46:35.283 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.0649
2026-04-28 16:46:35.284 | WARNING | src.browser.tile_placer:place_tiles:703 | Tile 'A' placement not verified — retrying with fresh jitter
2026-04-28 16:46:36.310 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121117 bytes (attempt 1)
2026-04-28 16:46:38.420 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121444 bytes (attempt 1)
2026-04-28 16:46:38.619 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.0600
2026-04-28 16:46:38.619 | ERROR   | src.browser.tile_placer:place_move:1078 | Tile placement failed for 'GAMBADE' (attempt 5): Tile 'A' at (8,16) failed to place after retry
2026-04-28 16:46:38.856 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 16:46:39.965 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120330 bytes (attempt 1)
2026-04-28 16:46:39.966 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1286.5, 750.3) (pass 1/10)
2026-04-28 16:46:41.989 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118614 bytes (attempt 1)
2026-04-28 16:46:42.157 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1283.5, 751.9) (pass 2/10)
2026-04-28 16:46:45.344 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119164 bytes (attempt 1)
2026-04-28 16:46:46.355 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1288.0, 749.0) (pass 3/10)
2026-04-28 16:46:49.434 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119138 bytes (attempt 1)
2026-04-28 16:46:49.724 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1285.8, 749.5) (pass 4/10)
2026-04-28 16:46:52.829 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118867 bytes (attempt 1)
2026-04-28 16:46:53.125 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1283.8, 748.1) (pass 5/10)
2026-04-28 16:46:54.855 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118274 bytes (attempt 1)
2026-04-28 16:46:54.927 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1288.5, 751.3) (pass 6/10)
2026-04-28 16:46:56.572 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119000 bytes (attempt 1)
2026-04-28 16:46:56.637 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1283.0, 753.4) (pass 7/10)
2026-04-28 16:46:58.311 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118271 bytes (attempt 1)
2026-04-28 16:46:58.386 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1287.5, 749.8) (pass 8/10)
2026-04-28 16:47:00.162 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 118710 bytes (attempt 1)
2026-04-28 16:47:00.220 | INFO    | src.browser.tile_placer:_recall_tiles:885 | Clicking recall button at (1287.0, 749.5) (pass 9/10)
```

## Subprocess stderr (tail)
```
[32m17:01:56[0m | [1mINFO   [0m | Blacklisted rejected word 'zoeae' (total: 245)
[32m17:01:57[0m | [1mINFO   [0m | Clicking recall button at (1287.5, 748.9) (pass 1/10)
[32m17:01:59[0m | [1mINFO   [0m | Clicking recall button at (1287.4, 751.9) (pass 2/10)
[32m17:02:02[0m | [1mINFO   [0m | Clicking recall button at (1283.6, 750.7) (pass 3/10)
[32m17:02:04[0m | [1mINFO   [0m | Clicking recall button at (1283.0, 751.9) (pass 4/10)
[32m17:02:07[0m | [1mINFO   [0m | Clicking recall button at (1283.5, 748.2) (pass 5/10)
[32m17:02:09[0m | [1mINFO   [0m | Clicking recall button at (1286.1, 753.1) (pass 6/10)
[32m17:02:11[0m | [1mINFO   [0m | Clicking recall button at (1287.4, 749.7) (pass 7/10)
[32m17:02:13[0m | [1mINFO   [0m | Clicking recall button at (1285.4, 750.1) (pass 8/10)
[32m17:02:16[0m | [1mINFO   [0m | Clicking recall button at (1287.7, 749.9) (pass 9/10)
[32m17:02:18[0m | [1mINFO   [0m | Clicking recall button at (1287.3, 750.7) (pass 10/10)
[32m17:02:20[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m17:02:21[0m | [1mINFO   [0m | Word attempt 3/5: 'ADOZE' (score=30)
[32m17:02:21[0m | [1mINFO   [0m | Placing tile 'A' (slot 1) -> board (8,16) | src=(1035.6,827.3) dst=(1298.2,459.4)
[32m17:02:24[0m | [1mINFO   [0m | Tile 'A' verified at (8,16)
[32m17:02:24[0m | [1mINFO   [0m | Placing tile 'O' (slot 3) -> board (10,16) | src=(1145.0,827.1) dst=(1300.1,529.0)
[32m17:02:28[0m | [1mINFO   [0m | Tile 'O' verified at (10,16)
[32m17:02:28[0m | [1mINFO   [0m | Placing tile 'Z' (slot 6) -> board (11,16) | src=(1313.4,826.2) dst=(1299.1,566.7)
[32m17:02:31[0m | [1mINFO   [0m | Tile 'Z' verified at (11,16)
[32m17:02:31[0m | [1mINFO   [0m | Placing tile 'E' (slot 0) -> board (12,16) | src=(979.1,829.2) dst=(1300.1,599.9)
[32m17:02:34[0m | [1mINFO   [0m | Tile 'E' verified at (12,16)
[32m17:02:36[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.2, 752.9)
[32m17:02:37[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1149.2, 752.2)
[32m17:02:41[0m | [1mINFO   [0m | Word 'ADOZE' rejected (attempt 3/5) — recalling tiles
[32m17:02:41[0m | [1mINFO   [0m | Blacklisted rejected word 'adoze' (total: 246)
[32m17:02:42[0m | [1mINFO   [0m | Clicking recall button at (1283.0, 750.8) (pass 1/10)
[32m17:02:43[0m | [1mINFO   [0m | Clicking recall button at (1283.1, 751.9) (pass 2/10)
[32m17:02:46[0m | [1mINFO   [0m | Clicking recall button at (1284.9, 751.0) (pass 3/10)
[32m17:02:48[0m | [1mINFO   [0m | Clicking recall button at (1283.6, 750.8) (pass 4/10)
[32m17:02:51[0m | [1mINFO   [0m | Clicking recall button at (1287.7, 749.3) (pass 5/10)
[32m17:02:53[0m | [1mINFO   [0m | Clicking recall button at (1282.7, 750.3) (pass 6/10)
[32m17:02:55[0m | [1mINFO   [0m | Clicking recall button at (1286.5, 753.6) (pass 7/10)
[32m17:02:58[0m | [1mINFO   [0m | Clicking recall button at (1288.6, 749.5) (pass 8/10)
[32m17:03:00[0m | [1mINFO   [0m | Clicking recall button at (1288.3, 750.6) (pass 9/10)
[32m17:03:03[0m | [1mINFO   [0m | Clicking recall button at (1282.7, 754.0) (pass 10/10)
[32m17:03:05[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m17:03:06[0m | [1mINFO   [0m | Word attempt 4/5: 'QUOAD' (score=30)
[32m17:03:06[0m | [1mINFO   [0m | Placing tile 'Q' (slot 5) -> board (5,16) | src=(1258.8,829.8) dst=(1295.5,359.2)
[32m17:03:09[0m | [1mINFO   [0m | Tile 'Q' verified at (5,16)
[32m17:03:09[0m | [1mINFO   [0m | Placing tile 'U' (slot 4) -> board (6,16) | src=(1201.4,829.9) dst=(1299.5,393.1)
[32m17:03:12[0m | [1mINFO   [0m | Tile 'U' verified at (6,16)
[32m17:03:13[0m | [1mINFO   [0m | Placing tile 'O' (slot 3) -> board (7,16) | src=(1145.5,828.4) dst=(1295.4,427.4)
[32m17:03:16[0m | [1mINFO   [0m | Tile 'O' verified at (7,16)
[32m17:03:16[0m | [1mINFO   [0m | Placing tile 'A' (slot 1) -> board (8,16) | src=(1034.7,827.6) dst=(1300.5,461.4)
[32m17:03:19[0m | [1mINFO   [0m | Tile 'A' verified at (8,16)
[32m17:03:20[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.4, 748.1)
[32m17:03:22[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.1, 748.4)
[32m17:03:25[0m | [1mINFO   [0m | Word 'QUOAD' rejected (attempt 4/5) — recalling tiles
[32m17:03:25[0m | [1mINFO   [0m | Blacklisted rejected word 'quoad' (total: 247)
[32m17:03:26[0m | [1mINFO   [0m | Clicking recall button at (1287.3, 751.2) (pass 1/10)
[32m17:03:28[0m | [1mINFO   [0m | Clicking recall button at (1284.8, 748.7) (pass 2/10)
[32m17:03:30[0m | [1mINFO   [0m | Clicking recall button at (1282.8, 749.4) (pass 3/10)
[32m17:03:32[0m | [1mINFO   [0m | Recall complete after 3 click(s) — canvas stable
[32m17:03:33[0m | [1mINFO   [0m | Word attempt 5/5: 'EQUID' (score=30)
[32m17:03:33[0m | [1mINFO   [0m | Placing tile 'E' (slot 0) -> board (5,16) | src=(978.9,828.7) dst=(1299.7,355.2)
[32m17:03:36[0m | [1mINFO   [0m | Tile 'E' verified at (5,16)
[32m17:03:36[0m | [1mINFO   [0m | Placing tile 'Q' (slot 5) -> board (6,16) | src=(1255.2,829.4) dst=(1299.6,393.3)
[32m17:03:40[0m | [1mINFO   [0m | Tile 'Q' verified at (6,16)
[32m17:03:40[0m | [1mINFO   [0m | Placing tile 'U' (slot 4) -> board (7,16) | src=(1201.7,831.1) dst=(1296.0,424.3)
[32m17:03:43[0m | [1mINFO   [0m | Tile 'U' verified at (7,16)
[32m17:03:44[0m | [1mINFO   [0m | Placing tile 'I' (slot 2) -> board (8,16) | src=(1090.9,826.9) dst=(1300.7,460.4)
[32m17:03:46[0m | [1mINFO   [0m | Tile 'I' verified at (8,16)
[32m17:03:48[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.2, 753.2)
[32m17:03:49[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.4, 749.3)
[32m17:03:53[0m | [1mINFO   [0m | Word 'EQUID' rejected (attempt 5/5) — recalling tiles
[32m17:03:53[0m | [1mINFO   [0m | Blacklisted rejected word 'equid' (total: 248)
[32m17:03:53[0m | [1mINFO   [0m | Clicking recall button at (1287.0, 748.4) (pass 1/10)
[32m17:03:55[0m | [1mINFO   [0m | Clicking recall button at (1285.6, 748.1) (pass 2/10)
[32m17:03:57[0m | [1mINFO   [0m | Clicking recall button at (1286.9, 750.1) (pass 3/10)
[32m17:03:59[0m | [1mINFO   [0m | Clicking recall button at (1285.2, 751.4) (pass 4/10)
[32m17:04:01[0m | [1mINFO   [0m | Clicking recall button at (1284.6, 753.6) (pass 5/10)
[32m17:04:03[0m | [1mINFO   [0m | Clicking recall button at (1284.4, 753.8) (pass 6/10)
[32m17:04:06[0m | [1mINFO   [0m | Clicking recall button at (1285.3, 752.3) (pass 7/10)
[32m17:04:08[0m | [1mINFO   [0m | Clicking recall button at (1287.8, 748.1) (pass 8/10)
[32m17:04:10[0m | [1mINFO   [0m | Recall complete after 8 click(s) — canvas stable
[32m17:04:11[0m | [33m[1mWARNING[0m | All 5 word attempt(s) failed — performing tile swap fallback
[32m17:04:11[0m | [33m[1mWARNING[0m | Falling back to tile swap at (1006.6, 752.4) — no valid words accepted after 5 attempts
[32m17:04:11[0m | [1mINFO   [0m | Turn 5: no move accepted (swap/skip)
[32m17:04:11[0m | [1mINFO   [0m | Reached max_turns=5 — exiting cleanly
[32m17:04:11[0m | [1mINFO   [0m | Headless autoplay finished in 1423.3s
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
?? debug/tile_placer/pre_play_attempt1_AMOEBA.png
?? debug/tile_placer/pre_play_attempt1_ANNUAL.png
?? debug/tile_placer/pre_play_attempt1_ANORAK.png
?? debug/tile_placer/pre_play_attempt1_ARABIC.png
?? debug/tile_placer/pre_play_attempt1_BEANY.png
?? debug/tile_placer/pre_play_attempt1_BIN.png
?? debug/tile_placer/pre_play_attempt1_BITTY.png
?? debug/tile_placer/pre_play_attempt1_BODEGA.png
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
?? debug/tile_placer/pre_play_attempt1_FIG.png
?? debug/tile_placer/pre_play_attempt1_FIQUE.png
?? debug/tile_placer/pre_play_attempt1_FIZ.png
?? debug/tile_placer/pre_play_attempt1_FLEET.png
?? debug/tile_placer/pre_play_attempt1_FOGIE.png
?? debug/tile_placer/pre_play_attempt1_FORKY.png
?? debug/tile_placer/pre_play_attempt1_FOUR.png
?? debug/tile_placer/pre_play_attempt1_FROG.png
?? debug/tile_placer/pre_play_attempt1_FUTURE.png
?? debug/tile_placer/pre_play_attempt1_FYCE.png
?? debug/tile_placer/pre_play_attempt1_GARNET.png
?? debug/tile_placer/pre_play_attempt1_GAUZIER.png
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
?? debug/tile_placer/pre_play_attempt1_OCHRED.png
?? debug/tile_placer/pre_play_attempt1_OI.png
?? debug/tile_placer/pre_play_attempt1_OUTVIE.png
?? debug/tile_placer/pre_play_attempt1_PIX.png
?? debug/tile_placer/pre_play_attempt1_PIXEL.png
?? debug/tile_placer/pre_play_attempt1_PODGIEST.png
?? debug/tile_placer/pre_play_attempt1_PORTAGE.png
?? debug/tile_placer/pre_play_attempt1_PROVEN.png
?? debug/tile_placer/pre_play_attempt1_PUGH.png
?? debug/tile_placer/pre_play_attempt1_QUIMS.png
?? debug/tile_placer/pre_play_attempt1_QUIZ.png
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
?? debug/tile_placer/pre_play_attempt2_AUF.png
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
?? debug/tile_placer/pre_play_attempt2_FOG.png
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
?? debug/tile_placer/pre_play_attempt2_MADGE.png
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
?? debug/tile_placer/pre_play_attempt2_QUOIF.png
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
?? debug/tile_placer/pre_play_attempt2_ZAIRE.png
?? debug/tile_placer/pre_play_attempt2_ZOEAE.png
?? debug/tile_placer/pre_play_attempt2_ZONING.png
?? debug/tile_placer/pre_play_attempt2_ZOOT.png
?? debug/tile_placer/pre_play_attempt3_ACARI.png
?? debug/tile_placer/pre_play_attempt3_ADOZE.png
?? debug/tile_placer/pre_play_attempt3_AGLOO.png
?? debug/tile_placer/pre_play_attempt3_ARABIC.png
?? debug/tile_placer/pre_play_attempt3_BADGE.png
?? debug/tile_placer/pre_play_attempt3_BEAN.png
?? debug/tile_placer/pre_play_attempt3_BI.png
?? debug/tile_placer/pre_play_attempt3_BIN.png
?? debug/tile_placer/pre_play_attempt3_BITTY.png
?? debug/tile_placer/pre_play_attempt3_BUNYA.png
?? debug/tile_placer/pre_play_attempt3_CALKED.png
?? debug/tile_placer/pre_play_attempt3_DIV.png
?? debug/tile_placer/pre_play_attempt3_ENDUE.png
?? debug/tile_placer/pre_play_attempt3_EXEAT.png
?? debug/tile_placer/pre_play_attempt3_FAG.png
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
?? debug/tile_placer/pre_play_attempt3_GHAZI.png
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
?? debug/tile_placer/pre_play_attempt3_OAF.png
?? debug/tile_placer/pre_play_attempt3_OF.png
?? debug/tile_placer/pre_play_attempt3_OUTVIE.png
?? debug/tile_placer/pre_play_attempt3_PORTAGE.png
?? debug/tile_placer/pre_play_attempt3_POZ.png
?? debug/tile_placer/pre_play_attempt3_QI.png
?? debug/tile_placer/pre_play_attempt3_REW.png
?? debug/tile_placer/pre_play_attempt3_ROAD.png
?? debug/tile_placer/pre_play_attempt3_ROQUE.png
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
?? debug/tile_placer/pre_play_attempt4_FIGO.png
?? debug/tile_placer/pre_play_attempt4_FIL.png
?? debug/tile_placer/pre_play_attempt4_FROW.png
?? debug/tile_placer/pre_play_attempt4_FURY.png
?? debug/tile_placer/pre_play_attempt4_GAK.png
?? debug/tile_placer/pre_play_attempt4_GEEZ.png
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
?? debug/tile_placer/pre_play_attempt4_QUOAD.png
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
?? debug/tile_placer/pre_play_attempt5_EQUID.png
?? debug/tile_placer/pre_play_attempt5_ETNA.png
?? debug/tile_placer/pre_play_attempt5_EVITE.png
?? debug/tile_placer/pre_play_attempt5_FACULA.png
?? debug/tile_placer/pre_play_attempt5_FANGO.png
?? debug/tile_placer/pre_play_attempt5_FEG.png
?? debug/tile_placer/pre_play_attempt5_FEU.png
?? debug/tile_placer/pre_play_attempt5_FON.png
?? debug/tile_placer/pre_play_attempt5_GALOOT.png
?? debug/tile_placer/pre_play_attempt5_GAUZE.png
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
?? debug/turn_detection/frame_20260428_164116_835181_pre_start_attempt1.png
?? logs/
?? scripts/auto_debug.py
?? scripts/autoplay_headless.py
?? src/engine/rejected_words.py
```

## git diff --stat
```
debug/preprocessed_debug.png               | Bin 371628 -> 391662 bytes
 debug/tile_placer/post_recall_attempt1.png | Bin 117178 -> 125791 bytes
 debug/tile_placer/post_recall_attempt2.png | Bin 120237 -> 125505 bytes
 debug/tile_placer/post_recall_attempt3.png | Bin 119929 -> 125990 bytes
 debug/tile_placer/post_recall_attempt4.png | Bin 119657 -> 125123 bytes
 debug/tile_placer/post_recall_attempt5.png | Bin 120024 -> 125274 bytes
 src/bot/autoplay_cog.py                    |  39 +++-
 src/browser/capture.py                     |  92 +++++++-
 src/browser/navigator.py                   |  17 +-
 src/browser/tile_placer.py                 | 354 +++++++++++++++++++++++++----
 src/browser/turn_detector.py               | 192 +++++++++++++++-
 src/vision/__init__.py                     | 152 ++++++++++---
 tests/test_tile_placer.py                  |  79 ++++++-
 13 files changed, 809 insertions(+), 116 deletions(-)
```