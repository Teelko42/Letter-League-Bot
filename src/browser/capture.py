from __future__ import annotations

import asyncio
from typing import Any

import cv2
import numpy as np
from loguru import logger

# Module-level flag: once we've seen the Activity iframe visible we skip
# the ~30 s wait_for on subsequent captures. A screenshot failure clears
# the flag so the next capture re-verifies the iframe is alive.
_iframe_verified = False


def invalidate_iframe_cache() -> None:
    """Force the next capture_canvas() to re-run its visibility wait_for().

    Call after a navigator re-launch or any event that could have replaced
    the iframe. Idempotent — cheap to call speculatively.
    """
    global _iframe_verified
    _iframe_verified = False


async def _log_iframe_missing_diagnostic(page: Any) -> None:
    """Log details about the page state when the iframe screenshot fails.

    Guess-free diagnostic for 'iframe disappeared mid-game' bugs: dumps the
    current page.url, the list of frame URLs still attached, and saves a
    viewport-level screenshot to debug/iframe_missing.png so we can see
    whatever Discord is showing in place of the activity. Best-effort — any
    exception is swallowed so this never masks the original screenshot error.
    """
    try:
        url = page.url
        frames = [f.url for f in page.frames if f.url]
        logger.warning(
            "Iframe screenshot failed — page.url={!r}, {} frames attached: {}",
            url, len(frames), frames,
        )
        from pathlib import Path
        debug_path = Path("debug") / "iframe_missing.png"
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(debug_path), timeout=10_000)
        logger.warning("Viewport screenshot saved -> {}", debug_path)
    except Exception as exc:
        logger.debug("iframe-missing diagnostic best-effort failed: {}", exc)


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
    global _iframe_verified

    # Wait for the activity iframe to be visible on first call only. Once
    # verified, we skip the wait_for — it's redundant and adds ~100 ms per
    # capture when the iframe is alive, and 30 s when it's dead. A
    # screenshot failure below resets the flag so the next capture re-verifies.
    iframe_locator = page.locator('iframe[src*="discordsays.com"]')
    if not _iframe_verified:
        try:
            await iframe_locator.wait_for(state="visible", timeout=30_000)
            _iframe_verified = True
            logger.info("Activity iframe verified visible")
        except Exception:
            logger.warning("Activity iframe not visible after 30s")

    if render_wait:
        await asyncio.sleep(3.0)  # Buffer for game render completion
    else:
        await asyncio.sleep(0.3)  # Brief settle time for fast captures

    for attempt in range(1, max_retries + 1):
        try:
            # Python-side hard ceiling around the Playwright screenshot call.
            # Playwright's `timeout=15_000` is normally enough, but iter_003
            # observed a single screenshot blocking for ~15 minutes after the
            # iframe quietly died — Playwright's deadline tracking went
            # negative ("Timeout -873596ms exceeded") and the RPC never
            # returned in a timely fashion. asyncio.wait_for guarantees we
            # bail in 20 s no matter what the Playwright/patchright side does,
            # so the existing iframe-dead recovery path can take over.
            screenshot_bytes: bytes = await asyncio.wait_for(
                iframe_locator.screenshot(timeout=15_000),
                timeout=20.0,
            )
        except asyncio.TimeoutError:
            _iframe_verified = False
            await _log_iframe_missing_diagnostic(page)
            # Re-raise with an iframe-flavoured message so callers'
            # _is_iframe_dead_error classifier matches and re-navigates,
            # rather than treating it as a generic transient failure.
            raise RuntimeError(
                "Locator.screenshot: hard timeout exceeded — iframe likely dead "
                "(asyncio.wait_for fired after Playwright RPC stalled)"
            )
        except Exception:
            # Screenshot raised (usually iframe visibility lost mid-flight).
            # Clear the cached-visible flag so the next call re-verifies, and
            # log diagnostic state so we can see *why* the iframe went away.
            _iframe_verified = False
            await _log_iframe_missing_diagnostic(page)
            raise

        if is_non_blank(screenshot_bytes):
            logger.debug(
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
