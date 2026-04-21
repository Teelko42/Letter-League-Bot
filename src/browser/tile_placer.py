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
CONFIRM_X_FRAC = 0.499527  # PLAY button center X — calibrated from live 1057x768: x=528 (gray button)
CONFIRM_Y_FRAC = 0.901042  # PLAY button center Y — calibrated from live 1057x768: y=692 (button bar y=681-703)
# NOTE: Previous CONFIRM_Y_FRAC=0.858209 was wrong — calibrated on 1537x670 screenshot, not 1057x768.
# In live 1057x768 frame, 0.858*768=659 lands on game board tiles; correct button bar is at y=681-703.

MAX_WORD_RETRIES = 5        # max different words to try before tile swap

# Acceptance-detection polling: how many times (and how often) to re-check the
# turn state after clicking confirm.  Total wait ≈ polls × interval.
_ACCEPT_POLLS = 4           # number of post-confirm screenshots
_ACCEPT_POLL_INTERVAL_S = 1.0  # seconds between each poll

# Debug screenshot directory — captures pre-PLAY and post-RECALL states.
# Saved to debug/tile_placer/ alongside other debug images.
_DEBUG_DIR = Path("debug/tile_placer")
RECALL_X_FRAC = 0.589404   # RECALL button X — RIGHT of PLAY. Three-button layout: SWAP(0.41) | PLAY(0.50) | RECALL(0.59)
RECALL_Y_FRAC = 0.901042   # RECALL button Y — same button bar row as PLAY (y=692 at 1057x768)
SWAP_X_FRAC = 0.409650     # SWAP button X — LEFT of PLAY (x=433 at 1057x768). NOT the same as RECALL.
SWAP_Y_FRAC = 0.901042     # SWAP button Y (fraction of canvas height)


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------


class PlacementError(Exception):
    """Raised when tile placement fails after retries."""


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

    def confirm_btn_px(self) -> tuple[float, float]:
        """Return viewport pixel coordinates for the confirm button.

        Returns:
            ``(x, y)`` viewport pixel coordinates.
        """
        x = self._bbox["x"] + CONFIRM_X_FRAC * self._bbox["width"]
        y = self._bbox["y"] + CONFIRM_Y_FRAC * self._bbox["height"]
        return x, y

    def recall_btn_px(self) -> tuple[float, float]:
        """Return viewport pixel coordinates for the recall/undo button.

        Clicking this button clears placed tiles from the board back to the
        rack, allowing the bot to retry with a different word.

        Returns:
            ``(x, y)`` viewport pixel coordinates.
        """
        x = self._bbox["x"] + RECALL_X_FRAC * self._bbox["width"]
        y = self._bbox["y"] + RECALL_Y_FRAC * self._bbox["height"]
        return x, y

    def swap_btn_px(self) -> tuple[float, float]:
        """Return viewport pixel coordinates for the tile swap button.

        Clicking this button performs a tile swap when no valid words can be
        placed. Used as a final fallback after MAX_WORD_RETRIES attempts.

        Returns:
            ``(x, y)`` viewport pixel coordinates.
        """
        x = self._bbox["x"] + SWAP_X_FRAC * self._bbox["width"]
        y = self._bbox["y"] + SWAP_Y_FRAC * self._bbox["height"]
        return x, y


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

            # Strategy 3: compute the button's pixel position from the known 7-column
            # alphabetical grid layout and click via viewport mouse.
            COLS = 7
            DIALOG_LEFT_FRAC = 0.32
            DIALOG_RIGHT_FRAC = 0.68
            GRID_TOP_FRAC = 0.36
            GRID_BOTTOM_FRAC = 0.67

            letter_idx = ord(letter) - ord("A")
            col_idx = letter_idx % COLS
            row_idx = letter_idx // COLS

            cell_w = (DIALOG_RIGHT_FRAC - DIALOG_LEFT_FRAC) / COLS
            cell_h = (GRID_BOTTOM_FRAC - GRID_TOP_FRAC) / 4

            frac_x = DIALOG_LEFT_FRAC + (col_idx + 0.5) * cell_w
            frac_y = GRID_TOP_FRAC + (row_idx + 0.5) * cell_h

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

    async def _verify_placement(self, before_bytes: bytes) -> bool:
        """Verify a tile was placed by comparing before/after screenshots.

        Captures a new screenshot and computes the mean absolute pixel
        difference against the pre-drag screenshot. A difference > 0.15
        indicates the canvas changed (tile landed).

        The threshold is deliberately low because a single tile placement only
        affects ~2 small regions (board cell + rack slot) out of the full
        ~1057x768 image, producing a mean diff of roughly 0.3-0.5 even for a
        successful placement.

        Args:
            before_bytes: PNG screenshot bytes captured before the drag.

        Returns:
            ``True`` if the canvas changed (diff > 0.15), ``False`` otherwise
            or if either image fails to decode.
        """
        after_bytes = await capture_canvas(self._page, render_wait=False)

        def _decode(data: bytes) -> np.ndarray | None:
            arr = np.frombuffer(data, dtype=np.uint8)
            return cv2.imdecode(arr, cv2.IMREAD_COLOR)

        before_img = _decode(before_bytes)
        after_img = _decode(after_bytes)

        if before_img is None or after_img is None:
            logger.warning("_verify_placement: image decode failed — treating as unverified")
            return False

        diff = float(np.mean(np.abs(before_img.astype(np.int32) - after_img.astype(np.int32))))
        logger.debug("Placement pixel diff: {:.4f}", diff)
        return diff > 0.15

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def place_tiles(self, move: Move, rack: list[str]) -> None:
        """Place all rack tiles for a move via drag-and-drop.

        Orchestration steps:
          1. Fetch canvas bounding box and build a ``CoordMapper``.
          2. Retrieve rack tiles from the move.
          3. Assign each rack tile to a rack slot index.
          4. Sort placements in word-spelling order (left-to-right for
             horizontal; top-to-bottom for vertical).
          5. For each tile: compute jittered source + target coordinates,
             capture a before screenshot, drag the tile, verify placement.
             Retry once on failure; raise ``PlacementError`` if retry fails.
          6. Sleep 1–3 seconds between placements for human-like pacing.

        Args:
            move: The ``Move`` to execute.
            rack: Current rack as a list of letter strings (``'?'`` for blank).

        Raises:
            PlacementError: If any tile placement fails after one retry.
            ValueError: If rack assignment fails (tile not in rack).
        """
        from src.engine.models import Move as _Move  # noqa: F401 — ensure type available

        bbox = await self._get_canvas_bbox()
        mapper = CoordMapper(bbox)

        rack_tiles: list[TileUse] = move.rack_tiles_consumed()
        if not rack_tiles:
            logger.info("No rack tiles to place for move '{}'", move.word)
            return

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

            # Place tile via click-select, click-place with verification.
            # Capture a before screenshot, drag the tile, then verify the
            # canvas changed.  Retry once on failure with fresh jitter.
            before_bytes = await capture_canvas(self._page, render_wait=False)
            await self._drag_tile(rx, ry, bx, by)
            await asyncio.sleep(0.3)  # Let the game register the placement.

            placed = await self._verify_placement(before_bytes)
            if not placed:
                logger.warning(
                    "Tile '{}' placement not verified — retrying with fresh jitter",
                    tile.letter,
                )
                rx2, ry2 = jitter(*mapper.rack_tile_px(slot_idx))
                bx2, by2 = jitter(*mapper.board_cell_px(tile.row, tile.col))
                before_bytes = await capture_canvas(self._page, render_wait=False)
                await self._drag_tile(rx2, ry2, bx2, by2)
                await asyncio.sleep(0.3)

                placed = await self._verify_placement(before_bytes)
                if not placed:
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

    async def _recall_tiles(self, mapper: CoordMapper, attempt_num: int = 0) -> None:
        """Click the recall/undo button to return placed tiles to the rack.

        Called after a word rejection so the bot can try a different word.
        Uses viewport-level ``page.mouse.click`` — the same mechanism that
        ``_drag_tile`` uses.  Synthetic JS dispatch silently "succeeds" on
        canvas-rendered buttons without triggering the game's handlers.

        The post-click delay is intentionally generous (1.0–1.5 s) — the game
        animates tiles flying back from the board to the rack, and if the next
        placement starts before the animation finishes the game may reject or
        mishandle the subsequent clicks.

        Args:
            mapper:      ``CoordMapper`` instance for current canvas dimensions.
            attempt_num: Current word attempt index (used in the debug filename).
        """
        rx, ry = mapper.recall_btn_px()
        jx, jy = jitter(rx, ry)
        logger.info("Clicking recall button at ({:.1f}, {:.1f}) to clear placed tiles", jx, jy)
        await self._page.mouse.click(jx, jy)

        # Give the game's recall animation time to fully complete before the
        # next placement cycle starts.  0.3-0.5 s was too short in testing.
        await asyncio.sleep(random.uniform(1.0, 1.5))
        await self._save_debug_screenshot(f"post_recall_attempt{attempt_num}")

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
    ) -> bool:
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
            ``True`` if a word was accepted; ``False`` if all attempts failed.
        """
        attempt_limit = min(len(moves), MAX_WORD_RETRIES)

        for attempt_num, move in enumerate(moves[:attempt_limit], start=1):
            logger.info(
                "Word attempt {}/{}: '{}' (score={})",
                attempt_num,
                attempt_limit,
                move.word,
                move.score,
            )

            try:
                await self.place_tiles(move, rack)
            except (PlacementError, ValueError) as exc:
                logger.error(
                    "Tile placement failed for '{}' (attempt {}): {}",
                    move.word,
                    attempt_num,
                    exc,
                )
                # Attempt recall before moving on to next word.
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
                return True

            logger.info(
                "Word '{}' rejected (attempt {}/{}) — recalling tiles",
                move.word,
                attempt_num,
                attempt_limit,
            )
            await self._recall_tiles(mapper, attempt_num=attempt_num)

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
        return False
