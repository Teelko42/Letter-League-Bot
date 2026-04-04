"""Tests for TilePlacer (Phase B1).

All Playwright interactions are mocked — no real browser needed.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock

import numpy as np
import cv2
import pytest

from src.browser.tile_placer import CoordMapper, PlacementError, TilePlacer
from src.engine.models import Move, ScoreBreakdown, TileUse


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BBOX = {"x": 0, "y": 0, "width": 1057, "height": 768}


def _make_move(word: str, direction: str, tiles: list[TileUse]) -> Move:
    return Move(
        word=word,
        start_row=tiles[0].row if tiles else 0,
        start_col=tiles[0].col if tiles else 0,
        direction=direction,
        tiles_used=tiles,
        score_breakdown=ScoreBreakdown(
            base_letter_sum=10, word_multiplier=1, total=10
        ),
        score=10,
    )


def _h_tiles(letters: str, row: int, start_col: int) -> list[TileUse]:
    """Create horizontal rack tiles."""
    return [
        TileUse(row=row, col=start_col + i, letter=ch, is_blank=False, from_rack=True)
        for i, ch in enumerate(letters)
    ]


def _v_tiles(letters: str, start_row: int, col: int) -> list[TileUse]:
    """Create vertical rack tiles."""
    return [
        TileUse(row=start_row + i, col=col, letter=ch, is_blank=False, from_rack=True)
        for i, ch in enumerate(letters)
    ]


def _make_different_png() -> bytes:
    """Return a PNG whose pixels differ from a black image."""
    img = np.full((50, 50, 3), 128, dtype=np.uint8)
    _, buf = cv2.imencode(".png", img)
    return buf.tobytes()


def _make_black_png() -> bytes:
    img = np.zeros((50, 50, 3), dtype=np.uint8)
    _, buf = cv2.imencode(".png", img)
    return buf.tobytes()


def _make_placer() -> tuple[TilePlacer, MagicMock]:
    page = MagicMock()
    page.mouse = AsyncMock()
    page.mouse.move = AsyncMock()
    page.mouse.down = AsyncMock()
    page.mouse.up = AsyncMock()
    page.mouse.click = AsyncMock()
    page.keyboard = AsyncMock()
    page.keyboard.press = AsyncMock()
    return TilePlacer(page), page


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestPlaceTiles:
    @pytest.mark.asyncio
    async def test_place_tiles_calls_drag_in_order(self):
        """Horizontal tiles are placed left-to-right by column."""
        placer, page = _make_placer()
        tiles = _h_tiles("CAB", row=5, start_col=3)
        move = _make_move("CAB", "H", tiles)

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", new_callable=AsyncMock, return_value=True),
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer.place_tiles(move, ["C", "A", "B"])

        # 3 tiles = 6 clicks (2 clicks per tile: select + place)
        assert page.mouse.click.call_count == 6

    @pytest.mark.asyncio
    async def test_place_tiles_vertical_order(self):
        """Vertical tiles are placed top-to-bottom by row."""
        placer, page = _make_placer()
        tiles = _v_tiles("DOG", start_row=2, col=5)
        move = _make_move("DOG", "V", tiles)

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", new_callable=AsyncMock, return_value=True),
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer.place_tiles(move, ["D", "O", "G"])

        assert page.mouse.click.call_count == 6

    @pytest.mark.asyncio
    async def test_place_tiles_single_click_pair_per_tile(self):
        """Each tile uses exactly one click-select + click-place (no verification)."""
        placer, page = _make_placer()
        tiles = [TileUse(row=0, col=0, letter="A", is_blank=False, from_rack=True)]
        move = _make_move("A", "H", tiles)

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer.place_tiles(move, ["A"])

        # 1 tile = 2 clicks (select rack tile + place on board)
        assert page.mouse.click.call_count == 2

    @pytest.mark.asyncio
    async def test_place_tiles_no_rack_tiles_skips(self):
        """Move with no rack tiles consumed results in no drags."""
        placer, page = _make_placer()
        board_tiles = [TileUse(row=0, col=0, letter="A", is_blank=False, from_rack=False)]
        move = _make_move("A", "H", board_tiles)

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
        ):
            await placer.place_tiles(move, ["B", "C"])

        assert page.mouse.down.call_count == 0


class TestPlaceMove:
    @pytest.mark.asyncio
    async def test_place_move_accepted_first_try(self):
        placer, page = _make_placer()
        tiles = _h_tiles("AB", row=0, start_col=0)
        move = _make_move("AB", "H", tiles)

        with (
            patch.object(placer, "place_tiles", new_callable=AsyncMock),
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_click_confirm", new_callable=AsyncMock),
            patch.object(placer, "_wait_for_acceptance", new_callable=AsyncMock, return_value=True),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await placer.place_move([move], ["A", "B"])

        assert result is True

    @pytest.mark.asyncio
    async def test_place_move_rejected_then_accepted(self):
        placer, page = _make_placer()
        tiles1 = _h_tiles("AB", row=0, start_col=0)
        tiles2 = _h_tiles("CD", row=1, start_col=0)
        move1 = _make_move("AB", "H", tiles1)
        move2 = _make_move("CD", "H", tiles2)

        with (
            patch.object(placer, "place_tiles", new_callable=AsyncMock),
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_click_confirm", new_callable=AsyncMock),
            patch.object(placer, "_wait_for_acceptance", new_callable=AsyncMock, side_effect=[False, True]),
            patch.object(placer, "_recall_tiles", new_callable=AsyncMock),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await placer.place_move([move1, move2], ["A", "B", "C", "D"])

        assert result is True

    @pytest.mark.asyncio
    async def test_place_move_all_rejected_tile_swap(self):
        placer, page = _make_placer()
        tiles = _h_tiles("AB", row=0, start_col=0)
        move = _make_move("AB", "H", tiles)

        with (
            patch.object(placer, "place_tiles", new_callable=AsyncMock),
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_click_confirm", new_callable=AsyncMock),
            patch.object(placer, "_wait_for_acceptance", new_callable=AsyncMock, return_value=False),
            patch.object(placer, "_recall_tiles", new_callable=AsyncMock),
            patch.object(placer, "_tile_swap", new_callable=AsyncMock) as mock_swap,
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await placer.place_move([move], ["A", "B"])

        assert result is False
        mock_swap.assert_called_once()

    @pytest.mark.asyncio
    async def test_place_move_placement_error_continues(self):
        """PlacementError on first move doesn't stop trying the next."""
        placer, page = _make_placer()
        tiles1 = _h_tiles("AB", row=0, start_col=0)
        tiles2 = _h_tiles("CD", row=1, start_col=0)
        move1 = _make_move("AB", "H", tiles1)
        move2 = _make_move("CD", "H", tiles2)

        call_count = 0

        async def place_tiles_side_effect(move, rack):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise PlacementError("drag failed")

        with (
            patch.object(placer, "place_tiles", new_callable=AsyncMock, side_effect=place_tiles_side_effect),
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_click_confirm", new_callable=AsyncMock),
            patch.object(placer, "_wait_for_acceptance", new_callable=AsyncMock, return_value=True),
            patch.object(placer, "_recall_tiles", new_callable=AsyncMock),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await placer.place_move([move1, move2], ["A", "B", "C", "D"])

        assert result is True


class TestGetCanvasBbox:
    @pytest.mark.asyncio
    async def test_canvas_found(self):
        placer, page = _make_placer()

        canvas_locator = AsyncMock()
        canvas_locator.bounding_box = AsyncMock(return_value=BBOX)

        frame_locator = MagicMock()
        locator_mock = MagicMock()
        locator_mock.first = canvas_locator
        frame_locator.locator.return_value = locator_mock
        page.frame_locator.return_value = frame_locator

        result = await placer._get_canvas_bbox()
        assert result == BBOX

    @pytest.mark.asyncio
    async def test_fallback_to_iframe(self):
        placer, page = _make_placer()

        # Canvas locator raises
        canvas_locator = AsyncMock()
        canvas_locator.bounding_box = AsyncMock(side_effect=Exception("no canvas"))
        frame_locator = MagicMock()
        locator_mock = MagicMock()
        locator_mock.first = canvas_locator
        frame_locator.locator.return_value = locator_mock
        page.frame_locator.return_value = frame_locator

        # Iframe fallback returns bbox
        iframe_locator = AsyncMock()
        iframe_locator.bounding_box = AsyncMock(return_value=BBOX)
        page.locator.return_value = iframe_locator

        result = await placer._get_canvas_bbox()
        assert result == BBOX

    @pytest.mark.asyncio
    async def test_both_fail(self):
        placer, page = _make_placer()

        canvas_locator = AsyncMock()
        canvas_locator.bounding_box = AsyncMock(side_effect=Exception("no canvas"))
        frame_locator = MagicMock()
        locator_mock = MagicMock()
        locator_mock.first = canvas_locator
        frame_locator.locator.return_value = locator_mock
        page.frame_locator.return_value = frame_locator

        iframe_locator = AsyncMock()
        iframe_locator.bounding_box = AsyncMock(return_value=None)
        page.locator.return_value = iframe_locator

        with pytest.raises(PlacementError, match="None"):
            await placer._get_canvas_bbox()
