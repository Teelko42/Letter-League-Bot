from __future__ import annotations

from collections import deque

from src.engine.tiles import ALPHABET
from src.vision.schema import OFFICIAL_MULTIPLIER_LAYOUT


def validate_extraction(data: dict) -> list[str]:
    """Validate extracted board state data against four checks.

    Checks (in order):
      1. Valid letters — every placed tile must have an A-Z letter.
      2. Connectivity — all placed tiles must form a single connected group
         (orthogonal adjacency). Uses flood-fill (BFS) to detect floating tiles.
      3. Multiplier positions — each tile's reported multiplier must match
         OFFICIAL_MULTIPLIER_LAYOUT (or NONE for positions not in the layout).
      4. Rack count and contents — at most 7 tiles, each A-Z or '?'.

    Args:
        data: Parsed JSON dict conforming to BOARD_SCHEMA.

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
        if cell["letter"] not in ALPHABET:
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

    return errors
