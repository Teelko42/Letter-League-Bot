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
                {"row": 9, "col": 13, "letter": "H", "is_blank": False, "multiplier": "DW"},
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
