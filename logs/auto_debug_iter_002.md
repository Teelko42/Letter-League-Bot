# Auto-debug iteration 2

- exit_code: `-9`
- duration: 1800.4s
- error_signature: `61a2bd105ecd`

## Recent debug artifacts
- `debug/tile_placer/pre_play_attempt2_TOFU.png`
- `debug/tile_placer/post_recall_attempt1.png`
- `debug/tile_placer/pre_play_attempt1_FOUR.png`
- `debug/turn_detection/frame_20260428_113826_776417_pre_start_attempt1.png`
- `debug/preprocessed_debug.png`

## Autoplay log — error region
```
2026-04-28 11:41:56.568 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.1360
2026-04-28 11:41:56.569 | WARNING | src.browser.tile_placer:place_tiles:699 | Tile 'F' placement not verified — retrying with fresh jitter
2026-04-28 11:41:57.379 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 109827 bytes (attempt 1)
2026-04-28 11:41:59.244 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110155 bytes (attempt 1)
2026-04-28 11:41:59.368 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.0639
2026-04-28 11:41:59.370 | ERROR   | src.browser.tile_placer:place_move:1074 | Tile placement failed for 'GOWF' (attempt 3): Tile 'F' at (11,15) failed to place after retry
2026-04-28 11:41:59.546 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x731 @ (375,149)
2026-04-28 11:42:00.946 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 110433 bytes (attempt 1)
2026-04-28 11:42:00.947 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.2, 785.2) (pass 1/10)
2026-04-28 11:42:03.180 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108201 bytes (attempt 1)
2026-04-28 11:42:03.336 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.6, 785.9) (pass 2/10)
2026-04-28 11:42:07.807 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107898 bytes (attempt 1)
2026-04-28 11:42:08.161 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.1, 789.7) (pass 3/10)
2026-04-28 11:42:10.424 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 107370 bytes (attempt 1)
2026-04-28 11:42:10.574 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1287.6, 789.3) (pass 4/10)
2026-04-28 11:42:12.486 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108399 bytes (attempt 1)
2026-04-28 11:42:12.715 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1284.2, 789.4) (pass 5/10)
2026-04-28 11:42:14.793 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108269 bytes (attempt 1)
2026-04-28 11:42:14.921 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1286.8, 786.6) (pass 6/10)
2026-04-28 11:42:17.039 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108418 bytes (attempt 1)
2026-04-28 11:42:17.159 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1282.6, 790.1) (pass 7/10)
2026-04-28 11:42:19.266 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108069 bytes (attempt 1)
2026-04-28 11:42:19.506 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1285.5, 789.8) (pass 8/10)
2026-04-28 11:42:21.522 | DEBUG   | src.browser.capture:capture_canvas:134 | Game screenshot captured — 108041 bytes (attempt 1)
2026-04-28 11:42:21.652 | INFO    | src.browser.tile_placer:_recall_tiles:881 | Clicking recall button at (1283.5, 786.1) (pass 9/10)
```

## Subprocess stderr (tail)
```
[32m12:05:00[0m | [1mINFO   [0m | Clicking recall button at (1285.4, 790.5) (pass 2/10)
[32m12:05:02[0m | [1mINFO   [0m | Clicking recall button at (1284.4, 788.7) (pass 3/10)
[32m12:05:04[0m | [1mINFO   [0m | Clicking recall button at (1286.5, 785.5) (pass 4/10)
[32m12:05:06[0m | [1mINFO   [0m | Recall complete after 4 click(s) — canvas stable
[32m12:05:08[0m | [1mINFO   [0m | Word attempt 5/5: 'WOG' (score=14)
[32m12:05:08[0m | [1mINFO   [0m | Placing tile 'W' (slot 0) -> board (8,15) | src=(979.1,833.5) dst=(1244.3,481.2)
[32m12:05:11[0m | [1mINFO   [0m | Tile 'W' verified at (8,15)
[32m12:05:12[0m | [1mINFO   [0m | Placing tile 'G' (slot 5) -> board (10,15) | src=(1256.3,831.1) dst=(1248.2,547.7)
[32m12:05:15[0m | [1mINFO   [0m | Tile 'G' verified at (10,15)
[32m12:05:16[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1145.5, 788.6)
[32m12:05:18[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.9, 789.1)
[32m12:05:21[0m | [1mINFO   [0m | Word 'WOG' rejected (attempt 5/5) — recalling tiles
[32m12:05:21[0m | [1mINFO   [0m | Blacklisted rejected word 'wog' (total: 126)
[32m12:05:22[0m | [1mINFO   [0m | Clicking recall button at (1282.9, 788.7) (pass 1/10)
[32m12:05:24[0m | [1mINFO   [0m | Clicking recall button at (1287.2, 785.8) (pass 2/10)
[32m12:05:26[0m | [1mINFO   [0m | Clicking recall button at (1287.6, 786.2) (pass 3/10)
[32m12:05:28[0m | [1mINFO   [0m | Clicking recall button at (1284.1, 788.6) (pass 4/10)
[32m12:05:30[0m | [1mINFO   [0m | Clicking recall button at (1285.2, 787.1) (pass 5/10)
[32m12:05:32[0m | [1mINFO   [0m | Clicking recall button at (1286.1, 785.7) (pass 6/10)
[32m12:05:34[0m | [1mINFO   [0m | Recall complete after 6 click(s) — canvas stable
[32m12:05:35[0m | [33m[1mWARNING[0m | All 5 word attempt(s) failed — returning to caller for re-vision
[32m12:05:35[0m | [33m[1mWARNING[0m | No move accepted (candidates=5) — re-vision + swap fallback
[32m12:05:38[0m | [1mINFO   [0m | Vision pipeline start — mode=wild
[32m12:05:39[0m | [1mINFO   [0m | Preprocessing complete — 329265 bytes
[32m12:05:39[0m | [1mINFO   [0m | Calling Claude Vision API — retry=False
[32m12:05:43[0m | [1mINFO   [0m | Claude Vision response received — latency=4.54s  input_tokens=2905  output_tokens=179
[32m12:05:43[0m | [1mINFO   [0m | Extraction complete (first attempt)
[32m12:05:43[0m | [1mINFO   [0m | Validation result — 1 error(s)
[32m12:05:43[0m | [33m[1mWARNING[0m | Validation failed (1 errors), retrying: ['Position accuracy suspect: 5/5 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m12:05:43[0m | [1mINFO   [0m | Calling Claude Vision API — retry=True
[32m12:05:50[0m | [1mINFO   [0m | Claude Vision response received — latency=6.35s  input_tokens=2960  output_tokens=181
[32m12:05:50[0m | [1mINFO   [0m | Extraction complete (retry)
[32m12:05:50[0m | [1mINFO   [0m | Validation result after retry — 1 error(s)
[32m12:05:50[0m | [33m[1mWARNING[0m | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 5/5 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m12:05:50[0m | [1mINFO   [0m | Vision pipeline complete — 11.30s  tiles=5  rack_size=7
[32m12:05:50[0m | [1mINFO   [0m | Word attempt 1/5: 'FOUR' (score=14)
[32m12:05:50[0m | [1mINFO   [0m | Placing tile 'F' (slot 6) -> board (8,15) | src=(1311.5,831.5) dst=(1249.3,482.2)
[32m12:05:53[0m | [1mINFO   [0m | Tile 'F' verified at (8,15)
[32m12:05:53[0m | [1mINFO   [0m | Placing tile 'U' (slot 1) -> board (10,15) | src=(1035.3,832.4) dst=(1247.0,549.2)
[32m12:05:57[0m | [1mINFO   [0m | Tile 'U' verified at (10,15)
[32m12:05:57[0m | [1mINFO   [0m | Placing tile 'R' (slot 3) -> board (11,15) | src=(1147.5,828.8) dst=(1247.3,580.2)
[32m12:06:00[0m | [1mINFO   [0m | Tile 'R' verified at (11,15)
[32m12:06:02[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1145.6, 787.4)
[32m12:06:03[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.2, 787.9)
[32m12:06:06[0m | [1mINFO   [0m | Word 'FOUR' rejected (attempt 1/5) — recalling tiles
[32m12:06:06[0m | [1mINFO   [0m | Blacklisted rejected word 'four' (total: 127)
[32m12:06:07[0m | [1mINFO   [0m | Clicking recall button at (1285.7, 788.2) (pass 1/10)
[32m12:06:10[0m | [1mINFO   [0m | Clicking recall button at (1284.9, 785.8) (pass 2/10)
[32m12:06:12[0m | [1mINFO   [0m | Clicking recall button at (1287.6, 787.0) (pass 3/10)
[32m12:06:14[0m | [1mINFO   [0m | Clicking recall button at (1285.6, 785.9) (pass 4/10)
[32m12:06:16[0m | [1mINFO   [0m | Clicking recall button at (1285.4, 790.6) (pass 5/10)
[32m12:06:18[0m | [1mINFO   [0m | Clicking recall button at (1287.5, 785.2) (pass 6/10)
[32m12:06:20[0m | [1mINFO   [0m | Clicking recall button at (1285.2, 787.9) (pass 7/10)
[32m12:06:22[0m | [1mINFO   [0m | Clicking recall button at (1283.0, 786.4) (pass 8/10)
[32m12:06:24[0m | [1mINFO   [0m | Clicking recall button at (1287.0, 788.4) (pass 9/10)
[32m12:06:26[0m | [1mINFO   [0m | Clicking recall button at (1287.6, 788.9) (pass 10/10)
[32m12:06:28[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m12:06:29[0m | [1mINFO   [0m | Word attempt 2/5: 'TOFU' (score=14)
[32m12:06:30[0m | [1mINFO   [0m | Placing tile 'T' (slot 2) -> board (8,15) | src=(1088.4,830.8) dst=(1246.3,478.1)
[32m12:06:32[0m | [1mINFO   [0m | Tile 'T' verified at (8,15)
[32m12:06:33[0m | [1mINFO   [0m | Placing tile 'F' (slot 6) -> board (10,15) | src=(1311.3,831.5) dst=(1245.3,549.2)
[32m12:06:36[0m | [1mINFO   [0m | Tile 'F' verified at (10,15)
[32m12:06:37[0m | [1mINFO   [0m | Placing tile 'U' (slot 1) -> board (11,15) | src=(1033.6,831.1) dst=(1247.3,577.0)
[32m12:06:39[0m | [1mINFO   [0m | Tile 'U' verified at (11,15)
[32m12:06:41[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1144.6, 789.2)
[32m12:06:42[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1145.2, 785.8)
[32m12:06:46[0m | [1mINFO   [0m | Word 'TOFU' rejected (attempt 2/5) — recalling tiles
[32m12:06:46[0m | [1mINFO   [0m | Blacklisted rejected word 'tofu' (total: 128)
[32m12:06:47[0m | [1mINFO   [0m | Clicking recall button at (1285.9, 789.4) (pass 1/10)
[32m12:06:49[0m | [1mINFO   [0m | Clicking recall button at (1286.4, 788.7) (pass 2/10)
[32m12:06:51[0m | [1mINFO   [0m | Clicking recall button at (1286.1, 790.4) (pass 3/10)
[32m12:06:53[0m | [1mINFO   [0m | Clicking recall button at (1288.0, 787.8) (pass 4/10)
[32m12:06:55[0m | [1mINFO   [0m | Clicking recall button at (1283.5, 790.7) (pass 5/10)
[32m12:06:57[0m | [1mINFO   [0m | Clicking recall button at (1287.6, 789.8) (pass 6/10)
[32m12:06:59[0m | [1mINFO   [0m | Clicking recall button at (1288.4, 787.8) (pass 7/10)
[32m12:07:01[0m | [1mINFO   [0m | Clicking recall button at (1285.9, 790.5) (pass 8/10)
[32m12:07:03[0m | [1mINFO   [0m | Clicking recall button at (1287.7, 785.1) (pass 9/10)
[32m12:07:05[0m | [1mINFO   [0m | Clicking recall button at (1282.8, 785.9) (pass 10/10)

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
?? debug/tile_placer/pre_play_attempt1_FOUR.png
?? debug/tile_placer/pre_play_attempt1_FROG.png
?? debug/tile_placer/pre_play_attempt1_FUTURE.png
?? debug/tile_placer/pre_play_attempt1_GINZO.png
?? debug/tile_placer/pre_play_attempt1_GOOD.png
?? debug/tile_placer/pre_play_attempt1_GOOGOL.png
?? debug/tile_placer/pre_play_attempt1_GOOLD.png
?? debug/tile_placer/pre_play_attempt1_GOWF.png
?? debug/tile_placer/pre_play_attempt1_GROW.png
?? debug/tile_placer/pre_play_attempt1_HINGED.png
?? debug/tile_placer/pre_play_attempt1_ID.png
?? debug/tile_placer/pre_play_attempt1_JIAO.png
?? debug/tile_placer/pre_play_attempt1_JOEY.png
?? debug/tile_placer/pre_play_attempt1_JOINT.png
?? debug/tile_placer/pre_play_attempt1_JOINTS.png
?? debug/tile_placer/pre_play_attempt1_KENDO.png
?? debug/tile_placer/pre_play_attempt1_KURU.png
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
?? debug/tile_placer/pre_play_attempt2_KUTU.png
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
?? debug/tile_placer/pre_play_attempt3_EXEAT.png
?? debug/tile_placer/pre_play_attempt3_FAKE.png
?? debug/tile_placer/pre_play_attempt3_FAUCAL.png
?? debug/tile_placer/pre_play_attempt3_FER.png
?? debug/tile_placer/pre_play_attempt3_FRUG.png
?? debug/tile_placer/pre_play_attempt3_FUG.png
?? debug/tile_placer/pre_play_attempt3_FUR.png
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
?? debug/tile_placer/pre_play_attempt4_CARIBE.png
?? debug/tile_placer/pre_play_attempt4_CERIA.png
?? debug/tile_placer/pre_play_attempt4_DOL.png
?? debug/tile_placer/pre_play_attempt4_DOR.png
?? debug/tile_placer/pre_play_attempt4_DOTAL.png
?? debug/tile_placer/pre_play_attempt4_FAUNAL.png
?? debug/tile_placer/pre_play_attempt4_FROW.png
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
?? debug/tile_placer/pre_play_attempt5_AREIC.png
?? debug/tile_placer/pre_play_attempt5_AZO.png
?? debug/tile_placer/pre_play_attempt5_BARIC.png
?? debug/tile_placer/pre_play_attempt5_BI.png
?? debug/tile_placer/pre_play_attempt5_BITTY.png
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
?? logs/
?? scripts/auto_debug.py
?? scripts/autoplay_headless.py
?? src/engine/rejected_words.py
```

## git diff --stat
```
debug/preprocessed_debug.png               | Bin 371628 -> 329265 bytes
 debug/tile_placer/post_recall_attempt1.png | Bin 117178 -> 115223 bytes
 debug/tile_placer/post_recall_attempt2.png | Bin 120237 -> 115288 bytes
 debug/tile_placer/post_recall_attempt3.png | Bin 119929 -> 116233 bytes
 debug/tile_placer/post_recall_attempt4.png | Bin 119657 -> 106908 bytes
 debug/tile_placer/post_recall_attempt5.png | Bin 120024 -> 114962 bytes
 src/bot/autoplay_cog.py                    |  39 +++-
 src/browser/capture.py                     |  71 +++++-
 src/browser/tile_placer.py                 | 340 +++++++++++++++++++++++++----
 src/browser/turn_detector.py               | 192 +++++++++++++++-
 src/vision/__init__.py                     | 127 ++++++++---
 tests/test_tile_placer.py                  |  79 ++++++-
 12 files changed, 740 insertions(+), 108 deletions(-)
```