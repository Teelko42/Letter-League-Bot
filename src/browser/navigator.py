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
    # Step 2a: Dismiss any blocking modals (e.g. "How'd the call go?")
    # ------------------------------------------------------------------
    await asyncio.sleep(2)  # let page settle
    await page.keyboard.press("Escape")
    await asyncio.sleep(0.5)

    # ------------------------------------------------------------------
    # Step 2b: Join the voice channel if a Join Voice button is visible
    # ------------------------------------------------------------------
    join_btn = page.locator('button:has-text("Join Voice")')
    try:
        await join_btn.wait_for(state="visible", timeout=10_000)
        logger.info("Join Voice button found — clicking to join voice channel")
        await join_btn.click()
        await asyncio.sleep(3)  # Wait for voice UI to fully load
    except Exception:
        logger.info("No Join Voice button — assuming already in voice channel")

    # ------------------------------------------------------------------
    # Step 3: Click the Activity shelf rocket button
    # ------------------------------------------------------------------
    activity_btn = page.locator('button[aria-label="Start An Activity"]')
    await activity_btn.wait_for(state="visible", timeout=15_000)
    await activity_btn.click()
    logger.info("Opened Activity shelf")

    # ------------------------------------------------------------------
    # Step 4: Launch Letter League (or detect already running)
    # ------------------------------------------------------------------
    # Check if the Activity iframe is already present (game in progress)
    for f in page.frames:
        if re.search(r"discordsays\.com", f.url):
            logger.info("Activity iframe already present — skipping launch")
            return f

    await asyncio.sleep(1)  # let shelf animate in
    search_input = page.locator('input[placeholder="Search"]')
    await search_input.wait_for(state="visible", timeout=10_000)
    await search_input.fill("Letter League")
    await asyncio.sleep(1)  # wait for search results

    # Click the first search result that matches
    result = page.locator('text="Letter League"').first
    await result.click(force=True, timeout=10_000)
    logger.info("Selected Letter League from shelf")

    # Click the "Play" button if it appears (not shown when game already exists)
    play_btn = page.locator('button:has-text("Play")')
    try:
        await play_btn.wait_for(state="visible", timeout=5_000)
        await play_btn.click()
        logger.info("Clicked Play — launching activity")
    except Exception:
        logger.info("No Play button — game may already be launching")

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
