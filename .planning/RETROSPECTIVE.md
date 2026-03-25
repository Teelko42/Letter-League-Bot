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

## Milestone: v1.1 — Vision + Discord Integration

**Shipped:** 2026-03-25
**Phases:** 2 | **Plans:** 4 | **Sessions:** ~2

### What Was Built
- Vision pipeline: OpenCV HSV board detection + Pillow 2x LANCZOS upscale + Claude Vision API with structured JSON schema output
- Four-check validator: A-Z letter check, BFS flood-fill connectivity, multiplier position matching, rack validation
- discord.py bot skeleton with per-channel state, color-coded embeds, text-art board renderer
- AdvisorCog: /analyze (full vision+engine pipeline), /setdifficulty (0-100%), /setmode (Classic/Wild)
- End-to-end flow human-verified in a live Discord guild

### What Worked
- Structured output (`output_config json_schema`) eliminated all JSON parse errors from Vision API — no need for retry on parse failures
- Defer-first pattern prevented Discord interaction timeouts during 4-15s vision+engine processing
- Pure-function formatter module with no bot/interaction references — fully testable in isolation
- asyncio.to_thread wrapper for CPU-bound engine calls — clean async/sync boundary
- Scope adjustment (shipping Phases 3-4 as v1.1, deferring 5-6) was pragmatic — advisor mode is usable standalone

### What Was Inefficient
- Dependencies (opencv-python, anthropic, discord.py, etc.) were listed in STACK.md but not installed — every plan needed a Rule 3 auto-fix for missing packages
- HSV calibration values were initially guesses — required real-screenshot calibration pass after implementation
- Phase 3 progress table had a formatting bug (missing v1.1 milestone column for row 3)

### Patterns Established
- AsyncAnthropic client at module level (not per-call) to avoid connection overhead
- defer-first: await interaction.response.defer(ephemeral=True) as absolute first line of long-running slash commands
- Local import in setup_hook to avoid circular dependencies at module load time
- DISCORD_TEST_GUILD_ID env var for instant command sync during development
- Color-coded Discord embeds: green=success, gold=warning, red=error, blurple=info

### Key Lessons
1. Install dependencies during project setup, not during plan execution — every plan hitting "not installed" wastes a Rule 3 deviation
2. Structured output (json_schema) is strictly better than free-text JSON for vision extraction — eliminates an entire error class
3. BFS flood-fill is the correct connectivity algorithm for word games — per-tile neighbor checks give false positives on word endpoints
4. Scope adjustment at milestone completion is healthy — shipping a usable product beats waiting for all planned features

### Cost Observations
- Model mix: balanced profile (opus for planning, sonnet for execution agents)
- Sessions: ~2
- Notable: 4 plans completed in ~14 minutes total — faster than v1.0 due to smaller plan scope and established patterns

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | ~2 | 2 | Initial baseline — TDD, strict phase ordering |
| v1.1 | ~2 | 2 | Vision + Discord integration, scope adjustment at completion |

### Cumulative Quality

| Milestone | Tests | Coverage | Zero-Dep Additions |
|-----------|-------|----------|-------------------|
| v1.0 | 94 | — | 6 plans |
| v1.1 | 107 | — | 4 plans |

### Top Lessons (Verified Across Milestones)

1. Pure function design enables isolated, fast testing (v1.0 formatter, v1.1 embeds — verified)
2. Install all dependencies at project init, not during plan execution (v1.0 had zero issues, v1.1 hit it on every plan)
3. Strict phase ordering with clean interfaces eliminates rework (verified across both milestones)
