from __future__ import annotations

from io import BytesIO

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from loguru import logger
from src.vision.errors import INVALID_SCREENSHOT, VisNError

# Maximum dimension (px) Claude Vision accepts without auto-downsampling.
MAX_VISION_EDGE = 1568

# Upscale factor applied after cropping to improve letter readability.
UPSCALE_FACTOR = 2

# Extra vertical padding below the board grid, as a fraction of the grid height.
# The player's tile rack sits just below the board.
RACK_PADDING_RATIO = 0.18

BOARD_ROWS = 19
BOARD_COLS = 27

# ---------------------------------------------------------------------------
# Grid position fractions — sourced from CoordMapper calibration.
# These define the board grid position as fractions of the game canvas
# (activity iframe), calibrated at 1057×768.  They are resolution-independent.
# ---------------------------------------------------------------------------
GRID_X0_FRAC = 0.056820   # left edge of cell (0,0) as fraction of canvas width
GRID_Y0_FRAC = 0.070587   # top edge of cell (0,0) as fraction of canvas height
CELL_W_FRAC = 0.032756    # width of one cell as fraction of canvas width
CELL_H_FRAC = 0.045038    # height of one cell as fraction of canvas height

# HSV range for peach board background — used only for validation, not positioning.
BOARD_HSV_LOWER = np.array([10, 30, 200])
BOARD_HSV_UPPER = np.array([25, 68, 255])
MIN_BOARD_PEACH_RATIO = 0.05  # at least 5% of grid area must be peach


def _add_reference_markers(
    board_img: Image.Image,
    board_w: int,
    board_h: int,
) -> Image.Image:
    """Draw column numbers along the top and row numbers along the left side.

    Overlays every column number (0-26) above each column and every row
    number (0-18) to the left of each row.  Also draws a bright green
    marker at the center star (9,13).

    Args:
        board_img: Cropped board image (may include rack padding below).
        board_w:   Width of the board region (pixels, excluding rack area).
        board_h:   Height of the board region (pixels, excluding rack area).

    Returns:
        The image with coordinate labels drawn (mutates in-place via draw).
    """
    draw = ImageDraw.Draw(board_img)

    cell_w = board_w / BOARD_COLS
    cell_h = board_h / BOARD_ROWS
    font_size = max(8, int(min(cell_w, cell_h) * 0.55))

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except (OSError, IOError):
        font = ImageFont.load_default()

    label_color = (255, 0, 0)       # red for labels
    outline_color = (255, 255, 255) # white outline for readability

    # Column numbers along the top — every column
    for col in range(BOARD_COLS):
        cx = int((col + 0.5) * cell_w)
        label = str(col)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            draw.text((cx - font_size // 2 + dx, 1 + dy), label,
                      fill=outline_color, font=font)
        draw.text((cx - font_size // 2, 1), label, fill=label_color, font=font)

    # Row numbers along the left side — every row
    for row in range(BOARD_ROWS):
        cy = int((row + 0.5) * cell_h)
        label = str(row)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            draw.text((1 + dx, cy - font_size // 2 + dy), label,
                      fill=outline_color, font=font)
        draw.text((1, cy - font_size // 2), label, fill=label_color, font=font)

    # Thin gridlines at cell boundaries — helps Vision API align tiles to cells
    grid_color = (200, 0, 0)  # faint red, visible but not overpowering
    for col in range(BOARD_COLS + 1):
        x = int(col * cell_w)
        draw.line([(x, 0), (x, board_h)], fill=grid_color, width=1)
    for row in range(BOARD_ROWS + 1):
        y = int(row * cell_h)
        draw.line([(0, y), (board_w, y)], fill=grid_color, width=1)

    # Green crosshair at center star (9,13)
    cx = int((13 + 0.5) * cell_w)
    cy = int((9 + 0.5) * cell_h)
    r = 6
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(0, 220, 0))
    draw.line((cx - r - 3, cy, cx + r + 3, cy), fill=(0, 220, 0), width=2)
    draw.line((cx, cy - r - 3, cx, cy + r + 3), fill=(0, 220, 0), width=2)

    return board_img


def preprocess_screenshot(img_bytes: bytes) -> bytes:
    """Crop the board grid using known position fractions, upscale, and return PNG.

    Uses calibrated grid fractions (from CoordMapper) to locate the board
    precisely within the game canvas screenshot.  This avoids HSV-based
    detection which is prone to including non-board UI elements.

    Steps:
    1. Decode bytes and compute grid pixel coordinates from known fractions.
    2. Validate that the grid region contains peach board background.
    3. Crop to the grid region + rack padding below.
    4. Draw coordinate reference markers at exact cell positions.
    5. Upscale 2x with LANCZOS resampling.
    6. Clamp to MAX_VISION_EDGE on the long edge.
    7. Encode to PNG and return bytes.

    Args:
        img_bytes: Raw image bytes (PNG, JPEG, or any OpenCV/Pillow format).

    Returns:
        PNG-encoded bytes of the preprocessed board region.

    Raises:
        VisNError: With code INVALID_SCREENSHOT if the image can't be decoded
            or doesn't contain a recognisable board.
    """
    # Step 1: Decode and compute grid position
    nparr = np.frombuffer(img_bytes, np.uint8)
    bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if bgr is None:
        raise VisNError(
            INVALID_SCREENSHOT,
            "Failed to decode image — file may be corrupt or an unsupported format.",
        )

    img_h, img_w = bgr.shape[:2]

    # Calculate the board grid pixel coordinates from known fractions.
    # These fractions are resolution-independent — they work at any canvas size.
    grid_x = int(GRID_X0_FRAC * img_w)
    grid_y = int(GRID_Y0_FRAC * img_h)
    grid_w = int(BOARD_COLS * CELL_W_FRAC * img_w)
    grid_h = int(BOARD_ROWS * CELL_H_FRAC * img_h)

    # Clamp to image bounds
    grid_x = max(0, grid_x)
    grid_y = max(0, grid_y)
    grid_w = min(grid_w, img_w - grid_x)
    grid_h = min(grid_h, img_h - grid_y)

    logger.debug(
        "Grid crop: ({},{}) {}×{} from {}×{} canvas",
        grid_x, grid_y, grid_w, grid_h, img_w, img_h,
    )

    # Step 2: Validate — check that the grid area has enough peach background
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    grid_roi = hsv[grid_y:grid_y + grid_h, grid_x:grid_x + grid_w]
    peach_mask = cv2.inRange(grid_roi, BOARD_HSV_LOWER, BOARD_HSV_UPPER)
    peach_ratio = float(peach_mask.sum() / 255) / (grid_w * grid_h) if grid_w * grid_h > 0 else 0

    if peach_ratio < MIN_BOARD_PEACH_RATIO:
        raise VisNError(
            INVALID_SCREENSHOT,
            f"Board region not detected — peach ratio {peach_ratio:.1%} is below "
            f"threshold {MIN_BOARD_PEACH_RATIO:.0%}. This may not be a game screenshot.",
        )

    # Step 3: Crop to grid region + rack padding
    rack_pad = int(grid_h * RACK_PADDING_RATIO)
    crop_bottom = min(grid_y + grid_h + rack_pad, img_h)

    pil_img = Image.open(BytesIO(img_bytes))
    cropped = pil_img.crop((grid_x, grid_y, grid_x + grid_w, crop_bottom))

    # Step 4: Draw reference markers at exact cell positions
    cropped = _add_reference_markers(cropped, grid_w, grid_h)

    # Step 5: 2x upscale with LANCZOS
    new_w = cropped.width * UPSCALE_FACTOR
    new_h = cropped.height * UPSCALE_FACTOR

    # Step 6: Clamp to MAX_VISION_EDGE on the long edge
    if max(new_w, new_h) > MAX_VISION_EDGE:
        ratio = MAX_VISION_EDGE / max(new_w, new_h)
        new_w = int(new_w * ratio)
        new_h = int(new_h * ratio)

    upscaled = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Debug: save preprocessed image for diagnostic inspection
    try:
        from pathlib import Path
        debug_path = Path("debug/preprocessed_debug.png")
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        upscaled.save(debug_path, format="PNG")
        logger.debug("Preprocessed debug image saved → {}", debug_path)
    except Exception:
        pass

    # Step 7: Encode as PNG and return bytes
    buf = BytesIO()
    upscaled.save(buf, format="PNG")
    return buf.getvalue()
