Tests pass.

## Report

**Root cause:** The activity iframe died mid-game (around 11:14, then again at 11:25 after a `game_over → my_turn` transition where Discord dropped the `discordsays.com` frame). When that happened mid-turn, every `capture_canvas` call paid a ~30 s `wait_for(state="visible")` plus a ~30 s `Locator.screenshot` timeout. The `IframeDeadError` recovery in `scripts/autoplay_headless.py` only fires from `poll_turn`, and only after 5 consecutive failures (~5 min). In-turn paths — `clear_stale_placements`, the vision retry block, `place_move`, and the post-rejection re-vision — caught their own exceptions and silently `continue`'d, so the bot loop spent ~13 minutes burning timeouts before the auto-debug subprocess sent SIGKILL (exit code -9).

**Files changed:**
- `scripts/autoplay_headless.py` — added `_is_iframe_dead_error(exc)` helper that matches Playwright's iframe-loss signatures (`Locator.screenshot: Timeout`, `Element is not attached to the DOM`, `discordsays.com`/`iframe`); refactored the existing recovery into an inner `_recover_iframe(reason)` helper; wired it in at the vision retry, `place_move`, and post-rejection re-vision sites so any iframe-dead exception immediately re-navigates instead of looping into the next 30s timeout.
- `src/browser/turn_detector.py` — lowered `MAX_CAPTURE_FAILURES` from 5 → 3 so even when only `poll_turn` sees the dead iframe, recovery fires in ~3 min instead of ~5 min.

**Why next run will do better:** The single biggest time sink (vision attempt 1 fails, vision attempt 2 fails, skip turn, poll_turn fails 5×) collapses from ~7 min/cycle to a single ~60 s detection followed by `navigate_to_activity` + `ensure_game_started`. With `MAX_IFRAME_RECOVERIES=2` the bot still bounds itself, so a truly dead session still exits cleanly. Existing `tests/test_turn_detector.py` (23) and `tests/test_tile_placer.py` (23) all pass.
