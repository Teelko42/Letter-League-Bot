"""Browser foundation end-to-end test.

Chains: BrowserSession.start() -> navigate_to_activity() -> capture_canvas() -> extract_board_state()

Usage:
    python -m scripts.browser_test
"""
from __future__ import annotations

import asyncio
import os
import sys

from dotenv import load_dotenv
from loguru import logger

from src.browser.session import BrowserSession
from src.browser.navigator import navigate_to_activity
from src.browser.capture import capture_canvas
from src.vision import extract_board_state


async def main() -> None:
    load_dotenv()
    channel_url = os.getenv("DISCORD_CHANNEL_URL")
    if not channel_url:
        logger.error("DISCORD_CHANNEL_URL not set in .env")
        sys.exit(1)

    session = BrowserSession()
    try:
        page = await session.start()
        frame = await navigate_to_activity(page, channel_url)
        screenshot = await capture_canvas(page, frame)

        # Full vision pipeline validation (locked decision — not just non-blank)
        board, rack = await extract_board_state(screenshot)
        logger.info("Vision pipeline OK — Board: {}x{}, Rack: {}", board.rows, board.cols, rack)
    except Exception:
        logger.exception("Browser test failed")
        sys.exit(1)
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
