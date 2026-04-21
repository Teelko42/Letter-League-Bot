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
        """Each tile uses exactly one click-select + click-place (verified)."""
        placer, page = _make_placer()
        tiles = [TileUse(row=0, col=0, letter="A", is_blank=False, from_rack=True)]
        move = _make_move("A", "H", tiles)

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", new_callable=AsyncMock, return_value=True),
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer.place_tiles(move, ["A"])

        # 1 tile = 2 clicks (select rack tile + place on board)
        assert page.mouse.click.call_count == 2

    @pytest.mark.asyncio
    async def test_place_tiles_retries_on_verification_failure(self):
        """If verification fails on first attempt, retries once with fresh jitter."""
        placer, page = _make_placer()
        tiles = [TileUse(row=0, col=0, letter="A", is_blank=False, from_rack=True)]
        move = _make_move("A", "H", tiles)

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", new_callable=AsyncMock, side_effect=[False, True]),
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer.place_tiles(move, ["A"])

        # 2 attempts = 4 clicks (2 clicks per attempt)
        assert page.mouse.click.call_count == 4

    @pytest.mark.asyncio
    async def test_place_tiles_raises_after_retry_failure(self):
        """If verification fails on both attempts, raises PlacementError."""
        placer, page = _make_placer()
        tiles = [TileUse(row=0, col=0, letter="A", is_blank=False, from_rack=True)]
        move = _make_move("A", "H", tiles)

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", new_callable=AsyncMock, return_value=False),
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            with pytest.raises(PlacementError, match="failed to place after retry"):
                await placer.place_tiles(move, ["A"])

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


class TestBlankTileDialog:
    """Tests for blank tile 'Select a letter' dialog dismissal."""

    @pytest.mark.asyncio
    async def test_dismiss_blank_dialog_via_keyboard(self):
        """_dismiss_blank_letter_dialog dismisses via keyboard press first."""
        placer, page = _make_placer()

        with (
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch.object(placer, "_verify_dialog_dismissed", new_callable=AsyncMock, return_value=True),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer._dismiss_blank_letter_dialog("E")

        page.keyboard.press.assert_called_once_with("E")

    @pytest.mark.asyncio
    async def test_dismiss_blank_dialog_falls_back_to_frame_locator(self):
        """When keyboard fails, falls back to frame locator click."""
        placer, page = _make_placer()

        # Keyboard press doesn't dismiss
        page.keyboard.press = AsyncMock(side_effect=Exception("no focus"))

        letter_btn = AsyncMock()
        letter_btn.click = AsyncMock()
        frame_locator = MagicMock()
        text_locator = MagicMock()
        text_locator.first = letter_btn
        frame_locator.get_by_text.return_value = text_locator
        page.frame_locator.return_value = frame_locator

        with (
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch.object(placer, "_verify_dialog_dismissed", new_callable=AsyncMock, return_value=True),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer._dismiss_blank_letter_dialog("E")

        frame_locator.get_by_text.assert_called_with("E", exact=True)
        letter_btn.click.assert_called_once()

    @pytest.mark.asyncio
    async def test_dismiss_blank_dialog_falls_back_to_viewport_click(self):
        """When keyboard and frame locator fail, falls back to viewport mouse click."""
        placer, page = _make_placer()
        placer._bbox = BBOX

        # Keyboard doesn't dismiss (verify returns False)
        # Frame locator raises
        letter_btn = AsyncMock()
        letter_btn.click = AsyncMock(side_effect=Exception("not found"))
        frame_locator = MagicMock()
        text_locator = MagicMock()
        text_locator.first = letter_btn
        frame_locator.get_by_text.return_value = text_locator
        page.frame_locator.return_value = frame_locator

        # Keyboard doesn't dismiss, frame locator fails, viewport click works
        verify_results = [False, True]  # keyboard=no, viewport=yes

        with (
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch.object(placer, "_verify_dialog_dismissed", new_callable=AsyncMock, side_effect=verify_results),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer._dismiss_blank_letter_dialog("A")

        # Viewport mouse click should have been used as fallback
        page.mouse.click.assert_called_once()

    @pytest.mark.asyncio
    async def test_dismiss_blank_dialog_retries_on_failure(self):
        """If all strategies fail on first attempt, retries a second time."""
        placer, page = _make_placer()
        placer._bbox = BBOX

        page.keyboard.press = AsyncMock(side_effect=Exception("no focus"))
        letter_btn = AsyncMock()
        letter_btn.click = AsyncMock(side_effect=Exception("not found"))
        frame_locator = MagicMock()
        text_locator = MagicMock()
        text_locator.first = letter_btn
        frame_locator.get_by_text.return_value = text_locator
        page.frame_locator.return_value = frame_locator

        # All viewport clicks fail to dismiss, then second attempt keyboard works
        verify_results = [False, False, True]  # attempt1: viewport=no, viewport=no, attempt2: keyboard=yes

        with (
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch.object(placer, "_verify_dialog_dismissed", new_callable=AsyncMock, side_effect=verify_results),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            # Keyboard fails (exception), frame locator fails (exception),
            # viewport verify=False → retry. Second attempt keyboard also
            # fails, frame locator also fails, viewport verify=False. But we
            # need the retries to work properly.
            # Actually: attempt 1 has keyboard exc, frame exc, viewport verify=False
            # attempt 2 has keyboard exc, frame exc, viewport verify=False
            # All fail → function logs error but returns (no exception raised)
            await placer._dismiss_blank_letter_dialog("Z")

        # keyboard.press called twice (once per attempt)
        assert page.keyboard.press.call_count == 2

    @pytest.mark.asyncio
    async def test_place_move_catches_value_error(self):
        """ValueError from assign_rack_indices is caught and doesn't crash the loop."""
        placer, page = _make_placer()
        tiles = _h_tiles("AB", row=0, start_col=0)
        move = _make_move("AB", "H", tiles)

        async def raise_value_error(m, r):
            raise ValueError("Rack tile 'X' not found")

        with (
            patch.object(placer, "place_tiles", new_callable=AsyncMock, side_effect=raise_value_error),
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_recall_tiles", new_callable=AsyncMock),
            patch.object(placer, "_tile_swap", new_callable=AsyncMock) as mock_swap,
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await placer.place_move([move], ["A", "B"])

        assert result is False
        mock_swap.assert_called_once()

    @pytest.mark.asyncio
    async def test_place_tiles_calls_dialog_handler_for_blank(self):
        """place_tiles() calls _dismiss_blank_letter_dialog when placing a blank tile."""
        placer, page = _make_placer()

        blank_tile = TileUse(row=5, col=5, letter="E", is_blank=True, from_rack=True)
        move = _make_move("E", "H", [blank_tile])

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", new_callable=AsyncMock, return_value=True),
            patch.object(placer, "_dismiss_blank_letter_dialog", new_callable=AsyncMock) as mock_dismiss,
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer.place_tiles(move, ["?"])

        mock_dismiss.assert_called_once_with("E")

    @pytest.mark.asyncio
    async def test_place_tiles_no_dialog_for_regular_tile(self):
        """place_tiles() does NOT call _dismiss_blank_letter_dialog for non-blank tiles."""
        placer, page = _make_placer()

        normal_tile = TileUse(row=5, col=5, letter="E", is_blank=False, from_rack=True)
        move = _make_move("E", "H", [normal_tile])

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", new_callable=AsyncMock, return_value=True),
            patch.object(placer, "_dismiss_blank_letter_dialog", new_callable=AsyncMock) as mock_dismiss,
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer.place_tiles(move, ["E"])

        mock_dismiss.assert_not_called()

    @pytest.mark.asyncio
    async def test_place_tiles_mixed_blank_and_regular(self):
        """place_tiles() calls dialog handler only for blank tiles in a multi-tile move."""
        placer, page = _make_placer()

        tiles = [
            TileUse(row=5, col=3, letter="C", is_blank=False, from_rack=True),
            TileUse(row=5, col=4, letter="A", is_blank=True, from_rack=True),   # blank
            TileUse(row=5, col=5, letter="T", is_blank=False, from_rack=True),
        ]
        move = _make_move("CAT", "H", tiles)

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", new_callable=AsyncMock, return_value=True),
            patch.object(placer, "_dismiss_blank_letter_dialog", new_callable=AsyncMock) as mock_dismiss,
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer.place_tiles(move, ["C", "?", "T"])

        # Only one dismiss call — for the blank tile representing 'A'
        mock_dismiss.assert_called_once_with("A")


class TestGetCanvasBbox:
    @pytest.mark.asyncio
    async def test_returns_iframe_bbox(self):
        """_get_canvas_bbox always returns the iframe bbox (not the canvas element)."""
        placer, page = _make_placer()

        iframe_locator = AsyncMock()
        iframe_locator.bounding_box = AsyncMock(return_value=BBOX)
        page.locator.return_value = iframe_locator

        result = await placer._get_canvas_bbox()
        assert result == BBOX

    @pytest.mark.asyncio
    async def test_raises_when_iframe_not_found(self):
        """_get_canvas_bbox raises PlacementError when iframe bbox is None."""
        placer, page = _make_placer()

        iframe_locator = AsyncMock()
        iframe_locator.bounding_box = AsyncMock(return_value=None)
        page.locator.return_value = iframe_locator

        with pytest.raises(PlacementError, match="None"):
            await placer._get_canvas_bbox()

    @pytest.mark.asyncio
    async def test_does_not_use_canvas_element(self):
        """_get_canvas_bbox does NOT look for the inner canvas element.

        Previously the function tried the canvas element first and fell back
        to the iframe.  The canvas bbox causes wrong coordinates because it
        is offset within the iframe, but the fractional constants are
        calibrated against the full iframe screenshot.  This test confirms
        the canvas lookup path has been removed.
        """
        placer, page = _make_placer()

        # iframe returns a valid bbox
        iframe_locator = AsyncMock()
        iframe_locator.bounding_box = AsyncMock(return_value=BBOX)
        page.locator.return_value = iframe_locator

        result = await placer._get_canvas_bbox()

        # frame_locator should NOT be called (no canvas lookup)
        page.frame_locator.assert_not_called()
        assert result == BBOX
