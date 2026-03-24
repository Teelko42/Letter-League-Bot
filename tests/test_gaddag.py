from __future__ import annotations

import pickle
from pathlib import Path

import pytest

from src.engine.gaddag import GADDAG


class TestGADDAGBuild:
    """Tests for GADDAG construction from wordlist."""

    def test_build_from_wordlist(self, small_wordlist_file):
        """GADDAG built from wordlist should have a non-empty root dict."""
        gaddag = GADDAG.from_wordlist(small_wordlist_file)
        assert isinstance(gaddag.root, dict)
        assert len(gaddag.root) > 0

    def test_word_lookup_valid(self, small_wordlist_file, small_wordlist):
        """Every word in the wordlist should be recognised as valid."""
        gaddag = GADDAG.from_wordlist(small_wordlist_file)
        for word in small_wordlist:
            assert gaddag.is_valid_word(word), f"Expected '{word}' to be valid"

    def test_word_lookup_case_insensitive(self, small_wordlist_file):
        """Word lookup should be case-insensitive."""
        gaddag = GADDAG.from_wordlist(small_wordlist_file)
        assert gaddag.is_valid_word('cab')
        assert gaddag.is_valid_word('CAB')
        assert gaddag.is_valid_word('Cab')

    def test_word_lookup_invalid(self, small_wordlist_file):
        """Words not in the wordlist should be rejected."""
        gaddag = GADDAG.from_wordlist(small_wordlist_file)
        for word in ('ZZZ', 'QWERTY', 'XYZ', 'ABCDEF'):
            assert not gaddag.is_valid_word(word), f"Expected '{word}' to be invalid"

    def test_single_letter_rejected(self, small_wordlist_file):
        """Single-letter words should always be rejected (minimum length is 2)."""
        gaddag = GADDAG.from_wordlist(small_wordlist_file)
        for letter in ('A', 'I'):
            assert not gaddag.is_valid_word(letter), (
                f"Expected single letter '{letter}' to be rejected"
            )


class TestGADDAGCache:
    """Tests for GADDAG pickle cache serialization and invalidation."""

    def test_cache_roundtrip(self, small_wordlist_file, small_wordlist, tmp_path):
        """Save GADDAG to cache, load from cache, verify word lookups match."""
        cache_path = tmp_path / 'gaddag.pkl'

        # Build and save
        gaddag_original = GADDAG.from_wordlist(small_wordlist_file, cache_path)
        assert cache_path.exists(), "Cache file should have been created"

        # Load from cache
        gaddag_cached = GADDAG.from_wordlist(small_wordlist_file, cache_path)

        for word in small_wordlist:
            assert gaddag_cached.is_valid_word(word), (
                f"Cached GADDAG should recognise '{word}'"
            )
        for word in ('ZZZ', 'QWERTY'):
            assert not gaddag_cached.is_valid_word(word)

    def test_cache_invalidation(self, tmp_path, small_wordlist):
        """Cache is rebuilt when the wordlist changes."""
        wordlist_file = tmp_path / 'wordlist.txt'
        cache_path = tmp_path / 'gaddag.pkl'

        # Initial build — write wordlist without 'ZEBRA'
        words_v1 = [w for w in small_wordlist if w != 'RACE']
        wordlist_file.write_text('\n'.join(words_v1), encoding='utf-8')

        gaddag_v1 = GADDAG.from_wordlist(wordlist_file, cache_path)
        assert not gaddag_v1.is_valid_word('ZEBRA'), "ZEBRA not in v1 list"

        # Modify wordlist — add 'ZEBRA', remove 'RED'
        words_v2 = [w for w in words_v1 if w != 'RED'] + ['ZEBRA']
        wordlist_file.write_text('\n'.join(words_v2), encoding='utf-8')

        gaddag_v2 = GADDAG.from_wordlist(wordlist_file, cache_path)
        assert gaddag_v2.is_valid_word('ZEBRA'), "ZEBRA should be valid in v2"
        assert not gaddag_v2.is_valid_word('RED'), "RED was removed from v2"


class TestGADDAGEdgeCases:
    """Tests for edge-case input handling."""

    def test_separator_not_in_words(self, tmp_path):
        """Words containing the GADDAG separator '+' should be silently skipped."""
        wordlist_file = tmp_path / 'wordlist.txt'
        wordlist_file.write_text('CAT\nDO+G\nFOX\n', encoding='utf-8')

        gaddag = GADDAG.from_wordlist(wordlist_file)
        assert gaddag.is_valid_word('CAT')
        assert gaddag.is_valid_word('FOX')
        # DO+G should be skipped, not cause an error
        assert not gaddag.is_valid_word('DOG')
        assert not gaddag.is_valid_word('DO+G')

    def test_empty_lines_and_whitespace(self, tmp_path, small_wordlist):
        """Wordlist with blank lines, leading/trailing whitespace, and mixed case builds correctly."""
        wordlist_file = tmp_path / 'wordlist.txt'
        # Write with extra whitespace and blank lines
        content = '\n'.join(
            f'  {w.lower()}  ' if i % 2 == 0 else f'{w.upper()}'
            for i, w in enumerate(small_wordlist)
        )
        content = '\n\n' + content + '\n\n   \n'
        wordlist_file.write_text(content, encoding='utf-8')

        gaddag = GADDAG.from_wordlist(wordlist_file)
        for word in small_wordlist:
            assert gaddag.is_valid_word(word), (
                f"Expected '{word}' to be valid from messy wordlist"
            )
