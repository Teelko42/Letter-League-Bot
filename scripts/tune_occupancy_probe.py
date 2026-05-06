"""Offline tuning of the empty-vs-occupied cell probe.

Rationale: empty board cells (peach) and empty multipliers (2L/3L/2W/3W) render
as nearly-uniform colour. Tiles render with a coloured background AND a letter
glyph in the centre — committed tiles use a dark glyph, staged tiles use a
white glyph. Either way the cell becomes bimodal in V (HSV brightness).

Heuristic: V_range = V.max() - V.min() in a 50% cell-sized sample around the
cell centre. Empty cells produce V_range <= 70 (the upper end is the "shadow"
that committed tiles render into the cell below). Any tile produces
V_range >= 128 in the corpus under debug/tile_placer/. A threshold of 100
cleanly separates the two with margin on both sides.

Sample fraction was lowered from 0.9 to 0.5 because committed tiles render
with a multiplier badge that protrudes above the cell's top edge; a 90%
sample of a *neighbouring* empty cell catches that bleed and reads as
occupied (V_range up to 140). 0.5 keeps the sample inside the cell's true
content area, isolating it from neighbour bleed.

Run:
    py scripts/tune_occupancy_probe.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np

GRID_X0_FRAC = 0.056820
GRID_Y0_FRAC = 0.070587
CELL_W_FRAC = 0.032756
CELL_H_FRAC = 0.045038
ROWS = 19
COLS = 27

SAMPLE_FRAC = 0.5
V_RANGE_THRESHOLD = 100


def cell_center(img_w: int, img_h: int, row: int, col: int) -> tuple[int, int]:
    cx = (GRID_X0_FRAC + (col + 0.5) * CELL_W_FRAC) * img_w
    cy = (GRID_Y0_FRAC + (row + 0.5) * CELL_H_FRAC) * img_h
    return int(cx), int(cy)


def cell_size_px(img_w: int, img_h: int) -> tuple[int, int]:
    return int(CELL_W_FRAC * img_w), int(CELL_H_FRAC * img_h)


def v_range(img_bgr: np.ndarray, row: int, col: int) -> int:
    h, w = img_bgr.shape[:2]
    cx, cy = cell_center(w, h, row, col)
    cw, ch = cell_size_px(w, h)
    half_w = int(cw * SAMPLE_FRAC * 0.5)
    half_h = int(ch * SAMPLE_FRAC * 0.5)
    x0, x1 = max(0, cx - half_w), min(w, cx + half_w)
    y0, y1 = max(0, cy - half_h), min(h, cy + half_h)
    if x1 <= x0 or y1 <= y0:
        return 0
    crop = img_bgr[y0:y1, x0:x1]
    v = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)[:, :, 2]
    return int(v.max()) - int(v.min())


def annotate(img_bgr: np.ndarray, out_path: Path) -> None:
    h, w = img_bgr.shape[:2]
    overlay = img_bgr.copy()
    for r in range(ROWS):
        for c in range(COLS):
            cx, cy = cell_center(w, h, r, c)
            vr = v_range(img_bgr, r, c)
            occupied = vr > V_RANGE_THRESHOLD
            color = (0, 200, 0) if occupied else (0, 0, 200)
            cv2.circle(overlay, (cx, cy), 4, color, -1)
            cv2.circle(overlay, (cx, cy), 4, (255, 255, 255), 1)
    blend = cv2.addWeighted(img_bgr, 0.6, overlay, 0.4, 0)
    cv2.imwrite(str(out_path), blend)


def main() -> int:
    src_dir = Path("debug/tile_placer")
    out_dir = Path("debug/probe_tuning")
    out_dir.mkdir(parents=True, exist_ok=True)

    screenshots = sorted(src_dir.glob("pre_play_*.png"))
    if not screenshots:
        print(f"No pre_play_*.png in {src_dir}", file=sys.stderr)
        return 1

    print(f"Tuning probe on {len(screenshots)} screenshots")
    print(f"  SAMPLE_FRAC={SAMPLE_FRAC}  V_RANGE_THRESHOLD={V_RANGE_THRESHOLD}")

    for p in screenshots:
        img = cv2.imread(str(p))
        if img is None:
            continue
        annotate(img, out_dir / p.name)
    print(f"Wrote {len(screenshots)} overlays to {out_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
