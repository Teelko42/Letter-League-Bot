"""Tests for CoordMapper, assign_rack_indices, and jitter (Phase A1-A3).

Pure function tests — no browser or mocking needed.
"""

from __future__ import annotations

import pytest

from src.browser.tile_placer import (
    CELL_H_FRAC,
    CELL_W_FRAC,
    CONFIRM_X_FRAC,
    CONFIRM_Y_FRAC,
    CoordMapper,
    GRID_X0_FRAC,
    GRID_Y0_FRAC,
    PlacementError,
    RACK_TILE_STEP_FRAC,
    RACK_X0_FRAC,
    RACK_Y_FRAC,
    RECALL_X_FRAC,
    RECALL_Y_FRAC,
    SWAP_X_FRAC,
    SWAP_Y_FRAC,
    assign_rack_indices,
    jitter,
)
from src.engine.models import TileUse


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SIMPLE_BBOX = {"x": 0, "y": 0, "width": 1000, "height": 800}
OFFSET_BBOX = {"x": 100, "y": 50, "width": 1000, "height": 800}


# ---------------------------------------------------------------------------
# A1: CoordMapper tests
# ---------------------------------------------------------------------------


class TestCoordMapper:
    def test_board_cell_px_origin(self):
        mapper = CoordMapper(SIMPLE_BBOX)
        x, y = mapper.board_cell_px(0, 0)
        assert x == pytest.approx(GRID_X0_FRAC * 1000)
        assert y == pytest.approx(GRID_Y0_FRAC * 800)

    def test_board_cell_px_offset(self):
        mapper = CoordMapper(SIMPLE_BBOX)
        x, y = mapper.board_cell_px(7, 7)
        assert x == pytest.approx((GRID_X0_FRAC + 7 * CELL_W_FRAC) * 1000)
        assert y == pytest.approx((GRID_Y0_FRAC + 7 * CELL_H_FRAC) * 800)

    def test_board_cell_px_with_nonzero_bbox_origin(self):
        mapper = CoordMapper(OFFSET_BBOX)
        x, y = mapper.board_cell_px(0, 0)
        assert x == pytest.approx(100 + GRID_X0_FRAC * 1000)
        assert y == pytest.approx(50 + GRID_Y0_FRAC * 800)

    def test_rack_tile_px_slot_0(self):
        mapper = CoordMapper(SIMPLE_BBOX)
        x, y = mapper.rack_tile_px(0)
        assert x == pytest.approx(RACK_X0_FRAC * 1000)
        assert y == pytest.approx(RACK_Y_FRAC * 800)

    def test_rack_tile_px_slot_6(self):
        mapper = CoordMapper(SIMPLE_BBOX)
        x, y = mapper.rack_tile_px(6)
        assert x == pytest.approx((RACK_X0_FRAC + 6 * RACK_TILE_STEP_FRAC) * 1000)
        assert y == pytest.approx(RACK_Y_FRAC * 800)

    def test_confirm_btn_px(self):
        mapper = CoordMapper(SIMPLE_BBOX)
        x, y = mapper.confirm_btn_px()
        assert x == pytest.approx(CONFIRM_X_FRAC * 1000)
        assert y == pytest.approx(CONFIRM_Y_FRAC * 800)

    def test_recall_btn_px(self):
        mapper = CoordMapper(SIMPLE_BBOX)
        x, y = mapper.recall_btn_px()
        assert x == pytest.approx(RECALL_X_FRAC * 1000)
        assert y == pytest.approx(RECALL_Y_FRAC * 800)

    def test_swap_btn_px(self):
        mapper = CoordMapper(SIMPLE_BBOX)
        x, y = mapper.swap_btn_px()
        assert x == pytest.approx(SWAP_X_FRAC * 1000)
        assert y == pytest.approx(SWAP_Y_FRAC * 800)

    def test_none_bbox_raises(self):
        with pytest.raises(PlacementError, match="None"):
            CoordMapper(None)


# ---------------------------------------------------------------------------
# A2: assign_rack_indices tests
# ---------------------------------------------------------------------------


class TestAssignRackIndices:
    def test_assign_simple_unique_letters(self):
        rack = ["A", "B", "C"]
        tiles = [
            TileUse(row=0, col=0, letter="A", is_blank=False, from_rack=True),
            TileUse(row=0, col=2, letter="C", is_blank=False, from_rack=True),
        ]
        assert assign_rack_indices(rack, tiles) == [0, 2]

    def test_assign_duplicate_letters(self):
        rack = ["A", "A", "B"]
        tiles = [
            TileUse(row=0, col=0, letter="A", is_blank=False, from_rack=True),
            TileUse(row=0, col=1, letter="A", is_blank=False, from_rack=True),
        ]
        assert assign_rack_indices(rack, tiles) == [0, 1]

    def test_assign_blank_tile(self):
        rack = ["A", "?", "B"]
        tiles = [
            TileUse(row=0, col=0, letter="X", is_blank=True, from_rack=True),
        ]
        assert assign_rack_indices(rack, tiles) == [1]

    def test_assign_missing_letter_raises(self):
        rack = ["A", "B"]
        tiles = [
            TileUse(row=0, col=0, letter="C", is_blank=False, from_rack=True),
        ]
        with pytest.raises(ValueError, match="not found"):
            assign_rack_indices(rack, tiles)

    def test_assign_empty_rack_tiles(self):
        rack = ["A", "B", "C"]
        assert assign_rack_indices(rack, []) == []


# ---------------------------------------------------------------------------
# A3: jitter tests
# ---------------------------------------------------------------------------


class TestJitter:
    def test_jitter_within_bounds(self):
        for _ in range(200):
            x, y = jitter(100.0, 200.0, px=5)
            assert 95.0 <= x <= 105.0
            assert 195.0 <= y <= 205.0

    def test_jitter_zero_px(self):
        x, y = jitter(100.0, 200.0, px=0)
        assert x == 100.0
        assert y == 200.0
