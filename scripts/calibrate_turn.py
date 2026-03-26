"""Calibration script for turn detection HSV thresholds.

Run during a live Letter League game to capture screenshots and print
HSV statistics for the banner region. Saves frames to debug/turn_detection/
for visual inspection and threshold tuning.

Usage:
    python scripts/calibrate_turn.py

Requires DISCORD_CHANNEL_URL in .env file.
Press Ctrl+C to stop capturing.
"""
from __future__ import annotations

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
from dotenv import load_dotenv
from loguru import logger

from src.browser import BrowserSession, capture_canvas, navigate_to_activity
from src.browser.turn_detector import (
    BANNER_CONFIDENCE,
    BANNER_HSV_LOWER,
    BANNER_HSV_UPPER,
    BANNER_ROI_FRAC,
)
from src.vision.preprocessor import BOARD_HSV_LOWER, BOARD_HSV_UPPER

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEBUG_DIR = Path("debug/turn_detection")  # Relative to CWD (project root)
BANNER_ROI_FRAC = BANNER_ROI_FRAC        # Re-export for clarity — same as turn_detector
CAPTURE_INTERVAL = 2.0                    # Seconds between captures


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def main() -> None:
    """Run the interactive calibration capture loop."""
    load_dotenv()

    channel_url = os.environ.get("DISCORD_CHANNEL_URL")
    if not channel_url:
        logger.error(
            "DISCORD_CHANNEL_URL not set. Add it to your .env file and retry."
        )
        sys.exit(1)

    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("Debug frames will be saved to: {}", DEBUG_DIR.resolve())

    session = BrowserSession()
    page = await session.start()

    try:
        await navigate_to_activity(page, channel_url)
        logger.info(
            "Starting calibration — capturing every {}s. Press Ctrl+C to stop.",
            CAPTURE_INTERVAL,
        )

        # Accumulators for summary statistics across all captured frames.
        all_h: list[float] = []
        all_s: list[float] = []
        all_v: list[float] = []
        all_orange_ratios: list[float] = []
        all_peach_ratios: list[float] = []

        count = 0
        try:
            while True:
                # --- Capture ---
                img_bytes = await capture_canvas(page)

                # --- Save to disk ---
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                frame_path = DEBUG_DIR / f"frame_{timestamp}.png"
                frame_path.write_bytes(img_bytes)

                # --- Decode ---
                arr = np.frombuffer(img_bytes, dtype=np.uint8)
                bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                if bgr is None:
                    logger.warning("Frame {} could not be decoded — skipping.", count)
                    count += 1
                    await asyncio.sleep(CAPTURE_INTERVAL)
                    continue

                h_img, w_img = bgr.shape[:2]

                # --- Banner ROI (top fraction of canvas) ---
                y_start = int(h_img * BANNER_ROI_FRAC[0])
                y_end = int(h_img * BANNER_ROI_FRAC[1])
                roi = bgr[y_start:y_end, :]
                hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                h_chan = hsv_roi[:, :, 0].astype(float)
                s_chan = hsv_roi[:, :, 1].astype(float)
                v_chan = hsv_roi[:, :, 2].astype(float)

                med_h = float(np.median(h_chan))
                med_s = float(np.median(s_chan))
                med_v = float(np.median(v_chan))
                min_h, min_s, min_v = float(h_chan.min()), float(s_chan.min()), float(v_chan.min())
                max_h, max_s, max_v = float(h_chan.max()), float(s_chan.max()), float(v_chan.max())

                orange_mask = cv2.inRange(hsv_roi, BANNER_HSV_LOWER, BANNER_HSV_UPPER)
                orange_ratio = float(np.count_nonzero(orange_mask) / orange_mask.size)

                # --- Centre region (middle 50%) for game-over calibration ---
                cy_start = int(h_img * 0.25)
                cy_end = int(h_img * 0.75)
                cx_start = int(w_img * 0.25)
                cx_end = int(w_img * 0.75)
                centre = bgr[cy_start:cy_end, cx_start:cx_end]
                hsv_centre = cv2.cvtColor(centre, cv2.COLOR_BGR2HSV)
                peach_mask = cv2.inRange(hsv_centre, BOARD_HSV_LOWER, BOARD_HSV_UPPER)
                peach_ratio = float(np.count_nonzero(peach_mask) / peach_mask.size)

                # --- Accumulate for end-of-session summary ---
                all_h.append(med_h)
                all_s.append(med_s)
                all_v.append(med_v)
                all_orange_ratios.append(orange_ratio)
                all_peach_ratios.append(peach_ratio)

                # --- Log per-frame stats ---
                logger.info(
                    "Frame {:04d} | banner ROI HSV median=({:.1f},{:.1f},{:.1f}) "
                    "min=({:.0f},{:.0f},{:.0f}) max=({:.0f},{:.0f},{:.0f}) | "
                    "orange_ratio={:.4f} (threshold={:.2f}) | "
                    "centre_peach_ratio={:.4f} | saved={}",
                    count,
                    med_h, med_s, med_v,
                    min_h, min_s, min_v,
                    max_h, max_s, max_v,
                    orange_ratio,
                    BANNER_CONFIDENCE,
                    peach_ratio,
                    frame_path.name,
                )

                count += 1
                await asyncio.sleep(CAPTURE_INTERVAL)

        except KeyboardInterrupt:
            logger.info(
                "Calibration stopped. {} frames saved to {}", count, DEBUG_DIR.resolve()
            )

            # --- End-of-session summary ---
            if count > 0:
                logger.info("--- Session Summary ---")
                logger.info(
                    "Banner ROI median H: min={:.1f}  max={:.1f}  mean={:.1f}",
                    min(all_h), max(all_h), float(np.mean(all_h)),
                )
                logger.info(
                    "Banner ROI median S: min={:.1f}  max={:.1f}  mean={:.1f}",
                    min(all_s), max(all_s), float(np.mean(all_s)),
                )
                logger.info(
                    "Banner ROI median V: min={:.1f}  max={:.1f}  mean={:.1f}",
                    min(all_v), max(all_v), float(np.mean(all_v)),
                )
                logger.info(
                    "Orange pixel ratio: min={:.4f}  max={:.4f}  mean={:.4f}",
                    min(all_orange_ratios), max(all_orange_ratios), float(np.mean(all_orange_ratios)),
                )
                logger.info(
                    "Centre peach ratio: min={:.4f}  max={:.4f}  mean={:.4f}",
                    min(all_peach_ratios), max(all_peach_ratios), float(np.mean(all_peach_ratios)),
                )
                logger.info(
                    "Suggested BANNER_HSV_LOWER: [{:.0f}, <your_S_min>, <your_V_min>]",
                    min(all_h),
                )
                logger.info(
                    "Suggested BANNER_HSV_UPPER: [{:.0f}, 255, 255]",
                    max(all_h),
                )

    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
