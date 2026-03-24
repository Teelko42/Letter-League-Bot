from __future__ import annotations

import pytest

from src.difficulty import FrequencyIndex


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
    """OOV game-dictionary words return Zipf 0.0 (not excluded)."""

    def test_frequency_oov_words(self, freq: FrequencyIndex) -> None:
        oov_words = ['zyzzyva', 'xu', 'qat']
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
