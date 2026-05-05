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
        RuntimeError: If the Activity iframe does not appear within 60 seconds on
            the final retry attempt.
    """
    last_exc: BaseException | None = None

    # Per-attempt ceiling — Playwright can hang silently if the browser wedges;
    # wait_for converts that into a TimeoutError the retry loop can recover from.
    per_attempt_timeout_s = 120.0

    for attempt in range(1, max_retries + 1):
        try:
            # On retry, force a reload — Discord's SPA can hold stale
            # activity-shelf state that page.goto(same_url) won't clear.
            if attempt > 1:
                try:
                    await asyncio.wait_for(
                        page.reload(wait_until="domcontentloaded"),
                        timeout=20.0,
                    )
                    logger.info("Hard-reloaded page before retry {}", attempt)
                    await asyncio.sleep(2)
                except Exception as reload_exc:
                    logger.warning(
                        "Page reload before retry {} failed: {}", attempt, reload_exc
                    )
            return await asyncio.wait_for(
                _run_navigation(page, channel_url),
                timeout=per_attempt_timeout_s,
            )
        except (Exception, asyncio.TimeoutError) as exc:
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

    # Settle for SPA re-render — wait_for can race with the launcher card mount.
    await asyncio.sleep(2)

    # Click the launcher button if it appears (not shown when game already
    # exists). Discord varies the label by activity state: "Play" for fresh
    # launches; "Launch", "Start Activity", "Resume", or "Join Activity" when a
    # previous session is winding down or has ended.
    launcher_selectors = (
        'button:has-text("Play")',
        'button:has-text("Launch")',
        'button:has-text("Start Activity")',
        'button:has-text("Resume")',
        'button:has-text("Join Activity")',
    )

    async def _try_click_launcher() -> bool:
        """Best-effort click on whichever launcher button is currently visible."""
        for sel in launcher_selectors:
            loc = page.locator(sel).first
            try:
                if await loc.is_visible():
                    await loc.click(force=True, timeout=3_000)
                    logger.info("Clicked launcher button: {}", sel)
                    return True
            except Exception as click_exc:
                logger.debug("Launcher click on {} failed: {}", sel, click_exc)
                continue
        return False

    launcher_btn = page.locator(launcher_selectors[0])
    for _sel in launcher_selectors[1:]:
        launcher_btn = launcher_btn.or_(page.locator(_sel))
    try:
        await launcher_btn.wait_for(state="visible", timeout=8_000)
        if not await _try_click_launcher():
            # wait_for matched but every individual selector reported
            # not-visible — fall back to clicking .first directly so we at
            # least try something.
            await launcher_btn.first.click(force=True, timeout=3_000)
            logger.info("Clicked launcher button — launching activity (fallback)")
    except Exception as exc:
        # Log the exception type so it's clear whether wait_for timed out,
        # the frame detached, or the click raised.
        logger.info(
            "No launcher button — game may already be launching ({}: {})",
            type(exc).__name__, exc,
        )

    # ------------------------------------------------------------------
    # Step 5: Wait for the Activity iframe (discordsays.com)
    # ------------------------------------------------------------------
    # Cold-start can take >30s when Discord has to spin up a new activity
    # session (especially right after a previous session ended). Give it
    # more time before declaring failure.
    deadline = 60  # seconds
    poll_interval = 0.5
    elapsed = 0.0
    # Periodically re-click the launcher: the initial click can land before
    # the button finishes mounting, leaving us waiting on an iframe Discord
    # never spawned.
    last_relaunch_at = 0.0

    while elapsed < deadline:
        for frame in page.frames:
            if re.search(r"discordsays\.com", frame.url):
                logger.info("Activity iframe found: {}", frame.url)
                await _hide_chat_panel(page)
                return frame
        if elapsed - last_relaunch_at >= 15:
            try:
                if await _try_click_launcher():
                    logger.info("Re-clicked launcher mid-wait (iframe still absent)")
            except Exception as relaunch_exc:
                logger.debug("Mid-wait launcher retry failed: {}", relaunch_exc)
            last_relaunch_at = elapsed
        await asyncio.sleep(poll_interval)
        elapsed += poll_interval

    # Dump all frame URLs to disambiguate "iframe loaded under an unexpected
    # URL pattern" from "iframe never loaded at all".
    try:
        frame_urls = [getattr(f, "url", "<no-url>") for f in page.frames]
        logger.error(
            "Iframe wait timed out after {}s. Page frames ({}): {}",
            deadline,
            len(frame_urls),
            frame_urls,
        )
    except Exception as exc:
        logger.error("Iframe wait timed out and frame dump failed: {}", exc)

    raise RuntimeError(
        f"Activity iframe did not appear within {deadline} seconds"
    )


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
