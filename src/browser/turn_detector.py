from __future__ import annotations

import asyncio
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

import cv2
import numpy as np
from loguru import logger

from src.vision.preprocessor import BOARD_HSV_LOWER, BOARD_HSV_UPPER

# ---------------------------------------------------------------------------
# Type alias
# ---------------------------------------------------------------------------

TurnState = Literal["my_turn", "not_my_turn", "game_over", "idle_timeout", "stop_requested"]

# ---------------------------------------------------------------------------
# HSV constants — Calibrated from live screenshots 2026-03-26
# ---------------------------------------------------------------------------

# Orange "YOUR TURN" banner: lower and upper HSV bounds.
# Observed banner pixels: H=[6-22], S=[80-242], V=[176-255].
# Placeholder range [5-20,120-255,150-255] confirmed correct — kept unchanged.
# Tight range keeps separation vs Letter League logo orange (~3.7% baseline).
BANNER_HSV_LOWER = np.array([5, 120, 150])   # Calibrated 2026-03-26 — confirmed from observed H=[6-22]
BANNER_HSV_UPPER = np.array([20, 255, 255])  # Calibrated 2026-03-26 — confirmed from observed H=[6-22]

# Fractional vertical range of the banner ROI within the canvas (top 10%).
# Top 10% captures the header/score bar where orange signal is concentrated.
# At 15%, rows 10-15% are empty in the live UI, diluting the ratio below
# the BANNER_CONFIDENCE threshold; top 10% gives 0.10 for my_turn and 0.04
# for not_my_turn — clean separation at the 0.07 threshold.
BANNER_ROI_FRAC = (0.0, 0.10)  # Updated 2026-04-14 — tightened from 0.15 to fix live-game miss

# Minimum ratio of orange pixels in the ROI required to declare "my turn".
# my_turn: ~9-10% orange | not_my_turn: ~3.7% (logo only) | threshold at 7%.
BANNER_CONFIDENCE = 0.07  # Calibrated 2026-03-26

# Peach ratio in the centre region below which we suspect game-over.
# Gameplay: ~57-60% peach | Game-over overlay: ~12% peach | threshold at 25%.
GAME_OVER_BOARD_THRESHOLD = 0.25  # Calibrated 2026-03-26

# Polling intervals (seconds).
POLL_FAST_S = 1.5   # Fast interval during active gameplay.
POLL_SLOW_S = 5.0   # Slow interval after extended idle period.

# Seconds of "not my turn" before switching to slow polling.
IDLE_THRESHOLD_S = 30.0

# Maximum seconds to poll "not my turn" before returning idle_timeout.
MAX_IDLE_S = 300.0  # 5 minutes

# Seconds to wait for the game board to appear during startup.
GAME_READY_TIMEOUT_S = 60.0
GAME_READY_POLL_S = 2.0

# START GAME button fractional position within the canvas/iframe.
# Calibrated from title screen screenshot — button is bottom-right of canvas.
START_GAME_X_FRAC = 0.935
START_GAME_Y_FRAC = 0.957

# Title screen sidebar detection.
# The title/lobby screen has a distinctive large orange/salmon sidebar
# covering the right ~25% of the canvas.  During actual gameplay the board
# extends across the full canvas width and no such sidebar exists.
# HSV range for the sidebar colour (warm salmon/coral).
SIDEBAR_HSV_LOWER = np.array([3, 100, 140])
SIDEBAR_HSV_UPPER = np.array([25, 220, 255])
# Fraction of canvas width to sample from the right edge.
SIDEBAR_STRIP_FRAC = 0.20
# Minimum ratio of sidebar-coloured pixels in the right strip.
SIDEBAR_MIN_RATIO = 0.30

# Debug output directory (relative to project root).
_DEBUG_DIR = Path(__file__).parent.parent.parent / "debug" / "turn_detection"


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _save_debug_screenshot(img_bytes: bytes, label: str = "") -> Path:
    """Save raw image bytes to the debug directory with a timestamped filename.

    Args:
        img_bytes: Raw PNG (or other format) bytes to persist.
        label: Optional string appended after the timestamp (e.g. "preflight").

    Returns:
        Path to the saved file.
    """
    _DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    suffix = f"_{label}" if label else ""
    path = _DEBUG_DIR / f"frame_{timestamp}{suffix}.png"
    path.write_bytes(img_bytes)
    return path


def _decode_bgr(img_bytes: bytes) -> np.ndarray | None:
    """Decode raw image bytes to a BGR numpy array. Returns None on failure."""
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return bgr  # May be None if decoding fails


def _is_my_turn(img_bytes: bytes) -> bool:
    """Return True if the orange "YOUR TURN" banner is visible in the canvas.

    Crops the top BANNER_ROI_FRAC[0]..BANNER_ROI_FRAC[1] fraction of the image,
    converts to HSV, and checks whether the ratio of orange pixels meets the
    BANNER_CONFIDENCE threshold.

    Args:
        img_bytes: Raw screenshot bytes from capture_canvas().

    Returns:
        True if the banner is detected with sufficient confidence.
    """
    bgr = _decode_bgr(img_bytes)
    if bgr is None:
        return False

    h, w = bgr.shape[:2]
    y_start = int(h * BANNER_ROI_FRAC[0])
    y_end = int(h * BANNER_ROI_FRAC[1])
    roi = bgr[y_start:y_end, :]

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, BANNER_HSV_LOWER, BANNER_HSV_UPPER)
    orange_ratio = np.count_nonzero(mask) / mask.size

    return bool(orange_ratio >= BANNER_CONFIDENCE)


def _is_game_over(img_bytes: bytes) -> bool:
    """Return True if the game-over leaderboard overlay is likely present.

    Heuristic: the leaderboard overlay covers the centre of the canvas, hiding
    the board's peach background. If the peach ratio in the centre 50%x50%
    region falls below GAME_OVER_BOARD_THRESHOLD while the image itself is
    non-blank, a game-over overlay is presumed.

    Also returns True when: no orange banner is present AND the centre has
    minimal peach colour (i.e. it is not a normal "not my turn" frame).

    Args:
        img_bytes: Raw screenshot bytes from capture_canvas().

    Returns:
        True if game-over is suspected.
    """
    bgr = _decode_bgr(img_bytes)
    if bgr is None:
        return False

    h, w = bgr.shape[:2]

    # Centre 50% region — where the leaderboard would obscure the board.
    y_start = int(h * 0.25)
    y_end = int(h * 0.75)
    x_start = int(w * 0.25)
    x_end = int(w * 0.75)
    centre = bgr[y_start:y_end, x_start:x_end]

    hsv_centre = cv2.cvtColor(centre, cv2.COLOR_BGR2HSV)
    peach_mask = cv2.inRange(hsv_centre, BOARD_HSV_LOWER, BOARD_HSV_UPPER)
    peach_ratio = np.count_nonzero(peach_mask) / peach_mask.size

    if peach_ratio >= GAME_OVER_BOARD_THRESHOLD:
        # Sufficient board peach colour visible — this is normal gameplay.
        return False

    # Peach is nearly absent from centre; confirm the image is not blank.
    overall_std = float(np.std(bgr))
    if overall_std < 5.0:
        # Blank or near-blank frame — not a game-over signal.
        return False

    return True


def _is_title_screen(img_bytes: bytes) -> bool:
    """Return True if the frame shows the title/lobby screen.

    The title screen has a distinctive large orange/salmon sidebar covering
    the right ~25% of the canvas (character illustrations panel).  During
    actual gameplay the board extends across the full canvas width and no
    such sidebar exists.

    Checks the rightmost SIDEBAR_STRIP_FRAC of the image for warm-coloured
    pixels.  A high ratio indicates the title screen sidebar.
    """
    bgr = _decode_bgr(img_bytes)
    if bgr is None:
        return False

    h, w = bgr.shape[:2]
    x_start = int(w * (1.0 - SIDEBAR_STRIP_FRAC))
    right_strip = bgr[:, x_start:]

    hsv = cv2.cvtColor(right_strip, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, SIDEBAR_HSV_LOWER, SIDEBAR_HSV_UPPER)
    ratio = np.count_nonzero(mask) / mask.size

    return bool(ratio >= SIDEBAR_MIN_RATIO)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def classify_frame(img_bytes: bytes) -> TurnState:
    """Classify a single canvas screenshot into a TurnState.

    Evaluation order:
      1. title_screen — lobby/title screen with orange sidebar; treated as
         game_over so poll_turn's game_seen guard prevents false positives.
      2. game_over  — prevents infinite polling after the game ends.
      3. my_turn    — orange banner is present.
      4. not_my_turn — default when neither condition is met.

    Args:
        img_bytes: Raw screenshot bytes from capture_canvas().

    Returns:
        One of "my_turn", "not_my_turn", or "game_over".
    """
    if _is_title_screen(img_bytes):
        return "game_over"
    if _is_game_over(img_bytes):
        return "game_over"
    if _is_my_turn(img_bytes):
        return "my_turn"
    return "not_my_turn"


async def preflight_check(page: Any) -> None:
    """Capture one frame, classify it, save a debug screenshot, and log the result.

    Intended to be called once before entering the poll_turn loop. Verifies that
    the capture pipeline is operational and turn detection does not crash.

    Args:
        page: A patchright Page object.

    Raises:
        RuntimeError: If capture_canvas() raises for any reason.
    """
    from src.browser.capture import capture_canvas  # local import avoids circular ref

    try:
        img_bytes = await capture_canvas(page)
    except Exception as exc:
        raise RuntimeError(
            f"Pre-flight turn detection failed: capture_canvas raised {exc!r}"
        ) from exc

    state: TurnState = classify_frame(img_bytes)
    debug_path = _save_debug_screenshot(img_bytes, label="preflight")
    logger.info(
        "Pre-flight turn detection check passed — initial state: {} (debug: {})",
        state,
        debug_path,
    )


def _has_board(img_bytes: bytes) -> bool:
    """Return True if the peach board background is visible in the frame.

    Used to confirm the game has fully loaded (not a splash/loading screen).
    """
    bgr = _decode_bgr(img_bytes)
    if bgr is None:
        return False

    h, w = bgr.shape[:2]
    centre = bgr[int(h * 0.25):int(h * 0.75), int(w * 0.25):int(w * 0.75)]
    hsv = cv2.cvtColor(centre, cv2.COLOR_BGR2HSV)
    peach_mask = cv2.inRange(hsv, BOARD_HSV_LOWER, BOARD_HSV_UPPER)
    peach_ratio = np.count_nonzero(peach_mask) / peach_mask.size
    return bool(peach_ratio >= GAME_OVER_BOARD_THRESHOLD)


async def wait_for_game_ready(page: Any) -> None:
    """Poll until the game board is visible, indicating the game has loaded.

    Prevents the turn loop from starting while the game is still on a
    splash screen or loading state.

    Args:
        page: A patchright Page object.

    Raises:
        TimeoutError: If the board is not detected within GAME_READY_TIMEOUT_S.
    """
    from src.browser.capture import capture_canvas

    elapsed = 0.0
    while elapsed < GAME_READY_TIMEOUT_S:
        try:
            img_bytes = await capture_canvas(page)
            if _has_board(img_bytes):
                logger.info("Game board detected — ready to play")
                return
        except Exception as exc:
            logger.warning("wait_for_game_ready: capture failed — {}", exc)

        await asyncio.sleep(GAME_READY_POLL_S)
        elapsed += GAME_READY_POLL_S

    raise TimeoutError(
        f"Game board not detected after {GAME_READY_TIMEOUT_S:.0f}s — "
        "game may not have loaded"
    )


async def click_start_game(page: Any) -> None:
    """Click the START GAME button on the title screen to begin the match.

    Should be called after wait_for_game_ready() confirms the board is visible.
    The title screen shows a decorative board with a START GAME button in the
    bottom-right. If the game is already in progress, the click lands on the
    player info panel area and is harmless.

    After clicking, polls briefly until the frame state changes from the title
    screen (game_over-like classification) to actual gameplay (my_turn or
    not_my_turn with sufficient board peach).

    Args:
        page: A patchright Page object.
    """
    iframe_locator = page.locator('iframe[src*="discordsays.com"]')
    bbox = await iframe_locator.bounding_box(timeout=10_000)
    if bbox is None:
        logger.warning("click_start_game: iframe not found — skipping")
        return

    x = bbox["x"] + START_GAME_X_FRAC * bbox["width"]
    y = bbox["y"] + START_GAME_Y_FRAC * bbox["height"]

    logger.info("Clicking START GAME button at ({:.1f}, {:.1f})", x, y)
    await page.mouse.click(x, y)

    # Wait for the title screen sidebar to disappear, confirming the game
    # has actually started.  The title screen has a distinctive orange sidebar
    # that is absent during gameplay.
    from src.browser.capture import capture_canvas

    for i in range(15):  # up to ~30 seconds
        await asyncio.sleep(2.0)
        try:
            img_bytes = await capture_canvas(page)
            if not _is_title_screen(img_bytes):
                state = classify_frame(img_bytes)
                logger.info("Game started — initial state: {}", state)
                return
            logger.debug("click_start_game: still on title screen (poll {})", i)
        except Exception as exc:
            logger.warning("click_start_game: capture failed on poll {}: {}", i, exc)

    logger.warning("click_start_game: game did not transition after clicking — continuing anyway")


async def poll_turn(
    page: Any,
    stop_event: asyncio.Event | None = None,
) -> TurnState:
    """Poll the canvas until the turn state changes to "my_turn" or "game_over".

    Implements an adaptive polling loop:
    - Polls every POLL_FAST_S seconds while the state has changed recently.
    - After IDLE_THRESHOLD_S seconds without a state change, slows to POLL_SLOW_S.
    - Snaps back to fast polling the moment a state change is detected.
    - Logs only on state transitions (quiet logging per CONTEXT.md decisions).
    - Retries with exponential backoff on capture failures.
    - Will not return "game_over" until at least one gameplay frame (my_turn or
      not_my_turn) has been observed, preventing false positives from lobby/loading
      screens that lack the peach board background.
    - Returns "idle_timeout" after MAX_IDLE_S of continuous not_my_turn polling.
    - Returns "stop_requested" immediately if stop_event is set while sleeping.

    Args:
        page:       A patchright Page object.
        stop_event: Optional asyncio.Event; when set the loop exits with
                    "stop_requested" instead of sleeping until the next poll.

    Returns:
        "my_turn", "game_over", "idle_timeout", or "stop_requested".
    """
    from src.browser.capture import capture_canvas  # local import avoids circular ref

    async def _interruptible_sleep(seconds: float) -> bool:
        """Sleep for *seconds*, waking early if stop_event fires.

        Returns True if the stop_event was set (caller should exit), False
        if the sleep completed normally.
        """
        if stop_event is None:
            await asyncio.sleep(seconds)
            return False
        try:
            await asyncio.wait_for(
                asyncio.shield(stop_event.wait()),
                timeout=seconds,
            )
            # wait_for returned without raising — stop_event is set
            return True
        except asyncio.TimeoutError:
            return False

    last_state: TurnState | None = None
    idle_duration: float = 0.0
    capture_backoff: float = 1.0  # Seconds between retry attempts on failure
    game_seen: bool = False  # True once we've seen my_turn or not_my_turn

    while True:
        # --- Stop-event check at top of each iteration ---
        if stop_event is not None and stop_event.is_set():
            logger.info("poll_turn: stop_event set — returning stop_requested")
            return "stop_requested"

        # --- Idle timeout check ---
        if idle_duration >= MAX_IDLE_S:
            logger.warning(
                "poll_turn: idle for {:.0f}s without a turn — returning idle_timeout",
                idle_duration,
            )
            return "idle_timeout"

        # --- Capture frame with retry/backoff on failure ---
        try:
            img_bytes = await capture_canvas(page)
            capture_backoff = 1.0  # Reset backoff on success
        except Exception as exc:
            logger.warning(
                "capture_canvas failed (will retry in {:.1f}s): {}", capture_backoff, exc
            )
            stopped = await _interruptible_sleep(capture_backoff)
            if stopped:
                logger.info("poll_turn: stop_event set during capture backoff — returning stop_requested")
                return "stop_requested"
            capture_backoff = min(capture_backoff * 2, 30.0)
            continue

        # --- Classify the frame ---
        state: TurnState = classify_frame(img_bytes)

        # --- Guard: ignore game_over until we've seen actual gameplay ---
        if state == "game_over" and not game_seen:
            # Lobby / loading screen — treat as waiting, keep polling.
            if last_state != "game_over":
                logger.info("Turn state: game_over before gameplay detected — treating as loading screen, waiting")
                last_state = "game_over"
            idle_duration += POLL_FAST_S
            stopped = await _interruptible_sleep(POLL_FAST_S)
            if stopped:
                logger.info("poll_turn: stop_event set during pre-game wait — returning stop_requested")
                return "stop_requested"
            continue

        if state in ("my_turn", "not_my_turn"):
            game_seen = True

        # --- Log only on state change (quiet logging) ---
        if state != last_state:
            logger.info("Turn state changed: {} -> {}", last_state, state)
            idle_duration = 0.0
            last_state = state

        # --- Return on terminal states ---
        if state in ("my_turn", "game_over"):
            return state

        # --- Adaptive polling interval ---
        interval = POLL_SLOW_S if idle_duration >= IDLE_THRESHOLD_S else POLL_FAST_S
        idle_duration += interval
        stopped = await _interruptible_sleep(interval)
        if stopped:
            logger.info("poll_turn: stop_event set during polling sleep — returning stop_requested")
            return "stop_requested"
