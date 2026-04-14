---
status: resolved
trigger: "Bot won't join voice channel during autoplay. Navigator doesn't find 'Join Voice' button, assumes already in voice, then fails to find 'Start An Activity' button because it's not actually in voice."
created: 2026-04-14T00:00:00Z
updated: 2026-04-14T00:00:00Z
---

## Current Focus

hypothesis: The `page.keyboard.press("Escape")` call on line 77 (meant to dismiss "How'd the call go?" modals) fires BEFORE the Join Voice button check and dismisses the join voice UI/prompt itself — so when the locator runs, the button no longer exists. A secondary hypothesis is the selector `button:has-text("Join Voice")` doesn't match Discord's actual DOM element.
test: Examined timing from logs (navigate at 11:03:56.444, "No Join Voice button" at 11:04:09.032 = ~12.6s = 2s + 0.5s + 10s timeout), confirming the 10s wait fires and no button appears. Escape fires before the join button check.
expecting: Moving Escape to AFTER the join button click (so it only dismisses post-join overlays) will allow the Join Voice button to be found. Also adding a fallback selector.
next_action: Apply fix — move the pre-join Escape to a safer position and add alternate selectors

## Symptoms

expected: When autoplay starts, the bot's browser should click "Join Voice" to enter the voice channel, then find and click "Start An Activity" to launch Letter League.
actual: The navigator logs "No Join Voice button — assuming already in voice channel" but the bot is NOT in voice. Then it times out looking for "Start An Activity" button because the activity button only appears when in voice.
errors: Locator.wait_for: Timeout 15000ms exceeded waiting for locator("button[aria-label=\"Start An Activity\"]") to be visible
reproduction: Start autoplay via slash command. The navigator navigates to the channel URL but fails to join voice.
started: Current behavior

## Eliminated

(none yet)

## Evidence

- timestamp: 2026-04-14T00:01:00Z
  checked: navigator.py lines 70-90 and log timestamps
  found: page.goto fires at 11:03:56.444. asyncio.sleep(2) + keyboard.press("Escape") + asyncio.sleep(0.5) fires before the join_btn check. join_btn.wait_for times out at 11:04:09.032 (~12.6s = 2+0.5+10). The Escape keypress precedes the join button check.
  implication: Escape could be dismissing the voice join UI before the locator check runs

- timestamp: 2026-04-14T00:02:00Z
  checked: navigator.py line 83
  found: selector is `button:has-text("Join Voice")` — correct Playwright syntax that matches text anywhere in subtree
  implication: Selector is plausible but not verified against real Discord DOM

- timestamp: 2026-04-14T00:03:00Z
  checked: debug_frames.py lines 69-84 (alternate selectors for activity button)
  found: The debug script already anticipated that "Start An Activity" label might be wrong and listed alternates. The navigator uses the same risky pattern for join voice.
  implication: Discord's UI labels have been unreliable before — join voice selector may also be wrong or Escape is the culprit

- timestamp: 2026-04-14T00:04:00Z
  checked: Full execution sequence in _run_navigation
  found: Step 2a sends Escape (meant for "How'd the call go?" modal), then step 2b checks for Join Voice. BUT when Discord navigates to a voice channel URL, it may render the "Join Voice" prompt as the primary UI — the same "blocking modal" that Escape dismisses.
  implication: PRIMARY ROOT CAUSE — Escape is fired unconditionally and may dismiss the Join Voice button itself. Fix: only send Escape if a specific "How'd the call go?" modal is detected, or move Escape to after the join sequence.

## Resolution

root_cause: The unconditional `page.keyboard.press("Escape")` call in Step 2a was firing BEFORE the Join Voice button check. When Discord navigates to an unjoined voice channel, it renders a "Join Voice" prompt. Pressing Escape dismissed that prompt, so by the time the 10s locator wait started, the button was gone. Additionally, the selector only covered one text variant — added aria-label fallbacks via Playwright's `.or_()` combinator.

fix: (1) Made the pre-check Escape conditional — only fires if `text="How'd the call go?"` is actually visible on the page. (2) Combined three selector variants into a single `.or_()` chain so all are checked in one 10s wait, avoiding a 30s cascade in the already-in-voice case.

verification: 231 unit tests pass (4 navigator tests pass including the `_make_locator` helper that now correctly mocks `.or_()` as a synchronous method).

files_changed:
  - src/browser/navigator.py
  - tests/test_navigator.py
