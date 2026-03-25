from __future__ import annotations

import pytest

from src.vision.validator import validate_extraction
from src.vision.schema import OFFICIAL_MULTIPLIER_LAYOUT


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_data(
    cells: list[dict],
    rack: list[str] | None = None,
) -> dict:
    """Build a minimal data dict compatible with BOARD_SCHEMA."""
    if rack is None:
        rack = []

    rows = [c["row"] for c in cells] if cells else [0]
    cols = [c["col"] for c in cells] if cells else [0]

    return {
        "board": {
            "min_row": min(rows),
            "max_row": max(rows),
            "min_col": min(cols),
            "max_col": max(cols),
            "cells": cells,
        },
        "rack": rack,
    }


def _cell(row: int, col: int, letter: str = "A", is_blank: bool = False) -> dict:
    """Build a cell dict with the correct multiplier from the official layout."""
    multiplier = OFFICIAL_MULTIPLIER_LAYOUT.get((row, col), "NONE")
    return {
        "row": row,
        "col": col,
        "letter": letter,
        "is_blank": is_blank,
        "multiplier": multiplier,
    }


# ---------------------------------------------------------------------------
# Test 1: valid extraction passes all four checks
# ---------------------------------------------------------------------------

def test_valid_extraction_passes():
    """A well-formed extraction with connected tiles and a valid rack passes."""
    # Three connected cells in a row: (9, 12), (9, 13), (9, 14) — "CAT"
    cells = [
        _cell(9, 12, "C"),
        _cell(9, 13, "A"),
        _cell(9, 14, "T"),
    ]
    data = _make_data(cells, rack=["D", "E", "F"])
    errors = validate_extraction(data)
    assert errors == [], f"Expected no errors, got: {errors}"


# ---------------------------------------------------------------------------
# Test 2: invalid letter detected
# ---------------------------------------------------------------------------

def test_invalid_letter_detected():
    """A cell with a non-A-Z letter produces an 'Invalid letter' error."""
    cells = [_cell(5, 5, "3")]
    data = _make_data(cells)
    errors = validate_extraction(data)
    assert any("Invalid letter" in e for e in errors), (
        f"Expected 'Invalid letter' error, got: {errors}"
    )


# ---------------------------------------------------------------------------
# Test 3: floating tile detected
# ---------------------------------------------------------------------------

def test_floating_tile_detected():
    """Two cells that are not orthogonally connected produce a 'Floating tile' error."""
    cells = [
        _cell(5, 5, "A"),
        _cell(10, 10, "B"),  # Not adjacent to (5, 5)
    ]
    data = _make_data(cells)
    errors = validate_extraction(data)
    assert any("Floating tile" in e for e in errors), (
        f"Expected 'Floating tile' error, got: {errors}"
    )


# ---------------------------------------------------------------------------
# Test 4: connected word passes connectivity check
# ---------------------------------------------------------------------------

def test_connected_word_passes_connectivity():
    """Horizontal word 'CAT' at (9,12)-(9,14) has no connectivity errors."""
    cells = [
        _cell(9, 12, "C"),
        _cell(9, 13, "A"),
        _cell(9, 14, "T"),
    ]
    data = _make_data(cells)
    errors = validate_extraction(data)
    connectivity_errors = [e for e in errors if "Floating tile" in e]
    assert connectivity_errors == [], (
        f"Expected no connectivity errors, got: {connectivity_errors}"
    )


# ---------------------------------------------------------------------------
# Test 5: single tile passes connectivity check
# ---------------------------------------------------------------------------

def test_single_tile_passes_connectivity():
    """A board with only one placed tile trivially passes the connectivity check."""
    cells = [_cell(9, 13, "A")]
    data = _make_data(cells)
    errors = validate_extraction(data)
    connectivity_errors = [e for e in errors if "Floating tile" in e]
    assert connectivity_errors == [], (
        f"Expected no connectivity errors for single tile, got: {connectivity_errors}"
    )


# ---------------------------------------------------------------------------
# Test 6: multiplier mismatch detected
# ---------------------------------------------------------------------------

def test_multiplier_mismatch_detected():
    """A cell whose multiplier doesn't match OFFICIAL_MULTIPLIER_LAYOUT is flagged."""
    # (3, 7) is TW in the official layout — report it as NONE
    cell = {
        "row": 3,
        "col": 7,
        "letter": "A",
        "is_blank": False,
        "multiplier": "NONE",  # Should be "TW"
    }
    data = _make_data([cell])
    errors = validate_extraction(data)
    assert any("Multiplier mismatch" in e for e in errors), (
        f"Expected 'Multiplier mismatch' error, got: {errors}"
    )


# ---------------------------------------------------------------------------
# Test 7: rack with too many tiles
# ---------------------------------------------------------------------------

def test_rack_too_many_tiles():
    """A rack with 8 tiles produces a 'max 7' error."""
    cells = [_cell(9, 13, "A")]
    data = _make_data(cells, rack=["A", "B", "C", "D", "E", "F", "G", "H"])
    errors = validate_extraction(data)
    assert any("max 7" in e for e in errors), (
        f"Expected 'max 7' error, got: {errors}"
    )


# ---------------------------------------------------------------------------
# Test 8: invalid rack tile detected
# ---------------------------------------------------------------------------

def test_invalid_rack_tile_detected():
    """A rack containing a digit produces an 'Invalid rack tile' error."""
    cells = [_cell(9, 13, "A")]
    data = _make_data(cells, rack=["A", "1"])
    errors = validate_extraction(data)
    assert any("Invalid rack tile" in e for e in errors), (
        f"Expected 'Invalid rack tile' error, got: {errors}"
    )
