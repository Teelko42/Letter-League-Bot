from __future__ import annotations

import asyncio
import re
from typing import Any

from loguru import logger


async def navigate_to_activity(
    page: Any,
    channel_url: str,
    max_retries: int = 3,
) -> Any:
    """Navigate to a Discord voice channel and launch the Letter League Activity.

    Navigates to the given Discord channel URL, joins the voice channel if needed,
    opens the Activity shelf, selects Letter League, and waits for the Activity
    iframe to appear.

    Args:
        page: A patchright Page object (typed as Any to avoid import complexity).
        channel_url: The full Discord channel URL, e.g.
            "https://discord.com/channels/SERVER_ID/CHANNEL_ID".
        max_retries: Number of attempts before re-raising the last exception.

    Returns:
        A patchright Frame object for the discordsays.com Activity iframe.

    Raises:
        RuntimeError: If the Activity iframe does not appear within 30 seconds on
            the final retry attempt.
    """
    last_exc: Exception | None = None

    for attempt in range(1, max_retries + 1):
        try:
            return await _run_navigation(page, channel_url)
        except Exception as exc:
            last_exc = exc
            if attempt < max_retries:
                logger.warning(
                    "Navigation attempt {}/{} failed: {}. Retrying in 3 seconds...",
                    attempt,
                    max_retries,
                    exc,
                )
                await asyncio.sleep(3)
            else:
                logger.error(
                    "Navigation failed after {} attempts: {}", max_retries, exc
                )

    raise last_exc  # type: ignore[misc]


async def _run_navigation(page: Any, channel_url: str) -> Any:
    """Execute the full navigation sequence (single attempt).

    Args:
        page: A patchright Page object.
        channel_url: The full Discord channel URL.

    Returns:
        A patchright Frame object for the discordsays.com Activity iframe.
    """
    # ------------------------------------------------------------------
    # Step 1: Navigate to the voice channel
    # ------------------------------------------------------------------
    await page.goto(channel_url, wait_until="domcontentloaded")
    logger.info("Navigated to channel: {}", channel_url)

    # ------------------------------------------------------------------
    # Step 2: Join the voice channel if a Join Voice button is visible
    # ------------------------------------------------------------------
    join_btn = page.locator('button:has-text("Join Voice")')
    if await join_btn.count() > 0:
        logger.info("Join Voice button found — clicking to join voice channel")
        await join_btn.click()
        await asyncio.sleep(2)  # Wait for voice panel to appear
    else:
        logger.info("Already in voice channel or no Join Voice button found")

    # ------------------------------------------------------------------
    # Step 3: Click the Activity shelf rocket button
    # ------------------------------------------------------------------
    activity_btn = page.locator('button[aria-label="Start an Activity"]')
    await activity_btn.wait_for(state="visible", timeout=10_000)
    await activity_btn.click()
    logger.info("Opened Activity shelf")

    # ------------------------------------------------------------------
    # Step 4: Select Letter League from the Activity shelf
    # ------------------------------------------------------------------
    letter_league_btn = page.get_by_text("Letter League", exact=False).first
    await letter_league_btn.wait_for(state="visible", timeout=10_000)
    await letter_league_btn.click()
    logger.info("Launched Letter League activity")

    # ------------------------------------------------------------------
    # Step 5: Wait for the Activity iframe (discordsays.com)
    # ------------------------------------------------------------------
    deadline = 30  # seconds
    poll_interval = 0.5
    elapsed = 0.0

    while elapsed < deadline:
        for frame in page.frames:
            if re.search(r"discordsays\.com", frame.url):
                logger.info("Activity iframe found: {}", frame.url)
                return frame
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    raise RuntimeError("Activity iframe did not appear within 30 seconds")
