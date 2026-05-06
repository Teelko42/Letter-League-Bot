from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _isolate_rejected_words(tmp_path, monkeypatch):
    """Point the rejected_words module at an empty per-test file.

    The production blacklist at data/rejected_words.txt accrues 100s of
    entries from real autoplay rejections. compute_cross_checks now consults
    that list, so tests that were written against a clean dictionary would
    flake against whatever the global blacklist happens to contain (e.g.
    "be" is currently blacklisted, which broke test_cross_checks_between_tiles).
    """
    from src.engine import rejected_words

    empty = tmp_path / "rejected_words.txt"
    empty.write_text("", encoding="utf-8")
    rejected_words.configure(empty)
    yield
    rejected_words.configure(rejected_words.DEFAULT_PATH)


@pytest.fixture
def sample_rack() -> list[str]:
    """A sample 7-tile rack for testing."""
    return ['A', 'B', 'C', 'D', 'E', 'R', 'S']


@pytest.fixture
def small_wordlist() -> list[str]:
    """A small wordlist of ~25 common 2-5 letter words for testing."""
    return [
        'AB', 'AD', 'AE', 'BE', 'BA',
        'CAB', 'CAR', 'CARD', 'CARDS', 'CARE',
        'BRACE', 'RACED', 'SCARE', 'CABS', 'ARE',
        'ACE', 'ACES', 'RED', 'BED', 'BAD',
        'BAR', 'BARS', 'SCAR', 'ARCS', 'RACE',
    ]


@pytest.fixture
def small_wordlist_file(tmp_path, small_wordlist):
    """Write small_wordlist to a temp file and return the path."""
    wordlist_file = tmp_path / 'wordlist.txt'
    wordlist_file.write_text('\n'.join(small_wordlist), encoding='utf-8')
    return wordlist_file
