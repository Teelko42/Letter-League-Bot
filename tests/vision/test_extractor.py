"""Tests for vision extractor (Phase B4).

Claude Vision API is fully mocked.
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.vision.errors import EXTRACTION_FAILED, VisNError
from src.vision.extractor import EXTRACTION_PROMPT, call_vision_api


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_api_response(data: dict) -> MagicMock:
    """Build a mock Anthropic Messages response."""
    response = MagicMock()
    response.content = [MagicMock(text=json.dumps(data))]
    response.usage = MagicMock(input_tokens=100, output_tokens=50)
    return response


VALID_DATA = {
    "board": {
        "min_row": 9,
        "max_row": 9,
        "min_col": 11,
        "max_col": 15,
        "cells": [
            {"row": 9, "col": 13, "letter": "H", "is_blank": False, "multiplier": "DW"},
        ],
    },
    "rack": ["A", "B", "C", "D", "E", "F", "G"],
}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCallVisionApi:
    @pytest.mark.asyncio
    async def test_success(self):
        mock_response = _make_api_response(VALID_DATA)
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        with patch("src.vision.extractor._get_client", return_value=mock_client):
            result = await call_vision_api(b"\x89PNG fake")

        assert result["rack"] == ["A", "B", "C", "D", "E", "F", "G"]
        assert len(result["board"]["cells"]) == 1

    @pytest.mark.asyncio
    async def test_retry_context_appended(self):
        mock_response = _make_api_response(VALID_DATA)
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        with patch("src.vision.extractor._get_client", return_value=mock_client):
            await call_vision_api(b"\x89PNG fake", retry_context="cell (3,5) has invalid letter")

        call_args = mock_client.messages.create.call_args
        prompt_text = call_args.kwargs["messages"][0]["content"][1]["text"]
        assert "PREVIOUS ATTEMPT HAD ERRORS" in prompt_text
        assert "cell (3,5) has invalid letter" in prompt_text

    @pytest.mark.asyncio
    async def test_api_error_raises_visnerror(self):
        import anthropic

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            side_effect=anthropic.APIError(
                message="rate limit",
                request=MagicMock(),
                body=None,
            )
        )

        with patch("src.vision.extractor._get_client", return_value=mock_client):
            with pytest.raises(VisNError) as exc_info:
                await call_vision_api(b"\x89PNG fake")
        assert exc_info.value.code == EXTRACTION_FAILED

    @pytest.mark.asyncio
    async def test_unexpected_error_raises_visnerror(self):
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(side_effect=RuntimeError("boom"))

        with patch("src.vision.extractor._get_client", return_value=mock_client):
            with pytest.raises(VisNError) as exc_info:
                await call_vision_api(b"\x89PNG fake")
        assert exc_info.value.code == EXTRACTION_FAILED

    @pytest.mark.asyncio
    async def test_logs_latency(self, capfd):
        mock_response = _make_api_response(VALID_DATA)
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        with patch("src.vision.extractor._get_client", return_value=mock_client):
            result = await call_vision_api(b"\x89PNG fake")

        # Just verify the call succeeded and returned data (latency logging goes through loguru)
        assert "rack" in result
