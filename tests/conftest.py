from __future__ import annotations

import pytest


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
