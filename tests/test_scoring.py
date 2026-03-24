"""Tests for the scoring engine -- Classic and Wild modes.

TDD: tests written before implementation.
"""
from __future__ import annotations

from src.engine.models import Cell, MultiplierType, ScoreBreakdown
from src.engine.scoring import score_move, score_word


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def make_cell(
    row: int,
    col: int,
    letter: str | None = None,
    is_blank: bool = False,
    sq_mult: MultiplierType = MultiplierType.NONE,
    bonded_mult: MultiplierType = MultiplierType.NONE,
) -> Cell:
    """Build a Cell with minimal boilerplate for tests."""
    return Cell(
        row=row,
        col=col,
        letter=letter,
        is_blank=is_blank,
        square_multiplier=sq_mult,
        bonded_multiplier=bonded_mult,
    )


# ---------------------------------------------------------------------------
# Classic mode tests
# ---------------------------------------------------------------------------

class TestClassicMode:

    def test_classic_simple_word_no_multipliers(self):
        """Place 'CAT' on empty NONE squares. Score = C(3)+A(1)+T(1) = 5."""
        cells = [
            make_cell(7, 7, 'C'),
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T'),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        bd = score_move(cells, placed, [], tiles_from_rack=3, rack_size=7, mode='classic')
        assert bd.base_letter_sum == 5
        assert bd.word_multiplier == 1
        assert bd.bingo_multiplier == 1
        assert bd.total == 5

    def test_classic_double_letter(self):
        """Place 'CAT' where 'A' lands on DL. Score = C(3)+A(1*2)+T(1) = 6."""
        cells = [
            make_cell(7, 7, 'C'),
            make_cell(7, 8, 'A', sq_mult=MultiplierType.DL),
            make_cell(7, 9, 'T'),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        bd = score_move(cells, placed, [], tiles_from_rack=3, rack_size=7, mode='classic')
        assert bd.base_letter_sum == 6
        assert bd.word_multiplier == 1
        assert bd.total == 6

    def test_classic_triple_letter(self):
        """Place 'CAT' where 'C' lands on TL. Score = C(3*3)+A(1)+T(1) = 11."""
        cells = [
            make_cell(7, 7, 'C', sq_mult=MultiplierType.TL),
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T'),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        bd = score_move(cells, placed, [], tiles_from_rack=3, rack_size=7, mode='classic')
        assert bd.base_letter_sum == 11
        assert bd.word_multiplier == 1
        assert bd.total == 11

    def test_classic_double_word(self):
        """Place 'CAT' where 'A' lands on DW. letter_sum=5, word_mult=2, total=10."""
        cells = [
            make_cell(7, 7, 'C'),
            make_cell(7, 8, 'A', sq_mult=MultiplierType.DW),
            make_cell(7, 9, 'T'),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        bd = score_move(cells, placed, [], tiles_from_rack=3, rack_size=7, mode='classic')
        assert bd.base_letter_sum == 5
        assert bd.word_multiplier == 2
        assert bd.total == 10

    def test_classic_triple_word(self):
        """Place 'CAT' where 'T' lands on TW. letter_sum=5, word_mult=3, total=15."""
        cells = [
            make_cell(7, 7, 'C'),
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T', sq_mult=MultiplierType.TW),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        bd = score_move(cells, placed, [], tiles_from_rack=3, rack_size=7, mode='classic')
        assert bd.base_letter_sum == 5
        assert bd.word_multiplier == 3
        assert bd.total == 15

    def test_classic_multiple_word_multipliers(self):
        """Two tiles land on DW squares -- word_mult = 2*2 = 4."""
        cells = [
            make_cell(7, 7, 'C', sq_mult=MultiplierType.DW),
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T', sq_mult=MultiplierType.DW),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        # letter_sum = 3+1+1 = 5, word_mult = 4, total = 20
        bd = score_move(cells, placed, [], tiles_from_rack=3, rack_size=7, mode='classic')
        assert bd.word_multiplier == 4
        assert bd.total == 20

    def test_classic_multiplier_only_on_new_tiles(self):
        """'CA' already on board (TL square on C, placed last turn). Add 'T'.
        Classic: multiplier does NOT apply to pre-existing tiles.
        Score = C(3)+A(1)+T(1) = 5, word_mult=1.
        """
        # 'C' is on a TL square but was NOT placed this turn
        cells = [
            make_cell(7, 7, 'C', sq_mult=MultiplierType.TL),  # existing
            make_cell(7, 8, 'A'),                               # existing
            make_cell(7, 9, 'T'),                               # newly placed
        ]
        # Only 'T' is newly placed
        placed = {(7, 9)}
        bd = score_move(cells, placed, [], tiles_from_rack=1, rack_size=7, mode='classic')
        assert bd.base_letter_sum == 5
        assert bd.word_multiplier == 1
        assert bd.total == 5

    def test_classic_blank_tile_zero_points(self):
        """Blank tile playing as 'Z' on a DL square scores 0 (DL of 0 = 0)."""
        cells = [
            make_cell(7, 7, 'Z', is_blank=True, sq_mult=MultiplierType.DL),
        ]
        placed = {(7, 7)}
        letter_sum, word_mult = score_word(cells, placed, mode='classic')
        assert letter_sum == 0
        assert word_mult == 1

    def test_classic_perpendicular_word_scored(self):
        """Place 'S' to form 'CATS' and a perpendicular word 'SA'.
        Total = score(CATS) + score(SA). Each scored independently.
        """
        # Main word CATS: C(3)+A(1)+T(1)+S(1) = 6, word_mult=1
        main = [
            make_cell(7, 7, 'C'),
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T'),
            make_cell(7, 10, 'S'),
        ]
        placed = {(7, 10)}  # only 'S' newly placed
        # Perpendicular word SA: S(1)+A(1) = 2, word_mult=1
        perp_sa = [
            make_cell(7, 10, 'S'),  # the newly placed tile
            make_cell(8, 10, 'A'),  # existing tile below
        ]
        bd = score_move(main, placed, [perp_sa], tiles_from_rack=1, rack_size=7, mode='classic')
        assert bd.total == 6 + 2   # CATS=6, SA=2

    def test_classic_bingo_doubles_main_word(self):
        """Use all 7 rack tiles -- main word score x2 (bingo). Perp NOT doubled."""
        # Word PLACING: P(3)+L(1)+A(1)+C(3)+I(1)+N(1)+G(2) = 12, word_mult=1
        cells = [
            make_cell(7, 7, 'P'),
            make_cell(7, 8, 'L'),
            make_cell(7, 9, 'A'),
            make_cell(7, 10, 'C'),
            make_cell(7, 11, 'I'),
            make_cell(7, 12, 'N'),
            make_cell(7, 13, 'G'),
        ]
        placed = {(7, 7), (7, 8), (7, 9), (7, 10), (7, 11), (7, 12), (7, 13)}
        # Perpendicular word 'GA': G(2)+A(1) = 3
        perp = [
            make_cell(7, 13, 'G'),
            make_cell(8, 13, 'A'),
        ]
        bd = score_move(cells, placed, [perp], tiles_from_rack=7, rack_size=7, mode='classic')
        assert bd.bingo_multiplier == 2
        # main = 12 * 1 * 2 = 24; perp = 3 (NOT doubled)
        assert bd.total == 24 + 3

    def test_classic_bingo_partial_rack(self):
        """Rack has 4 tiles, all 4 used -- bingo fires."""
        cells = [
            make_cell(7, 7, 'C'),
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T'),
            make_cell(7, 10, 'S'),
        ]
        placed = {(7, 7), (7, 8), (7, 9), (7, 10)}
        bd = score_move(cells, placed, [], tiles_from_rack=4, rack_size=4, mode='classic')
        assert bd.bingo_multiplier == 2
        # C(3)+A(1)+T(1)+S(1) = 6 * 2 = 12
        assert bd.total == 12

    def test_classic_perpendicular_gets_own_multipliers(self):
        """New tile on DW square: DW applies to main word AND the perpendicular word
        formed at that position (tile is newly placed in both contexts).
        """
        # Main word CAT: C(3)+A(1)+T(1) = 5
        # 'A' is on a DW square and is newly placed
        main = [
            make_cell(7, 7, 'C'),
            make_cell(7, 8, 'A', sq_mult=MultiplierType.DW),
            make_cell(7, 9, 'T'),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        # Perpendicular word 'AB': A(1)+B(3) = 4
        # 'A' is newly placed so DW also applies here: 4*2 = 8
        perp = [
            make_cell(7, 8, 'A', sq_mult=MultiplierType.DW),
            make_cell(8, 8, 'B'),
        ]
        bd = score_move(main, placed, [perp], tiles_from_rack=3, rack_size=7, mode='classic')
        # main: 5*2 = 10; perp: 4*2 = 8; total = 18
        assert bd.total == 18


# ---------------------------------------------------------------------------
# Wild mode tests
# ---------------------------------------------------------------------------

class TestWildMode:

    def test_wild_bonded_letter_multiplier(self):
        """Cell has bonded_multiplier=DL, letter='A'. Wild score = A(1*2) = 2."""
        cells = [make_cell(7, 7, 'A', bonded_mult=MultiplierType.DL)]
        placed = {(7, 7)}
        letter_sum, word_mult = score_word(cells, placed, mode='wild')
        assert letter_sum == 2
        assert word_mult == 1

    def test_wild_bonded_word_multiplier(self):
        """'CAT' where 'A' has bonded_multiplier=DW. letter_sum=5, word_mult=2, total=10."""
        cells = [
            make_cell(7, 7, 'C'),
            make_cell(7, 8, 'A', bonded_mult=MultiplierType.DW),
            make_cell(7, 9, 'T'),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        bd = score_move(cells, placed, [], tiles_from_rack=3, rack_size=7, mode='wild')
        assert bd.base_letter_sum == 5
        assert bd.word_multiplier == 2
        assert bd.total == 10

    def test_wild_existing_tiles_keep_multipliers(self):
        """Core Wild mode distinction: 'CA' already on board with C bonded to TL.
        Place 'T' to form 'CAT'. C's TL still applies.
        Score: C(3*3)+A(1)+T(1) = 11, word_mult=1.
        """
        cells = [
            make_cell(7, 7, 'C', bonded_mult=MultiplierType.TL),  # pre-existing, bonded TL
            make_cell(7, 8, 'A'),                                   # pre-existing
            make_cell(7, 9, 'T'),                                   # newly placed
        ]
        # Only 'T' newly placed, but Wild uses bonded_multiplier for ALL tiles
        placed = {(7, 9)}
        bd = score_move(cells, placed, [], tiles_from_rack=1, rack_size=7, mode='wild')
        assert bd.base_letter_sum == 11
        assert bd.word_multiplier == 1
        assert bd.total == 11

    def test_wild_multiplicative_stacking(self):
        """Two DW-bonded tiles: word_mult = 2*2 = 4. letter_sum=5, total=20."""
        cells = [
            make_cell(7, 7, 'C', bonded_mult=MultiplierType.DW),
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T', bonded_mult=MultiplierType.DW),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        bd = score_move(cells, placed, [], tiles_from_rack=3, rack_size=7, mode='wild')
        assert bd.word_multiplier == 4
        assert bd.total == 20

    def test_wild_tw_plus_dw_stacking(self):
        """TW + DW bonded tiles: word_mult = 3*2 = 6 (multiplicative)."""
        cells = [
            make_cell(7, 7, 'C', bonded_mult=MultiplierType.TW),
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T', bonded_mult=MultiplierType.DW),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        bd = score_move(cells, placed, [], tiles_from_rack=3, rack_size=7, mode='wild')
        assert bd.word_multiplier == 6
        # letter_sum = 3+1+1 = 5; total = 5*6 = 30
        assert bd.total == 30

    def test_wild_new_tile_bonds_on_placement(self):
        """Newly placed tile 'A' on DW square in Wild mode.
        The Cell should have bonded_multiplier=DW. Score_word reads bonded_multiplier.
        """
        cells = [
            make_cell(7, 7, 'C'),
            make_cell(7, 8, 'A', bonded_mult=MultiplierType.DW),  # bonded during placement
            make_cell(7, 9, 'T'),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        letter_sum, word_mult = score_word(cells, placed, mode='wild')
        assert letter_sum == 5
        assert word_mult == 2

    def test_wild_blank_tile_bonded_still_zero(self):
        """Blank tile with bonded_multiplier=TL in Wild mode. Score = 0*3 = 0."""
        cells = [make_cell(7, 7, 'Z', is_blank=True, bonded_mult=MultiplierType.TL)]
        placed = {(7, 7)}
        letter_sum, word_mult = score_word(cells, placed, mode='wild')
        assert letter_sum == 0
        assert word_mult == 1

    def test_wild_perpendicular_with_bonded(self):
        """Perp word contains a bonded-multiplier tile from a previous turn.
        The bonded multiplier applies in the perp word scoring.
        """
        main = [
            make_cell(7, 7, 'C'),
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T'),
        ]
        placed = {(7, 7), (7, 8), (7, 9)}
        # Perpendicular word 'AB': A(1, bonded DW)+B(3) = 4*2 = 8
        # But 'A' is at (7,8) which IS in newly_placed for this turn
        # The bonded_multiplier is what Wild uses, and it's bonded to A at placement
        perp = [
            make_cell(7, 8, 'A', bonded_mult=MultiplierType.DW),
            make_cell(8, 8, 'B'),
        ]
        bd = score_move(main, placed, [perp], tiles_from_rack=3, rack_size=7, mode='wild')
        # main: 5*2 = 10 (A has DW bonded); perp: 4*2 = 8
        assert bd.perpendicular_scores == [8]

    def test_wild_bingo(self):
        """Wild mode bingo: same rule as Classic -- main word x2 when all rack tiles used."""
        cells = [
            make_cell(7, 7, 'C', bonded_mult=MultiplierType.TL),
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T'),
            make_cell(7, 10, 'S'),
        ]
        placed = {(7, 7), (7, 8), (7, 9), (7, 10)}
        bd = score_move(cells, placed, [], tiles_from_rack=4, rack_size=4, mode='wild')
        assert bd.bingo_multiplier == 2
        # C(3*3)+A(1)+T(1)+S(1) = 12; word_mult=1; bingo=2; total=24
        assert bd.total == 24

    def test_classic_vs_wild_different_scores(self):
        """Same board layout, same placement, Classic vs Wild produce different scores
        when pre-existing tiles have multipliers on their squares.
        Classic ignores pre-existing tile multipliers; Wild applies bonded multipliers.
        """
        # 'C' was placed on a TL square in a previous turn
        # Wild: C has bonded_multiplier=TL; Classic: sq_mult=TL but not newly placed
        cells_classic = [
            make_cell(7, 7, 'C', sq_mult=MultiplierType.TL),  # pre-existing, not placed this turn
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T'),
        ]
        cells_wild = [
            make_cell(7, 7, 'C', bonded_mult=MultiplierType.TL),  # bonded from previous turn
            make_cell(7, 8, 'A'),
            make_cell(7, 9, 'T'),
        ]
        placed = {(7, 9)}  # only T placed this turn

        classic_bd = score_move(cells_classic, placed, [], tiles_from_rack=1, rack_size=7, mode='classic')
        wild_bd = score_move(cells_wild, placed, [], tiles_from_rack=1, rack_size=7, mode='wild')

        # Classic: C(3)+A(1)+T(1) = 5 (TL not applied to pre-existing C)
        assert classic_bd.total == 5
        # Wild: C(3*3)+A(1)+T(1) = 11 (TL bonded, always applies)
        assert wild_bd.total == 11
        assert classic_bd.total != wild_bd.total
