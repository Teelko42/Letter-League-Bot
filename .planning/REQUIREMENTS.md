# Requirements: Letter League Bot

**Defined:** 2026-03-25
**Core Value:** Analyze a Letter League board state and find the best possible word placement

## v1.2 Requirements

Requirements for milestone v1.2: Browser Automation + Autonomous Play. Each maps to roadmap phases.

### Browser Session

- [x] **BROW-01**: Bot launches persistent Playwright browser session with saved Discord web login that survives restarts
- [x] **BROW-02**: Bot detects expired sessions at startup and notifies the operator instead of silently failing
- [ ] **BROW-03**: Bot reconnects gracefully when the browser session or Activity disconnects mid-game

### Activity Navigation

- [ ] **ANAV-01**: Bot navigates Discord web client to the target voice channel
- [ ] **ANAV-02**: Bot opens the Letter League Activity and locates the game iframe
- [ ] **ANAV-03**: Bot captures a non-blank canvas screenshot from inside the Activity iframe

### Turn Detection

- [x] **TURN-01**: Bot detects when it is the active player via visual state polling and does not act out of turn

### Tile Placement

- [x] **TILE-01**: Bot computes pixel coordinates for board cells and rack tiles from canvas bounding box
- [x] **TILE-02**: Bot clicks rack tiles and board cells to place a chosen word move
- [x] **TILE-03**: Bot confirms word placement via the game's UI confirmation mechanism

### Game Loop

- [ ] **LOOP-01**: Async game loop runs concurrent with discord.py event loop without blocking
- [ ] **LOOP-02**: User can run `/autoplay start`, `/autoplay stop`, and `/autoplay status` slash commands
- [ ] **LOOP-03**: Bot uses human-like timing jitter (random delays between actions)
- [ ] **LOOP-04**: Bot falls back to tile swap when no valid moves exist
- [x] **LOOP-05**: Bot posts Discord status updates showing what word was played and the score

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Advisor Enhancements

- **ADVX-01**: Score breakdown per component shown in response (requires Scorer API change)
- **ADVX-02**: Per-user difficulty persistence across sessions (sqlite)
- **ADVX-03**: Two-shot vision retry on parse failure with error feedback
- **ADVX-04**: Bingo callout for 7-tile plays
- **ADVX-05**: Vision confidence flags per cell for low-confidence reads

### Autonomous Enhancements

- **AUTX-01**: Multi-game / multi-session support (requires multiple Discord accounts)
- **AUTX-02**: Adaptive ML-based turn detection
- **AUTX-03**: Tile swap strategy integration with difficulty engine

## Out of Scope

| Feature | Reason |
|---------|--------|
| OCR fallback (Tesseract) | Claude Vision handles canvas-rendered text natively |
| Headless browser in production | Discord detects headless Chromium; use headed with virtual display |
| Selfbot via discord.py gateway | Discord TOS explicitly bans automated user accounts via gateway; Playwright is the only path |
| Multiple autonomous sessions simultaneously | Each needs own browser context + Discord account; multiplies TOS risk |
| WebSocket game protocol interception | More brittle than vision approach; game protocol is undocumented and may change |
| Automating Discord login programmatically | Fragile and risks account termination; one-time manual login with persistent context instead |
| Bot token joining Activity via API | Activity endpoints require user tokens, not bot tokens; no official API exists |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| BROW-01 | Phase 5 | Complete |
| BROW-02 | Phase 5 | Complete |
| BROW-03 | Phase 8 | Pending |
| ANAV-01 | Phase 5 | Pending |
| ANAV-02 | Phase 5 | Pending |
| ANAV-03 | Phase 5 | Pending |
| TURN-01 | Phase 6 | Complete |
| TILE-01 | Phase 7 | Complete |
| TILE-02 | Phase 7 | Complete |
| TILE-03 | Phase 7 | Complete |
| LOOP-01 | Phase 8 | Pending |
| LOOP-02 | Phase 8 | Pending |
| LOOP-03 | Phase 8 | Pending |
| LOOP-04 | Phase 8 | Pending |
| LOOP-05 | Phase 8 | Complete |

**Coverage:**
- v1.2 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0

---
*Requirements defined: 2026-03-25*
*Last updated: 2026-03-25 after roadmap creation — all 15 requirements mapped*
