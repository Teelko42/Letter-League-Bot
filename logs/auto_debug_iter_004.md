# Auto-debug iteration 4

- exit_code: `0`
- duration: 1283.3s
- error_signature: `53b2dd5bd30a`

## Recent debug artifacts
- `debug/tile_placer/pre_play_attempt3_RUNNEL.png`
- `debug/tile_placer/post_recall_attempt2.png`
- `debug/tile_placer/pre_play_attempt2_ENE.png`
- `debug/turn_detection/frame_20260428_144214_795442_pre_start_attempt1.png`
- `debug/preprocessed_debug.png`

## Autoplay log — error region
```
2026-04-28 15:02:07.259 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 2) -> board (11,16) | src=(1090.9,828.6) dst=(1296.5,561.6)
2026-04-28 15:02:08.099 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120913 bytes (attempt 1)
2026-04-28 15:02:11.044 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121107 bytes (attempt 1)
2026-04-28 15:02:11.244 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3605
2026-04-28 15:02:11.248 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (11,16)
2026-04-28 15:02:11.655 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'N' (slot 3) -> board (12,16) | src=(1143.1,830.8) dst=(1296.3,597.9)
2026-04-28 15:02:12.571 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121484 bytes (attempt 1)
2026-04-28 15:02:14.675 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122286 bytes (attempt 1)
2026-04-28 15:02:14.786 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.6460
2026-04-28 15:02:14.787 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'N' verified at (12,16)
2026-04-28 15:02:15.298 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'E' (slot 1) -> board (13,16) | src=(1037.2,828.9) dst=(1297.9,630.9)
2026-04-28 15:02:16.497 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121635 bytes (attempt 1)
2026-04-28 15:02:18.579 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 125393 bytes (attempt 1)
2026-04-28 15:02:18.931 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 1.4254
2026-04-28 15:02:18.932 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'E' verified at (13,16)
2026-04-28 15:02:19.550 | INFO    | src.browser.tile_placer:place_tiles:678 | Placing tile 'L' (slot 0) -> board (14,16) | src=(979.3,827.1) dst=(1299.4,665.8)
2026-04-28 15:02:20.510 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122561 bytes (attempt 1)
2026-04-28 15:02:22.517 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 123317 bytes (attempt 1)
2026-04-28 15:02:22.652 | DEBUG   | src.browser.tile_placer:_verify_placement:624 | Placement pixel diff: 0.3361
2026-04-28 15:02:22.653 | INFO    | src.browser.tile_placer:place_tiles:726 | Tile 'L' verified at (14,16)
2026-04-28 15:02:23.654 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122459 bytes (attempt 1)
2026-04-28 15:02:23.662 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:845 | Debug screenshot saved -> debug\tile_placer\pre_play_attempt3_RUNNEL.png
2026-04-28 15:02:24.578 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 15:02:24.579 | INFO    | src.browser.tile_placer:_click_confirm:795 | Clicking confirm/PLAY button at (1149.1, 750.6)
2026-04-28 15:02:26.161 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 112083 bytes (attempt 1)
2026-04-28 15:02:26.273 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:820 | Post-confirm poll 1/3: not_my_turn
2026-04-28 15:02:26.273 | INFO    | src.browser.tile_placer:place_move:1102 | Word 'RUNNEL' accepted! (score=18, attempt 3/3)
2026-04-28 15:02:26.274 | INFO    | __main__:_run:267 | Turn 5: played 'RUNNEL' (score=18)
2026-04-28 15:02:26.275 | INFO    | __main__:_run:151 | Reached max_turns=5 — exiting cleanly
2026-04-28 15:02:26.798 | INFO    | __main__:main:300 | Headless autoplay finished in 1266.9s
```

## Subprocess stderr (tail)
```
[32m15:00:13[0m | [1mINFO   [0m | Claude Vision response received — latency=6.10s  input_tokens=2903  output_tokens=281
[32m15:00:13[0m | [1mINFO   [0m | Extraction complete (first attempt)
[32m15:00:13[0m | [1mINFO   [0m | Validation result — 4 error(s)
[32m15:00:13[0m | [33m[1mWARNING[0m | Validation failed (4 errors), retrying: ["Floating tile 'T' at (7, 11) — not connected to other tiles", "Floating tile 'A' at (7, 12) — not connected to other tiles", "Floating tile 'G' at (7, 13) — not connected to other tiles", 'Position accuracy suspect: 7/9 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m15:00:13[0m | [1mINFO   [0m | Calling Claude Vision API — retry=True
[32m15:00:30[0m | [1mINFO   [0m | Claude Vision response received — latency=17.18s  input_tokens=3021  output_tokens=449
[32m15:00:30[0m | [1mINFO   [0m | Extraction complete (retry)
[32m15:00:30[0m | [1mINFO   [0m | Merged 1 cell(s) from first attempt that retry dropped: [('T', 7, 11)]
[32m15:00:30[0m | [1mINFO   [0m | Validation result after retry — 7 error(s)
[32m15:00:30[0m | [33m[1mWARNING[0m | Vision attempt 1 failed: [VALIDATION_FAILED] Validation failed after retry: Invalid letter ' T' at (7, 12); Floating tile 'T' at (7, 11) — not connected to other tiles; Floating tile ' T' at (7, 12) — not connected to other tiles; Floating tile 'A' at (7, 13) — not connected to other tiles; Floating tile 'G' at (7, 14) — not connected to other tiles; Position accuracy suspect: 8/9 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.; Invalid word(s) on board: 'T TAG' at row 7 cols 11-14 — tile positions are likely off by 1. Re-count carefully from center star at (9,13).
[32m15:00:34[0m | [1mINFO   [0m | Vision pipeline start — mode=wild
[32m15:00:34[0m | [1mINFO   [0m | Preprocessing complete — 379387 bytes
[32m15:00:34[0m | [1mINFO   [0m | Calling Claude Vision API — retry=False
[32m15:00:39[0m | [1mINFO   [0m | Claude Vision response received — latency=5.22s  input_tokens=2903  output_tokens=280
[32m15:00:39[0m | [1mINFO   [0m | Extraction complete (first attempt)
[32m15:00:39[0m | [1mINFO   [0m | Validation result — 4 error(s)
[32m15:00:39[0m | [33m[1mWARNING[0m | Validation failed (4 errors), retrying: ["Floating tile 'T' at (7, 11) — not connected to other tiles", "Floating tile 'A' at (7, 12) — not connected to other tiles", "Floating tile 'G' at (7, 13) — not connected to other tiles", 'Position accuracy suspect: 7/9 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m15:00:39[0m | [1mINFO   [0m | Calling Claude Vision API — retry=True
[32m15:00:47[0m | [1mINFO   [0m | Claude Vision response received — latency=7.22s  input_tokens=3021  output_tokens=279
[32m15:00:47[0m | [1mINFO   [0m | Extraction complete (retry)
[32m15:00:47[0m | [1mINFO   [0m | Validation result after retry — 4 error(s)
[32m15:00:47[0m | [33m[1mWARNING[0m | Removed 3 floating tile(s) to salvage extraction
[32m15:00:47[0m | [33m[1mWARNING[0m | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 7/9 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m15:00:47[0m | [1mINFO   [0m | Vision pipeline complete — 13.14s  tiles=6  rack_size=7
[32m15:00:47[0m | [1mINFO   [0m | Word attempt 1/3: 'EEN' (score=20)
[32m15:00:47[0m | [1mINFO   [0m | Placing tile 'E' (slot 1) -> board (10,12) | src=(1033.6,830.4) dst=(1095.9,531.1)
[32m15:00:51[0m | [1mINFO   [0m | Tile 'E' verified at (10,12)
[32m15:00:51[0m | [1mINFO   [0m | Placing tile 'E' (slot 4) -> board (10,13) | src=(1204.2,827.7) dst=(1149.0,527.9)
[32m15:00:55[0m | [1mINFO   [0m | Tile 'E' verified at (10,13)
[32m15:00:55[0m | [1mINFO   [0m | Placing tile 'N' (slot 2) -> board (10,14) | src=(1088.2,831.1) dst=(1198.9,530.1)
[32m15:00:59[0m | [1mINFO   [0m | Tile 'N' verified at (10,14)
[32m15:01:00[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.6, 751.1)
[32m15:01:02[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1145.3, 753.0)
[32m15:01:05[0m | [1mINFO   [0m | Word 'EEN' rejected (attempt 1/3) — recalling tiles
[32m15:01:05[0m | [1mINFO   [0m | Blacklisted rejected word 'een' (total: 170)
[32m15:01:06[0m | [1mINFO   [0m | Clicking recall button at (1285.7, 753.8) (pass 1/10)
[32m15:01:08[0m | [1mINFO   [0m | Clicking recall button at (1284.2, 748.4) (pass 2/10)
[32m15:01:10[0m | [1mINFO   [0m | Clicking recall button at (1284.5, 753.3) (pass 3/10)
[32m15:01:12[0m | [1mINFO   [0m | Clicking recall button at (1283.5, 753.1) (pass 4/10)
[32m15:01:14[0m | [1mINFO   [0m | Clicking recall button at (1284.0, 752.2) (pass 5/10)
[32m15:01:17[0m | [1mINFO   [0m | Clicking recall button at (1286.8, 750.0) (pass 6/10)
[32m15:01:19[0m | [1mINFO   [0m | Recall complete after 6 click(s) — canvas stable
[32m15:01:19[0m | [1mINFO   [0m | Word attempt 2/3: 'ENE' (score=20)
[32m15:01:19[0m | [1mINFO   [0m | Placing tile 'E' (slot 1) -> board (8,11) | src=(1035.2,826.7) dst=(1046.8,457.6)
[32m15:01:22[0m | [1mINFO   [0m | Tile 'E' verified at (8,11)
[32m15:01:23[0m | [1mINFO   [0m | Placing tile 'N' (slot 2) -> board (8,12) | src=(1089.8,828.8) dst=(1097.1,461.4)
[32m15:01:25[0m | [1mINFO   [0m | Tile 'N' verified at (8,12)
[32m15:01:26[0m | [1mINFO   [0m | Placing tile 'E' (slot 4) -> board (8,13) | src=(1203.7,827.2) dst=(1148.7,460.2)
[32m15:01:29[0m | [1mINFO   [0m | Tile 'E' verified at (8,13)
[32m15:01:30[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1148.0, 750.9)
[32m15:01:32[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1148.0, 751.9)
[32m15:01:35[0m | [1mINFO   [0m | Word 'ENE' rejected (attempt 2/3) — recalling tiles
[32m15:01:35[0m | [1mINFO   [0m | Blacklisted rejected word 'ene' (total: 171)
[32m15:01:38[0m | [1mINFO   [0m | Clicking recall button at (1286.8, 749.5) (pass 1/10)
[32m15:01:41[0m | [1mINFO   [0m | Clicking recall button at (1286.8, 752.8) (pass 2/10)
[32m15:01:43[0m | [1mINFO   [0m | Clicking recall button at (1287.0, 749.5) (pass 3/10)
[32m15:01:45[0m | [1mINFO   [0m | Clicking recall button at (1283.3, 749.1) (pass 4/10)
[32m15:01:47[0m | [1mINFO   [0m | Clicking recall button at (1285.7, 749.4) (pass 5/10)
[32m15:01:49[0m | [1mINFO   [0m | Clicking recall button at (1287.1, 753.1) (pass 6/10)
[32m15:01:52[0m | [1mINFO   [0m | Clicking recall button at (1285.9, 748.6) (pass 7/10)
[32m15:01:54[0m | [1mINFO   [0m | Clicking recall button at (1285.7, 748.9) (pass 8/10)
[32m15:01:56[0m | [1mINFO   [0m | Clicking recall button at (1286.3, 751.3) (pass 9/10)
[32m15:01:58[0m | [1mINFO   [0m | Clicking recall button at (1282.8, 748.2) (pass 10/10)
[32m15:02:01[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m15:02:03[0m | [1mINFO   [0m | Word attempt 3/3: 'RUNNEL' (score=18)
[32m15:02:03[0m | [1mINFO   [0m | Placing tile 'U' (slot 6) -> board (10,16) | src=(1314.4,827.3) dst=(1296.0,530.7)
[32m15:02:06[0m | [1mINFO   [0m | Tile 'U' verified at (10,16)
[32m15:02:07[0m | [1mINFO   [0m | Placing tile 'N' (slot 2) -> board (11,16) | src=(1090.9,828.6) dst=(1296.5,561.6)
[32m15:02:11[0m | [1mINFO   [0m | Tile 'N' verified at (11,16)
[32m15:02:11[0m | [1mINFO   [0m | Placing tile 'N' (slot 3) -> board (12,16) | src=(1143.1,830.8) dst=(1296.3,597.9)
[32m15:02:14[0m | [1mINFO   [0m | Tile 'N' verified at (12,16)
[32m15:02:15[0m | [1mINFO   [0m | Placing tile 'E' (slot 1) -> board (13,16) | src=(1037.2,828.9) dst=(1297.9,630.9)
[32m15:02:18[0m | [1mINFO   [0m | Tile 'E' verified at (13,16)
[32m15:02:19[0m | [1mINFO   [0m | Placing tile 'L' (slot 0) -> board (14,16) | src=(979.3,827.1) dst=(1299.4,665.8)
[32m15:02:22[0m | [1mINFO   [0m | Tile 'L' verified at (14,16)
[32m15:02:24[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1149.1, 750.6)
[32m15:02:26[0m | [1mINFO   [0m | Word 'RUNNEL' accepted! (score=18, attempt 3/3)
[32m15:02:26[0m | [1mINFO   [0m | Turn 5: played 'RUNNEL' (score=18)
[32m15:02:26[0m | [1mINFO   [0m | Reached max_turns=5 — exiting cleanly
[32m15:02:26[0m | [1mINFO   [0m | Headless autoplay finished in 1266.9s
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
?? debug/tile_placer/pre_play_attempt1_DOG.png
?? debug/tile_placer/pre_play_attempt1_EEN.png
?? debug/tile_placer/pre_play_attempt1_EL.png
?? debug/tile_placer/pre_play_attempt1_FAKE.png
?? debug/tile_placer/pre_play_attempt1_FIBERS.png
?? debug/tile_placer/pre_play_attempt1_FIZ.png
?? debug/tile_placer/pre_play_attempt1_FORKY.png
?? debug/tile_placer/pre_play_attempt1_FOUR.png
?? debug/tile_placer/pre_play_attempt1_FROG.png
?? debug/tile_placer/pre_play_attempt1_FUTURE.png
?? debug/tile_placer/pre_play_attempt1_FYCE.png
?? debug/tile_placer/pre_play_attempt1_GARNET.png
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
?? debug/tile_placer/pre_play_attempt2_DITTY.png
?? debug/tile_placer/pre_play_attempt2_DOGGO.png
?? debug/tile_placer/pre_play_attempt2_EEL.png
?? debug/tile_placer/pre_play_attempt2_ENE.png
?? debug/tile_placer/pre_play_attempt2_FET.png
?? debug/tile_placer/pre_play_attempt2_FEW.png
?? debug/tile_placer/pre_play_attempt2_FLAUTA.png
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
?? debug/tile_placer/pre_play_attempt3_ENDUE.png
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
?? debug/tile_placer/pre_play_attempt4_LEU.png
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
?? debug/tile_placer/pre_play_attempt5_EA.png
?? debug/tile_placer/pre_play_attempt5_ETNA.png
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
?? debug/turn_detection/frame_20260428_144214_795442_pre_start_attempt1.png
?? logs/
?? scripts/auto_debug.py
?? scripts/autoplay_headless.py
?? src/engine/rejected_words.py
```

## git diff --stat
```
debug/preprocessed_debug.png               | Bin 371628 -> 379387 bytes
 debug/tile_placer/post_recall_attempt1.png | Bin 117178 -> 117852 bytes
 debug/tile_placer/post_recall_attempt2.png | Bin 120237 -> 119847 bytes
 debug/tile_placer/post_recall_attempt3.png | Bin 119929 -> 119778 bytes
 debug/tile_placer/post_recall_attempt4.png | Bin 119657 -> 119775 bytes
 debug/tile_placer/post_recall_attempt5.png | Bin 120024 -> 116753 bytes
 src/bot/autoplay_cog.py                    |  39 +++-
 src/browser/capture.py                     |  92 +++++++-
 src/browser/navigator.py                   |  17 +-
 src/browser/tile_placer.py                 | 340 +++++++++++++++++++++++++----
 src/browser/turn_detector.py               | 192 +++++++++++++++-
 src/vision/__init__.py                     | 127 ++++++++---
 tests/test_tile_placer.py                  |  79 ++++++-
 13 files changed, 775 insertions(+), 111 deletions(-)
```