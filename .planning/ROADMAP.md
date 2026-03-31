# Roadmap: Letter League Bot

## Overview

The build order is dictated by a strict dependency chain: the word engine is pure Python and was built and verified in isolation first; difficulty scaling layered on top of the engine before any I/O was introduced; the vision pipeline is the highest-risk v1.1 component and must be validated against real screenshots before connecting downstream; Discord advisor mode wires vision and engine together into the MVP; browser foundation resolves Playwright unknowns as isolated discovery spikes before game logic is written; turn detection is a separate high-uncertainty phase gated on live observation; tile placement requires calibrated coordinates from live measurements; and the autonomous game loop is the final integration layer that closes the end-to-end play cycle. Each phase delivers a coherent, independently verifiable capability before the next begins.

## Milestones

- ✅ **v1.0 Word Engine + Difficulty System** — Phases 1-2 (shipped 2026-03-23)
- ✅ **v1.1 Vision + Discord Integration** — Phases 3-4 (shipped 2026-03-25)
- 📋 **v1.2 Browser Automation + Autonomous Play** — Phases 5-8 (planned)

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

<details>
<summary>✅ v1.1 Vision + Discord Integration (Phases 3-4) — SHIPPED 2026-03-25</summary>

- [x] Phase 3: Vision Pipeline (2/2 plans) — completed 2026-03-24
- [x] Phase 4: Discord Advisor Mode (2/2 plans) — completed 2026-03-25

See: `.planning/milestones/v1.1-ROADMAP.md` for full details.

</details>

### 📋 v1.2 Browser Automation + Autonomous Play (Planned)

**Milestone Goal:** Enable the bot to join Letter League games autonomously via browser automation and play without human input.

- [ ] **Phase 5: Browser Foundation** — Persistent browser session, session health, Discord navigation, and canvas screenshot with vision wire-up
- [x] **Phase 6: Turn Detection** — Visual polling to identify when the bot is the active player (completed 2026-03-26)
- [x] **Phase 7: Tile Placement** — Pixel coordinate calibration and tile/board click mechanics (completed 2026-03-26)
- [ ] **Phase 8: Autonomous Game Loop** — Full end-to-end play loop with slash commands, resilience, and status reporting

## Phase Details

### Phase 5: Browser Foundation
**Goal**: The bot runs a persistent patchright browser session, detects expired Discord logins at startup, navigates to a voice channel, opens the Letter League Activity iframe, and captures a non-blank canvas screenshot that passes through the existing vision pipeline
**Depends on**: Phase 4
**Requirements**: BROW-01, BROW-02, ANAV-01, ANAV-02, ANAV-03
**Success Criteria** (what must be TRUE):
  1. Bot launches Chromium with a saved Discord login and reaches the Discord web client without a re-authentication prompt across restarts
  2. Bot detects a missing or expired session at startup and prints an operator-visible warning instead of proceeding silently
  3. Bot navigates to a target voice channel URL, clicks through to the Letter League Activity, and holds a live reference to the game iframe
  4. A canvas screenshot captured from inside the Activity iframe is non-blank (not solid black/white) and is verified as such by a pixel-variance check
  5. That same screenshot bytes flow through the existing `extract_board_state()` call and return a valid `(Board, rack)` result without modification to any vision code
**Plans**: 2 plans
- [ ] 05-01-PLAN.md — Browser session manager (persistent context, first-run login, expired session detection)
- [ ] 05-02-PLAN.md — Activity navigation and canvas capture (channel nav, iframe discovery, screenshot + vision wire-up)

### Phase 6: Turn Detection
**Goal**: The bot correctly identifies when it is the active player by inspecting the game canvas and does not attempt tile placement out of turn
**Depends on**: Phase 5
**Requirements**: TURN-01
**Success Criteria** (what must be TRUE):
  1. Turn-detection signal is documented from live gameplay observation (at least 2 full games watched, specific UI element or pixel region identified and recorded with DevTools screenshots)
  2. `_is_my_turn(screenshot_bytes)` correctly classifies "my turn" vs "not my turn" for at least 10 recorded game screenshots with zero false positives
  3. The polling loop skips the play pipeline and waits when it is not the bot's turn, confirmed by running a session where the bot observes several opponent turns without acting
**Plans**: 2 plans
- [ ] 06-01-PLAN.md — Turn detection module + calibration tooling (TurnState, classify_frame, poll_turn, preflight_check, calibration script)
- [ ] 06-02-PLAN.md — Live calibration and threshold verification (run calibration during game, update HSV constants, verify accuracy)

### Phase 7: Tile Placement
**Goal**: The bot translates a chosen word move into a sequence of pixel clicks that correctly places tiles on the board and submits the play via the game UI
**Depends on**: Phase 6
**Requirements**: TILE-01, TILE-02, TILE-03
**Success Criteria** (what must be TRUE):
  1. Rack tile pixel coordinates are computed from the live canvas bounding box and fractional offsets calibrated from real game measurements — no hardcoded absolute coordinates
  2. Board cell pixel coordinates are computed the same way, and the coordinate map is recalculated whenever the vision output reports a board dimension change
  3. Clicking a 5-letter word sequence moves the correct tiles from the rack to the correct board cells as confirmed by visual inspection of the game canvas after each click
  4. The play confirmation click dismisses the confirmation UI and the word is accepted by the game (tiles remain on board, score updates)
**Plans**: 2 plans
- [ ] 07-01-PLAN.md — Coordinate mapping and tile drag logic (CoordMapper, TilePlacer.place_tiles, calibration script)
- [ ] 07-02-PLAN.md — Play confirmation, rejection recovery, and retry loop (confirm click, acceptance detection, tile swap fallback)

### Phase 8: Autonomous Game Loop
**Goal**: A `/autoplay start` command launches a self-sustaining turn loop that reads the board, selects a move, places tiles, and posts a status update — all concurrent with discord.py — and can be stopped cleanly with `/autoplay stop`
**Depends on**: Phase 7
**Requirements**: LOOP-01, LOOP-02, LOOP-03, LOOP-04, LOOP-05, BROW-03
**Success Criteria** (what must be TRUE):
  1. `/autoplay start`, `/autoplay stop`, and `/autoplay status` slash commands respond correctly without blocking concurrent Discord commands during a live game session
  2. The game loop runs as an asyncio task sharing discord.py's event loop — no thread blocking, no `RuntimeError: This event loop is already running`
  3. When the Activity disconnects mid-game the bot logs the event, attempts reconnection, and resumes the loop without operator intervention
  4. Bot waits a randomised 1-3 second delay between each action (rack click, board click, confirm click) rather than firing clicks at machine speed
  5. When no valid word moves exist the bot performs a tile swap instead of hanging or erroring
  6. After each successful turn the bot posts a Discord message showing the word played and the points scored
**Plans**: 2 plans
Plans:
- [ ] 08-01-PLAN.md — Autoplay state types and embed builders (LoopState, AutoPlayPhase, turn/swap/gameover embeds)
- [ ] 08-02-PLAN.md — AutoPlayCog with game loop, reconnection, slash commands, and bot.py registration

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Word Engine | v1.0 | 4/4 | Complete | 2026-03-24 |
| 2. Difficulty System | v1.0 | 2/2 | Complete | 2026-03-24 |
| 3. Vision Pipeline | v1.1 | 2/2 | Complete | 2026-03-24 |
| 4. Discord Advisor Mode | v1.1 | 2/2 | Complete | 2026-03-25 |
| 5. Browser Foundation | 1/2 | In Progress|  | - |
| 6. Turn Detection | 1/2 | Complete    | 2026-03-26 | - |
| 7. Tile Placement | 2/2 | Complete   | 2026-03-26 | - |
| 8. Autonomous Game Loop | 1/2 | In Progress|  | - |
