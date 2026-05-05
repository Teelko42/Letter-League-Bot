# Auto-debug iteration 1

- exit_code: `0`
- duration: 1722.3s
- error_signature: `3f00468e8ebc`
- words placed: 3
- turns skipped (swap/skip — these are FAILURES for the user goal): 7
- terminal marker reached: True

**User goal: the bot must place a word every turn.** A turn that ends in
swap/skip means the placement pipeline failed (vision drift, retries
exhausted, etc.) and the engine fell back to swap. The fix needs to make
more turns end with a placed word, not just keep the run alive longer.

## Recent debug artifacts
- `debug/tile_placer/post_recall_attempt3.png`
- `debug/tile_placer/pre_play_attempt3_GEED.png`
- `debug/tile_placer/post_recall_attempt2.png`
- `debug/turn_detection/frame_20260504_135923_986702_pre_start_attempt1.png`
- `debug/preprocessed_debug.png`

## Autoplay log — error region
```
2026-05-04 14:26:41.250 | INFO    | src.browser.tile_placer:_click_confirm:812 | Clicking confirm/PLAY button at (1145.4, 749.5)
2026-05-04 14:26:42.942 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 131130 bytes (attempt 1)
2026-05-04 14:26:43.026 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:837 | Post-confirm poll 1/6: my_turn
2026-05-04 14:26:44.800 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 131627 bytes (attempt 1)
2026-05-04 14:26:44.883 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:837 | Post-confirm poll 2/6: my_turn
2026-05-04 14:26:46.619 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 130841 bytes (attempt 1)
2026-05-04 14:26:46.707 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:837 | Post-confirm poll 3/6: my_turn
2026-05-04 14:26:46.708 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:843 | Re-clicking PLAY (retry after 3 polls)
2026-05-04 14:26:46.708 | INFO    | src.browser.tile_placer:_click_confirm:812 | Clicking confirm/PLAY button at (1143.8, 749.6)
2026-05-04 14:26:48.511 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 131070 bytes (attempt 1)
2026-05-04 14:26:48.590 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:837 | Post-confirm poll 4/6: my_turn
2026-05-04 14:26:50.327 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 131706 bytes (attempt 1)
2026-05-04 14:26:50.407 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:837 | Post-confirm poll 5/6: my_turn
2026-05-04 14:26:52.147 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 131284 bytes (attempt 1)
2026-05-04 14:26:52.236 | DEBUG   | src.browser.tile_placer:_wait_for_acceptance:837 | Post-confirm poll 6/6: my_turn
2026-05-04 14:26:52.237 | INFO    | src.browser.tile_placer:place_move:1114 | Word 'GEED' rejected (attempt 3/3) — recalling tiles
2026-05-04 14:26:52.240 | INFO    | src.engine.rejected_words:add:71 | Blacklisted rejected word 'geed' (total: 290)
2026-05-04 14:26:52.240 | INFO    | src.browser.tile_placer:_recall_tiles:909 | Clicking recall button at (1288.5, 753.0) (pass 1/5)
2026-05-04 14:26:53.154 | INFO    | src.browser.tile_placer:_recall_tiles:909 | Clicking recall button at (1283.3, 748.7) (pass 2/5)
2026-05-04 14:26:53.931 | INFO    | src.browser.tile_placer:_recall_tiles:909 | Clicking recall button at (1287.5, 753.5) (pass 3/5)
2026-05-04 14:26:54.656 | INFO    | src.browser.tile_placer:_recall_tiles:909 | Clicking recall button at (1285.2, 749.6) (pass 4/5)
2026-05-04 14:26:55.486 | INFO    | src.browser.tile_placer:_recall_tiles:909 | Clicking recall button at (1284.7, 752.9) (pass 5/5)
2026-05-04 14:26:56.910 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 131272 bytes (attempt 1)
2026-05-04 14:26:56.912 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:862 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt3.png
2026-05-04 14:26:56.913 | WARNING | src.browser.tile_placer:place_move:1129 | All 3 word attempt(s) failed — performing tile swap fallback
2026-05-04 14:26:57.011 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:420 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-04 14:26:57.012 | WARNING | src.browser.tile_placer:_tile_swap:993 | Falling back to tile swap at (1009.6, 750.3) — no valid words accepted after 3 attempts
2026-05-04 14:26:57.027 | INFO    | __main__:_run:270 | Turn 10: no move accepted (swap/skip)
2026-05-04 14:26:57.028 | INFO    | __main__:_run:151 | Reached max_turns=10 — exiting cleanly
2026-05-04 14:26:57.595 | INFO    | __main__:main:300 | Headless autoplay finished in 1710.3s
```

## Subprocess stderr (tail)
```
[32m14:25:04[0m | [1mINFO   [0m | Tile 'E' verified at (16,16)
[32m14:25:05[0m | [1mINFO   [0m | Placing tile 'E' (slot 4) -> board (16,17) | src=(1199.5,825.8) dst=(1346.5,736.5)
[32m14:25:07[0m | [1mINFO   [0m | Tile 'E' verified at (16,17)
[32m14:25:08[0m | [1mINFO   [0m | Placing tile 'D' (slot 3) -> board (16,18) | src=(1146.2,826.9) dst=(1398.8,735.4)
[32m14:25:10[0m | [1mINFO   [0m | Tile 'D' verified at (16,18)
[32m14:25:12[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1149.4, 749.4)
[32m14:25:17[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1146.5, 752.9)
[32m14:25:23[0m | [1mINFO   [0m | Word 'OGEED' rejected (attempt 3/3) — recalling tiles
[32m14:25:23[0m | [1mINFO   [0m | Blacklisted rejected word 'ogeed' (total: 287)
[32m14:25:23[0m | [1mINFO   [0m | Clicking recall button at (1287.7, 752.1) (pass 1/6)
[32m14:25:24[0m | [1mINFO   [0m | Clicking recall button at (1284.9, 748.9) (pass 2/6)
[32m14:25:24[0m | [1mINFO   [0m | Clicking recall button at (1282.8, 749.7) (pass 3/6)
[32m14:25:25[0m | [1mINFO   [0m | Clicking recall button at (1285.1, 748.6) (pass 4/6)
[32m14:25:26[0m | [1mINFO   [0m | Clicking recall button at (1284.8, 751.7) (pass 5/6)
[32m14:25:27[0m | [1mINFO   [0m | Clicking recall button at (1284.3, 752.6) (pass 6/6)
[32m14:25:28[0m | [33m[1mWARNING[0m | All 3 word attempt(s) failed — returning to caller for re-vision
[32m14:25:28[0m | [33m[1mWARNING[0m | No move accepted (candidates=5) — re-vision + swap fallback
[32m14:25:32[0m | [1mINFO   [0m | Vision pipeline start — mode=wild
[32m14:25:32[0m | [1mINFO   [0m | Preprocessing complete — 416476 bytes
[32m14:25:32[0m | [1mINFO   [0m | Calling Claude Vision API — retry=False
[32m14:25:35[0m | [1mINFO   [0m | Claude Vision response received — latency=2.97s  input_tokens=2903  output_tokens=79
[32m14:25:35[0m | [1mINFO   [0m | Extraction complete (first attempt)
[32m14:25:35[0m | [1mINFO   [0m | Validation result — 0 error(s)
[32m14:25:35[0m | [1mINFO   [0m | Vision pipeline complete — 3.29s  tiles=1  rack_size=6
[32m14:25:35[0m | [1mINFO   [0m | Word attempt 1/3: 'EVO' (score=12)
[32m14:25:35[0m | [1mINFO   [0m | Placing tile 'E' (slot 1) -> board (14,16) | src=(1036.6,830.0) dst=(1297.5,665.6)
[32m14:25:38[0m | [1mINFO   [0m | Tile 'E' verified at (14,16)
[32m14:25:38[0m | [1mINFO   [0m | Placing tile 'V' (slot 5) -> board (15,16) | src=(1258.4,827.0) dst=(1297.9,700.2)
[32m14:25:41[0m | [1mINFO   [0m | Tile 'V' verified at (15,16)
[32m14:25:41[0m | [1mINFO   [0m | Placing tile 'O' (slot 0) -> board (16,16) | src=(982.2,829.8) dst=(1296.9,736.4)
[32m14:25:44[0m | [1mINFO   [0m | Tile 'O' verified at (16,16)
[32m14:25:45[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1145.2, 749.3)
[32m14:25:51[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.1, 750.3)
[32m14:25:56[0m | [1mINFO   [0m | Word 'EVO' rejected (attempt 1/3) — recalling tiles
[32m14:25:56[0m | [1mINFO   [0m | Blacklisted rejected word 'evo' (total: 288)
[32m14:25:56[0m | [1mINFO   [0m | Clicking recall button at (1285.8, 748.4) (pass 1/5)
[32m14:25:57[0m | [1mINFO   [0m | Clicking recall button at (1288.1, 748.1) (pass 2/5)
[32m14:25:58[0m | [1mINFO   [0m | Clicking recall button at (1288.1, 751.2) (pass 3/5)
[32m14:25:59[0m | [1mINFO   [0m | Clicking recall button at (1287.8, 749.4) (pass 4/5)
[32m14:26:00[0m | [1mINFO   [0m | Clicking recall button at (1283.8, 753.5) (pass 5/5)
[32m14:26:01[0m | [1mINFO   [0m | Word attempt 2/3: 'GEODE' (score=12)
[32m14:26:01[0m | [1mINFO   [0m | Placing tile 'E' (slot 1) -> board (16,16) | src=(1035.3,831.0) dst=(1297.6,739.1)
[32m14:26:04[0m | [1mINFO   [0m | Tile 'E' verified at (16,16)
[32m14:26:04[0m | [1mINFO   [0m | Placing tile 'O' (slot 0) -> board (16,17) | src=(979.8,827.7) dst=(1346.2,735.9)
[32m14:26:07[0m | [1mINFO   [0m | Tile 'O' verified at (16,17)
[32m14:26:07[0m | [1mINFO   [0m | Placing tile 'D' (slot 3) -> board (16,18) | src=(1148.2,831.0) dst=(1400.1,736.2)
[32m14:26:10[0m | [1mINFO   [0m | Tile 'D' verified at (16,18)
[32m14:26:10[0m | [1mINFO   [0m | Placing tile 'E' (slot 4) -> board (16,19) | src=(1203.6,827.2) dst=(1450.1,736.4)
[32m14:26:13[0m | [1mINFO   [0m | Tile 'E' verified at (16,19)
[32m14:26:14[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1147.0, 749.7)
[32m14:26:19[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1148.8, 750.5)
[32m14:26:25[0m | [1mINFO   [0m | Word 'GEODE' rejected (attempt 2/3) — recalling tiles
[32m14:26:25[0m | [1mINFO   [0m | Blacklisted rejected word 'geode' (total: 289)
[32m14:26:25[0m | [1mINFO   [0m | Clicking recall button at (1283.8, 750.9) (pass 1/6)
[32m14:26:26[0m | [1mINFO   [0m | Clicking recall button at (1283.9, 751.4) (pass 2/6)
[32m14:26:27[0m | [1mINFO   [0m | Clicking recall button at (1284.7, 750.5) (pass 3/6)
[32m14:26:27[0m | [1mINFO   [0m | Clicking recall button at (1286.9, 753.9) (pass 4/6)
[32m14:26:28[0m | [1mINFO   [0m | Clicking recall button at (1283.1, 751.7) (pass 5/6)
[32m14:26:29[0m | [1mINFO   [0m | Clicking recall button at (1283.8, 749.8) (pass 6/6)
[32m14:26:31[0m | [1mINFO   [0m | Word attempt 3/3: 'GEED' (score=11)
[32m14:26:31[0m | [1mINFO   [0m | Placing tile 'E' (slot 1) -> board (16,16) | src=(1033.3,831.4) dst=(1300.0,736.6)
[32m14:26:33[0m | [1mINFO   [0m | Tile 'E' verified at (16,16)
[32m14:26:34[0m | [1mINFO   [0m | Placing tile 'E' (slot 4) -> board (16,17) | src=(1203.5,828.4) dst=(1347.6,739.0)
[32m14:26:36[0m | [1mINFO   [0m | Tile 'E' verified at (16,17)
[32m14:26:37[0m | [1mINFO   [0m | Placing tile 'D' (slot 3) -> board (16,18) | src=(1148.6,825.7) dst=(1400.6,739.7)
[32m14:26:39[0m | [1mINFO   [0m | Tile 'D' verified at (16,18)
[32m14:26:41[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1145.4, 749.5)
[32m14:26:46[0m | [1mINFO   [0m | Clicking confirm/PLAY button at (1143.8, 749.6)
[32m14:26:52[0m | [1mINFO   [0m | Word 'GEED' rejected (attempt 3/3) — recalling tiles
[32m14:26:52[0m | [1mINFO   [0m | Blacklisted rejected word 'geed' (total: 290)
[32m14:26:52[0m | [1mINFO   [0m | Clicking recall button at (1288.5, 753.0) (pass 1/5)
[32m14:26:53[0m | [1mINFO   [0m | Clicking recall button at (1283.3, 748.7) (pass 2/5)
[32m14:26:53[0m | [1mINFO   [0m | Clicking recall button at (1287.5, 753.5) (pass 3/5)
[32m14:26:54[0m | [1mINFO   [0m | Clicking recall button at (1285.2, 749.6) (pass 4/5)
[32m14:26:55[0m | [1mINFO   [0m | Clicking recall button at (1284.7, 752.9) (pass 5/5)
[32m14:26:56[0m | [33m[1mWARNING[0m | All 3 word attempt(s) failed — performing tile swap fallback
[32m14:26:57[0m | [33m[1mWARNING[0m | Falling back to tile swap at (1009.6, 750.3) — no valid words accepted after 3 attempts
[32m14:26:57[0m | [1mINFO   [0m | Turn 10: no move accepted (swap/skip)
[32m14:26:57[0m | [1mINFO   [0m | Reached max_turns=10 — exiting cleanly
[32m14:26:57[0m | [1mINFO   [0m | Headless autoplay finished in 1710.3s
```

## git status --short
```
M .gitignore
 D TESTING_REPORT.md
 M data/rejected_words.txt
 M debug/iframe_missing.png
 M debug/preprocessed_debug.png
 M debug/tile_placer/post_recall_attempt1.png
 M debug/tile_placer/post_recall_attempt2.png
 M debug/tile_placer/post_recall_attempt3.png
 M debug/tile_placer/post_recall_attempt4.png
 M debug/tile_placer/post_recall_attempt5.png
 M debug/tile_placer/pre_play_attempt1_ST.png
 M debug/tile_placer/pre_play_attempt2_ENE.png
 M logs/auto_debug.log
 M logs/auto_debug_console.log
 M logs/auto_debug_iter_001.md
 M logs/auto_debug_iter_001_response.md
 M logs/auto_debug_iter_002.md
 M logs/auto_debug_iter_002_response.md
 M logs/autoplay.log
 M scripts/auto_debug.py
 M scripts/autoplay_headless.py
 M src/browser/navigator.py
 M src/browser/tile_placer.py
 M src/vision/__init__.py
?? debug/tile_placer/pre_play_attempt1_AERIALS.png
?? debug/tile_placer/pre_play_attempt1_AGATE.png
?? debug/tile_placer/pre_play_attempt1_AIDER.png
?? debug/tile_placer/pre_play_attempt1_ANNOYERS.png
?? debug/tile_placer/pre_play_attempt1_ATELIER.png
?? debug/tile_placer/pre_play_attempt1_BAYE.png
?? debug/tile_placer/pre_play_attempt1_BECAP.png
?? debug/tile_placer/pre_play_attempt1_BIOTITE.png
?? debug/tile_placer/pre_play_attempt1_BLUGGY.png
?? debug/tile_placer/pre_play_attempt1_BY.png
?? debug/tile_placer/pre_play_attempt1_COB.png
?? debug/tile_placer/pre_play_attempt1_DE.png
?? debug/tile_placer/pre_play_attempt1_DELATING.png
?? debug/tile_placer/pre_play_attempt1_DEMO.png
?? debug/tile_placer/pre_play_attempt1_DIALOGIC.png
?? debug/tile_placer/pre_play_attempt1_DISME.png
?? debug/tile_placer/pre_play_attempt1_DOUC.png
?? debug/tile_placer/pre_play_attempt1_DOVE.png
?? debug/tile_placer/pre_play_attempt1_EVO.png
?? debug/tile_placer/pre_play_attempt1_FAE.png
?? debug/tile_placer/pre_play_attempt1_FAMINE.png
?? debug/tile_placer/pre_play_attempt1_FAP.png
?? debug/tile_placer/pre_play_attempt1_FAR.png
?? debug/tile_placer/pre_play_attempt1_FRIED.png
?? debug/tile_placer/pre_play_attempt1_GANNETRY.png
?? debug/tile_placer/pre_play_attempt1_GAUDIER.png
?? debug/tile_placer/pre_play_attempt1_GEMEL.png
?? debug/tile_placer/pre_play_attempt1_GLADIATE.png
?? debug/tile_placer/pre_play_attempt1_GLAZE.png
?? debug/tile_placer/pre_play_attempt1_GOAL.png
?? debug/tile_placer/pre_play_attempt1_GOBIID.png
?? debug/tile_placer/pre_play_attempt1_HILUS.png
?? debug/tile_placer/pre_play_attempt1_INEPTER.png
?? debug/tile_placer/pre_play_attempt1_IRADE.png
?? debug/tile_placer/pre_play_attempt1_IRKED.png
?? debug/tile_placer/pre_play_attempt1_JAPS.png
?? debug/tile_placer/pre_play_attempt1_JAUP.png
?? debug/tile_placer/pre_play_attempt1_JAY.png
?? debug/tile_placer/pre_play_attempt1_JIBE.png
?? debug/tile_placer/pre_play_attempt1_JIRD.png
?? debug/tile_placer/pre_play_attempt1_JOUGS.png
?? debug/tile_placer/pre_play_attempt1_JOW.png
?? debug/tile_placer/pre_play_attempt1_JOWS.png
?? debug/tile_placer/pre_play_attempt1_KO.png
?? debug/tile_placer/pre_play_attempt1_KOP.png
?? debug/tile_placer/pre_play_attempt1_LEGGIE.png
?? debug/tile_placer/pre_play_attempt1_LIEU.png
?? debug/tile_placer/pre_play_attempt1_LOFT.png
?? debug/tile_placer/pre_play_attempt1_LOGIA.png
?? debug/tile_placer/pre_play_attempt1_LOUDISH.png
?? debug/tile_placer/pre_play_attempt1_MADE.png
?? debug/tile_placer/pre_play_attempt1_MEW.png
?? debug/tile_placer/pre_play_attempt1_MOJO.png
?? debug/tile_placer/pre_play_attempt1_MOJOS.png
?? debug/tile_placer/pre_play_attempt1_MOVED.png
?? debug/tile_placer/pre_play_attempt1_MOW.png
?? debug/tile_placer/pre_play_attempt1_NENE.png
?? debug/tile_placer/pre_play_attempt1_NGWEE.png
?? debug/tile_placer/pre_play_attempt1_NY.png
?? debug/tile_placer/pre_play_attempt1_ONETIME.png
?? debug/tile_placer/pre_play_attempt1_OOBIT.png
?? debug/tile_placer/pre_play_attempt1_OVERRAN.png
?? debug/tile_placer/pre_play_attempt1_OYE.png
?? debug/tile_placer/pre_play_attempt1_PARENTS.png
?? debug/tile_placer/pre_play_attempt1_PEEL.png
?? debug/tile_placer/pre_play_attempt1_PERCID.png
?? debug/tile_placer/pre_play_attempt1_PIU.png
?? debug/tile_placer/pre_play_attempt1_QUARTER.png
?? debug/tile_placer/pre_play_attempt1_QUELEA.png
?? debug/tile_placer/pre_play_attempt1_REGRAFT.png
?? debug/tile_placer/pre_play_attempt1_REMISED.png
?? debug/tile_placer/pre_play_attempt1_REMOVED.png
?? debug/tile_placer/pre_play_attempt1_REPENT.png
?? debug/tile_placer/pre_play_attempt1_RIP.png
?? debug/tile_placer/pre_play_attempt1_SCRAPE.png
?? debug/tile_placer/pre_play_attempt1_SELS.png
?? debug/tile_placer/pre_play_attempt1_SNORT.png
?? debug/tile_placer/pre_play_attempt1_STEALAGE.png
?? debug/tile_placer/pre_play_attempt1_TALLAGE.png
?? debug/tile_placer/pre_play_attempt1_TAVERN.png
?? debug/tile_placer/pre_play_attempt1_TAWIE.png
?? debug/tile_placer/pre_play_attempt1_TREADING.png
?? debug/tile_placer/pre_play_attempt1_TRECENTO.png
?? debug/tile_placer/pre_play_attempt1_TUTOY.png
?? debug/tile_placer/pre_play_attempt1_UGSOME.png
?? debug/tile_placer/pre_play_attempt1_VROOMED.png
?? debug/tile_placer/pre_play_attempt1_VROT.png
?? debug/tile_placer/pre_play_attempt1_WAILED.png
?? debug/tile_placer/pre_play_attempt1_WAITED.png
?? debug/tile_placer/pre_play_attempt1_WALTZER.png
?? debug/tile_placer/pre_play_attempt1_WAQF.png
?? debug/tile_placer/pre_play_attempt1_WEIL.png
?? debug/tile_placer/pre_play_attempt1_WENGE.png
?? debug/tile_placer/pre_play_attempt1_WIKI.png
?? debug/tile_placer/pre_play_attempt1_YET.png
?? debug/tile_placer/pre_play_attempt1_YETI.png
?? debug/tile_placer/pre_play_attempt1_YU.png
?? debug/tile_placer/pre_play_attempt1_ZEUGMA.png
?? debug/tile_placer/pre_play_attempt2_ABLEGATE.png
?? debug/tile_placer/pre_play_attempt2_ABYE.png
?? debug/tile_placer/pre_play_attempt2_AGUED.png
?? debug/tile_placer/pre_play_attempt2_AQUAE.png
?? debug/tile_placer/pre_play_attempt2_AREDE.png
?? debug/tile_placer/pre_play_attempt2_ARGUED.png
?? debug/tile_placer/pre_play_attempt2_AYE.png
?? debug/tile_placer/pre_play_attempt2_AYU.png
?? debug/tile_placer/pre_play_attempt2_DESIRE.png
?? debug/tile_placer/pre_play_attempt2_DIALOG.png
?? debug/tile_placer/pre_play_attempt2_DOAT.png
?? debug/tile_placer/pre_play_attempt2_DOLIA.png
?? debug/tile_placer/pre_play_attempt2_EEEW.png
?? debug/tile_placer/pre_play_attempt2_ELM.png
?? debug/tile_placer/pre_play_attempt2_EME.png
?? debug/tile_placer/pre_play_attempt2_EMOTE.png
?? debug/tile_placer/pre_play_attempt2_EMOVE.png
?? debug/tile_placer/pre_play_attempt2_EVOE.png
?? debug/tile_placer/pre_play_attempt2_FAB.png
?? debug/tile_placer/pre_play_attempt2_FARL.png
?? debug/tile_placer/pre_play_attempt2_FIE.png
?? debug/tile_placer/pre_play_attempt2_FOP.png
?? debug/tile_placer/pre_play_attempt2_FRAILTY.png
?? debug/tile_placer/pre_play_attempt2_FUMS.png
?? debug/tile_placer/pre_play_attempt2_GAITED.png
?? debug/tile_placer/pre_play_attempt2_GALEATE.png
?? debug/tile_placer/pre_play_attempt2_GAMGEE.png
?? debug/tile_placer/pre_play_attempt2_GEODE.png
?? debug/tile_placer/pre_play_attempt2_GLEBY.png
?? debug/tile_placer/pre_play_attempt2_HIND.png
?? debug/tile_placer/pre_play_attempt2_HUIS.png
?? debug/tile_placer/pre_play_attempt2_INCAGED.png
?? debug/tile_placer/pre_play_attempt2_IODIC.png
?? debug/tile_placer/pre_play_attempt2_IRISED.png
?? debug/tile_placer/pre_play_attempt2_JAGS.png
?? debug/tile_placer/pre_play_attempt2_JAPE.png
?? debug/tile_placer/pre_play_attempt2_JAW.png
?? debug/tile_placer/pre_play_attempt2_JEFE.png
?? debug/tile_placer/pre_play_attempt2_JERID.png
?? debug/tile_placer/pre_play_attempt2_JO.png
?? debug/tile_placer/pre_play_attempt2_JOMO.png
?? debug/tile_placer/pre_play_attempt2_JOMOS.png
?? debug/tile_placer/pre_play_attempt2_KIWI.png
?? debug/tile_placer/pre_play_attempt2_KON.png
?? debug/tile_placer/pre_play_attempt2_LAID.png
?? debug/tile_placer/pre_play_attempt2_LOFTS.png
?? debug/tile_placer/pre_play_attempt2_MAZE.png
?? debug/tile_placer/pre_play_attempt2_MEWL.png
?? debug/tile_placer/pre_play_attempt2_MODE.png
?? debug/tile_placer/pre_play_attempt2_OATY.png
?? debug/tile_placer/pre_play_attempt2_OLDISH.png
?? debug/tile_placer/pre_play_attempt2_ORNATE.png
?? debug/tile_placer/pre_play_attempt2_OW.png
?? debug/tile_placer/pre_play_attempt2_PAL.png
?? debug/tile_placer/pre_play_attempt2_PRIEF.png
?? debug/tile_placer/pre_play_attempt2_PROW.png
?? debug/tile_placer/pre_play_attempt2_PURI.png
?? debug/tile_placer/pre_play_attempt2_QUAI.png
?? debug/tile_placer/pre_play_attempt2_RETURF.png
?? debug/tile_placer/pre_play_attempt2_SOJU.png
?? debug/tile_placer/pre_play_attempt2_STEADING.png
?? debug/tile_placer/pre_play_attempt2_TALLAGED.png
?? debug/tile_placer/pre_play_attempt2_TANNERY.png
?? debug/tile_placer/pre_play_attempt2_TORQUER.png
?? debug/tile_placer/pre_play_attempt2_TRONS.png
?? debug/tile_placer/pre_play_attempt2_UEY.png
?? debug/tile_placer/pre_play_attempt2_VANE.png
?? debug/tile_placer/pre_play_attempt2_VANTS.png
?? debug/tile_placer/pre_play_attempt2_VENOMED.png
?? debug/tile_placer/pre_play_attempt2_WALTZ.png
?? debug/tile_placer/pre_play_attempt2_WEEN.png
?? debug/tile_placer/pre_play_attempt2_WEM.png
?? debug/tile_placer/pre_play_attempt2_WIGLET.png
?? debug/tile_placer/pre_play_attempt2_YAE.png
?? debug/tile_placer/pre_play_attempt2_YARNING.png
?? debug/tile_placer/pre_play_attempt3_BLUEY.png
?? debug/tile_placer/pre_play_attempt3_CANNERY.png
?? debug/tile_placer/pre_play_attempt3_DISH.png
?? debug/tile_placer/pre_play_attempt3_DOME.png
?? debug/tile_placer/pre_play_attempt3_DOUT.png
?? debug/tile_placer/pre_play_attempt3_DULLISH.png
?? debug/tile_placer/pre_play_attempt3_DWELT.png
?? debug/tile_placer/pre_play_attempt3_EEN.png
?? debug/tile_placer/pre_play_attempt3_EEW.png
?? debug/tile_placer/pre_play_attempt3_EYOT.png
?? debug/tile_placer/pre_play_attempt3_FA.png
?? debug/tile_placer/pre_play_attempt3_FAN.png
?? debug/tile_placer/pre_play_attempt3_FAY.png
?? debug/tile_placer/pre_play_attempt3_FEY.png
?? debug/tile_placer/pre_play_attempt3_FIB.png
?? debug/tile_placer/pre_play_attempt3_FIND.png
?? debug/tile_placer/pre_play_attempt3_FOGS.png
?? debug/tile_placer/pre_play_attempt3_FOLK.png
?? debug/tile_placer/pre_play_attempt3_GADE.png
?? debug/tile_placer/pre_play_attempt3_GALATEA.png
?? debug/tile_placer/pre_play_attempt3_GALEATED.png
?? debug/tile_placer/pre_play_attempt3_GALLETA.png
?? debug/tile_placer/pre_play_attempt3_GAUZE.png
?? debug/tile_placer/pre_play_attempt3_GAWK.png
?? debug/tile_placer/pre_play_attempt3_GEED.png
?? debug/tile_placer/pre_play_attempt3_GEM.png
?? debug/tile_placer/pre_play_attempt3_GENE.png
?? debug/tile_placer/pre_play_attempt3_GOLD.png
?? debug/tile_placer/pre_play_attempt3_GRADE.png
?? debug/tile_placer/pre_play_attempt3_GRADIENT.png
?? debug/tile_placer/pre_play_attempt3_JASP.png
?? debug/tile_placer/pre_play_attempt3_JEEP.png
?? debug/tile_placer/pre_play_attempt3_JIG.png
?? debug/tile_placer/pre_play_attempt3_JOGS.png
?? debug/tile_placer/pre_play_attempt3_JOWL.png
?? debug/tile_placer/pre_play_attempt3_KAW.png
?? debug/tile_placer/pre_play_attempt3_LEME.png
?? debug/tile_placer/pre_play_attempt3_LOAD.png
?? debug/tile_placer/pre_play_attempt3_LOID.png
?? debug/tile_placer/pre_play_attempt3_MAW.png
?? debug/tile_placer/pre_play_attempt3_MISER.png
?? debug/tile_placer/pre_play_attempt3_MOVE.png
?? debug/tile_placer/pre_play_attempt3_MUGGEE.png
?? debug/tile_placer/pre_play_attempt3_OGEED.png
?? debug/tile_placer/pre_play_attempt3_OOM.png
?? debug/tile_placer/pre_play_attempt3_OUTRAGE.png
?? debug/tile_placer/pre_play_attempt3_OVERMEN.png
?? debug/tile_placer/pre_play_attempt3_PAN.png
?? debug/tile_placer/pre_play_attempt3_PI.png
?? debug/tile_placer/pre_play_attempt3_PLAINTS.png
?? debug/tile_placer/pre_play_attempt3_PODOMERE.png
?? debug/tile_placer/pre_play_attempt3_POLK.png
?? debug/tile_placer/pre_play_attempt3_PRICED.png
?? debug/tile_placer/pre_play_attempt3_PUIR.png
?? debug/tile_placer/pre_play_attempt3_QANAT.png
?? debug/tile_placer/pre_play_attempt3_QUATE.png
?? debug/tile_placer/pre_play_attempt3_RAGED.png
?? debug/tile_placer/pre_play_attempt3_RESIDE.png
?? debug/tile_placer/pre_play_attempt3_RORTS.png
?? debug/tile_placer/pre_play_attempt3_SEDATING.png
?? debug/tile_placer/pre_play_attempt3_TANE.png
?? debug/tile_placer/pre_play_attempt3_TAY.png
?? debug/tile_placer/pre_play_attempt3_TROTS.png
?? debug/tile_placer/pre_play_attempt3_TYE.png
?? debug/tile_placer/pre_play_attempt3_VERA.png
?? debug/tile_placer/pre_play_attempt3_VORS.png
?? debug/tile_placer/pre_play_attempt3_WAREZ.png
?? debug/tile_placer/pre_play_attempt3_WEEM.png
?? debug/tile_placer/pre_play_attempt3_WIDGET.png
?? debug/tile_placer/pre_play_attempt3_WOO.png
?? debug/tile_placer/pre_play_attempt3_YE.png
?? debug/tile_placer/pre_play_attempt3_YEARNING.png
?? debug/tile_placer/pre_play_attempt3_YOU.png
?? debug/tile_placer/pre_play_attempt3_YOUR.png
?? debug/tile_placer/pre_play_attempt4_DATO.png
?? debug/tile_placer/pre_play_attempt4_DEP.png
?? debug/tile_placer/pre_play_attempt4_DISHFUL.png
?? debug/tile_placer/pre_play_attempt4_EIDER.png
?? debug/tile_placer/pre_play_attempt4_EQUATOR.png
?? debug/tile_placer/pre_play_attempt4_FE.png
?? debug/tile_placer/pre_play_attempt4_FER.png
?? debug/tile_placer/pre_play_attempt4_FEY.png
?? debug/tile_placer/pre_play_attempt4_FUGS.png
?? debug/tile_placer/pre_play_attempt4_GAZE.png
?? debug/tile_placer/pre_play_attempt4_GLUEY.png
?? debug/tile_placer/pre_play_attempt4_GRATE.png
?? debug/tile_placer/pre_play_attempt4_GRIDE.png
?? debug/tile_placer/pre_play_attempt4_HIS.png
?? debug/tile_placer/pre_play_attempt4_IWI.png
?? debug/tile_placer/pre_play_attempt4_JAP.png
?? debug/tile_placer/pre_play_attempt4_JUGS.png
?? debug/tile_placer/pre_play_attempt4_KUIA.png
?? debug/tile_placer/pre_play_attempt4_LEGGE.png
?? debug/tile_placer/pre_play_attempt4_MAIZE.png
?? debug/tile_placer/pre_play_attempt4_MEG.png
?? debug/tile_placer/pre_play_attempt4_MIGGLE.png
?? debug/tile_placer/pre_play_attempt4_OY.png
?? debug/tile_placer/pre_play_attempt4_PFUI.png
?? debug/tile_placer/pre_play_attempt4_QAT.png
?? debug/tile_placer/pre_play_attempt4_RAGE.png
?? debug/tile_placer/pre_play_attempt4_RATE.png
?? debug/tile_placer/pre_play_attempt4_RONTS.png
?? debug/tile_placer/pre_play_attempt4_SLAINTE.png
?? debug/tile_placer/pre_play_attempt4_SOV.png
?? debug/tile_placer/pre_play_attempt4_TORTS.png
?? debug/tile_placer/pre_play_attempt4_UNITY.png
?? debug/tile_placer/pre_play_attempt4_VENA.png
?? debug/tile_placer/pre_play_attempt4_YATE.png
?? debug/tile_placer/pre_play_attempt4_YEA.png
?? debug/tile_placer/pre_play_attempt4_YEAR.png
?? debug/tile_placer/pre_play_attempt4_YO.png
?? debug/tile_placer/pre_play_attempt4_ZARF.png
?? debug/tile_placer/pre_play_attempt5_ANTE.png
?? debug/tile_placer/pre_play_attempt5_AY.png
?? debug/tile_placer/pre_play_attempt5_CAHOOTS.png
?? debug/tile_placer/pre_play_attempt5_FAZE.png
?? debug/tile_placer/pre_play_attempt5_FUJIS.png
?? debug/tile_placer/pre_play_attempt5_GJUS.png
?? debug/tile_placer/pre_play_attempt5_GLIME.png
?? debug/tile_placer/pre_play_attempt5_IF.png
?? debug/tile_placer/pre_play_attempt5_JAG.png
?? debug/tile_placer/pre_play_attempt5_JEU.png
?? debug/tile_placer/pre_play_attempt5_OUTEAT.png
?? debug/tile_placer/pre_play_attempt5_PIR.png
?? debug/tile_placer/pre_play_attempt5_RUGATE.png
?? debug/tile_placer/pre_play_attempt5_SIDH.png
?? debug/tile_placer/pre_play_attempt5_TOEY.png
?? debug/tile_placer/pre_play_attempt5_TORRS.png
?? debug/tile_placer/pre_play_attempt5_TOY.png
?? debug/tile_placer/pre_play_attempt5_TROT.png
?? debug/tile_placer/pre_play_attempt5_URP.png
?? debug/tile_placer/pre_play_attempt5_VARE.png
?? debug/tile_placer/pre_play_attempt5_VOR.png
?? debug/tile_placer/pre_play_attempt5_WAUK.png
?? debug/tile_placer/pre_play_attempt5_WEB.png
?? debug/tile_placer/pre_play_attempt5_WIGGLE.png
?? debug/tile_placer/pre_play_attempt5_YA.png
?? debug/tile_placer/pre_play_attempt5_YEAN.png
?? debug/turn_detection/frame_20260503_223115_507963_pre_start_attempt1.png
?? debug/turn_detection/frame_20260503_233616_632456_pre_start_attempt1.png
?? debug/turn_detection/frame_20260503_234731_800800_pre_start_attempt1.png
?? debug/turn_detection/frame_20260504_003844_025327_pre_start_attempt1.png
?? debug/turn_detection/frame_20260504_004243_566671_pre_start_attempt1.png
?? debug/turn_detection/frame_20260504_010118_725200_pre_start_attempt1.png
?? debug/turn_detection/frame_20260504_120246_494048_pre_start_attempt1.png
?? debug/turn_detection/frame_20260504_124139_325957_pre_start_attempt1.png
?? debug/turn_detection/frame_20260504_125218_496629_pre_start_attempt1.png
?? debug/turn_detection/frame_20260504_132451_848706_pre_start_attempt1.png
?? debug/turn_detection/frame_20260504_135804_512835_preflight.png
?? debug/turn_detection/frame_20260504_135923_986702_pre_start_attempt1.png
?? logs/_autoplay_stderr.tmp
?? logs/auto_debug_console.prev.log
?? logs/auto_debug_console.prev2.log
?? logs/auto_debug_console.prev3.log
?? logs/autoplay.2026-05-03_20-13-32_300969.log
```

## git diff --stat
```
.gitignore                                  |     2 +-
 TESTING_REPORT.md                           |   409 -
 data/rejected_words.txt                     |   569 +-
 debug/iframe_missing.png                    |   Bin 135250 -> 207414 bytes
 debug/preprocessed_debug.png                |   Bin 383175 -> 416476 bytes
 debug/tile_placer/post_recall_attempt1.png  |   Bin 15698 -> 130958 bytes
 debug/tile_placer/post_recall_attempt2.png  |   Bin 121791 -> 130481 bytes
 debug/tile_placer/post_recall_attempt3.png  |   Bin 122711 -> 131272 bytes
 debug/tile_placer/post_recall_attempt4.png  |   Bin 122785 -> 118589 bytes
 debug/tile_placer/post_recall_attempt5.png  |   Bin 123531 -> 117675 bytes
 debug/tile_placer/pre_play_attempt1_ST.png  |   Bin 112348 -> 121462 bytes
 debug/tile_placer/pre_play_attempt2_ENE.png |   Bin 120152 -> 118475 bytes
 logs/auto_debug.log                         |    82 +-
 logs/auto_debug_console.log                 |    82 +-
 logs/auto_debug_iter_001.md                 |  2218 +-
 logs/auto_debug_iter_001_response.md        |    10 +-
 logs/auto_debug_iter_002.md                 |   910 +-
 logs/auto_debug_iter_002_response.md        |     7 +
 logs/autoplay.log                           | 41531 ++++++++------------------
 scripts/auto_debug.py                       |   517 +-
 scripts/autoplay_headless.py                |    27 +-
 src/browser/navigator.py                    |   114 +-
 src/browser/tile_placer.py                  |    28 +-
 src/vision/__init__.py                      |    83 +-
 24 files changed, 13652 insertions(+), 32937 deletions(-)
```