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

# After this many consecutive capture_canvas failures, poll_turn gives up
# and raises IframeDeadError so the caller can re-launch the activity.
# When the iframe is truly dead each attempt costs ~30s wait_for + 30s
# diagnostic ≈ 60s, so 3 failures ≈ 3 minutes — enough to ride out a
# transient blip, fast enough to recover before the autoplay subprocess
# timeout fires (lowered from 5 after iter_001 hit the timeout).
MAX_CAPTURE_FAILURES = 3


class IframeDeadError(RuntimeError):
    """Raised by poll_turn when the game iframe is unreachable.

    Signals that the Discord Activity iframe has gone away (activity closed,
    voice call dropped, Discord re-rendered the shelf). The caller should
    re-navigate and re-ensure the game is started before resuming polling.
    """

# Seconds to wait for the game board to appear during startup.
GAME_READY_TIMEOUT_S = 60.0
GAME_READY_POLL_S = 2.0

# START GAME button fractional position within the canvas/iframe.
# Re-calibrated 2026-04-21 from debug/menu_screen.png — contour-detected
# button bbox spans (0.764-0.981, 0.900-0.981); center at (0.872, 0.940).
# The previous values (0.935, 0.957) landed near the rounded right edge of
# the pill and sometimes missed when iframe dimensions differed from the
# calibration screenshot.
START_GAME_X_FRAC = 0.872
START_GAME_Y_FRAC = 0.940

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

    # Position relative to the iframe's top-left corner (CSS px). Using the
    # locator's own click() keeps Playwright's hit-testing inside the iframe
    # element and is DPR-safe.
    pos_x = START_GAME_X_FRAC * bbox["width"]
    pos_y = START_GAME_Y_FRAC * bbox["height"]
    abs_x = bbox["x"] + pos_x
    abs_y = bbox["y"] + pos_y

    logger.info(
        "Clicking START GAME button at iframe-relative ({:.1f}, {:.1f}) / page ({:.1f}, {:.1f})",
        pos_x, pos_y, abs_x, abs_y,
    )
    # Hover-then-click sequence — some Discord overlays only respond after a
    # mousemove event lands on the target.
    try:
        await page.mouse.move(abs_x, abs_y, steps=8)
        await asyncio.sleep(0.15)
        await iframe_locator.click(
            position={"x": pos_x, "y": pos_y},
            timeout=10_000,
            force=True,
        )
    except Exception as exc:
        logger.warning("click_start_game: locator click failed ({}), falling back to mouse.click", exc)
        await page.mouse.click(abs_x, abs_y)

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


async def ensure_game_started(
    page: Any,
    max_attempts: int = 4,
    splash_timeout_s: float = 30.0,
) -> TurnState:
    """Drive the activity into a running game regardless of current screen.

    Handles three pre-game states idempotently:

    - **Splash / loading screen**: blank or low-variance frames where neither
      the lobby sidebar nor a banner is visible. Waits up to
      ``splash_timeout_s`` for it to clear.
    - **Lobby / title screen**: detected by the orange sidebar. Clicks the
      START GAME button, waits for the sidebar to disappear, then verifies a
      gameplay banner appears. Retries up to ``max_attempts`` times.
    - **Game already in progress**: detected by ``my_turn`` / ``not_my_turn``
      banners. Returns immediately without clicking anything.

    Required before entering the turn loop for single-player autoplay, where
    the headless runner cannot assume a game has been started by a human.

    Args:
        page: A patchright Page object.
        max_attempts: Start-game click retries before giving up.
        splash_timeout_s: Max seconds to wait for a splash screen to clear.

    Returns:
        The first observed gameplay ``TurnState`` (``"my_turn"`` or
        ``"not_my_turn"``).

    Raises:
        RuntimeError: If no gameplay frame is observed after retries.
    """
    from src.browser.capture import capture_canvas  # local import avoids circular ref

    # --- Step 1: wait out any splash/loading screen -----------------------
    splash_elapsed = 0.0
    while splash_elapsed < splash_timeout_s:
        try:
            img_bytes = await capture_canvas(page)
        except Exception as exc:
            logger.warning("ensure_game_started: capture failed on splash wait: {}", exc)
            await asyncio.sleep(2.0)
            splash_elapsed += 2.0
            continue

        bgr = _decode_bgr(img_bytes)
        if bgr is not None:
            std = float(np.std(bgr))
            # A real screen (splash logo, lobby, or game) has std well above 20.
            # Pure loading blanks or partly-rendered frames sit below that.
            if std > 20.0 and (_is_title_screen(img_bytes) or _has_board(img_bytes)):
                break
        await asyncio.sleep(1.5)
        splash_elapsed += 1.5
    else:
        raise RuntimeError(
            f"ensure_game_started: splash never cleared after {splash_timeout_s:.0f}s"
        )

    # --- Step 2: click START GAME until we see gameplay -------------------
    for attempt in range(1, max_attempts + 1):
        try:
            img_bytes = await capture_canvas(page)
        except Exception as exc:
            logger.warning(
                "ensure_game_started: capture failed (attempt {}): {}", attempt, exc
            )
            await asyncio.sleep(2.0)
            continue

        state = classify_frame(img_bytes)

        # Already in a running game — done.
        if state in ("my_turn", "not_my_turn"):
            logger.info("ensure_game_started: game already in progress ({})", state)
            return state

        # Lobby screen — click START GAME and verify transition.
        if _is_title_screen(img_bytes):
            logger.info(
                "ensure_game_started: lobby detected — clicking START GAME (attempt {}/{})",
                attempt, max_attempts,
            )
            _save_debug_screenshot(img_bytes, label=f"pre_start_attempt{attempt}")
            await click_start_game(page)

            # Poll for up to ~15s looking for a gameplay banner.
            for _ in range(10):
                await asyncio.sleep(1.5)
                try:
                    img_bytes = await capture_canvas(page)
                except Exception:
                    continue
                next_state = classify_frame(img_bytes)
                if next_state in ("my_turn", "not_my_turn"):
                    logger.info(
                        "ensure_game_started: game started — initial state: {}", next_state
                    )
                    return next_state
            logger.warning(
                "ensure_game_started: no banner after click (attempt {})", attempt,
            )
            continue

        # Neither lobby nor gameplay — probably a loading transition. Wait.
        logger.info(
            "ensure_game_started: ambiguous frame (state={}) — waiting then retry",
            state,
        )
        await asyncio.sleep(2.0)

    # Exhausted retries.
    try:
        img_bytes = await capture_canvas(page)
        _save_debug_screenshot(img_bytes, label="ensure_game_started_fail")
    except Exception:
        pass
    raise RuntimeError(
        f"ensure_game_started: failed to enter gameplay after {max_attempts} attempts"
    )


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
    capture_failures: int = 0  # Consecutive capture failures; resets on success
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
            capture_failures = 0
        except Exception as exc:
            capture_failures += 1
            if capture_failures >= MAX_CAPTURE_FAILURES:
                logger.error(
                    "poll_turn: {} consecutive capture failures — iframe is dead, giving up",
                    capture_failures,
                )
                raise IframeDeadError(
                    f"Activity iframe unreachable after {capture_failures} attempts"
                ) from exc
            logger.warning(
                "capture_canvas failed ({}/{}, retry in {:.1f}s): {}",
                capture_failures, MAX_CAPTURE_FAILURES, capture_backoff, exc,
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
