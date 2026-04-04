from __future__ import annotations

from io import BytesIO

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from src.vision.errors import INVALID_SCREENSHOT, VisNError

# Minimum contour area (in pixels) for a detected region to be considered a board.
# Regions smaller than this are rejected as noise or irrelevant UI elements.
MIN_BOARD_AREA = 10_000

# Maximum dimension (px) Claude Vision accepts without auto-downsampling.
# Source: https://platform.claude.com/docs/en/build-with-claude/vision
MAX_VISION_EDGE = 1568

# Upscale factor applied after cropping to improve letter readability.
UPSCALE_FACTOR = 2

# Extra vertical padding below the detected board region, as a fraction of the
# board height.  The player's tile rack sits just below the board on a different
# background colour and would otherwise be cropped out.
RACK_PADDING_RATIO = 0.18

# HSV range for Letter League board background — calibrated against real screenshots.
# Board background is a consistent peach color: HSV ~(16, 57, 255), RGB ~(255, 229, 198).
BOARD_HSV_LOWER = np.array([10, 30, 200])
BOARD_HSV_UPPER = np.array([25, 80, 255])

BOARD_ROWS = 19
BOARD_COLS = 27


def _add_reference_markers(
    board_img: Image.Image,
    board_w: int,
    board_h: int,
) -> Image.Image:
    """Draw small coordinate labels at known landmark positions on the board.

    Places labels at the center star (9,13) and the four Triple Word squares
    (3,7), (3,19), (15,7), (15,19). These landmarks let the Vision API
    calibrate its position counting without requiring every cell to be
    individually labeled.

    Args:
        board_img: Cropped board image (may include rack padding below).
        board_w:   Width of the board region (pixels, excluding rack area).
        board_h:   Height of the board region (pixels, excluding rack area).

    Returns:
        The image with reference markers drawn (mutates in-place via draw).
    """
    draw = ImageDraw.Draw(board_img)

    try:
        font = ImageFont.truetype("arial.ttf", 10)
    except (OSError, IOError):
        font = ImageFont.load_default()

    cell_w = board_w / BOARD_COLS
    cell_h = board_h / BOARD_ROWS

    # Landmarks: (row, col, label_text, color)
    landmarks = [
        (9, 13, "9,13", (0, 180, 0)),       # center — green
        (3, 7, "3,7", (200, 0, 0)),          # TW — red
        (3, 19, "3,19", (200, 0, 0)),
        (15, 7, "15,7", (200, 0, 0)),
        (15, 19, "15,19", (200, 0, 0)),
    ]

    for row, col, label, color in landmarks:
        cx = int((col + 0.5) * cell_w)
        cy = int((row + 0.5) * cell_h)
        # Dot and coordinate label
        r = 5
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
        draw.text((cx + r + 2, cy - 6), label, fill=color, font=font)

    return board_img


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

    # Step 2b: Morphological closing to merge fragmented board regions.
    # The board background is peach but multiplier squares (blue, green, yellow)
    # create gaps in the mask. Closing bridges these gaps into one large region.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 50))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

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

    # Step 5: Crop to bounding rect + rack padding using Pillow
    x, y, w, h = cv2.boundingRect(largest)
    img_h, img_w = bgr.shape[:2]

    # Step 5a: Refine crop to match expected board aspect ratio.
    # Letter League's 27×19 grid has approximately square cells, giving an
    # expected aspect ratio of ~1.42.  The HSV contour often includes
    # sidebar/UI slivers, making the bounding rect too wide.  Trim the
    # excess width (or height) and centre the result.
    expected_ratio = BOARD_COLS / BOARD_ROWS          # 27/19 ≈ 1.4211
    detected_ratio = w / h if h > 0 else expected_ratio

    if detected_ratio > expected_ratio * 1.03:        # wider than expected
        new_w = int(h * expected_ratio)
        trim = w - new_w
        x += trim // 2
        w = new_w
    elif detected_ratio < expected_ratio * 0.97:      # taller than expected
        new_h = int(w / expected_ratio)
        trim = h - new_h
        y += trim // 2
        h = new_h

    # Extend the crop downward to include the tile rack below the board.
    rack_pad = int(h * RACK_PADDING_RATIO)
    crop_bottom = min(y + h + rack_pad, img_h)

    pil_img = Image.open(BytesIO(img_bytes))
    cropped = pil_img.crop((x, y, x + w, crop_bottom))

    # Step 5b: Draw reference markers at known landmark positions
    cropped = _add_reference_markers(cropped, w, h)

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
