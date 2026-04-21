from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from loguru import logger

from src.engine.tiles import ALPHABET
from src.vision.schema import OFFICIAL_MULTIPLIER_LAYOUT

if TYPE_CHECKING:
    from src.engine.gaddag import GADDAG


def correct_positions(data: dict) -> None:
    """Auto-correct tile positions using multiplier alignment.

    The vision API sometimes miscounts absolute positions by 1-3 cells while
    correctly identifying the multiplier colours underneath tiles.  This
    function tries all (row, col) shifts in [-3, +3] and applies the shift
    that best aligns the *reported* multipliers with the official layout.

    Must be called **before** ``validate_extraction``, which overwrites the
    reported multipliers with expected values (destroying the signal).

    Modifies *data* in-place.  No-op when shifting cannot improve alignment.
    """
    cells = data["board"]["cells"]
    if not cells:
        return

    def _mult_score(dr: int, dc: int) -> tuple[int, int]:
        """Return (matches, informative) for a global shift of *(dr, dc)*.

        Uses binary presence matching: a tile "matches" if the Vision API
        reported a non-NONE multiplier AND the official layout also has a
        non-NONE multiplier at the shifted position.  Only tiles where the
        Vision API actively reported a color are counted — tiles reporting
        NONE are excluded because placed tiles often cover the multiplier
        square's color, making NONE reports ambiguous.  Binary matching
        (rather than exact type matching) is used because the Vision API
        reliably detects multiplier *presence* but frequently confuses
        specific types (e.g. DW vs TL).
        """
        matches = 0
        informative = 0
        for cell in cells:
            row, col = cell["row"] + dr, cell["col"] + dc
            if not (0 <= row <= 18 and 0 <= col <= 26):
                return -1, 0  # shift pushes tiles out of bounds
            expected = OFFICIAL_MULTIPLIER_LAYOUT.get((row, col), "NONE")
            reported = cell["multiplier"]
            # Only count tiles where Vision actively detected a multiplier.
            if reported != "NONE":
                informative += 1
                if expected != "NONE":
                    matches += 1
        return matches, informative

    curr_matches, curr_info = _mult_score(0, 0)
    if curr_info == 0 or curr_matches == curr_info:
        return  # already perfect or no multiplier info to anchor on

    best_dr, best_dc = 0, 0
    best_matches = curr_matches

    for dr in range(-3, 4):
        for dc in range(-3, 4):
            if dr == 0 and dc == 0:
                continue
            matches, _ = _mult_score(dr, dc)
            if matches > best_matches:
                best_dr, best_dc = dr, dc
                best_matches = matches

    if best_dr == 0 and best_dc == 0:
        return  # no shift improves alignment

    # Require strong evidence before applying a shift: at least 2 multiplier
    # matches AND more than half of informative cells must agree.  Without
    # this threshold, a single coincidental match can shift the entire board
    # to wrong positions (e.g. a (-3,-3) shift that makes everything worse).
    #
    # Exception: for small shifts (|dr|+|dc| <= 1), a single multiplier match
    # is strong evidence — a ±1 cell drift is the most common vision error,
    # and a coincidental match at ±1 is unlikely.  Large shifts still require
    # ≥2 matches to prevent false corrections.
    is_small_shift = abs(best_dr) + abs(best_dc) <= 1
    min_matches = 1 if is_small_shift else 2

    if best_matches < min_matches or best_matches / curr_info < 0.5:
        logger.debug(
            "Position auto-correction skipped: insufficient evidence "
            "(matches={}, informative={}, threshold={} or 50%)",
            best_matches,
            curr_info,
            min_matches,
        )
        return

    logger.info(
        "Position auto-correction: shifting tiles by ({:+d}, {:+d}) — "
        "multiplier matches {} → {}",
        best_dr,
        best_dc,
        curr_matches,
        best_matches,
    )

    for cell in cells:
        cell["row"] += best_dr
        cell["col"] += best_dc

    # Update bounding box
    rows = [c["row"] for c in cells]
    cols = [c["col"] for c in cells]
    data["board"]["min_row"] = min(rows)
    data["board"]["max_row"] = max(rows)
    data["board"]["min_col"] = min(cols)
    data["board"]["max_col"] = max(cols)


def correct_positions_center_star(data: dict) -> None:
    """Correct positions for single-word boards using the center star constraint.

    In Letter League the first word must cross the center star at (9, 13).
    If the extracted tiles form a single run and none occupies (9, 13), the
    positions are definitely wrong.  This function tries each shift that
    would place one tile on (9, 13) and picks the one with the best
    multiplier alignment.  On a tie, prefers the smallest shift.

    Must be called **after** ``correct_positions`` (which handles the general
    case) and only matters when ``correct_positions`` had insufficient
    evidence to correct a drift.

    Modifies *data* in-place.  No-op when:
    - Board is empty or has < 2 tiles.
    - A tile already occupies (9, 13).
    - Tiles form more than one disconnected run (not a first-word board).
    """
    cells = data["board"]["cells"]
    if not cells or len(cells) < 2:
        return

    positions = {(c["row"], c["col"]) for c in cells}
    if (9, 13) in positions:
        return  # center star already occupied

    # Only apply for single runs (the first word on an otherwise empty board).
    runs = _find_tile_runs(cells)
    if len(runs) != 1:
        return

    best_dr, best_dc = 0, 0
    best_score = -1

    for cell in cells:
        dr = 9 - cell["row"]
        dc = 13 - cell["col"]
        if dr == 0 and dc == 0:
            continue

        # All tiles must stay in bounds after the shift.
        if not all(
            0 <= c["row"] + dr <= 18 and 0 <= c["col"] + dc <= 26
            for c in cells
        ):
            continue

        # Score: multiplier alignment with official layout.
        score = 0
        for c in cells:
            r, co = c["row"] + dr, c["col"] + dc
            expected = OFFICIAL_MULTIPLIER_LAYOUT.get((r, co), "NONE")
            reported = c["multiplier"]
            if reported == expected:
                score += 2
            elif reported != "NONE" and expected != "NONE":
                score += 1  # type mismatch but both non-NONE

        # Prefer smallest shift on tie.
        shift_mag = abs(dr) + abs(dc)
        if score > best_score or (
            score == best_score
            and shift_mag < abs(best_dr) + abs(best_dc)
        ):
            best_score = score
            best_dr, best_dc = dr, dc

    if best_dr == 0 and best_dc == 0:
        return

    logger.info(
        "Center star correction: shifting tiles by ({:+d}, {:+d}) "
        "to place a tile on (9,13) — multiplier score {}",
        best_dr,
        best_dc,
        best_score,
    )
    for cell in cells:
        cell["row"] += best_dr
        cell["col"] += best_dc

    # Update bounding-box metadata.
    rows = [c["row"] for c in cells]
    cols = [c["col"] for c in cells]
    data["board"]["min_row"] = min(rows)
    data["board"]["max_row"] = max(rows)
    data["board"]["min_col"] = min(cols)
    data["board"]["max_col"] = max(cols)


def _count_valid_word_runs(cells: list[dict], gaddag: "GADDAG", dr: int, dc: int) -> int:
    """Count how many tile runs form valid dictionary words at a given (dr, dc) shift.

    Used by correct_positions_gaddag to score candidate global shifts.  Only
    tiles that remain in-bounds after the shift are included.

    Args:
        cells: List of cell dicts from the extraction (unmodified).
        gaddag: GADDAG instance for word lookups.
        dr:     Row shift to apply.
        dc:     Column shift to apply.

    Returns:
        Number of tile runs (of length >= 2) that are valid GADDAG words at this
        shift.  Single-tile cells that form no multi-tile runs are not counted.
    """
    # Build a shifted grid, dropping out-of-bounds cells.
    grid: dict[tuple[int, int], str] = {}
    for cell in cells:
        r, c = cell["row"] + dr, cell["col"] + dc
        if 0 <= r <= 18 and 0 <= c <= 26:
            grid[(r, c)] = cell["letter"]

    valid_count = 0

    for (r, c) in sorted(grid):
        # Horizontal run starting at this cell
        if (r, c - 1) not in grid:
            run: list[str] = []
            cc = c
            while (r, cc) in grid:
                run.append(grid[(r, cc)])
                cc += 1
            if len(run) >= 2 and gaddag.is_valid_word("".join(run)):
                valid_count += 1

        # Vertical run starting at this cell
        if (r - 1, c) not in grid:
            run = []
            rr = r
            while (rr, c) in grid:
                run.append(grid[(rr, c)])
                rr += 1
            if len(run) >= 2 and gaddag.is_valid_word("".join(run)):
                valid_count += 1

    return valid_count


def correct_positions_gaddag(data: dict, gaddag: "GADDAG") -> None:
    """Auto-correct tile positions using word-validity scoring as the signal.

    Complements :func:`correct_positions` (which uses multiplier colours).
    When tiles cover most multiplier squares the multiplier-based function
    cannot detect drift.  This function instead tries all global (row, col)
    shifts in ``[-2, +2]`` and picks the one under which the most tile runs
    form valid dictionary words.

    Only runs when:
    - At least two tile runs of length >= 2 exist (single-word boards have
      only one run; a uniform shift cannot be detected from one word alone).
    - The best candidate shift strictly increases the count of valid runs
      compared to the current positions.

    Must be called **before** ``validate_extraction``, which does not shift
    tiles.  Call **after** ``correct_positions`` so that multiplier-based
    correction has already been applied if possible.

    Modifies *data* in-place.  No-op when no shift improves validity.
    """
    cells = data["board"]["cells"]
    if not cells:
        return

    # Tally existing runs to see if there is multi-run signal.
    runs_at_zero = _find_tile_runs(cells)
    if len(runs_at_zero) < 2:
        # Single word (or no runs) — cannot distinguish drift from a uniform
        # shift by word validity alone, because the word stays valid at any
        # shift that keeps its letters consecutive.
        return

    current_valid = sum(
        1 for word, _ in runs_at_zero if gaddag.is_valid_word(word)
    )
    total_runs = len(runs_at_zero)

    # Already perfect — nothing to correct.
    if current_valid == total_runs:
        return

    best_dr, best_dc = 0, 0
    best_valid = current_valid

    for dr in range(-2, 3):
        for dc in range(-2, 3):
            if dr == 0 and dc == 0:
                continue
            score = _count_valid_word_runs(cells, gaddag, dr, dc)
            if score > best_valid:
                best_valid = score
                best_dr, best_dc = dr, dc

    if best_dr == 0 and best_dc == 0:
        logger.debug(
            "GADDAG position correction: no shift improves word validity "
            "(current {}/{} valid runs)",
            current_valid,
            total_runs,
        )
        return

    logger.info(
        "GADDAG position correction: shifting tiles by ({:+d}, {:+d}) — "
        "valid runs {} → {} (out of {})",
        best_dr,
        best_dc,
        current_valid,
        best_valid,
        total_runs,
    )

    for cell in cells:
        cell["row"] += best_dr
        cell["col"] += best_dc

    # Update bounding box metadata.
    rows = [c["row"] for c in cells]
    cols = [c["col"] for c in cells]
    data["board"]["min_row"] = min(rows)
    data["board"]["max_row"] = max(rows)
    data["board"]["min_col"] = min(cols)
    data["board"]["max_col"] = max(cols)


def _find_tile_runs(cells: list[dict]) -> list[tuple[str, str]]:
    """Find all horizontal and vertical runs of 2+ consecutive tiles.

    Returns a list of (word, location_description) tuples.
    """
    grid: dict[tuple[int, int], str] = {}
    for cell in cells:
        grid[(cell["row"], cell["col"])] = cell["letter"]

    words: list[tuple[str, str]] = []

    for (r, c) in sorted(grid):
        # Horizontal run starting at this cell (no tile to the left)
        if (r, c - 1) not in grid:
            run: list[str] = []
            cc = c
            while (r, cc) in grid:
                run.append(grid[(r, cc)])
                cc += 1
            if len(run) >= 2:
                words.append(("".join(run), f"row {r} cols {c}-{cc - 1}"))

        # Vertical run starting at this cell (no tile above)
        if (r - 1, c) not in grid:
            run = []
            rr = r
            while (rr, c) in grid:
                run.append(grid[(rr, c)])
                rr += 1
            if len(run) >= 2:
                words.append(("".join(run), f"col {c} rows {r}-{rr - 1}"))

    return words


def validate_extraction(
    data: dict,
    gaddag: GADDAG | None = None,
) -> list[str]:
    """Validate extracted board state data against five checks.

    Checks (in order):
      1. Valid letters — every placed tile must have an A-Z letter.
      2. Connectivity — all placed tiles must form a single connected group
         (orthogonal adjacency). Uses flood-fill (BFS) to detect floating tiles.
      3. Multiplier positions — each tile's reported multiplier must match
         OFFICIAL_MULTIPLIER_LAYOUT (or NONE for positions not in the layout).
      4. Rack count and contents — at most 7 tiles, each A-Z or '?'.
      5. Word validity — every horizontal/vertical run of 2+ tiles must form
         a valid dictionary word (requires gaddag parameter).

    Args:
        data: Parsed JSON dict conforming to BOARD_SCHEMA.
        gaddag: Optional GADDAG dictionary for word validation.

    Returns:
        List of error message strings. An empty list means all checks passed.
    """
    errors: list[str] = []
    cells = data["board"]["cells"]
    rack = data["rack"]

    # ------------------------------------------------------------------
    # Check 0 — Duplicate positions / out-of-bounds coordinates
    # ------------------------------------------------------------------
    seen_positions: set[tuple[int, int]] = set()
    for cell in cells:
        pos = (cell["row"], cell["col"])
        if pos in seen_positions:
            errors.append(
                f"Duplicate tile at ({cell['row']}, {cell['col']}) — "
                f"two tiles cannot occupy the same cell"
            )
        seen_positions.add(pos)

        # Bounds check: 19 rows (0-18), 27 cols (0-26)
        if not (0 <= cell["row"] <= 18 and 0 <= cell["col"] <= 26):
            errors.append(
                f"Tile '{cell['letter']}' at ({cell['row']}, {cell['col']}) "
                f"is outside the 19x27 board"
            )

    # ------------------------------------------------------------------
    # Check 1 — Valid letters (A-Z only)
    # ------------------------------------------------------------------
    for cell in cells:
        if len(cell["letter"]) != 1 or cell["letter"] not in ALPHABET:
            errors.append(
                f"Invalid letter '{cell['letter']}' at ({cell['row']}, {cell['col']})"
            )

    # ------------------------------------------------------------------
    # Check 2 — Connectivity (flood-fill from first tile)
    # ------------------------------------------------------------------
    placed: set[tuple[int, int]] = {(cell["row"], cell["col"]) for cell in cells}

    if len(placed) > 1:
        # BFS from the first tile in the set
        start = next(iter(placed))
        visited: set[tuple[int, int]] = set()
        queue: deque[tuple[int, int]] = deque([start])
        visited.add(start)

        while queue:
            r, c = queue.popleft()
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                neighbor = (r + dr, c + dc)
                if neighbor in placed and neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        # Any tile in placed but not visited is floating
        floating = placed - visited
        if floating:
            # Build a lookup from (row, col) -> letter for readable error messages
            coord_to_letter = {(cell["row"], cell["col"]): cell["letter"] for cell in cells}
            for r, c in sorted(floating):
                letter = coord_to_letter.get((r, c), "?")
                errors.append(
                    f"Floating tile '{letter}' at ({r}, {c}) — not connected to other tiles"
                )

    # ------------------------------------------------------------------
    # Check 3 — Multiplier positions: detect coordinate accuracy issues
    # ------------------------------------------------------------------
    # Compare vision-reported multipliers against the official layout.
    # Mismatches on non-NONE squares are a strong signal that the Vision API
    # miscounted positions. If too many tiles on multiplier squares have
    # the wrong multiplier, flag it as a position accuracy error.
    #
    # The engine uses the official layout regardless, so we auto-correct
    # after checking.
    mult_check_total = 0   # tiles where reported OR expected multiplier is non-NONE
    mult_check_wrong = 0   # tiles where reported != expected among those

    for cell in cells:
        row, col = cell["row"], cell["col"]
        expected = OFFICIAL_MULTIPLIER_LAYOUT.get((row, col), "NONE")
        reported = cell["multiplier"]

        # Only count cells where at least one side is non-NONE (informative)
        if reported != "NONE" or expected != "NONE":
            mult_check_total += 1
            if reported != expected:
                mult_check_wrong += 1

        if reported != expected:
            cell["multiplier"] = expected

    # If more than half of informative multiplier checks fail, positions
    # are likely wrong — report as a validation error to trigger a retry.
    if mult_check_total >= 2 and mult_check_wrong / mult_check_total > 0.5:
        errors.append(
            f"Position accuracy suspect: {mult_check_wrong}/{mult_check_total} "
            f"multiplier mismatches — tile coordinates may be off. "
            f"Re-count positions using the center star at (9,13) as reference."
        )

    # ------------------------------------------------------------------
    # Check 4 — Rack count (1-7) and valid rack tile characters
    # ------------------------------------------------------------------
    if len(rack) == 0:
        errors.append("Rack is empty — the player's tile rack should have at least 1 tile")

    if len(rack) > 7:
        errors.append(f"Rack has {len(rack)} tiles (max 7)")

    valid_rack_chars = ALPHABET + "?"
    for tile in rack:
        if tile not in valid_rack_chars:
            errors.append(f"Invalid rack tile '{tile}'")

    # ------------------------------------------------------------------
    # Check 5 — Word validity (requires GADDAG)
    # ------------------------------------------------------------------
    # Every horizontal/vertical run of 2+ consecutive tiles on the board
    # must be a valid dictionary word. Invalid sequences are a strong
    # signal that tile positions are off by 1.
    if gaddag is not None:
        runs = _find_tile_runs(cells)
        invalid = [(word, loc) for word, loc in runs if not gaddag.is_valid_word(word)]
        if invalid:
            invalid_strs = [f"'{w}' at {loc}" for w, loc in invalid]
            errors.append(
                f"Invalid word(s) on board: {', '.join(invalid_strs)} — "
                f"tile positions are likely off by 1. Re-count carefully "
                f"from center star at (9,13)."
            )

    return errors
