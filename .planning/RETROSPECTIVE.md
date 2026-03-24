# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.0 — Word Engine + Difficulty System

**Shipped:** 2026-03-23
**Phases:** 2 | **Plans:** 6 | **Sessions:** ~2

### What Was Built
- GADDAG dictionary with O(word_length) lookup, pickle caching with MD5 invalidation
- Board state management (19x27 configurable grid, multiplier layout, anchors, cross-checks)
- Classic and Wild mode scoring engine with bingo bonus and perpendicular word scoring
- Gordon (1994) LeftPart/ExtendRight move generation with GADDAG-arc blank tile pruning
- GameEngine stateful public API wrapping the complete word engine pipeline
- DifficultyEngine with blended alpha-weighted score/frequency selection (0-100%)

### What Worked
- TDD two-commit pattern (RED then GREEN) enforced clean interfaces and caught bugs early
- Strict phase dependency ordering — Phase 2 consumed Phase 1 APIs with zero rework
- Gordon (1994) algorithm reference provided clear implementation blueprint
- Dict-based GADDAG node representation was simpler and faster than class-per-node alternatives
- Audit workflow caught zero critical gaps — clean execution throughout

### What Was Inefficient
- Phase 2 plan checkboxes in ROADMAP.md not marked `[x]` despite plans being complete (cosmetic but confusing)
- 02-02 percentile index algorithm was inverted in the plan — had to correct during implementation
- Total session count wasn't tracked precisely — consider tracking in STATE.md

### Patterns Established
- TDD two-commit pattern: `test(XX-YY): add failing tests (RED)` then `feat(XX-YY): implement (GREEN)`
- TYPE_CHECKING guard pattern for avoiding circular imports while preserving type annotations
- Pure functions for scoring (no Board dependency) — enables isolated testing
- GameEngine as stateful facade over pure subsystems

### Key Lessons
1. Plan algorithms carefully — the percentile index inversion in 02-02 would have been caught by a plan review step
2. Dict-based data structures in CPython are fast enough — don't over-engineer with custom node classes
3. Pickle cache + MD5 invalidation is a reliable pattern for expensive build artifacts

### Cost Observations
- Model mix: balanced profile (opus for planning, sonnet/haiku for execution)
- Sessions: ~2
- Notable: 6 plans completed in ~41 minutes total — fast execution due to well-defined phase boundaries

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | ~2 | 2 | Initial baseline — TDD, strict phase ordering |

### Cumulative Quality

| Milestone | Tests | Coverage | Zero-Dep Additions |
|-----------|-------|----------|-------------------|
| v1.0 | 94 | — | 6 plans |

### Top Lessons (Verified Across Milestones)

1. TDD two-commit pattern catches interface issues early (v1.0 — to be verified in future milestones)
2. Pure function design enables isolated, fast testing (v1.0 — to be verified)
