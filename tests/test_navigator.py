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


def _make_locator(*, wait_for_exc=None, is_visible=False, click_exc=None):
    """Build a synchronous MagicMock that looks like a Playwright Locator.

    Playwright Locator is returned synchronously by page.locator() but its
    methods (wait_for, click, is_visible, fill) are coroutines.  The .or_()
    method is synchronous and returns another Locator — we make it return the
    same mock so chaining works transparently.
    """
    loc = MagicMock()
    loc.wait_for = AsyncMock(side_effect=wait_for_exc) if wait_for_exc else AsyncMock()
    loc.click = AsyncMock(side_effect=click_exc) if click_exc else AsyncMock()
    loc.is_visible = AsyncMock(return_value=is_visible)
    loc.fill = AsyncMock()
    # .or_() is synchronous and returns a Locator — return self for simplicity
    loc.or_ = MagicMock(return_value=loc)
    loc.first = loc  # for .first chaining
    loc.count = AsyncMock(return_value=0)
    return loc


def _make_page(frames=None) -> MagicMock:
    page = MagicMock()
    page.goto = AsyncMock()
    page.keyboard = AsyncMock()
    page.keyboard.press = AsyncMock()
    page.frames = frames or []

    # Default locators
    join_btn = _make_locator(wait_for_exc=Exception("not found"))
    activity_btn = _make_locator()
    post_call_modal = _make_locator(is_visible=False)
    search_input = _make_locator()
    result_locator = _make_locator()
    play_btn = _make_locator(wait_for_exc=Exception("not found"))

    def locator_side_effect(selector):
        if "How" in selector and "call" in selector:
            return post_call_modal
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
            return _make_locator()
        return _make_locator()

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
