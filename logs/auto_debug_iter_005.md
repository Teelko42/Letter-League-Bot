# Auto-debug iteration 5

- exit_code: `0`
- duration: 1746.0s
- error_signature: `a8752ce119c8`

## Recent debug artifacts
- `debug/tile_placer/post_recall_attempt5.png`
- `debug/tile_placer/pre_play_attempt5_HETE.png`
- `debug/tile_placer/post_recall_attempt4.png`
- `debug/turn_detection/frame_20260428_151327_322704_pre_start_attempt1.png`
- `debug/preprocessed_debug.png`

## Autoplay log — error region
```
2026-04-28 15:33:03.637 | INFO    | src.vision:extract_board_state:187 | Extraction complete (retry)
2026-04-28 15:33:03.638 | DEBUG   | src.vision:_log_extracted_state:40 | Vision extracted 0 cells
2026-04-28 15:33:03.639 | INFO    | src.vision:extract_board_state:205 | Merged 8 cell(s) from first attempt that retry dropped: [('N', 8, 12), ('A', 8, 13), ('Y', 8, 14), ('N', 10, 12), ('A', 10, 13), ('W', 10, 14), ('A', 10, 15), ('B', 10, 16)]
2026-04-28 15:33:03.640 | INFO    | src.vision:extract_board_state:234 | Validation result after retry — 10 error(s)
2026-04-28 15:33:03.641 | WARNING | __main__:_run:187 | Vision attempt 2 failed: [VALIDATION_FAILED] Validation failed after retry: Floating tile 'N' at (8, 12) — not connected to other tiles; Floating tile 'A' at (8, 13) — not connected to other tiles; Floating tile 'Y' at (8, 14) — not connected to other tiles; Invalid rack tile ' L'; Invalid rack tile ' F'; Invalid rack tile ' D'; Invalid rack tile ' V'; Invalid rack tile ' G'; Invalid rack tile ' T'; Invalid rack tile ' I'
2026-04-28 15:33:03.642 | ERROR   | __main__:_run:202 | Vision failed twice — skipping turn
2026-04-28 15:33:07.215 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120771 bytes (attempt 1)
2026-04-28 15:33:07.330 | INFO    | src.browser.turn_detector:poll_turn:648 | Turn state changed: None -> my_turn
2026-04-28 15:33:07.458 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 15:33:08.432 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119928 bytes (attempt 1)
2026-04-28 15:33:09.711 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120239 bytes (attempt 1)
2026-04-28 15:33:09.714 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1287.6, 749.3) (pass 1/10)
2026-04-28 15:33:11.627 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120540 bytes (attempt 1)
2026-04-28 15:33:11.752 | INFO    | src.browser.tile_placer:clear_stale_placements:955 | Pre-turn recall click at (1283.7, 748.2) (pass 2/10)
2026-04-28 15:33:13.705 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120515 bytes (attempt 1)
2026-04-28 15:33:13.832 | INFO    | src.browser.tile_placer:clear_stale_placements:973 | Pre-turn recall complete after 2 click(s) — canvas stable
2026-04-28 15:33:17.360 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120333 bytes (attempt 1)
2026-04-28 15:33:17.361 | INFO    | src.vision:extract_board_state:125 | Vision pipeline start — mode=wild
2026-04-28 15:33:17.400 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,54) 1366×657 from 1545×768 canvas
2026-04-28 15:33:17.640 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-04-28 15:33:17.760 | INFO    | src.vision:extract_board_state:131 | Preprocessing complete — 378995 bytes
2026-04-28 15:33:17.761 | INFO    | src.vision.extractor:call_vision_api:95 | Calling Claude Vision API — retry=False
2026-04-28 15:33:23.134 | INFO    | src.vision.extractor:call_vision_api:149 | Claude Vision response received — latency=5.37s  input_tokens=2903  output_tokens=254
2026-04-28 15:33:23.134 | INFO    | src.vision:extract_board_state:137 | Extraction complete (first attempt)
2026-04-28 15:33:23.135 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (7,12)=N[TL] (7,13)=A*[DL] (7,14)=Y[TL] (9,12)=N[DW] (9,13)=A[DL] (9,14)=W[DW] (9,15)=A[DL] (9,16)=B[DW]
```

## Subprocess stderr (tail)
```
[32m15:37:45[0m | [1mINFO   [0m | Clicking recall button at (1283.6, 748.7) (pass 2/10)
[32m15:37:48[0m | [1mINFO   [0m | Clicking recall button at (1287.2, 751.5) (pass 3/10)
[32m15:37:50[0m | [1mINFO   [0m | Clicking recall button at (1286.7, 750.1) (pass 4/10)
[32m15:37:52[0m | [1mINFO   [0m | Clicking recall button at (1285.1, 748.8) (pass 5/10)
[32m15:37:54[0m | [1mINFO   [0m | Clicking recall button at (1286.8, 751.8) (pass 6/10)
[32m15:37:56[0m | [1mINFO   [0m | Recall complete after 6 click(s) — canvas stable
[32m15:37:57[0m | [1mINFO   [0m | Word attempt 3/5: 'FEH' (score=39)
[32m15:37:57[0m | [1mINFO   [0m | Placing tile 'F' (slot 1) -> board (5,9) | src=(1035.5,830.9) dst=(941.4,357.1)
[32m15:38:01[0m | [1mINFO   [0m | Tile 'F' verified at (5,9)
[32m15:38:01[0m | [1mINFO   [0m | Placing tile 'E' (slot 0) -> board (5,10) | src=(981.0,828.3) dst=(993.8,354.7)
[32m15:38:04[0m | [1mINFO   [0m | Tile 'E' verified at (5,10)
[32m15:38:05[0m | [1mINFO   [0m | Placing tile 'H' (slot 5) -> board (5,11) | src=(1254.0,828.0) dst=(1042.9,355.4)
[32m15:38:07[0m | [1mINFO   [0m | Tile 'H' verified at (5,11)
[32m15:38:09[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.5, 750.5)
[32m15:38:11[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.2, 752.7)
[32m15:38:16[0m | [1mINFO   [0m | Word 'FEH' rejected (attempt 3/5) — recalling tiles
[32m15:38:16[0m | [1mINFO   [0m | Blacklisted rejected word 'feh' (total: 199)
[32m15:38:18[0m | [1mINFO   [0m | Clicking recall button at (1283.8, 751.1) (pass 1/10)
[32m15:38:20[0m | [1mINFO   [0m | Clicking recall button at (1283.1, 750.9) (pass 2/10)
[32m15:38:23[0m | [1mINFO   [0m | Clicking recall button at (1285.0, 748.1) (pass 3/10)
[32m15:38:28[0m | [1mINFO   [0m | Clicking recall button at (1285.9, 752.7) (pass 4/10)
[32m15:38:30[0m | [1mINFO   [0m | Clicking recall button at (1282.8, 751.9) (pass 5/10)
[32m15:38:32[0m | [1mINFO   [0m | Clicking recall button at (1284.3, 749.2) (pass 6/10)
[32m15:38:34[0m | [1mINFO   [0m | Clicking recall button at (1283.3, 752.3) (pass 7/10)
[32m15:38:37[0m | [1mINFO   [0m | Clicking recall button at (1284.8, 751.6) (pass 8/10)
[32m15:38:40[0m | [1mINFO   [0m | Clicking recall button at (1287.7, 748.4) (pass 9/10)
[32m15:38:42[0m | [1mINFO   [0m | Clicking recall button at (1286.1, 750.7) (pass 10/10)
[32m15:38:44[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m15:38:45[0m | [1mINFO   [0m | Word attempt 4/5: 'HELE' (score=39)
[32m15:38:45[0m | [1mINFO   [0m | Placing tile 'H' (slot 5) -> board (7,9) | src=(1256.7,828.5) dst=(941.9,427.4)
[32m15:38:49[0m | [1mINFO   [0m | Tile 'H' verified at (7,9)
[32m15:38:49[0m | [1mINFO   [0m | Placing tile 'E' (slot 0) -> board (7,10) | src=(977.7,830.5) dst=(991.7,426.2)
[32m15:38:53[0m | [1mINFO   [0m | Tile 'E' verified at (7,10)
[32m15:38:53[0m | [1mINFO   [0m | Placing tile 'L' (slot 3) -> board (7,11) | src=(1144.8,828.5) dst=(1047.7,425.4)
[32m15:38:56[0m | [1mINFO   [0m | Tile 'L' verified at (7,11)
[32m15:38:57[0m | [1mINFO   [0m | Placing tile 'E' (slot 6) -> board (7,12) | src=(1312.2,831.3) dst=(1094.0,427.6)
[32m15:39:00[0m | [33m[1mWARNING[0m | Tile 'E' placement not verified — retrying with fresh jitter
[32m15:39:03[0m | [1mINFO   [0m | Tile 'E' verified at (7,12)
[32m15:39:05[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1145.5, 753.6)
[32m15:39:07[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1145.5, 753.7)
[32m15:39:11[0m | [1mINFO   [0m | Word 'HELE' rejected (attempt 4/5) — recalling tiles
[32m15:39:11[0m | [1mINFO   [0m | Blacklisted rejected word 'hele' (total: 200)
[32m15:39:12[0m | [1mINFO   [0m | Clicking recall button at (1283.5, 753.3) (pass 1/10)
[32m15:39:16[0m | [1mINFO   [0m | Clicking recall button at (1284.3, 753.4) (pass 2/10)
[32m15:39:18[0m | [1mINFO   [0m | Clicking recall button at (1284.0, 748.4) (pass 3/10)
[32m15:39:20[0m | [1mINFO   [0m | Clicking recall button at (1288.5, 751.1) (pass 4/10)
[32m15:39:23[0m | [1mINFO   [0m | Clicking recall button at (1286.3, 749.7) (pass 5/10)
[32m15:39:25[0m | [1mINFO   [0m | Clicking recall button at (1287.7, 752.8) (pass 6/10)
[32m15:39:28[0m | [1mINFO   [0m | Clicking recall button at (1284.4, 753.6) (pass 7/10)
[32m15:39:30[0m | [1mINFO   [0m | Clicking recall button at (1285.1, 750.2) (pass 8/10)
[32m15:39:33[0m | [1mINFO   [0m | Clicking recall button at (1286.7, 751.5) (pass 9/10)
[32m15:39:35[0m | [1mINFO   [0m | Clicking recall button at (1285.8, 749.2) (pass 10/10)
[32m15:39:37[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m15:39:38[0m | [1mINFO   [0m | Word attempt 5/5: 'HETE' (score=36)
[32m15:39:38[0m | [1mINFO   [0m | Placing tile 'H' (slot 5) -> board (7,9) | src=(1255.4,831.3) dst=(944.4,427.0)
[32m15:39:42[0m | [1mINFO   [0m | Tile 'H' verified at (7,9)
[32m15:39:43[0m | [1mINFO   [0m | Placing tile 'E' (slot 0) -> board (7,10) | src=(977.4,828.0) dst=(996.9,427.1)
[32m15:39:47[0m | [1mINFO   [0m | Tile 'E' verified at (7,10)
[32m15:39:48[0m | [1mINFO   [0m | Placing tile 'T' (slot 2) -> board (7,11) | src=(1091.3,828.3) dst=(1043.8,423.2)
[32m15:39:50[0m | [1mINFO   [0m | Tile 'T' verified at (7,11)
[32m15:39:51[0m | [1mINFO   [0m | Placing tile 'E' (slot 6) -> board (7,12) | src=(1309.5,828.4) dst=(1094.2,423.3)
[32m15:39:54[0m | [1mINFO   [0m | Tile 'E' verified at (7,12)
[32m15:39:56[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.8, 748.5)
[32m15:39:58[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.1, 749.9)
[32m15:40:01[0m | [1mINFO   [0m | Word 'HETE' rejected (attempt 5/5) — recalling tiles
[32m15:40:01[0m | [1mINFO   [0m | Blacklisted rejected word 'hete' (total: 201)
[32m15:40:02[0m | [1mINFO   [0m | Clicking recall button at (1284.3, 752.5) (pass 1/10)
[32m15:40:05[0m | [1mINFO   [0m | Clicking recall button at (1283.9, 750.9) (pass 2/10)
[32m15:40:07[0m | [1mINFO   [0m | Clicking recall button at (1286.3, 751.4) (pass 3/10)
[32m15:40:10[0m | [1mINFO   [0m | Clicking recall button at (1287.7, 753.5) (pass 4/10)
[32m15:40:12[0m | [1mINFO   [0m | Clicking recall button at (1285.2, 751.8) (pass 5/10)
[32m15:40:14[0m | [1mINFO   [0m | Clicking recall button at (1287.7, 751.0) (pass 6/10)
[32m15:40:17[0m | [1mINFO   [0m | Clicking recall button at (1288.5, 748.8) (pass 7/10)
[32m15:40:19[0m | [1mINFO   [0m | Clicking recall button at (1287.5, 749.1) (pass 8/10)
[32m15:40:21[0m | [1mINFO   [0m | Recall complete after 8 click(s) — canvas stable
[32m15:40:23[0m | [33m[1mWARNING[0m | All 5 word attempt(s) failed — performing tile swap fallback
[32m15:40:23[0m | [33m[1mWARNING[0m | Falling back to tile swap at (1010.3, 748.2) — no valid words accepted after 5 attempts
[32m15:40:23[0m | [1mINFO   [0m | Turn 5: no move accepted (swap/skip)
[32m15:40:23[0m | [1mINFO   [0m | Reached max_turns=5 — exiting cleanly
[32m15:40:23[0m | [1mINFO   [0m | Headless autoplay finished in 1728.2s
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
?? debug/tile_placer/pre_play_attempt1_QUIMS.png
?? debug/tile_placer/pre_play_attempt1_RANULAE.png
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
?? debug/tile_placer/pre_play_attempt2_GAZON.png
?? debug/tile_placer/pre_play_attempt2_GLOAT.png
?? debug/tile_placer/pre_play_attempt2_GOOLD.png
?? debug/tile_placer/pre_play_attempt2_GURNET.png
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
?? debug/tile_placer/pre_play_attempt2_UNRATE.png
?? debug/tile_placer/pre_play_attempt2_VELETA.png
?? debug/tile_placer/pre_play_attempt2_WINGLET.png
?? debug/tile_placer/pre_play_attempt2_YAGI.png
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
?? debug/tile_placer/pre_play_attempt3_GOOGOL.png
?? debug/tile_placer/pre_play_attempt3_GOOLD.png
?? debug/tile_placer/pre_play_attempt3_GRACKLE.png
?? debug/tile_placer/pre_play_attempt3_HIELD.png
?? debug/tile_placer/pre_play_attempt3_JOEY.png
?? debug/tile_placer/pre_play_attempt3_KRONA.png
?? debug/tile_placer/pre_play_attempt3_LACUNA.png
?? debug/tile_placer/pre_play_attempt3_LANDAU.png
?? debug/tile_placer/pre_play_attempt3_LEE.png
?? debug/tile_placer/pre_play_attempt3_LEK.png
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
?? debug/tile_placer/pre_play_attempt4_HELE.png
?? debug/tile_placer/pre_play_attempt4_IF.png
?? debug/tile_placer/pre_play_attempt4_JAILED.png
?? debug/tile_placer/pre_play_attempt4_KEEF.png
?? debug/tile_placer/pre_play_attempt4_LACUNAE.png
?? debug/tile_placer/pre_play_attempt4_LAGUNE.png
?? debug/tile_placer/pre_play_attempt4_LANGUE.png
?? debug/tile_placer/pre_play_attempt4_LEU.png
?? debug/tile_placer/pre_play_attempt4_LIT.png
?? debug/tile_placer/pre_play_attempt4_LUCKED.png
?? debug/tile_placer/pre_play_attempt4_MOZO.png
?? debug/tile_placer/pre_play_attempt4_NEAT.png
?? debug/tile_placer/pre_play_attempt4_NUBIA.png
?? debug/tile_placer/pre_play_attempt4_OUTVIE.png
?? debug/tile_placer/pre_play_attempt4_PORTAGE.png
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
?? logs/
?? scripts/auto_debug.py
?? scripts/autoplay_headless.py
?? src/engine/rejected_words.py
```

## git diff --stat
```
debug/preprocessed_debug.png               | Bin 371628 -> 377689 bytes
 debug/tile_placer/post_recall_attempt1.png | Bin 117178 -> 118984 bytes
 debug/tile_placer/post_recall_attempt2.png | Bin 120237 -> 119798 bytes
 debug/tile_placer/post_recall_attempt3.png | Bin 119929 -> 120132 bytes
 debug/tile_placer/post_recall_attempt4.png | Bin 119657 -> 120041 bytes
 debug/tile_placer/post_recall_attempt5.png | Bin 120024 -> 119268 bytes
 src/bot/autoplay_cog.py                    |  39 +++-
 src/browser/capture.py                     |  92 +++++++-
 src/browser/navigator.py                   |  17 +-
 src/browser/tile_placer.py                 | 340 +++++++++++++++++++++++++----
 src/browser/turn_detector.py               | 192 +++++++++++++++-
 src/vision/__init__.py                     | 127 ++++++++---
 tests/test_tile_placer.py                  |  79 ++++++-
 13 files changed, 775 insertions(+), 111 deletions(-)
```