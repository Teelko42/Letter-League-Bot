---
phase: 02-difficulty-system
plan: 01
subsystem: difficulty
tags: [wordfreq, zipf, frequency, word-commonality, difficulty-engine]

# Dependency graph
requires:
  - phase: 01-word-engine
    provides: GameEngine.find_all_moves() producing candidate move list for difficulty scoring
provides:
  - FrequencyIndex class with O(1) amortized Zipf and normalized frequency lookups via wordfreq
  - src/difficulty/ module package with clean re-exports
  - 7 unit tests covering common, uncommon, OOV, case-insensitive, normalized, and consistency scenarios
affects:
  - 02-02-difficulty-engine (consumes FrequencyIndex for blended difficulty scoring)
  - any future phase needing word commonality data

# Tech tracking
tech-stack:
  added: [wordfreq==3.1.1]
  patterns: [lazy-cache over external library lookup, fixed-constant normalization, case-lowering at API boundary]

key-files:
  created:
    - src/difficulty/__init__.py
    - src/difficulty/frequency.py
    - tests/test_difficulty.py
  modified: []

key-decisions:
  - "zipf_frequency() with lazy dict cache over pre-built Zipf dict — avoids ~321k entry startup cost while maintaining O(1) amortized lookups"
  - "get_frequency_dict() returns raw frequencies (not Zipf) — confirmed via probe; zipf_frequency() used for correct scale"
  - "OOV words return 0.0 and are not excluded — consistent with user decision in CONTEXT.md; maximally obscure but still playable"
  - "MAX_ZIPF=8.0 fixed constant for normalization — prevents rare words from inflating to 1.0 when common words absent"
  - "Test OOV examples corrected: xu (3.33) and qat (1.86) are in wordfreq; zyzzyva and qoph are true OOV"

patterns-established:
  - "Difficulty module at src/difficulty/ — parallel to src/engine/; clean separation of concerns"
  - "Case normalization at API boundary: word.lower() in zipf() — callers never need to think about case"
  - "Module-scoped pytest fixture for expensive external-library objects (scope='module' on FrequencyIndex)"

requirements-completed: [DIFF-02]

# Metrics
duration: 2min
completed: 2026-03-24
---

# Phase 2 Plan 01: Word Frequency Index Summary

**wordfreq 3.1.1 integration via lazy-cached zipf_frequency() lookups, giving O(1) amortized Zipf scores (0.0-8.0) and normalized [0.0, 1.0] values with OOV words returning 0.0**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-24T03:55:40Z
- **Completed:** 2026-03-24T03:58:00Z
- **Tasks:** 1 (TDD: RED + GREEN commits)
- **Files modified:** 3

## Accomplishments

- Installed wordfreq 3.1.1 and probed API to confirm `get_frequency_dict` returns raw frequencies (not Zipf), selecting `zipf_frequency()` with lazy caching as the correct implementation approach
- FrequencyIndex class provides case-insensitive Zipf lookups (`the` returns 7.73, `cat` 4.78, OOV words 0.0) and `normalized()` mapping to [0.0, 1.0]
- 7 unit tests written and passing; all 72 Phase 1 tests unaffected

## Task Commits

Each task was committed atomically (TDD two-commit pattern):

1. **RED: Failing tests** - `9d75713` (test)
2. **GREEN: FrequencyIndex implementation** - `9aa7792` (feat)

_Note: TDD plan — RED commit contains failing tests, GREEN commit adds implementation and test data fix._

## Files Created/Modified

- `src/difficulty/__init__.py` - Module re-exports FrequencyIndex for clean `from src.difficulty import FrequencyIndex` imports
- `src/difficulty/frequency.py` - FrequencyIndex class wrapping wordfreq zipf_frequency() with lazy dict cache, case-insensitive lookup, and [0.0, 1.0] normalization
- `tests/test_difficulty.py` - 7 frequency tests: common words (Zipf > 4.0), uncommon words (positive but lower), OOV (0.0), case-insensitive, normalized range, normalized OOV=0.0, repeated instantiation consistency

## Decisions Made

- **wordfreq API approach:** `get_frequency_dict` returns raw probabilities (e.g. 'the' = 0.054), not Zipf. Used `zipf_frequency(word, 'en')` with lazy caching instead of pre-building a 321k-entry dict at init time. Instantiation is now near-instant; first-access cost is amortized.
- **OOV test words corrected:** Plan suggested `xu`, `xu`, `qat` as OOV examples. API probe showed `xu`=3.33, `qat`=1.86 (both in corpus). Replaced with `zyzzyva`=0.0 and `qoph`=0.0 as verified true OOV words.
- **Fixed MAX_ZIPF=8.0:** Normalization uses a fixed upper bound matching the Zipf scale maximum, not the max of any word set. This preserves the absolute meaning of "common" vs "rare".

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Corrected OOV test examples**
- **Found during:** Task 1 GREEN phase (test run failure)
- **Issue:** Plan listed 'xu' and 'qat' as OOV words; wordfreq knows both (xu=3.33, qat=1.86). Test failed with `AssertionError: Expected OOV word 'xu' to return 0.0, got 3.33`
- **Fix:** Replaced 'xu' and 'qat' with 'zyzzyva' (0.0) and 'qoph' (0.0), confirmed truly absent from wordfreq corpus via API probe. Added clarifying comment in test.
- **Files modified:** tests/test_difficulty.py
- **Verification:** All 7 tests pass after correction
- **Committed in:** 9aa7792 (part of GREEN implementation commit)

---

**Total deviations:** 1 auto-fixed (Rule 1 — incorrect test data, not implementation bug)
**Impact on plan:** Fix necessary for test validity. Plan intent (OOV words return 0.0) is fully implemented and tested correctly. No scope creep.

## Issues Encountered

- Python `pip` command not found in bash environment; used full path to `/c/Users/Ninja/AppData/Local/Programs/Python/Python310/python.exe -m pip` to install wordfreq and run tests. All subsequent commands used full Python path.

## User Setup Required

None - wordfreq is installed as a package dependency; no external service configuration required.

## Next Phase Readiness

- FrequencyIndex is ready for consumption by DifficultyEngine (plan 02-02)
- `from src.difficulty import FrequencyIndex` import works correctly
- Zipf scale confirmed: 'the'=7.73, 'cat'=4.78, 'quasar'~2.9, OOV=0.0
- Normalized scale confirmed: 'the'=0.97, OOV=0.0, all values in [0.0, 1.0]

## Self-Check: PASSED

- src/difficulty/__init__.py — FOUND
- src/difficulty/frequency.py — FOUND
- tests/test_difficulty.py — FOUND
- .planning/phases/02-difficulty-system/02-01-SUMMARY.md — FOUND
- Commit 9d75713 (RED: failing tests) — FOUND
- Commit 9aa7792 (GREEN: implementation) — FOUND

---
*Phase: 02-difficulty-system*
*Completed: 2026-03-24*
