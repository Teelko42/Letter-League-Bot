from __future__ import annotations

import hashlib
import pickle
from pathlib import Path
from typing import Optional


class GADDAG:
    """GADDAG data structure for fast bidirectional word lookup.

    Implements the Gordon (1994) GADDAG algorithm using a pure-Python
    dict-based node graph. Each node is a dict mapping a character to
    the next node. Terminal word positions are marked with TERMINAL -> None.

    The GADDAG encodes every word W of length N as N+1 paths:
        Path 0: SEPARATOR + W          (anchor at first letter)
        Path i (1..N-1): rev(W[:i]) + SEPARATOR + W[i:]
        Path N: rev(W) + SEPARATOR     (full reversal path)
    Each path is terminated with the TERMINAL marker.
    """

    SEPARATOR = '+'
    TERMINAL = '$'

    def __init__(self) -> None:
        self.root: dict = {}

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def add_word(self, word: str) -> None:
        """Add all GADDAG paths for a single word (must be uppercase, alpha-only)."""
        n = len(word)
        for i in range(n):
            # Build: reversed(word[:i]) + SEPARATOR + word[i:]
            node = self.root
            # Reversed prefix (empty when i == 0)
            for ch in reversed(word[:i]):
                node = node.setdefault(ch, {})
            # Separator
            node = node.setdefault(self.SEPARATOR, {})
            # Forward suffix
            for ch in word[i:]:
                node = node.setdefault(ch, {})
            # Mark terminal
            node[self.TERMINAL] = None

    def build_from_file(self, wordlist_path: Path) -> None:
        """Read a wordlist file line by line and populate the GADDAG.

        Lines are stripped, uppercased, and filtered:
        - Skip words shorter than 2 characters.
        - Skip words containing non-alpha characters or the separator.
        """
        with open(wordlist_path, encoding='utf-8') as f:
            for line in f:
                word = line.strip().upper()
                if len(word) < 2:
                    continue
                if not word.isalpha():
                    continue
                if self.SEPARATOR in word:
                    continue
                self.add_word(word)

    # ------------------------------------------------------------------
    # Word lookup
    # ------------------------------------------------------------------

    def is_valid_word(self, word: str) -> bool:
        """Return True if *word* is in the GADDAG dictionary.

        Lookup uses the path: word[0] + SEPARATOR + word[1:]
        (anchor at the first letter — the simplest GADDAG lookup).

        Single-letter words are always rejected (minimum word length is 2).
        """
        word = word.strip().upper()
        if len(word) < 2:
            return False

        node = self.root
        # First character
        if word[0] not in node:
            return False
        node = node[word[0]]
        # Separator
        if self.SEPARATOR not in node:
            return False
        node = node[self.SEPARATOR]
        # Remaining characters
        for ch in word[1:]:
            if ch not in node:
                return False
            node = node[ch]
        # Terminal marker
        return self.TERMINAL in node

    # ------------------------------------------------------------------
    # Cache serialization
    # ------------------------------------------------------------------

    @staticmethod
    def _wordlist_hash(wordlist_path: Path) -> str:
        """Return the MD5 hex digest of the wordlist file contents."""
        return hashlib.md5(wordlist_path.read_bytes()).hexdigest()

    def save_cache(self, cache_path: Path, wordlist_path: Path) -> None:
        """Pickle the GADDAG root and the wordlist hash to *cache_path*."""
        cache_path.parent.mkdir(exist_ok=True, parents=True)
        payload = {
            'root': self.root,
            'hash': self._wordlist_hash(wordlist_path),
        }
        with open(cache_path, 'wb') as f:
            pickle.dump(payload, f)

    @classmethod
    def load_cache(cls, cache_path: Path, wordlist_path: Path) -> Optional['GADDAG']:
        """Attempt to load GADDAG from pickle cache.

        Returns a GADDAG instance if the cache exists and the wordlist hash
        matches; otherwise returns None (cache miss or stale).
        """
        if not cache_path.exists():
            return None
        try:
            with open(cache_path, 'rb') as f:
                cached = pickle.load(f)
            current_hash = cls._wordlist_hash(wordlist_path)
            if cached.get('hash') != current_hash:
                return None
            instance = cls()
            instance.root = cached['root']
            return instance
        except Exception:
            return None

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_wordlist(
        cls,
        wordlist_path: Path,
        cache_path: Optional[Path] = None,
    ) -> 'GADDAG':
        """Build or load a GADDAG for the given wordlist.

        If *cache_path* is provided, attempts to load from cache first.
        On cache miss, builds from the wordlist file and saves to cache.
        """
        wordlist_path = Path(wordlist_path)

        if cache_path is not None:
            cache_path = Path(cache_path)
            cached = cls.load_cache(cache_path, wordlist_path)
            if cached is not None:
                return cached

        instance = cls()
        instance.build_from_file(wordlist_path)

        if cache_path is not None:
            instance.save_cache(cache_path, wordlist_path)

        return instance
