from __future__ import annotations

import asyncio
import random
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

GRID_X0_FRAC = 0.085401    # top-left of cell(0,0) X (fraction of canvas width)
GRID_Y0_FRAC = 0.057552    # top-left of cell(0,0) Y (fraction of canvas height)
CELL_W_FRAC = 0.02889      # one cell width  (fraction of canvas width)  — 27 cols
CELL_H_FRAC = 0.03900      # one cell height (fraction of canvas height) — 19 rows

# Canvas dimensions when the grid constants above were calibrated.
# Used to compute the game render area inside the iframe when the <canvas>
# element cannot be found (the game maintains this aspect ratio).
CALIBRATION_CANVAS_W = 1057
CALIBRATION_CANVAS_H = 768
RACK_Y_FRAC = 0.932836     # rack row vertical center — PLACEHOLDER pending live game
RACK_X0_FRAC = 0.400781    # first rack tile center — PLACEHOLDER pending live game
RACK_TILE_STEP_FRAC = 0.032531  # spacing between rack tile centers — PLACEHOLDER
CONFIRM_X_FRAC = 0.499024  # PLAY button center X — PLACEHOLDER pending live game
CONFIRM_Y_FRAC = 0.858209  # PLAY button center Y — PLACEHOLDER pending live game

MAX_WORD_RETRIES = 5        # max different words to try before tile swap
RECALL_X_FRAC = 0.416396   # SWAP button X — doubles as recall when tiles placed (fraction of canvas width)
RECALL_Y_FRAC = 0.858209   # SWAP button Y (fraction of canvas height)
SWAP_X_FRAC = 0.416396     # SWAP button X for tile swap fallback (fraction of canvas width)
SWAP_Y_FRAC = 0.858209     # SWAP button Y (fraction of canvas height)


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

        Args:
            row: Zero-based row index on the board.
            col: Zero-based column index on the board.

        Returns:
            ``(x, y)`` viewport pixel coordinates.
        """
        x = self._bbox["x"] + (GRID_X0_FRAC + col * CELL_W_FRAC) * self._bbox["width"]
        y = self._bbox["y"] + (GRID_Y0_FRAC + row * CELL_H_FRAC) * self._bbox["height"]
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

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _get_canvas_bbox(self) -> dict:
        """Retrieve the game element's bounding box from the iframe.

        Tries the ``<canvas>`` element first; falls back to the iframe
        element and computes the game render area within it using the
        calibration aspect ratio.

        The Letter League game renders at a fixed aspect ratio
        (CALIBRATION_CANVAS_W × CALIBRATION_CANVAS_H).  When the iframe is
        wider or taller than that ratio, the game is centered with empty
        margins (pillarbox / letterbox).  The fractional grid constants are
        relative to the game area, not the full iframe, so we must return
        the game-area bounding box.

        Returns:
            Bounding box dict with keys ``x``, ``y``, ``width``, ``height``.

        Raises:
            PlacementError: If the bounding box is ``None`` (iframe not found).
        """
        # Try canvas inside the iframe first.
        try:
            bbox = await (
                self._page
                .frame_locator('iframe[src*="discordsays.com"]')
                .locator("canvas")
                .first
                .bounding_box(timeout=5_000)
            )
            if bbox is not None:
                return bbox
        except Exception:
            pass

        # Fallback: use the iframe element, then compute the game area.
        iframe_bbox = await (
            self._page
            .locator('iframe[src*="discordsays.com"]')
            .bounding_box(timeout=10_000)
        )
        if iframe_bbox is None:
            raise PlacementError(
                "Canvas bounding box is None — iframe or canvas not found."
            )

        # If the iframe matches the calibration aspect ratio (within 5%),
        # use it directly — the game fills the full iframe.
        cal_aspect = CALIBRATION_CANVAS_W / CALIBRATION_CANVAS_H
        iframe_aspect = iframe_bbox["width"] / iframe_bbox["height"]

        if abs(iframe_aspect - cal_aspect) / cal_aspect < 0.05:
            logger.debug(
                "Iframe aspect matches calibration — using iframe bbox directly "
                "({:.0f}x{:.0f})",
                iframe_bbox["width"],
                iframe_bbox["height"],
            )
            return iframe_bbox

        # Aspect ratios differ — compute the game render area within the
        # iframe, maintaining the calibration aspect ratio.
        if iframe_aspect > cal_aspect:
            # Iframe wider than game → pillarbox (centered horizontally)
            game_h = iframe_bbox["height"]
            game_w = game_h * cal_aspect
            x_offset = (iframe_bbox["width"] - game_w) / 2
            game_bbox = {
                "x": iframe_bbox["x"] + x_offset,
                "y": iframe_bbox["y"],
                "width": game_w,
                "height": game_h,
            }
        else:
            # Iframe taller than game → letterbox (centered vertically)
            game_w = iframe_bbox["width"]
            game_h = game_w / cal_aspect
            y_offset = (iframe_bbox["height"] - game_h) / 2
            game_bbox = {
                "x": iframe_bbox["x"],
                "y": iframe_bbox["y"] + y_offset,
                "width": game_w,
                "height": game_h,
            }

        logger.debug(
            "No canvas element — computed game area within iframe: "
            "iframe=({:.0f}x{:.0f}) game=({:.0f}x{:.0f} @ x={:.0f},y={:.0f})",
            iframe_bbox["width"],
            iframe_bbox["height"],
            game_bbox["width"],
            game_bbox["height"],
            game_bbox["x"],
            game_bbox["y"],
        )
        return game_bbox

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
        await asyncio.sleep(0.25)
        await self._page.mouse.click(to_x, to_y)

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

            # Place tile via click-select, click-place.  Skip per-tile
            # screenshot verification — the confirm/reject cycle already
            # catches misplacements and the overhead (~1.2s per tile) is
            # too expensive for a timed game.
            await self._drag_tile(rx, ry, bx, by)

            logger.info(
                "Tile '{}' placed at ({},{})",
                tile.letter,
                tile.row,
                tile.col,
            )

            # Brief inter-tile pause (skip after last tile).
            if ordinal < len(order) - 1:
                delay = random.uniform(0.15, 0.4)
                await asyncio.sleep(delay)

    async def _click_confirm(self, mapper: CoordMapper) -> None:
        """Click the confirm button with jitter to submit the placed word.

        Uses ``page.mouse.click`` (teleport, not drag) as confirm is a simple
        button click rather than a drag-and-drop interaction.

        Args:
            mapper: ``CoordMapper`` instance for current canvas dimensions.
        """
        cx, cy = jitter(*mapper.confirm_btn_px())
        logger.info("Clicking confirm button at ({:.1f}, {:.1f})", cx, cy)
        await self._page.mouse.click(cx, cy)

    async def _wait_for_acceptance(self) -> bool:
        """Wait 1-2 seconds then check if the word was accepted by the game.

        Captures a fresh screenshot and calls ``classify_frame()`` to determine
        the current turn state. If the state is not ``"my_turn"``, the bot's
        turn has ended (word was accepted or the game moved on).

        Returns:
            ``True`` if the word was accepted (turn ended).
            ``False`` if still ``"my_turn"`` (word was rejected by the game).
        """
        delay = random.uniform(0.3, 0.7)
        logger.debug("Waiting {:.2f}s for server to process word submission", delay)
        await asyncio.sleep(delay)

        img_bytes = await capture_canvas(self._page)
        state = classify_frame(img_bytes)
        logger.debug("Post-confirm turn state: {}", state)
        return state != "my_turn"

    async def _recall_tiles(self, mapper: CoordMapper) -> None:
        """Click the recall/undo button to return placed tiles to the rack.

        Called after a word rejection so the bot can try a different word.
        Waits briefly after clicking for the animation to complete.

        Args:
            mapper: ``CoordMapper`` instance for current canvas dimensions.
        """
        rx, ry = jitter(*mapper.recall_btn_px())
        logger.info("Clicking recall button at ({:.1f}, {:.1f}) to clear placed tiles", rx, ry)
        await self._page.mouse.click(rx, ry)
        await asyncio.sleep(random.uniform(0.3, 0.5))

    async def _tile_swap(self, mapper: CoordMapper) -> None:
        """Click the tile swap button as a fallback when no valid words can be placed.

        Used after MAX_WORD_RETRIES word attempts have all been rejected. Logs
        a warning since tile swap sacrifices a turn.

        Args:
            mapper: ``CoordMapper`` instance for current canvas dimensions.
        """
        sx, sy = jitter(*mapper.swap_btn_px())
        logger.warning(
            "Falling back to tile swap at ({:.1f}, {:.1f}) — no valid words accepted after {} attempts",
            sx,
            sy,
            MAX_WORD_RETRIES,
        )
        await self._page.mouse.click(sx, sy)

    async def place_move(self, moves: list[Move], rack: list[str]) -> bool:
        """Orchestrate the full tile placement + confirmation flow.

        Iterates through up to ``MAX_WORD_RETRIES`` candidate moves (sorted
        best-first by the caller). For each move:

        1. Drag tiles onto the board via ``place_tiles()``.
        2. Click the confirm button.
        3. Wait 1-2 seconds and check acceptance via ``classify_frame()``.
        4. If accepted: log success and return ``True``.
        5. If rejected: log rejection, recall tiles, try the next move.

        If all word attempts are exhausted without acceptance, performs a tile
        swap as a last resort and returns ``False``.

        PlacementError exceptions raised during ``place_tiles()`` are caught
        per-move — the bot logs the error, attempts recall, and continues to
        the next candidate move. If the final attempt also fails with
        PlacementError, execution falls through to tile swap.

        Args:
            moves: Candidate ``Move`` objects sorted by score descending (best
                first). Typically from ``find_all_moves()`` or a ranked subset.
                This method does not call the engine — the caller provides the
                list.
            rack: Current rack as a list of letter strings (``'?'`` for blank).

        Returns:
            ``True`` if a word was accepted; ``False`` if tile swap was used.
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
            except PlacementError as exc:
                logger.error(
                    "PlacementError during tile drag for '{}' (attempt {}): {}",
                    move.word,
                    attempt_num,
                    exc,
                )
                # Attempt recall before moving on to next word.
                try:
                    bbox = await self._get_canvas_bbox()
                    mapper = CoordMapper(bbox)
                    await self._recall_tiles(mapper)
                except Exception as recall_exc:
                    logger.warning("Recall after PlacementError also failed: {}", recall_exc)
                continue

            # Tiles placed — click confirm and wait for server response.
            bbox = await self._get_canvas_bbox()
            mapper = CoordMapper(bbox)
            await self._click_confirm(mapper)

            accepted = await self._wait_for_acceptance()

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
            await self._recall_tiles(mapper)

        # All word attempts exhausted — fall back to tile swap.
        logger.warning(
            "All {} word attempt(s) failed — performing tile swap fallback",
            attempt_limit,
        )
        bbox = await self._get_canvas_bbox()
        mapper = CoordMapper(bbox)
        await self._tile_swap(mapper)
        return False
