---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Vision + Discord Integration
status: in_progress
last_updated: "2026-03-25T01:49:42Z"
progress:
  total_phases: 1
  completed_phases: 1
  total_plans: 3
  completed_plans: 1
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-24)

**Core value:** Analyze a Letter League board state and find the best possible word placement
**Current focus:** Phase 4 — Discord Advisor Mode (plan 1 of 3 complete)

## Current Position

Phase: 4 of 6 (Discord Advisor Mode)
Plan: 1 of 3 complete
Status: In Progress
Last activity: 2026-03-25 — 04-01 complete (bot skeleton, channel state, formatter, embed builders)

Progress: [███░░░░░░░] 33% (1/3 plans complete in Phase 4)

## Performance Metrics

**Velocity (v1.0):**
- Total plans completed: 6
- Average duration: ~7 min
- Total execution time: ~41 min

**By Phase (v1.0):**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Word Engine | 4 | ~28 min | ~7 min |
| 2. Difficulty System | 2 | ~13 min | ~6.5 min |

*v1.1 metrics will populate as plans complete.*

**v1.1 Phase 3 (Vision Pipeline):**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| 03-01 Vision Foundation | 3 min | 3 | 6 |
| 03-02 Vision Extractor + Validator | 3 min | 3 | 4 |

**v1.1 Phase 4 (Discord Advisor Mode):**

| Plan | Duration | Tasks | Files |
|------|----------|-------|-------|
| 04-01 Bot Skeleton + Formatter | 3 min | 3 | 4 |

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
v1.0 decisions archived — see `.planning/milestones/v1.0-ROADMAP.md`.

Recent decisions affecting v1.1:
- Use `AsyncAnthropic` (not sync) — sync client blocks discord.py event loop
- Use `playwright.async_api` exclusively — sync API raises RuntimeError inside asyncio
- Recommended model: `claude-sonnet-4-6` (~$0.004/screenshot); do not use Haiku 3 (retires 2026-04-19)
- Wrap all engine calls with `asyncio.to_thread()` in Discord handlers — engine is CPU-bound sync code
- Always `await interaction.response.defer()` as first line of `/analyze` handler — vision API takes 4-15s
- [Phase 03-vision-pipeline]: opencv-python, Pillow, numpy installed (were listed in STACK.md but not installed in Python 3.10.4 env)
- [Phase 03-vision-pipeline]: OFFICIAL_MULTIPLIER_LAYOUT HSV calibration deferred — initial estimates hardcoded with TODO comment for empirical calibration against real screenshots
- [Phase 03-vision-pipeline]: claude-sonnet-4-6 with output_config json_schema for structured Vision API output — eliminates JSON parse errors
- [Phase 03-vision-pipeline]: BFS flood-fill for tile connectivity validation — avoids false positives on word endpoint tiles
- [Phase 03-vision-pipeline]: anthropic==0.86.0 and loguru==0.7.3 installed (were in STACK.md but not in Python 3.10.4 env)
- [Phase 04-discord-advisor-mode]: discord.py 2.7.1 and python-dotenv 1.2.2 installed (not previously in Python 3.10.4 env)
- [Phase 04-discord-advisor-mode]: Per-channel settings are in-memory only (reset on restart) — no persistence layer for initial advisor mode
- [Phase 04-discord-advisor-mode]: GADDAG loaded fail-loud in setup_hook via asyncio.to_thread — bot refuses to start without core resource
- [Phase 04-discord-advisor-mode]: Formatter is a pure-function module (no bot/interaction refs) — testable in isolation

### Pending Todos

None.

### Blockers/Concerns

- Vision pipeline accuracy on Letter League's tile font/color scheme is unknown until tested against real screenshots — plan for multiple prompt iterations; gate phase on <2% per-tile error rate across 20+ screenshots
- Discord Activity iframe selectors are undocumented — requires headed Playwright + DevTools inspection before writing navigator code
- Playwright canvas screenshot blank in headless Chromium (issue #19225) — requires time-boxed spike with wait strategy + canvas.toDataURL() fallback before committing to headless deployment
- Turn-detection UI signal and tile coordinate mapping require live in-game observation — highest-risk items in Phase 6

## Session Continuity

Last session: 2026-03-25
Stopped at: Completed 04-01-PLAN.md (bot skeleton, channel state, formatter, embed builders)
Resume file: None
