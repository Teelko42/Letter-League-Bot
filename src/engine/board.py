from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from src.engine.models import Cell, MultiplierType
from src.engine.tiles import ALPHABET

if TYPE_CHECKING:
    from src.engine.gaddag import GADDAG


class Board:
    """Represents the game board state with multiplier layout, tile placement,
    and precomputation methods for move generation (anchors, cross-checks,
    left-limits).

    The board is a configurable grid of Cell objects. The default size is
    19 rows x 27 columns per Letter League's board layout.
    """

    DEFAULT_ROWS = 19
    DEFAULT_COLS = 27

    def __init__(
        self,
        rows: int = DEFAULT_ROWS,
        cols: int = DEFAULT_COLS,
        multiplier_layout: dict[tuple[int, int], MultiplierType] | None = None,
    ) -> None:
        """Initialize the board.

        Args:
            rows: Number of rows. Defaults to 19.
            cols: Number of columns. Defaults to 27.
            multiplier_layout: Optional dict mapping (row, col) to MultiplierType.
                Cells not in the dict default to MultiplierType.NONE.
        """
        self.rows = rows
        self.cols = cols
        self._multiplier_layout: dict[tuple[int, int], MultiplierType] = multiplier_layout or {}
        self.grid: list[list[Cell]] = [
            [
                Cell(r, c, square_multiplier=self._multiplier_layout.get((r, c), MultiplierType.NONE))
                for c in range(cols)
            ]
            for r in range(rows)
        ]

    # ------------------------------------------------------------------
    # Cell access
    # ------------------------------------------------------------------

    def get_cell(self, row: int, col: int) -> Cell:
        """Return the Cell at (row, col).

        Raises:
            IndexError: If (row, col) is outside the board boundaries.
        """
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            raise IndexError(
                f"Cell ({row}, {col}) out of bounds for {self.rows}x{self.cols} board"
            )
        return self.grid[row][col]

    # ------------------------------------------------------------------
    # Tile placement
    # ------------------------------------------------------------------

    def place_tile(
        self,
        row: int,
        col: int,
        letter: str,
        is_blank: bool = False,
        mode: str = 'classic',
    ) -> None:
        """Place a tile on the board.

        Args:
            row: Row index.
            col: Column index.
            letter: The letter to place (will be uppercased).
            is_blank: True if this is a blank tile (worth 0 pts).
            mode: 'classic' (no bonding) or 'wild' (bonds the square multiplier
                to the tile permanently).
        """
        cell = self.get_cell(row, col)
        cell.letter = letter.upper()
        cell.is_blank = is_blank
        if mode == 'wild':
            cell.bonded_multiplier = cell.square_multiplier

    # ------------------------------------------------------------------
    # Board state queries
    # ------------------------------------------------------------------

    def is_empty(self) -> bool:
        """Return True if no tiles have been placed on the board."""
        return all(cell.letter is None for row in self.grid for cell in row)

    @property
    def center(self) -> tuple[int, int]:
        """Return the (row, col) of the board's center cell."""
        return (self.rows // 2, self.cols // 2)

    # ------------------------------------------------------------------
    # Anchor squares
    # ------------------------------------------------------------------

    def find_anchors(self, direction: str) -> list[tuple[int, int]]:
        """Find all anchor squares for move generation.

        An anchor is any empty cell that has at least one orthogonally adjacent
        occupied cell (up, down, left, or right). Anchors are direction-independent;
        the direction parameter exists for API consistency with compute_cross_checks
        and compute_left_limit.

        On an empty board, returns [self.center] as the sole synthetic anchor
        (the first move must pass through the center).

        Args:
            direction: 'H' or 'V' (ignored for anchor computation; anchors are
                the same regardless of placement direction).

        Returns:
            List of (row, col) tuples that are anchor squares.
        """
        if self.is_empty():
            return [self.center]

        anchors: list[tuple[int, int]] = []
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if cell.letter is not None:
                    continue  # Occupied cells are never anchors
                # Check all four orthogonal neighbors
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        if self.grid[nr][nc].letter is not None:
                            anchors.append((r, c))
                            break
        return anchors

    # ------------------------------------------------------------------
    # Cross-check precomputation
    # ------------------------------------------------------------------

    def compute_cross_checks(
        self, gaddag: 'GADDAG', direction: str
    ) -> dict[tuple[int, int], set[str]]:
        """Compute cross-check letter sets for all empty cells.

        For each empty cell, determine which letters can legally be placed there
        without forming an invalid perpendicular word. If no perpendicular tiles
        exist adjacent to a cell, all 26 letters are valid.

        Cross-checks are direction-dependent:
        - direction='H' (generating horizontal moves): validates VERTICAL
          perpendicular words. Gather tiles above and below the candidate cell.
        - direction='V' (generating vertical moves): validates HORIZONTAL
          perpendicular words. Gather tiles left and right of the candidate cell.

        Args:
            gaddag: GADDAG instance used to validate candidate perpendicular words.
            direction: 'H' or 'V' — the direction of the primary move being generated.

        Returns:
            Dict mapping (row, col) to set[str] for all empty cells. Cells with
            no perpendicular tiles have a full 26-letter set.
        """
        result: dict[tuple[int, int], set[str]] = {}
        all_letters = set(ALPHABET)

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].letter is not None:
                    continue  # Only compute for empty cells

                perp = self._gather_perpendicular(r, c, direction)
                if perp is None:
                    # No perpendicular tiles — all letters are valid
                    result[(r, c)] = set(all_letters)
                else:
                    prefix, suffix = perp
                    valid: set[str] = set()
                    for letter in ALPHABET:
                        word = prefix + letter + suffix
                        if gaddag.is_valid_word(word):
                            valid.add(letter)
                    result[(r, c)] = valid

        return result

    def _gather_perpendicular(
        self, row: int, col: int, direction: str
    ) -> tuple[str, str] | None:
        """Gather contiguous tiles in the perpendicular direction from (row, col).

        For direction='H' (horizontal moves): scan up (for prefix) and down (for suffix).
        For direction='V' (vertical moves): scan left (for prefix) and right (for suffix).

        The prefix is read in the natural reading direction (top-to-bottom or
        left-to-right), so we collect upward letters in reverse order.

        Args:
            row: Row index of the candidate cell.
            col: Column index of the candidate cell.
            direction: 'H' or 'V'.

        Returns:
            (prefix, suffix) strings if any perpendicular tiles exist, else None.
        """
        if direction == 'H':
            # Gather above (upward scan, reversed to read top-down)
            prefix_letters: list[str] = []
            r = row - 1
            while r >= 0 and self.grid[r][col].letter is not None:
                prefix_letters.append(self.grid[r][col].letter)  # type: ignore[arg-type]
                r -= 1
            prefix = ''.join(reversed(prefix_letters))

            # Gather below (downward scan)
            suffix_letters: list[str] = []
            r = row + 1
            while r < self.rows and self.grid[r][col].letter is not None:
                suffix_letters.append(self.grid[r][col].letter)  # type: ignore[arg-type]
                r += 1
            suffix = ''.join(suffix_letters)

        else:  # direction == 'V'
            # Gather left (leftward scan, reversed to read left-right)
            prefix_letters = []
            c = col - 1
            while c >= 0 and self.grid[row][c].letter is not None:
                prefix_letters.append(self.grid[row][c].letter)  # type: ignore[arg-type]
                c -= 1
            prefix = ''.join(reversed(prefix_letters))

            # Gather right (rightward scan)
            suffix_letters = []
            c = col + 1
            while c < self.cols and self.grid[row][c].letter is not None:
                suffix_letters.append(self.grid[row][c].letter)  # type: ignore[arg-type]
                c += 1
            suffix = ''.join(suffix_letters)

        if not prefix and not suffix:
            return None
        return (prefix, suffix)

    # ------------------------------------------------------------------
    # Left-limit computation
    # ------------------------------------------------------------------

    def compute_left_limit(
        self,
        anchor_row: int,
        anchor_col: int,
        direction: str,
        rack_size: int,
    ) -> int:
        """Compute the left-limit for the LeftPart algorithm at an anchor.

        Determines how many empty cells the LeftPart algorithm can use to extend
        before the anchor. Scans left (for 'H') or up (for 'V') from the cell
        immediately before the anchor, counting empty cells until hitting an
        occupied cell or the board edge. Capped at rack_size - 1.

        If a tile exists immediately to the left (or above) the anchor, the
        left-limit is 0 — no room to extend; those existing tiles are handled
        as a forced prefix in move generation.

        Args:
            anchor_row: Row index of the anchor cell.
            anchor_col: Column index of the anchor cell.
            direction: 'H' (scan left) or 'V' (scan up).
            rack_size: Size of the player's rack.

        Returns:
            Integer left-limit count (0 = no room to extend).
        """
        cap = rack_size - 1
        count = 0

        if direction == 'H':
            c = anchor_col - 1
            while c >= 0 and count < cap:
                if self.grid[anchor_row][c].letter is not None:
                    # Hit an occupied cell — stop scanning but return
                    # the empty cells found so far. Words placed in the
                    # gap won't include the distant tile (non-contiguous),
                    # and _build_move validates the resulting word.
                    break
                count += 1
                c -= 1
        else:  # direction == 'V'
            r = anchor_row - 1
            while r >= 0 and count < cap:
                if self.grid[r][anchor_col].letter is not None:
                    break
                count += 1
                r -= 1

        return count
