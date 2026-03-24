# Requirements: Letter League Bot

**Defined:** 2026-03-24
**Core Value:** Analyze a Letter League board state and find the best possible word placement

## v1.1 Requirements

Requirements for milestone v1.1: Vision + Discord Integration. Each maps to roadmap phases.

### Vision Pipeline

- [ ] **VISN-01**: User can submit a Letter League screenshot and receive a structured board state extraction (grid cells, letters, positions)
- [ ] **VISN-02**: User's tile rack is extracted from the screenshot alongside the board
- [ ] **VISN-03**: Multiplier squares (DL/TL/DW/TW) are detected and mapped to board positions
- [ ] **VISN-04**: Screenshots are cropped to the board region and upscaled before API processing for accuracy
- [ ] **VISN-05**: Extracted board state is validated against engine constraints before being passed to the word engine

### Discord Bot

- [ ] **DISC-01**: Discord bot connects to gateway with proper token auth and privileged intents
- [ ] **DISC-02**: User can run `/analyze` slash command with a screenshot attachment to receive move suggestions
- [ ] **DISC-03**: Bot responds with top-3 move recommendations (word, position, direction, score) as an ephemeral message
- [ ] **DISC-04**: User can run `/setdifficulty` to configure bot play strength (0-100%)
- [ ] **DISC-05**: User can specify Classic or Wild scoring mode as a parameter
- [ ] **DISC-06**: Bot returns actionable error messages for bad screenshots, API failures, or zero valid moves

### Browser Automation

- [ ] **AUTO-01**: Playwright launches persistent Chromium session with saved Discord web login
- [ ] **AUTO-02**: Bot navigates Discord web client to join a voice channel and open the Letter League Activity
- [ ] **AUTO-03**: Bot captures non-blank canvas screenshots from within the Activity iframe
- [ ] **AUTO-04**: Bot detects when it is its turn via visual state changes
- [ ] **AUTO-05**: Bot places word moves by clicking rack tiles and board cells at computed pixel coordinates
- [ ] **AUTO-06**: Bot confirms word placement via the game's UI confirmation mechanism

## v2 Requirements

Deferred to future release. Tracked but not in current roadmap.

### Advisor Enhancements

- **ADVX-01**: Score breakdown per component shown in response (requires Scorer API change)
- **ADVX-02**: Per-user difficulty persistence across sessions (sqlite)
- **ADVX-03**: Two-shot vision retry on parse failure with error feedback
- **ADVX-04**: Bingo callout for 7-tile plays
- **ADVX-05**: Vision confidence flags per cell for low-confidence reads

### Autonomous Enhancements

- **AUTX-01**: Graceful disconnect and re-join on connection drop
- **AUTX-02**: Tile swap detection (swap vs. pass when no good move exists)
- **AUTX-03**: Human-like timing jitter between actions

## Out of Scope

| Feature | Reason |
|---------|--------|
| OCR fallback (Tesseract) | Claude Vision handles canvas-rendered text natively; OCR needs training data for Letter League's font |
| Real-time continuous screen polling in advisor mode | That IS autonomous mode; advisor stays per-screenshot |
| Vision result caching per screenshot hash | Screenshots change every turn; near-zero cache hits for added complexity |
| Prefix commands (!analyze) | Discord deprecated prefix commands; slash commands have native attachment UI |
| Embed board visualization | 27x19 grid rendering is a product in itself; user can see the board |
| Multi-server configuration dashboard | Web dashboard for config is massive complexity; slash commands cover 100% of config |
| Global leaderboard | Ranks bot usage, not skill; adds database for zero gameplay value |
| Multiple autonomous sessions simultaneously | Each needs own browser context + Discord account; multiplies TOS risk |
| Headless browser in production | Discord detects headless Chromium; use headed with virtual display |
| Selenium instead of Playwright | Playwright has superior async, iframe, screenshot APIs; specified in PROJECT.md |
| Selfbot via discord.py gateway | Discord TOS explicitly bans automated user accounts; permanent ban |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| VISN-01 | Phase 3 | Pending |
| VISN-02 | Phase 3 | Pending |
| VISN-03 | Phase 3 | Pending |
| VISN-04 | Phase 3 | Pending |
| VISN-05 | Phase 3 | Pending |
| DISC-01 | Phase 4 | Pending |
| DISC-02 | Phase 4 | Pending |
| DISC-03 | Phase 4 | Pending |
| DISC-04 | Phase 4 | Pending |
| DISC-05 | Phase 4 | Pending |
| DISC-06 | Phase 4 | Pending |
| AUTO-01 | Phase 5 | Pending |
| AUTO-02 | Phase 5 | Pending |
| AUTO-03 | Phase 5 | Pending |
| AUTO-04 | Phase 6 | Pending |
| AUTO-05 | Phase 6 | Pending |
| AUTO-06 | Phase 6 | Pending |

**Coverage:**
- v1.1 requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0 ✓

---
*Requirements defined: 2026-03-24*
*Last updated: 2026-03-24 — traceability table populated after roadmap creation*
