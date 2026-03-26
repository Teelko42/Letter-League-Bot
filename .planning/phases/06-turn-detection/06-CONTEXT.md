# Phase 6: Turn Detection - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Visual polling to identify when the bot is the active player by inspecting the game canvas. Returns one of three states: my turn, not my turn, or game over. Does not act on the detected state — downstream phases (tile placement, game loop) consume the turn signal.

</domain>

<decisions>
## Implementation Decisions

### Signal Discovery
- The "my turn" indicator is an orange square banner with white "YOUR TURN" text at the top of the game canvas
- When it is the opponent's turn, the banner disappears entirely — absence of the banner = not my turn
- Detection uses pixel/color matching only — no OCR or text recognition
- Automated screenshot collection during a live game to calibrate the exact pixel region and orange color values

### Polling Behavior
- Poll every 1-2 seconds initially
- Adaptive backoff: after ~30 seconds of "not my turn", gradually slow to ~5 second intervals
- Snap back to 1-2s polling immediately when a turn change is detected
- Quiet logging: only log when a turn state change occurs (my turn detected, game over detected), not every poll cycle
- On screenshot/capture failure: retry with exponential backoff before escalating

### Confidence & Safety
- Strict confidence threshold — only trigger "my turn" when pixel match confidence is very high; better to miss one poll cycle than act out of turn
- Pre-flight calibration check: before entering the poll loop, verify the bot can see and detect the banner region in the expected screen area — fail early if the UI layout changed
- Save reference screenshots to disk (debug folder) during calibration and signal discovery for threshold tuning and future validation

### Game State Detection
- Three recognized states: `my_turn`, `not_my_turn`, `game_over`
- Game-over detection: the game-over screen shows a leaderboard overlay in the center with players, winner on the right side, and the board on the left side — visually distinct from normal gameplay
- Game-over signal causes the detector to return a distinct state so downstream code can stop the loop

### Claude's Discretion
- Exact HSV/RGB thresholds for the orange banner color
- Pixel region detection algorithm (bounding box search, fixed region, etc.)
- Game-over detection method (could be leaderboard overlay detection, absence of game board, etc.)
- Backoff curve shape and exact timing
- Reference screenshot storage format and cleanup policy

</decisions>

<specifics>
## Specific Ideas

- The orange banner is high-contrast (orange background, white text) — should be a strong, reliable signal for color-based detection
- Banner presence = my turn, banner absence = not my turn — a clean binary signal with no ambiguous intermediate state
- Game-over screen has a fundamentally different layout (leaderboard overlay, players centered, winner on right, board on left) — should be distinguishable from normal game view

</specifics>

<deferred>
## Deferred Ideas

- Post final game score to Discord when game ends — belongs in Phase 8 (Autonomous Game Loop) which already covers Discord status messages
- Detect opponent disconnection as a distinct state — handle via error recovery in Phase 8 if needed

</deferred>

---

*Phase: 06-turn-detection*
*Context gathered: 2026-03-26*
