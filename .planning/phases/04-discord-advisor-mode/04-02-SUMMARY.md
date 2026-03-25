---
phase: 04-discord-advisor-mode
plan: 02
subsystem: discord
tags: [discord.py, slash-commands, app_commands, cog, vision, engine, asyncio, ephemeral, loguru]

# Dependency graph
requires:
  - phase: 01-word-engine
    provides: find_all_moves, Board, Move models consumed in /analyze handler
  - phase: 02-difficulty-system
    provides: DifficultyEngine.select_move called in /analyze difficulty step
  - phase: 03-vision-pipeline
    provides: extract_board_state async function, VisNError codes mapped to error embeds
  - phase: 04-discord-advisor-mode
    plan: 01
    provides: LetterLeagueBot skeleton, ChannelStore, all embed builder functions

provides:
  - AdvisorCog with /analyze, /setdifficulty, /setmode slash commands fully implemented
  - Full end-to-end analyze flow: defer -> validate -> vision -> engine -> difficulty -> embed
  - Per-channel difficulty and mode update handlers
  - DISCORD_TEST_GUILD_ID support for instant dev guild command sync

affects: [human-verify-checkpoint, future-cog-additions]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - Defer-first pattern — await interaction.response.defer(ephemeral=True) as absolute first line of /analyze
    - CPU-bound sync calls wrapped in asyncio.to_thread (find_all_moves, select_move)
    - Content-type validation with startswith() to handle Discord charset suffixes
    - Local import of AdvisorCog inside setup_hook to avoid circular dependency
    - DISCORD_TEST_GUILD_ID env var for instant guild-scoped command sync during development

key-files:
  created:
    - src/bot/cog.py
  modified:
    - src/bot/bot.py

key-decisions:
  - "Deferred /analyze immediately (defer-first) to prevent 3s Discord interaction timeout during vision+engine processing"
  - "Local import of AdvisorCog inside setup_hook (from src.bot.cog import AdvisorCog) to avoid circular dependency at module load"
  - "DISCORD_TEST_GUILD_ID env var enables instant command sync to test guild vs 1-hour global propagation delay"
  - "Attachment content_type validated with startswith() — Discord may append charset suffix to MIME type"

patterns-established:
  - "defer-first: /analyze handler defers before any other action, followup.send used for all subsequent responses"
  - "asyncio.to_thread wrapper: all CPU-bound sync engine calls wrapped, never called directly from async context"
  - "Difficulty reorder: selected move placed first, followed by next 2 highest-scoring for top_moves list"

requirements-completed: [DISC-02, DISC-04, DISC-05]

# Metrics
duration: 2min
completed: 2026-03-25
---

# Phase 4 Plan 02: Discord Advisor Cog Summary

**AdvisorCog with /analyze (defer+vision+engine+difficulty+embed), /setdifficulty (Range[0-100]), and /setmode (Classic/Wild choices) wired into LetterLeagueBot via setup_hook**

## Performance

- **Duration:** ~2 min
- **Started:** 2026-03-25T01:53:24Z
- **Completed:** 2026-03-25T01:55:24Z
- **Tasks:** 1 auto (Task 2 is a human-verify checkpoint)
- **Files modified:** 2

## Accomplishments

- Created AdvisorCog with /analyze: defers immediately, validates attachment (type + size), runs vision pipeline async, runs find_all_moves and DifficultyEngine.select_move in asyncio.to_thread, returns top-3 moves as ephemeral success embed
- /setdifficulty uses app_commands.Range[int, 0, 100] for Discord-side validation — no manual range check needed
- /setmode uses @app_commands.choices with Classic/Wild options, accesses value via mode.value
- Updated bot.py setup_hook to register AdvisorCog after GADDAG and DifficultyEngine are loaded; added DISCORD_TEST_GUILD_ID support for instant test guild command sync
- 107 existing tests all pass — no regressions

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement AdvisorCog with all slash commands and update bot.py** - `3839ec8` (feat)
2. **Task 2: Verify bot connects and slash commands work in Discord** - N/A (human-verify checkpoint, approved by user — all 6 steps passed)

**Plan metadata:** `dba7fee` (docs: complete AdvisorCog plan — checkpoint before human verify)

## Files Created/Modified

- `src/bot/cog.py` - AdvisorCog with /analyze, /setdifficulty, /setmode slash commands
- `src/bot/bot.py` - setup_hook updated: registers AdvisorCog after resource loading, DISCORD_TEST_GUILD_ID support

## Decisions Made

- Deferred /analyze immediately (defer-first) to prevent 3s Discord interaction timeout during vision+engine processing (4-15s expected)
- Local import of AdvisorCog inside setup_hook to avoid circular dependency at module load time
- DISCORD_TEST_GUILD_ID env var enables instant test guild command sync vs potentially 1-hour global propagation delay
- Attachment content_type validated with startswith() since Discord may append "; charset=utf-8" to MIME type

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

**External services require manual configuration before the bot can be verified:**

- `DISCORD_TOKEN` — bot token from Discord Developer Portal (Applications > Bot > Token)
- `ANTHROPIC_API_KEY` — API key for vision pipeline (Claude Vision)
- `DISCORD_TEST_GUILD_ID` — optional, guild ID for instant command sync during development
- Wordlist file at `data/wordlist.txt` (required for GADDAG build)
- Bot must be invited with `applications.commands` OAuth2 scope

**To start the bot:**
```
python -m src.bot.bot
```

## Next Phase Readiness

- Phase 4 is fully complete — the end-to-end Discord advisor MVP is human-verified and functional in a real Discord guild
- User submits a screenshot via /analyze and receives top-3 move recommendations as an ephemeral embed with "Bot is thinking..." deferral
- /setdifficulty and /setmode both confirmed working with ephemeral confirmations
- Error handling verified: non-game image returns red error embed, text file returns invalid type error
- Phase 5 (Browser Automation Foundation) begins next: Playwright infrastructure for Discord Activity interaction
- Active blockers: Discord Activity iframe selectors are undocumented (requires headed Playwright + DevTools inspection); Playwright canvas screenshot blank in headless Chromium (requires spike with canvas.toDataURL() fallback)

---
*Phase: 04-discord-advisor-mode*
*Completed: 2026-03-25*
