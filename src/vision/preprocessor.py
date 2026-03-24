from __future__ import annotations

from io import BytesIO

import cv2
import numpy as np
from PIL import Image

from src.vision.errors import INVALID_SCREENSHOT, VisNError

# Minimum contour area (in pixels) for a detected region to be considered a board.
# Regions smaller than this are rejected as noise or irrelevant UI elements.
MIN_BOARD_AREA = 10_000

# Maximum dimension (px) Claude Vision accepts without auto-downsampling.
# Source: https://platform.claude.com/docs/en/build-with-claude/vision
MAX_VISION_EDGE = 1568

# Upscale factor applied after cropping to improve letter readability.
UPSCALE_FACTOR = 2

# HSV range for Letter League board background — needs empirical calibration
# against real screenshots. These are initial estimates.
# The board appears to have a beige/cream/tan background color.
BOARD_HSV_LOWER = np.array([15, 20, 160])
BOARD_HSV_UPPER = np.array([35, 80, 240])


def preprocess_screenshot(img_bytes: bytes) -> bytes:
    """Detect the board region, crop to it, upscale 2x, and return PNG bytes.

    Steps:
    1. Decode bytes to a BGR numpy array via OpenCV.
    2. Convert to HSV and apply a color mask to isolate the board background.
    3. Find contours; select the largest by area.
    4. Raise VisNError(INVALID_SCREENSHOT) if no contour found or area < MIN_BOARD_AREA.
    5. Crop the original image (via Pillow) to the bounding rect of the largest contour.
    6. Upscale the crop by UPSCALE_FACTOR using LANCZOS resampling.
    7. Clamp to MAX_VISION_EDGE on the long edge (proportional downscale if needed).
    8. Encode to PNG and return bytes.

    Args:
        img_bytes: Raw image bytes (PNG, JPEG, or any format supported by OpenCV/Pillow).

    Returns:
        PNG-encoded bytes of the preprocessed board region.

    Raises:
        VisNError: With code INVALID_SCREENSHOT if no board region is detected or the
            detected region is too small to be a valid board.
    """
    # Step 1: Decode to BGR numpy array
    nparr = np.frombuffer(img_bytes, np.uint8)
    bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if bgr is None:
        raise VisNError(
            INVALID_SCREENSHOT,
            "Failed to decode image — file may be corrupt or an unsupported format.",
        )

    # Step 2: HSV conversion and color mask
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, BOARD_HSV_LOWER, BOARD_HSV_UPPER)

    # Step 3: Find contours on the binary mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 4: Validate contour presence and minimum area
    if not contours:
        raise VisNError(
            INVALID_SCREENSHOT,
            "Board region not detected — no matching color region found. "
            "This may not be a Letter League screenshot.",
        )

    largest = max(contours, key=cv2.contourArea)

    if cv2.contourArea(largest) < MIN_BOARD_AREA:
        raise VisNError(
            INVALID_SCREENSHOT,
            f"Board region too small (area={cv2.contourArea(largest):.0f}px, "
            f"minimum={MIN_BOARD_AREA}px) — this may not be a Letter League screenshot.",
        )

    # Step 5: Crop to bounding rect using Pillow
    x, y, w, h = cv2.boundingRect(largest)
    pil_img = Image.open(BytesIO(img_bytes))
    cropped = pil_img.crop((x, y, x + w, y + h))

    # Step 6: 2x upscale with LANCZOS for quality letter readability
    new_w = cropped.width * UPSCALE_FACTOR
    new_h = cropped.height * UPSCALE_FACTOR

    # Step 7: Clamp to MAX_VISION_EDGE on the long edge
    if max(new_w, new_h) > MAX_VISION_EDGE:
        ratio = MAX_VISION_EDGE / max(new_w, new_h)
        new_w = int(new_w * ratio)
        new_h = int(new_h * ratio)

    upscaled = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Step 8: Encode as PNG and return bytes
    buf = BytesIO()
    upscaled.save(buf, format="PNG")
    return buf.getvalue()
