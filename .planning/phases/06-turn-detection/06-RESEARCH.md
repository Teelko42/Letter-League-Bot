# Phase 6: Turn Detection - Research

**Researched:** 2026-03-26
**Domain:** Computer vision color detection (OpenCV/NumPy), async polling loop, state machine design
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Signal Discovery**
- The "my turn" indicator is an orange square banner with white "YOUR TURN" text at the top of the game canvas
- When it is the opponent's turn, the banner disappears entirely — absence of the banner = not my turn
- Detection uses pixel/color matching only — no OCR or text recognition
- Automated screenshot collection during a live game to calibrate the exact pixel region and orange color values

**Polling Behavior**
- Poll every 1-2 seconds initially
- Adaptive backoff: after ~30 seconds of "not my turn", gradually slow to ~5 second intervals
- Snap back to 1-2s polling immediately when a turn change is detected
- Quiet logging: only log when a turn state change occurs (my turn detected, game over detected), not every poll cycle
- On screenshot/capture failure: retry with exponential backoff before escalating

**Confidence & Safety**
- Strict confidence threshold — only trigger "my turn" when pixel match confidence is very high; better to miss one poll cycle than act out of turn
- Pre-flight calibration check: before entering the poll loop, verify the bot can see and detect the banner region in the expected screen area — fail early if the UI layout changed
- Save reference screenshots to disk (debug folder) during calibration and signal discovery for threshold tuning and future validation

**Game State Detection**
- Three recognized states: `my_turn`, `not_my_turn`, `game_over`
- Game-over detection: the game-over screen shows a leaderboard overlay in the center with players, winner on the right side, and the board on the left side — visually distinct from normal gameplay
- Game-over signal causes the detector to return a distinct state so downstream code can stop the loop

### Claude's Discretion
- Exact HSV/RGB thresholds for the orange banner color
- Pixel region detection algorithm (bounding box search, fixed region, etc.)
- Game-over detection method (could be leaderboard overlay detection, absence of game board, etc.)
- Backoff curve shape and exact timing
- Reference screenshot storage format and cleanup policy

### Deferred Ideas (OUT OF SCOPE)
- Post final game score to Discord when game ends — belongs in Phase 8 (Autonomous Game Loop)
- Detect opponent disconnection as a distinct state — handle via error recovery in Phase 8 if needed
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| TURN-01 | Bot detects when it is the active player via visual state polling and does not act out of turn | OpenCV HSV `cv2.inRange` on fixed ROI for orange banner; three-state enum (`my_turn`, `not_my_turn`, `game_over`); async polling loop with adaptive backoff; pre-flight calibration; strict confidence threshold |
</phase_requirements>

---

## Summary

Phase 6 is a pure computer-vision polling problem: capture a screenshot from the game canvas, crop to a fixed region at the top of the canvas where the orange "YOUR TURN" banner appears, run an HSV color-presence check, and return one of three states. The stack is entirely already installed: `opencv-python 4.13`, `numpy 2.2.6`, `loguru 0.7.3`, and `patchright 1.58.2` for canvas capture. No new dependencies are required.

The detection logic is deliberately simple — the orange banner is high-contrast against the rest of the game UI. OpenCV's `cv2.inRange()` on a fixed region of interest (ROI) is the standard approach for this class of problem and is already used in the project's vision pipeline (`preprocessor.py`). The confidence check is a simple pixel-count ratio: if more than N% of pixels in the banner ROI fall within the orange HSV range, return `my_turn`. The threshold must be calibrated from live screenshots, which the CONTEXT.md requires as part of signal discovery. Game-over detection uses a secondary HSV or structural check on a different region (leaderboard overlay area).

The polling loop is an `async def` coroutine in `src/browser/turn_detector.py` that calls `capture_canvas()` from Phase 5, classifies the state, applies adaptive backoff, and logs only on state transitions. This module is consumed by Phase 8's game loop. The phase includes a calibration script (`scripts/calibrate_turn.py`) that watches live gameplay, saves timestamped screenshots, and prints detected HSV values — this is the first task of Wave 1.

**Primary recommendation:** Use `cv2.inRange()` on a fixed ROI crop of the top ~15% of the canvas image. Calibrate HSV thresholds from ≥10 live screenshots before coding the detection function. Store thresholds as named constants in `turn_detector.py`.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| opencv-python | 4.13.0.92 | HSV color space conversion, `inRange` mask, pixel counting | Already installed; already used in `preprocessor.py` — identical pattern |
| numpy | 2.2.6 | Array operations, pixel ratio computation | Already installed; required by OpenCV |
| loguru | 0.7.3 | State-transition logging | Already installed; consistent with all other modules |
| patchright | 1.58.2 | Canvas screenshot capture (via `capture_canvas()`) | Already decided in Phase 5; reuse existing function |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pathlib | stdlib | Debug screenshot directory creation and path construction | Creating `debug/turn_detection/` folder |
| asyncio | stdlib | `asyncio.sleep()` for adaptive polling backoff | Already used throughout the browser module |
| datetime | stdlib | Timestamped filenames for saved debug screenshots | During calibration script |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `cv2.inRange` pixel-count ratio | Template matching (`cv2.matchTemplate`) | Template matching is sensitive to scale changes if Discord resizes the canvas; color-range is more robust to minor dimension drift |
| `cv2.inRange` pixel-count ratio | `cv2.matchTemplate` on "YOUR TURN" text crop | Would require a reference template image; breaks if Discord updates banner font/text; color approach is more maintainable |
| Fixed ROI crop | Full-frame contour search | Fixed ROI is faster (no contour computation) and safer (banner position is predictable at top of canvas) |
| Manual HSV constants | Dynamic threshold from histogram | Manual constants calibrated once from live screenshots are adequate for a static UI; dynamic approach adds complexity with no benefit |

**Installation:** No new packages required. All dependencies are already installed.

---

## Architecture Patterns

### Recommended Project Structure

```
src/
├── browser/
│   ├── __init__.py           # Add: is_my_turn, TurnState export
│   ├── session.py            # Unchanged
│   ├── navigator.py          # Unchanged
│   ├── capture.py            # Unchanged (reused by turn_detector)
│   └── turn_detector.py      # NEW: TurnState enum, _classify_frame(), poll_turn()
scripts/
├── calibrate_turn.py         # NEW: live calibration script, saves debug screenshots
debug/
└── turn_detection/           # Created at runtime — timestamped PNG screenshots
```

### Pattern 1: Fixed ROI Color-Presence Detection

**What:** Crop a fixed rectangular region from the canvas screenshot, convert to HSV, run `cv2.inRange()`, count white pixels in the mask, compare ratio against threshold.

**When to use:** When the signal has a known, stable screen position — exactly the case for the "YOUR TURN" banner at the top of the game canvas.

**Example:**
```python
# Source: opencv.org/blog/cropping-an-image-using-opencv + docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
import cv2
import numpy as np

# Calibrated from live screenshots (Wave 1 task — exact values TBD)
BANNER_HSV_LOWER = np.array([5, 120, 150])   # orange lower bound — PLACEHOLDER
BANNER_HSV_UPPER = np.array([20, 255, 255])  # orange upper bound — PLACEHOLDER
BANNER_ROI_Y_START = 0.00   # top of canvas (fraction of canvas height)
BANNER_ROI_Y_END   = 0.15   # bottom of banner region (fraction)
CONFIDENCE_THRESHOLD = 0.10  # 10% of ROI pixels must be orange — PLACEHOLDER

def classify_banner(img_bytes: bytes) -> bool:
    """Return True if the 'YOUR TURN' banner is present in the screenshot."""
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None:
        return False

    h, w = bgr.shape[:2]
    y0 = int(h * BANNER_ROI_Y_START)
    y1 = int(h * BANNER_ROI_Y_END)
    roi = bgr[y0:y1, :]   # full width, top N% of height

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, BANNER_HSV_LOWER, BANNER_HSV_UPPER)

    orange_ratio = np.count_nonzero(mask) / mask.size
    return orange_ratio >= CONFIDENCE_THRESHOLD
```

**Notes on HSV orange range:** OpenCV uses H: 0–179, S: 0–255, V: 0–255. Orange falls in H: 5–20 (approximating 10°–40° on standard 0°–360° wheel halved). Multiple authoritative sources agree on H:[10,25], S:[100,255], V:[20,255] as a starting point (source: GeeksforGeeks OpenCV inRange article, OpenCV official docs). The exact values MUST be calibrated from actual game screenshots — treat any pre-coded values as placeholders until Wave 1 calibration is complete.

### Pattern 2: Three-State Enum with TurnState

**What:** Use a `Literal` type or simple string constants to represent the three states, ensuring downstream phases have a typed contract.

**When to use:** Any time a function can return one of a fixed set of states — prevents downstream string comparison bugs.

```python
from typing import Literal

TurnState = Literal["my_turn", "not_my_turn", "game_over"]

def classify_frame(img_bytes: bytes) -> TurnState:
    """Classify a single canvas screenshot into a turn state."""
    # 1. Check game-over first (leaderboard overlay)
    if _is_game_over(img_bytes):
        return "game_over"
    # 2. Check for orange banner
    if classify_banner(img_bytes):
        return "my_turn"
    return "not_my_turn"
```

### Pattern 3: Adaptive Polling Loop

**What:** An async coroutine that polls at fast rate initially, slows down after a configurable idle duration, and snaps back to fast rate on state change.

**When to use:** When the event frequency is low and unknown (waiting for opponent turn), and you want to avoid wasting CPU on frequent polls during long waits.

```python
import asyncio
from loguru import logger

# Polling intervals
POLL_FAST_S = 1.5       # Default fast poll: 1-2 seconds (midpoint)
POLL_SLOW_S = 5.0       # Slow poll after idle threshold
IDLE_THRESHOLD_S = 30.0 # Start slowing after 30s same state
CAPTURE_RETRY_BASE = 1.0  # Base retry delay for capture failures

async def poll_turn(page) -> TurnState:
    """Poll until state changes from not_my_turn, or game_over is detected.

    Returns the detected TurnState when it is no longer not_my_turn.
    Caller is responsible for handling my_turn and game_over.
    """
    last_state: TurnState | None = None
    idle_duration = 0.0
    capture_backoff = CAPTURE_RETRY_BASE

    while True:
        # --- Capture with retry on failure ---
        try:
            img_bytes = await capture_canvas(page)
            capture_backoff = CAPTURE_RETRY_BASE  # reset on success
        except Exception as exc:
            logger.warning("Canvas capture failed: {}. Retrying in {:.1f}s", exc, capture_backoff)
            await asyncio.sleep(capture_backoff)
            capture_backoff = min(capture_backoff * 2, 30.0)  # cap at 30s
            continue

        # --- Classify state ---
        state = classify_frame(img_bytes)

        # --- Log only on state change ---
        if state != last_state:
            logger.info("Turn state changed: {} -> {}", last_state, state)
            last_state = state
            idle_duration = 0.0

        # --- Return if actionable ---
        if state in ("my_turn", "game_over"):
            return state

        # --- Adaptive backoff ---
        idle_duration += POLL_FAST_S if idle_duration < IDLE_THRESHOLD_S else POLL_SLOW_S
        interval = POLL_SLOW_S if idle_duration >= IDLE_THRESHOLD_S else POLL_FAST_S
        await asyncio.sleep(interval)
```

**Note:** The `backoff` PyPI library (litl/backoff) supports async coroutines and is the de-facto standard for retry logic. For this phase, hand-rolled exponential backoff on capture failure is simpler (no new dependency) and sufficient — the polling loop already handles the outer retry via `continue`.

### Pattern 4: Pre-Flight Calibration Check

**What:** Before entering the poll loop, run a single classification on a known "live game" screenshot to verify the detection pipeline works end-to-end. Fail fast if the environment has changed.

**When to use:** At bot startup, before any polling begins.

```python
async def preflight_check(page) -> None:
    """Verify turn detection pipeline is operational.

    Captures one frame and confirms it classifies as a valid game state
    (any state is acceptable — we just need non-crash classification).
    Saves the frame to debug/ for inspection.
    Raises RuntimeError if the screenshot cannot be captured or decoded.
    """
    img_bytes = await capture_canvas(page)
    state = classify_frame(img_bytes)
    _save_debug_screenshot(img_bytes, label="preflight")
    logger.info("Pre-flight turn detection check passed — initial state: {}", state)
```

### Pattern 5: Debug Screenshot Saving

**What:** Write PNG bytes to a timestamped file in a `debug/turn_detection/` directory during calibration.

**When to use:** In the calibration script and during preflight check.

```python
from pathlib import Path
from datetime import datetime

DEBUG_DIR = Path("debug/turn_detection")

def _save_debug_screenshot(img_bytes: bytes, label: str = "") -> Path:
    """Save screenshot bytes to debug directory with timestamp."""
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    suffix = f"_{label}" if label else ""
    path = DEBUG_DIR / f"frame_{ts}{suffix}.png"
    path.write_bytes(img_bytes)
    return path
```

### Pattern 6: Game-Over Detection

**What:** The game-over leaderboard overlay is visually distinct from gameplay — it features a large centered overlay. Detection can use one of:
1. **Color structure check:** Leaderboard overlay has a dark semi-transparent background unlike any normal game state; check for a large contiguous dark region covering most of the center of the frame.
2. **Absence of board colors:** The board's peach background (`BOARD_HSV_LOWER`/`BOARD_HSV_UPPER` from `preprocessor.py`) will still be visible (board is shown on the left) but the overall structure changes. A large dark overlay will reduce total orange/peach pixel count significantly.
3. **Approach recommended:** Treat as Claude's discretion — implement a simple check during calibration; document the detected signal in RESEARCH notes during Wave 1.

The existing `BOARD_HSV_LOWER`/`BOARD_HSV_UPPER` constants from `preprocessor.py` can be reused to detect board presence as a secondary signal.

### Anti-Patterns to Avoid

- **Hard-coding banner pixel coordinates as absolute px:** Canvas dimensions are 1280×800 (viewport-locked, see STATE.md), but using fractional ROI (e.g., top 15% of height) is more robust if viewport ever changes.
- **Logging every poll cycle:** The CONTEXT.md explicitly requires quiet logging (only on state changes). Noisy logging at 1-5s intervals would flood logs over a game session.
- **Using OCR to read "YOUR TURN" text:** Locked out in CONTEXT.md. Color matching is sufficient and cheaper.
- **Assuming the banner is always present when `my_turn`:** The banner may briefly flicker or take a frame to appear. Use the strict confidence threshold to avoid false triggers, but accept that one missed poll cycle is acceptable.
- **Calling `capture_canvas()` with a hard timeout that fails the whole loop:** Capture failures are transient. The loop should catch them, apply backoff, and continue rather than crashing.
- **Treating game-over detection as an afterthought:** If game-over is not detected, the polling loop will run forever after the game ends. Implement and test game-over detection in the same wave as `my_turn` detection.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| HSV range detection | Custom pixel iteration | `cv2.inRange()` | Vectorized C++ implementation; handles all edge cases; already proven in `preprocessor.py` |
| Pixel counting | Manual loop over mask | `np.count_nonzero(mask)` | One-line; vectorized; correct |
| Exponential backoff for retries | Custom doubling loop | Standard `min(val * 2, cap)` pattern OR `backoff` PyPI library | Trivial to get wrong (missing cap, wrong base); `backoff` library is tested and async-compatible |
| Debug screenshot paths | Custom path logic | `pathlib.Path` with `mkdir(parents=True, exist_ok=True)` | Handles all OS path quirks; already used in `session.py` |
| Turn state representation | Integer flags (0/1/2) | `Literal["my_turn", "not_my_turn", "game_over"]` | Type-checked by mypy; readable; no magic number bugs |

**Key insight:** The detection algorithm here is identical in structure to what `preprocessor.py` already does — `cv2.inRange()` + `cv2.contourArea()` or `np.count_nonzero()`. The new code is a simplified version of existing code, not a new problem domain.

---

## Common Pitfalls

### Pitfall 1: HSV Threshold Calibrated on Wrong Color Space

**What goes wrong:** Code captures a screenshot, calls `cv2.inRange()`, gets zero matches even though the orange banner is clearly visible in the image.

**Why it happens:** OpenCV loads images as BGR (not RGB). If the developer samples the orange color from a tool that outputs RGB values, then converts to HSV using an RGB→HSV formula, the resulting HSV values will be wrong (B and R are swapped). The project's `preprocessor.py` correctly uses `cv2.COLOR_BGR2HSV` — this must be reused, not deviated from.

**How to avoid:** Always use `cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)`. The calibration script must print HSV values derived from OpenCV's own conversion (not external tools). The placeholder constants in code must say `# CALIBRATE FROM LIVE SCREENSHOTS`.

**Warning signs:** `orange_ratio` is always near 0 even when the banner is visible; HSV values from external color pickers don't match OpenCV behavior.

### Pitfall 2: Fixed ROI Misses the Banner Due to Canvas Offset

**What goes wrong:** The banner ROI crops correctly when the canvas fills the iframe, but the Activity iframe has padding or a letterbox, so the banner appears lower or in a different region than expected.

**Why it happens:** The `capture_canvas()` function screenshots the iframe element directly (not the whole page), but the game canvas inside the iframe may have its own layout margins. The actual banner position relative to the iframe screenshot must be measured from live game screenshots.

**How to avoid:** The calibration task in Wave 1 must measure and document the exact ROI. Save full iframe screenshots during calibration and visually inspect where the banner appears. Set ROI constants with a comment explaining where they were measured from.

**Warning signs:** `classify_banner()` returns `False` even when the banner is clearly visible in saved debug screenshots.

### Pitfall 3: Adaptive Backoff Snaps Back Incorrectly

**What goes wrong:** After slowing to 5s intervals, a state change is detected but the loop doesn't snap back to 1-2s intervals, causing the bot to miss the next turn.

**Why it happens:** The backoff tracking variable (`idle_duration`) is not reset when a state change occurs.

**How to avoid:** Always reset `idle_duration = 0.0` on state change detection. The code pattern in Architecture Pattern 3 above handles this correctly.

**Warning signs:** After a state change, subsequent polls are still 5 seconds apart.

### Pitfall 4: Game-Over Not Detected, Polling Loop Runs Forever

**What goes wrong:** The game ends but the loop never exits, leaving the bot polling an ended game indefinitely.

**Why it happens:** Game-over detection is not implemented, or the leaderboard overlay detection threshold is set too high and misses the signal.

**How to avoid:** Implement game-over detection in the same wave as my-turn detection. The CONTEXT.md explicitly includes `game_over` as a required third state. Test with a deliberately saved game-over screenshot.

**Warning signs:** After game ends in test, `poll_turn()` never returns; loop continues indefinitely.

### Pitfall 5: Pre-Flight Check Passes on a Blank/Loading Screen

**What goes wrong:** The pre-flight check runs before the game canvas is fully loaded, captures a blank or loading screen, classifies it as `not_my_turn` (no orange banner), and declares the pipeline healthy — then the real game state is never correctly classified because the ROI constants are wrong.

**Why it happens:** Pre-flight runs `capture_canvas()` which retries until non-blank, but a partially-rendered loading screen can pass the non-blank check.

**How to avoid:** Pre-flight should additionally verify the image passes `is_non_blank()` AND that the overall image structure looks like an active game (e.g., the board peach region is detectable using existing `BOARD_HSV_LOWER`/`BOARD_HSV_UPPER`). A pre-flight failure should log a clear warning and halt, not silently pass.

**Warning signs:** Pre-flight reports `game_over` or always reports `not_my_turn` even when it should be `my_turn`.

### Pitfall 6: Windows Path Issues for Debug Screenshots

**What goes wrong:** `debug/turn_detection/` directory creation fails or screenshots are written to an unexpected location.

**Why it happens:** Relative paths are relative to the working directory when the script is run, not the project root. On Windows, running from a different directory puts debug files in unexpected places.

**How to avoid:** Use `Path(__file__).parent.parent.parent / "debug" / "turn_detection"` to build the path relative to `turn_detector.py`'s location (3 levels up = project root). This is consistent with how `BrowserSession` builds `./browser_data/` paths.

**Warning signs:** Debug screenshots not found where expected; `FileNotFoundError` on screenshot save.

---

## Code Examples

Verified patterns from official sources:

### HSV Color Detection (Standard Pattern from Project)

```python
# Source: Mirrors preprocessor.py pattern already in this project
# docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
import cv2
import numpy as np

# THESE ARE PLACEHOLDERS — calibrate from live screenshots in Wave 1
BANNER_HSV_LOWER = np.array([5, 120, 150])
BANNER_HSV_UPPER = np.array([20, 255, 255])
BANNER_ROI_FRAC = (0.0, 0.15)   # top 15% of canvas height
CONFIDENCE_THRESHOLD = 0.10      # 10% of ROI pixels must be orange

def classify_banner(img_bytes: bytes) -> bool:
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None:
        return False
    h, w = bgr.shape[:2]
    y0, y1 = int(h * BANNER_ROI_FRAC[0]), int(h * BANNER_ROI_FRAC[1])
    roi = bgr[y0:y1, :]
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, BANNER_HSV_LOWER, BANNER_HSV_UPPER)
    orange_ratio = np.count_nonzero(mask) / mask.size
    return orange_ratio >= CONFIDENCE_THRESHOLD
```

### Calibration Script Pattern

```python
# scripts/calibrate_turn.py
# Captures screenshots during live gameplay and prints HSV stats for banner ROI
import asyncio
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from loguru import logger

from src.browser.session import BrowserSession
from src.browser.navigator import navigate_to_activity
from src.browser.capture import capture_canvas


DEBUG_DIR = Path("debug/turn_detection")
BANNER_ROI_FRAC = (0.0, 0.15)   # top 15% — adjust if needed


async def main() -> None:
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    session = BrowserSession()
    page = await session.start()
    await navigate_to_activity(page, ...)

    logger.info("Starting calibration — press Ctrl+C to stop")
    count = 0
    try:
        while True:
            img_bytes = await capture_canvas(page)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            path = DEBUG_DIR / f"frame_{ts}.png"
            path.write_bytes(img_bytes)

            arr = np.frombuffer(img_bytes, dtype=np.uint8)
            bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            h, w = bgr.shape[:2]
            y0, y1 = int(h * BANNER_ROI_FRAC[0]), int(h * BANNER_ROI_FRAC[1])
            roi = bgr[y0:y1, :]
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

            # Print median HSV of the ROI for threshold calibration
            median_h = int(np.median(hsv[:, :, 0]))
            median_s = int(np.median(hsv[:, :, 1]))
            median_v = int(np.median(hsv[:, :, 2]))
            logger.info(
                "Frame {} — ROI median HSV: ({}, {}, {}) — saved: {}",
                count, median_h, median_s, median_v, path.name
            )
            count += 1
            await asyncio.sleep(2.0)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Calibration stopped. {} frames saved to {}", count, DEBUG_DIR)
    finally:
        await session.close()
```

### TurnState Module Skeleton

```python
# src/browser/turn_detector.py
from __future__ import annotations

import asyncio
from pathlib import Path
from datetime import datetime
from typing import Literal

import cv2
import numpy as np
from loguru import logger

from src.browser.capture import capture_canvas
from src.vision.preprocessor import BOARD_HSV_LOWER, BOARD_HSV_UPPER  # reuse for game-over


TurnState = Literal["my_turn", "not_my_turn", "game_over"]

# --- Constants (calibrate from live screenshots — see calibrate_turn.py) ---
BANNER_HSV_LOWER = np.array([5, 120, 150])   # PLACEHOLDER
BANNER_HSV_UPPER = np.array([20, 255, 255])  # PLACEHOLDER
BANNER_ROI_FRAC = (0.0, 0.15)               # top 15% of canvas height
BANNER_CONFIDENCE = 0.10                     # PLACEHOLDER — 10% of ROI pixels

POLL_FAST_S = 1.5
POLL_SLOW_S = 5.0
IDLE_THRESHOLD_S = 30.0

_DEBUG_DIR = Path(__file__).parent.parent.parent / "debug" / "turn_detection"


def _is_my_turn(img_bytes: bytes) -> bool:
    """Return True if the orange 'YOUR TURN' banner is present."""
    ...  # classify_banner() implementation above


def _is_game_over(img_bytes: bytes) -> bool:
    """Return True if the game-over leaderboard overlay is detected."""
    ...  # Claude's discretion — implement during Wave 1 calibration


def classify_frame(img_bytes: bytes) -> TurnState:
    """Classify canvas screenshot into a TurnState."""
    if _is_game_over(img_bytes):
        return "game_over"
    if _is_my_turn(img_bytes):
        return "my_turn"
    return "not_my_turn"


async def poll_turn(page) -> TurnState:
    """Poll until my_turn or game_over. Returns the detected state."""
    ...  # adaptive polling loop — see Architecture Pattern 3


async def preflight_check(page) -> None:
    """Verify turn detection is operational. Raises RuntimeError on failure."""
    ...  # see Architecture Pattern 4
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| OCR-based turn detection | Color-region detection | N/A for this project | No Tesseract dependency; no model inference; near-instant check |
| Polling with fixed interval | Adaptive backoff polling | Common practice 2020+ | Reduces CPU/capture overhead during long opponent turns |
| String-based state | `Literal` type annotation | Python 3.8+ (already baseline) | Static type checking catches downstream state comparison bugs |
| Absolute pixel coordinates | Fractional ROI (% of height/width) | Best practice | Robust to viewport dimension changes |

**No deprecated approaches apply here.** The pattern is straightforward and uses stable, battle-tested OpenCV APIs that have not changed significantly since OpenCV 3.x.

---

## Open Questions

1. **Exact banner ROI position and height**
   - What we know: CONTEXT.md says the orange banner appears "at the top of the game canvas"; it is a square banner (square, not thin strip)
   - What's unclear: Exact pixel region — does it span the full width? How tall is it? Is it inset or flush with the canvas edge?
   - Recommendation: Answer during Wave 1 calibration script by visually inspecting saved screenshots. Set fractional constants accordingly. Budget: calibration task includes ≥10 screenshots per state (my_turn + not_my_turn).

2. **Game-over overlay detection method**
   - What we know: CONTEXT.md describes leaderboard overlay in center, players, winner right, board left; "visually distinct from normal gameplay"
   - What's unclear: Whether the overlay has a distinguishable color profile (dark background? grey? specific accent?), or whether structural detection is needed
   - Recommendation: Classify as Claude's discretion. During calibration, save at least 2 game-over screenshots. Try: (a) absence of orange peach board color covering expected board region — game-over shows board but the center is occluded; (b) or a distinct overlay color that can be detected with a second `cv2.inRange()` call. Pick whichever is more reliable from the saved screenshots.

3. **False positive rate for orange detection**
   - What we know: The banner color is described as "high-contrast orange" against the rest of the UI
   - What's unclear: Whether any other UI element in the game canvas ever shows orange in the top-of-canvas region (tile colors? score display?)
   - Recommendation: The confidence threshold (% of ROI pixels) + fixed ROI should prevent false positives. If calibration reveals other orange elements in the banner region, narrow the ROI or increase the threshold. The CONTEXT.md requirement of "strict confidence threshold — better to miss one poll cycle than act out of turn" directly addresses this.

4. **Canvas dimensions at 1280x800 viewport**
   - What we know: Viewport is locked at 1280x800 (STATE.md decision); `capture_canvas()` screenshots the iframe element directly
   - What's unclear: Whether the game canvas fills the entire iframe or has letterboxing
   - Recommendation: Record iframe screenshot dimensions during calibration. If the game canvas is padded, adjust ROI constants accordingly. This is the same uncertainty that Phase 5 documented as an open question.

---

## Sources

### Primary (HIGH confidence)
- `src/vision/preprocessor.py` in this project — direct reference for `cv2.COLOR_BGR2HSV`, `cv2.inRange()`, `np.count_nonzero()`, ROI crop via array slicing; pattern is identical and proven in production
- `src/browser/capture.py` in this project — `capture_canvas()` signature and return type `bytes`; reused directly
- OpenCV official docs: docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html — HSV colorspace conversion, H range 0-179, S/V range 0-255 confirmed
- OpenCV official docs: docs.opencv.org/4.x/d3/df2/tutorial_py_basic_ops.html — array slicing for ROI confirmed
- Python stdlib docs: docs.python.org/3/library/asyncio.html — `asyncio.sleep()` for polling loops

### Secondary (MEDIUM confidence)
- GeeksforGeeks: geeksforgeeks.org/computer-vision/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-with-cv-inrange-opencv/ — orange HSV range H:[10,25] documented; cross-verified with multiple sources
- GitHub: github.com/litl/backoff — `backoff` library supports async coroutines for retry logic (not used but noted as available)
- `.planning/phases/06-turn-detection/06-CONTEXT.md` — locked decisions about banner detection and polling behavior

### Tertiary (LOW confidence)
- Starting HSV orange thresholds `[5, 120, 150]` to `[20, 255, 255]` — reasonable starting point based on documented orange ranges, but MUST be calibrated from actual game screenshots; do not use without calibration
- Game-over detection approach via peach-board-absence — logical deduction from CONTEXT.md description; needs live validation

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all dependencies already installed and proven in the project; no new packages required
- Architecture: HIGH — detection pattern is a simplified version of existing `preprocessor.py`; async polling pattern is standard asyncio; fractional ROI is best practice
- Pitfalls: HIGH — most pitfalls identified from direct codebase knowledge (BGR vs RGB, path handling, pre-flight, game-over detection gap); not speculation
- HSV threshold values: LOW — placeholder until Wave 1 calibration; treat as starting point only

**Research date:** 2026-03-26
**Valid until:** 2026-04-26 (stable — OpenCV API is version-stable; Discord game UI may change but detection approach is resilient to minor changes)
