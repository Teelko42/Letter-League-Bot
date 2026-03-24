from __future__ import annotations

from typing import TYPE_CHECKING

from src.difficulty.frequency import FrequencyIndex

if TYPE_CHECKING:
    from src.engine.models import Move


class DifficultyEngine:
    """Selects a move calibrated to a target difficulty level.

    Wraps the word frequency index and blended-score selection algorithm.
    Downstream consumers call select_move(); they never touch frequency
    data directly.

    The algorithm:
    1. Normalize raw scores within the move set to [0, 1].
    2. Compute adjusted_score = alpha * norm_score + (1-alpha) * norm_freq
       where alpha = difficulty/100 (0.0-1.0).
    3. Sort moves by adjusted_score descending.
    4. Return the move at index 0 (the best adjusted score for this alpha).

    At alpha=1.0 (difficulty=100): blended = norm_score -> best scorer wins.
    At alpha=0.0 (difficulty=0): blended = norm_freq -> most common word wins.
    At intermediate values: blends both dimensions smoothly.

    Deterministic: same inputs always produce the same output.
    """

    def __init__(self, lang: str = 'en') -> None:
        """Initialize with word frequency data.

        Loads the frequency dictionary once. Instantiate at bot startup,
        reuse across turns.

        Args:
            lang: Language code for wordfreq. Default 'en'.
        """
        self._freq = FrequencyIndex(lang)

    @property
    def freq(self) -> FrequencyIndex:
        """Expose frequency index for callers that need direct access."""
        return self._freq

    def select_move(
        self, moves: list[Move], difficulty: int | float
    ) -> Move | None:
        """Return the move best matching the target difficulty.

        Args:
            moves: All valid moves from GameEngine.find_moves() (score-sorted
                descending). Must not be modified by this method.
            difficulty: Target difficulty as integer 0-100 (percentage).
                0 = weakest play, 100 = optimal play.
                Values outside 0-100 are clamped.

        Returns:
            A single Move matching the target difficulty, or None if moves
            is empty. Never returns None when moves is non-empty.
        """
        if not moves:
            return None
        if len(moves) == 1:
            return moves[0]

        # Normalize difficulty to 0.0-1.0 (alpha)
        alpha = max(0.0, min(1.0, float(difficulty) / 100.0))

        # Normalize raw scores to [0, 1] within this move set
        scores = [m.score for m in moves]
        max_s = max(scores)
        min_s = min(scores)
        score_range = max_s - min_s or 1  # avoid division by zero

        # Compute adjusted score for each move and sort
        def adjusted_score(move: Move) -> tuple[float, float]:
            """Return (adjusted_score, freq_tiebreaker) for sorting.

            Tiebreaker: among equal adjusted scores, prefer more common word.
            """
            norm_score = (move.score - min_s) / score_range
            norm_freq = self._freq.normalized(move.word)
            blended = alpha * norm_score + (1.0 - alpha) * norm_freq
            return (blended, norm_freq)  # freq as tiebreaker

        ranked = sorted(moves, key=adjusted_score, reverse=True)

        # Always return the best move for the current adjusted-score ranking.
        # At alpha=1.0: ranking is by raw score -> index 0 is the top scorer.
        # At alpha=0.0: ranking is by frequency -> index 0 is the most common word.
        # At intermediate alpha: the ranking blends both; index 0 is best overall.
        return ranked[0]
