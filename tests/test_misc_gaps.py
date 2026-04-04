"""Misc gap tests (Phase C6): VisNError and Move.rack_tiles_consumed."""

from __future__ import annotations

from src.engine.models import Move, ScoreBreakdown, TileUse
from src.vision.errors import EXTRACTION_FAILED, VisNError


class TestVisNError:
    def test_stores_code_and_message(self):
        err = VisNError(EXTRACTION_FAILED, "something broke")
        assert err.code == EXTRACTION_FAILED
        assert err.message == "something broke"
        assert EXTRACTION_FAILED in str(err)


class TestMoveRackTilesConsumed:
    def test_rack_tiles_consumed(self):
        tiles = [
            TileUse(row=0, col=0, letter="A", is_blank=False, from_rack=True),
            TileUse(row=0, col=1, letter="B", is_blank=False, from_rack=False),
            TileUse(row=0, col=2, letter="C", is_blank=False, from_rack=True),
        ]
        move = Move(
            word="ABC",
            start_row=0,
            start_col=0,
            direction="H",
            tiles_used=tiles,
            score_breakdown=ScoreBreakdown(base_letter_sum=5, word_multiplier=1, total=5),
            score=5,
        )
        consumed = move.rack_tiles_consumed()
        assert len(consumed) == 2
        assert all(t.from_rack for t in consumed)
        assert consumed[0].letter == "A"
        assert consumed[1].letter == "C"
