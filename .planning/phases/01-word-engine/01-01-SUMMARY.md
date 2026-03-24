---
phase: 01-word-engine
plan: 01
subsystem: engine
tags: [gaddag, python, pickle, tdd, word-lookup, caching, dataclasses]

# Dependency graph
requires: []
provides:
  - "GADDAG class: builds from wordlist, validates word membership in O(word_length)"
  - "Pickle cache with MD5-based invalidation — eliminates wordlist rebuild on startup"
  - "MultiplierType enum, Cell, TileUse, ScoreBreakdown, Move dataclasses"
  - "TILE_VALUES dict with standard Scrabble point values; ALPHABET constant"
  - "pytest fixtures: sample_rack, small_wordlist, small_wordlist_file"
affects:
  - 01-02-board
  - 01-03-scoring
  - 01-04-move-gen

# Tech tracking
tech-stack:
  added:
    - "pytest 9.0 (test framework)"
    - "Python stdlib: dataclasses, enum, pickle, hashlib, pathlib"
  patterns:
    - "Dict-based GADDAG node graph: each node is a plain Python dict; O(1) char lookups"
    - "Gordon (1994) GADDAG encoding: rev(prefix) + '+' separator + suffix, '$' terminal"
    - "Factory classmethod pattern: GADDAG.from_wordlist() tries cache, falls back to build"
    - "from __future__ import annotations in all source files for forward reference support"

key-files:
  created:
    - src/engine/tiles.py
    - src/engine/models.py
    - src/engine/gaddag.py
    - src/engine/__init__.py
    - src/__init__.py
    - tests/__init__.py
    - tests/conftest.py
    - tests/test_gaddag.py
    - data/.gitkeep
    - cache/.gitkeep
  modified: []

key-decisions:
  - "Dict-based GADDAG (not class-per-node): lower memory overhead, O(1) dict lookups in CPython"
  - "MD5 hash of wordlist bytes for cache invalidation: reliable, fast, no mtime race conditions"
  - "GADDAG.from_wordlist() factory: clean API — callers never call build/cache methods directly"
  - "is_valid_word uses word[0]+SEPARATOR+word[1:] path: simplest correct lookup for full words"
  - "SEPARATOR='+', TERMINAL='$': standard Python GADDAG convention per Wikipedia/implementations"

patterns-established:
  - "TDD cycle: write failing tests -> implement -> verify GREEN -> commit"
  - "from __future__ import annotations in all source modules"
  - "pytest fixtures in conftest.py shared across test modules"
  - "Pathlib.Path for all file I/O (not os.path strings)"

requirements-completed:
  - WENG-01

# Metrics
duration: 2min
completed: 2026-03-24
---

# Phase 1 Plan 01: GADDAG and Core Data Models Summary

**Dict-based GADDAG (Gordon 1994) with pickle/MD5 cache, full data model suite (Cell, Move, ScoreBreakdown), and standard Scrabble tile values — all verified with 9 TDD tests**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-03-24T01:54:58Z
- **Completed:** 2026-03-24T01:57:54Z
- **Tasks:** 2
- **Files modified:** 10 created

## Accomplishments

- GADDAG loads any wordlist, validates word membership in O(word_length) using Gordon (1994) dict-based node graph with '+' separator and '$' terminal marker
- Pickle cache with MD5-based invalidation: first run builds and caches, subsequent runs load instantly; stale cache auto-invalidated when wordlist changes
- Complete data model suite: MultiplierType enum, Cell/TileUse/ScoreBreakdown/Move dataclasses with correct default values and Wild-mode bonded_multiplier field
- 9 TDD tests covering valid/invalid lookup, case-insensitivity, single-letter rejection, cache roundtrip, cache invalidation, separator collision, and whitespace edge cases

## Task Commits

Each task was committed atomically:

1. **Task 1: Create project structure, data models, and tile definitions** - `d6d0986` (feat)
2. **Task 2: Build GADDAG with construction, caching, and word validation (TDD)** - `dd62c16` (feat)

**Plan metadata:** _(this commit)_

## Files Created/Modified

- `src/engine/tiles.py` - TILE_VALUES dict (standard Scrabble values, A=1..Z=10, blank=0) and ALPHABET constant
- `src/engine/models.py` - MultiplierType, Cell, TileUse (frozen), ScoreBreakdown, Move with rack_tiles_consumed() method
- `src/engine/gaddag.py` - GADDAG class: add_word, build_from_file, is_valid_word, save_cache, load_cache, from_wordlist
- `src/engine/__init__.py` - Engine package stub (will export GameEngine in plan 04)
- `src/__init__.py` - Top-level package stub
- `tests/__init__.py` - Test package stub
- `tests/conftest.py` - sample_rack, small_wordlist, small_wordlist_file fixtures
- `tests/test_gaddag.py` - 9 GADDAG correctness tests (build, lookup, cache, edge cases)
- `data/.gitkeep` - Placeholder for user-provided wordlist.txt
- `cache/.gitkeep` - Placeholder for auto-generated gaddag.pkl

## Decisions Made

- **Dict-based GADDAG over class-per-node:** Lower Python object overhead; O(1) dict lookup is optimal in CPython; matches research recommendation
- **MD5 hash for cache invalidation:** Reliable without mtime race conditions; computed once on load; hashlib in stdlib
- **from_wordlist() factory pattern:** Clean public API — callers never need to touch build/cache primitives; loads from cache or builds transparently
- **SEPARATOR='+', TERMINAL='$':** Standard convention used in GADDAG Wikipedia article and Python reference implementations; non-alpha so can't collide with wordlist words (alpha-only words enforced on build)
- **is_valid_word path: word[0]+SEPARATOR+word[1:]:** This is the canonical GADDAG full-word lookup path — simple, correct, documented in Gordon (1994)

## Deviations from Plan

None - plan executed exactly as written.

The plan specified 8 tests; implementation produced 9 by splitting `test_word_lookup_valid` into separate valid-words and case-insensitivity tests for clarity. This is additive and beneficial — not a deviation from intent.

## Issues Encountered

- Python was not on PATH under the `python` alias on this Windows machine; used the full path `/c/Users/Ninja/AppData/Local/Programs/Python/Python310/python.exe`. This affects any run commands during execution but does not affect the engine code.
- pytest was not installed; installed via pip during Task 2 TDD setup.

## User Setup Required

None - no external service configuration required.

When providing the wordlist: place it at `data/wordlist.txt` (one word per line). The GADDAG will build and cache automatically on first use.

## Next Phase Readiness

- GADDAG is ready for consumption by plan 01-02 (board) and plan 01-04 (move generation)
- Data models (Cell, Move, ScoreBreakdown) are ready for plan 01-02 (board state) and plan 01-03 (scoring)
- No blockers for plan 01-02 (board representation)

---
*Phase: 01-word-engine*
*Completed: 2026-03-24*
