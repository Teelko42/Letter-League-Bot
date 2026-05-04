# Auto-debug iteration 9

- exit_code: `-9`
- duration: 114536.1s
- error_signature: `62b26e713bbc`

## Recent debug artifacts
- `debug/tile_placer/post_recall_attempt1.png`
- `debug/tile_placer/post_recall_attempt4.png`
- `debug/tile_placer/pre_play_attempt4_ZOO.png`
- `debug/turn_detection/frame_20260430_020406_119332_pre_start_attempt1.png`
- `debug/turn_detection/frame_20260428_181722_695879_pre_start_attempt1.png`
- `debug/iframe_missing.png`

## Autoplay log — error region
```
2026-04-28 18:29:21.189 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.0000
2026-04-28 18:29:21.189 | WARNING | src.browser.tile_placer:place_tiles:703 | Tile 'U' placement not verified — retrying with fresh jitter
2026-04-28 18:29:21.696 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 14977 bytes (attempt 1)
2026-04-28 18:29:23.568 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 14977 bytes (attempt 1)
2026-04-28 18:29:23.736 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.0000
2026-04-28 18:29:23.798 | ERROR   | src.browser.tile_placer:place_move:1061 | Tile placement failed for 'FUZIL' (attempt 1): Tile 'U' at (6,16) failed to place after retry
2026-04-28 18:29:24.183 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-28 18:29:24.183 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1284.8, 748.0) (pass 1/9)
2026-04-28 18:29:24.992 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1285.8, 750.7) (pass 2/9)
2026-04-28 18:29:25.904 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1284.9, 752.6) (pass 3/9)
2026-04-28 18:29:26.782 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1288.5, 753.6) (pass 4/9)
2026-04-28 18:29:27.613 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1286.8, 750.7) (pass 5/9)
2026-04-30 02:01:18.501 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1286.5, 748.7) (pass 6/9)
2026-04-30 02:01:20.195 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1285.1, 753.4) (pass 7/9)
2026-04-30 02:01:22.155 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1286.6, 753.8) (pass 8/9)
2026-04-30 02:01:23.009 | INFO    | src.browser.tile_placer:_recall_tiles:896 | Clicking recall button at (1288.5, 749.1) (pass 9/9)
2026-04-30 02:01:29.533 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 15698 bytes (attempt 1)
2026-04-30 02:01:29.548 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:849 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-04-30 02:01:29.549 | INFO    | src.browser.tile_placer:place_move:1050 | Word attempt 2/4: 'IGLU' (score=22)
2026-04-30 02:01:30.536 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:407 | Using iframe bbox: 1545x768 @ (375,112)
2026-04-30 02:01:30.536 | INFO    | src.browser.tile_placer:place_tiles:682 | Placing tile 'I' (slot 5) -> board (8,12) | src=(1257.9,827.4) dst=(1092.6,458.4)
2026-04-30 02:01:33.345 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 15698 bytes (attempt 1)
2026-04-30 02:01:35.608 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 15698 bytes (attempt 1)
2026-04-30 02:01:35.950 | DEBUG   | src.browser.tile_placer:_verify_placement:628 | Placement pixel diff: 0.0000
2026-04-30 02:01:35.966 | WARNING | src.browser.tile_placer:place_tiles:703 | Tile 'I' placement not verified — retrying with fresh jitter
2026-04-30 02:01:37.279 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 15698 bytes (attempt 1)
2026-04-30 02:02:00.110 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:38 | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
2026-04-30 02:02:02.541 | WARNING | src.browser.capture:_log_iframe_missing_diagnostic:46 | Viewport screenshot saved -> debug\iframe_missing.png
2026-04-30 02:02:02.542 | WARNING | __main__:_run:222 | place_move raised: Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)
2026-04-30 02:02:02.542 | ERROR   | __main__:_run:224 | place_move hit iframe-dead error — re-navigating: Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)
2026-04-30 02:02:02.543 | WARNING | __main__:_recover_iframe:140 | Iframe dead (1/2) — re-navigating: Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)
2026-04-30 02:02:08.289 | INFO    | src.browser.navigator:_run_navigation:82 | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
2026-04-30 02:02:28.835 | INFO    | src.browser.navigator:_run_navigation:125 | No Join Voice button found — assuming already in voice channel
2026-04-30 02:02:51.103 | WARNING | src.browser.navigator:navigate_to_activity:53 | Navigation attempt 1/3 failed: Locator.wait_for: Timeout 15000ms exceeded.
Call log:
  - waiting for locator("button[aria-label=\"Start An Activity\"]") to be visible
  - waiting for locator("button[aria-label=\"Start An Activity\"]")
. Retrying in 3 seconds...
2026-04-30 02:02:56.292 | INFO    | src.browser.navigator:_run_navigation:82 | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
2026-04-30 02:03:16.185 | INFO    | src.browser.navigator:_run_navigation:121 | Join Voice button found — clicking to join voice channel
2026-04-30 02:03:23.702 | INFO    | src.browser.navigator:_run_navigation:137 | Opened Activity shelf
2026-04-30 02:03:31.133 | INFO    | src.browser.navigator:_run_navigation:158 | Selected Letter League from shelf
2026-04-30 02:03:36.001 | INFO    | src.browser.navigator:_run_navigation:165 | Clicked Play — launching activity
2026-04-30 02:03:40.143 | INFO    | src.browser.navigator:_run_navigation:179 | Activity iframe found: https://879863686565621790.discordsays.com/?instance_id=i-1499305204376670279-gc-1486201751353819208-1486201752477761590&location_id=gc-1486201751353819208-1486201752477761590&launch_id=1499305204376670279&referrer_id=undefined&custom_id=undefined&discord_proxy_ticket=faux-proxy-ticket&guild_id=1486201751353819208&channel_id=1486201752477761590&frame_id=cf406e64-5499-4ad7-8adf-25d2e09e2461&platform=desktop
2026-04-30 02:03:42.027 | INFO    | src.browser.navigator:_hide_chat_panel:200 | Chat panel already hidden
2026-04-30 02:03:42.575 | INFO    | src.browser.capture:capture_canvas:113 | Activity iframe verified visible
2026-04-30 02:03:54.828 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 10655 bytes (attempt 1)
2026-04-30 02:04:01.764 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 108719 bytes (attempt 1)
2026-04-30 02:04:06.028 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 108464 bytes (attempt 1)
```

## Subprocess stderr (tail)
```
[32m18:29:19[0m | [1mINFO   [0m | Vision pipeline complete — 13.86s  tiles=2  rack_size=7
[32m18:29:19[0m | [1mINFO   [0m | Word attempt 1/4: 'FUZIL' (score=23)
[32m18:29:19[0m | [1mINFO   [0m | Placing tile 'U' (slot 6) -> board (6,16) | src=(1309.6,831.2) dst=(1299.9,392.8)
[32m18:29:21[0m | [33m[1mWARNING[0m | Tile 'U' placement not verified — retrying with fresh jitter
[32m18:29:23[0m | [31m[1mERROR  [0m | Tile placement failed for 'FUZIL' (attempt 1): Tile 'U' at (6,16) failed to place after retry
[32m18:29:24[0m | [1mINFO   [0m | Clicking recall button at (1284.8, 748.0) (pass 1/9)
[32m18:29:24[0m | [1mINFO   [0m | Clicking recall button at (1285.8, 750.7) (pass 2/9)
[32m18:29:25[0m | [1mINFO   [0m | Clicking recall button at (1284.9, 752.6) (pass 3/9)
[32m18:29:26[0m | [1mINFO   [0m | Clicking recall button at (1288.5, 753.6) (pass 4/9)
[32m18:29:27[0m | [1mINFO   [0m | Clicking recall button at (1286.8, 750.7) (pass 5/9)
[32m02:01:18[0m | [1mINFO   [0m | Clicking recall button at (1286.5, 748.7) (pass 6/9)
[32m02:01:20[0m | [1mINFO   [0m | Clicking recall button at (1285.1, 753.4) (pass 7/9)
[32m02:01:22[0m | [1mINFO   [0m | Clicking recall button at (1286.6, 753.8) (pass 8/9)
[32m02:01:23[0m | [1mINFO   [0m | Clicking recall button at (1288.5, 749.1) (pass 9/9)
[32m02:01:29[0m | [1mINFO   [0m | Word attempt 2/4: 'IGLU' (score=22)
[32m02:01:30[0m | [1mINFO   [0m | Placing tile 'I' (slot 5) -> board (8,12) | src=(1257.9,827.4) dst=(1092.6,458.4)
[32m02:01:35[0m | [33m[1mWARNING[0m | Tile 'I' placement not verified — retrying with fresh jitter
[32m02:02:00[0m | [33m[1mWARNING[0m | Iframe screenshot failed — page.url='https://discord.com/channels/1486201751353819208/1486201752477761590', 2 frames attached: ['https://discord.com/channels/1486201751353819208/1486201752477761590', 'about:blank']
[32m02:02:02[0m | [33m[1mWARNING[0m | Viewport screenshot saved -> debug\iframe_missing.png
[32m02:02:02[0m | [33m[1mWARNING[0m | place_move raised: Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)
[32m02:02:02[0m | [31m[1mERROR  [0m | place_move hit iframe-dead error — re-navigating: Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)
[32m02:02:02[0m | [33m[1mWARNING[0m | Iframe dead (1/2) — re-navigating: Locator.screenshot: hard timeout exceeded — iframe likely dead (asyncio.wait_for fired after Playwright RPC stalled)
[32m02:02:08[0m | [1mINFO   [0m | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
[32m02:02:28[0m | [1mINFO   [0m | No Join Voice button found — assuming already in voice channel
[32m02:02:51[0m | [33m[1mWARNING[0m | Navigation attempt 1/3 failed: Locator.wait_for: Timeout 15000ms exceeded.
Call log:
  - waiting for locator("button[aria-label=\"Start An Activity\"]") to be visible
  - waiting for locator("button[aria-label=\"Start An Activity\"]")
. Retrying in 3 seconds...
[32m02:02:56[0m | [1mINFO   [0m | Navigated to channel: https://discord.com/channels/1486201751353819208/1486201752477761590
[32m02:03:16[0m | [1mINFO   [0m | Join Voice button found — clicking to join voice channel
[32m02:03:23[0m | [1mINFO   [0m | Opened Activity shelf
[32m02:03:31[0m | [1mINFO   [0m | Selected Letter League from shelf
[32m02:03:36[0m | [1mINFO   [0m | Clicked Play — launching activity
[32m02:03:40[0m | [1mINFO   [0m | Activity iframe found: https://879863686565621790.discordsays.com/?instance_id=i-1499305204376670279-gc-1486201751353819208-1486201752477761590&location_id=gc-1486201751353819208-1486201752477761590&launch_id=1499305204376670279&referrer_id=undefined&custom_id=undefined&discord_proxy_ticket=faux-proxy-ticket&guild_id=1486201751353819208&channel_id=1486201752477761590&frame_id=cf406e64-5499-4ad7-8adf-25d2e09e2461&platform=desktop
[32m02:03:42[0m | [1mINFO   [0m | Chat panel already hidden
[32m02:03:42[0m | [1mINFO   [0m | Activity iframe verified visible
[32m02:04:06[0m | [1mINFO   [0m | ensure_game_started: lobby detected — clicking START GAME (attempt 1/4)
[32m02:04:06[0m | [1mINFO   [0m | Clicking START GAME button at iframe-relative (1347.2, 721.9) / page (1722.2, 833.9)
[32m02:04:12[0m | [1mINFO   [0m | Game started — initial state: my_turn
[32m02:04:20[0m | [1mINFO   [0m | ensure_game_started: game started — initial state: my_turn
[32m02:04:20[0m | [1mINFO   [0m | Reached max_turns=5 — exiting cleanly
[32m02:04:25[0m | [1mINFO   [0m | Headless autoplay finished in 114492.2s
Exception ignored in: <function _ProactorBasePipeTransport.__del__ at 0x0000019EA5E01F80>
Traceback (most recent call last):
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\proactor_events.py", line 116, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
Exception ignored in: <function BaseSubprocessTransport.__del__ at 0x0000019EA5E00540>
Traceback (most recent call last):
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\base_subprocess.py", line 129, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\base_subprocess.py", line 73, in __repr__
    info.append(f'stdin={stdin.pipe}')
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
Exception ignored in: <function _ProactorBasePipeTransport.__del__ at 0x0000019EA5E01F80>
Traceback (most recent call last):
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\proactor_events.py", line 116, in __del__
    _warn(f"unclosed transport {self!r}", ResourceWarning, source=self)
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\proactor_events.py", line 80, in __repr__
    info.append(f'fd={self._sock.fileno()}')
  File "C:\Users\Ninja\AppData\Local\Programs\Python\Python313\Lib\asyncio\windows_utils.py", line 102, in fileno
    raise ValueError("I/O operation on closed pipe")
ValueError: I/O operation on closed pipe
Future exception was never retrieved
future: <Future finished exception=TimeoutError('Timeout 30000ms exceeded.\nCall log:\n  2 × waiting for locator("iframe[src*=\\"discordsays.com\\"]")\n')>
patchright._impl._errors.TimeoutError: Timeout 30000ms exceeded.
Call log:
  2 × waiting for locator("iframe[src*=\"discordsays.com\"]")


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
?? debug/tile_placer/pre_play_attempt1_FEZES.png
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
?? debug/tile_placer/pre_play_attempt1_GLITZ.png
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
?? debug/tile_placer/pre_play_attempt1_OCTAVE.png
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
?? debug/tile_placer/pre_play_attempt1_SWIZ.png
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
?? debug/tile_placer/pre_play_attempt1_WIG.png
?? debug/tile_placer/pre_play_attempt1_WIZ.png
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
?? debug/tile_placer/pre_play_attempt2_WIGGLE.png
?? debug/tile_placer/pre_play_attempt2_WINGLET.png
?? debug/tile_placer/pre_play_attempt2_WUZ.png
?? debug/tile_placer/pre_play_attempt2_YAGI.png
?? debug/tile_placer/pre_play_attempt2_YEZ.png
?? debug/tile_placer/pre_play_attempt2_ZA.png
?? debug/tile_placer/pre_play_attempt2_ZAIRE.png
?? debug/tile_placer/pre_play_attempt2_ZOEAE.png
?? debug/tile_placer/pre_play_attempt2_ZOL.png
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
?? debug/tile_placer/pre_play_attempt3_LUGGIE.png
?? debug/tile_placer/pre_play_attempt3_LUTZ.png
?? debug/tile_placer/pre_play_attempt3_LUZ.png
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
?? debug/tile_placer/pre_play_attempt3_WILT.png
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
?? debug/tile_placer/pre_play_attempt4_CUZ.png
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
?? debug/tile_placer/pre_play_attempt4_ZEL.png
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
?? debug/tile_placer/pre_play_attempt5_LEZ.png
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
?? debug/tile_placer/pre_play_attempt5_ZIT.png
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
?? debug/turn_detection/frame_20260428_181722_695879_pre_start_attempt1.png
?? debug/turn_detection/frame_20260430_020406_119332_pre_start_attempt1.png
?? logs/
?? scripts/auto_debug.py
?? scripts/autoplay_headless.py
?? src/engine/rejected_words.py
```

## git diff --stat
```
debug/preprocessed_debug.png               | Bin 371628 -> 383175 bytes
 debug/tile_placer/post_recall_attempt1.png | Bin 117178 -> 15698 bytes
 debug/tile_placer/post_recall_attempt2.png | Bin 120237 -> 121791 bytes
 debug/tile_placer/post_recall_attempt3.png | Bin 119929 -> 122711 bytes
 debug/tile_placer/post_recall_attempt4.png | Bin 119657 -> 122785 bytes
 debug/tile_placer/post_recall_attempt5.png | Bin 120024 -> 123531 bytes
 src/bot/autoplay_cog.py                    |  39 +++-
 src/browser/capture.py                     |  92 +++++++-
 src/browser/navigator.py                   |  17 +-
 src/browser/tile_placer.py                 | 354 ++++++++++++++++++++++++-----
 src/browser/turn_detector.py               | 192 +++++++++++++++-
 src/vision/__init__.py                     | 152 ++++++++++---
 tests/test_tile_placer.py                  |  79 ++++++-
 13 files changed, 804 insertions(+), 121 deletions(-)
```