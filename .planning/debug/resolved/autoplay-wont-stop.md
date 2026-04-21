---
status: verifying
trigger: "autoplay acknowledges stop command but keeps running"
created: 2026-04-14T00:00:00Z
updated: 2026-04-14T00:00:00Z
---

## Current Focus

hypothesis: poll_turn() runs an infinite while True loop with no stop_event check, so it can block for up to POLL_SLOW_S (5s) or MAX_IDLE_S (300s) indefinitely — the outer while not self._stop_event.is_set() check is never re-evaluated until poll_turn() returns
test: confirmed by reading autoplay_cog.py lines 203-276 and turn_detector.py lines 393-443
expecting: fix = pass stop_event into poll_turn and check it on each sleep iteration OR cancel the task
next_action: implement fix — pass stop_event into poll_turn, check it before each asyncio.sleep

## Symptoms

expected: When the stop command is issued, autoplay should stop its game loop and become idle.
actual: The stop command is acknowledged (bot responds) but autoplay continues running. The bot must be restarted to recover.
errors: No crash or error — it just keeps going despite the stop acknowledgment.
reproduction: Start autoplay, then issue the stop command. Autoplay continues running.
started: Unknown — may have never worked correctly.

## Eliminated

(none yet)

## Evidence

- timestamp: 2026-04-14T00:01:00Z
  checked: autoplay_cog.py _run_game_loop lines 203-276
  found: The outer while loop is `while not self._stop_event.is_set()` — correct. But the FIRST thing inside the loop is `await poll_turn(page)`, which can block indefinitely. The stop_event is only re-evaluated after poll_turn() returns.
  implication: Setting the stop_event during a poll_turn() call has no effect until poll_turn() naturally returns — which could take up to MAX_IDLE_S = 300 seconds (5 minutes).

- timestamp: 2026-04-14T00:01:01Z
  checked: turn_detector.py poll_turn() lines 393-443
  found: poll_turn() is an infinite `while True:` loop. It sleeps POLL_FAST_S (1.5s) or POLL_SLOW_S (5.0s) per iteration using asyncio.sleep(). It has zero awareness of any external stop signal. It only returns when state is "my_turn", "game_over", or "idle_timeout".
  implication: Even if _stop_event is set immediately after a turn completes, the loop will continue until poll_turn() detects a turn (could be up to 5 minutes of waiting for the opponent). During that entire wait, the stop command is acknowledged but completely ignored.

- timestamp: 2026-04-14T00:01:02Z
  checked: autoplay_cog.py autoplay_stop() lines 117-131
  found: stop() correctly sets self._stop_event and responds to the user. The issue is not in the stop command handler but in poll_turn() not respecting the event.
  implication: The stop is acknowledged (bot says "Finishing current turn, then stopping") but the game loop is stuck inside poll_turn() waiting for the opponent. It will not stop until either the opponent moves or MAX_IDLE_S expires.

## Resolution

root_cause: poll_turn() in turn_detector.py contained an infinite while True loop with no mechanism to observe the stop_event. The outer game loop in autoplay_cog.py checks stop_event at the while condition, but immediately awaits poll_turn() — which can block for up to POLL_SLOW_S (5s) per iteration or MAX_IDLE_S (300s) total waiting for the opponent. Setting stop_event during this await had zero effect until poll_turn() naturally returned.

fix: Added optional stop_event: asyncio.Event | None = None parameter to poll_turn(). Introduced _interruptible_sleep() helper inside poll_turn() that uses asyncio.wait_for(asyncio.shield(stop_event.wait()), timeout=seconds) to wake early when the event fires. All three asyncio.sleep() calls inside poll_turn() replaced with _interruptible_sleep(); each returns "stop_requested" if the event fired. A guard check at the top of each iteration handles the event being set before sleeping. TurnState literal extended with "stop_requested". autoplay_cog.py passes self._stop_event to poll_turn() and breaks the loop immediately on "stop_requested".

verification: 35/35 tests pass including 3 new TestPollTurnStopEvent tests and 1 new test_stop_during_poll_turn_exits_cleanly test confirming the fix.

files_changed:
  - src/browser/turn_detector.py
  - src/bot/autoplay_cog.py
  - tests/test_turn_detector.py
  - tests/test_autoplay_cog.py
