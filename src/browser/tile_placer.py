from __future__ import annotations

import asyncio
import re
import random
from pathlib import Path
from typing import TYPE_CHECKING, Any

import cv2
import numpy as np
from loguru import logger

from src.browser.capture import capture_canvas
from src.browser.turn_detector import classify_frame
from src.engine import rejected_words

if TYPE_CHECKING:
    from src.engine.models import Move, TileUse

# ---------------------------------------------------------------------------
# Fractional constants
# ---------------------------------------------------------------------------
# All fractions are relative to the GAME CANVAS width or height (not the
# outer iframe — see _get_canvas_bbox for how the game area is computed when
# the <canvas> element cannot be located).
#
# Calibrated from live iframe at 1057x768 (viewport 1920x1080, chat hidden).
# GRID_X0/Y0 point to the TOP-LEFT corner of cell(0,0).
# board_cell_px(r,c) returns the top-left of each cell (close enough to the
# center for click-to-place to register).
#
# Board is 19 rows x 27 columns.

GRID_X0_FRAC = 0.056820    # top-left of cell(0,0) X (fraction of canvas width)
GRID_Y0_FRAC = 0.070587    # top-left of cell(0,0) Y (fraction of canvas height)
CELL_W_FRAC = 0.032756     # one cell width  (fraction of canvas width)  — 27 cols
CELL_H_FRAC = 0.045038     # one cell height (fraction of canvas height) — 19 rows

# Canvas dimensions when the grid constants above were calibrated.
# Kept for reference only — not used in placement logic.
CALIBRATION_CANVAS_W = 1057
CALIBRATION_CANVAS_H = 768
RACK_Y_FRAC = 0.932836     # rack row vertical center — calibrated from live 1057x768: y=716 on tile body
RACK_X0_FRAC = 0.391675    # first rack tile center — calibrated from live 1057x768: x=414
RACK_TILE_STEP_FRAC = 0.035793  # spacing between rack tile centers — calibrated from live 1057x768: ~38px
CONFIRM_X_FRAC = 0.499527  # PLAY button center X — X frac is ~0.5 at every canvas width we've seen
# Button-bar Y is NOT a constant fraction of canvas height — the game reflows
# the UI when the window widens, pushing the rack+button-bar further up from
# the canvas bottom.  Two real-world calibrations:
#   width=1057 → button bar center y=692 (y_frac=0.9010)
#   width=1545 → button bar center y=639 (y_frac=0.8320)
# Linear fit: y = 692 - 0.1086*(w - 1057).  See _button_bar_y() in CoordMapper.
# Prior bug: a fixed CONFIRM_Y_FRAC=0.901 on a 1545-wide canvas landed 53px
# BELOW the button bar, so PLAY/RECALL clicks hit empty space — every word
# was silently "rejected" because the click never reached the button.

MAX_WORD_RETRIES = 2        # max different words to try before tile swap
# Lowered 5 → 3 → 2.  Multiple consecutive runs show 100% of accepted plays
# came from attempt 1 of each vision pass; attempts 2+ from the *same* vision
# share the same root-cause failure (vision position drift, or a candidate
# the game's dictionary just won't accept) so they almost always reject too,
# burning ~30 s each.  The autoplay loop already re-vision-retries with a
# fresh candidate list, so the effective per-turn cap is still 4 attempts —
# enough headroom for the rare 2-attempts-needed turn while reclaiming
# wallclock for additional turns within the 30-min orchestrator timeout.

# Acceptance-detection polling: how many times (and how often) to re-check the
# turn state after clicking confirm.  Total wait ≈ polls × (interval + ~0.4 s
# screenshot).
#
# Why this is generous: Letter League's server-side validation + commit
# animation has high variance — observed acceptances range from 1.4 s (fast)
# to >4 s (slow) on the same network. The Massive-patch-#2 tightening to
# 3×0.6 s ≈ 1.8 s caused valid words (DISH, RAGE, GRADE, BLUEY, ARGUED, etc.)
# to be misclassified as rejected: the orange "your turn" banner was still
# visible at the final poll, the bot recalled the tiles mid-validation, and
# blacklisted the word. Restoring a wider window (6×1.0 s ≈ 6 s plus capture
# overhead) is the right tradeoff: an extra ~4 s on the rare actual rejection
# is far cheaper than turning every slow acceptance into a phantom rejection.
_ACCEPT_POLLS = 6           # number of post-confirm screenshots
_ACCEPT_POLL_INTERVAL_S = 1.0  # seconds between each poll

# Debug screenshot directory — captures pre-PLAY and post-RECALL states.
# Saved to debug/tile_placer/ alongside other debug images.
_DEBUG_DIR = Path("debug/tile_placer")
RECALL_X_FRAC = 0.589404   # RECALL button X — RIGHT of PLAY. Three-button layout: SWAP(0.41) | PLAY(0.50) | RECALL(0.59)
SWAP_X_FRAC = 0.409650     # SWAP button X — LEFT of PLAY (x=433 at 1057x768). NOT the same as RECALL.
# RECALL/SWAP share the PLAY row; Y is computed by CoordMapper._button_bar_y().

# "Select a letter" blank-tile dialog — probe points for open-state detection.
# Calibrated from data/calibration/post_recall_attempt5.png (1545x768 canvas).
# The X close button's inner cross is pure white (255,255,255) when visible;
# when absent, the same screen position shows a board cell color (peach, 2W
# green, 3W pink, etc.) — never near-white. The dialog title "Select a letter"
# at y≈0.329h renders orange text (BGR≈92,136,255) on cream; the same position
# on the bare board shows peach (BGR≈198,229,255). Combining both probes
# eliminates the aspect-ratio ambiguity either one alone has.
BLANK_DIALOG_X_BTN_FRAC = (0.6434, 0.2448)
BLANK_DIALOG_TITLE_FRAC = (0.400, 0.329)


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------


class PlacementError(Exception):
    """Raised when tile placement fails after retries."""


class CoordinateDriftError(PlacementError):
    """Placement failed with the 'global canvas changed but target cell didn't' signature.

    The mouse click registered (rack tile highlighted, score banner repainted,
    PLAY label changed) but no tile landed in or near the targeted cell. Almost
    always means the engine's (row, col) does not correspond to the live
    board's cell — i.e. vision drift cascaded into the placer. Trying further
    candidates from the same vision pass will hit the same misaligned cells,
    so the placer raises this to short-circuit the candidate loop and let the
    orchestrator re-vision before its next attempt.
    """


def _canvas_unchanged(before: bytes, after: bytes, threshold: float = 0.15) -> bool:
    """Return True when two PNG captures are nearly identical.

    Used by the recall loop to detect that no further tiles are flying back
    to the rack — the signal that the board has been fully cleared.

    Args:
        before: PNG bytes from before a click.
        after:  PNG bytes from after the click (+ settle delay).
        threshold: Mean per-pixel absolute difference above which the two
            frames are considered to differ.  0.15 matches the threshold
            used by ``_verify_placement`` and is large enough to ignore
            anti-aliasing / timer-text flicker while catching a real tile
            animation.
    """
    arr_b = np.frombuffer(before, dtype=np.uint8)
    arr_a = np.frombuffer(after, dtype=np.uint8)
    img_b = cv2.imdecode(arr_b, cv2.IMREAD_COLOR)
    img_a = cv2.imdecode(arr_a, cv2.IMREAD_COLOR)
    if img_b is None or img_a is None or img_b.shape != img_a.shape:
        return False
    diff = float(np.mean(np.abs(img_b.astype(np.int32) - img_a.astype(np.int32))))
    return diff <= threshold


# Pre-flight anchor probe. When the engine plans a move it cites cells that
# are *already* occupied by committed tiles (the move's anchors — TileUse with
# from_rack=False) and cells that must be empty (TileUse with from_rack=True).
# Vision drift produces moves whose anchor cells aren't actually occupied on
# the live board; placing such a move always rejects and burns ~30 s. Probing
# the cells before any click catches drift without cost.
#
# Heuristic (tuned offline against debug/tile_placer/pre_play_*.png):
# committed tiles render with a coloured background AND a contrasting letter
# glyph, so a cell-centred sample yields V_range > 100 (typically ~224).
# Empty cells (peach board background or any of the 2L/3L/2W/3W multipliers)
# are nearly uniform with V_range == 0 when isolated.
#
# Sample fraction is 0.5 (not full cell) because committed tiles render with
# a small "DW²" multiplier badge that protrudes a few pixels above the cell's
# nominal top edge, and a drop shadow that bleeds a few pixels into the cell
# below. A 90% sample of a *neighbouring* empty cell would catch that bleed
# and produce V_range up to 140, falsely flagging the empty cell as occupied
# (and rejecting every candidate the engine planned that touched such a
# cell). At 0.5 the worst empty-cell-with-neighbour reading is V_range≈70
# (the drop-shadow case below a tile); the wide ambiguous band (50-150) gives
# margin against borderline cases without false anchor rejections in
# multi-word states where vision may report tiles slightly offset from where
# they actually render.
_PROBE_SAMPLE_FRAC = 0.5
_V_RANGE_OCCUPIED = 150  # cell is occupied if V.max - V.min > this in the sample
_V_RANGE_EMPTY = 50      # cell is empty if V.max - V.min <= this; in-between is ambiguous


def _cell_v_range(img: np.ndarray, row: int, col: int) -> int:
    """Return the V (HSV brightness) range in a 90% cell-sized sample at (row, col).

    Args:
        img: BGR image of the iframe screenshot.
        row: Zero-based board row.
        col: Zero-based board column.

    Returns:
        V.max() - V.min() over the sample crop, or 0 if the crop falls
        outside the image bounds.
    """
    h, w = img.shape[:2]
    cx = (GRID_X0_FRAC + (col + 0.5) * CELL_W_FRAC) * w
    cy = (GRID_Y0_FRAC + (row + 0.5) * CELL_H_FRAC) * h
    half_w = int(CELL_W_FRAC * w * _PROBE_SAMPLE_FRAC * 0.5)
    half_h = int(CELL_H_FRAC * h * _PROBE_SAMPLE_FRAC * 0.5)
    x0, x1 = max(0, int(cx) - half_w), min(w, int(cx) + half_w)
    y0, y1 = max(0, int(cy) - half_h), min(h, int(cy) + half_h)
    if x1 <= x0 or y1 <= y0:
        return 0
    crop = img[y0:y1, x0:x1]
    v = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)[:, :, 2]
    return int(v.max()) - int(v.min())


def _check_move_anchors(img_bytes: bytes, move: Move) -> str | None:
    """Verify the move's anchor and rack-tile cells match the live board.

    For each tile in ``move.tiles_used``:
      * ``from_rack=False`` (anchor) — the engine believes a committed tile
        already sits at this position. The cell must register as occupied
        (V_range > _V_RANGE_OCCUPIED).
      * ``from_rack=True``  (destination) — a rack tile is about to be placed
        here. The cell must register as empty (V_range <= _V_RANGE_EMPTY).

    Cells whose V_range falls between the two thresholds are treated as
    ambiguous and ignored — the heuristic refuses to pronounce the engine
    wrong on borderline pixel readings.

    Args:
        img_bytes: PNG screenshot bytes from ``capture_canvas``.
        move:      The Move about to be placed.

    Returns:
        ``None`` if every probed cell agrees with the engine. Otherwise a
        human-readable description of the first disagreement, suitable for
        a CoordinateDriftError message.
    """
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        return None  # decode failure; don't gate placement on a bad screenshot

    for tile in move.tiles_used:
        vr = _cell_v_range(img, tile.row, tile.col)
        if not tile.from_rack:
            # Anchor must be occupied. Only flag if unambiguously empty.
            if vr <= _V_RANGE_EMPTY:
                return (
                    f"anchor '{tile.letter}' at ({tile.row},{tile.col}) "
                    f"is empty on the live board (V_range={vr}); engine "
                    f"believes a committed tile is here"
                )
        else:
            # Rack-tile destination must be empty. Only flag if unambiguously occupied.
            if vr > _V_RANGE_OCCUPIED:
                return (
                    f"rack-tile destination ({tile.row},{tile.col}) is "
                    f"already occupied (V_range={vr}); engine plans to "
                    f"place '{tile.letter}' here"
                )
    return None


def _is_blank_dialog_open(img_bytes: bytes) -> bool:
    """Pixel-sample whether the 'Select a letter' blank-tile dialog is visible.

    A blank tile placed on the board but never assigned a letter leaves the
    modal "Select a letter" dialog open. That dialog blocks every canvas
    button (PLAY, RECALL, SWAP) — and if the bot crashes, or the user
    manually intervenes, the dialog persists into the next autoplay run.
    Downstream vision reads see the overlay's letter grid as phantom board
    tiles, which drives the engine to attempt impossible moves.

    We probe two fixed points instead of one because the dialog is centered
    over the board, where any single pixel could coincide with a same-colored
    board feature under a different aspect ratio:
      * X close button center — pure white when the dialog is up; peach /
        green / pink board-cell colors otherwise.
      * Dialog title text area — bright orange on cream when the dialog is
        up; peach board background otherwise.

    Args:
        img_bytes: PNG screenshot bytes from ``capture_canvas``.

    Returns:
        ``True`` iff both probe points match the dialog's signature colors.
        On decode failure or out-of-bounds sampling, returns ``False`` so the
        caller treats the state as "dialog absent" and proceeds normally.
    """
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # BGR
    if img is None:
        return False
    h, w = img.shape[:2]
    x1 = int(BLANK_DIALOG_X_BTN_FRAC[0] * w)
    y1 = int(BLANK_DIALOG_X_BTN_FRAC[1] * h)
    x2 = int(BLANK_DIALOG_TITLE_FRAC[0] * w)
    y2 = int(BLANK_DIALOG_TITLE_FRAC[1] * h)
    if not (0 <= x1 < w and 0 <= y1 < h and 0 <= x2 < w and 0 <= y2 < h):
        return False
    b1, g1, r1 = (int(v) for v in img[y1, x1])
    b2, g2, r2 = (int(v) for v in img[y2, x2])
    x_btn_is_white = b1 >= 240 and g1 >= 240 and r1 >= 240
    # Orange title: high red, low-mid green, low blue; board peach has
    # near-saturated green (≥220) and blue (≥240), so the ceiling on g2/b2
    # rejects peach without clipping legitimate title pixels.
    title_is_orange = r2 >= 230 and g2 <= 180 and b2 <= 150
    return x_btn_is_white and title_is_orange


# ---------------------------------------------------------------------------
# CoordMapper
# ---------------------------------------------------------------------------


class CoordMapper:
    """Translates board grid indices and rack slot indices into viewport pixels.

    All coordinates are computed from fractional constants relative to the
    canvas bounding box. This makes the mapper resolution-independent —
    fractional constants remain valid regardless of window size, as long as the
    aspect ratio stays consistent.

    Args:
        bbox: Canvas bounding box dict with keys ``x``, ``y``, ``width``,
            ``height`` (as returned by Playwright/patchright
            ``element.bounding_box()``).

    Raises:
        PlacementError: If ``bbox`` is ``None``.
    """

    def __init__(self, bbox: dict) -> None:
        if bbox is None:
            raise PlacementError("Canvas bounding box is None — cannot map coordinates.")
        self._bbox = bbox

    # ------------------------------------------------------------------
    # Public coordinate helpers
    # ------------------------------------------------------------------

    def board_cell_px(self, row: int, col: int) -> tuple[float, float]:
        """Return viewport pixel coordinates for the center of board cell (row, col).

        GRID_X0/Y0 mark the top-left corner of cell(0,0), so we add half a
        cell width/height to land on the cell centre rather than on the
        boundary between adjacent cells.

        Args:
            row: Zero-based row index on the board.
            col: Zero-based column index on the board.

        Returns:
            ``(x, y)`` viewport pixel coordinates.
        """
        x = self._bbox["x"] + (GRID_X0_FRAC + (col + 0.5) * CELL_W_FRAC) * self._bbox["width"]
        y = self._bbox["y"] + (GRID_Y0_FRAC + (row + 0.5) * CELL_H_FRAC) * self._bbox["height"]
        return x, y

    def rack_tile_px(self, slot_index: int) -> tuple[float, float]:
        """Return viewport pixel coordinates for rack tile at given slot index.

        Args:
            slot_index: Zero-based rack slot index (0 = leftmost tile).

        Returns:
            ``(x, y)`` viewport pixel coordinates.
        """
        x = self._bbox["x"] + (RACK_X0_FRAC + slot_index * RACK_TILE_STEP_FRAC) * self._bbox["width"]
        y = self._bbox["y"] + RACK_Y_FRAC * self._bbox["height"]
        return x, y

    def _button_bar_y(self) -> float:
        """Return viewport y-coordinate for the center of the SWAP/PLAY/RECALL row.

        Letter League's UI shifts the button bar vertically as the canvas
        widens — at width 1057 the bar is at iframe-y 692; at width 1545 it
        is at iframe-y 639.  Linear fit between those two measurements.
        Clamped to [550, 720] so a degenerate bbox never produces an insane
        click coordinate that would bypass the safety of a missed click.
        """
        w = self._bbox["width"]
        y_iframe = 692.0 - 0.1086 * (w - 1057.0)
        y_iframe = max(550.0, min(720.0, y_iframe))
        return self._bbox["y"] + y_iframe

    def confirm_btn_px(self) -> tuple[float, float]:
        """Return viewport pixel coordinates for the confirm button.

        Returns:
            ``(x, y)`` viewport pixel coordinates.
        """
        x = self._bbox["x"] + CONFIRM_X_FRAC * self._bbox["width"]
        return x, self._button_bar_y()

    def recall_btn_px(self) -> tuple[float, float]:
        """Return viewport pixel coordinates for the recall/undo button.

        Clicking this button clears placed tiles from the board back to the
        rack, allowing the bot to retry with a different word.

        Returns:
            ``(x, y)`` viewport pixel coordinates.
        """
        x = self._bbox["x"] + RECALL_X_FRAC * self._bbox["width"]
        return x, self._button_bar_y()

    def swap_btn_px(self) -> tuple[float, float]:
        """Return viewport pixel coordinates for the tile swap button.

        Clicking this button performs a tile swap when no valid words can be
        placed. Used as a final fallback after MAX_WORD_RETRIES attempts.

        Returns:
            ``(x, y)`` viewport pixel coordinates.
        """
        x = self._bbox["x"] + SWAP_X_FRAC * self._bbox["width"]
        return x, self._button_bar_y()


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def jitter(x: float, y: float, px: int = 3) -> tuple[float, float]:
    """Add uniform random jitter within +/-px to both coordinates.

    Introduces human-like imprecision to mouse movements so that placements
    do not hit exactly the same pixel every time.

    Args:
        x: Base X coordinate.
        y: Base Y coordinate.
        px: Maximum jitter magnitude in pixels (inclusive).

    Returns:
        ``(x + dx, y + dy)`` with ``dx, dy`` each drawn from ``[-px, px]``.
    """
    return (
        x + random.uniform(-px, px),
        y + random.uniform(-px, px),
    )


def assign_rack_indices(rack: list[str], rack_tiles: list[TileUse]) -> list[int]:
    """Map each TileUse to a leftmost available rack slot index.

    For blank tiles (``tile.is_blank == True``), the search matches ``'?'``
    in the remaining rack slots rather than ``tile.letter``.

    The function consumes slots greedily left-to-right — when multiple tiles
    share the same letter (or blank), each successive tile is mapped to the
    next available slot further to the right.

    Args:
        rack: Current rack as a list of letter strings (e.g. ``['A', 'B', '?', 'C']``).
            ``'?'`` represents a blank tile.
        rack_tiles: Ordered list of ``TileUse`` objects whose ``from_rack`` is
            ``True`` that need to be mapped to rack slots.

    Returns:
        List of integer slot indices (same length as ``rack_tiles``), where
        ``result[i]`` is the rack slot index for ``rack_tiles[i]``.

    Raises:
        ValueError: If any tile letter (or blank ``'?'``) is not found among
            the remaining (unconsumed) rack slots.
    """
    remaining: list[str | None] = list(rack)  # copy; consumed slots become None

    indices: list[int] = []
    for tile in rack_tiles:
        search_letter = "?" if tile.is_blank else tile.letter
        found_idx: int | None = None
        for i, slot in enumerate(remaining):
            if slot == search_letter:
                found_idx = i
                break
        if found_idx is None:
            raise ValueError(
                f"Rack tile '{search_letter}' not found in remaining rack slots: "
                f"{[s for s in remaining if s is not None]}"
            )
        remaining[found_idx] = None  # Consume the slot
        indices.append(found_idx)

    return indices


# ---------------------------------------------------------------------------
# TilePlacer
# ---------------------------------------------------------------------------


class TilePlacer:
    """Orchestrates drag-and-drop tile placements on the game canvas.

    Uses the patchright ``page.mouse`` API to drag tiles from rack slots to
    board cells. Every placement is verified via a pixel-diff screenshot check
    and retried once on failure.

    Args:
        page: A patchright ``Page`` object (typed as ``Any`` to avoid import
            complexity; the caller is responsible for passing a valid page).
    """

    def __init__(self, page: Any) -> None:
        self._page = page
        self._bbox: dict | None = None  # stashed by place_move for in-frame clicks
        # Last verify diffs, exposed for the drift detector in place_tiles.
        # Initialised to +inf so that mocked _verify_placement in unit tests
        # (which never updates these) is treated as "no drift signal".
        self._last_global_diff: float = float("inf")
        self._last_local_diff: float = float("inf")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _get_canvas_bbox(self) -> dict:
        """Retrieve the game iframe's bounding box.

        All fractional grid constants (GRID_X0_FRAC, RECALL_X_FRAC, etc.)
        are calibrated against the **full iframe screenshot** as returned by
        ``capture_canvas``.  That screenshot encompasses the entire iframe
        area, including any gray letterbox / pillarbox margins the game
        engine adds when the iframe is larger than the game's natural render
        resolution.  The fractional constants already encode those margins as
        part of their measured offsets.

        We intentionally do NOT use the inner ``<canvas>`` element's bbox:
        the canvas is centered inside the iframe and its bounding box origin
        is NOT at (0, 0) in the iframe's local coordinate system.  Applying
        iframe-calibrated fractions to the narrower canvas bbox would
        produce wrong pixel coordinates — both for viewport mouse clicks and
        for the ``_click_in_frame`` JS dispatch that uses iframe-local
        coordinates.

        Returns:
            Bounding box dict with keys ``x``, ``y``, ``width``, ``height``.

        Raises:
            PlacementError: If the bounding box is ``None`` (iframe not found).
        """
        iframe_bbox = await (
            self._page
            .locator('iframe[src*="discordsays.com"]')
            .bounding_box(timeout=10_000)
        )
        if iframe_bbox is None:
            raise PlacementError(
                "Canvas bounding box is None — iframe not found."
            )

        logger.debug(
            "Using iframe bbox: {:.0f}x{:.0f} @ ({:.0f},{:.0f})",
            iframe_bbox["width"],
            iframe_bbox["height"],
            iframe_bbox["x"],
            iframe_bbox["y"],
        )
        return iframe_bbox

    async def _drag_tile(
        self,
        from_x: float,
        from_y: float,
        to_x: float,
        to_y: float,
        steps: int = 10,
    ) -> None:
        """Place a tile using click-to-select then click-to-place.

        Letter League (Discord Activity) uses a click-based interaction model
        rather than HTML5 drag-and-drop: click a rack tile to pick it up, then
        click a board cell to place it.

        Falls back to a slow drag if the click-click approach doesn't work
        (e.g. future game updates change the interaction model).

        Args:
            from_x: Source X viewport coordinate (rack tile).
            from_y: Source Y viewport coordinate (rack tile).
            to_x: Destination X viewport coordinate (board cell).
            to_y: Destination Y viewport coordinate (board cell).
            steps: Number of intermediate mouse-move steps (used for drag fallback).
        """
        # Click-to-select the rack tile, then click-to-place on the board cell.
        await self._page.mouse.click(from_x, from_y)
        await asyncio.sleep(0.5)
        await self._page.mouse.click(to_x, to_y)

    async def _dismiss_blank_letter_dialog(self, letter: str) -> None:
        """Dismiss the "Select a letter" dialog that appears after placing a blank tile.

        When a blank tile ('?') is placed on the board, the game shows a modal
        dialog with a grid of A-Z letter buttons.  The player (or bot) must click
        the desired letter before the game will allow the PLAY button to be
        active.

        Tries three strategies in order, retrying up to 2 times:
          1. **Keyboard press** — presses the letter key.  Cheapest approach and
             works if the game accepts keyboard input while the dialog is open.
          2. **Frame locator click** — finds the button whose exact text matches
             ``letter`` inside the game iframe and clicks it.
          3. **Viewport click** — clicks the computed pixel position of the
             letter button within the dialog's 7-column grid.

        After each round of strategies, captures a screenshot to verify the
        dialog closed (significant pixel change). Retries once if it didn't.

        Args:
            letter: The uppercase letter the blank tile should represent (A-Z).
        """
        letter = letter.upper()

        before_bytes = await capture_canvas(self._page, render_wait=False)

        for attempt in range(2):
            if attempt > 0:
                logger.warning(
                    "Blank dialog: retry {} for letter '{}'", attempt, letter,
                )
                await asyncio.sleep(0.5)

            # Strategy 1: press the letter key on the keyboard.
            try:
                await self._page.keyboard.press(letter)
                await asyncio.sleep(0.4)
                if await self._verify_dialog_dismissed(before_bytes):
                    logger.info("Blank dialog: dismissed '{}' via keyboard press", letter)
                    return
            except Exception as exc:
                logger.debug("Blank dialog: keyboard press failed for '{}' ({})", letter, exc)

            # Strategy 2: find the letter button as a DOM element inside the iframe.
            try:
                frame = self._page.frame_locator('iframe[src*="discordsays.com"]')
                letter_btn = frame.get_by_text(letter, exact=True).first
                await letter_btn.click(timeout=3_000)
                await asyncio.sleep(0.4)
                if await self._verify_dialog_dismissed(before_bytes):
                    logger.info("Blank dialog: dismissed '{}' via frame locator", letter)
                    return
            except Exception as exc:
                logger.debug("Blank dialog: frame locator failed for '{}' ({})", letter, exc)

            # Strategy 3: compute the button's pixel position from the known
            # 4-row alphabetical grid and click via viewport mouse.
            #
            # Grid layout (measured from a live 1545×768 dialog screenshot):
            #   Row 0 (y_frac 0.351):   A B C D E F G   (cols 0..6)
            #   Row 1 (y_frac 0.445):   H I J K L M N   (cols 0..6)
            #   Row 2 (y_frac 0.540):   O P Q R S T U   (cols 0..6)
            #   Row 3 (y_frac 0.634):     V W X Y Z     (cols 1..5, last row is
            #                                            5 buttons centered by a
            #                                            +1 column offset — NOT
            #                                            left-aligned)
            # Col step:  (0.6126 − 0.3860) / 6 = 0.03777  (frac of canvas width)
            # Row step:  (0.6337 − 0.3510) / 3 = 0.09423  (frac of canvas height)
            #
            # The previous formula used (right-left)/COLS for the *inter-center*
            # step and a +0.5 offset on every axis, which put the click ~34 px
            # below and ~10 px left of every letter — the dialog was never
            # dismissed.  That's why every subsequent PLAY click was blocked.
            COL0_FRAC_X = 0.3860   # column 0 button centre (A, H, O)
            COL_STEP_FRAC_X = 0.03777
            ROW0_FRAC_Y = 0.3510   # row 0 button centre (A..G)
            ROW_STEP_FRAC_Y = 0.09423

            letter_idx = ord(letter) - ord("A")
            row_idx = letter_idx // 7
            col_idx = letter_idx % 7
            if row_idx == 3:
                # V-Z sit in cols 1..5 (centred), not cols 0..4.
                col_idx = (letter_idx - 21) + 1

            frac_x = COL0_FRAC_X + col_idx * COL_STEP_FRAC_X
            frac_y = ROW0_FRAC_Y + row_idx * ROW_STEP_FRAC_Y

            bbox = self._bbox
            if bbox is None:
                try:
                    bbox = await self._get_canvas_bbox()
                except Exception:
                    logger.warning("Blank dialog: cannot get bbox for viewport click — skipping")
                    continue

            vp_x = bbox["x"] + frac_x * bbox["width"]
            vp_y = bbox["y"] + frac_y * bbox["height"]

            try:
                await self._page.mouse.click(vp_x, vp_y)
                await asyncio.sleep(0.4)
                if await self._verify_dialog_dismissed(before_bytes):
                    logger.info(
                        "Blank dialog: dismissed '{}' via viewport at ({:.1f}, {:.1f})",
                        letter, vp_x, vp_y,
                    )
                    return
            except Exception as exc:
                logger.warning("Blank dialog: viewport click failed for '{}': {}", letter, exc)

        logger.error(
            "Blank dialog: FAILED to dismiss for '{}' after all attempts — "
            "subsequent placements may fail",
            letter,
        )

    async def _verify_dialog_dismissed(self, before_bytes: bytes) -> bool:
        """Check if the blank-tile dialog was dismissed by comparing screenshots.

        A significant pixel change indicates the dialog overlay disappeared.
        Uses the same approach as ``_verify_placement`` but with a lower
        threshold since the dialog covers a large portion of the screen.

        Args:
            before_bytes: PNG screenshot captured while the dialog was visible.

        Returns:
            ``True`` if the screen changed (dialog likely closed).
        """
        after_bytes = await capture_canvas(self._page, render_wait=False)

        def _decode(data: bytes) -> np.ndarray | None:
            arr = np.frombuffer(data, dtype=np.uint8)
            return cv2.imdecode(arr, cv2.IMREAD_COLOR)

        before_img = _decode(before_bytes)
        after_img = _decode(after_bytes)

        if before_img is None or after_img is None:
            return True  # Can't verify — assume success

        diff = float(np.mean(np.abs(before_img.astype(np.int32) - after_img.astype(np.int32))))
        logger.debug("Blank dialog dismiss pixel diff: {:.4f}", diff)
        return diff > 0.10

    async def _verify_placement(
        self,
        before_bytes: bytes,
        target_local_xy: tuple[float, float] | None = None,
        cell_w_px: float | None = None,
        cell_h_px: float | None = None,
    ) -> bool:
        """Verify a tile was placed by comparing before/after screenshots.

        Two-gate check when ``target_local_xy`` is provided:
          1. Global mean abs diff > 0.10 (the original gate — confirms the
             canvas changed at all).
          2. Cell-region mean abs diff > 1.0, where the region is a 1.5×
             cell-sized crop centred on the target cell.

        The cell-local gate exists because a global diff is fooled when a
        drag is rejected and the tile snaps back to the rack: the rack
        slot redraws briefly, the score banner can update, and the PLAY
        button label changes — all of which inflate the global diff while
        the target cell remains untouched. A real landing produces a large
        local diff because an empty multiplier square (saturated colour +
        white "2L"/"3W" text) is replaced by a tile (pastel background +
        large dark letter + small score number).

        Falls back to the global-only check if no target is given (used by
        the blank-letter dialog dismissal path, which has no specific cell
        to inspect).

        Args:
            before_bytes: PNG screenshot bytes captured before the drag.
            target_local_xy: Iframe-local (x, y) of the target cell centre,
                in pixels. ``None`` to skip the cell-local gate.
            cell_w_px: Cell width in screenshot pixels. Required when
                ``target_local_xy`` is given.
            cell_h_px: Cell height in screenshot pixels. Required when
                ``target_local_xy`` is given.

        Returns:
            ``True`` if both gates pass (or the global gate passes when no
            target is given). ``False`` otherwise, or if image decode fails.
        """
        after_bytes = await capture_canvas(self._page, render_wait=False)

        def _decode(data: bytes) -> np.ndarray | None:
            arr = np.frombuffer(data, dtype=np.uint8)
            return cv2.imdecode(arr, cv2.IMREAD_COLOR)

        before_img = _decode(before_bytes)
        after_img = _decode(after_bytes)

        if before_img is None or after_img is None:
            logger.warning("_verify_placement: image decode failed — treating as unverified")
            self._last_global_diff = float("inf")
            self._last_local_diff = float("inf")
            return False

        global_diff = float(
            np.mean(np.abs(before_img.astype(np.int32) - after_img.astype(np.int32)))
        )
        self._last_global_diff = global_diff

        if target_local_xy is None or cell_w_px is None or cell_h_px is None:
            logger.debug("Placement pixel diff (global): {:.4f}", global_diff)
            self._last_local_diff = float("inf")
            return global_diff > 0.10

        h_img, w_img = before_img.shape[:2]
        cx, cy = target_local_xy
        half_w = cell_w_px * 0.75
        half_h = cell_h_px * 0.75
        x0 = max(0, int(cx - half_w))
        y0 = max(0, int(cy - half_h))
        x1 = min(w_img, int(cx + half_w))
        y1 = min(h_img, int(cy + half_h))
        if x1 <= x0 or y1 <= y0:
            logger.warning(
                "Placement target ({:.0f},{:.0f}) outside screenshot {}x{} — "
                "falling back to global gate (diff={:.4f})",
                cx, cy, w_img, h_img, global_diff,
            )
            self._last_local_diff = float("inf")
            return global_diff > 0.10

        before_crop = before_img[y0:y1, x0:x1].astype(np.int32)
        after_crop = after_img[y0:y1, x0:x1].astype(np.int32)
        local_diff = float(np.mean(np.abs(before_crop - after_crop)))
        self._last_local_diff = local_diff
        logger.debug(
            "Placement pixel diff: global={:.4f} local={:.4f} cell=({:.0f},{:.0f}) crop={}x{}",
            global_diff, local_diff, cx, cy, x1 - x0, y1 - y0,
        )
        return global_diff > 0.10 and local_diff > 1.0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def place_tiles(self, move: Move, rack: list[str]) -> None:
        """Place all rack tiles for a move via drag-and-drop.

        Orchestration steps:
          1. Fetch canvas bounding box and build a ``CoordMapper``.
          2. Pre-flight anchor probe: capture the canvas and verify every
             ``from_rack=False`` cell already has a committed tile, and every
             ``from_rack=True`` cell is empty. Aborts with
             ``CoordinateDriftError`` on mismatch — saves ~30 s of
             click-then-reject when vision drift produced an impossible move.
          3. Retrieve rack tiles from the move.
          4. Assign each rack tile to a rack slot index.
          5. Sort placements in word-spelling order (left-to-right for
             horizontal; top-to-bottom for vertical).
          6. For each tile: compute jittered source + target coordinates,
             capture a before screenshot, drag the tile, verify placement.
             Retry once on failure; raise ``PlacementError`` if retry fails.
          7. Sleep 1–3 seconds between placements for human-like pacing.

        Args:
            move: The ``Move`` to execute.
            rack: Current rack as a list of letter strings (``'?'`` for blank).

        Raises:
            CoordinateDriftError: If the pre-flight anchor probe shows the
                live board doesn't match the engine's view of the move.
            PlacementError: If any tile placement fails after one retry.
            ValueError: If rack assignment fails (tile not in rack).
        """
        from src.engine.models import Move as _Move  # noqa: F401 — ensure type available

        bbox = await self._get_canvas_bbox()
        mapper = CoordMapper(bbox)

        # Cell dimensions in screenshot pixels — used by _verify_placement for
        # the cell-local crop. Computed once so the per-tile call site stays
        # quiet.
        cell_w_px = CELL_W_FRAC * bbox["width"]
        cell_h_px = CELL_H_FRAC * bbox["height"]

        rack_tiles: list[TileUse] = move.rack_tiles_consumed()
        if not rack_tiles:
            logger.info("No rack tiles to place for move '{}'", move.word)
            return

        # Pre-flight anchor probe. If the move's anchor cells (committed tiles
        # the engine plans to build off of) aren't actually occupied on the
        # live board, vision drift produced this candidate and every later
        # candidate from the same vision pass shares the same wrong frame.
        # Aborting here saves the ~30 s the placement+rejection cycle would
        # otherwise burn.
        preflight_bytes = await capture_canvas(self._page, render_wait=False)
        mismatch = _check_move_anchors(preflight_bytes, move)
        if mismatch is not None:
            raise CoordinateDriftError(
                f"Pre-flight anchor probe rejected '{move.word}': {mismatch}"
            )

        slot_indices = assign_rack_indices(rack, rack_tiles)

        # Sort placements in word-spelling order.
        if move.direction == "H":
            order = sorted(range(len(rack_tiles)), key=lambda i: rack_tiles[i].col)
        else:
            order = sorted(range(len(rack_tiles)), key=lambda i: rack_tiles[i].row)

        for ordinal, i in enumerate(order):
            tile = rack_tiles[i]
            slot_idx = slot_indices[i]

            rx, ry = jitter(*mapper.rack_tile_px(slot_idx))
            bx, by = jitter(*mapper.board_cell_px(tile.row, tile.col))

            logger.info(
                "Placing tile '{}' (slot {}) -> board ({},{}) | src=({:.1f},{:.1f}) dst=({:.1f},{:.1f})",
                tile.letter,
                slot_idx,
                tile.row,
                tile.col,
                rx,
                ry,
                bx,
                by,
            )

            # Iframe-local target for the cell-region verify crop. The
            # screenshot from capture_canvas is the iframe element, so the
            # bbox.x/.y origin must be subtracted from viewport coords.
            target_local = (bx - bbox["x"], by - bbox["y"])

            # Place tile via click-select, click-place with verification.
            # Capture a before screenshot, drag the tile, then verify the
            # canvas changed.  Retry once on failure with fresh jitter.
            before_bytes = await capture_canvas(self._page, render_wait=False)
            await self._drag_tile(rx, ry, bx, by)
            await asyncio.sleep(0.3)  # Let the game register the placement.

            placed = await self._verify_placement(
                before_bytes,
                target_local_xy=target_local,
                cell_w_px=cell_w_px,
                cell_h_px=cell_h_px,
            )
            # Snapshot the verifier's diffs immediately — the retry below will
            # overwrite them, and we need both attempts' values to decide
            # whether the failure looks like coordinate drift.
            attempt1_global = self._last_global_diff
            attempt1_local = self._last_local_diff
            if not placed:
                logger.warning(
                    "Tile '{}' placement not verified — retrying with fresh jitter",
                    tile.letter,
                )
                rx2, ry2 = jitter(*mapper.rack_tile_px(slot_idx))
                bx2, by2 = jitter(*mapper.board_cell_px(tile.row, tile.col))
                target_local2 = (bx2 - bbox["x"], by2 - bbox["y"])
                before_bytes = await capture_canvas(self._page, render_wait=False)
                await self._drag_tile(rx2, ry2, bx2, by2)
                await asyncio.sleep(0.3)

                placed = await self._verify_placement(
                    before_bytes,
                    target_local_xy=target_local2,
                    cell_w_px=cell_w_px,
                    cell_h_px=cell_h_px,
                )
                attempt2_global = self._last_global_diff
                attempt2_local = self._last_local_diff
                if not placed:
                    # Coordinate-drift signature: the click registered (rack
                    # repaints / score banner / PLAY label all push global_diff
                    # above the success threshold) but the target cell crop is
                    # essentially untouched. When this fires twice on the very
                    # first tile of a move, every later tile and every later
                    # candidate from the same vision pass will hit the same
                    # misaligned cells, so we abort the whole move and let the
                    # caller (place_move) re-vision instead of burning ~30 s
                    # per additional candidate.
                    drift1 = attempt1_global > 0.10 and attempt1_local < 1.0
                    drift2 = attempt2_global > 0.10 and attempt2_local < 1.0
                    if ordinal == 0 and drift1 and drift2:
                        raise CoordinateDriftError(
                            f"Tile '{tile.letter}' at ({tile.row},{tile.col}): "
                            f"two consecutive clicks failed to land in the "
                            f"target cell (local diffs {attempt1_local:.3f}, "
                            f"{attempt2_local:.3f}; canvas changed by "
                            f"{attempt1_global:.3f}, {attempt2_global:.3f}) — "
                            f"engine coordinates do not match the live board"
                        )
                    raise PlacementError(
                        f"Tile '{tile.letter}' at ({tile.row},{tile.col}) failed "
                        f"to place after retry"
                    )

            # If this is a blank tile, the game immediately opens a "Select a
            # letter" modal dialog.  We must dismiss it by clicking the target
            # letter before the bot can continue placing other tiles or clicking
            # PLAY.  Without this step the dialog blocks all subsequent UI
            # interaction and the word is never submitted.
            if tile.is_blank:
                await asyncio.sleep(0.5)  # Give the dialog time to animate in.
                await self._dismiss_blank_letter_dialog(tile.letter)
                await asyncio.sleep(0.5)  # Let the dialog fully close before next tile.

            logger.info(
                "Tile '{}' verified at ({},{})",
                tile.letter,
                tile.row,
                tile.col,
            )

            # Brief inter-tile pause (skip after last tile).
            if ordinal < len(order) - 1:
                delay = random.uniform(0.4, 0.7)
                await asyncio.sleep(delay)

    def _get_game_frame(self) -> Any | None:
        """Return the discordsays.com Frame object, or None."""
        for f in self._page.frames:
            if "discordsays.com" in (f.url or ""):
                return f
        return None

    async def _click_in_frame(self, local_x: float, local_y: float) -> None:
        """Dispatch a full pointer+mouse click sequence inside the game iframe.

        When ``page.mouse.click()`` at viewport coordinates fails to reach
        game UI elements (buttons rendered on a canvas inside a cross-origin
        iframe), this helper dispatches synthetic pointer and mouse events
        directly in the iframe's JavaScript context at *iframe-local*
        coordinates.  This bypasses any outer-page overlays or event-capture
        layers that might intercept viewport-level clicks.

        Args:
            local_x: X coordinate relative to the iframe's top-left corner.
            local_y: Y coordinate relative to the iframe's top-left corner.
        """
        game_frame = self._get_game_frame()
        if game_frame is None:
            raise PlacementError("Game frame not found for in-frame click")

        await game_frame.evaluate(
            """([x, y]) => {
                const el = document.elementFromPoint(x, y) || document.body;
                const opts = {clientX: x, clientY: y, bubbles: true,
                              cancelable: true, pointerId: 1,
                              pointerType: 'mouse', button: 0};
                el.dispatchEvent(new PointerEvent('pointerdown', opts));
                el.dispatchEvent(new MouseEvent('mousedown',
                    {clientX: x, clientY: y, bubbles: true, button: 0}));
                el.dispatchEvent(new PointerEvent('pointerup', opts));
                el.dispatchEvent(new MouseEvent('mouseup',
                    {clientX: x, clientY: y, bubbles: true, button: 0}));
                el.dispatchEvent(new MouseEvent('click',
                    {clientX: x, clientY: y, bubbles: true, button: 0}));
            }""",
            [local_x, local_y],
        )

    async def _click_confirm(self, mapper: CoordMapper) -> None:
        """Click the confirm button to submit the placed word.

        Uses viewport-level ``page.mouse.click`` — the same mechanism that
        ``_drag_tile`` uses to place tiles on the board.  Synthetic JS
        dispatch (``_click_in_frame``) silently "succeeds" on canvas-rendered
        buttons without actually triggering the game's event handlers, so we
        avoid it here.

        Args:
            mapper: ``CoordMapper`` instance for current canvas dimensions.
        """
        cx, cy = mapper.confirm_btn_px()
        vx, vy = jitter(cx, cy)
        logger.info("Clicking confirm/PLAY button at ({:.1f}, {:.1f})", vx, vy)
        await self._page.mouse.click(vx, vy)

    async def _wait_for_acceptance(self, mapper: CoordMapper) -> bool:
        """Poll the turn state to detect word acceptance, retrying PLAY once.

        After clicking confirm, the game needs time to validate and animate.
        Polls up to ``_ACCEPT_POLLS`` times.  If no state change is detected
        after half the polls, re-clicks the PLAY button once (the first click
        may have been consumed by an overlay or event handler) and continues
        polling for the remaining attempts.

        Args:
            mapper: ``CoordMapper`` for re-clicking if the first attempt failed.

        Returns:
            ``True`` if the word was accepted (turn ended).
            ``False`` if still ``"my_turn"`` after all polls (word rejected).
        """
        retry_at = _ACCEPT_POLLS // 2  # re-click PLAY halfway through

        for attempt in range(1, _ACCEPT_POLLS + 1):
            await asyncio.sleep(_ACCEPT_POLL_INTERVAL_S)
            img_bytes = await capture_canvas(self._page, render_wait=False)
            state = classify_frame(img_bytes)
            logger.debug("Post-confirm poll {}/{}: {}", attempt, _ACCEPT_POLLS, state)
            if state != "my_turn":
                return True

            # Retry PLAY click once, halfway through the poll window.
            if attempt == retry_at:
                logger.debug("Re-clicking PLAY (retry after {} polls)", retry_at)
                await self._click_confirm(mapper)

        return False

    async def _save_debug_screenshot(self, label: str) -> None:
        """Capture and save a debug screenshot to debug/tile_placer/.

        Saves a PNG named ``{label}.png`` for diagnostic inspection.  Failures
        are logged at WARNING and never propagate — this is best-effort.

        Args:
            label: Short descriptive name for the screenshot file (no extension).
        """
        try:
            _DEBUG_DIR.mkdir(parents=True, exist_ok=True)
            img_bytes = await capture_canvas(self._page, render_wait=False)
            debug_path = _DEBUG_DIR / f"{label}.png"
            debug_path.write_bytes(img_bytes)
            logger.debug("Debug screenshot saved -> {}", debug_path)
        except Exception as exc:
            logger.warning("Debug screenshot '{}' failed: {}", label, exc)

    async def _recall_tiles(
        self,
        mapper: CoordMapper,
        attempt_num: int = 0,
        expected_tiles: int | None = None,
    ) -> None:
        """Click the recall/undo button to return placed tiles to the rack.

        Called after a word rejection so the bot can try a different word.
        Uses viewport-level ``page.mouse.click`` — the same mechanism that
        ``_drag_tile`` uses.  Synthetic JS dispatch silently "succeeds" on
        canvas-rendered buttons without triggering the game's handlers.

        Empirically a single recall click returns one staged tile, so a
        7-tile placement needs at least 7 clicks. Fast successive clicks
        (≤400 ms apart) were observed to be coalesced by the game's input
        handler, so we space them at ≥0.7 s.

        When ``expected_tiles`` is known we click exactly that many times
        plus a small safety margin and skip canvas-diff stability detection
        entirely.  The diff check was unreliable under live play: the bot's
        turn timer and opponent-side UI animate continuously, so the
        per-frame mean pixel diff stays above the 0.15 stability threshold
        even after the rack has fully refilled — the loop consistently hit
        its 10-click cap and burned ~22 s on every rejected word.  At five
        rejections per turn that wasted ~110 s, repeatedly pushing the run
        past the auto-debug 30-min wallclock cap.  Count-based recall is
        deterministic and cuts that to ~7 s.

        Args:
            mapper:         ``CoordMapper`` instance for current canvas dimensions.
            attempt_num:    Current word attempt index (used in the debug filename).
            expected_tiles: Number of tiles staged in the rejected attempt.
                When ``None``, falls back to a fixed safety cap suitable
                for an unknown placement.
        """
        rx, ry = mapper.recall_btn_px()
        if expected_tiles is not None and expected_tiles > 0:
            target_clicks = expected_tiles + 2  # +2 safety for coalesced clicks
        else:
            target_clicks = 9  # generic safety cap (max rack 7 + 2)
        for i in range(target_clicks):
            jx, jy = jitter(rx, ry)
            logger.info(
                "Clicking recall button at ({:.1f}, {:.1f}) (pass {}/{})",
                jx, jy, i + 1, target_clicks,
            )
            await self._page.mouse.click(jx, jy)
            await asyncio.sleep(random.uniform(0.7, 0.9))

        await self._save_debug_screenshot(f"post_recall_attempt{attempt_num}")

    async def clear_stale_placements(self) -> None:
        """Click recall once to clear any uncommitted tiles left on the board.

        Call this at the start of each turn (after poll_turn returns "my_turn"
        but before capturing the board) so that tiles staged by a previous
        attempt — or by the human before autoplay took over — cannot pollute
        the engine's view of the board or block the next move submission.

        Before recalling, we probe for a stuck "Select a letter" dialog (an
        unassigned blank tile from a prior run will leave this modal open)
        and dismiss it — the dialog otherwise swallows the RECALL click and
        the subsequent vision read sees its letter grid as phantom board
        tiles.

        Safe to call when the board is already clean: the recall click on an
        empty placement set is a no-op from the game's perspective.
        """
        try:
            bbox = await self._get_canvas_bbox()
        except Exception as exc:
            logger.warning("clear_stale_placements: cannot get bbox ({}) — skipping", exc)
            return

        try:
            probe_bytes = await capture_canvas(self._page, render_wait=False)
            if _is_blank_dialog_open(probe_bytes):
                logger.warning(
                    "clear_stale_placements: 'Select a letter' dialog detected "
                    "— assigning 'A' to the stuck blank tile so recall can run"
                )
                self._bbox = bbox  # viewport-click fallback needs a bbox stash
                await self._dismiss_blank_letter_dialog("A")
                await asyncio.sleep(0.5)
        except Exception as exc:
            logger.warning(
                "clear_stale_placements: dialog probe failed ({}) — continuing to recall",
                exc,
            )

        mapper = CoordMapper(bbox)
        rx, ry = mapper.recall_btn_px()
        # Click recall a fixed small number of times.  We previously waited
        # for the canvas to "stabilise" between clicks but live play has
        # continuous animation (turn timer, opponent UI) that pushes every
        # adjacent-frame diff above the 0.15 threshold, so the loop always
        # ran the full 10 clicks and burned ~20 s every turn.  At the start
        # of a turn the board is normally clean — at most a handful of
        # stale tiles from a manual intervention or crashed prior run, so
        # capping at 4 covers any realistic situation while keeping the
        # cost bounded.
        MAX_PASSES = 4
        for i in range(MAX_PASSES):
            jx, jy = jitter(rx, ry)
            logger.info(
                "Pre-turn recall click at ({:.1f}, {:.1f}) (pass {}/{})",
                jx, jy, i + 1, MAX_PASSES,
            )
            try:
                await self._page.mouse.click(jx, jy)
            except Exception as exc:
                logger.warning("clear_stale_placements: recall click failed: {}", exc)
                return
            await asyncio.sleep(random.uniform(0.7, 0.9))

    async def _tile_swap(self, mapper: CoordMapper) -> None:
        """Click the tile swap button as a fallback when no valid words can be placed.

        Used after MAX_WORD_RETRIES word attempts have all been rejected. Logs
        a warning since tile swap sacrifices a turn.

        Args:
            mapper: ``CoordMapper`` instance for current canvas dimensions.
        """
        sx, sy = mapper.swap_btn_px()
        jx, jy = jitter(sx, sy)
        logger.warning(
            "Falling back to tile swap at ({:.1f}, {:.1f}) — no valid words accepted after {} attempts",
            jx,
            jy,
            MAX_WORD_RETRIES,
        )
        await self._page.mouse.click(jx, jy)

    async def place_move(
        self,
        moves: list[Move],
        rack: list[str],
        swap_on_fail: bool = True,
    ) -> Move | None:
        """Orchestrate the full tile placement + confirmation flow.

        Iterates through up to ``MAX_WORD_RETRIES`` candidate moves (sorted
        best-first by the caller). For each move:

        1. Drag tiles onto the board via ``place_tiles()``.
        2. Click the confirm button.
        3. Wait 1-2 seconds and check acceptance via ``classify_frame()``.
        4. If accepted: log success and return ``True``.
        5. If rejected: log rejection, recall tiles, try the next move.

        If all word attempts are exhausted without acceptance, performs a tile
        swap as a last resort (unless ``swap_on_fail`` is ``False``) and
        returns ``False``.

        Args:
            moves: Candidate ``Move`` objects sorted by score descending (best
                first). Typically from ``find_all_moves()`` or a ranked subset.
                This method does not call the engine — the caller provides the
                list.
            rack: Current rack as a list of letter strings (``'?'`` for blank).
            swap_on_fail: If ``True`` (default), perform a tile swap when all
                word attempts fail.  If ``False``, return ``False`` without
                swapping — the caller can retry with fresh vision data.

        Returns:
            The accepted ``Move`` if a word was accepted; ``None`` if all
            attempts failed. (Truthy/falsy semantics are preserved, so
            ``if accepted:`` still works for callers.)
        """
        # Drop candidates whose word is already blacklisted from prior runs,
        # and dedupe repeated .word entries (the engine emits the same word
        # at multiple anchor positions — once the game rejects it the first
        # placement, retrying another placement of the same word is wasted
        # work that also feeds the stuck-on-my_turn failure mode).
        deduped: list[Move] = []
        seen_words: set[str] = set()
        skipped_blacklisted = 0
        for m in moves:
            key = m.word.lower()
            if key in seen_words:
                continue
            if rejected_words.is_rejected(key):
                skipped_blacklisted += 1
                continue
            seen_words.add(key)
            deduped.append(m)
        if skipped_blacklisted:
            logger.info(
                "place_move: skipped {} candidate(s) already on the rejection blacklist",
                skipped_blacklisted,
            )

        attempt_limit = min(len(deduped), MAX_WORD_RETRIES)

        for attempt_num, move in enumerate(deduped[:attempt_limit], start=1):
            logger.info(
                "Word attempt {}/{}: '{}' (score={})",
                attempt_num,
                attempt_limit,
                move.word,
                move.score,
            )

            try:
                await self.place_tiles(move, rack)
            except CoordinateDriftError as exc:
                # First tile failed twice with the "click missed cell"
                # signature — every other candidate from this vision pass
                # shares the same coordinate frame and will fail the same
                # way. Recall whatever (if anything) staged and bail out so
                # the orchestrator re-visions before trying again.
                logger.error(
                    "Coordinate drift on '{}' (attempt {}/{}): {} — aborting "
                    "candidate list to trigger re-vision",
                    move.word, attempt_num, attempt_limit, exc,
                )
                try:
                    bbox = await self._get_canvas_bbox()
                    mapper = CoordMapper(bbox)
                    await self._recall_tiles(mapper, attempt_num=attempt_num)
                except Exception as recall_exc:
                    logger.warning(
                        "Recall after CoordinateDriftError failed: {}", recall_exc,
                    )
                return None
            except (PlacementError, ValueError) as exc:
                logger.error(
                    "Tile placement failed for '{}' (attempt {}): {}",
                    move.word,
                    attempt_num,
                    exc,
                )
                # Attempt recall before moving on to next word. We don't
                # know how many tiles actually landed (the failure may have
                # been mid-placement), so let _recall_tiles use its generic
                # safety cap.
                try:
                    bbox = await self._get_canvas_bbox()
                    mapper = CoordMapper(bbox)
                    await self._recall_tiles(mapper, attempt_num=attempt_num)
                except Exception as recall_exc:
                    logger.warning("Recall after PlacementError also failed: {}", recall_exc)
                continue

            # Tiles placed — save diagnostic screenshot, then brief settle
            # before clicking confirm.  The pre-PLAY screenshot lets us verify
            # that tiles are at the correct board cells before submission.
            await self._save_debug_screenshot(f"pre_play_attempt{attempt_num}_{move.word}")
            await asyncio.sleep(random.uniform(0.4, 0.8))
            bbox = await self._get_canvas_bbox()
            self._bbox = bbox  # stash for _click_confirm in-frame strategy
            mapper = CoordMapper(bbox)
            await self._click_confirm(mapper)

            accepted = await self._wait_for_acceptance(mapper)

            if accepted:
                logger.info(
                    "Word '{}' accepted! (score={}, attempt {}/{})",
                    move.word,
                    move.score,
                    attempt_num,
                    attempt_limit,
                )
                return move

            logger.info(
                "Word '{}' rejected (attempt {}/{}) — recalling tiles",
                move.word,
                attempt_num,
                attempt_limit,
            )
            rejected_words.add(move.word)
            await self._recall_tiles(
                mapper,
                attempt_num=attempt_num,
                expected_tiles=len(move.rack_tiles_consumed()),
            )

        # All word attempts exhausted.
        if swap_on_fail:
            logger.warning(
                "All {} word attempt(s) failed — performing tile swap fallback",
                attempt_limit,
            )
            bbox = await self._get_canvas_bbox()
            mapper = CoordMapper(bbox)
            await self._tile_swap(mapper)
        else:
            logger.warning(
                "All {} word attempt(s) failed — returning to caller for re-vision",
                attempt_limit,
            )
        return None
