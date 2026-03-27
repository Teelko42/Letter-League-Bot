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
    """Capture screenshot, overlay grid, save to debug/, return canvas bbox."""
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

    # Draw grid overlay on screenshot
    overlay = img.copy()
    origin_x = GRID_X0_FRAC * w - 0.5 * CELL_W_FRAC * w
    origin_y = GRID_Y0_FRAC * h - 0.5 * CELL_H_FRAC * h
    cell_w = CELL_W_FRAC * w
    cell_h = CELL_H_FRAC * h

    for r in range(16):
        y = int(origin_y + r * cell_h)
        cv2.line(overlay, (int(origin_x), y), (int(origin_x + 15 * cell_w), y), (0, 255, 0), 1)
    for c in range(16):
        x = int(origin_x + c * cell_w)
        cv2.line(overlay, (x, int(origin_y)), (x, int(origin_y + 15 * cell_h)), (0, 255, 0), 1)

    # Cell centers
    for r in range(15):
        for c in range(15):
            cx = int((GRID_X0_FRAC + c * CELL_W_FRAC) * w)
            cy = int((GRID_Y0_FRAC + r * CELL_H_FRAC) * h)
            cv2.circle(overlay, (cx, cy), 2, (0, 0, 255), -1)

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
    from src.engine.gaddag import GADDAG
    from src.engine.move_generator import find_all_moves

    logger.info("Loading dictionary...")
    gaddag = GADDAG.from_file("data/twl06.txt")

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
