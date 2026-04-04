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
    IDLE_THRESHOLD_S,
    POLL_FAST_S,
    POLL_SLOW_S,
    _is_game_over,
    _is_my_turn,
    classify_frame,
    poll_turn,
    preflight_check,
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


# ---------------------------------------------------------------------------
# classify_frame tests
# ---------------------------------------------------------------------------


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
        game_over_img = _make_game_over_image()
        page = MagicMock()

        with (
            patch("src.browser.capture.capture_canvas", new_callable=AsyncMock, return_value=game_over_img),
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
