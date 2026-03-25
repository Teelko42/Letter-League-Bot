# Roadmap: Letter League Bot

## Overview

The build order is dictated by a strict dependency chain: the word engine is pure Python and was built and verified in isolation first; difficulty scaling layered on top of the engine before any I/O was introduced; the vision pipeline is the highest-risk v1.1 component and must be validated against real screenshots before connecting downstream; Discord advisor mode wires vision and engine together into the MVP; browser automation resolves Playwright unknowns as an isolated engineering spike; and autonomous play is the final layer that closes the game loop. Each phase delivers a coherent, independently verifiable capability before the next begins.

## Milestones

- ✅ **v1.0 Word Engine + Difficulty System** — Phases 1-2 (shipped 2026-03-23)
- 🚧 **v1.1 Vision + Discord Integration** — Phases 3-6 (in progress)

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

<details>
<summary>✅ v1.0 Word Engine + Difficulty System (Phases 1-2) — SHIPPED 2026-03-23</summary>

- [x] Phase 1: Word Engine (4/4 plans) — completed 2026-03-24
- [x] Phase 2: Difficulty System (2/2 plans) — completed 2026-03-24

See: `.planning/milestones/v1.0-ROADMAP.md` for full details.

</details>

### 🚧 v1.1 Vision + Discord Integration (In Progress)

**Milestone Goal:** Enable the bot to read Letter League board state from screenshots and play the game — either advising a user or playing autonomously via browser automation.

- [x] **Phase 3: Vision Pipeline** — Board state extraction from screenshots via Claude Vision API (completed 2026-03-24)
- [x] **Phase 4: Discord Advisor Mode** — End-to-end MVP: screenshot in, word suggestion out (completed 2026-03-25)
- [ ] **Phase 5: Browser Automation Foundation** — Playwright infrastructure for Discord Activity interaction
- [ ] **Phase 6: Autonomous Play** — Bot joins game, detects turn, and places tiles independently

## Phase Details

### Phase 3: Vision Pipeline
**Goal**: The bot can reliably extract a complete, validated board state from a Letter League screenshot
**Depends on**: Phase 1
**Requirements**: VISN-01, VISN-02, VISN-03, VISN-04, VISN-05
**Success Criteria** (what must be TRUE):
  1. A real Letter League screenshot yields a structured board state with all placed tiles identified at their correct grid positions
  2. The tile rack contents are correctly extracted from the screenshot alongside the board in a single API call
  3. All multiplier square types (DL, TL, DW, TW) are detected and mapped to their correct grid coordinates
  4. Screenshots are cropped to the board region and upscaled before API submission, and the resulting board state passes engine validation before being handed off to the word engine
**Plans**: 2 plans
- [ ] 03-01-PLAN.md — Schema, errors, multiplier layout, and image preprocessor
- [ ] 03-02-PLAN.md — Vision extractor, validator, and pipeline entry point

### Phase 4: Discord Advisor Mode
**Goal**: A user can submit a screenshot to the Discord bot and receive actionable word recommendations as an ephemeral message
**Depends on**: Phase 2, Phase 3
**Requirements**: DISC-01, DISC-02, DISC-03, DISC-04, DISC-05, DISC-06
**Success Criteria** (what must be TRUE):
  1. Bot connects to the Discord gateway and all slash commands register and respond correctly in a guild
  2. User attaches a screenshot to `/analyze` and receives the top-3 move recommendations — word, position, direction, score — as an ephemeral message, without the interaction timing out
  3. User runs `/setdifficulty` to configure play strength (0-100%) and specifies Classic or Wild scoring mode; bot applies both for all subsequent analysis in the session
  4. Bot returns a clear, actionable error message when given a bad screenshot, when the vision API fails, or when no valid moves exist
**Plans**: 2 plans
- [x] 04-01-PLAN.md — Bot foundation, channel state, and formatter (Wave 1)
- [x] 04-02-PLAN.md — Cog slash commands, pipeline wiring, and integration checkpoint (Wave 2)

### Phase 5: Browser Automation Foundation
**Goal**: The bot can launch a persistent browser session, navigate Discord's web client, and capture a non-blank game canvas from inside the Letter League Activity iframe
**Depends on**: Phase 4
**Requirements**: AUTO-01, AUTO-02, AUTO-03
**Success Criteria** (what must be TRUE):
  1. Playwright launches a persistent Chromium session using saved Discord web login credentials without triggering re-authentication
  2. Bot navigates to a voice channel and opens the Letter League Activity, reaching the game iframe without manual intervention
  3. A non-blank screenshot of the game canvas is captured from inside the Activity iframe and is usable as input to the vision pipeline
**Plans**: TBD

### Phase 6: Autonomous Play
**Goal**: The bot detects its turn, selects the best word via the engine, places tiles on the board, and confirms the play — completing a full turn without human input
**Depends on**: Phase 5
**Requirements**: AUTO-04, AUTO-05, AUTO-06
**Success Criteria** (what must be TRUE):
  1. Bot correctly detects when it is the active player via visual state change and does not act out of turn
  2. Bot clicks rack tiles and board cells at the correct canvas-relative pixel coordinates to place a chosen word
  3. Bot completes word submission via the game's UI confirmation mechanism, completing a full autonomous turn from turn-detection through placement confirmation
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Word Engine | v1.0 | 4/4 | Complete | 2026-03-24 |
| 2. Difficulty System | v1.0 | 2/2 | Complete | 2026-03-24 |
| 3. Vision Pipeline | 2/2 | Complete   | 2026-03-24 | - |
| 4. Discord Advisor Mode | v1.1 | 2/2 | Complete | 2026-03-25 |
| 5. Browser Automation Foundation | v1.1 | 0/? | Not started | - |
| 6. Autonomous Play | v1.1 | 0/? | Not started | - |
