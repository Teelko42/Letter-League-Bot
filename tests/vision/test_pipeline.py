"""Tests for vision pipeline integration (Phase B5).

Preprocessor, extractor, and validator are all mocked.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.vision import extract_board_state
from src.vision.errors import VALIDATION_FAILED, VisNError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _valid_extraction() -> dict:
    """Return a valid extraction result that passes validation."""
    return {
        "board": {
            "min_row": 9,
            "max_row": 9,
            "min_col": 13,
            "max_col": 13,
            "cells": [
                {"row": 9, "col": 13, "letter": "H", "is_blank": False, "multiplier": "NONE"},
            ],
        },
        "rack": ["A", "B", "C", "D", "E", "F", "G"],
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestExtractBoardState:
    @pytest.mark.asyncio
    async def test_pipeline_success_end_to_end(self):
        data = _valid_extraction()

        with (
            patch("src.vision.preprocess_screenshot", return_value=b"processed"),
            patch("src.vision.call_vision_api", new_callable=AsyncMock, return_value=data),
            patch("src.vision.validate_extraction", return_value=[]),  # no errors
        ):
            board, rack = await extract_board_state(b"raw screenshot")

        assert rack == ["A", "B", "C", "D", "E", "F", "G"]
        # Board should have the placed tile
        cell = board.grid[9][13]
        assert cell.letter == "H"

    @pytest.mark.asyncio
    async def test_pipeline_retries_on_validation_failure(self):
        data = _valid_extraction()

        call_count = 0

        async def mock_vision_api(img_bytes, retry_context=None):
            nonlocal call_count
            call_count += 1
            return data

        with (
            patch("src.vision.preprocess_screenshot", return_value=b"processed"),
            patch("src.vision.call_vision_api", side_effect=mock_vision_api),
            patch("src.vision.validate_extraction", side_effect=[["error: bad cell"], []]),
        ):
            board, rack = await extract_board_state(b"raw screenshot")

        assert call_count == 2  # first attempt + retry

    @pytest.mark.asyncio
    async def test_pipeline_raises_after_max_retries(self):
        data = _valid_extraction()

        with (
            patch("src.vision.preprocess_screenshot", return_value=b"processed"),
            patch("src.vision.call_vision_api", new_callable=AsyncMock, return_value=data),
            patch("src.vision.validate_extraction", return_value=["persistent error"]),
        ):
            with pytest.raises(VisNError) as exc_info:
                await extract_board_state(b"raw screenshot")

        assert exc_info.value.code == VALIDATION_FAILED

    @pytest.mark.asyncio
    async def test_word_validity_error_is_soft_after_retry(self):
        """Word validity failures after retry must NOT raise — they are soft errors.

        This is the multi-word board regression: Vision API position imprecision
        on crowded boards causes word runs to fail dictionary lookup.  The pipeline
        should proceed with the best-effort extraction rather than raising
        VisNError(VALIDATION_FAILED).
        """
        data = _valid_extraction()
        word_error = (
            "Invalid word(s) on board: 'HELXO' at row 9 cols 13-17 — "
            "tile positions are likely off by 1. Re-count carefully from center star at (9,13)."
        )

        with (
            patch("src.vision.preprocess_screenshot", return_value=b"processed"),
            patch("src.vision.call_vision_api", new_callable=AsyncMock, return_value=data),
            # First call: word error triggers retry. Second call: word error persists.
            patch(
                "src.vision.validate_extraction",
                side_effect=[[word_error], [word_error]],
            ),
        ):
            # Must NOT raise — word errors are soft after retry
            board, rack = await extract_board_state(b"raw screenshot")

        assert rack == ["A", "B", "C", "D", "E", "F", "G"]
        # Board still populated with the single extracted cell
        assert board.grid[9][13].letter == "H"

    @pytest.mark.asyncio
    async def test_hard_errors_still_raise_after_retry(self):
        """Non-soft errors (e.g. duplicate tiles, out-of-bounds) must still raise."""
        data = _valid_extraction()
        hard_error = "Duplicate tile at (9, 13) — two tiles cannot occupy the same cell"

        with (
            patch("src.vision.preprocess_screenshot", return_value=b"processed"),
            patch("src.vision.call_vision_api", new_callable=AsyncMock, return_value=data),
            patch(
                "src.vision.validate_extraction",
                side_effect=[[hard_error], [hard_error]],
            ),
        ):
            with pytest.raises(VisNError) as exc_info:
                await extract_board_state(b"raw screenshot")

        assert exc_info.value.code == VALIDATION_FAILED

    @pytest.mark.asyncio
    async def test_position_accuracy_error_is_soft_after_retry(self):
        """Position accuracy suspect errors after retry must NOT raise.

        This is the second half of the multi-word board regression: when many
        tiles land on multiplier squares and positions drift, the multiplier
        mismatch check fires as well as (or instead of) the word validity check.
        Both have the same root cause (global position drift) and should be
        treated as soft — the validator already overwrites multiplier values with
        the official layout so the engine is unaffected.
        """
        data = _valid_extraction()
        position_error = (
            "Position accuracy suspect: 4/6 multiplier mismatches — "
            "tile coordinates may be off. Re-count positions using the center star at (9,13) "
            "as reference."
        )

        with (
            patch("src.vision.preprocess_screenshot", return_value=b"processed"),
            patch("src.vision.call_vision_api", new_callable=AsyncMock, return_value=data),
            # First call: position error triggers retry. Second call: error persists.
            patch(
                "src.vision.validate_extraction",
                side_effect=[[position_error], [position_error]],
            ),
        ):
            # Must NOT raise — position accuracy errors are soft after retry
            board, rack = await extract_board_state(b"raw screenshot")

        assert rack == ["A", "B", "C", "D", "E", "F", "G"]
        assert board.grid[9][13].letter == "H"

    @pytest.mark.asyncio
    async def test_position_and_word_errors_both_soft_after_retry(self):
        """Position accuracy + word validity errors together are both soft after retry.

        On a crowded multi-word board both error types typically fire together.
        Neither alone nor together should cause a raise.
        """
        data = _valid_extraction()
        position_error = (
            "Position accuracy suspect: 3/4 multiplier mismatches — "
            "tile coordinates may be off. Re-count positions using the center star at (9,13) "
            "as reference."
        )
        word_error = (
            "Invalid word(s) on board: 'HELXO' at row 9 cols 13-17 — "
            "tile positions are likely off by 1. Re-count carefully from center star at (9,13)."
        )
        both_errors = [position_error, word_error]

        with (
            patch("src.vision.preprocess_screenshot", return_value=b"processed"),
            patch("src.vision.call_vision_api", new_callable=AsyncMock, return_value=data),
            patch(
                "src.vision.validate_extraction",
                side_effect=[both_errors, both_errors],
            ),
        ):
            board, rack = await extract_board_state(b"raw screenshot")

        assert rack == ["A", "B", "C", "D", "E", "F", "G"]
        assert board.grid[9][13].letter == "H"

    @pytest.mark.asyncio
    async def test_pipeline_preprocessor_called_first(self):
        data = _valid_extraction()
        preprocess_called = False
        api_called_with = None

        def mock_preprocess(img_bytes):
            nonlocal preprocess_called
            preprocess_called = True
            return b"preprocessed_output"

        async def mock_api(img_bytes, retry_context=None):
            nonlocal api_called_with
            api_called_with = img_bytes
            return data

        with (
            patch("src.vision.preprocess_screenshot", side_effect=mock_preprocess),
            patch("src.vision.call_vision_api", side_effect=mock_api),
            patch("src.vision.validate_extraction", return_value=[]),
        ):
            await extract_board_state(b"raw screenshot")

        assert preprocess_called
        assert api_called_with == b"preprocessed_output"
