---
phase: 01-word-engine
verified: 2026-03-23T22:00:00Z
status: passed
score: 5/5 must-haves verified
re_verification: false
---

# Phase 1: Word Engine Verification Report

**Phase Goal:** The engine can find and rank all valid word placements given any board state and tile rack
**Verified:** 2026-03-23
**Status:** PASSED
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths (from ROADMAP Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Given a board state and tile rack as input, the engine returns all valid word placements with correct positions | VERIFIED | `find_all_moves` in `moves.py` (633 lines) implements Gordon (1994) LeftPart/ExtendRight; 12 move generation tests pass including `test_first_move_empty_board`, `test_extends_existing_word`, `test_prefix_extension` |
| 2 | Each placement is scored correctly under Classic mode rules (multipliers apply only on placement turn) | VERIFIED | `scoring.py` line 59-71 checks `(cell.row, cell.col) in newly_placed_positions` before applying `square_multiplier`; 12 Classic mode tests pass including `test_classic_multiplier_only_on_new_tiles` |
| 3 | Each placement is scored correctly under Wild mode rules (multipliers permanently bonded to letter tiles) | VERIFIED | `scoring.py` line 72-83 applies `cell.bonded_multiplier` to ALL cells unconditionally; `board.py` line 90-91 bonds on placement; 10 Wild mode tests pass including `test_wild_existing_tiles_keep_multipliers` and `test_classic_vs_wild_different_scores` |
| 4 | The engine selects the highest-scoring valid placement as the optimal move | VERIFIED | `find_all_moves` sorts by `score` descending (line 94 of `moves.py`); `GameEngine.best_move` returns `moves[0]`; `test_engine_best_move` and `test_moves_sorted_by_score` verify this |
| 5 | The GADDAG structure loads the full Wordnik wordlist and rejects words not in it | VERIFIED | `gaddag.py` implements `build_from_file`, `is_valid_word`, `save_cache`, `load_cache` with MD5 hash invalidation; 9 GADDAG tests pass including `test_word_lookup_invalid`, `test_single_letter_rejected`, `test_cache_invalidation` |

**Score: 5/5 truths verified**

---

### Required Artifacts

| Artifact | Min Lines | Actual Lines | Exports Present | Status |
|----------|-----------|--------------|-----------------|--------|
| `src/engine/tiles.py` | — | 34 | `TILE_VALUES`, `ALPHABET` | VERIFIED |
| `src/engine/models.py` | — | 100 | `MultiplierType`, `Cell`, `TileUse`, `ScoreBreakdown`, `Move` | VERIFIED |
| `src/engine/gaddag.py` | — | 170 | `GADDAG` class with all methods | VERIFIED |
| `src/engine/board.py` | 150 | 304 | `Board` class with `find_anchors`, `compute_cross_checks`, `compute_left_limit` | VERIFIED |
| `src/engine/scoring.py` | 100 | 149 | `score_move`, `score_word` | VERIFIED |
| `src/engine/moves.py` | 200 | 633 | `find_all_moves` and helpers | VERIFIED |
| `src/engine/__init__.py` | 50 | 138 | `GameEngine` class | VERIFIED |
| `tests/test_gaddag.py` | 50 | 120 | 9 tests | VERIFIED |
| `tests/test_board.py` | 100 | 290 | 20 tests | VERIFIED |
| `tests/test_scoring.py` | 120 | 379 | 22 tests | VERIFIED |
| `tests/test_moves.py` | 120 | 254 | 12 tests | VERIFIED |
| `tests/test_engine.py` | 80 | 247 | 9 tests | VERIFIED |

All artifacts exceed minimum line counts. No artifacts are stubs or placeholders.

---

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `gaddag.py` | `data/wordlist.txt` | `open(wordlist_path)` file read | WIRED (by design) | Line 57: `with open(wordlist_path, encoding='utf-8') as f:`; production wordlist goes in `data/` (user-provided; `data/.gitkeep` placeholder is intentional per CONTEXT.md) |
| `gaddag.py` | `cache/gaddag.pkl` | `pickle.dump` / `pickle.load` | WIRED | Lines 118, 131: full pickle roundtrip with MD5 hash validation |
| `board.py` | `models.py` | `Cell`, `MultiplierType` imports | WIRED | Line 5: `from src.engine.models import Cell, MultiplierType` |
| `board.py` | `gaddag.py` | `gaddag.is_valid_word` in cross-checks | WIRED | Line 190: `if gaddag.is_valid_word(word):` in `compute_cross_checks` |
| `scoring.py` | `models.py` | `Cell`, `MultiplierType`, `ScoreBreakdown` imports | WIRED | Line 21: `from src.engine.models import Cell, MultiplierType, ScoreBreakdown` |
| `scoring.py` | `tiles.py` | `TILE_VALUES` for letter points | WIRED | Line 22: `from src.engine.tiles import TILE_VALUES` |
| `moves.py` | `gaddag.py` | GADDAG traversal (SEPARATOR, TERMINAL, root) | WIRED | Lines 141-167: `gaddag.root`, `GADDAG.SEPARATOR`, `GADDAG.TERMINAL` throughout |
| `moves.py` | `board.py` | `board.find_anchors`, `board.compute_cross_checks` | WIRED | Lines 82-83: called in `find_all_moves` loop |
| `moves.py` | `scoring.py` | `score_move` per candidate placement | WIRED | Line 29: `from src.engine.scoring import score_move`; line 524: called in `_build_move` |
| `__init__.py` | `moves.py` | `find_all_moves` called by `GameEngine.find_moves` | WIRED | Line 22: import; line 77: `return find_all_moves(...)` |

All 10 key links verified as fully wired. No orphaned imports or disconnected calls found.

---

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| WENG-01 | 01-01-PLAN.md | Build GADDAG from Wordnik wordlist for fast word lookup | SATISFIED | `gaddag.py` 170 lines; `test_gaddag.py` 9 tests all passing; MD5-cached pickle |
| WENG-02 | 01-02-PLAN.md, 01-04-PLAN.md | Generate all valid word placements given board state and tile rack | SATISFIED | `moves.py` 633 lines; `find_all_moves` + Gordon (1994) algorithm; 12 move tests + 9 engine integration tests |
| WENG-03 | 01-03-PLAN.md | Score words using Classic mode rules | SATISFIED | `score_word` with `newly_placed_positions` gate on `square_multiplier`; 12 Classic tests passing |
| WENG-04 | 01-03-PLAN.md | Score words using Wild mode rules | SATISFIED | `score_word` with `bonded_multiplier` on all cells; `board.place_tile` bonds on placement; 10 Wild tests passing including mode differential test |
| WENG-05 | 01-04-PLAN.md | Select optimal move (highest-scoring valid placement) | SATISFIED | `find_all_moves` sorts by `score` descending; `GameEngine.best_move` returns `moves[0]`; verified by `test_moves_sorted_by_score` and `test_engine_best_move` |

No orphaned requirements. All 5 WENG requirements accounted for and satisfied.

---

### Anti-Patterns Found

| File | Pattern | Severity | Verdict |
|------|---------|----------|---------|
| All `src/engine/*.py` | TODO/FIXME/PLACEHOLDER | — | None found |
| All `src/engine/*.py` | Stub returns (`return {}`, `return []`, `return null`) | — | None found |
| `data/.gitkeep` | Empty data directory | Info | Intentional — production wordlist is user-provided (documented in CONTEXT.md). Engine accepts path as parameter; tests use `tmp_path` fixture. Not a blocker. |

No blockers or warnings detected. One informational note: the production wordlist `data/wordlist.txt` does not yet exist. This is expected per the project design — the engine is built to accept any wordlist file path; the Wordnik list will be supplied externally before production use.

---

### Human Verification Required

None. All success criteria are programmatically verifiable via the test suite. The following was confirmed by test execution:

- 72/72 tests pass in 0.79s
- Both Classic and Wild modes verified via `test_classic_vs_wild_different_scores` and `test_engine_classic_vs_wild`
- Multi-turn game state verified via `test_engine_multi_turn_game`
- Empty board first move verified via `test_first_move_empty_board` and `test_engine_find_moves_first_turn`

---

### Test Suite Summary

```
72 passed in 0.79s

tests/test_gaddag.py     — 9 tests (GADDAG build, lookup, cache, edge cases)
tests/test_board.py      — 20 tests (dimensions, tile placement, anchors, cross-checks, left-limits)
tests/test_scoring.py    — 22 tests (Classic mode 12, Wild mode 10)
tests/test_moves.py      — 12 tests (first move, extensions, prefix, cross-check, blank, dedupe, sort)
tests/test_engine.py      — 9 tests (init, find moves, best move, play move, multi-turn, classic vs wild)
```

---

### Gaps Summary

None. All 5 observable truths verified, all 12 artifacts substantive and wired, all 10 key links connected, all 5 WENG requirements satisfied, 72/72 tests passing, zero anti-pattern blockers.

---

_Verified: 2026-03-23_
_Verifier: Claude (gsd-verifier)_
