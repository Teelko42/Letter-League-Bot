"""Letter League word engine — public API.

The GameEngine class is the single entry point for downstream phases
(difficulty system, Discord integration). It wraps the GADDAG, Board,
and move generation components into a stateful, turn-based API.

Usage:
    from src.engine import GameEngine

    engine = GameEngine(wordlist_path, cache_path=Path('cache/gaddag.pkl'))
    moves = engine.find_moves(['C', 'A', 'R', 'D', 'S', 'E', 'B'])
    best = engine.best_move(['C', 'A', 'R', 'D', 'S', 'E', 'B'])
    engine.play_move(best)   # updates board state for subsequent turns
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from src.engine.gaddag import GADDAG
from src.engine.board import Board
from src.engine.moves import find_all_moves
from src.engine.models import Move, ScoreBreakdown, Cell, MultiplierType, TileUse
from src.engine.tiles import TILE_VALUES, ALPHABET


class GameEngine:
    """Public API for the Letter League word engine.

    Stateful: tracks board state across turns via play_move().
    Downstream phases (difficulty, Discord) consume this API.

    Attributes:
        gaddag: The GADDAG dictionary structure (loaded from wordlist).
        board: The current board state.
        mode: Scoring mode — 'classic' or 'wild'.
    """

    def __init__(
        self,
        wordlist_path: Path,
        cache_path: Path | None = None,
        rows: int = Board.DEFAULT_ROWS,
        cols: int = Board.DEFAULT_COLS,
        multiplier_layout: dict[tuple[int, int], MultiplierType] | None = None,
        mode: str = 'classic',
    ) -> None:
        """Initialize engine with wordlist, board config, and scoring mode.

        Builds or loads the GADDAG from the wordlist (with optional pickle cache).
        Creates the Board with given dimensions and multiplier layout.

        Args:
            wordlist_path: Path to the wordlist file (one word per line).
            cache_path: Optional path to pickle cache for the GADDAG.
            rows: Number of board rows. Defaults to Board.DEFAULT_ROWS (19).
            cols: Number of board columns. Defaults to Board.DEFAULT_COLS (27).
            multiplier_layout: Optional mapping of (row, col) -> MultiplierType.
            mode: Scoring mode — 'classic' or 'wild'.
        """
        self.gaddag = GADDAG.from_wordlist(Path(wordlist_path), cache_path)
        self.board = Board(rows, cols, multiplier_layout)
        self.mode = mode

    def find_moves(self, rack: list[str]) -> list[Move]:
        """Find all valid moves for the given rack on the current board.

        Returns moves sorted by score descending.
        The first element is the optimal move (WENG-05).

        Args:
            rack: Player's tile rack. Use '_' for blank tiles.

        Returns:
            List of Move objects sorted by score descending. Empty list if no moves.
        """
        return find_all_moves(self.board, rack, self.gaddag, self.mode)

    def best_move(self, rack: list[str]) -> Move | None:
        """Return the highest-scoring valid move, or None if no moves available.

        Convenience wrapper around find_moves()[0].

        Args:
            rack: Player's tile rack. Use '_' for blank tiles.

        Returns:
            The highest-scoring Move, or None if no valid moves exist.
        """
        moves = self.find_moves(rack)
        return moves[0] if moves else None

    def play_move(self, move: Move) -> None:
        """Apply a move to the board: place all rack tiles from the move.

        Updates board state for subsequent turns. Only places tiles that
        came from the rack (from_rack=True). Existing board tiles are unchanged.

        Args:
            move: The Move to apply (must have been returned by find_moves/best_move).
        """
        for tile_use in move.rack_tiles_consumed():
            self.board.place_tile(
                tile_use.row,
                tile_use.col,
                tile_use.letter,
                tile_use.is_blank,
                self.mode,
            )

    def is_valid_word(self, word: str) -> bool:
        """Check if a word is in the dictionary.

        Args:
            word: The word to check (case-insensitive).

        Returns:
            True if the word is in the GADDAG dictionary.
        """
        return self.gaddag.is_valid_word(word)

    @property
    def is_first_turn(self) -> bool:
        """True if no tiles have been placed on the board yet."""
        return self.board.is_empty()


# Re-export key types for downstream consumers
__all__ = [
    'GameEngine',
    'Move',
    'ScoreBreakdown',
    'Cell',
    'MultiplierType',
    'TileUse',
    'TILE_VALUES',
    'ALPHABET',
]
