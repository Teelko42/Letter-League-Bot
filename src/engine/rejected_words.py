"""Persistent blacklist of words the live game has rejected.

Letter League's dictionary is stricter than the bot's GADDAG wordlist, so
the engine regularly generates words that get rejected by the game UI.
Each rejection costs ~45 s (tile placement + confirm poll + recall). This
module records every word the game rejects and filters it out of future
candidate lists.

The blacklist is a flat text file (one lowercase word per line) loaded on
process start and updated in-memory + on disk when words are added. It is
intentionally append-only — if a word turns out to be legitimately playable
in a different context, the cost is that we miss one candidate, not that
the bot gets stuck.
"""

from __future__ import annotations

from pathlib import Path
from threading import Lock

from loguru import logger

DEFAULT_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "rejected_words.txt"

_lock = Lock()
_cache: set[str] | None = None
_path: Path = DEFAULT_PATH


def _load(path: Path) -> set[str]:
    if not path.exists():
        return set()
    with path.open("r", encoding="utf-8") as fh:
        return {line.strip().lower() for line in fh if line.strip()}


def configure(path: Path) -> None:
    """Override the blacklist file path (tests, alternative profiles)."""
    global _cache, _path
    with _lock:
        _path = path
        _cache = None  # Force reload on next access


def _ensure_loaded() -> set[str]:
    global _cache
    if _cache is None:
        _cache = _load(_path)
        logger.info("Loaded {} rejected words from {}", len(_cache), _path)
    return _cache


def is_rejected(word: str) -> bool:
    """Return True if *word* is in the blacklist (case-insensitive)."""
    with _lock:
        cache = _ensure_loaded()
        return word.lower() in cache


def add(word: str) -> bool:
    """Persist *word* as rejected. Returns True if newly added."""
    with _lock:
        cache = _ensure_loaded()
        normalized = word.lower()
        if normalized in cache:
            return False
        cache.add(normalized)
        _path.parent.mkdir(parents=True, exist_ok=True)
        with _path.open("a", encoding="utf-8") as fh:
            fh.write(normalized + "\n")
        logger.info("Blacklisted rejected word '{}' (total: {})", normalized, len(cache))
        return True


def filter_moves(moves):  # type: ignore[no-untyped-def]
    """Drop moves whose .word is blacklisted.

    Kept duck-typed so engine module imports stay minimal — callers pass
    any iterable of objects with a `.word` attribute and get back a list
    preserving the original ordering.
    """
    with _lock:
        cache = _ensure_loaded()
    materialized = list(moves)
    if not cache:
        return materialized
    kept = [m for m in materialized if m.word.lower() not in cache]
    dropped = len(materialized) - len(kept)
    if dropped:
        logger.debug("rejected_words: filtered {} blacklisted candidate(s)", dropped)
    return kept
