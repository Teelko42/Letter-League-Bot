All 35 tests pass.

## Report

**Root cause**: Two unbounded Playwright hangs ate the auto_debug 30-min run-timeout. (1) `iframe_locator.screenshot(timeout=15_000)` in `capture.py:124` blocked for ~15 minutes after the iframe quietly died — the Node side reported `Timeout -873596ms exceeded` (Playwright's internal deadline tracking went negative and `setTimeout(-873596)` was clamped to 1ms by Node), so the RPC never honoured the 15s limit. (2) `_run_navigation` in `navigator.py` then hung for ~30 minutes between `page.goto()` and the next Playwright call during recovery. Combined, these consumed the entire run budget so the bot only completed turn 4 plus a swap before the subprocess was killed.

**Files changed**:
- `src/browser/capture.py` — wrapped the `iframe_locator.screenshot` call with `asyncio.wait_for(..., 20.0)` and re-raise asyncio.TimeoutError as a RuntimeError whose message contains `Locator.screenshot` so the existing `_is_iframe_dead_error` classifier in `autoplay_headless.py` matches and triggers re-navigation.
- `src/browser/navigator.py` — wrapped each `_run_navigation` retry attempt in `asyncio.wait_for(..., 120.0)` so a wedged Playwright session can't burn 30 minutes on a single attempt; the existing 3-retry loop now sees the timeout as a normal failure and retries.

**Why next run does better**: The pathological 15-min screenshot hang now fires the iframe-dead recovery in 20s, and re-navigation has a 2-min ceiling per attempt (well under the 30-min run-timeout). Recovery still has its existing 2-recovery cap, so a truly dead browser exits to fresh process — but a transient iframe glitch (the most common case) now costs ~140s instead of ~45 minutes, leaving plenty of budget to reach `--max-turns 5`.
