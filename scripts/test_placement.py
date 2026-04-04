"""Phase 7 verification: live tile placement test.

Launches a headed browser, navigates to Letter League, captures the game state,
finds a move, and places tiles. Run with:

    $env:PYTHONPATH = "."
    & "C:\\Users\\Ninja\\AppData\\Local\\Programs\\Python\\Python310\\python.exe" scripts/test_placement.py

Pass --dry-run to skip actual tile placement and just verify calibration.
"""
from __future__ import annotations

import asyncio
import os
import sys

import cv2
import numpy as np
from dotenv import load_dotenv
from loguru import logger

from src.browser.capture import capture_canvas
from src.browser.navigator import navigate_to_activity
from src.browser.tile_placer import (
    CoordMapper,
    GRID_X0_FRAC,
    GRID_Y0_FRAC,
    CELL_W_FRAC,
    CELL_H_FRAC,
)
from src.browser.turn_detector import classify_frame


async def launch_headed(profile_dir: str = "./browser_data"):
    """Launch a headed patchright browser with existing session."""
    from patchright.async_api import async_playwright

    pw = await async_playwright().start()
    context = await pw.chromium.launch_persistent_context(
        user_data_dir=profile_dir,
        headless=False,
        viewport={"width": 1920, "height": 1080},
    )
    page = context.pages[0] if context.pages else await context.new_page()
    return pw, context, page


async def verify_calibration(page) -> dict | None:
    """Capture screenshot, detect the board grid, overlay it, save to debug/.

    Uses blue (DL) multiplier square detection to fit the 19x27 grid precisely,
    independent of iframe resolution or aspect ratio.  Falls back to the
    tile_placer fractional constants when detection fails.
    """
    from collections import defaultdict
    from src.vision.schema import OFFICIAL_MULTIPLIER_LAYOUT

    BOARD_ROWS = 19
    BOARD_COLS = 27

    logger.info("Capturing canvas screenshot...")
    img_bytes = await capture_canvas(page)

    # Decode
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    h, w = img.shape[:2]
    logger.info("Canvas screenshot: {}x{}", w, h)

    # Classify turn state
    state = classify_frame(img_bytes)
    logger.info("Turn state: {}", state)

    # Get game element bounding box (canvas or iframe fallback)
    bbox = None
    try:
        bbox = await (
            page.frame_locator('iframe[src*="discordsays.com"]')
            .locator("canvas")
            .first
            .bounding_box(timeout=5_000)
        )
        if bbox:
            logger.info("Canvas bbox: x={x:.0f} y={y:.0f} w={width:.0f} h={height:.0f}", **bbox)
    except Exception:
        pass

    if bbox is None:
        logger.info("No canvas element — using iframe bbox")
        try:
            bbox = await page.locator('iframe[src*="discordsays.com"]').bounding_box(timeout=10_000)
            if bbox:
                logger.info("Iframe bbox: x={x:.0f} y={y:.0f} w={width:.0f} h={height:.0f}", **bbox)
        except Exception as e:
            logger.warning("Iframe bbox also failed: {}", e)

    # ------------------------------------------------------------------
    # Detect grid from blue (DL) multiplier squares
    # ------------------------------------------------------------------
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    blue_mask = cv2.inRange(hsv, np.array([85, 40, 150]), np.array([130, 200, 255]))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    blue_centers = []
    for c in contours:
        bx, by, bw, bh = cv2.boundingRect(c)
        if 200 < cv2.contourArea(c) < 2000:
            blue_centers.append((bx + bw // 2, by + bh // 2))
    blue_centers.sort(key=lambda p: p[1])

    # Group by Y into rows (15px tolerance)
    rows_dict: dict[int, list[int]] = defaultdict(list)
    for cx, cy in blue_centers:
        placed = False
        for key in sorted(rows_dict.keys()):
            if abs(cy - key) < 15:
                rows_dict[key].append(cx)
                placed = True
                break
        if not placed:
            rows_dict[cy].append(cx)

    # Row 0 DL columns: [3, 6, 8, 11, 15, 18, 20, 23]
    known_row0_cols = [3, 6, 8, 11, 15, 18, 20, 23]
    cell_w = cell_h = x_off = y_off = None

    for ykey, xs in sorted(rows_dict.items()):
        if len(xs) == len(known_row0_cols):
            xs_sorted = np.array(sorted(xs), dtype=float)
            cols_arr = np.array(known_row0_cols, dtype=float)
            A = np.vstack([cols_arr, np.ones(len(cols_arr))]).T
            cw, xo = np.linalg.lstsq(A, xs_sorted, rcond=None)[0]
            resid = xs_sorted - (cw * cols_arr + xo)
            if max(abs(resid)) < 5:
                cell_w = cw
                x_off = xo
                logger.info("Horizontal fit: cell_w={:.2f}px x_off={:.1f}px resid<{:.1f}px", cw, xo, max(abs(resid)))
                break

    if cell_w is not None:
        # Match Y-rows to board rows via DL column patterns
        dl_by_row: dict[int, list[int]] = defaultdict(list)
        for (r, cc), m in OFFICIAL_MULTIPLIER_LAYOUT.items():
            if m == "DL":
                dl_by_row[r].append(cc)

        row_matches: list[tuple[int, float]] = []
        for yk, x_list in sorted(rows_dict.items()):
            x_list_sorted = sorted(x_list)
            for board_row, dl_cols in dl_by_row.items():
                if len(x_list_sorted) == len(dl_cols):
                    expected = [cell_w * c + x_off for c in sorted(dl_cols)]
                    if max(abs(a - b) for a, b in zip(x_list_sorted, expected)) < 10:
                        row_matches.append((board_row, yk))
                        break

        # Disambiguate symmetric rows: assign in ascending Y order
        row_matches.sort(key=lambda m: m[1])
        used_rows: set[int] = set()
        clean_matches: list[tuple[int, float]] = []
        for br, yk in row_matches:
            # Board is vertically symmetric; pick the row not yet used
            mirror = 18 - br
            if br not in used_rows:
                clean_matches.append((br, yk))
                used_rows.add(br)
            elif mirror not in used_rows:
                clean_matches.append((mirror, yk))
                used_rows.add(mirror)

        if len(clean_matches) >= 4:
            rows_arr = np.array([m[0] for m in clean_matches], dtype=float)
            ys_arr = np.array([m[1] for m in clean_matches], dtype=float)
            A = np.vstack([rows_arr, np.ones(len(rows_arr))]).T
            ch, yo = np.linalg.lstsq(A, ys_arr, rcond=None)[0]
            cell_h = ch
            y_off = yo
            resid = ys_arr - (ch * rows_arr + yo)
            logger.info("Vertical fit: cell_h={:.2f}px y_off={:.1f}px resid<{:.1f}px ({} rows)", ch, yo, max(abs(resid)), len(clean_matches))

    # Fallback to tile_placer constants if detection failed
    if cell_w is None or cell_h is None:
        logger.warning("Grid detection failed — falling back to tile_placer constants")
        cell_w = CELL_W_FRAC * w
        cell_h = CELL_H_FRAC * h
        x_off = GRID_X0_FRAC * w
        y_off = GRID_Y0_FRAC * h

    # ------------------------------------------------------------------
    # Draw overlay
    # ------------------------------------------------------------------
    origin_x = x_off - 0.5 * cell_w
    origin_y = y_off - 0.5 * cell_h

    overlay = img.copy()
    GREEN = (0, 255, 0)
    RED = (0, 0, 255)

    for r in range(BOARD_ROWS + 1):
        y = int(origin_y + r * cell_h)
        cv2.line(overlay, (int(origin_x), y), (int(origin_x + BOARD_COLS * cell_w), y), GREEN, 1)
    for c in range(BOARD_COLS + 1):
        x = int(origin_x + c * cell_w)
        cv2.line(overlay, (x, int(origin_y)), (x, int(origin_y + BOARD_ROWS * cell_h)), GREEN, 1)

    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            cx = int(x_off + c * cell_w)
            cy = int(y_off + r * cell_h)
            cv2.circle(overlay, (cx, cy), 2, RED, -1)

    cv2.imwrite("debug/live_calibration_overlay.png", overlay)
    cv2.imwrite("debug/live_screenshot.png", img)
    logger.info("Saved debug/live_calibration_overlay.png and debug/live_screenshot.png")

    return bbox


async def test_placement(page, dry_run: bool = False):
    """Full placement test: vision -> engine -> place tiles."""
    from src.vision import extract_board_state
    from src.browser.tile_placer import TilePlacer

    # Step 1: Capture and verify state
    img_bytes = await capture_canvas(page)
    state = classify_frame(img_bytes)

    if state != "my_turn":
        logger.warning("Not your turn (state='{}') — cannot test placement", state)
        return False

    if dry_run:
        logger.info("[DRY RUN] Skipping vision, move generation, and placement")
        return True

    # Step 2: Extract board state via vision
    logger.info("Running vision pipeline...")
    board, rack = await extract_board_state(img_bytes)
    logger.info("Board: {}x{}, Rack: {}", board.rows, board.cols, rack)

    # Step 3: Find moves
    from pathlib import Path
    from src.engine.gaddag import GADDAG
    from src.engine.moves import find_all_moves

    logger.info("Loading dictionary...")
    gaddag = GADDAG.from_wordlist(Path("data/wordlist.txt"), cache_path=Path("cache/gaddag.pkl"))

    logger.info("Finding moves...")
    moves = find_all_moves(board, rack, gaddag)
    if not moves:
        logger.warning("No valid moves found!")
        return False

    moves.sort(key=lambda m: m.score, reverse=True)
    logger.info("Found {} moves. Top 3:", len(moves))
    for m in moves[:3]:
        logger.info("  {} ({},{}) {} — {} pts", m.word, m.start_row, m.start_col, m.direction, m.score)

    # Step 4: Place the top move
    placer = TilePlacer(page)
    logger.info("Placing top move: '{}' for {} points", moves[0].word, moves[0].score)
    accepted = await placer.place_move(moves[:3], rack)
    logger.info("Result: accepted={}", accepted)
    return accepted


async def main():
    load_dotenv()
    channel_url = os.getenv("DISCORD_CHANNEL_URL")
    if not channel_url:
        logger.error("DISCORD_CHANNEL_URL not set in .env")
        sys.exit(1)

    dry_run = "--dry-run" in sys.argv

    pw, context, page = await launch_headed()
    try:
        # Navigate to game
        logger.info("Navigating to Letter League...")
        try:
            await navigate_to_activity(page, channel_url)
        except Exception as nav_exc:
            logger.warning("Auto-navigation failed: {}. Checking for existing iframe...", nav_exc)
            # Check if iframe is already present
            import re
            found = False
            for frame in page.frames:
                if re.search(r"discordsays\.com", frame.url):
                    logger.info("Activity iframe already present — continuing")
                    found = True
                    break
            if not found:
                logger.error("No game iframe found. Please open Letter League manually, then re-run.")
                logger.info("Keeping browser open for 120s for manual setup...")
                await asyncio.sleep(120)
                return
        await asyncio.sleep(3)  # let game fully render

        # Dismiss any lingering popups (soundboard, etc.)
        await page.keyboard.press("Escape")
        await asyncio.sleep(1)

        # Verify calibration
        bbox = await verify_calibration(page)
        if bbox is None:
            logger.error("Could not get canvas bounding box")
            return

        # Run placement test
        await test_placement(page, dry_run=dry_run)

        # Keep browser open for inspection
        logger.info("Done! Browser stays open for 60s for inspection...")
        await asyncio.sleep(60)

    except KeyboardInterrupt:
        logger.info("Interrupted")
    except Exception:
        logger.exception("Test failed")
    finally:
        await context.close()
        await pw.stop()


if __name__ == "__main__":
    asyncio.run(main())
