# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-23)

**Core value:** Analyze a Letter League board state and find the best possible word placement
**Current focus:** Phase 1 - Word Engine

## Current Position

Phase: 1 of 6 (Word Engine)
Plan: 3 of 4 in current phase
Status: In progress
Last activity: 2026-03-24 — 01-03 (scoring engine, Classic + Wild modes) complete

Progress: [██░░░░░░░░] 12% (3/24 plans)

## Performance Metrics

**Velocity:**
- Total plans completed: 3
- Average duration: ~5 min
- Total execution time: 0.22 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 01-word-engine | 3/4 | ~15 min | ~5 min |

**Recent Trend:**
- Last 5 plans: 01-01 (~2 min), 01-02 (~5 min), 01-03 (~8 min)
- Trend: Plans growing with complexity as expected

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- [Init]: Python 3.11 + discord.py 2.7.1 — ecosystem sweet spot, full async slash command support
- [Init]: Custom GADDAG over DAWG — 2x faster move generation; required for 170k+ Wordnik wordlist
- [Init]: Claude Vision API for board reading — outperforms Tesseract/EasyOCR on styled game screenshots
- [Init]: Playwright async API exclusively — sync API raises RuntimeError inside discord.py's event loop
- [Init]: Advisor mode before autonomous — zero TOS risk; validates core engine before adding automation
- [01-01]: Dict-based GADDAG (not class-per-node) — lower memory overhead, O(1) dict lookups in CPython
- [01-01]: MD5 hash of wordlist bytes for cache invalidation — reliable, no mtime race conditions
- [01-01]: GADDAG.from_wordlist() factory pattern — clean public API, callers never touch build/cache primitives directly
- [01-01]: SEPARATOR='+', TERMINAL='$' — standard Python GADDAG convention, non-alpha so can't collide with wordlist words
- [01-02]: Anchors are direction-independent — same set for H and V; direction parameter exists for API consistency with cross-checks and left-limits
- [01-02]: Cross-checks are direction-dependent — H validates vertical perpendicular words (gather up/down), V validates horizontal (gather left/right)
- [01-02]: left_limit returns 0 on adjacent occupied cell — existing tile chain is a forced prefix, handled separately in move generation
- [01-02]: TYPE_CHECKING guard for GADDAG import in board.py — avoids circular import while preserving type annotations
- [01-03]: score_word/score_move accept cells+positions as params, not Board — keeps scoring pure and testable
- [01-03]: Wild uses bonded_multiplier; Classic uses square_multiplier filtered by newly_placed_positions
- [01-03]: Wild stacking is multiplicative (DW+DW=x4, TW+DW=x6) per research recommendation
- [01-03]: Bingo fires on tiles_from_rack==rack_size; doubles main word only (not perp words, not +50)

### Pending Todos

None yet.

### Blockers/Concerns

- [Phase 3]: Vision pipeline accuracy on Letter League's tile font/color scheme is unknown until tested against real screenshots — plan for iteration
- [Phase 5]: Playwright canvas screenshot bug (#19225) in headless mode requires a time-boxed spike before committing to automation architecture
- [Phase 6]: Turn-detection UI signal and tile placement coordinate mapping require live game testing — highest-risk phase

## Session Continuity

Last session: 2026-03-24
Stopped at: Completed 01-03-PLAN.md (scoring engine, Classic + Wild modes)
Resume file: None
