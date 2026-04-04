from __future__ import annotations

import asyncio
from typing import Any

import cv2
import numpy as np
from loguru import logger


def is_non_blank(img_bytes: bytes, threshold: float = 5.0) -> bool:
    """Check whether image bytes represent a non-blank screenshot.

    Decodes the bytes and uses pixel standard deviation as a proxy for content.
    A completely blank or near-uniform image will have a very low std dev.

    Args:
        img_bytes: Raw image bytes (PNG, JPEG, or any OpenCV-supported format).
        threshold: Minimum standard deviation across all pixels to be considered
            non-blank. Default 5.0 is deliberately conservative — real game
            screenshots exceed this by orders of magnitude.

    Returns:
        True if the image decodes successfully and has pixel variance above
        threshold; False if decoding fails or image is blank/near-blank.
    """
    if not img_bytes:
        return False

    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        return False

    return float(np.std(img)) > threshold


async def capture_canvas(
    page: Any,
    max_retries: int = 3,
    render_wait: bool = True,
) -> bytes:
    """Capture a screenshot of the Letter League game from the Activity iframe.

    Waits for the iframe to be visible, then screenshots the iframe element
    directly. Validates that the screenshot is non-blank (pixel variance check).
    Retries up to max_retries times if the screenshot is blank.

    Args:
        page: A patchright Page object (typed as Any to avoid import complexity).
        max_retries: Maximum number of blank-screenshot retries.
        render_wait: If True (default), wait 3 seconds for the game to finish
            rendering after navigation.  Set to False for fast captures during
            placement verification where the game is already rendered.

    Returns:
        Non-blank PNG screenshot bytes of the game.

    Raises:
        RuntimeError: If all retries yield a blank screenshot.
    """
    # Wait for the activity iframe to be visible.
    iframe_locator = page.locator('iframe[src*="discordsays.com"]')
    try:
        await iframe_locator.wait_for(state="visible", timeout=30_000)
        logger.info("Activity iframe visible")
    except Exception:
        logger.warning("Activity iframe not visible after 30s")

    if render_wait:
        await asyncio.sleep(3.0)  # Buffer for game render completion
    else:
        await asyncio.sleep(0.3)  # Brief settle time for fast captures

    for attempt in range(1, max_retries + 1):
        screenshot_bytes: bytes = await iframe_locator.screenshot(timeout=15_000)

        if is_non_blank(screenshot_bytes):
            logger.info(
                "Game screenshot captured — {} bytes (attempt {})",
                len(screenshot_bytes),
                attempt,
            )
            return screenshot_bytes

        if attempt < max_retries:
            logger.warning(
                "Screenshot blank (attempt {}/{}), retrying...", attempt, max_retries
            )
            await asyncio.sleep(2)
        else:
            logger.error(
                "Game screenshot is blank after {} attempts", max_retries
            )

    raise RuntimeError(
        f"Game screenshot is blank after {max_retries} attempts"
    )
