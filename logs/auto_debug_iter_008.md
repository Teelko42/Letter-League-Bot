# Auto-debug iteration 8

- exit_code: `-9`
- duration: 1801.7s
- error_signature: `57b8cba597dd`

## Recent debug artifacts
- `debug/tile_placer/post_recall_attempt4.png`
- `debug/tile_placer/pre_play_attempt4_RHINE.png`
- `debug/tile_placer/post_recall_attempt3.png`
- `debug/turn_detection/frame_20260428_174352_045943_pre_start_attempt1.png`
- `debug/turn_detection/frame_20260428_174052_650475_pre_start_attempt1.png`
- `debug/preprocessed_debug.png`

## Autoplay log — error region
```

2026-04-28 17:42:38.499 | WARNING | __main__:_run:222 | place_move raised: Locator.bounding_box: Timeout 10000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

2026-04-28 17:42:38.500 | ERROR   | __main__:_run:224 | place_move hit iframe-dead error — re-navigating: Locator.bounding_box: Timeout 10000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

2026-04-28 17:42:38.500 | WARNING | __main__:_recover_iframe:140 | Iframe dead (1/2) — re-navigating: Locator.bounding_box: Timeout 10000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")

2026-04-28 17:42:39.013 | INFO    | src.browser.navigator:_run_navigation:82 | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
2026-04-28 17:42:52.830 | INFO    | src.browser.navigator:_run_navigation:125 | No Join Voice button found — assuming already in voice channel
2026-04-28 17:43:09.012 | WARNING | src.browser.navigator:navigate_to_activity:53 | Navigation attempt 1/3 failed: Locator.wait_for: Timeout 15000ms exceeded.
Call log:
  - waiting for locator("button[aria-label=\"Start An Activity\"]") to be visible
  - waiting for locator("button[aria-label=\"Start An Activity\"]")
. Retrying in 3 seconds...
2026-04-28 17:43:12.532 | INFO    | src.browser.navigator:_run_navigation:82 | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
2026-04-28 17:43:16.726 | INFO    | src.browser.navigator:_run_navigation:121 | Join Voice button found — clicking to join voice channel
2026-04-28 17:43:29.245 | INFO    | src.browser.navigator:_run_navigation:137 | Opened Activity shelf
2026-04-28 17:43:35.007 | INFO    | src.browser.navigator:_run_navigation:158 | Selected Letter League from shelf
2026-04-28 17:43:35.540 | INFO    | src.browser.navigator:_run_navigation:165 | Clicked Play — launching activity
```

## Subprocess stderr (tail)
```
[32m18:07:30[0m | [1mINFO   [0m | Word attempt 2/5: 'TEHR' (score=32)
[32m18:07:30[0m | [1mINFO   [0m | Placing tile 'T' (slot 3) -> board (10,10) | src=(1143.1,830.2) dst=(996.9,530.2)
[32m18:07:33[0m | [1mINFO   [0m | Tile 'T' verified at (10,10)
[32m18:07:34[0m | [1mINFO   [0m | Placing tile 'E' (slot 0) -> board (10,11) | src=(982.0,828.9) dst=(1047.4,530.9)
[32m18:07:36[0m | [1mINFO   [0m | Tile 'E' verified at (10,11)
[32m18:07:37[0m | [1mINFO   [0m | Placing tile 'H' (slot 4) -> board (10,12) | src=(1201.7,828.4) dst=(1093.5,529.4)
[32m18:07:40[0m | [1mINFO   [0m | Tile 'H' verified at (10,12)
[32m18:07:40[0m | [1mINFO   [0m | Placing tile 'R' (slot 2) -> board (10,13) | src=(1093.2,831.1) dst=(1148.6,527.3)
[32m18:07:44[0m | [1mINFO   [0m | Tile 'R' verified at (10,13)
[32m18:07:46[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1149.3, 750.0)
[32m18:07:47[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.2, 749.1)
[32m18:07:51[0m | [1mINFO   [0m | Word 'TEHR' rejected (attempt 2/5) — recalling tiles
[32m18:07:51[0m | [1mINFO   [0m | Blacklisted rejected word 'tehr' (total: 268)
[32m18:07:52[0m | [1mINFO   [0m | Clicking recall button at (1286.6, 751.2) (pass 1/10)
[32m18:07:54[0m | [1mINFO   [0m | Clicking recall button at (1284.1, 748.5) (pass 2/10)
[32m18:07:56[0m | [1mINFO   [0m | Clicking recall button at (1286.8, 751.6) (pass 3/10)
[32m18:07:58[0m | [1mINFO   [0m | Clicking recall button at (1283.8, 749.8) (pass 4/10)
[32m18:08:01[0m | [1mINFO   [0m | Clicking recall button at (1283.2, 749.8) (pass 5/10)
[32m18:08:03[0m | [1mINFO   [0m | Clicking recall button at (1287.6, 748.6) (pass 6/10)
[32m18:08:05[0m | [1mINFO   [0m | Clicking recall button at (1288.5, 749.7) (pass 7/10)
[32m18:08:08[0m | [1mINFO   [0m | Clicking recall button at (1282.7, 752.6) (pass 8/10)
[32m18:08:10[0m | [1mINFO   [0m | Clicking recall button at (1285.7, 752.8) (pass 9/10)
[32m18:08:12[0m | [1mINFO   [0m | Clicking recall button at (1284.5, 748.0) (pass 10/10)
[32m18:08:14[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m18:08:15[0m | [1mINFO   [0m | Word attempt 3/5: 'DERTH' (score=32)
[32m18:08:15[0m | [1mINFO   [0m | Placing tile 'D' (slot 5) -> board (10,8) | src=(1259.4,827.1) dst=(891.4,531.9)
[32m18:08:19[0m | [1mINFO   [0m | Tile 'D' verified at (10,8)
[32m18:08:19[0m | [1mINFO   [0m | Placing tile 'E' (slot 0) -> board (10,9) | src=(979.7,829.4) dst=(945.0,530.6)
[32m18:08:22[0m | [1mINFO   [0m | Tile 'E' verified at (10,9)
[32m18:08:22[0m | [1mINFO   [0m | Placing tile 'R' (slot 2) -> board (10,10) | src=(1090.1,826.5) dst=(992.2,529.0)
[32m18:08:26[0m | [1mINFO   [0m | Tile 'R' verified at (10,10)
[32m18:08:26[0m | [1mINFO   [0m | Placing tile 'T' (slot 3) -> board (10,11) | src=(1143.8,828.8) dst=(1044.2,532.3)
[32m18:08:29[0m | [1mINFO   [0m | Tile 'T' verified at (10,11)
[32m18:08:29[0m | [1mINFO   [0m | Placing tile 'H' (slot 4) -> board (10,12) | src=(1202.8,828.1) dst=(1094.4,530.7)
[32m18:08:33[0m | [1mINFO   [0m | Tile 'H' verified at (10,12)
[32m18:08:34[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.7, 753.0)
[32m18:08:37[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1145.4, 753.0)
[32m18:08:40[0m | [1mINFO   [0m | Word 'DERTH' rejected (attempt 3/5) — recalling tiles
[32m18:08:40[0m | [1mINFO   [0m | Blacklisted rejected word 'derth' (total: 269)
[32m18:08:41[0m | [1mINFO   [0m | Clicking recall button at (1284.3, 750.0) (pass 1/10)
[32m18:08:43[0m | [1mINFO   [0m | Clicking recall button at (1284.5, 753.8) (pass 2/10)
[32m18:08:45[0m | [1mINFO   [0m | Clicking recall button at (1284.7, 748.3) (pass 3/10)
[32m18:08:47[0m | [1mINFO   [0m | Clicking recall button at (1284.7, 753.7) (pass 4/10)
[32m18:08:49[0m | [1mINFO   [0m | Clicking recall button at (1286.7, 750.5) (pass 5/10)
[32m18:08:51[0m | [1mINFO   [0m | Clicking recall button at (1285.0, 750.1) (pass 6/10)
[32m18:08:53[0m | [1mINFO   [0m | Clicking recall button at (1283.8, 753.5) (pass 7/10)
[32m18:08:55[0m | [1mINFO   [0m | Clicking recall button at (1284.4, 750.6) (pass 8/10)
[32m18:08:58[0m | [1mINFO   [0m | Clicking recall button at (1284.3, 752.7) (pass 9/10)
[32m18:09:00[0m | [1mINFO   [0m | Clicking recall button at (1283.5, 752.2) (pass 10/10)
[32m18:09:02[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m18:09:03[0m | [1mINFO   [0m | Word attempt 4/5: 'RHINE' (score=32)
[32m18:09:03[0m | [1mINFO   [0m | Placing tile 'R' (slot 2) -> board (7,16) | src=(1089.5,826.3) dst=(1300.4,424.7)
[32m18:09:07[0m | [1mINFO   [0m | Tile 'R' verified at (7,16)
[32m18:09:07[0m | [1mINFO   [0m | Placing tile 'H' (slot 4) -> board (8,16) | src=(1198.4,826.0) dst=(1300.4,462.6)
[32m18:09:10[0m | [1mINFO   [0m | Tile 'H' verified at (8,16)
[32m18:09:11[0m | [1mINFO   [0m | Placing tile 'N' (slot 6) -> board (10,16) | src=(1313.1,830.3) dst=(1299.8,527.2)
[32m18:09:14[0m | [1mINFO   [0m | Tile 'N' verified at (10,16)
[32m18:09:14[0m | [1mINFO   [0m | Placing tile 'E' (slot 0) -> board (11,16) | src=(981.0,829.6) dst=(1300.4,562.6)
[32m18:09:17[0m | [1mINFO   [0m | Tile 'E' verified at (11,16)
[32m18:09:19[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.7, 748.5)
[32m18:09:21[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.2, 749.4)
[32m18:09:24[0m | [1mINFO   [0m | Word 'RHINE' rejected (attempt 4/5) — recalling tiles
[32m18:09:24[0m | [1mINFO   [0m | Blacklisted rejected word 'rhine' (total: 270)
[32m18:09:25[0m | [1mINFO   [0m | Clicking recall button at (1283.4, 750.1) (pass 1/10)
[32m18:09:27[0m | [1mINFO   [0m | Clicking recall button at (1287.6, 749.0) (pass 2/10)
[32m18:09:29[0m | [1mINFO   [0m | Clicking recall button at (1285.8, 751.0) (pass 3/10)
[32m18:09:32[0m | [1mINFO   [0m | Clicking recall button at (1287.8, 751.7) (pass 4/10)
[32m18:09:34[0m | [1mINFO   [0m | Clicking recall button at (1285.4, 752.1) (pass 5/10)
[32m18:09:37[0m | [1mINFO   [0m | Clicking recall button at (1283.7, 753.6) (pass 6/10)
[32m18:09:39[0m | [1mINFO   [0m | Clicking recall button at (1284.2, 751.2) (pass 7/10)
[32m18:09:41[0m | [1mINFO   [0m | Clicking recall button at (1284.4, 752.8) (pass 8/10)
[32m18:09:44[0m | [1mINFO   [0m | Clicking recall button at (1282.8, 750.0) (pass 9/10)
[32m18:09:46[0m | [1mINFO   [0m | Clicking recall button at (1284.8, 753.3) (pass 10/10)
[32m18:09:48[0m | [33m[1mWARNING[0m | Recall hit cap (10 clicks) without stabilising
[32m18:09:49[0m | [1mINFO   [0m | Word attempt 5/5: 'EDH' (score=30)
[32m18:09:50[0m | [1mINFO   [0m | Placing tile 'E' (slot 0) -> board (10,10) | src=(983.0,827.3) dst=(994.8,527.7)
[32m18:09:52[0m | [1mINFO   [0m | Tile 'E' verified at (10,10)
[32m18:09:53[0m | [1mINFO   [0m | Placing tile 'D' (slot 5) -> board (10,11) | src=(1255.3,826.9) dst=(1047.1,528.7)

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
?? debug/tile_placer/pre_play_attempt1_AMOEBA.png
?? debug/tile_placer/pre_play_attempt1_ANNUAL.png
?? debug/tile_placer/pre_play_attempt1_ANORAK.png
?? debug/tile_placer/pre_play_attempt1_ARABIC.png
?? debug/tile_placer/pre_play_attempt1_BEANY.png
?? debug/tile_placer/pre_play_attempt1_BIN.png
?? debug/tile_placer/pre_play_attempt1_BITTY.png
?? debug/tile_placer/pre_play_attempt1_BODEGA.png
?? debug/tile_placer/pre_play_attempt1_CAULKER.png
?? debug/tile_placer/pre_play_attempt1_CORDIAL.png
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
?? debug/tile_placer/pre_play_attempt1_HE.png
?? debug/tile_placer/pre_play_attempt1_HINGED.png
?? debug/tile_placer/pre_play_attempt1_HOLDER.png
?? debug/tile_placer/pre_play_attempt1_ID.png
?? debug/tile_placer/pre_play_attempt1_JIAO.png
?? debug/tile_placer/pre_play_attempt1_JO.png
?? debug/tile_placer/pre_play_attempt1_JOEY.png
?? debug/tile_placer/pre_play_attempt1_JOHN.png
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
?? debug/tile_placer/pre_play_attempt1_THINE.png
?? debug/tile_placer/pre_play_attempt1_THIRLED.png
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
?? debug/tile_placer/pre_play_attempt2_HELD.png
?? debug/tile_placer/pre_play_attempt2_HOLDEN.png
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
?? debug/tile_placer/pre_play_attempt2_TEHR.png
?? debug/tile_placer/pre_play_attempt2_THIOL.png
?? debug/tile_placer/pre_play_attempt2_THIRD.png
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
?? debug/tile_placer/pre_play_attempt3_DERTH.png
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
?? debug/tile_placer/pre_play_attempt3_HELL.png
?? debug/tile_placer/pre_play_attempt3_HIELD.png
?? debug/tile_placer/pre_play_attempt3_HODJA.png
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
?? debug/tile_placer/pre_play_attempt3_THIRL.png
?? debug/tile_placer/pre_play_attempt3_THOLED.png
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
?? debug/tile_placer/pre_play_attempt4_JOLL.png
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
?? debug/tile_placer/pre_play_attempt4_RHINE.png
?? debug/tile_placer/pre_play_attempt4_TERGA.png
?? debug/tile_placer/pre_play_attempt4_THE.png
?? debug/tile_placer/pre_play_attempt4_THEN.png
?? debug/tile_placer/pre_play_attempt4_TON.png
?? debug/tile_placer/pre_play_attempt4_TRINDLE.png
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
?? debug/tile_placer/pre_play_attempt5_HERD.png
?? debug/tile_placer/pre_play_attempt5_HETE.png
?? debug/tile_placer/pre_play_attempt5_JOINED.png
?? debug/tile_placer/pre_play_attempt5_KEEF.png
?? debug/tile_placer/pre_play_attempt5_LACKED.png
?? debug/tile_placer/pre_play_attempt5_LAGUNA.png
?? debug/tile_placer/pre_play_attempt5_LANATE.png
?? debug/tile_placer/pre_play_attempt5_LAUGHING.png
?? debug/tile_placer/pre_play_attempt5_LEHR.png
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
?? debug/turn_detection/frame_20260428_174052_650475_pre_start_attempt1.png
?? debug/turn_detection/frame_20260428_174352_045943_pre_start_attempt1.png
?? logs/
?? scripts/auto_debug.py
?? scripts/autoplay_headless.py
?? src/engine/rejected_words.py
```

## git diff --stat
```
debug/preprocessed_debug.png               | Bin 371628 -> 382345 bytes
 debug/tile_placer/post_recall_attempt1.png | Bin 117178 -> 120516 bytes
 debug/tile_placer/post_recall_attempt2.png | Bin 120237 -> 121292 bytes
 debug/tile_placer/post_recall_attempt3.png | Bin 119929 -> 121020 bytes
 debug/tile_placer/post_recall_attempt4.png | Bin 119657 -> 121029 bytes
 debug/tile_placer/post_recall_attempt5.png | Bin 120024 -> 120765 bytes
 src/bot/autoplay_cog.py                    |  39 +++-
 src/browser/capture.py                     |  92 +++++++-
 src/browser/navigator.py                   |  17 +-
 src/browser/tile_placer.py                 | 354 +++++++++++++++++++++++++----
 src/browser/turn_detector.py               | 192 +++++++++++++++-
 src/vision/__init__.py                     | 152 ++++++++++---
 tests/test_tile_placer.py                  |  79 ++++++-
 13 files changed, 809 insertions(+), 116 deletions(-)
```