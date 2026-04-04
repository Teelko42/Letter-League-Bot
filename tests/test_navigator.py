"""Tests for navigator.py (Phase C2).

All Playwright interactions are mocked.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.browser.navigator import navigate_to_activity


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_page(frames=None) -> MagicMock:
    page = MagicMock()
    page.goto = AsyncMock()
    page.keyboard = AsyncMock()
    page.keyboard.press = AsyncMock()
    page.frames = frames or []

    # Default locators
    join_btn = AsyncMock()
    join_btn.wait_for = AsyncMock(side_effect=Exception("not found"))
    join_btn.click = AsyncMock()

    activity_btn = AsyncMock()
    activity_btn.wait_for = AsyncMock()
    activity_btn.click = AsyncMock()

    search_input = AsyncMock()
    search_input.wait_for = AsyncMock()
    search_input.fill = AsyncMock()

    result_locator = MagicMock()
    result_first = AsyncMock()
    result_first.click = AsyncMock()
    result_locator.first = result_first

    play_btn = AsyncMock()
    play_btn.wait_for = AsyncMock(side_effect=Exception("not found"))
    play_btn.click = AsyncMock()

    def locator_side_effect(selector):
        if "Join Voice" in selector:
            return join_btn
        elif "Start An Activity" in selector:
            return activity_btn
        elif "Search" in selector:
            return search_input
        elif "Letter League" in selector:
            return result_locator
        elif "Play" in selector:
            return play_btn
        elif "iframe" in selector:
            return MagicMock()
        return MagicMock()

    page.locator = MagicMock(side_effect=locator_side_effect)
    return page


def _make_frame(url: str = "https://discordsays.com/game") -> MagicMock:
    frame = MagicMock()
    frame.url = url
    return frame


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestNavigateToActivity:
    @pytest.mark.asyncio
    async def test_navigate_success(self):
        """Navigation succeeds when iframe is already present."""
        frame = _make_frame()
        page = _make_page(frames=[frame])

        with patch("src.browser.navigator.asyncio.sleep", new_callable=AsyncMock):
            result = await navigate_to_activity(page, "https://discord.com/channels/123/456")

        assert result is frame

    @pytest.mark.asyncio
    async def test_navigate_retries_on_timeout(self):
        frame = _make_frame()
        attempt = 0

        async def mock_run_navigation(page, channel_url):
            nonlocal attempt
            attempt += 1
            if attempt == 1:
                raise TimeoutError("iframe not found")
            return frame

        with (
            patch("src.browser.navigator._run_navigation", side_effect=mock_run_navigation),
            patch("src.browser.navigator.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await navigate_to_activity(MagicMock(), "https://discord.com/channels/123/456", max_retries=3)

        assert result is frame
        assert attempt == 2

    @pytest.mark.asyncio
    async def test_navigate_raises_after_max_retries(self):
        async def always_fail(page, channel_url):
            raise RuntimeError("iframe not found")

        with (
            patch("src.browser.navigator._run_navigation", side_effect=always_fail),
            patch("src.browser.navigator.asyncio.sleep", new_callable=AsyncMock),
        ):
            with pytest.raises(RuntimeError, match="iframe not found"):
                await navigate_to_activity(MagicMock(), "https://discord.com/channels/123/456", max_retries=2)

    @pytest.mark.asyncio
    async def test_navigate_invalid_channel_url(self):
        """Malformed URL still causes navigation attempt (Discord handles the error)."""
        async def fail_goto(page, channel_url):
            raise RuntimeError("Navigation failed")

        with (
            patch("src.browser.navigator._run_navigation", side_effect=fail_goto),
            patch("src.browser.navigator.asyncio.sleep", new_callable=AsyncMock),
        ):
            with pytest.raises(RuntimeError):
                await navigate_to_activity(MagicMock(), "not-a-url", max_retries=1)
