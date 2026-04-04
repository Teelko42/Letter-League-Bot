"""Tests for capture.py: is_non_blank (Phase A4) and capture_canvas (Phase C1).

is_non_blank tests are pure functions — no mocking needed.
capture_canvas tests mock Playwright.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import cv2
import numpy as np
import pytest

from src.browser.capture import capture_canvas, is_non_blank


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _encode_png(img: np.ndarray) -> bytes:
    """Encode a numpy array as PNG bytes."""
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()


def _colorful_image(h: int = 100, w: int = 100) -> bytes:
    """Create a PNG with varied pixel values (non-blank)."""
    rng = np.random.RandomState(42)
    img = rng.randint(0, 256, (h, w, 3), dtype=np.uint8)
    return _encode_png(img)


# ---------------------------------------------------------------------------
# A4: is_non_blank tests
# ---------------------------------------------------------------------------


class TestIsNonBlank:
    def test_colorful_image(self):
        assert is_non_blank(_colorful_image()) is True

    def test_solid_black(self):
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        assert is_non_blank(_encode_png(img)) is False

    def test_solid_white(self):
        img = np.full((100, 100, 3), 255, dtype=np.uint8)
        assert is_non_blank(_encode_png(img)) is False

    def test_empty_bytes(self):
        assert is_non_blank(b"") is False

    def test_corrupt_bytes(self):
        assert is_non_blank(b"\x00\x01\x02garbage") is False


# ---------------------------------------------------------------------------
# C1: capture_canvas tests (mocked Playwright)
# ---------------------------------------------------------------------------


class TestCaptureCanvas:
    @pytest.mark.asyncio
    async def test_capture_canvas_returns_png_bytes(self):
        valid_png = _colorful_image()
        page = MagicMock()
        iframe_locator = AsyncMock()
        iframe_locator.wait_for = AsyncMock()
        iframe_locator.screenshot = AsyncMock(return_value=valid_png)
        page.locator.return_value = iframe_locator

        with patch("src.browser.capture.asyncio.sleep", new_callable=AsyncMock):
            result = await capture_canvas(page)

        assert result == valid_png
        assert result[:4] == b"\x89PNG"

    @pytest.mark.asyncio
    async def test_capture_canvas_retries_on_blank(self):
        blank_png = _encode_png(np.zeros((100, 100, 3), dtype=np.uint8))
        valid_png = _colorful_image()

        page = MagicMock()
        iframe_locator = AsyncMock()
        iframe_locator.wait_for = AsyncMock()
        iframe_locator.screenshot = AsyncMock(side_effect=[blank_png, valid_png])
        page.locator.return_value = iframe_locator

        with patch("src.browser.capture.asyncio.sleep", new_callable=AsyncMock):
            result = await capture_canvas(page, max_retries=2)

        assert result == valid_png
        assert iframe_locator.screenshot.call_count == 2

    @pytest.mark.asyncio
    async def test_capture_canvas_raises_after_max_retries(self):
        blank_png = _encode_png(np.zeros((100, 100, 3), dtype=np.uint8))

        page = MagicMock()
        iframe_locator = AsyncMock()
        iframe_locator.wait_for = AsyncMock()
        iframe_locator.screenshot = AsyncMock(return_value=blank_png)
        page.locator.return_value = iframe_locator

        with patch("src.browser.capture.asyncio.sleep", new_callable=AsyncMock):
            with pytest.raises(RuntimeError, match="blank after 2 attempts"):
                await capture_canvas(page, max_retries=2)
