from __future__ import annotations

import asyncio
import base64
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
    frame: Any,
    max_retries: int = 3,
) -> bytes:
    """Capture a screenshot of the Letter League canvas from the Activity iframe.

    Waits for the page to reach network idle, then captures the canvas element
    using a FrameLocator screenshot call. Falls back to a JavaScript
    canvas.toDataURL() call if the primary method fails.

    Validates that the screenshot is non-blank (pixel variance check). Retries
    up to max_retries times if the screenshot is blank.

    Args:
        page: A patchright Page object (typed as Any to avoid import complexity).
        frame: A patchright Frame object pointing to the discordsays.com iframe
            (typed as Any to avoid import complexity).
        max_retries: Maximum number of blank-screenshot retries.

    Returns:
        Non-blank PNG screenshot bytes of the game canvas.

    Raises:
        RuntimeError: If all retries yield a blank screenshot.
    """
    # Wait for the page and iframe to finish loading before capturing.
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(1.0)  # Extra buffer for canvas render completion

    for attempt in range(1, max_retries + 1):
        screenshot_bytes = await _capture_once(page, frame)

        if is_non_blank(screenshot_bytes):
            logger.info(
                "Canvas screenshot captured — {} bytes (attempt {})",
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
                "Canvas screenshot is blank after {} attempts", max_retries
            )

    raise RuntimeError(
        f"Canvas screenshot is blank after {max_retries} attempts"
    )


async def _capture_once(page: Any, frame: Any) -> bytes:
    """Attempt a single canvas capture, falling back to JS toDataURL if needed.

    Args:
        page: A patchright Page object.
        frame: A patchright Frame object for the Activity iframe.

    Returns:
        Raw screenshot bytes (PNG).
    """
    try:
        # Primary method: use FrameLocator to target the canvas inside the iframe.
        canvas_locator = (
            page.frame_locator('iframe[src*="discordsays.com"]')
            .locator("canvas")
            .first
        )
        screenshot_bytes: bytes = await canvas_locator.screenshot()
        return screenshot_bytes
    except Exception as primary_exc:
        logger.warning(
            "Primary canvas screenshot failed ({}), falling back to toDataURL",
            primary_exc,
        )

    # Fallback method: evaluate canvas.toDataURL() inside the iframe context.
    data_url: str = await frame.evaluate(
        "document.querySelector('canvas').toDataURL('image/png')"
    )
    # data_url is "data:image/png;base64,<base64data>"
    b64_data = data_url.split(",", 1)[1]
    return base64.b64decode(b64_data)
