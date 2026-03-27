"""Debug: headed session to inspect Activity iframe discovery.

Runs headed so you can see the browser. Dumps all frame URLs after each step.
"""
from __future__ import annotations

import asyncio
import os
import re
import sys

from dotenv import load_dotenv
from loguru import logger


async def main() -> None:
    load_dotenv()
    channel_url = os.getenv("DISCORD_CHANNEL_URL")
    if not channel_url:
        logger.error("DISCORD_CHANNEL_URL not set in .env")
        sys.exit(1)

    from patchright.async_api import async_playwright

    pw = await async_playwright().start()
    ctx = await pw.chromium.launch_persistent_context(
        user_data_dir="./browser_data",
        headless=False,
        viewport={"width": 1280, "height": 800},
    )

    page = ctx.pages[0] if ctx.pages else await ctx.new_page()

    def dump_frames(label: str) -> None:
        logger.info("=== FRAMES after: {} ===", label)
        for i, f in enumerate(page.frames):
            logger.info("  [{}] {}", i, f.url)
        logger.info("=== END FRAMES ===")

    # Step 1: Navigate to channel
    await page.goto(channel_url, wait_until="domcontentloaded")
    await asyncio.sleep(2)
    dump_frames("goto channel")

    # Step 2: Dismiss modals
    await page.keyboard.press("Escape")
    await asyncio.sleep(1)

    # Step 3: Join voice if needed
    join_btn = page.locator('button:has-text("Join Voice")')
    try:
        await join_btn.wait_for(state="visible", timeout=10_000)
        logger.info("Clicking Join Voice...")
        await join_btn.click()
        await asyncio.sleep(3)
    except Exception:
        logger.info("No Join Voice button")

    dump_frames("after join voice")

    # Step 4: Click Activity shelf
    activity_btn = page.locator('button[aria-label="Start An Activity"]')
    try:
        await activity_btn.wait_for(state="visible", timeout=15_000)
        await activity_btn.click()
        logger.info("Opened Activity shelf")
        await asyncio.sleep(2)
    except Exception:
        logger.warning("Activity shelf button not found — trying alternate selectors")
        # Try alternate selectors
        for selector in [
            'button[aria-label="Activities"]',
            'button[aria-label="Start an Activity"]',
            '[class*="activity"] button',
        ]:
            try:
                btn = page.locator(selector)
                await btn.wait_for(state="visible", timeout=3_000)
                await btn.click()
                logger.info("Found activity button with: {}", selector)
                await asyncio.sleep(2)
                break
            except Exception:
                continue

    dump_frames("after activity shelf")

    # Step 5: Search and select Letter League
    search_input = page.locator('input[placeholder="Search"]')
    try:
        await search_input.wait_for(state="visible", timeout=10_000)
        await search_input.fill("Letter League")
        await asyncio.sleep(1)
        result = page.locator('text="Letter League"').first
        await result.click(force=True, timeout=10_000)
        logger.info("Selected Letter League")
        await asyncio.sleep(2)
    except Exception as e:
        logger.warning("Search/select failed: {}", e)

    dump_frames("after select Letter League")

    # Step 6: Click Play if available
    play_btn = page.locator('button:has-text("Play")')
    try:
        await play_btn.wait_for(state="visible", timeout=5_000)
        await play_btn.click()
        logger.info("Clicked Play")
    except Exception:
        logger.info("No Play button")

    # Step 7: Wait and poll for frames
    logger.info("Polling frames for 60 seconds...")
    for i in range(60):
        await asyncio.sleep(1)
        for frame in page.frames:
            if re.search(r"discordsays\.com|letter.?league|activities", frame.url, re.IGNORECASE):
                logger.info(">>> FOUND TARGET FRAME: {}", frame.url)
        if i % 10 == 9:
            dump_frames(f"poll {i+1}s")

    dump_frames("final (60s)")

    logger.info("Debug complete. Browser stays open — press Ctrl+C to close.")
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, asyncio.CancelledError):
        pass
    finally:
        await ctx.close()
        await pw.stop()


if __name__ == "__main__":
    asyncio.run(main())
