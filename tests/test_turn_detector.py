"""Tests for turn_detector.py (Phase B2).

classify_frame, _is_my_turn, _is_game_over are tested with synthetic images.
poll_turn and preflight_check are tested with mocked capture_canvas.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import cv2
import numpy as np
import pytest

from src.browser.turn_detector import (
    BANNER_CONFIDENCE,
    BANNER_HSV_LOWER,
    BANNER_HSV_UPPER,
    BANNER_ROI_FRAC,
    GAME_OVER_BOARD_THRESHOLD,
    GAME_READY_TIMEOUT_S,
    IDLE_THRESHOLD_S,
    MAX_IDLE_S,
    POLL_FAST_S,
    POLL_SLOW_S,
    SIDEBAR_HSV_LOWER,
    SIDEBAR_HSV_UPPER,
    SIDEBAR_MIN_RATIO,
    SIDEBAR_STRIP_FRAC,
    _is_game_over,
    _is_my_turn,
    _is_title_screen,
    classify_frame,
    poll_turn,
    preflight_check,
    wait_for_game_ready,
)
from src.vision.preprocessor import BOARD_HSV_LOWER as PEACH_LOWER, BOARD_HSV_UPPER as PEACH_UPPER


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _encode_png(img: np.ndarray) -> bytes:
    _, buf = cv2.imencode(".png", img)
    return buf.tobytes()


def _make_orange_banner_image(h: int = 200, w: int = 300) -> bytes:
    """Create an image with an orange banner in the top 15% and peach in center.

    The peach center prevents _is_game_over from triggering (since classify_frame
    checks game_over before my_turn).
    """
    img = np.full((h, w, 3), 200, dtype=np.uint8)  # grey base

    # Orange banner in top 15%
    banner_h = int(h * BANNER_ROI_FRAC[1])
    hsv_pixel = np.array([10, 200, 255], dtype=np.uint8)
    bgr_pixel = cv2.cvtColor(hsv_pixel.reshape(1, 1, 3), cv2.COLOR_HSV2BGR).flatten()
    img[:banner_h, :] = bgr_pixel

    # Peach in center 50% to prevent game_over detection
    y_start = int(h * 0.25)
    y_end = int(h * 0.75)
    x_start = int(w * 0.25)
    x_end = int(w * 0.75)
    peach_hsv = np.array([
        (int(PEACH_LOWER[0]) + int(PEACH_UPPER[0])) // 2,
        (int(PEACH_LOWER[1]) + int(PEACH_UPPER[1])) // 2,
        (int(PEACH_LOWER[2]) + int(PEACH_UPPER[2])) // 2,
    ], dtype=np.uint8)
    peach_bgr = cv2.cvtColor(peach_hsv.reshape(1, 1, 3), cv2.COLOR_HSV2BGR).flatten()
    img[y_start:y_end, x_start:x_end] = peach_bgr

    return _encode_png(img)


def _make_not_my_turn_image(h: int = 200, w: int = 300) -> bytes:
    """Create an image with no orange banner but visible board peach in center."""
    img = np.full((h, w, 3), 200, dtype=np.uint8)  # neutral grey

    # Fill center 50% with peach colour (in the BOARD_HSV range)
    y_start = int(h * 0.25)
    y_end = int(h * 0.75)
    x_start = int(w * 0.25)
    x_end = int(w * 0.75)

    # Peach in HSV: pick mid of PEACH_LOWER/UPPER
    peach_hsv = np.array([
        (int(PEACH_LOWER[0]) + int(PEACH_UPPER[0])) // 2,
        (int(PEACH_LOWER[1]) + int(PEACH_UPPER[1])) // 2,
        (int(PEACH_LOWER[2]) + int(PEACH_UPPER[2])) // 2,
    ], dtype=np.uint8)
    peach_bgr = cv2.cvtColor(peach_hsv.reshape(1, 1, 3), cv2.COLOR_HSV2BGR).flatten()
    img[y_start:y_end, x_start:x_end] = peach_bgr

    return _encode_png(img)


def _make_game_over_image(h: int = 200, w: int = 300) -> bytes:
    """Create image with no orange banner AND low peach in center (game-over)."""
    rng = np.random.RandomState(99)
    # Random varied image (non-blank) but no peach or orange
    img = rng.randint(50, 150, (h, w, 3), dtype=np.uint8)
    # Make sure the blue channel dominates to avoid peach/orange detection
    img[:, :, 0] = 150  # B channel high
    img[:, :, 1] = 60   # G channel low
    img[:, :, 2] = 60   # R channel low
    return _encode_png(img)


def _make_title_screen_image(h: int = 200, w: int = 300) -> bytes:
    """Create an image simulating the title/lobby screen.

    The title screen has a peach board in the main area and a large
    orange/salmon sidebar covering the right ~25% of the canvas.
    """
    img = np.full((h, w, 3), 200, dtype=np.uint8)  # grey base

    # Peach board in center area
    y_start = int(h * 0.25)
    y_end = int(h * 0.75)
    x_start = int(w * 0.10)
    x_end = int(w * 0.70)
    peach_hsv = np.array([
        (int(PEACH_LOWER[0]) + int(PEACH_UPPER[0])) // 2,
        (int(PEACH_LOWER[1]) + int(PEACH_UPPER[1])) // 2,
        (int(PEACH_LOWER[2]) + int(PEACH_UPPER[2])) // 2,
    ], dtype=np.uint8)
    peach_bgr = cv2.cvtColor(peach_hsv.reshape(1, 1, 3), cv2.COLOR_HSV2BGR).flatten()
    img[y_start:y_end, x_start:x_end] = peach_bgr

    # Orange/salmon sidebar on right 25% (full height)
    sidebar_x = int(w * 0.75)
    sidebar_hsv = np.array([12, 140, 210], dtype=np.uint8)  # warm salmon
    sidebar_bgr = cv2.cvtColor(sidebar_hsv.reshape(1, 1, 3), cv2.COLOR_HSV2BGR).flatten()
    img[:, sidebar_x:] = sidebar_bgr

    return _encode_png(img)


# ---------------------------------------------------------------------------
# classify_frame tests
# ---------------------------------------------------------------------------


class TestIsTitleScreen:
    def test_title_screen_detected(self):
        img = _make_title_screen_image()
        assert _is_title_screen(img) is True

    def test_gameplay_not_title_screen(self):
        img = _make_not_my_turn_image()
        assert _is_title_screen(img) is False

    def test_orange_banner_not_title_screen(self):
        """Orange banner in top 15% only should NOT trigger sidebar detection."""
        img = _make_orange_banner_image()
        assert _is_title_screen(img) is False


class TestClassifyFrame:
    def test_classify_frame_my_turn(self):
        img = _make_orange_banner_image()
        assert classify_frame(img) == "my_turn"

    def test_classify_frame_not_my_turn(self):
        img = _make_not_my_turn_image()
        assert classify_frame(img) == "not_my_turn"

    def test_classify_frame_game_over(self):
        img = _make_game_over_image()
        assert classify_frame(img) == "game_over"

    def test_classify_frame_title_screen_as_game_over(self):
        """Title screen should be classified as game_over to prevent processing."""
        img = _make_title_screen_image()
        assert classify_frame(img) == "game_over"

    def test_classify_frame_invalid_bytes(self):
        result = classify_frame(b"not an image at all")
        # Should not crash; returns a safe default
        assert result in ("my_turn", "not_my_turn", "game_over")


# ---------------------------------------------------------------------------
# _is_my_turn threshold tests
# ---------------------------------------------------------------------------


class TestIsMyTurn:
    def test_above_threshold(self):
        img = _make_orange_banner_image()
        assert _is_my_turn(img) is True

    def test_below_threshold(self):
        # Grey image with no orange
        grey = np.full((200, 300, 3), 128, dtype=np.uint8)
        assert _is_my_turn(_encode_png(grey)) is False


# ---------------------------------------------------------------------------
# poll_turn tests (mocked capture_canvas)
# ---------------------------------------------------------------------------


class TestPollTurn:
    @pytest.mark.asyncio
    async def test_poll_turn_returns_my_turn_immediately(self):
        my_turn_img = _make_orange_banner_image()
        page = MagicMock()

        with (
            patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, return_value=my_turn_img),
            patch("src.browser.turn_detector.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await poll_turn(page)

        assert result == "my_turn"

    @pytest.mark.asyncio
    async def test_poll_turn_game_over_detected(self):
        # poll_turn requires at least one gameplay frame before it will return
        # "game_over" (the game_seen guard prevents false positives from
        # lobby/loading screens). Provide a not_my_turn frame first.
        not_my_turn_img = _make_not_my_turn_image()
        game_over_img = _make_game_over_image()
        page = MagicMock()

        with (
            patch(
                "src.browser.capture.capture_canvas",
                new_callable=AsyncMock,
                side_effect=[not_my_turn_img, game_over_img],
            ),
            patch("src.browser.turn_detector.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await poll_turn(page)

        assert result == "game_over"

    @pytest.mark.asyncio
    async def test_poll_turn_slow_polling_after_idle(self):
        """After IDLE_THRESHOLD_S of not_my_turn, polling interval switches to POLL_SLOW_S."""
        not_my_turn_img = _make_not_my_turn_image()
        my_turn_img = _make_orange_banner_image()

        # Return not_my_turn enough times to exceed IDLE_THRESHOLD_S, then my_turn
        polls_to_idle = int(IDLE_THRESHOLD_S / POLL_FAST_S) + 2
        images = [not_my_turn_img] * polls_to_idle + [my_turn_img]

        page = MagicMock()
        sleep_calls = []

        async def track_sleep(duration):
            sleep_calls.append(duration)

        with (
            patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, side_effect=images),
            patch("src.browser.turn_detector.asyncio.sleep", side_effect=track_sleep),
        ):
            result = await poll_turn(page)

        assert result == "my_turn"
        # Verify slow polling was used at some point
        assert POLL_SLOW_S in sleep_calls


# ---------------------------------------------------------------------------
# preflight_check tests
# ---------------------------------------------------------------------------


class TestPreflightCheck:
    @pytest.mark.asyncio
    async def test_preflight_check_passes(self):
        valid_img = _make_not_my_turn_image()
        page = MagicMock()

        with patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, return_value=valid_img):
            # Should not raise
            await preflight_check(page)

    @pytest.mark.asyncio
    async def test_preflight_check_fails_on_capture_error(self):
        page = MagicMock()

        with patch(
            "src.browser.capture.capture_canvas",
            new_callable=AsyncMock,
            side_effect=RuntimeError("blank"),
        ):
            with pytest.raises(RuntimeError, match="Pre-flight"):
                await preflight_check(page)


# ---------------------------------------------------------------------------
# poll_turn idle timeout tests
# ---------------------------------------------------------------------------


class TestPollTurnIdleTimeout:
    @pytest.mark.asyncio
    async def test_poll_turn_returns_idle_timeout(self):
        """After MAX_IDLE_S of not_my_turn, poll_turn returns idle_timeout."""
        not_my_turn_img = _make_not_my_turn_image()
        page = MagicMock()

        # Need enough frames to exceed MAX_IDLE_S
        polls_needed = int(MAX_IDLE_S / POLL_FAST_S) + 10
        images = [not_my_turn_img] * polls_needed

        with (
            patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, side_effect=images),
            patch("src.browser.turn_detector.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await poll_turn(page)

        assert result == "idle_timeout"

    @pytest.mark.asyncio
    async def test_my_turn_before_idle_timeout(self):
        """my_turn returned before idle timeout is reached."""
        not_my_turn_img = _make_not_my_turn_image()
        my_turn_img = _make_orange_banner_image()
        page = MagicMock()

        # A few not_my_turn then my_turn — well before timeout
        images = [not_my_turn_img] * 3 + [my_turn_img]

        with (
            patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, side_effect=images),
            patch("src.browser.turn_detector.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await poll_turn(page)

        assert result == "my_turn"


# ---------------------------------------------------------------------------
# poll_turn stop_event tests
# ---------------------------------------------------------------------------


class TestPollTurnStopEvent:
    @pytest.mark.asyncio
    async def test_stop_event_already_set_returns_stop_requested(self):
        """If stop_event is already set before polling starts, returns stop_requested immediately."""
        not_my_turn_img = _make_not_my_turn_image()
        page = MagicMock()

        stop_event = asyncio.Event()
        stop_event.set()  # already set before poll_turn is called

        with patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, return_value=not_my_turn_img):
            result = await poll_turn(page, stop_event=stop_event)

        assert result == "stop_requested"

    @pytest.mark.asyncio
    async def test_stop_event_fires_during_sleep_returns_stop_requested(self):
        """stop_event set while sleeping between polls returns stop_requested."""
        not_my_turn_img = _make_not_my_turn_image()
        page = MagicMock()

        stop_event = asyncio.Event()

        call_count = 0

        async def set_event_on_second_capture(_page):
            nonlocal call_count
            call_count += 1
            if call_count >= 2:
                stop_event.set()
            return not_my_turn_img

        with patch("src.browser.capture.capture_canvas", side_effect=set_event_on_second_capture):
            result = await poll_turn(page, stop_event=stop_event)

        assert result == "stop_requested"

    @pytest.mark.asyncio
    async def test_no_stop_event_behaves_as_before(self):
        """Without stop_event, poll_turn still returns my_turn normally."""
        my_turn_img = _make_orange_banner_image()
        page = MagicMock()

        with (
            patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, return_value=my_turn_img),
            patch("src.browser.turn_detector.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await poll_turn(page)  # no stop_event

        assert result == "my_turn"


# ---------------------------------------------------------------------------
# wait_for_game_ready tests
# ---------------------------------------------------------------------------


class TestWaitForGameReady:
    @pytest.mark.asyncio
    async def test_ready_immediately(self):
        """Board visible on first capture — returns immediately."""
        board_img = _make_not_my_turn_image()  # has peach board
        page = MagicMock()

        with (
            patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, return_value=board_img),
            patch("src.browser.turn_detector.asyncio.sleep", new_callable=AsyncMock),
        ):
            await wait_for_game_ready(page)  # should not raise

    @pytest.mark.asyncio
    async def test_ready_after_loading_screens(self):
        """Board appears after a few non-board frames."""
        loading_img = _make_game_over_image()  # no peach board
        board_img = _make_not_my_turn_image()   # has peach board
        page = MagicMock()

        images = [loading_img] * 3 + [board_img]

        with (
            patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, side_effect=images),
            patch("src.browser.turn_detector.asyncio.sleep", new_callable=AsyncMock),
        ):
            await wait_for_game_ready(page)  # should not raise

    @pytest.mark.asyncio
    async def test_timeout_raises(self):
        """TimeoutError raised when board never appears."""
        loading_img = _make_game_over_image()
        page = MagicMock()

        with (
            patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, return_value=loading_img),
            patch("src.browser.turn_detector.asyncio.sleep", new_callable=AsyncMock),
            patch("src.browser.turn_detector.GAME_READY_TIMEOUT_S", 4.0),
            patch("src.browser.turn_detector.GAME_READY_POLL_S", 1.0),
        ):
            with pytest.raises(TimeoutError, match="Game board not detected"):
                await wait_for_game_ready(page)
