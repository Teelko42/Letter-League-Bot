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
    # Check 3 — Multiplier positions match official layout
    # ------------------------------------------------------------------
    for cell in cells:
        row, col = cell["row"], cell["col"]
        expected = OFFICIAL_MULTIPLIER_LAYOUT.get((row, col), "NONE")
        if cell["multiplier"] != expected:
            errors.append(
                f"Multiplier mismatch at ({row}, {col}): "
                f"got {cell['multiplier']}, expected {expected}"
            )

    # ------------------------------------------------------------------
    # Check 4 — Rack count <= 7 and valid rack tile characters
    # ------------------------------------------------------------------
    if len(rack) > 7:
        errors.append(f"Rack has {len(rack)} tiles (max 7)")

    valid_rack_chars = ALPHABET + "?"
    for tile in rack:
        if tile not in valid_rack_chars:
            errors.append(f"Invalid rack tile '{tile}'")

    return errors
