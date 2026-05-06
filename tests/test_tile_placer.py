"""Tests for TilePlacer (Phase B1).

All Playwright interactions are mocked — no real browser needed.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock

import numpy as np
import cv2
import pytest

from src.browser.tile_placer import (
    CELL_H_FRAC,
    CELL_W_FRAC,
    CoordinateDriftError,
    CoordMapper,
    GRID_X0_FRAC,
    GRID_Y0_FRAC,
    PlacementError,
    TilePlacer,
    _cell_v_range,
    _check_move_anchors,
)
from src.engine.models import Move, ScoreBreakdown, TileUse


@pytest.fixture(autouse=True)
def _isolate_rejected_words(tmp_path, monkeypatch):
    """Point rejected_words at an empty temp file so test words never appear
    pre-blacklisted from prior real-game runs."""
    from src.engine import rejected_words

    rejected_words.configure(tmp_path / "rejected.txt")
    yield
    # Reset to default after each test
    rejected_words.configure(rejected_words.DEFAULT_PATH)


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


def _make_board_png(tile_cells: set[tuple[int, int]]) -> bytes:
    """Build a synthetic 1545x768 board image with painted tiles at given cells.

    Empty cells are filled with peach (uniform → V_range == 0).  Tile cells
    are painted with a checkerboard of black and white pixels so V_range
    reaches 255 — the classic occupied-cell signature.

    Args:
        tile_cells: Set of (row, col) coordinates that should read as occupied.
    """
    h, w = 768, 1545
    img = np.full((h, w, 3), (210, 230, 250), dtype=np.uint8)  # peach BGR

    for row, col in tile_cells:
        cx = int((GRID_X0_FRAC + (col + 0.5) * CELL_W_FRAC) * w)
        cy = int((GRID_Y0_FRAC + (row + 0.5) * CELL_H_FRAC) * h)
        cw = int(CELL_W_FRAC * w)
        ch = int(CELL_H_FRAC * h)
        x0, x1 = cx - cw // 2, cx + cw // 2
        y0, y1 = cy - ch // 2, cy + ch // 2
        # Paint two horizontal stripes — black on top, white on bottom — so any
        # sample that lands inside the cell sees V values from 0 to 255.
        img[y0 : (y0 + y1) // 2, x0:x1] = (0, 0, 0)
        img[(y0 + y1) // 2 : y1, x0:x1] = (255, 255, 255)

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
    async def test_place_tiles_raises_coordinate_drift_on_first_tile(self):
        """First-tile failure with drift signature (high global, ~zero local)
        on both attempts raises CoordinateDriftError, not plain PlacementError."""
        placer, page = _make_placer()
        tiles = [TileUse(row=0, col=0, letter="A", is_blank=False, from_rack=True)]
        move = _make_move("A", "H", tiles)

        async def fake_verify(*args, **kwargs):
            placer._last_global_diff = 0.95
            placer._last_local_diff = 0.0
            return False

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", side_effect=fake_verify),
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            with pytest.raises(CoordinateDriftError, match="do not match the live board"):
                await placer.place_tiles(move, ["A"])

    @pytest.mark.asyncio
    async def test_place_tiles_no_drift_when_global_low(self):
        """Verifier failure with low global diff is *not* drift — the click
        was a no-op (e.g. dialog blocking it). Falls through to plain
        PlacementError so the orchestrator continues with other candidates."""
        placer, page = _make_placer()
        tiles = [TileUse(row=0, col=0, letter="A", is_blank=False, from_rack=True)]
        move = _make_move("A", "H", tiles)

        async def fake_verify(*args, **kwargs):
            placer._last_global_diff = 0.05  # below the 0.10 drift floor
            placer._last_local_diff = 0.0
            return False

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", side_effect=fake_verify),
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            with pytest.raises(PlacementError, match="failed to place after retry") as exc_info:
                await placer.place_tiles(move, ["A"])
            assert not isinstance(exc_info.value, CoordinateDriftError)

    @pytest.mark.asyncio
    async def test_place_tiles_drift_only_fires_on_first_tile(self):
        """Drift detection is gated to ordinal == 0. A later-tile failure with
        the same diff signature still raises plain PlacementError because by
        then we've already proven the coordinate frame is correct (the first
        tile landed)."""
        placer, page = _make_placer()
        tiles = _h_tiles("AB", row=0, start_col=0)
        move = _make_move("AB", "H", tiles)

        call_count = 0

        async def fake_verify(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            # First call (tile A, ordinal 0): pass.
            # Subsequent calls (tile B, ordinal 1): fail with drift signature.
            if call_count == 1:
                placer._last_global_diff = 5.0
                placer._last_local_diff = 30.0
                return True
            placer._last_global_diff = 0.95
            placer._last_local_diff = 0.0
            return False

        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_verify_placement", side_effect=fake_verify),
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=_make_black_png()),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            with pytest.raises(PlacementError, match="failed to place after retry") as exc_info:
                await placer.place_tiles(move, ["A", "B"])
            assert not isinstance(exc_info.value, CoordinateDriftError)

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


class TestAnchorProbe:
    """Tests for the pre-flight anchor occupancy probe."""

    def test_v_range_empty_uniform_image(self):
        """A uniform-color image yields V_range == 0 at any cell."""
        img = np.full((768, 1545, 3), (210, 230, 250), dtype=np.uint8)
        assert _cell_v_range(img, 5, 5) == 0

    def test_v_range_high_at_painted_cell(self):
        """A cell painted with a black/white split yields V_range == 255."""
        img_bytes = _make_board_png({(5, 13)})
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        assert _cell_v_range(img, 5, 13) >= 200

    def test_v_range_zero_at_unpainted_cell(self):
        """A cell *not* in the painted set still reads as empty."""
        img_bytes = _make_board_png({(5, 13)})
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        assert _cell_v_range(img, 7, 7) == 0

    def test_check_anchors_passes_when_all_cells_match(self):
        """Probe accepts the move when every anchor is occupied and every
        rack-tile destination is empty."""
        # Anchor at (5,13); rack tiles at (5,14) and (5,15)
        img_bytes = _make_board_png({(5, 13)})
        move = _make_move(
            "ABC", "H",
            [
                TileUse(row=5, col=13, letter="A", is_blank=False, from_rack=False),
                TileUse(row=5, col=14, letter="B", is_blank=False, from_rack=True),
                TileUse(row=5, col=15, letter="C", is_blank=False, from_rack=True),
            ],
        )
        assert _check_move_anchors(img_bytes, move) is None

    def test_check_anchors_rejects_empty_anchor(self):
        """Engine claims an anchor exists, but the live cell is empty."""
        # Painted cells: only (5, 14). Engine's anchor at (5, 13) is empty.
        img_bytes = _make_board_png({(5, 14)})
        move = _make_move(
            "AB", "H",
            [
                TileUse(row=5, col=13, letter="A", is_blank=False, from_rack=False),
                TileUse(row=5, col=14, letter="B", is_blank=False, from_rack=True),
            ],
        )
        result = _check_move_anchors(img_bytes, move)
        assert result is not None
        assert "anchor 'A'" in result
        assert "(5,13)" in result

    def test_check_anchors_rejects_occupied_destination(self):
        """Engine plans to place a rack tile where one already exists."""
        # (5, 14) is already occupied. Engine's plan tries to place there.
        img_bytes = _make_board_png({(5, 13), (5, 14)})
        move = _make_move(
            "AB", "H",
            [
                TileUse(row=5, col=13, letter="A", is_blank=False, from_rack=False),
                TileUse(row=5, col=14, letter="B", is_blank=False, from_rack=True),
            ],
        )
        result = _check_move_anchors(img_bytes, move)
        assert result is not None
        assert "rack-tile destination" in result
        assert "(5,14)" in result

    def test_check_anchors_returns_none_on_decode_failure(self):
        """A garbage screenshot does not block placement — the probe yields
        to the downstream verifier rather than producing a false positive."""
        move = _make_move("A", "H", _h_tiles("A", row=0, start_col=0))
        assert _check_move_anchors(b"not-a-png", move) is None


class TestPlaceTilesPreflight:
    @pytest.mark.asyncio
    async def test_place_tiles_aborts_on_missing_anchor(self):
        """When the pre-flight probe sees no tile at an anchor cell, place_tiles
        raises CoordinateDriftError without making a single placement click."""
        placer, page = _make_placer()
        # Anchor at (5,13); rack tile at (5,14). Live board has neither.
        empty_board = _make_board_png(set())
        move = _make_move(
            "AB", "H",
            [
                TileUse(row=5, col=13, letter="A", is_blank=False, from_rack=False),
                TileUse(row=5, col=14, letter="B", is_blank=False, from_rack=True),
            ],
        )

        bbox = {"x": 0, "y": 0, "width": 1545, "height": 768}
        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=bbox),
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=empty_board),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            with pytest.raises(CoordinateDriftError, match="Pre-flight anchor probe"):
                await placer.place_tiles(move, ["B", "C"])

        # Crucial: no placement click should have happened
        assert page.mouse.click.call_count == 0

    @pytest.mark.asyncio
    async def test_place_tiles_proceeds_when_anchors_match(self):
        """When the live board matches the move, place_tiles continues to
        click placement as normal."""
        placer, page = _make_placer()
        live_board = _make_board_png({(5, 13)})
        move = _make_move(
            "AB", "H",
            [
                TileUse(row=5, col=13, letter="A", is_blank=False, from_rack=False),
                TileUse(row=5, col=14, letter="B", is_blank=False, from_rack=True),
            ],
        )

        bbox = {"x": 0, "y": 0, "width": 1545, "height": 768}
        with (
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=bbox),
            patch.object(placer, "_verify_placement", new_callable=AsyncMock, return_value=True),
            patch("src.browser.tile_placer.capture_canvas", new_callable=AsyncMock, return_value=live_board),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer.place_tiles(move, ["B", "C"])

        # 1 rack tile = 2 clicks (select rack + place on board)
        assert page.mouse.click.call_count == 2


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

        assert result is not None

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

        assert result is not None

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

        assert result is None
        mock_swap.assert_called_once()

    @pytest.mark.asyncio
    async def test_place_move_dedupes_repeated_word(self):
        """Same word at multiple board positions is only tried once —
        once rejected, subsequent placements of the identical word are
        skipped rather than replayed."""
        placer, _ = _make_placer()
        # Same word "KEEF" at four distinct anchor positions plus one
        # alternate word "FAKE".
        keef1 = _make_move("KEEF", "H", _h_tiles("KEEF", row=9, start_col=10))
        keef2 = _make_move("KEEF", "H", _h_tiles("KEEF", row=9, start_col=11))
        keef3 = _make_move("KEEF", "H", _h_tiles("KEEF", row=9, start_col=12))
        keef4 = _make_move("KEEF", "H", _h_tiles("KEEF", row=9, start_col=13))
        fake = _make_move("FAKE", "H", _h_tiles("FAKE", row=9, start_col=12))

        with (
            patch.object(placer, "place_tiles", new_callable=AsyncMock) as mock_place_tiles,
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_click_confirm", new_callable=AsyncMock),
            patch.object(placer, "_wait_for_acceptance", new_callable=AsyncMock, return_value=False),
            patch.object(placer, "_recall_tiles", new_callable=AsyncMock),
            patch.object(placer, "_tile_swap", new_callable=AsyncMock),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            await placer.place_move([keef1, keef2, keef3, keef4, fake], ["K", "E", "E", "F", "F", "A"])

        # Only two distinct words, so place_tiles should run twice total —
        # once for KEEF, once for FAKE — regardless of how many KEEF variants
        # were in the candidate list.
        assert mock_place_tiles.call_count == 2
        played_words = [c.args[0].word for c in mock_place_tiles.call_args_list]
        assert played_words == ["KEEF", "FAKE"]

    @pytest.mark.asyncio
    async def test_place_move_skips_prebaklisted_words(self):
        """Candidates whose word is already in the rejected_words blacklist
        are filtered out before any placement attempt."""
        from src.engine import rejected_words

        placer, _ = _make_placer()
        blocked = _make_move("ZZZ", "H", _h_tiles("ZZZ", row=0, start_col=0))
        playable = _make_move("CAT", "H", _h_tiles("CAT", row=0, start_col=0))

        rejected_words.add("zzz")

        with (
            patch.object(placer, "place_tiles", new_callable=AsyncMock) as mock_place_tiles,
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_click_confirm", new_callable=AsyncMock),
            patch.object(placer, "_wait_for_acceptance", new_callable=AsyncMock, return_value=True),
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await placer.place_move([blocked, playable], ["Z", "Z", "Z", "C", "A", "T"])

        assert result is not None
        assert result.word == "CAT"
        assert mock_place_tiles.call_count == 1

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

        assert result is not None

    @pytest.mark.asyncio
    async def test_place_move_short_circuits_on_coordinate_drift(self):
        """CoordinateDriftError on the first candidate aborts the whole loop:
        no second candidate is tried, no SWAP is performed, place_move returns
        None so the orchestrator can re-vision."""
        placer, page = _make_placer()
        tiles1 = _h_tiles("AB", row=0, start_col=0)
        tiles2 = _h_tiles("CD", row=1, start_col=0)
        move1 = _make_move("AB", "H", tiles1)
        move2 = _make_move("CD", "H", tiles2)

        place_tiles_mock = AsyncMock(
            side_effect=CoordinateDriftError("first tile missed cell"),
        )

        with (
            patch.object(placer, "place_tiles", place_tiles_mock),
            patch.object(placer, "_get_canvas_bbox", new_callable=AsyncMock, return_value=BBOX),
            patch.object(placer, "_click_confirm", new_callable=AsyncMock),
            patch.object(placer, "_wait_for_acceptance", new_callable=AsyncMock, return_value=True),
            patch.object(placer, "_recall_tiles", new_callable=AsyncMock) as mock_recall,
            patch.object(placer, "_tile_swap", new_callable=AsyncMock) as mock_swap,
            patch("src.browser.tile_placer.asyncio.sleep", new_callable=AsyncMock),
        ):
            result = await placer.place_move(
                [move1, move2], ["A", "B", "C", "D"], swap_on_fail=True,
            )

        assert result is None
        # Only the first candidate was attempted before the short-circuit.
        assert place_tiles_mock.call_count == 1
        # Recall ran (to clear any partial staging).
        mock_recall.assert_called_once()
        # No SWAP — drift means re-vision, not give-up-and-swap.
        mock_swap.assert_not_called()


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

        assert result is None
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
