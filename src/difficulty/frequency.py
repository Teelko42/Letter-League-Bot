from __future__ import annotations

from wordfreq import zipf_frequency


class FrequencyIndex:
    """Wraps wordfreq for O(1) amortized per-word Zipf frequency lookups.

    Uses lazy caching over zipf_frequency() to avoid the slow pre-computation
    of the full 321k-word dictionary at startup. Each word is looked up once
    and cached for O(1) subsequent access.

    The Zipf scale ranges from 0 (OOV/never seen) to ~8 (most common words
    like 'the'). 'cat' is ~4.8, 'quasar' is ~2.9.

    OOV words (not in wordfreq corpus) return 0.0 — they are not excluded from
    the difficulty system, just scored as maximally obscure.

    Example:
        freq = FrequencyIndex()
        freq.zipf('the')       # ~7.73
        freq.zipf('CAT')       # ~4.78 (case-insensitive)
        freq.zipf('zyzzyva')   # 0.0 (OOV)
        freq.normalized('the') # ~0.97 (in [0.0, 1.0])
    """

    OOV_ZIPF: float = 0.0
    MAX_ZIPF: float = 8.0  # approximate upper bound for normalization

    def __init__(self, lang: str = 'en') -> None:
        """Prepare a FrequencyIndex for the given language.

        No upfront dictionary loading — word lookups are lazy-cached on first
        access. This makes instantiation nearly instant.

        Args:
            lang: Language code for wordfreq. Default 'en' (English).
        """
        self._lang = lang
        self._cache: dict[str, float] = {}

    def zipf(self, word: str) -> float:
        """Return Zipf frequency for a word (0.0-8.0). OOV returns 0.0.

        Lookups are case-insensitive: 'CAT', 'cat', and 'Cat' all return the
        same score because wordfreq data is lowercase.

        Args:
            word: The word to look up (case-insensitive).

        Returns:
            Zipf frequency: ~8 for most common, ~0 for OOV/very rare.
        """
        key = word.lower()
        if key not in self._cache:
            self._cache[key] = zipf_frequency(key, self._lang)
        return self._cache[key]

    def normalized(self, word: str) -> float:
        """Return frequency normalized to [0.0, 1.0]. 1.0 = most common.

        Normalizes against MAX_ZIPF (fixed constant ~8.0), not against the
        current word set. This ensures a word common among rare words is not
        treated as common in absolute terms.

        OOV words return exactly 0.0.

        Args:
            word: The word to look up (case-insensitive).

        Returns:
            Normalized frequency in [0.0, 1.0].
        """
        return self.zipf(word) / self.MAX_ZIPF
