---
phase: 05-browser-foundation
plan: "02"
subsystem: browser
tags: [navigation, canvas-capture, discord-activity, vision-pipeline]
dependency_graph:
  requires: ["05-01"]
  provides: ["navigate_to_activity", "capture_canvas", "is_non_blank", "scripts/browser_test.py"]
  affects: ["06-turn-detection"]
tech_stack:
  added: []
  patterns: ["FrameLocator canvas screenshot", "toDataURL fallback", "pixel-variance blank detection", "retry wrapper with backoff"]
key_files:
  created:
    - src/browser/navigator.py
    - src/browser/capture.py
    - scripts/browser_test.py
    - scripts/__init__.py
  modified:
    - src/browser/__init__.py
decisions:
  - "capture_canvas() keeps capture and vision separate — entry-point script calls both in sequence"
  - "Primary capture uses FrameLocator.screenshot(); falls back to frame.evaluate(toDataURL) on failure"
  - "is_non_blank() uses np.std() threshold of 5.0 for blank detection pre-check"
metrics:
  duration: "~2 min"
  completed: "2026-03-25"
  tasks_completed: 2
  tasks_total: 3
  files_created: 4
  files_modified: 1
requirements:
  - ANAV-01
  - ANAV-02
  - ANAV-03
---

# Phase 05 Plan 02: Discord Navigation and Canvas Capture Summary

**One-liner:** Discord voice channel navigation, Activity iframe discovery, and canvas screenshot capture with pixel-variance blank validation and toDataURL fallback wired to the vision pipeline.

## Status: AWAITING HUMAN VERIFICATION (Task 3)

Tasks 1 and 2 are complete and committed. Task 3 is a `checkpoint:human-verify` gate requiring live Discord testing.

## What Was Built

### Task 1: Navigator Module (`src/browser/navigator.py`)

`navigate_to_activity(page, channel_url, max_retries=3)` implements the full Discord navigation flow:

1. `page.goto(channel_url)` — navigate to the Discord voice channel
2. Check for "Join Voice" button and click if present (2s wait for voice panel)
3. Click `button[aria-label="Start an Activity"]` — opens the Activity shelf
4. Click "Letter League" text — launches the game
5. Poll `page.frames` every 0.5s for up to 30s looking for a frame whose URL matches `discordsays\.com`
6. Return the Frame object on success; raise RuntimeError on timeout

Wrapped in a retry loop: on any exception, waits 3s and retries up to `max_retries` times.

### Task 2: Capture Module (`src/browser/capture.py`) + Package + Entry-point

**`is_non_blank(img_bytes, threshold=5.0)`** — decodes image bytes via `cv2.imdecode`, returns `True` if `np.std(img) > threshold`. Guards against blank/uniform screenshots before the expensive vision pipeline call.

**`capture_canvas(page, frame, max_retries=3)`**:
- Waits for `networkidle` + 1s render buffer
- Primary: `page.frame_locator('iframe[src*="discordsays.com"]').locator("canvas").first.screenshot()`
- Fallback: `frame.evaluate("document.querySelector('canvas').toDataURL('image/png')")` with base64 decode
- Retries up to `max_retries` times (2s delay) on blank screenshots

**`src/browser/__init__.py`** — Updated to export `BrowserSession`, `navigate_to_activity`, `capture_canvas`, `is_non_blank`.

**`scripts/browser_test.py`** — Permanent entry-point artifact: `BrowserSession.start()` -> `navigate_to_activity()` -> `capture_canvas()` -> `extract_board_state()`. Satisfies the locked decision to validate the full vision pipeline at startup.

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| Task 1 | 8821732 | feat(05-02): create navigator module |
| Task 2 | 3191f55 | feat(05-02): create capture module, update browser exports, add entry-point script |

## Verification

All automated checks pass:

```
python -c "from src.browser import BrowserSession, navigate_to_activity, capture_canvas, is_non_blank; print('OK')"
# OK

python -c "from src.browser.navigator import navigate_to_activity; import inspect; sig = inspect.signature(navigate_to_activity); assert 'page' in sig.parameters and 'channel_url' in sig.parameters; print('Sig OK')"
# Sig OK

python -c "from src.browser.capture import is_non_blank; blank = bytes(100); assert not is_non_blank(blank); print('Blank check OK')"
# Blank check OK
```

Human verification (Task 3) is pending.

## Deviations from Plan

None — plan executed exactly as written.

The only deviation was in the plan's own verification command for Task 2: it used `node.name` on `ast.Name` objects (which have `id`, not `name`). This is a bug in the plan's verification script, not in the implementation. Confirmed via correct AST inspection that `extract_board_state` is called in `scripts/browser_test.py`.

## Self-Check: PASSED

All files exist on disk:
- FOUND: src/browser/navigator.py
- FOUND: src/browser/capture.py
- FOUND: src/browser/__init__.py
- FOUND: scripts/browser_test.py

All commits verified in git log:
- FOUND: 8821732
- FOUND: 3191f55
