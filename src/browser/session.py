from __future__ import annotations

import sys
from pathlib import Path

from loguru import logger


class BrowserSession:
    """Manages a persistent patchright (Playwright) browser session for Discord.

    Three flows:
    1. First-run: headed launch → manual Discord login → session saved.
    2. Returning: headless launch → session validation → proceed.
    3. Expired session: log clear operator error → clean exit.
    """

    _LOGIN_SELECTOR = '[data-list-id="guildsnav"]'
    _LOGIN_TIMEOUT_MS = 300_000  # 5 minutes

    def __init__(self, profile_dir: str = "./browser_data") -> None:
        self._profile_dir = profile_dir
        self._pw = None
        self._context = None
        self._page = None

    async def start(self):
        """Launch browser and return an authenticated Page.

        Detects first-run vs returning session automatically.
        Exits the process if the session has expired.

        Returns:
            A patchright Page object ready for navigation.
        """
        is_first_run = not self._profile_exists()
        await self._launch(headless=not is_first_run)

        # Get or create a page from the persistent context.
        if self._context.pages:
            page = self._context.pages[0]
        else:
            page = await self._context.new_page()
        self._page = page

        if is_first_run:
            await self._first_run_login(page)
        else:
            valid = await self._validate_session(page)
            if not valid:
                logger.error(
                    "Discord session has expired. "
                    "Delete ./browser_data/ and re-run to log in again."
                )
                await self.close()
                sys.exit(1)

        return page

    async def _launch(self, headless: bool) -> None:
        """Launch a patchright persistent context at the configured profile directory.

        Args:
            headless: True for normal headless operation; False for first-run login.
        """
        from patchright.async_api import async_playwright

        self._pw = await async_playwright().start()
        self._context = await self._pw.chromium.launch_persistent_context(
            user_data_dir=self._profile_dir,
            headless=headless,
            viewport={"width": 1280, "height": 800},
        )

    def _profile_exists(self) -> bool:
        """Return True if the Chrome profile Cookies file exists at profile_dir."""
        cookies_path = Path(self._profile_dir) / "Default" / "Cookies"
        return cookies_path.exists()

    async def _first_run_login(self, page) -> None:
        """Open Discord login page and wait for the operator to complete login.

        Waits up to 5 minutes for the guild nav sidebar to appear, which indicates
        a successful login. Exits cleanly on timeout.

        Args:
            page: A patchright Page object.
        """
        logger.info(
            "First run detected — please log into Discord in the browser window."
        )
        await page.goto("https://discord.com/login")
        try:
            await page.wait_for_selector(
                self._LOGIN_SELECTOR, timeout=self._LOGIN_TIMEOUT_MS
            )
            logger.info("Discord login detected — session saved.")
        except Exception:
            logger.error("Login timed out after 5 minutes.")
            await self.close()
            sys.exit(1)

    async def _validate_session(self, page) -> bool:
        """Navigate to Discord home and check whether the session is still valid.

        Args:
            page: A patchright Page object.

        Returns:
            True if the session is valid (not redirected to login); False otherwise.
        """
        await page.goto(
            "https://discord.com/channels/@me", wait_until="domcontentloaded"
        )
        return "login" not in page.url

    async def close(self) -> None:
        """Close the browser context and stop the Playwright instance."""
        if self._context is not None:
            await self._context.close()
            self._context = None
        if self._pw is not None:
            await self._pw.stop()
            self._pw = None
