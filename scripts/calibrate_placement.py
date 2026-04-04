"""Calibration script for measuring tile_placer.py fractional constants.

Usage
-----
Run with a PNG screenshot captured from a live Letter League game::

    python scripts/calibrate_placement.py path/to/screenshot.png

The script opens the image in an OpenCV window and prompts you to click
8 reference points in sequence. After all 8 clicks the fractional constants
are computed and printed as a ready-to-paste Python block for tile_placer.py.

The board is 19 rows x 27 columns.  To avoid tiny-cell mis-clicks, cell
width and height are measured across 10-cell spans and divided.

Reference points (click in this order)
---------------------------------------
1. TOP-LEFT corner of board cell (0,0)   — top-left of the grid
2. TOP-LEFT corner of board cell (0,10)  — 10 cells to the right
3. TOP-LEFT corner of board cell (10,0)  — 10 cells below (0,0)
4. TOP-LEFT corner of board cell (0,26)  — rightmost column (for verification)
5. TOP-LEFT corner of board cell (18,0)  — bottom row (for verification)
6. CENTER of the first rack tile (slot 0, leftmost)
7. CENTER of the second rack tile (slot 1)
8. CENTER of the confirm button
"""

from __future__ import annotations

import sys

REQUIRED_CLICKS = 8

# Number of cells between click 1→2 (width) and click 1→3 (height).
CELL_SPAN_W = 10
CELL_SPAN_H = 10

PROMPTS = [
    "Click 1/8 — TOP-LEFT corner of board cell (0,0)   [top-left of grid]",
    "Click 2/8 — TOP-LEFT corner of board cell (0,10)   [10 cells RIGHT of (0,0)]",
    "Click 3/8 — TOP-LEFT corner of board cell (10,0)   [10 cells BELOW (0,0)]",
    "Click 4/8 — TOP-LEFT corner of board cell (0,26)   [rightmost column, for verification]",
    "Click 5/8 — TOP-LEFT corner of board cell (18,0)   [bottom row, for verification]",
    "Click 6/8 — CENTER of first rack tile (slot 0, leftmost)",
    "Click 7/8 — CENTER of second rack tile (slot 1)",
    "Click 8/8 — CENTER of confirm button",
]


def _compute_constants(clicks: list[tuple[int, int]], img_w: int, img_h: int) -> dict[str, float]:
    """Compute fractional constants from recorded click coordinates.

    Cell width is measured across a 10-cell span (clicks 1→2) for precision.
    Cell height is measured across a 10-cell span (clicks 1→3).
    Clicks 4 and 5 (rightmost column, bottom row) are used for verification.

    Args:
        clicks: List of (x, y) tuples in the order described in PROMPTS.
        img_w: Image width in pixels.
        img_h: Image height in pixels.

    Returns:
        Dict mapping constant name to fractional value.
    """
    (x0, y0) = clicks[0]   # cell (0,0)
    (x1, _) = clicks[1]    # cell (0,10)
    (_, y2) = clicks[2]    # cell (10,0)
    (x3, _) = clicks[3]    # cell (0,26)  — verification
    (_, y4) = clicks[4]    # cell (18,0)  — verification
    (x5, y5) = clicks[5]   # rack slot 0
    (x6, _) = clicks[6]    # rack slot 1
    (x7, y7) = clicks[7]   # confirm button

    cell_w = (x1 - x0) / CELL_SPAN_W
    cell_h = (y2 - y0) / CELL_SPAN_H

    # Verification: compare measured cell size with the full-span measurement.
    cell_w_verify = (x3 - x0) / 26  # 26 intervals for 27 columns
    cell_h_verify = (y4 - y0) / 18  # 18 intervals for 19 rows

    print(f"\n  Cell width  — 10-span: {cell_w:.1f}px, full-span: {cell_w_verify:.1f}px "
          f"(delta: {abs(cell_w - cell_w_verify):.1f}px)")
    print(f"  Cell height — 10-span: {cell_h:.1f}px, full-span: {cell_h_verify:.1f}px "
          f"(delta: {abs(cell_h - cell_h_verify):.1f}px)")

    if abs(cell_w - cell_w_verify) > 3:
        print("  ⚠ WARNING: cell width measurements disagree by >3px — recheck clicks!")
    if abs(cell_h - cell_h_verify) > 3:
        print("  ⚠ WARNING: cell height measurements disagree by >3px — recheck clicks!")

    return {
        "GRID_X0_FRAC": x0 / img_w,
        "GRID_Y0_FRAC": y0 / img_h,
        "CELL_W_FRAC": cell_w / img_w,
        "CELL_H_FRAC": cell_h / img_h,
        "RACK_X0_FRAC": x5 / img_w,
        "RACK_Y_FRAC": y5 / img_h,
        "RACK_TILE_STEP_FRAC": (x6 - x5) / img_w,
        "CONFIRM_X_FRAC": x7 / img_w,
        "CONFIRM_Y_FRAC": y7 / img_h,
    }


def _print_constants(constants: dict[str, float]) -> None:
    """Print computed constants as a ready-to-paste Python block."""
    print()
    print("=" * 60)
    print("Paste these constants into src/browser/tile_placer.py:")
    print("=" * 60)
    for name, value in constants.items():
        print(f"{name:<26} = {value:.6f}")
    print("=" * 60)


def main(image_path: str) -> None:
    """Run the interactive calibration session.

    Args:
        image_path: Path to the PNG screenshot to calibrate from.
    """
    try:
        import cv2
    except ImportError:
        print("Error: opencv-python is not installed. Run: pip install opencv-python")
        sys.exit(1)

    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image from '{image_path}'.")
        print("Make sure the path is correct and the file is a valid image.")
        sys.exit(1)

    img_h, img_w = img.shape[:2]
    print(f"Loaded image: {img_w}x{img_h} pixels")
    print()
    print("Instructions:")
    print("  - A window will open showing the screenshot.")
    print("  - Click the reference points in the order shown below.")
    print("  - Press 'q' to quit without saving.")
    print()
    print(PROMPTS[0])

    clicks: list[tuple[int, int]] = []
    window_name = "Tile Placement Calibration"

    def on_mouse(event: int, x: int, y: int, flags: int, param: object) -> None:
        import cv2 as _cv2  # local import to satisfy mypy in callback scope

        if event != _cv2.EVENT_LBUTTONDOWN:
            return

        idx = len(clicks)
        clicks.append((x, y))
        print(f"  => Recorded click {idx + 1}: ({x}, {y})")

        # Draw marker on the display image.
        display_img: cv2.typing.MatLike = param  # type: ignore[assignment]
        _cv2.circle(display_img, (x, y), 5, (0, 255, 0), -1)
        _cv2.putText(
            display_img,
            str(idx + 1),
            (x + 8, y - 8),
            _cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )
        _cv2.imshow(window_name, display_img)

        if len(clicks) < REQUIRED_CLICKS:
            print(PROMPTS[len(clicks)])
        else:
            print()
            print("All 6 points recorded — computing constants...")

    # Work on a display copy so markers don't overwrite the source image data.
    display = img.copy()

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, min(img_w, 1280), min(img_h, 800))
    cv2.setMouseCallback(window_name, on_mouse, display)
    cv2.imshow(window_name, display)

    while True:
        key = cv2.waitKey(50) & 0xFF
        if key == ord("q"):
            print("Quit — no constants computed.")
            break
        if len(clicks) >= REQUIRED_CLICKS:
            constants = _compute_constants(clicks, img_w, img_h)
            _print_constants(constants)
            print("Press any key or close the window to exit.")
            cv2.waitKey(0)
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/calibrate_placement.py <screenshot.png>")
        print()
        print(__doc__)
        sys.exit(0)

    main(sys.argv[1])
