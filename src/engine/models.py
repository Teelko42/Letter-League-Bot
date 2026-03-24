from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class MultiplierType(Enum):
    """Square and tile multiplier types."""
    NONE = 0
    DL = 1   # Double Letter
    TL = 2   # Triple Letter
    DW = 3   # Double Word
    TW = 4   # Triple Word


@dataclass
class Cell:
    """A single cell on the board.

    Attributes:
        row: Row index (0-based).
        col: Column index (0-based).
        letter: Letter placed on this cell, or None if empty.
        is_blank: True if a blank tile is placed here (letter is assigned but worth 0 pts).
        square_multiplier: The intrinsic multiplier of the square itself.
        bonded_multiplier: Wild mode only — the multiplier permanently bonded to the tile
            when it was placed on this square. Applies every subsequent turn the tile
            is part of a scoring word.
    """
    row: int
    col: int
    letter: Optional[str] = None
    is_blank: bool = False
    square_multiplier: MultiplierType = MultiplierType.NONE
    bonded_multiplier: MultiplierType = MultiplierType.NONE


@dataclass(frozen=True)
class TileUse:
    """Represents a single tile's use within a Move.

    Attributes:
        row: Row index of the tile on the board.
        col: Column index of the tile on the board.
        letter: The letter this tile represents (uppercase).
        is_blank: True if a blank tile is being used (worth 0 pts).
        from_rack: True if this tile came from the player's rack; False if it
            was an existing tile already on the board.
    """
    row: int
    col: int
    letter: str
    is_blank: bool
    from_rack: bool


@dataclass
class ScoreBreakdown:
    """Detailed breakdown of a move's score.

    Attributes:
        base_letter_sum: Sum of letter values (after letter multipliers applied).
        word_multiplier: Accumulated word multiplier (product of all DW/TW applied).
        bingo_multiplier: 1 normally; 2 if all rack tiles were used (Letter League bingo rule).
        perpendicular_scores: Scores of any perpendicular words formed by this move.
        total: Final total score (base_letter_sum * word_multiplier * bingo_multiplier
            + sum(perpendicular_scores)).
    """
    base_letter_sum: int
    word_multiplier: int
    bingo_multiplier: int = 1
    perpendicular_scores: list[int] = field(default_factory=list)
    total: int = 0


@dataclass
class Move:
    """A complete word placement move.

    Attributes:
        word: The word formed by this move (uppercase).
        start_row: Row of the first letter of the word.
        start_col: Column of the first letter of the word.
        direction: 'H' for horizontal, 'V' for vertical.
        tiles_used: All tiles involved in this word (rack tiles + existing board tiles).
        score_breakdown: Detailed scoring breakdown.
        score: Total score for this move (for sorting/ranking).
    """
    word: str
    start_row: int
    start_col: int
    direction: str  # 'H' or 'V'
    tiles_used: list[TileUse]
    score_breakdown: ScoreBreakdown
    score: int

    def rack_tiles_consumed(self) -> list[TileUse]:
        """Return only the tiles placed from the player's rack."""
        return [t for t in self.tiles_used if t.from_rack]
