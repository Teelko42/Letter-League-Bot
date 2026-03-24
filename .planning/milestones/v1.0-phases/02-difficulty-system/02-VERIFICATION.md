---
phase: 02-difficulty-system
verified: 2026-03-23T00:00:00Z
status: passed
score: 4/4 must-haves verified
re_verification: false
---

# Phase 2: Difficulty System Verification Report

**Phase Goal:** The engine produces moves calibrated to any target play strength from weakest to optimal
**Verified:** 2026-03-23
**Status:** PASSED
**Re-verification:** No — initial verification

---

## Goal Achievement

### Observable Truths (from ROADMAP Success Criteria)

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Setting difficulty to 100% always returns the highest-scoring valid move | VERIFIED | `test_100pct_returns_best_move` passes: QUIXOTIC (120) returned over CAT (30) and THE (15). `test_integration_with_game_engine` confirms `result_100.score == moves[0].score` against real GameEngine output. Algorithm: at alpha=1.0 blended=norm_score, so highest-scorer always ranks first. |
| 2 | Setting difficulty to 0% returns a measurably weaker move than 100% on the same board | VERIFIED | `test_0pct_weaker_than_100pct` passes: asserts `result_0.score < result_100.score`. `test_integration_difficulty_gradient` confirms with real moves. Algorithm: at alpha=0.0 blended=norm_freq, common words with low raw scores rise to top. |
| 3 | At lower difficulties, the selected word is drawn from more common vocabulary than at 100% | VERIFIED | `test_low_difficulty_prefers_common_words` passes: asserts `freq.zipf(result_0.word) >= freq.zipf(result_100.word)` on a set spanning THE/HOUSE/QUAFF/ZYZZYVA. `test_oov_words_handled` confirms OOV word (Zipf=0.0) is NOT selected at 0% but IS at 100%. |
| 4 | Difficulty setting is configurable as a numeric percentage without code changes | VERIFIED | `test_difficulty_configurable` passes: `select_move(moves, difficulty=d)` called with 25, 50, 75 — all return valid Move instances. API signature `difficulty: int \| float` accepts any numeric value. Clamping test confirms out-of-range values handled without crashes. |

**Score: 4/4 truths verified**

---

### Required Artifacts

| Artifact | Provided By | Min Lines | Actual Lines | Status | Details |
|----------|------------|-----------|--------------|--------|---------|
| `src/difficulty/__init__.py` | Module re-exports | — | 6 | VERIFIED | Exports `DifficultyEngine` and `FrequencyIndex` in `__all__`; both importable cleanly |
| `src/difficulty/frequency.py` | FrequencyIndex class | 30 | 74 | VERIFIED | Substantive: lazy-cache Zipf lookups, `zipf()`, `normalized()`, case normalization, OOV=0.0 handling |
| `src/difficulty/engine.py` | DifficultyEngine class | 60 | 95 | VERIFIED | Substantive: alpha-weighted blended scoring, score normalization, frequency tiebreaker, clamping, deterministic |
| `tests/test_difficulty.py` | Full test coverage | 120 | 483 | VERIFIED | 22 tests across 8 test classes covering all behavioral requirements + integration + edge cases |

All artifacts exceed minimum line thresholds. No stubs, placeholders, or empty implementations found.

---

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `src/difficulty/engine.py` | `src/difficulty/frequency.py` | `FrequencyIndex` instantiation + `normalized()` calls | WIRED | Line 5: `from src.difficulty.frequency import FrequencyIndex`; line 41: `self._freq = FrequencyIndex(lang)`; line 85: `self._freq.normalized(move.word)` — frequency actively used in blended scoring |
| `src/difficulty/engine.py` | `src/engine/models.py` | `Move` dataclass fields `score` and `word` | WIRED | Line 8: `from src.engine.models import Move` (TYPE_CHECKING guard); lines 84-85 access `move.score` and `move.word` at runtime — both consumed in `adjusted_score()` inner function |
| `tests/test_difficulty.py` | `src/difficulty/engine.py` | `DifficultyEngine.select_move()` behavioral verification | WIRED | Line 156-157: `from src.difficulty import DifficultyEngine; return DifficultyEngine()`; `select_move()` called in 15 test methods covering all DIFF requirements |

All three key links are fully wired — no orphaned artifacts, no partial connections.

---

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| DIFF-01 | 02-02-PLAN.md | Configurable difficulty as percentage of optimal play strength (100% = best, lower = weaker) | SATISFIED | `test_100pct_returns_best_move`, `test_0pct_weaker_than_100pct`, `test_difficulty_configurable`, `test_difficulty_clamping` all pass. API accepts 0-100 integer percentage, clamped silently. |
| DIFF-02 | 02-01-PLAN.md, 02-02-PLAN.md | Filter word candidates by vocabulary commonality at lower difficulties | SATISFIED | `test_low_difficulty_prefers_common_words` and `test_oov_words_handled` pass. FrequencyIndex provides Zipf scores (`the`=7.73, `cat`=4.78, OOV=0.0); blended scoring uses `(1-alpha)*norm_freq` to weight common vocabulary at low difficulty. |
| DIFF-03 | 02-02-PLAN.md | Vary play strategy (not just score targeting) based on difficulty setting | SATISFIED | `test_strategy_variation_produces_different_words` passes: across difficulties 0/25/50/75/100 on a 10-move list, at least 3 distinct words are selected. The blended algorithm produces genuinely different rankings, not just score tiers. |

All three DIFF requirements accounted for. No orphaned requirements found in REQUIREMENTS.md for Phase 2.

**Traceability check:** REQUIREMENTS.md maps DIFF-01, DIFF-02, DIFF-03 to Phase 2 with status "Complete" — consistent with what the code delivers.

---

### Anti-Patterns Found

No anti-patterns detected.

Scanned files:
- `src/difficulty/frequency.py` — No TODO/FIXME/placeholder comments; no empty implementations
- `src/difficulty/engine.py` — No TODO/FIXME/placeholder comments; no empty implementations; `return None` is a documented, intentional API contract for empty move list
- `tests/test_difficulty.py` — No stub test bodies; all assertions are substantive

---

### Algorithm Deviation Note

The plan specified a percentile-based index formula (`floor((1-alpha) * (len-1))`). The executor identified a logical inversion: at alpha=0.0 the sort already puts the most common word at index 0, so the percentile formula would select the LEAST common word at low difficulty — opposite the requirement. The fix (always select `ranked[0]`) is correct and simpler. This is verified by the passing tests, which assert the behavioral requirement directly, not the algorithm formula.

---

### Human Verification Required

None. All four success criteria are verifiable programmatically via the test suite, which covers the full behavioral contract including real GameEngine integration.

---

### Full Test Suite Status

22 difficulty tests pass (7 FrequencyIndex + 15 DifficultyEngine including 3 integration).
94 total tests pass (no regressions against Phase 1 word engine tests).
Test run time: 0.56s for difficulty suite, 0.94s for full suite.

---

## Summary

Phase 2 fully achieves its goal. The engine produces moves calibrated to any target play strength from weakest to optimal. All four success criteria from the ROADMAP are satisfied by substantive, wired implementations with comprehensive test coverage. The public API (`DifficultyEngine.select_move(moves, difficulty)`) is ready for consumption by Phase 4 (Discord bot).

---

_Verified: 2026-03-23_
_Verifier: Claude (gsd-verifier)_
