# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-25)

**Core value:** Analyze a Letter League board state and find the best possible word placement
**Current focus:** Phase 5 — Browser Foundation (v1.2 ready to plan)

## Current Position

Phase: 5 of 8 (Browser Foundation)
Plan: — of — (not yet planned)
Status: Ready to plan
Last activity: 2026-03-25 — v1.2 roadmap created (phases 5-8 defined)

Progress: [████░░░░░░] 40% (phases 1-4 complete; phases 5-8 not started)

## Performance Metrics

**Velocity (v1.0):**
- Total plans completed: 6
- Average duration: ~7 min
- Total execution time: ~41 min

**Velocity (v1.1):**
- Total plans completed: 4
- Average duration: ~3.5 min
- Total execution time: ~14 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Word Engine | 4 | ~28 min | ~7 min |
| 2. Difficulty System | 2 | ~13 min | ~6.5 min |
| 3. Vision Pipeline | 2 | ~6 min | ~3 min |
| 4. Discord Advisor Mode | 2 | ~8 min | ~4 min |

**Recent Trend:**
- Last 4 plans: ~3 min, ~3 min, ~4 min, ~4 min
- Trend: Stable

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
v1.0 decisions archived — see `.planning/milestones/v1.0-ROADMAP.md`.
v1.1 decisions archived — see `.planning/milestones/v1.1-ROADMAP.md`.

v1.2 decisions so far:
- Use `patchright 1.58.2` (drop-in Playwright fork) — patches CDP fingerprint leaks Discord uses for bot detection
- Single asyncio event loop shared by discord.py and patchright — never use sync Playwright API
- All new code in `src/browser/`; vision/engine/difficulty untouched
- Dedicated throwaway Discord account for Playwright session (separate from bot token)

### Pending Todos

None.

### Blockers/Concerns

- Phase 5: Discord Activity iframe selector is undocumented — confirm via live DevTools inspection before writing navigator code (expected pattern: `[src*="discordsays.com"]`)
- Phase 5: Canvas screenshot may be blank in headed+Xvfb mode (Playwright issue #19225) — spike must test `canvas.screenshot()` and `canvas.toDataURL()` fallback
- Phase 6: Turn-detection visual signal unknown until live gameplay observed — time-box observation spike at 4 hours; commit to screenshot-diff fallback if no reliable signal found
- Phase 7: Tile placement fractional constants in ARCHITECTURE.md are placeholders — must be measured from live game screenshots; budget for iteration

## Session Continuity

Last session: 2026-03-25
Stopped at: Roadmap created — phases 5-8 defined, ready to plan Phase 5
Resume file: None
