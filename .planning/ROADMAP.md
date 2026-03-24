# Roadmap: Letter League Bot

## Overview

The build order is dictated by a strict dependency chain: the word engine is pure Python and can be built and verified in isolation first; difficulty scaling layers on top of the engine before any I/O is introduced; the vision pipeline is the highest-risk component and must be validated against real screenshots before connecting downstream; Discord advisor mode wires all three together into the MVP; browser automation resolves Playwright unknowns as an isolated engineering problem; and autonomous play is the final layer that closes the game loop. Each phase delivers a coherent, independently verifiable capability before the next begins.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Word Engine** - GADDAG dictionary + move generation + Classic/Wild scoring
- [ ] **Phase 2: Difficulty System** - Configurable play strength filtering layered on the move engine
- [ ] **Phase 3: Vision Pipeline** - Board state extraction from screenshots via AI vision
- [ ] **Phase 4: Discord Advisor Mode** - End-to-end MVP: screenshot in, word suggestion out
- [ ] **Phase 5: Browser Automation Foundation** - Playwright infrastructure for Discord Activity interaction
- [ ] **Phase 6: Autonomous Play Mode** - Bot joins game and plays independently

## Phase Details

### Phase 1: Word Engine
**Goal**: The engine can find and rank all valid word placements given any board state and tile rack
**Depends on**: Nothing (first phase)
**Requirements**: WENG-01, WENG-02, WENG-03, WENG-04, WENG-05
**Success Criteria** (what must be TRUE):
  1. Given a board state and tile rack as input, the engine returns all valid word placements with correct positions
  2. Each placement is scored correctly under Classic mode rules (multipliers apply only on placement turn)
  3. Each placement is scored correctly under Wild mode rules (multipliers permanently bonded to letter tiles)
  4. The engine selects the highest-scoring valid placement as the optimal move
  5. The GADDAG structure loads the full Wordnik wordlist and rejects words not in it
**Plans:** 4 plans
  - [x] 01-01-PLAN.md -- Data models + GADDAG dictionary construction and caching
  - [ ] 01-02-PLAN.md -- Board state management, anchor squares, cross-check precomputation
  - [ ] 01-03-PLAN.md -- Classic and Wild mode scoring engine
  - [ ] 01-04-PLAN.md -- Move generation (LeftPart/ExtendRight) + GameEngine public API

### Phase 2: Difficulty System
**Goal**: The engine produces moves calibrated to any target play strength from weakest to optimal
**Depends on**: Phase 1
**Requirements**: DIFF-01, DIFF-02, DIFF-03
**Success Criteria** (what must be TRUE):
  1. Setting difficulty to 100% always returns the highest-scoring valid move
  2. Setting difficulty to 0% returns a measurably weaker move than 100% on the same board
  3. At lower difficulties, the selected word is drawn from more common vocabulary than at 100%
  4. Difficulty setting is configurable as a numeric percentage without code changes
**Plans**: TBD

### Phase 3: Vision Pipeline
**Goal**: The bot can reliably extract a complete, validated board state from a Letter League screenshot
**Depends on**: Phase 1
**Requirements**: VISN-01, VISN-02, VISN-03, VISN-04
**Success Criteria** (what must be TRUE):
  1. Given a real Letter League screenshot, the pipeline returns a structured board state with all placed tiles at correct positions
  2. The tile rack contents are correctly identified from the screenshot
  3. All multiplier square types (double letter, triple letter, double word, triple word) are identified at their correct grid positions
  4. The pipeline reports a confidence score and rejects or flags output that falls below a validation threshold
**Plans**: TBD

### Phase 4: Discord Advisor Mode
**Goal**: A user can send a screenshot to the bot and receive an actionable word suggestion
**Depends on**: Phase 2, Phase 3
**Requirements**: DISC-01, DISC-02, DISC-03, DISC-04
**Success Criteria** (what must be TRUE):
  1. User can invoke a slash command, attach a screenshot, and receive a word suggestion with placement location and expected score
  2. The bot responds without timing out, even when vision and engine processing takes several seconds
  3. The bot tracks game state across multiple turns in a session so the user does not need to re-specify settings each turn
  4. Clear error messages are returned when the screenshot cannot be parsed or no valid moves exist
**Plans**: TBD

### Phase 5: Browser Automation Foundation
**Goal**: The bot can launch a persistent browser, navigate to Discord, and capture the Letter League game canvas
**Depends on**: Phase 4
**Requirements**: AUTO-01
**Success Criteria** (what must be TRUE):
  1. The bot launches a Playwright Chromium browser and navigates to Discord without crashing the event loop
  2. The bot accesses the Letter League Activity iframe and captures a non-blank screenshot of the game canvas
  3. The browser session persists across turns without re-authenticating
**Plans**: TBD

### Phase 6: Autonomous Play Mode
**Goal**: The bot joins a Letter League game, detects its turn, and places tiles on the board without human input
**Depends on**: Phase 5
**Requirements**: AUTO-02, AUTO-03
**Success Criteria** (what must be TRUE):
  1. The bot correctly detects when it is the active player and does not act out of turn
  2. The bot successfully clicks tile rack slots and board positions to place a chosen word
  3. The bot completes a full turn — detecting turn start, reading board, selecting move, placing tiles — without manual intervention
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Word Engine | 1/4 | In progress | - |
| 2. Difficulty System | 0/? | Not started | - |
| 3. Vision Pipeline | 0/? | Not started | - |
| 4. Discord Advisor Mode | 0/? | Not started | - |
| 5. Browser Automation Foundation | 0/? | Not started | - |
| 6. Autonomous Play Mode | 0/? | Not started | - |
