# Requirements: Letter League Bot

**Defined:** 2026-03-23
**Core Value:** Analyze a Letter League board state and find the best possible word placement

## v1 Requirements

Requirements for initial release. Each maps to roadmap phases.

### Word Engine

- [x] **WENG-01**: Build GADDAG data structure from Wordnik wordlist for fast word lookup
- [ ] **WENG-02**: Generate all valid word placements given board state and tile rack
- [x] **WENG-03**: Score words using Classic mode rules (letter values + multiplier squares, bonuses apply only on placement turn)
- [x] **WENG-04**: Score words using Wild mode rules (multipliers permanently assigned to letters)
- [ ] **WENG-05**: Select optimal move (highest-scoring valid placement)

### Board Vision

- [ ] **VISN-01**: Parse Letter League board state from screenshot using AI vision
- [ ] **VISN-02**: Detect tile rack contents from screenshot
- [ ] **VISN-03**: Identify multiplier square types and positions on the board
- [ ] **VISN-04**: Report confidence score for board state extraction accuracy

### Difficulty

- [ ] **DIFF-01**: Configurable difficulty as percentage of optimal play strength (100% = best, lower = weaker)
- [ ] **DIFF-02**: Filter word candidates by vocabulary commonality at lower difficulties
- [ ] **DIFF-03**: Vary play strategy (not just score targeting) based on difficulty setting

### Discord Integration

- [ ] **DISC-01**: Register slash commands for bot interaction
- [ ] **DISC-02**: Accept screenshot image attachments of the game board
- [ ] **DISC-03**: Return word suggestion with placement location and expected score
- [ ] **DISC-04**: Track game session state across multiple turns

### Autonomous Play

- [ ] **AUTO-01**: Control browser via Playwright to interact with Letter League Activity
- [ ] **AUTO-02**: Detect when it's the bot's turn in the game
- [ ] **AUTO-03**: Automatically place tiles on the board to play chosen word

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Enhanced Features

- **ENHC-01**: Move explanations (why this word is the best choice)
- **ENHC-02**: Bingo detection and bonus scoring (using all tiles in rack)
- **ENHC-03**: Turn timing variation in autonomous mode (appear more human)
- **ENHC-04**: Auto-detect game start and end in autonomous mode
- **ENHC-05**: Multi-game support (handle multiple concurrent games)

## Out of Scope

| Feature | Reason |
|---------|--------|
| Mobile app or standalone GUI | Discord bot only — no separate UI |
| Voice chat interaction | Text-based commands only |
| Other word games | Letter League specific |
| Multiplayer coordination | Bot plays as a single player |
| Real-time game streaming | Not needed for advisor or auto-play |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| WENG-01 | Phase 1 | Complete (01-01) |
| WENG-02 | Phase 1 | Pending |
| WENG-03 | Phase 1 | Complete (01-03) |
| WENG-04 | Phase 1 | Complete (01-03) |
| WENG-05 | Phase 1 | Pending |
| VISN-01 | Phase 3 | Pending |
| VISN-02 | Phase 3 | Pending |
| VISN-03 | Phase 3 | Pending |
| VISN-04 | Phase 3 | Pending |
| DIFF-01 | Phase 2 | Pending |
| DIFF-02 | Phase 2 | Pending |
| DIFF-03 | Phase 2 | Pending |
| DISC-01 | Phase 4 | Pending |
| DISC-02 | Phase 4 | Pending |
| DISC-03 | Phase 4 | Pending |
| DISC-04 | Phase 4 | Pending |
| AUTO-01 | Phase 5 | Pending |
| AUTO-02 | Phase 6 | Pending |
| AUTO-03 | Phase 6 | Pending |

**Coverage:**
- v1 requirements: 19 total
- Mapped to phases: 19
- Unmapped: 0

---
*Requirements defined: 2026-03-23*
*Last updated: 2026-03-24 — WENG-03, WENG-04 complete (01-03-PLAN.md)*
