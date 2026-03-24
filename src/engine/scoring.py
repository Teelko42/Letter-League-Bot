"""Scoring engine for Classic and Wild modes.

Classic mode:
  - Letter multipliers (DL/TL) apply only to newly placed tiles.
  - Word multipliers (DW/TW) apply only when the tile is placed on that square this turn.
  - Pre-existing tiles' square multipliers are ignored.

Wild mode:
  - Every tile permanently bonds its square's multiplier when placed.
  - On every subsequent turn, the bonded multiplier applies to that tile.
  - Multiplicative stacking: DW+DW = x4, TW+DW = x6.

Shared rules:
  - Blank tiles always score 0 points regardless of multipliers.
  - Bingo doubles the main word score when all rack tiles are used (not +50).
  - Perpendicular words are scored independently and added to the total.
  - Bingo does NOT double perpendicular word scores.
"""
from __future__ import annotations

from src.engine.models import Cell, MultiplierType, ScoreBreakdown
from src.engine.tiles import TILE_VALUES


def score_word(
    cells_in_word: list[Cell],
    newly_placed_positions: set[tuple[int, int]],
    mode: str,
) -> tuple[int, int]:
    """Score a single word (main or perpendicular).

    Args:
        cells_in_word: Ordered list of Cell objects forming the word.
        newly_placed_positions: Set of (row, col) for tiles placed THIS turn.
        mode: 'classic' or 'wild'.

    Returns:
        (letter_sum_after_letter_multipliers, word_multiplier)

    Classic mode rules:
        - Only newly placed tiles trigger their square_multiplier.
        - DL/TL multiply the tile's letter value.
        - DW/TW accumulate into word_multiplier multiplicatively.
        - Pre-existing tile squares are ignored.

    Wild mode rules:
        - Every tile's bonded_multiplier is applied regardless of turn.
        - DL/TL multiply the tile's letter value.
        - DW/TW accumulate into word_multiplier multiplicatively.
        - This is the core difference: pre-existing bonded multipliers persist.
    """
    letter_sum = 0
    word_multiplier = 1

    for cell in cells_in_word:
        # Blank tiles always score 0 regardless of multipliers
        tile_value = 0 if cell.is_blank else TILE_VALUES.get(cell.letter or '?', 0)

        if mode == 'classic':
            # Only apply multipliers to newly placed tiles
            if (cell.row, cell.col) in newly_placed_positions:
                mult = cell.square_multiplier
                if mult == MultiplierType.DL:
                    tile_value *= 2
                elif mult == MultiplierType.TL:
                    tile_value *= 3
                elif mult == MultiplierType.DW:
                    word_multiplier *= 2
                elif mult == MultiplierType.TW:
                    word_multiplier *= 3
                # MultiplierType.NONE: no change
        elif mode == 'wild':
            # Apply bonded multiplier for ALL tiles (placed any turn)
            mult = cell.bonded_multiplier
            if mult == MultiplierType.DL:
                tile_value *= 2
            elif mult == MultiplierType.TL:
                tile_value *= 3
            elif mult == MultiplierType.DW:
                word_multiplier *= 2
            elif mult == MultiplierType.TW:
                word_multiplier *= 3
            # MultiplierType.NONE: no change
        else:
            raise ValueError(f"Unknown scoring mode: {mode!r}. Expected 'classic' or 'wild'.")

        letter_sum += tile_value

    return letter_sum, word_multiplier


def score_move(
    move_cells: list[Cell],
    newly_placed_positions: set[tuple[int, int]],
    perpendicular_words: list[list[Cell]],
    tiles_from_rack: int,
    rack_size: int,
    mode: str,
) -> ScoreBreakdown:
    """Score a complete move: main word + perpendicular words + bingo bonus.

    Args:
        move_cells: All cells forming the main word (existing + newly placed).
        newly_placed_positions: Set of (row, col) for tiles placed THIS turn.
        perpendicular_words: List of cell lists, one per perpendicular word formed.
        tiles_from_rack: Number of tiles placed from the player's rack this turn.
        rack_size: Total tiles currently in the player's rack before this move.
        mode: 'classic' or 'wild'.

    Returns:
        ScoreBreakdown with all components:
          - base_letter_sum: letter sum after letter multipliers (main word only)
          - word_multiplier: product of all DW/TW from main word
          - bingo_multiplier: 2 if all rack tiles consumed, else 1
          - perpendicular_scores: list of each perpendicular word's total score
          - total: base_letter_sum * word_multiplier * bingo_multiplier
                   + sum(perpendicular_scores)

    Bingo rule (Letter League, NOT Scrabble):
        - Fires when tiles_from_rack == rack_size (all rack tiles used).
        - Doubles the main word total only.
        - Perpendicular words are NOT doubled by bingo.
    """
    # 1. Score main word
    letter_sum, word_multiplier = score_word(move_cells, newly_placed_positions, mode)

    # 2. Main word total before bingo
    main_word_total = letter_sum * word_multiplier

    # 3. Score each perpendicular word independently
    perpendicular_scores: list[int] = []
    for perp_cells in perpendicular_words:
        perp_sum, perp_word_mult = score_word(perp_cells, newly_placed_positions, mode)
        perpendicular_scores.append(perp_sum * perp_word_mult)

    # 4. Bingo bonus: fires when all rack tiles are consumed
    bingo_multiplier = 2 if tiles_from_rack == rack_size else 1
    main_word_total *= bingo_multiplier

    # 5. Grand total
    total = main_word_total + sum(perpendicular_scores)

    return ScoreBreakdown(
        base_letter_sum=letter_sum,
        word_multiplier=word_multiplier,
        bingo_multiplier=bingo_multiplier,
        perpendicular_scores=perpendicular_scores,
        total=total,
    )
