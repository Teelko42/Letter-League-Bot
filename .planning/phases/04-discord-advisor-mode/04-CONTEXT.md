# Phase 4: Discord Advisor Mode - Context

**Gathered:** 2026-03-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Discord bot that accepts a Letter League screenshot via slash command and returns the top-3 word recommendations as an ephemeral embed. Wires together the vision pipeline (Phase 3) and word engine (Phase 1) with difficulty scaling (Phase 2) into a user-facing Discord interaction. Browser automation and autonomous play are separate phases.

</domain>

<decisions>
## Implementation Decisions

### Response presentation
- Rich Discord embed for all responses (success, error, warnings)
- Top-1 move displayed as a text-art mock board showing letter placement on the grid
- All 3 moves listed with: word, score, position+direction, and which rack tiles are consumed
- Moves #2 and #3 shown as text fields below the board (no separate boards)

### Difficulty & mode configuration
- Two separate slash commands: `/setdifficulty <0-100>` and `/setmode <classic|wild>`
- Settings scoped per-channel (not per-user)
- In-memory storage only — settings reset on bot restart
- Defaults: 100% strength, Classic scoring mode

### Interaction flow
- Screenshot input via `/analyze` slash command with attachment only — no channel image listener
- Use Discord's native defer (`interaction.response.defer(ephemeral=True)`) for "Bot is thinking..." indicator
- All responses are ephemeral (only visible to the invoking user)
- If pipeline exceeds Discord's interaction timeout, send a graceful error suggesting retry

### Error handling
- Specific, actionable error messages — tell the user what went wrong and how to fix it
- Color-coded embeds: green for success, yellow for warnings, red for errors
- Bad screenshot: explain what's wrong (e.g., "Couldn't detect a board — make sure the full game board is visible")
- No valid moves: always show something — surface low-scoring partial options rather than a blank "no moves" message
- Vision API down/rate-limited: tell user to retry later, no auto-retry or queuing

### Claude's Discretion
- Embed field layout and exact formatting
- Text-art board rendering approach (character set, spacing)
- Exact slash command parameter validation
- Logging and internal error handling strategy

</decisions>

<specifics>
## Specific Ideas

- The text board mock should show the placed word in context of existing tiles — user wants to see WHERE on the board the word goes, not just coordinates
- "Essentials + tiles used" was specifically chosen over full detail or bare minimum — users want to plan their next turn knowing which tiles get consumed

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 04-discord-advisor-mode*
*Context gathered: 2026-03-24*
