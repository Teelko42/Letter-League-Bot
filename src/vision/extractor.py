from __future__ import annotations

import base64
import json
import time

import anthropic
from loguru import logger

from src.vision.errors import EXTRACTION_FAILED, VisNError
from src.vision.schema import BOARD_SCHEMA

# Lazy-initialised async client.  Created on first API call so that
# load_dotenv() has already populated ANTHROPIC_API_KEY in the environment.
_client: anthropic.AsyncAnthropic | None = None


def _get_client() -> anthropic.AsyncAnthropic:
    global _client
    if _client is None:
        _client = anthropic.AsyncAnthropic()
    return _client

# Prompt sent to Claude Vision for board state extraction.
# The prompt anchors Claude to the exact 19x27 grid coordinate system,
# provides landmark reference points for position calibration, and
# instructs it to return only occupied cells plus the player's tile rack.
EXTRACTION_PROMPT = (
    "You are analyzing a Letter League game board screenshot.\n"
    "\n"
    "BOARD LAYOUT:\n"
    "The board is exactly 19 rows by 27 columns (0-indexed):\n"
    "  - Row 0 is the top row, row 18 is the bottom row.\n"
    "  - Column 0 is the leftmost column, column 26 is the rightmost column.\n"
    "  - Columns increase left-to-right; rows increase top-to-bottom.\n"
    "  - The center of the board (marked with a star) is at row 9, column 13.\n"
    "\n"
    "REFERENCE LANDMARKS — use these to calibrate your position counting:\n"
    "  - Center star: (9, 13) — the middle of the board.\n"
    "  - Triple Word squares (TW, red/dark red): ONLY at (3,7), (3,19), (15,7), (15,19).\n"
    "  - The board is symmetric around the center.\n"
    "  - Multiplier squares are colored: blue=DL, green=DW, orange=TL, red=TW.\n"
    "\n"
    "REFERENCE MARKERS ON THE IMAGE:\n"
    "  Small colored dots with coordinate labels have been placed at:\n"
    "  - Green dot: center star at (9,13)\n"
    "  - Red dots: the four TW squares at (3,7), (3,19), (15,7), (15,19)\n"
    "  Use these markers to calibrate your position counting.\n"
    "\n"
    "COUNTING STRATEGY:\n"
    "  1. Locate the green center marker at (9,13).\n"
    "  2. For each tile, count its row and column offset from the center.\n"
    "  3. Verify: the multiplier color of the square under each tile should\n"
    "     match what you report. If it doesn't, re-count.\n"
    "\n"
    "EXTRACT:\n"
    "\n"
    "1. BOARD CELLS — Only cells that contain a placed tile (skip empty squares).\n"
    "   For each placed tile, record:\n"
    "     - row: 0-indexed row number (0 = top)\n"
    "     - col: 0-indexed column number (0 = left)\n"
    "     - letter: the uppercase letter (A-Z) on the tile\n"
    "     - is_blank: true if this is a blank tile playing as the given letter "
    "(blank tiles are visually distinct — lighter color, different border, or "
    "no printed point value)\n"
    "     - multiplier: the square multiplier type underneath/behind the tile "
    "(NONE, DL, TL, DW, or TW) — use the square's color/marking, not the tile itself\n"
    "\n"
    "2. TILE RACK — The row of tiles displayed below the board (the player's current rack).\n"
    "   Return as a list of uppercase letter strings.\n"
    "   Use '?' for any blank tile in the rack.\n"
    "\n"
    "Return ONLY the JSON — no explanation, no markdown fences."
)


async def call_vision_api(
    img_bytes: bytes,
    retry_context: str | None = None,
) -> dict:
    """Call Claude Vision API with structured output to extract board state.

    Encodes the image as base64, sends it to claude-sonnet-4-6 with the
    extraction prompt, and returns the parsed JSON response.

    Args:
        img_bytes: PNG-encoded image bytes of the preprocessed board screenshot.
        retry_context: Optional error context from a previous failed extraction.
            When provided, it is appended to the prompt so Claude can correct
            the identified mistakes.

    Returns:
        Parsed JSON dict conforming to BOARD_SCHEMA.

    Raises:
        VisNError: With code EXTRACTION_FAILED if the API call fails.
    """
    is_retry = retry_context is not None
    logger.info(
        "Calling Claude Vision API — retry={}", is_retry
    )

    # Build the prompt — append error context for retry attempts
    prompt = EXTRACTION_PROMPT
    if retry_context is not None:
        prompt = (
            f"{prompt}\n\n"
            f"PREVIOUS ATTEMPT HAD ERRORS:\n{retry_context}\n"
            "Please correct these issues."
        )

    # Base64-encode the image bytes
    image_b64 = base64.standard_b64encode(img_bytes).decode("utf-8")

    start = time.monotonic()
    try:
        response = await _get_client().messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                }
            ],
            output_config={
                "format": {
                    "type": "json_schema",
                    "schema": BOARD_SCHEMA,
                }
            },
        )
    except anthropic.APIError as exc:
        raise VisNError(EXTRACTION_FAILED, str(exc)) from exc
    except Exception as exc:
        raise VisNError(EXTRACTION_FAILED, str(exc)) from exc

    elapsed = time.monotonic() - start

    logger.info(
        "Claude Vision response received — latency={:.2f}s  "
        "input_tokens={}  output_tokens={}",
        elapsed,
        response.usage.input_tokens,
        response.usage.output_tokens,
    )

    return json.loads(response.content[0].text)
