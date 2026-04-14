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
    # Step 2a: Let the SPA render, then dismiss any blocking modals
    #          that appeared from a *previous* session (e.g. "How'd the
    #          call go?").  We only press Escape if such a modal is
    #          actually visible — pressing it unconditionally risks
    #          closing the "Join Voice" prompt that Discord shows when
    #          navigating to an unjoined voice channel.
    # ------------------------------------------------------------------
    await asyncio.sleep(2)  # let page settle / React render

    post_call_modal = page.locator('text="How\'d the call go?"')
    try:
        is_visible = await post_call_modal.is_visible()
        if is_visible:
            logger.info("Post-call modal visible — dismissing with Escape")
            await page.keyboard.press("Escape")
            await asyncio.sleep(0.5)
    except Exception:
        pass  # modal check failed — safe to ignore

    # ------------------------------------------------------------------
    # Step 2b: Join the voice channel if a Join Voice button is visible.
    #
    #          Discord renders the join button as a <button> whose
    #          visible text is "Join Voice".  We combine all known
    #          selector variants into a single locator using .or() so
    #          that we wait once (10 s) rather than waiting 10 s per
    #          selector.  This also avoids a 30-second cascade in the
    #          "already in voice" case where none of the selectors match.
    # ------------------------------------------------------------------
    join_btn = (
        page.locator('button:has-text("Join Voice")')
        .or_(page.locator('button[aria-label="Join Voice"]'))
        .or_(page.locator('button[aria-label="Join Voice Channel"]'))
    )
    try:
        await join_btn.wait_for(state="visible", timeout=10_000)
        logger.info("Join Voice button found — clicking to join voice channel")
        await join_btn.click()
        await asyncio.sleep(3)  # Wait for voice UI to fully load
    except Exception:
        logger.info("No Join Voice button found — assuming already in voice channel")

    # Dismiss any post-join overlays (e.g. "How'd the call go?" scrim)
    await page.keyboard.press("Escape")
    await asyncio.sleep(1)

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
            await _hide_chat_panel(page)
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
                await _hide_chat_panel(page)
                return frame
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    raise RuntimeError("Activity iframe did not appear within 30 seconds")


async def _hide_chat_panel(page: Any) -> None:
    """Hide the right-side text chat panel to maximise Activity iframe space.

    Discord shows a voice-channel text chat panel on the right. The toggle
    is an unlabeled button in the center toolbar. We detect the chat via
    the ``<section>`` element and toggle it off if visible.
    """
    # Check if chat panel is actually visible
    chat_section = page.locator('section[aria-label*="Text chat"]')
    try:
        is_visible = await chat_section.is_visible()
        if not is_visible:
            logger.info("Chat panel already hidden")
            return
    except Exception:
        logger.info("Could not check chat panel visibility — skipping")
        return

    logger.info("Chat panel is visible — attempting to close it")

    # Strategy 1: Click the "Hide Chat" or "Show Chat" toggle button.
    for label_pattern in ["Hide Chat", "Show Chat", "Chat"]:
        toggle_btn = page.locator(f'button[aria-label*="{label_pattern}"]')
        try:
            if await toggle_btn.count() > 0:
                await toggle_btn.first.click(force=True, timeout=5_000)
                await asyncio.sleep(1)
                if not await chat_section.is_visible():
                    logger.info("Chat panel closed via '{}' button", label_pattern)
                    return
                # Undo if it toggled wrong way
                await toggle_btn.first.click(force=True, timeout=5_000)
                await asyncio.sleep(0.5)
        except Exception:
            pass

    # Strategy 2: Click any unlabeled center toolbar button that toggles chat off.
    center_btns = page.locator('button[class*="centerButton"]')
    try:
        count = await center_btns.count()
        for i in range(count):
            btn = center_btns.nth(i)
            label = await btn.get_attribute("aria-label", timeout=2_000) or ""
            if not label:
                await btn.click(force=True, timeout=5_000)
                await asyncio.sleep(1)
                if not await chat_section.is_visible():
                    logger.info("Chat panel closed via unlabeled toolbar button")
                    return
                await btn.click(force=True, timeout=5_000)
                await asyncio.sleep(0.5)
    except Exception as exc:
        logger.debug("Toolbar button approach failed: {}", exc)

    # Fallback: hide the chat panel via DOM manipulation and expand the iframe.
    try:
        hidden = await page.evaluate("""(() => {
            const section = document.querySelector('section[aria-label*="Text chat"]');
            if (!section) return false;

            // Walk up from the chat section to find the flex/grid container that
            // splits the activity iframe and the chat panel side-by-side.
            let chatColumn = section;
            while (chatColumn && chatColumn.parentElement) {
                const parent = chatColumn.parentElement;
                const style = window.getComputedStyle(parent);
                // The split container is typically a flex row
                if (style.display === 'flex' && style.flexDirection === 'row') {
                    // Hide the chat column entirely
                    chatColumn.style.display = 'none';
                    // Make the iframe sibling fill all available space
                    for (const sibling of parent.children) {
                        if (sibling !== chatColumn) {
                            sibling.style.flex = '1 1 100%';
                            sibling.style.maxWidth = '100%';
                            sibling.style.width = '100%';
                        }
                    }
                    // Also expand the iframe element itself
                    const iframe = parent.querySelector('iframe[src*="discordsays"]');
                    if (iframe) {
                        iframe.style.width = '100%';
                        iframe.style.maxWidth = '100%';
                    }
                    return true;
                }
                chatColumn = parent;
            }
            // Direct hide as last resort
            section.style.display = 'none';
            return true;
        })()""")
        if hidden:
            await asyncio.sleep(1)
            logger.info("Chat panel hidden via DOM manipulation")
            return
    except Exception as exc:
        logger.debug("DOM hide approach failed: {}", exc)

    logger.warning("Could not close chat panel — game may render at reduced width")
