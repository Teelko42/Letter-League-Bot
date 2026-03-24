from __future__ import annotations

from io import BytesIO

import pytest
from PIL import Image, ImageDraw

from src.vision.errors import INVALID_SCREENSHOT, VisNError
from src.vision.preprocessor import MAX_VISION_EDGE, preprocess_screenshot


# RGB color that maps to HSV [18, 58, 220] — falls within the board detection range.
# Verified: cv2.cvtColor([[[170, 200, 220]]], BGR2HSV) = [18, 58, 220] which is inside
# BOARD_HSV_LOWER=[15,20,160] and BOARD_HSV_UPPER=[35,80,240].
BOARD_COLOR = (220, 200, 170)


def _make_test_image(
    width: int,
    height: int,
    bg_color: tuple[int, int, int] = (0, 0, 0),
    rect: tuple[int, int, int, int] | None = None,
    rect_color: tuple[int, int, int] = BOARD_COLOR,
) -> bytes:
    """Create a test image with an optional colored rectangle.

    Args:
        width: Image width in pixels.
        height: Image height in pixels.
        bg_color: Background RGB color tuple.
        rect: Optional (x0, y0, x1, y1) bounding box for the colored rectangle.
        rect_color: RGB color of the rectangle.

    Returns:
        PNG-encoded image bytes.
    """
    img = Image.new("RGB", (width, height), bg_color)
    if rect is not None:
        draw = ImageDraw.Draw(img)
        draw.rectangle(rect, fill=rect_color)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_preprocess_returns_png_bytes() -> None:
    """Preprocessor returns bytes starting with PNG magic bytes."""
    # 800x600 image with a large board-colored rectangle
    img_bytes = _make_test_image(800, 600, rect=(50, 50, 750, 550))
    result = preprocess_screenshot(img_bytes)
    assert isinstance(result, bytes)
    assert result[:4] == b"\x89PNG", "Output must be valid PNG (wrong magic bytes)"


def test_preprocess_upscales_output() -> None:
    """Preprocessor upscales the detected crop region by at least 1x."""
    # 400x300 image with board color filling most of it
    img_bytes = _make_test_image(400, 300, rect=(10, 10, 390, 290))
    result = preprocess_screenshot(img_bytes)

    # The output image should be larger than the original image in at least one dimension
    out_img = Image.open(BytesIO(result))
    out_w, out_h = out_img.size
    # The detected region is ~380x280; after 2x upscale it should be ~760x560
    assert out_w > 400 or out_h > 300, (
        f"Output ({out_w}x{out_h}) should be larger than input (400x300) after 2x upscale"
    )


def test_preprocess_clamps_to_max_edge() -> None:
    """Output image's longest edge does not exceed MAX_VISION_EDGE (1568px)."""
    # Large image: board region is 1200x1000 — after 2x upscale = 2400x2000 (exceeds 1568)
    img_bytes = _make_test_image(1400, 1200, rect=(100, 100, 1300, 1100))
    result = preprocess_screenshot(img_bytes)

    out_img = Image.open(BytesIO(result))
    out_w, out_h = out_img.size
    assert max(out_w, out_h) <= MAX_VISION_EDGE, (
        f"Output longest edge ({max(out_w, out_h)}px) exceeds MAX_VISION_EDGE ({MAX_VISION_EDGE}px)"
    )


def test_preprocess_raises_on_no_board() -> None:
    """Preprocessor raises VisNError(INVALID_SCREENSHOT) on a solid black image."""
    img_bytes = _make_test_image(800, 600, bg_color=(0, 0, 0))
    with pytest.raises(VisNError) as exc_info:
        preprocess_screenshot(img_bytes)
    assert exc_info.value.code == INVALID_SCREENSHOT


def test_preprocess_raises_on_tiny_region() -> None:
    """Preprocessor raises VisNError(INVALID_SCREENSHOT) for a tiny board-colored area."""
    # 50x50 rectangle = 2500px area, well below MIN_BOARD_AREA (10000)
    img_bytes = _make_test_image(800, 600, bg_color=(0, 0, 0), rect=(375, 275, 425, 325))
    with pytest.raises(VisNError) as exc_info:
        preprocess_screenshot(img_bytes)
    assert exc_info.value.code == INVALID_SCREENSHOT
