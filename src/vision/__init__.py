from __future__ import annotations

import re
import time

from loguru import logger

from src.engine.board import Board
from src.vision.errors import (
    EXTRACTION_FAILED,
    INVALID_SCREENSHOT,
    VALIDATION_FAILED,
    VisNError,
)
from src.vision.extractor import call_vision_api
from src.vision.preprocessor import preprocess_screenshot
from src.vision.schema import MULT_STR_TO_ENGINE, OFFICIAL_MULTIPLIER_LAYOUT
from src.vision.validator import validate_extraction

# Pre-compute the multiplier layout in engine format once at import time.
# Maps (row, col) -> MultiplierType for use when constructing Board instances.
_MULTIPLIER_LAYOUT_ENGINE = {
    pos: MULT_STR_TO_ENGINE[mult_str]
    for pos, mult_str in OFFICIAL_MULTIPLIER_LAYOUT.items()
}

_FLOATING_RE = re.compile(r"Floating tile '.+' at \((\d+), (\d+)\)")


def _log_extracted_state(data: dict) -> None:
    """Log the extracted board state at DEBUG level for diagnostics."""
    cells = data.get("board", {}).get("cells", [])
    rack = data.get("rack", [])
    if not cells:
        logger.debug("Vision extracted 0 cells")
        return
    # Build a compact representation: (row,col)=LETTER[mult]
    cell_strs = [
        f"({c['row']},{c['col']})={c['letter']}"
        f"{'*' if c.get('is_blank') else ''}"
        f"[{c.get('multiplier', '?')}]"
        for c in cells
    ]
    logger.debug("Vision extracted cells: {}", " ".join(cell_strs))
    logger.debug("Vision extracted rack: {}", rack)


def _remove_floating_tiles(data: dict, floating_errors: list[str]) -> None:
    """Remove floating tiles from extraction data so the pipeline can proceed."""
    coords_to_remove: set[tuple[int, int]] = set()
    for err in floating_errors:
        m = _FLOATING_RE.search(err)
        if m:
            coords_to_remove.add((int(m.group(1)), int(m.group(2))))
    if coords_to_remove:
        data["board"]["cells"] = [
            c for c in data["board"]["cells"]
            if (c["row"], c["col"]) not in coords_to_remove
        ]


__all__ = [
    "extract_board_state",
    "VisNError",
    "INVALID_SCREENSHOT",
    "EXTRACTION_FAILED",
    "VALIDATION_FAILED",
]


async def extract_board_state(
    img_bytes: bytes,
    mode: str = "classic",
) -> tuple[Board, list[str]]:
    """Extract board state from a Letter League screenshot.

    Runs the full vision pipeline:
      1. Preprocess: detect board region, crop, upscale 2x, clamp to 1568px.
      2. Extract: call Claude Vision API with structured output.
      3. Validate: run four-check validator (letters, connectivity, multipliers, rack).
      4. Retry: if validation fails, re-call the API with error context and validate again.
      5. Populate: build a Board object and extract the rack list.

    Args:
        img_bytes: Raw image bytes (PNG, JPEG, or any OpenCV-supported format).
        mode: Board tile placement mode — 'classic' or 'wild'. Passed through
            to Board.place_tile for each extracted tile.

    Returns:
        A tuple (board, rack) where:
          - board is a populated Board with all extracted tiles placed.
          - rack is a list of uppercase letter strings (may include '?' for blanks).

    Raises:
        VisNError(INVALID_SCREENSHOT): If preprocessing fails — image is not a
            recognizable Letter League screenshot.
        VisNError(EXTRACTION_FAILED): If the Claude Vision API call fails.
        VisNError(VALIDATION_FAILED): If extracted data fails validation even
            after one retry.
    """
    pipeline_start = time.monotonic()
    logger.info("Vision pipeline start — mode={}", mode)

    # ------------------------------------------------------------------
    # Step 1: Preprocess
    # ------------------------------------------------------------------
    processed_bytes = preprocess_screenshot(img_bytes)  # raises VisNError on failure
    logger.info("Preprocessing complete — {} bytes", len(processed_bytes))

    # ------------------------------------------------------------------
    # Step 2: Extract (first attempt)
    # ------------------------------------------------------------------
    data = await call_vision_api(processed_bytes)
    logger.info("Extraction complete (first attempt)")
    _log_extracted_state(data)

    # ------------------------------------------------------------------
    # Step 3: Validate
    # ------------------------------------------------------------------
    errors = validate_extraction(data)
    logger.info(
        "Validation result — {} error(s)",
        len(errors),
    )

    # ------------------------------------------------------------------
    # Step 4: Retry on failure
    # ------------------------------------------------------------------
    if errors:
        retry_context = "\n".join(errors)
        logger.warning(
            "Validation failed ({} errors), retrying: {}",
            len(errors),
            errors,
        )
        data = await call_vision_api(processed_bytes, retry_context=retry_context)
        logger.info("Extraction complete (retry)")
        _log_extracted_state(data)
        errors = validate_extraction(data)
        logger.info(
            "Validation result after retry — {} error(s)",
            len(errors),
        )
        if errors:
            # If the only remaining errors are floating tiles, remove them
            # and proceed — incomplete data is better than a total failure.
            floating_errors = [e for e in errors if "Floating tile" in e]
            non_floating = [e for e in errors if "Floating tile" not in e]
            if not non_floating and floating_errors:
                _remove_floating_tiles(data, floating_errors)
                logger.warning(
                    "Removed {} floating tile(s) to salvage extraction",
                    len(floating_errors),
                )
            else:
                raise VisNError(
                    VALIDATION_FAILED,
                    f"Validation failed after retry: {'; '.join(errors)}",
                )

    # ------------------------------------------------------------------
    # Step 5: Populate Board
    # ------------------------------------------------------------------
    board = Board(rows=19, cols=27, multiplier_layout=_MULTIPLIER_LAYOUT_ENGINE)

    for cell in data["board"]["cells"]:
        board.place_tile(
            row=cell["row"],
            col=cell["col"],
            letter=cell["letter"],
            is_blank=cell["is_blank"],
            mode=mode,
        )

    # ------------------------------------------------------------------
    # Step 6: Extract rack
    # ------------------------------------------------------------------
    rack: list[str] = data["rack"]

    elapsed = time.monotonic() - pipeline_start
    logger.info(
        "Vision pipeline complete — {:.2f}s  tiles={}  rack_size={}",
        elapsed,
        len(data["board"]["cells"]),
        len(rack),
    )

    return board, rack
