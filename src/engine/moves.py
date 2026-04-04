"""Gordon (1994) LeftPart/ExtendRight move generation algorithm.

Finds ALL valid word placements on a Letter League board given a tile rack,
using the GADDAG data structure for bidirectional word traversal.

Algorithm overview:
  1. For each direction ('H', 'V'):
     a. Compute cross-check sets (letters valid for perpendicular words) for all empty cells.
     b. Find anchor squares (empty cells adjacent to occupied cells; or center on empty board).
     c. For each anchor, run LeftPart then ExtendRight.
  2. Deduplicate moves (same word+position+direction can arise from multiple anchors).
  3. Sort by score descending.

Key design decisions:
  - Rack is mutated in-place for backtracking (pop/insert) — no copying on each call.
  - Blank tiles ('_') only try letters with GADDAG arcs at the current node (not all 26).
  - Direction abstraction via _next_pos/_prev_pos helpers.
  - Cross-check enforcement: only place a letter if it's in cross_checks[(row, col)].
  - Left-part placed positions are threaded through to ExtendRight for accurate _build_move.

The left part is built to the LEFT of the anchor. Positions for left-part tiles are
computed from the anchor position during LeftPart recursion.
"""
from __future__ import annotations

from src.engine.board import Board
from src.engine.gaddag import GADDAG
from src.engine.models import Cell, Move, TileUse, ScoreBreakdown
from src.engine.scoring import score_move


# ---------------------------------------------------------------------------
# Direction helpers
# ---------------------------------------------------------------------------

def _next_pos(row: int, col: int, direction: str) -> tuple[int, int]:
    """Return the next position in the given direction."""
    if direction == 'H':
        return row, col + 1
    return row + 1, col


def _prev_pos(row: int, col: int, direction: str) -> tuple[int, int]:
    """Return the previous position in the given direction."""
    if direction == 'H':
        return row, col - 1
    return row - 1, col


def _in_bounds(board: Board, row: int, col: int) -> bool:
    """Return True if (row, col) is within board boundaries."""
    return 0 <= row < board.rows and 0 <= col < board.cols


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def find_all_moves(
    board: Board,
    rack: list[str],
    gaddag: GADDAG,
    mode: str = 'classic',
) -> list[Move]:
    """Find ALL valid word placements for the given rack on the current board.

    Returns moves sorted by score descending (WENG-05). The first element is
    the optimal (highest-scoring) move.

    Args:
        board: Current board state.
        rack: Player's tile rack. '_' represents a blank tile.
        gaddag: GADDAG for the game dictionary.
        mode: 'classic' or 'wild' — affects scoring.

    Returns:
        List of Move objects sorted by score descending.
    """
    # Normalize blank representation: vision pipeline uses '?' but
    # LeftPart/ExtendRight check for '_'.
    rack = ['_' if t == '?' else t for t in rack]

    all_moves: list[Move] = []

    for direction in ('H', 'V'):
        cross_checks = board.compute_cross_checks(gaddag, direction)
        anchors = board.find_anchors(direction)

        for anchor_row, anchor_col in anchors:
            moves = generate_moves_for_anchor(
                board, rack, gaddag,
                anchor_row, anchor_col,
                cross_checks, direction, mode,
            )
            all_moves.extend(moves)

    all_moves = _deduplicate_moves(all_moves)
    all_moves.sort(key=lambda m: m.score, reverse=True)
    return all_moves


# ---------------------------------------------------------------------------
# Per-anchor move generation
# ---------------------------------------------------------------------------

def generate_moves_for_anchor(
    board: Board,
    rack: list[str],
    gaddag: GADDAG,
    anchor_row: int,
    anchor_col: int,
    cross_checks: dict[tuple[int, int], set[str]],
    direction: str,
    mode: str,
) -> list[Move]:
    """Generate all moves whose anchor square is at (anchor_row, anchor_col).

    Checks whether there are existing tiles in the "left" direction (before the
    anchor). If so, they form a forced prefix that is traversed through the GADDAG
    to find the starting node; then ExtendRight is called directly.

    If no tiles exist to the left, LeftPart is called to build all possible
    left parts from the rack.
    """
    results: list[Move] = []

    # Check if there is an existing tile immediately before the anchor
    prev_row, prev_col = _prev_pos(anchor_row, anchor_col, direction)
    has_existing_prefix = (
        _in_bounds(board, prev_row, prev_col)
        and board.get_cell(prev_row, prev_col).letter is not None
    )

    if has_existing_prefix:
        # Collect all existing tiles before the anchor (reading left/up → reversed)
        prefix_letters: list[str] = []
        r, c = prev_row, prev_col
        while _in_bounds(board, r, c) and board.get_cell(r, c).letter is not None:
            prefix_letters.append(board.get_cell(r, c).letter)  # type: ignore[arg-type]
            r, c = _prev_pos(r, c, direction)

        # prefix_letters is in reversed reading order (closest to anchor first).
        # GADDAG encodes: rev(prefix) + SEPARATOR + suffix
        # So we feed prefix_letters as-is (they're already reversed from reading order).
        node = gaddag.root
        valid = True
        for ch in prefix_letters:
            node = node.get(ch)  # type: ignore[assignment]
            if node is None:
                valid = False
                break

        if valid and node is not None:
            sep_node = node.get(GADDAG.SEPARATOR)
            if sep_node is not None:
                # Partial word = prefix in reading order (reversed from prefix_letters)
                partial = ''.join(reversed(prefix_letters))
                # Existing tiles: none come from rack, so left_placed = []
                _extend_right(
                    sep_node, partial, [],  # no rack tiles placed in left part
                    list(rack),  # fresh copy
                    anchor_row, anchor_col,
                    board, gaddag, cross_checks, direction, mode, results,
                )
    else:
        # No existing prefix — run LeftPart from root
        left_limit = board.compute_left_limit(
            anchor_row, anchor_col, direction, len(rack)
        )
        _left_part(
            gaddag.root, '', [],  # no rack tiles in left part yet
            list(rack),  # fresh copy
            left_limit,
            anchor_row, anchor_col,
            board, gaddag, cross_checks, direction, mode, results,
        )

    return results


# ---------------------------------------------------------------------------
# LeftPart
# ---------------------------------------------------------------------------

def _left_part(
    node: dict,
    partial: str,
    left_placed: list[tuple[int, int, str, bool]],  # rack tiles placed in left part
    rack: list[str],
    limit: int,
    anchor_row: int,
    anchor_col: int,
    board: Board,
    gaddag: GADDAG,
    cross_checks: dict[tuple[int, int], set[str]],
    direction: str,
    mode: str,
    results: list[Move],
) -> None:
    """Build the left part of a word by traversing reversed-prefix arcs in the GADDAG.

    The left part letters are placed to the LEFT of the anchor. Their board positions
    are computed from the anchor position and the current left-part length.

    At each step:
    - If SEPARATOR exists in current node: cross it and call ExtendRight at the anchor.
    - If limit > 0: try each rack tile as the next left character.
    """
    # Try crossing SEPARATOR to start the right part at the anchor
    sep_node = node.get(GADDAG.SEPARATOR)
    if sep_node is not None:
        _extend_right(
            sep_node, partial, list(left_placed),  # copy so branches don't interfere
            list(rack),  # fresh copy for this branch
            anchor_row, anchor_col,
            board, gaddag, cross_checks, direction, mode, results,
        )

    if limit == 0:
        return

    # The next left-part tile will occupy the position `limit` cells to the left of anchor
    # (since we build left-to-right but add one letter at a time leftward)
    # Actually: partial has len(partial) chars, so the next tile goes at offset -(len(partial)+1)
    # from anchor.
    left_offset = len(partial) + 1  # how many steps left of anchor
    if direction == 'H':
        tile_row = anchor_row
        tile_col = anchor_col - left_offset
    else:
        tile_row = anchor_row - left_offset
        tile_col = anchor_col

    # Verify this position is in bounds and empty
    if not _in_bounds(board, tile_row, tile_col):
        return
    if board.get_cell(tile_row, tile_col).letter is not None:
        return  # Hit an occupied cell — can't place here

    tried: set[str] = set()
    i = 0
    while i < len(rack):
        tile = rack[i]

        if tile == '_':
            if '_' in tried:
                i += 1
                continue
            tried.add('_')
            rack.pop(i)
            # Blank: only try letters with GADDAG arcs at current node
            valid_letters = cross_checks.get((tile_row, tile_col), set())
            for letter in list(node.keys()):
                if letter in (GADDAG.SEPARATOR, GADDAG.TERMINAL):
                    continue
                if letter not in valid_letters:
                    continue
                child = node[letter]
                new_left_placed = left_placed + [(tile_row, tile_col, letter, True)]
                _left_part(
                    child,
                    letter + partial,  # prepend: left part builds right-to-left
                    new_left_placed,
                    rack,
                    limit - 1,
                    anchor_row, anchor_col,
                    board, gaddag, cross_checks, direction, mode, results,
                )
            rack.insert(i, tile)
            i += 1
        else:
            if tile in tried:
                i += 1
                continue
            tried.add(tile)
            if tile not in cross_checks.get((tile_row, tile_col), set()):
                i += 1
                continue
            child = node.get(tile)
            if child is not None:
                rack.pop(i)
                new_left_placed = left_placed + [(tile_row, tile_col, tile, False)]
                _left_part(
                    child,
                    tile + partial,  # prepend
                    new_left_placed,
                    rack,
                    limit - 1,
                    anchor_row, anchor_col,
                    board, gaddag, cross_checks, direction, mode, results,
                )
                rack.insert(i, tile)
            i += 1


# ---------------------------------------------------------------------------
# ExtendRight
# ---------------------------------------------------------------------------

def _extend_right(
    node: dict,
    partial: str,
    left_placed: list[tuple[int, int, str, bool]],  # rack tiles placed in left part
    rack: list[str],
    row: int,
    col: int,
    board: Board,
    gaddag: GADDAG,
    cross_checks: dict[tuple[int, int], set[str]],
    direction: str,
    mode: str,
    results: list[Move],
) -> None:
    """Extend the word rightward (or downward for 'V') from position (row, col).

    left_placed tracks rack tiles placed during LeftPart (to the left of anchor).
    right_placed (built here) tracks rack tiles placed during extension.

    At each position:
    - Out of bounds: if TERMINAL in node and at least one rack tile placed, record move.
    - Occupied cell: follow arc for existing letter.
    - Empty cell: try each rack tile; also record if TERMINAL and tiles placed.
    """
    _extend_right_inner(
        node, partial, left_placed, [],  # right_placed starts empty
        rack, row, col,
        board, gaddag, cross_checks, direction, mode, results,
    )


def _extend_right_inner(
    node: dict,
    partial: str,
    left_placed: list[tuple[int, int, str, bool]],
    right_placed: list[tuple[int, int, str, bool]],
    rack: list[str],
    row: int,
    col: int,
    board: Board,
    gaddag: GADDAG,
    cross_checks: dict[tuple[int, int], set[str]],
    direction: str,
    mode: str,
    results: list[Move],
) -> None:
    """Inner recursive extension function with full placed tracking."""
    out_of_bounds = not _in_bounds(board, row, col)
    all_placed = left_placed + right_placed

    if out_of_bounds:
        if GADDAG.TERMINAL in node and all_placed:
            move = _build_move(
                board, partial, left_placed, right_placed,
                direction, mode, len(rack) + len(all_placed),
            )
            if move is not None:
                results.append(move)
        return

    cell = board.get_cell(row, col)
    next_row, next_col = _next_pos(row, col, direction)

    if cell.letter is not None:
        # Occupied cell: must follow the existing letter's arc
        existing = cell.letter
        child = node.get(existing)
        if child is not None:
            _extend_right_inner(
                child, partial + existing,
                left_placed, right_placed,
                rack, next_row, next_col,
                board, gaddag, cross_checks, direction, mode, results,
            )
        return

    # Empty cell
    if GADDAG.TERMINAL in node and all_placed:
        move = _build_move(
            board, partial, left_placed, right_placed,
            direction, mode, len(rack) + len(all_placed),
        )
        if move is not None:
            results.append(move)

    # Try placing each rack tile
    valid_letters = cross_checks.get((row, col), set())
    tried: set[str] = set()
    i = 0
    while i < len(rack):
        tile = rack[i]

        if tile == '_':
            if '_' in tried:
                i += 1
                continue
            tried.add('_')
            rack.pop(i)
            for letter in list(node.keys()):
                if letter in (GADDAG.SEPARATOR, GADDAG.TERMINAL):
                    continue
                if letter not in valid_letters:
                    continue
                child = node[letter]
                new_right = right_placed + [(row, col, letter, True)]  # is_blank=True
                _extend_right_inner(
                    child, partial + letter,
                    left_placed, new_right,
                    rack, next_row, next_col,
                    board, gaddag, cross_checks, direction, mode, results,
                )
            rack.insert(i, tile)
            i += 1
        else:
            if tile in tried:
                i += 1
                continue
            tried.add(tile)
            if tile not in valid_letters:
                i += 1
                continue
            child = node.get(tile)
            if child is None:
                i += 1
                continue
            rack.pop(i)
            new_right = right_placed + [(row, col, tile, False)]
            _extend_right_inner(
                child, partial + tile,
                left_placed, new_right,
                rack, next_row, next_col,
                board, gaddag, cross_checks, direction, mode, results,
            )
            rack.insert(i, tile)
            i += 1


# ---------------------------------------------------------------------------
# Move construction
# ---------------------------------------------------------------------------

def _build_move(
    board: Board,
    word: str,
    left_placed: list[tuple[int, int, str, bool]],
    right_placed: list[tuple[int, int, str, bool]],
    direction: str,
    mode: str,
    original_rack_size: int,
) -> Move | None:
    """Construct a Move object from the placed tiles and word string.

    Args:
        board: Current board state.
        word: The complete word formed (left part + right extension).
        left_placed: Rack tiles placed in the left part (to left of anchor).
        right_placed: Rack tiles placed in the right extension.
        direction: 'H' or 'V'.
        mode: 'classic' or 'wild'.
        original_rack_size: Size of player's rack before this move.

    Returns:
        Move object, or None if the move is invalid.
    """
    all_rack_placed = left_placed + right_placed
    if not all_rack_placed or not word:
        return None

    # Build a lookup: position -> (letter, is_blank) for all rack-placed tiles
    placed_lookup: dict[tuple[int, int], tuple[str, bool]] = {
        (row, col): (letter, is_blank)
        for row, col, letter, is_blank in all_rack_placed
    }
    placed_positions = set(placed_lookup.keys())

    # Determine start position
    if direction == 'H':
        start_row = all_rack_placed[0][0]  # all tiles in same row
        # Find leftmost position: min col among rack tiles, then check for existing tiles further left
        min_rack_col = min(c for _, c, _, _ in all_rack_placed)
        start_col = min_rack_col
        c = min_rack_col - 1
        while c >= 0 and board.get_cell(start_row, c).letter is not None:
            start_col = c
            c -= 1
    else:  # 'V'
        start_col = all_rack_placed[0][1]  # all tiles in same col
        min_rack_row = min(r for r, _, _, _ in all_rack_placed)
        start_row = min_rack_row
        r = min_rack_row - 1
        while r >= 0 and board.get_cell(r, start_col).letter is not None:
            start_row = r
            r -= 1

    # Verify word length matches the span from start to after last tile
    # Walk the word and collect cells
    move_cells: list[Cell] = []
    tiles_used: list[TileUse] = []
    r, c = start_row, start_col

    for i, expected_letter in enumerate(word):
        if not _in_bounds(board, r, c):
            return None  # word extends out of bounds — invalid

        pos = (r, c)
        if pos in placed_lookup:
            letter, is_blank = placed_lookup[pos]
            if letter != expected_letter:
                return None  # Mismatch — shouldn't happen
            temp_cell = Cell(r, c, letter=letter, is_blank=is_blank)
            board_cell = board.get_cell(r, c)
            temp_cell.square_multiplier = board_cell.square_multiplier
            # Simulate wild-mode bonding: newly placed tiles bond the
            # square's multiplier, but place_tile() is never called for
            # hypothetical moves.  Use square_multiplier so wild-mode
            # scoring (which reads bonded_multiplier) applies correctly.
            temp_cell.bonded_multiplier = board_cell.square_multiplier
            move_cells.append(temp_cell)
            tiles_used.append(TileUse(r, c, letter, is_blank, from_rack=True))
        else:
            board_cell = board.get_cell(r, c)
            if board_cell.letter is None:
                return None  # Expected existing tile but cell is empty
            if board_cell.letter != expected_letter:
                return None  # Mismatch
            move_cells.append(board_cell)
            tiles_used.append(TileUse(r, c, board_cell.letter, board_cell.is_blank, from_rack=False))

        if direction == 'H':
            c += 1
        else:
            r += 1

    # Gather perpendicular words formed by newly placed tiles
    perp_words = _gather_perpendicular_words(board, all_rack_placed, direction)

    # Score the move
    tiles_from_rack = len(all_rack_placed)
    score_breakdown = score_move(
        move_cells,
        placed_positions,
        perp_words,
        tiles_from_rack,
        original_rack_size,
        mode,
    )

    return Move(
        word=word,
        start_row=start_row,
        start_col=start_col,
        direction=direction,
        tiles_used=tiles_used,
        score_breakdown=score_breakdown,
        score=score_breakdown.total,
    )


# ---------------------------------------------------------------------------
# Perpendicular word gathering
# ---------------------------------------------------------------------------

def _gather_perpendicular_words(
    board: Board,
    placed: list[tuple[int, int, str, bool]],
    direction: str,
) -> list[list[Cell]]:
    """Gather all perpendicular words formed by newly placed tiles.

    For direction 'H': each placed tile potentially forms a vertical word.
    For direction 'V': each placed tile potentially forms a horizontal word.

    Only words of length >= 2 are returned.

    Args:
        board: Current board state (placed tiles not yet committed).
        placed: All rack-placed tiles: (row, col, letter, is_blank).
        direction: Primary direction of the move.

    Returns:
        List of cell lists, each representing a complete perpendicular word.
    """
    result: list[list[Cell]] = []

    for row, col, letter, is_blank in placed:
        temp_cell = Cell(row, col, letter=letter, is_blank=is_blank)
        board_cell = board.get_cell(row, col)
        temp_cell.square_multiplier = board_cell.square_multiplier
        temp_cell.bonded_multiplier = board_cell.square_multiplier

        perp_cells: list[Cell] = []

        if direction == 'H':
            # Gather vertical word through (row, col)
            above: list[Cell] = []
            r = row - 1
            while r >= 0 and board.get_cell(r, col).letter is not None:
                above.append(board.get_cell(r, col))
                r -= 1
            perp_cells.extend(reversed(above))
            perp_cells.append(temp_cell)
            r = row + 1
            while r < board.rows and board.get_cell(r, col).letter is not None:
                perp_cells.append(board.get_cell(r, col))
                r += 1
        else:  # 'V'
            # Gather horizontal word through (row, col)
            left: list[Cell] = []
            c = col - 1
            while c >= 0 and board.get_cell(row, c).letter is not None:
                left.append(board.get_cell(row, c))
                c -= 1
            perp_cells.extend(reversed(left))
            perp_cells.append(temp_cell)
            c = col + 1
            while c < board.cols and board.get_cell(row, c).letter is not None:
                perp_cells.append(board.get_cell(row, c))
                c += 1

        if len(perp_cells) >= 2:
            result.append(perp_cells)

    return result


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _deduplicate_moves(moves: list[Move]) -> list[Move]:
    """Remove duplicate moves (same word, start position, direction).

    Adjacent anchors can generate the same word. Keep first occurrence.

    Args:
        moves: List of Move objects (potentially with duplicates).

    Returns:
        List of Move objects with duplicates removed.
    """
    seen: set[tuple[str, int, int, str]] = set()
    unique: list[Move] = []
    for move in moves:
        key = (move.word, move.start_row, move.start_col, move.direction)
        if key not in seen:
            seen.add(key)
            unique.append(move)
    return unique
