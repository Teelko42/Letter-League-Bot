"""Tests for BrowserSession (Phase C3).

Patchright/Playwright is fully mocked.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.browser.session import BrowserSession


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestBrowserSession:
    @pytest.mark.asyncio
    async def test_start_creates_context(self):
        session = BrowserSession(profile_dir="./test_profile")

        mock_page = AsyncMock()
        type(mock_page).url = "https://discord.com/channels/@me"
        mock_page.goto = AsyncMock()

        mock_context = AsyncMock()
        mock_context.pages = [mock_page]

        mock_pw = AsyncMock()
        mock_pw.chromium.launch_persistent_context = AsyncMock(return_value=mock_context)

        mock_playwright_cm = AsyncMock()
        mock_playwright_cm.start = AsyncMock(return_value=mock_pw)

        with (
            patch.object(session, "_profile_exists", return_value=True),
            patch("patchright.async_api.async_playwright", return_value=mock_playwright_cm),
            patch.object(session, "_validate_session", new_callable=AsyncMock, return_value=True),
        ):
            page = await session.start()

        assert page is mock_page

    @pytest.mark.asyncio
    async def test_stop_closes_resources(self):
        session = BrowserSession()
        mock_context = AsyncMock()
        mock_pw = AsyncMock()
        session._context = mock_context
        session._pw = mock_pw

        await session.close()

        mock_context.close.assert_called_once()
        mock_pw.stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_validates_login(self):
        session = BrowserSession()
        page = AsyncMock()
        page.goto = AsyncMock()
        type(page).url = "https://discord.com/channels/@me"

        result = await session._validate_session(page)
        assert result is True

    @pytest.mark.asyncio
    async def test_session_expired(self):
        session = BrowserSession()
        page = AsyncMock()
        page.goto = AsyncMock()
        type(page).url = "https://discord.com/login?redirect_to=%2Fchannels%2F%40me"

        result = await session._validate_session(page)
        assert result is False
