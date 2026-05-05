from __future__ import annotations

import re
import time
from collections import Counter
from typing import TYPE_CHECKING

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
from src.vision.validator import correct_positions, correct_positions_center_star, correct_positions_gaddag, validate_extraction

if TYPE_CHECKING:
    from src.engine.gaddag import GADDAG

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


def _strip_empty_cells(data: dict) -> None:
    """Drop cells with empty letter strings from extraction data in-place.

    Claude Vision sometimes returns the center-star position as a cell with
    letter="" to acknowledge "I see the star here, no tile on it".  Keeping
    such cells breaks downstream assumptions: the validator flags them as
    invalid letters, and the retry-merge logic re-adds them on every pass.
    The board population step already skips empty-letter cells, so dropping
    them here is a strict no-op for legitimate extractions.
    """
    cells = data.get("board", {}).get("cells", [])
    filtered = [c for c in cells if c.get("letter")]
    if len(filtered) != len(cells):
        data["board"]["cells"] = filtered


def _detect_uniform_shift(
    first_cells: list[dict],
    retry_cells: list[dict],
) -> tuple[int, int] | None:
    """Detect whether ``retry_cells`` is a uniform translation of ``first_cells``.

    The Vision API often re-reads the board with every tile shifted by 1-3
    cells in either direction — same letters, same relative layout, just
    anchored to a different origin.  Both reads are equally valid views of
    the same physical tiles, so the merge-back logic in ``extract_board_state``
    must not treat the first read's cells as "dropped" when this happens
    (re-adding them creates phantom duplicates that pollute engine state).

    Returns the dominant ``(dr, dc)`` if the retry is a clear uniform shift
    of the first attempt, else ``None``.  "Clear" means: at least 60% of
    first-attempt cells have a same-letter retry counterpart at a single
    consistent ``(dr, dc)``, and at least 2 cells participate in the agreement
    (single-letter shifts are too coincidental to act on).
    """
    if len(first_cells) < 2 or len(retry_cells) < 2:
        return None

    # Build a letter -> [retry positions] index for fast lookup.
    by_letter: dict[str, list[tuple[int, int]]] = {}
    for rc in retry_cells:
        by_letter.setdefault(rc["letter"], []).append((rc["row"], rc["col"]))

    deltas: Counter[tuple[int, int]] = Counter()
    for fc in first_cells:
        candidates = by_letter.get(fc["letter"])
        if not candidates:
            continue
        # Pick the closest retry cell with matching letter — minimises
        # spurious cross-pairings when a letter appears multiple times.
        closest = min(
            candidates,
            key=lambda rp: abs(rp[0] - fc["row"]) + abs(rp[1] - fc["col"]),
        )
        deltas[(closest[0] - fc["row"], closest[1] - fc["col"])] += 1

    if not deltas:
        return None

    (dr, dc), count = deltas.most_common(1)[0]
    threshold = max(2, int(len(first_cells) * 0.6))
    if count >= threshold:
        return (dr, dc)
    return None


def _anchor_to_known_tiles(
    data: dict,
    known_tiles: dict[tuple[int, int], str],
) -> None:
    """Authoritatively pin known-correct tiles into the vision data.

    For every position the bot has previously placed and had accepted, drop
    whatever vision currently thinks is at that position and re-inject the
    known ``(row, col, letter)`` tile. Cells vision reports at any other
    position are kept — they're the bot's best guess at opponent's tiles.

    Why this is the right shape rather than a global shift correction:
    in real failure cases the drift on dense boards is *not* uniform — one
    word may be misread as ``(-1, -2)`` while another adjacent word is
    ``(-1, 0)``. A single global shift fixes one and breaks the other.
    Pinning known cells in place is unconditionally correct; remaining
    vision cells (opponent's tiles) keep whatever positional error vision
    introduced, but they are the minority and the engine can still build
    moves through the dense block of authoritatively-positioned anchors.

    Also drops any vision cell that conflicts with a *non-anchored*
    known-position — defensive, since duplicates would later cause the
    Board.place_tile call to overwrite our anchor.
    """
    cells = data["board"]["cells"]
    known_positions = set(known_tiles.keys())

    # Step A: identify vision cells that are likely *drifted views* of our
    # known tiles. For each known tile, the same-letter vision cell closest
    # to its known position (within a 5-cell manhattan radius) is treated
    # as a duplicate of that tile and dropped. Without this, a known
    # tile pinned at (9,15) would coexist with vision's drifted copy at,
    # say, (8,13) and the engine would see the same letter twice.
    duplicates: set[int] = set()
    claimed: set[int] = set()
    for (kr, kc), kletter in known_tiles.items():
        best_id = None
        best_dist = 6
        for c in cells:
            if id(c) in claimed:
                continue
            if c["letter"] != kletter:
                continue
            dist = abs(c["row"] - kr) + abs(c["col"] - kc)
            if dist < best_dist:
                best_dist = dist
                best_id = id(c)
        if best_id is not None:
            duplicates.add(best_id)
            claimed.add(best_id)

    overwritten = 0
    kept: list[dict] = []
    for c in cells:
        pos = (c["row"], c["col"])
        if id(c) in duplicates:
            continue
        if pos in known_positions:
            if c["letter"] != known_tiles[pos]:
                overwritten += 1
            continue  # also drop — we'll inject the authoritative version below
        kept.append(c)

    # Step B: inject authoritative known tiles.
    injected = 0
    for (row, col), letter in known_tiles.items():
        kept.append({
            "row": row, "col": col, "letter": letter,
            "is_blank": False, "multiplier": "NONE",
        })
        injected += 1

    data["board"]["cells"] = kept

    if injected or overwritten or duplicates:
        logger.info(
            "Vision anchor: pinned {} known tile(s); dropped {} drifted "
            "duplicate(s); corrected {} vision letter(s) at known positions.",
            injected, len(duplicates), overwritten,
        )


def _normalize_letters(data: dict) -> None:
    """Normalize letter strings on board cells and rack tiles in-place.

    The Vision API occasionally pads single-letter strings with leading or
    trailing whitespace ("' L'", "' F'") and rarely returns lowercase.  The
    validator's character-set check is strict (A-Z plus '?'), so these
    cosmetic artefacts are reported as "Invalid rack tile" / "Invalid letter"
    — *hard* errors that block the floating-tile / soft-error recovery path
    and force the turn to be skipped entirely.  Stripping + upper-casing
    here is a no-op for clean extractions.
    """
    for cell in data.get("board", {}).get("cells", []):
        letter = cell.get("letter", "")
        if isinstance(letter, str):
            cell["letter"] = letter.strip().upper()
    rack = data.get("rack")
    if isinstance(rack, list):
        data["rack"] = [
            tile.strip().upper() if isinstance(tile, str) else tile
            for tile in rack
        ]


__all__ = [
    "extract_board_state",
    "VisNError",
    "INVALID_SCREENSHOT",
    "EXTRACTION_FAILED",
    "VALIDATION_FAILED",
    "correct_positions_gaddag",
]


async def extract_board_state(
    img_bytes: bytes,
    mode: str = "classic",
    gaddag: GADDAG | None = None,
    known_tiles: dict[tuple[int, int], str] | None = None,
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
        known_tiles: Optional ``{(row, col): letter}`` of tiles the bot has
            already confirmed on the board (from previous accepted moves).
            Used as anchor points: the pipeline detects whether the Vision
            API's read is uniformly shifted relative to these known-correct
            positions and applies the inverse shift, then authoritatively
            overwrites cells at known positions with their known letters.
            This stops vision drift on dense boards from feeding the engine
            a phantom board state, which was the dominant cause of "valid
            words rejected" turns (the engine generates a play valid in
            its drifted view, but Letter League rejects it because the real
            board doesn't match).

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

    # Strip cells with empty letters — Claude Vision occasionally reports the
    # center-star cell (9,13) as a cell with letter="".  Board.place_tile
    # already skips such cells, but validation flags them as "Invalid letter
    # ''", and the retry-merge logic re-adds them to every subsequent pass,
    # causing a hard validation failure for every turn.
    _strip_empty_cells(data)
    _normalize_letters(data)

    # ------------------------------------------------------------------
    # Step 3: Auto-correct positions & Validate
    # ------------------------------------------------------------------
    correct_positions(data)
    correct_positions_center_star(data)
    if gaddag is not None:
        correct_positions_gaddag(data, gaddag)
    errors = validate_extraction(data, gaddag=gaddag)
    logger.info(
        "Validation result — {} error(s)",
        len(errors),
    )

    # ------------------------------------------------------------------
    # Step 4: Retry on failure
    # ------------------------------------------------------------------
    if errors:
        # Save first attempt cells (post-correction) for merge-back if retry
        # drops tiles.  The retry often "fixes" an invalid word by removing a
        # misread tile, but the tile IS real — only its letter was wrong.
        # Preserving it lets the engine know there's a tile at that position
        # (critical for cross-word validation).
        first_attempt_cells = [dict(c) for c in data["board"]["cells"]]
        first_attempt_rack = list(data["rack"])

        # Strip "Rack is empty" from retry context.  Telling Claude the rack
        # must have ≥1 tile pressures it to invent rack letters by copying
        # from the board — an observed failure mode where a genuinely-empty
        # rack (end-of-game or all-tiles-just-consumed state) gets replaced
        # by phantom tiles that the engine then tries and fails to play.
        retry_errors = [e for e in errors if "Rack is empty" not in e]

        if retry_errors:
            retry_context = "\n".join(retry_errors)
            logger.warning(
                "Validation failed ({} errors), retrying: {}",
                len(errors),
                errors,
            )
            data = await call_vision_api(processed_bytes, retry_context=retry_context)
            logger.info("Extraction complete (retry)")
            _log_extracted_state(data)
            _strip_empty_cells(data)
            _normalize_letters(data)
            correct_positions(data)
            correct_positions_center_star(data)
            if gaddag is not None:
                correct_positions_gaddag(data, gaddag)

            # Merge back cells that the retry dropped.  The first attempt often
            # identifies the correct number of tiles even if it misreads a letter;
            # the retry may drop that tile to satisfy word validation, losing the
            # position entirely.  Re-adding the cell ensures the engine checks
            # cross-words at that column/row.
            #
            # Shift guard: if the retry is a uniform translation of the first
            # attempt (same letters, shifted by a consistent (dr, dc)), every
            # first-attempt cell at the *original* end of the run will look
            # "dropped" by simple position comparison — re-adding them creates
            # phantom duplicates (e.g., first sees 'COB PEEL', retry sees 'COB
            # PEE' shifted left, merge produces 'COBB PEELL' which the engine
            # plays against). Detect the shift first and skip the merge in
            # that case; the retry already represents the same tiles.
            shift = _detect_uniform_shift(first_attempt_cells, data["board"]["cells"])
            if shift is not None and shift != (0, 0):
                logger.info(
                    "Retry is a uniform ({:+d}, {:+d}) shift of first attempt "
                    "— skipping merge to avoid duplicate-tile phantoms.",
                    shift[0], shift[1],
                )
            else:
                retry_positions = {(c["row"], c["col"]) for c in data["board"]["cells"]}
                dropped = [c for c in first_attempt_cells if (c["row"], c["col"]) not in retry_positions]
                if dropped:
                    for cell in dropped:
                        data["board"]["cells"].append(cell)
                    logger.info(
                        "Merged {} cell(s) from first attempt that retry dropped: {}",
                        len(dropped),
                        [(c["letter"], c["row"], c["col"]) for c in dropped],
                    )

            # Hallucination guard: if the first attempt saw an empty rack but
            # the retry returned tiles drawn entirely from the board's letter
            # multiset, treat the retry rack as invented and reset to empty.
            # Real rack tiles come from the bag and will not perfectly match
            # what's already on the board — this pattern is Claude papering
            # over the "missing rack" hint by re-reading board letters.
            if not first_attempt_rack and data["rack"]:
                board_counts: Counter[str] = Counter(
                    c["letter"] for c in data["board"]["cells"]
                )
                rack_counts: Counter[str] = Counter(data["rack"])
                if all(
                    rack_counts[l] <= board_counts.get(l, 0)
                    for l in rack_counts
                ):
                    logger.warning(
                        "Retry rack {} appears hallucinated from board "
                        "letters — discarding and treating rack as empty",
                        data["rack"],
                    )
                    data["rack"] = []

            errors = validate_extraction(data, gaddag=gaddag)
            logger.info(
                "Validation result after retry — {} error(s)",
                len(errors),
            )
        else:
            logger.info(
                "Skipping retry — only error is empty rack (soft). "
                "Proceeding with first-attempt extraction."
            )
        if errors:
            # Categorise errors by severity — some are recoverable.
            floating_errors = [e for e in errors if "Floating tile" in e]
            rack_empty_errors = [e for e in errors if "Rack is empty" in e]
            word_errors = [e for e in errors if "Invalid word(s) on board" in e]
            # Position accuracy errors are caused by the same position drift as
            # word errors — both are soft after retry.  The validator already
            # overwrites multiplier values with the official layout (line 249 of
            # validator.py), so the engine is never affected by the mismatch.
            position_errors = [e for e in errors if "Position accuracy suspect" in e]
            hard_errors = [
                e for e in errors
                if "Floating tile" not in e
                and "Rack is empty" not in e
                and "Invalid word(s) on board" not in e
                and "Position accuracy suspect" not in e
            ]

            # Remove floating tiles if that's the only hard issue
            if floating_errors and not hard_errors:
                _remove_floating_tiles(data, floating_errors)
                logger.warning(
                    "Removed {} floating tile(s) to salvage extraction",
                    len(floating_errors),
                )

            # Empty rack is a soft error — log a warning but don't fail.
            # The game loop handles empty rack by swapping tiles.
            if rack_empty_errors and not hard_errors:
                logger.warning(
                    "Rack is empty — proceeding with board-only extraction. "
                    "Game may be in lobby or end-of-game state."
                )

            # Word validity errors are soft on multi-word boards — Vision API
            # position imprecision on crowded boards can produce invalid word
            # strings even when the extraction is structurally correct.  Log a
            # warning and proceed; the engine operates on coordinates, not the
            # string form, so small position drift is tolerable.
            if word_errors and not hard_errors:
                logger.warning(
                    "Word validity check failed ({} word(s)) after retry — "
                    "proceeding with best-effort extraction: {}",
                    len(word_errors),
                    word_errors,
                )

            # Position accuracy errors share the same root cause as word errors
            # (global position drift).  The multiplier values are already auto-
            # corrected by the validator, so this is a diagnostic warning only.
            if position_errors and not hard_errors:
                logger.warning(
                    "Position accuracy check failed after retry — "
                    "proceeding with auto-corrected multipliers: {}",
                    position_errors,
                )

            if hard_errors:
                raise VisNError(
                    VALIDATION_FAILED,
                    f"Validation failed after retry: {'; '.join(errors)}",
                )

    # ------------------------------------------------------------------
    # Step 4.5: Anchor cells against known-correct placements
    # ------------------------------------------------------------------
    # `known_tiles` is the bot's authoritative record of past accepted plays —
    # we know the EXACT (row, col, letter) of every tile we've placed and had
    # accepted by Letter League. Vision frequently drifts (off by 1-3 cells)
    # on dense boards, which makes the engine generate plays that are valid
    # in vision-space but invalid in reality-space (e.g., engine plays a
    # cross-word using a tile vision claims is at (8,14) but is actually at
    # (9,16); LL rejects).
    #
    # Two-pass correction:
    #   1. Diff vision's read against `known_tiles` to detect a global shift.
    #      Apply the inverse shift to ALL vision cells (so opponent tiles
    #      also get corrected — they drift the same amount as ours).
    #   2. Authoritatively overwrite every known cell: replace any vision
    #      cell at a known position, drop vision cells that conflict with
    #      a known tile's position, and inject the known tile if vision
    #      missed it entirely. This guarantees the engine sees our tiles
    #      where they actually are, regardless of any residual vision error.
    if known_tiles:
        _anchor_to_known_tiles(data, known_tiles)

    # ------------------------------------------------------------------
    # Step 5: Populate Board
    # ------------------------------------------------------------------
    board = Board(rows=19, cols=27, multiplier_layout=_MULTIPLIER_LAYOUT_ENGINE)

    for cell in data["board"]["cells"]:
        if not cell["letter"]:  # skip center-star / empty cells
            continue
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
