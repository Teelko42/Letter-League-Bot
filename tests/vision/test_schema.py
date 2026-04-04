"""Tests for vision schema (Phase C5).

Tests the JSON schema structure and the official multiplier layout.
"""

from __future__ import annotations

from src.vision.schema import BOARD_SCHEMA, MULT_STR_TO_ENGINE, OFFICIAL_MULTIPLIER_LAYOUT
from src.engine.models import MultiplierType


class TestBoardSchema:
    def test_schema_has_required_top_keys(self):
        assert "board" in BOARD_SCHEMA["properties"]
        assert "rack" in BOARD_SCHEMA["properties"]
        assert set(BOARD_SCHEMA["required"]) == {"board", "rack"}

    def test_cell_schema_has_required_fields(self):
        cell_schema = BOARD_SCHEMA["properties"]["board"]["properties"]["cells"]["items"]
        assert set(cell_schema["required"]) == {"row", "col", "letter", "is_blank", "multiplier"}

    def test_multiplier_enum_values(self):
        cell_schema = BOARD_SCHEMA["properties"]["board"]["properties"]["cells"]["items"]
        mult_enum = cell_schema["properties"]["multiplier"]["enum"]
        assert set(mult_enum) == {"NONE", "DL", "TL", "DW", "TW"}


class TestOfficialMultiplierLayout:
    def test_dimensions_19x27(self):
        """All positions must be within the 19x27 board."""
        for (row, col) in OFFICIAL_MULTIPLIER_LAYOUT:
            assert 0 <= row < 19, f"row {row} out of range"
            assert 0 <= col < 27, f"col {col} out of range"

    def test_symmetry(self):
        """Layout should be vertically symmetric (row r <-> row 18-r)."""
        for (row, col), mult in OFFICIAL_MULTIPLIER_LAYOUT.items():
            mirror_row = 18 - row
            mirror_key = (mirror_row, col)
            assert mirror_key in OFFICIAL_MULTIPLIER_LAYOUT, (
                f"({row},{col})={mult} has no vertical mirror at ({mirror_row},{col})"
            )
            assert OFFICIAL_MULTIPLIER_LAYOUT[mirror_key] == mult

    def test_valid_multiplier_strings(self):
        valid = {"DL", "TL", "DW", "TW"}
        for pos, mult in OFFICIAL_MULTIPLIER_LAYOUT.items():
            assert mult in valid, f"Invalid multiplier '{mult}' at {pos}"

    def test_mult_str_to_engine_mapping(self):
        assert MULT_STR_TO_ENGINE["NONE"] == MultiplierType.NONE
        assert MULT_STR_TO_ENGINE["DL"] == MultiplierType.DL
        assert MULT_STR_TO_ENGINE["TL"] == MultiplierType.TL
        assert MULT_STR_TO_ENGINE["DW"] == MultiplierType.DW
        assert MULT_STR_TO_ENGINE["TW"] == MultiplierType.TW
