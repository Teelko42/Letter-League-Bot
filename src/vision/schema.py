from __future__ import annotations

from src.engine.models import MultiplierType

# JSON schema for Claude Vision structured output.
# Used with output_config.format.type = "json_schema" in the Claude API call.
# The schema constrains Claude's token generation to produce only valid JSON
# matching this structure — parse errors are impossible on the primary path.
BOARD_SCHEMA: dict = {
    "type": "object",
    "properties": {
        "board": {
            "type": "object",
            "description": "Bounding rectangle of the occupied board area with all placed cells",
            "properties": {
                "min_row": {"type": "integer", "description": "Smallest row index of any placed tile"},
                "max_row": {"type": "integer", "description": "Largest row index of any placed tile"},
                "min_col": {"type": "integer", "description": "Smallest column index of any placed tile"},
                "max_col": {"type": "integer", "description": "Largest column index of any placed tile"},
                "cells": {
                    "type": "array",
                    "description": "All cells that contain a placed tile",
                    "items": {
                        "type": "object",
                        "properties": {
                            "row": {"type": "integer", "description": "0-indexed row (0 = top)"},
                            "col": {"type": "integer", "description": "0-indexed column (0 = left)"},
                            "letter": {"type": "string", "description": "Uppercase letter on the tile"},
                            "is_blank": {
                                "type": "boolean",
                                "description": "True if this tile is a blank tile playing as the given letter",
                            },
                            "multiplier": {
                                "type": "string",
                                "enum": ["NONE", "DL", "TL", "DW", "TW"],
                                "description": "Square multiplier visible at this board position",
                            },
                        },
                        "required": ["row", "col", "letter", "is_blank", "multiplier"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["min_row", "max_row", "min_col", "max_col", "cells"],
            "additionalProperties": False,
        },
        "rack": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Player's tile rack — list of uppercase letter strings, max 7 tiles",
            "maxItems": 7,
        },
    },
    "required": ["board", "rack"],
    "additionalProperties": False,
}


# TODO: Verify against real Letter League screenshots — update positions if needed.
#
# Official 19-row x 27-column Letter League board multiplier layout.
# Maps (row, col) → multiplier string for all non-NONE squares.
# Only non-NONE positions are included; any (row, col) absent from this dict is NONE.
# Positions are 0-indexed: row 0 = top row, col 0 = leftmost column.
#
# These positions follow symmetric Scrabble-like patterns and are approximate.
# They must be verified and corrected against actual Letter League screenshots
# before multiplier validation (check 3) can be relied upon.
OFFICIAL_MULTIPLIER_LAYOUT: dict[tuple[int, int], str] = {
    # TW — Triple Word
    (0, 0): "TW",
    (0, 13): "TW",
    (0, 26): "TW",
    (9, 0): "TW",
    (9, 26): "TW",
    (18, 0): "TW",
    (18, 13): "TW",
    (18, 26): "TW",
    # DW — Double Word
    (1, 1): "DW",
    (1, 25): "DW",
    (2, 2): "DW",
    (2, 24): "DW",
    (3, 3): "DW",
    (3, 23): "DW",
    (4, 4): "DW",
    (4, 22): "DW",
    (5, 5): "DW",
    (5, 21): "DW",
    (6, 6): "DW",
    (6, 20): "DW",
    (7, 7): "DW",
    (7, 19): "DW",
    (1, 7): "DW",
    (1, 19): "DW",
    (7, 1): "DW",
    (7, 25): "DW",
    (17, 1): "DW",
    (17, 25): "DW",
    (11, 1): "DW",
    (11, 25): "DW",
    (17, 7): "DW",
    (17, 19): "DW",
    (11, 7): "DW",
    (11, 19): "DW",
    (12, 6): "DW",
    (12, 20): "DW",
    (13, 5): "DW",
    (13, 21): "DW",
    (14, 4): "DW",
    (14, 22): "DW",
    (15, 3): "DW",
    (15, 23): "DW",
    (16, 2): "DW",
    (16, 24): "DW",
    # TL — Triple Letter
    (0, 4): "TL",
    (0, 9): "TL",
    (0, 17): "TL",
    (0, 22): "TL",
    (4, 0): "TL",
    (4, 13): "TL",
    (4, 26): "TL",
    (9, 4): "TL",
    (9, 9): "TL",
    (9, 17): "TL",
    (9, 22): "TL",
    (14, 0): "TL",
    (14, 13): "TL",
    (14, 26): "TL",
    (18, 4): "TL",
    (18, 9): "TL",
    (18, 17): "TL",
    (18, 22): "TL",
    # DL — Double Letter
    (1, 4): "DL",
    (1, 9): "DL",
    (1, 17): "DL",
    (1, 22): "DL",
    (2, 5): "DL",
    (2, 8): "DL",
    (2, 18): "DL",
    (2, 21): "DL",
    (3, 6): "DL",
    (3, 7): "DL",
    (3, 19): "DL",
    (3, 20): "DL",
    (4, 8): "DL",
    (4, 18): "DL",
    (5, 9): "DL",
    (5, 17): "DL",
    (6, 10): "DL",
    (6, 16): "DL",
    (7, 11): "DL",
    (7, 15): "DL",
    (8, 12): "DL",
    (8, 14): "DL",
    (8, 0): "DL",
    (8, 26): "DL",
    (10, 0): "DL",
    (10, 26): "DL",
    (10, 12): "DL",
    (10, 14): "DL",
    (11, 11): "DL",
    (11, 15): "DL",
    (12, 10): "DL",
    (12, 16): "DL",
    (13, 9): "DL",
    (13, 17): "DL",
    (14, 8): "DL",
    (14, 18): "DL",
    (15, 6): "DL",
    (15, 7): "DL",
    (15, 19): "DL",
    (15, 20): "DL",
    (16, 5): "DL",
    (16, 8): "DL",
    (16, 18): "DL",
    (16, 21): "DL",
    (17, 4): "DL",
    (17, 9): "DL",
    (17, 17): "DL",
    (17, 22): "DL",
}


# Maps schema multiplier strings to the engine's MultiplierType enum.
# Used when populating a Board from vision-extracted data.
MULT_STR_TO_ENGINE: dict[str, MultiplierType] = {
    "NONE": MultiplierType.NONE,
    "DL": MultiplierType.DL,
    "TL": MultiplierType.TL,
    "DW": MultiplierType.DW,
    "TW": MultiplierType.TW,
}
