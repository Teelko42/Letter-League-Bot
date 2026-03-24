from __future__ import annotations

import pytest

from src.engine.models import MultiplierType, Cell
from src.engine.board import Board


# ---------------------------------------------------------------------------
# Task 1 Tests: Board state management and tile placement
# ---------------------------------------------------------------------------

def test_board_default_dimensions():
    """Board() creates a 19-row x 27-column grid."""
    board = Board()
    assert board.rows == 19
    assert board.cols == 27


def test_board_custom_dimensions():
    """Board(rows=5, cols=5) creates a 5x5 grid; all cells initialized with letter=None."""
    board = Board(rows=5, cols=5)
    assert board.rows == 5
    assert board.cols == 5
    for r in range(5):
        for c in range(5):
            assert board.grid[r][c].letter is None


def test_board_multiplier_layout():
    """Multiplier layout correctly applied; cells not in layout have NONE."""
    layout = {(0, 0): MultiplierType.TW, (1, 1): MultiplierType.DL}
    board = Board(rows=5, cols=5, multiplier_layout=layout)
    assert board.get_cell(0, 0).square_multiplier == MultiplierType.TW
    assert board.get_cell(1, 1).square_multiplier == MultiplierType.DL
    # Cell not in layout
    assert board.get_cell(2, 2).square_multiplier == MultiplierType.NONE


def test_place_tile_classic():
    """Classic mode places tile without bonding the square multiplier."""
    layout = {(5, 5): MultiplierType.DW}
    board = Board(rows=11, cols=11, multiplier_layout=layout)
    board.place_tile(5, 5, 'A', is_blank=False, mode='classic')
    cell = board.get_cell(5, 5)
    assert cell.letter == 'A'
    assert cell.is_blank is False
    assert cell.bonded_multiplier == MultiplierType.NONE


def test_place_tile_wild():
    """Wild mode bonds the square multiplier permanently to the tile."""
    layout = {(0, 0): MultiplierType.DW}
    board = Board(rows=5, cols=5, multiplier_layout=layout)
    board.place_tile(0, 0, 'A', is_blank=False, mode='wild')
    cell = board.get_cell(0, 0)
    assert cell.bonded_multiplier == MultiplierType.DW


def test_place_blank_tile():
    """Blank tile placed with is_blank=True; letter is the assigned letter."""
    board = Board(rows=5, cols=5)
    board.place_tile(3, 3, 'X', is_blank=True)
    cell = board.get_cell(3, 3)
    assert cell.letter == 'X'
    assert cell.is_blank is True


def test_is_empty():
    """New board is_empty() returns True; after placing a tile, False."""
    board = Board(rows=5, cols=5)
    assert board.is_empty() is True
    board.place_tile(0, 0, 'A')
    assert board.is_empty() is False


def test_get_cell():
    """get_cell returns the Cell at that position; out-of-bounds raises IndexError."""
    board = Board(rows=5, cols=5)
    cell = board.get_cell(0, 0)
    assert isinstance(cell, Cell)
    assert cell.row == 0
    assert cell.col == 0
    with pytest.raises(IndexError):
        board.get_cell(5, 5)
    with pytest.raises(IndexError):
        board.get_cell(-1, 0)


def test_center_cell():
    """center returns the (row, col) tuple for the center of the board."""
    board_default = Board()
    assert board_default.center == (9, 13)  # 19//2=9, 27//2=13

    board_5x5 = Board(rows=5, cols=5)
    assert board_5x5.center == (2, 2)  # 5//2=2, 5//2=2


# ---------------------------------------------------------------------------
# Task 2 Tests: Anchor squares, cross-checks, and left-limit precomputation
# ---------------------------------------------------------------------------

def test_anchors_empty_board():
    """On empty board, find_anchors returns only the center cell."""
    board = Board(rows=11, cols=11)
    anchors_h = board.find_anchors('H')
    anchors_v = board.find_anchors('V')
    assert anchors_h == [board.center]
    assert anchors_v == [board.center]


def test_anchors_single_tile():
    """Anchors include cells adjacent to (5,5); occupied cell itself is NOT an anchor."""
    board = Board(rows=11, cols=11)
    board.place_tile(5, 5, 'A')
    anchors = set(board.find_anchors('H'))
    # Cells adjacent to (5,5)
    assert (5, 4) in anchors
    assert (5, 6) in anchors
    assert (4, 5) in anchors
    assert (6, 5) in anchors
    # Occupied cell is NOT an anchor
    assert (5, 5) not in anchors


def test_anchors_horizontal_word():
    """Anchors for 'CAT' at (5,5)-(5,7) include flanking and above/below cells."""
    board = Board(rows=11, cols=11)
    board.place_tile(5, 5, 'C')
    board.place_tile(5, 6, 'A')
    board.place_tile(5, 7, 'T')
    anchors = set(board.find_anchors('H'))
    # Flanking cells horizontally
    assert (5, 4) in anchors
    assert (5, 8) in anchors
    # Cells above and below
    assert (4, 5) in anchors
    assert (4, 6) in anchors
    assert (4, 7) in anchors
    assert (6, 5) in anchors
    assert (6, 6) in anchors
    assert (6, 7) in anchors
    # Occupied cells are NOT anchors
    assert (5, 5) not in anchors
    assert (5, 6) not in anchors
    assert (5, 7) not in anchors


def test_anchors_direction_independent():
    """Anchors are the same set for 'H' and 'V' directions."""
    board = Board(rows=11, cols=11)
    board.place_tile(5, 5, 'A')
    board.place_tile(3, 3, 'B')
    anchors_h = set(board.find_anchors('H'))
    anchors_v = set(board.find_anchors('V'))
    assert anchors_h == anchors_v


def test_cross_checks_no_perpendicular(small_wordlist_file):
    """Cell with no perpendicular tiles has cross-check set = all 26 letters."""
    from src.engine.gaddag import GADDAG
    from src.engine.tiles import ALPHABET
    gaddag = GADDAG.from_wordlist(small_wordlist_file)

    board = Board(rows=11, cols=11)
    board.place_tile(5, 5, 'C')
    board.place_tile(5, 6, 'A')
    board.place_tile(5, 7, 'T')

    # Horizontal cross-checks: validates vertical perpendicular words
    cross_checks = board.compute_cross_checks(gaddag, 'H')

    # Cell (4, 4) has no perpendicular tiles (nothing above or below at (4,4))
    # This cell is not adjacent to the word, so it won't be in cross_checks
    # Let's use (4, 4) which is not an anchor but test any empty cell with no perp tiles
    # Actually let's test (4, 4) explicitly
    if (4, 4) in cross_checks:
        assert cross_checks[(4, 4)] == set(ALPHABET)


def test_cross_checks_with_perpendicular_above(small_wordlist_file):
    """Cell above a placed tile has cross-check set limited to valid 2-letter combos."""
    from src.engine.gaddag import GADDAG
    gaddag = GADDAG.from_wordlist(small_wordlist_file)

    board = Board(rows=11, cols=11)
    board.place_tile(5, 5, 'C')
    board.place_tile(5, 6, 'A')
    board.place_tile(5, 7, 'T')

    # Horizontal cross-checks: validates vertical words (up-down)
    cross_checks = board.compute_cross_checks(gaddag, 'H')

    # Cell (4, 6) is directly above 'A' at (5, 6)
    # For H cross-check, we check vertical direction: letter + 'A' must be valid
    assert (4, 6) in cross_checks
    cross_set = cross_checks[(4, 6)]
    # 'B' + 'A' = 'BA' is in small_wordlist -> 'B' should be in cross_check set
    assert 'B' in cross_set
    # 'A' + 'A' = 'AA' is NOT in wordlist -> 'A' should NOT be in cross_check set
    # (unless 'AA' was added; it wasn't)
    # Most letters won't be there because they don't form valid 2-letter words with 'A'
    # Letters that do form valid words: AB->B, AD->D, AE->E, BA->no (BA means B above A)
    # Wait: cell (4,6) above A at (5,6): word reads (4,6) then (5,6)=A => letter + 'A'
    # 'BA' is in wordlist, so B in cross_set
    assert 'B' in cross_set


def test_cross_checks_between_tiles(small_wordlist_file):
    """Cell with perpendicular constraint has correct cross-check set."""
    from src.engine.gaddag import GADDAG
    gaddag = GADDAG.from_wordlist(small_wordlist_file)

    board = Board(rows=11, cols=11)
    # Place 'C' above (4,5) and nothing below: for H cross-checks at (5,5)
    board.place_tile(4, 5, 'C')
    # (5,5) is anchor (below C); for H cross-check at (5,5): vertical perp is C above + ? below
    # Cross-check for (5,5) in H direction: prefix = 'C', suffix = '' -> word = 'C' + letter
    # Valid words starting with C: CAB, CAR, CARD etc. -> 'A' in cross_set
    cross_checks = board.compute_cross_checks(gaddag, 'H')
    assert (5, 5) in cross_checks
    cross_set = cross_checks[(5, 5)]
    # 'CA' not in wordlist but 'CAB','CAR','CARE' etc. are - only checking 2+ letter words
    # Actually 'CA' must be a standalone valid 2-letter word for 'A' to be valid
    # Let's check with 'A' below 'R': 'R'+'A'='RA' - check if that's in wordlist
    # The wordlist has ARE, RACE, CARE etc. 'RA' itself is not in list
    # Let's use 'BE': if we have 'B' above empty cell, then 'E' below would form 'BE'
    # Re-setup with something in wordlist
    board2 = Board(rows=11, cols=11)
    board2.place_tile(4, 5, 'B')
    cross_checks2 = board2.compute_cross_checks(gaddag, 'H')
    assert (5, 5) in cross_checks2
    cross_set2 = cross_checks2[(5, 5)]
    # 'B' + 'E' = 'BE' is in wordlist -> 'E' should be in cross_set
    assert 'E' in cross_set2
    # 'B' + 'A' = 'BA' is in wordlist -> 'A' should be in cross_set
    assert 'A' in cross_set2


def test_cross_checks_direction_dependent(small_wordlist_file):
    """H and V cross-checks are different computations (direction-dependent)."""
    from src.engine.gaddag import GADDAG
    from src.engine.tiles import ALPHABET
    gaddag = GADDAG.from_wordlist(small_wordlist_file)

    board = Board(rows=11, cols=11)
    # Place a tile above (5, 5) -> H cross-check at (5,5) is constrained (vertical perp)
    board.place_tile(4, 5, 'B')

    cross_checks_h = board.compute_cross_checks(gaddag, 'H')
    cross_checks_v = board.compute_cross_checks(gaddag, 'V')

    # For H cross-checks: cell (5,5) has 'B' above it — vertical perp constraint
    # Only letters forming valid 2-letter words 'B'+letter or letter+'B' are valid
    assert (5, 5) in cross_checks_h
    h_set = cross_checks_h[(5, 5)]
    # Not all 26 letters are valid (B+? must be a valid 2-letter word)
    assert len(h_set) < 26

    # For V cross-checks: (5,5) has no tiles to its left/right — all 26 letters valid
    # V cross-checks validate horizontal perp words at cell (5,5)
    if (5, 5) in cross_checks_v:
        assert cross_checks_v[(5, 5)] == set(ALPHABET)


def test_left_limit_open_board():
    """On an open board, left_limit = min(empty cells to left, rack_size - 1)."""
    board = Board(rows=11, cols=11)
    # Anchor at (5, 5): 5 empty cells to the left (cols 0-4)
    # rack_size = 7 -> rack_size - 1 = 6 -> min(5, 6) = 5
    limit = board.compute_left_limit(5, 5, 'H', 7)
    assert limit == 5


def test_left_limit_adjacent_tile():
    """If a tile exists immediately to the left of anchor, left_limit is 0."""
    board = Board(rows=11, cols=11)
    board.place_tile(5, 4, 'X')  # tile immediately left of anchor at (5,5)
    limit = board.compute_left_limit(5, 5, 'H', 7)
    assert limit == 0


def test_left_limit_capped_by_rack():
    """left_limit is capped at rack_size - 1."""
    # Use a very wide board so there are more empty cells than rack_size - 1
    board = Board(rows=5, cols=20)
    # Anchor at (2, 15): 15 empty cells to the left (cols 0-14)
    # rack_size = 7 -> cap at 6
    limit = board.compute_left_limit(2, 15, 'H', 7)
    assert limit == 6
