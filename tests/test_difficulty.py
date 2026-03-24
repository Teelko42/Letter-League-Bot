from __future__ import annotations

import pytest

from src.difficulty import FrequencyIndex
from src.engine.models import Move, ScoreBreakdown, TileUse


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_move(word: str, score: int) -> Move:
    """Create a minimal Move for difficulty testing. Only word and score matter."""
    return Move(
        word=word,
        start_row=0,
        start_col=0,
        direction='H',
        tiles_used=[],
        score_breakdown=ScoreBreakdown(
            base_letter_sum=score,
            word_multiplier=1,
            total=score,
        ),
        score=score,
    )


# ---------------------------------------------------------------------------
# FrequencyIndex tests (from 02-01)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def freq() -> FrequencyIndex:
    """A single FrequencyIndex instance shared across the test module."""
    return FrequencyIndex()


class TestFrequencyCommonWords:
    """FrequencyIndex returns Zipf scores above 4.0 for common English words."""

    def test_frequency_common_words(self, freq: FrequencyIndex) -> None:
        common_words = ['the', 'cat', 'house', 'play', 'word']
        for word in common_words:
            score = freq.zipf(word)
            assert score > 4.0, (
                f"Expected '{word}' to have Zipf > 4.0, got {score}"
            )


class TestFrequencyUncommonWords:
    """Uncommon words score lower than common words but are still positive."""

    def test_frequency_uncommon_words(self, freq: FrequencyIndex) -> None:
        uncommon_words = ['quasar', 'zephyr']
        for word in uncommon_words:
            score = freq.zipf(word)
            assert score > 0.0, (
                f"Expected '{word}' to have Zipf > 0.0, got {score}"
            )

        # Uncommon words should score lower than a highly common word
        common_score = freq.zipf('the')
        for word in uncommon_words:
            assert freq.zipf(word) < common_score, (
                f"Expected '{word}' to score less than 'the' ({common_score})"
            )


class TestFrequencyOOVWords:
    """OOV game-dictionary words return Zipf 0.0 (not excluded).

    Note: 'xu' and 'qat' are present in wordfreq (Zipf 3.33 and 1.86) because
    they appear in English text. 'zyzzyva' and 'qoph' are truly absent.
    """

    def test_frequency_oov_words(self, freq: FrequencyIndex) -> None:
        # zyzzyva: a type of weevil, valid in Scrabble but not in wordfreq
        # qoph: Hebrew letter, valid in Scrabble but not in wordfreq
        oov_words = ['zyzzyva', 'qoph']
        for word in oov_words:
            score = freq.zipf(word)
            assert score == 0.0, (
                f"Expected OOV word '{word}' to return 0.0, got {score}"
            )


class TestFrequencyCaseInsensitive:
    """FrequencyIndex is case-insensitive — game uppercase maps to lowercase data."""

    def test_frequency_case_insensitive(self, freq: FrequencyIndex) -> None:
        upper = freq.zipf('CAT')
        lower = freq.zipf('cat')
        title = freq.zipf('Cat')

        assert upper == lower, (
            f"zipf('CAT') ({upper}) != zipf('cat') ({lower})"
        )
        assert lower == title, (
            f"zipf('cat') ({lower}) != zipf('Cat') ({title})"
        )
        assert upper > 0.0, "Case-insensitive 'CAT' lookup should find 'cat' in data"


class TestFrequencyNormalizedRange:
    """normalized() returns values in [0.0, 1.0]. Common words near 1.0."""

    def test_frequency_normalized_range(self, freq: FrequencyIndex) -> None:
        test_words = ['the', 'cat', 'house', 'play', 'word', 'quasar', 'zephyr', 'zyzzyva']
        for word in test_words:
            value = freq.normalized(word)
            assert 0.0 <= value <= 1.0, (
                f"normalized('{word}') = {value} is out of [0.0, 1.0] range"
            )

        # Common word 'the' should be close to 1.0 (> 0.9 with MAX_ZIPF ~8.0)
        the_norm = freq.normalized('the')
        assert the_norm > 0.9, (
            f"Expected normalized('the') > 0.9, got {the_norm}"
        )


class TestFrequencyNormalizedOOVIsZero:
    """normalized() returns exactly 0.0 for OOV words."""

    def test_frequency_normalized_oov_is_zero(self, freq: FrequencyIndex) -> None:
        result = freq.normalized('zyzzyva')
        assert result == 0.0, (
            f"Expected normalized('zyzzyva') == 0.0, got {result}"
        )


class TestFrequencySingletonReuse:
    """Creating FrequencyIndex twice returns correct, consistent values."""

    def test_frequency_singleton_reuse(self) -> None:
        freq1 = FrequencyIndex()
        freq2 = FrequencyIndex()

        test_words = ['the', 'cat', 'house', 'zyzzyva']
        for word in test_words:
            assert freq1.zipf(word) == freq2.zipf(word), (
                f"freq1.zipf('{word}') ({freq1.zipf(word)}) != "
                f"freq2.zipf('{word}') ({freq2.zipf(word)})"
            )


# ---------------------------------------------------------------------------
# DifficultyEngine tests (02-02) -- behavioral tests for DIFF-01/02/03
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def engine():
    """A single DifficultyEngine instance shared across the difficulty test module."""
    from src.difficulty import DifficultyEngine
    return DifficultyEngine()


class TestDifficultyAt100Pct:
    """DIFF-01: At difficulty=100, the highest-scoring move is always selected."""

    def test_100pct_returns_best_move(self, engine) -> None:
        """difficulty=100 always returns moves[0] (highest score)."""
        moves = [
            make_move('QUIXOTIC', 120),
            make_move('CAT', 30),
            make_move('THE', 15),
        ]
        result = engine.select_move(moves, difficulty=100)
        assert result is not None
        assert result.word == 'QUIXOTIC'
        assert result.score == 120


class TestDifficultyAt0Pct:
    """DIFF-01: At difficulty=0, a measurably weaker move is returned."""

    def test_0pct_weaker_than_100pct(self, engine) -> None:
        """difficulty=0 returns a lower-scoring move than difficulty=100."""
        moves = [
            make_move('QUIXOTIC', 120),
            make_move('CAT', 30),
            make_move('THE', 15),
        ]
        result_100 = engine.select_move(moves, difficulty=100)
        result_0 = engine.select_move(moves, difficulty=0)
        assert result_0 is not None
        assert result_100 is not None
        # At 0%, should return a weaker (lower or equal score but different) move
        assert result_0.score < result_100.score, (
            f"Expected 0% result score ({result_0.score}) < "
            f"100% result score ({result_100.score})"
        )

    def test_0pct_returns_worst_adjusted_move(self, engine) -> None:
        """At difficulty=0, result is different from difficulty=100 result."""
        moves = [
            make_move('QUIXOTIC', 120),
            make_move('CAT', 30),
            make_move('THE', 15),
        ]
        result_100 = engine.select_move(moves, difficulty=100)
        result_0 = engine.select_move(moves, difficulty=0)
        assert result_0 is not None
        assert result_0.word != result_100.word, (
            "Expected 0% and 100% to select different moves"
        )


class TestDifficultyConfigurable:
    """DIFF-01: Difficulty is configurable as numeric percentage 0-100."""

    def test_difficulty_configurable(self, engine) -> None:
        """select_move() accepts int percentages 25, 50, 75 without code changes."""
        moves = [
            make_move('QUIXOTIC', 120),
            make_move('SCARE', 60),
            make_move('RACE', 40),
            make_move('CAT', 30),
            make_move('THE', 15),
        ]
        for difficulty in [25, 50, 75]:
            result = engine.select_move(moves, difficulty=difficulty)
            assert result is not None, f"select_move returned None at difficulty={difficulty}"
            assert isinstance(result, Move), (
                f"Expected Move at difficulty={difficulty}, got {type(result)}"
            )


class TestDifficultyPrefersCommonWords:
    """DIFF-02: Lower difficulty prefers more common vocabulary (higher Zipf)."""

    def test_low_difficulty_prefers_common_words(self, engine) -> None:
        """At difficulty=0, selected word has higher Zipf than at difficulty=100."""
        freq = FrequencyIndex()
        moves = [
            make_move('THE', 10),
            make_move('HOUSE', 20),
            make_move('QUAFF', 40),
            make_move('ZYZZYVA', 60),
        ]
        result_0 = engine.select_move(moves, difficulty=0)
        result_100 = engine.select_move(moves, difficulty=100)
        assert result_0 is not None
        assert result_100 is not None

        zipf_0 = freq.zipf(result_0.word)
        zipf_100 = freq.zipf(result_100.word)
        assert zipf_0 >= zipf_100, (
            f"At difficulty=0, expected a more common word than at difficulty=100. "
            f"Got '{result_0.word}' (Zipf {zipf_0:.2f}) vs '{result_100.word}' (Zipf {zipf_100:.2f})"
        )


class TestDifficultyOOVHandling:
    """DIFF-02: OOV words are deprioritized at low difficulty but not excluded."""

    def test_oov_words_handled(self, engine) -> None:
        """At difficulty=0, OOV ('ZYZZYVA') is NOT selected; at 100% it IS selected."""
        moves = [
            make_move('ZYZZYVA', 50),
            make_move('CAT', 30),
            make_move('DOG', 25),
        ]
        result_0 = engine.select_move(moves, difficulty=0)
        result_100 = engine.select_move(moves, difficulty=100)
        assert result_0 is not None
        assert result_100 is not None

        # At 0%: OOV maximally obscure — should NOT be chosen
        assert result_0.word != 'ZYZZYVA', (
            f"At difficulty=0, OOV word 'ZYZZYVA' should be deprioritized, "
            f"but was selected"
        )
        # At 100%: highest score wins — 'ZYZZYVA' IS chosen
        assert result_100.word == 'ZYZZYVA', (
            f"At difficulty=100, highest-scoring move 'ZYZZYVA' should be selected, "
            f"got '{result_100.word}'"
        )


class TestDifficultyStrategyVariation:
    """DIFF-03: Different difficulties produce different word selections."""

    def test_strategy_variation_produces_different_words(self, engine) -> None:
        """At least 3 different words selected across difficulty levels 0/25/50/75/100."""
        # 10+ moves spanning scores and commonalities
        moves = [
            make_move('ZYZZYVA', 100),   # OOV, highest score
            make_move('QUIXOTIC', 85),   # rare, high score
            make_move('QUAFF', 70),      # uncommon, medium-high score
            make_move('SCARE', 55),      # uncommon, medium score
            make_move('BRACE', 45),      # uncommon, medium score
            make_move('RACE', 35),       # fairly common, medium score
            make_move('CARD', 28),       # common, low-medium score
            make_move('CAR', 22),        # common, low-medium score
            make_move('CAT', 18),        # common, low score
            make_move('THE', 10),        # most common, lowest score
        ]
        difficulties = [0, 25, 50, 75, 100]
        selected_words = [
            engine.select_move(moves, difficulty=d).word
            for d in difficulties
        ]
        unique_words = set(selected_words)
        assert len(unique_words) >= 3, (
            f"Expected at least 3 different words across difficulties, "
            f"got {len(unique_words)}: {unique_words}. "
            f"Selected: {list(zip(difficulties, selected_words))}"
        )


class TestDifficultyEdgeCases:
    """Edge cases: single move, same scores, empty list, determinism, clamping."""

    def test_single_move_edge_case(self, engine) -> None:
        """select_move with a single move returns it at any difficulty."""
        single = make_move('CAT', 30)
        result = engine.select_move([single], difficulty=50)
        assert result is not None
        assert result.word == 'CAT'
        assert result.score == 30

    def test_all_same_score_uses_frequency(self, engine) -> None:
        """When all moves have the same score, frequency tiebreaker applies; no crash."""
        moves = [
            make_move('THE', 30),
            make_move('QUAFF', 30),
            make_move('ZYZZYVA', 30),
        ]
        # Should not raise; specifically at difficulty=0 frequency dominates
        result_0 = engine.select_move(moves, difficulty=0)
        result_100 = engine.select_move(moves, difficulty=100)
        assert result_0 is not None
        assert result_100 is not None
        # With same scores, frequency tiebreaker should pick most common at 0%
        freq = FrequencyIndex()
        assert result_0.word == 'THE', (
            f"At difficulty=0 with same scores, expected 'THE' (most common), got '{result_0.word}'"
        )
        # At 100%, all scores equal; tiebreaker still picks most common
        assert result_100.word == 'THE', (
            f"At difficulty=100 with same scores, tiebreaker should pick 'THE' (highest freq), got '{result_100.word}'"
        )

    def test_empty_moves_returns_none(self, engine) -> None:
        """select_move([]) returns None without crashing."""
        result = engine.select_move([], difficulty=50)
        assert result is None

    def test_deterministic_output(self, engine) -> None:
        """Same inputs always produce the same output (no randomness)."""
        moves = [
            make_move('QUIXOTIC', 120),
            make_move('SCARE', 60),
            make_move('CAT', 30),
            make_move('THE', 15),
        ]
        result_1 = engine.select_move(moves, difficulty=42)
        result_2 = engine.select_move(moves, difficulty=42)
        assert result_1 is not None
        assert result_2 is not None
        assert result_1.word == result_2.word, (
            f"Non-deterministic: first call returned '{result_1.word}', "
            f"second returned '{result_2.word}'"
        )
        assert result_1.score == result_2.score

    def test_difficulty_clamping(self, engine) -> None:
        """Out-of-range difficulty values are clamped: >100 acts like 100, <0 acts like 0."""
        moves = [
            make_move('QUIXOTIC', 120),
            make_move('CAT', 30),
            make_move('THE', 15),
        ]
        result_100 = engine.select_move(moves, difficulty=100)
        result_over = engine.select_move(moves, difficulty=150)
        assert result_over is not None
        assert result_over.word == result_100.word, (
            f"difficulty=150 should behave like 100, but got '{result_over.word}' "
            f"vs '{result_100.word}'"
        )

        result_0 = engine.select_move(moves, difficulty=0)
        result_under = engine.select_move(moves, difficulty=-10)
        assert result_under is not None
        assert result_under.word == result_0.word, (
            f"difficulty=-10 should behave like 0, but got '{result_under.word}' "
            f"vs '{result_0.word}'"
        )


# ---------------------------------------------------------------------------
# Integration tests (Task 2): DifficultyEngine with real GameEngine output
# ---------------------------------------------------------------------------

class TestDifficultyIntegration:
    """Integration: DifficultyEngine works with real GameEngine move output."""

    def test_integration_with_game_engine(self, engine, small_wordlist_file) -> None:
        """DifficultyEngine.select_move() works on real GameEngine output."""
        from src.engine import GameEngine
        game_engine = GameEngine(str(small_wordlist_file))
        rack = ['C', 'A', 'R', 'D', 'S', 'E', 'B']
        moves = game_engine.find_moves(rack)

        if not moves:
            pytest.skip("No moves found for test rack — wordlist may be too small")

        result_100 = engine.select_move(moves, difficulty=100)
        result_0 = engine.select_move(moves, difficulty=0)

        assert result_100 is not None
        assert result_0 is not None
        # At 100%, should return the top-scoring move
        assert result_100.score == moves[0].score, (
            f"At difficulty=100, expected score {moves[0].score}, got {result_100.score}"
        )
        # At 0%, should return a different (weaker) move if multiple moves exist
        if len(moves) > 1:
            assert result_0.score <= result_100.score, (
                f"At difficulty=0, score ({result_0.score}) should be <= "
                f"difficulty=100 score ({result_100.score})"
            )

    def test_integration_difficulty_gradient(self, engine, small_wordlist_file) -> None:
        """Score at difficulty=100 >= 75 >= 50 >= 25 >= 0 (monotonic non-increasing)."""
        from src.engine import GameEngine
        game_engine = GameEngine(str(small_wordlist_file))
        rack = ['C', 'A', 'R', 'D', 'S', 'E', 'B']
        moves = game_engine.find_moves(rack)

        if len(moves) < 3:
            pytest.skip("Too few moves for gradient test")

        difficulties = [100, 75, 50, 25, 0]
        scores = [
            engine.select_move(moves, difficulty=d).score
            for d in difficulties
        ]
        # Monotonic non-increasing: each score <= previous
        for i in range(len(scores) - 1):
            assert scores[i] >= scores[i + 1], (
                f"Score non-monotonic: difficulty={difficulties[i]} score={scores[i]} "
                f"but difficulty={difficulties[i+1]} score={scores[i+1]}"
            )

    def test_integration_second_turn(self, engine, small_wordlist_file) -> None:
        """DifficultyEngine works on second-turn moves after a board play."""
        from src.engine import GameEngine
        game_engine = GameEngine(str(small_wordlist_file))

        # First turn: play best move
        first_rack = ['C', 'A', 'R', 'D', 'S', 'E', 'B']
        first_moves = game_engine.find_moves(first_rack)
        if not first_moves:
            pytest.skip("No first-turn moves found")

        best = first_moves[0]
        game_engine.play_move(best)

        # Second turn: find moves with a new rack
        second_rack = ['A', 'E', 'R', 'S', 'T', 'I', 'N']
        second_moves = game_engine.find_moves(second_rack)

        if not second_moves:
            pytest.skip("No second-turn moves found")

        # DifficultyEngine should work on second-turn moves
        result = engine.select_move(second_moves, difficulty=50)
        assert result is not None, "select_move returned None for second-turn moves"
        assert isinstance(result, Move)
