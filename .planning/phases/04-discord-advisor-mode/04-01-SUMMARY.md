---
phase: 04-discord-advisor-mode
plan: 01
subsystem: discord
tags: [discord.py, discord, embed, text-art, channel-state, bot, gaddag, loguru, python-dotenv]

# Dependency graph
requires:
  - phase: 01-word-engine
    provides: GADDAG, Move, Board, TileUse models used in formatter and bot entry point
  - phase: 02-difficulty-system
    provides: DifficultyEngine loaded in bot setup_hook
  - phase: 03-vision-pipeline
    provides: VisNError codes mapped in build_error_embed

provides:
  - LetterLeagueBot subclass connecting to Discord gateway with default intents
  - ChannelState dataclass and ChannelStore manager for per-channel settings isolation
  - Full embed/text-art formatting layer (build_success_embed, build_error_embed, build_no_moves_embed, build_info_embed, render_text_board)
  - main() entry point reading DISCORD_TOKEN/.env and loading GADDAG on startup

affects: [04-02-command-handlers, future-cog-additions]

# Tech tracking
tech-stack:
  added: [discord.py==2.7.1, python-dotenv==1.2.2]
  patterns:
    - Pure-function formatter module — no bot/interaction references, only returns discord.Embed
    - GADDAG loaded via asyncio.to_thread in setup_hook (fail-loud, non-blocking)
    - Per-channel in-memory state via ChannelStore dict keyed by Discord channel ID
    - Color-coded embeds — green/gold/red/blurple for success/warning/error/info

key-files:
  created:
    - src/bot/__init__.py
    - src/bot/channel_state.py
    - src/bot/formatter.py
    - src/bot/bot.py
  modified: []

key-decisions:
  - "discord.py 2.7.1 installed (not in environment before this plan)"
  - "Per-channel settings are in-memory only (reset on restart) — no persistence layer for now"
  - "GADDAG loaded in setup_hook via asyncio.to_thread — fail-loud on error, no silent degradation"
  - "Formatter is a pure-function module with no bot/interaction references"
  - "Text-art board uses [X] for new tiles, X for existing, . for empty; windowed view capped at 15 cols"

patterns-established:
  - "Color constants at module top: SUCCESS_COLOR=green, WARNING_COLOR=gold, ERROR_COLOR=red, INFO_COLOR=blurple"
  - "render_text_board: padding=2, MAX_WINDOW_COLS=15, row/col index labels for orientation"
  - "_format_move_detail: 'Across/Down from (row,col) | Tiles: A B C' format"

requirements-completed: [DISC-01, DISC-03, DISC-06]

# Metrics
duration: 3min
completed: 2026-03-25
---

# Phase 4 Plan 01: Discord Bot Skeleton Summary

**discord.py LetterLeagueBot with per-channel ChannelStore, color-coded embed builders, text-art board renderer, and GADDAG-loading entry point**

## Performance

- **Duration:** ~3 min
- **Started:** 2026-03-25T01:46:55Z
- **Completed:** 2026-03-25T01:49:42Z
- **Tasks:** 3
- **Files modified:** 4

## Accomplishments

- Created LetterLeagueBot subclass with default Discord intents, GADDAG loaded via asyncio.to_thread in setup_hook (fail-loud), and DifficultyEngine initialised before READY
- Created ChannelStore with per-channel ChannelState (difficulty=100, mode="classic") — isolated between channels, in-memory only
- Created full formatter layer: build_success_embed (top-3 moves + text-art board code block), build_error_embed (all 3 VisNError codes mapped to actionable messages), build_no_moves_embed (yellow warning with swap guidance), build_info_embed (blurple confirmations), render_text_board (windowed view with [X]/X/. chars and axis labels)
- Installed discord.py 2.7.1 and python-dotenv 1.2.2 (not previously in environment)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create channel state module** - `66b33ea` (feat)
2. **Task 2: Create formatter module with text-art board and embed builders** - `7ff4d63` (feat)
3. **Task 3: Create bot entry point with GADDAG and DifficultyEngine loading** - `8b97d10` (feat)

**Plan metadata:** TBD (docs commit)

## Files Created/Modified

- `src/bot/__init__.py` - Package init re-exporting LetterLeagueBot
- `src/bot/channel_state.py` - ChannelState dataclass + ChannelStore manager
- `src/bot/formatter.py` - All embed builders, color constants, render_text_board()
- `src/bot/bot.py` - LetterLeagueBot subclass + main() entry point

## Decisions Made

- discord.py 2.7.1 installed (not present in Python 3.10.4 env before this plan)
- Per-channel settings are in-memory only — no persistence layer needed for initial advisor mode
- GADDAG loaded fail-loud in setup_hook (bot refuses to start without its core resource)
- Formatter is a pure-function module — no bot/interaction references; testable in isolation
- Text-art board capped at 15 columns (MAX_WINDOW_COLS) to avoid Discord line-wrap

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 - Blocking] Installed discord.py and python-dotenv**
- **Found during:** Task 1 (pre-task environment check)
- **Issue:** discord.py and python-dotenv not installed in Python 3.10.4 env — all imports would fail
- **Fix:** Ran `pip install "discord.py>=2.3.2" python-dotenv` — discord.py 2.7.1 and python-dotenv 1.2.2 installed
- **Files modified:** None (package install only)
- **Verification:** `import discord` succeeds; all task verifications passed
- **Committed in:** N/A (pip install, not a code change)

---

**Total deviations:** 1 auto-fixed (blocking dependency install)
**Impact on plan:** Essential for any task to execute. No scope creep.

## Issues Encountered

None — plan executed cleanly after dependency installation.

## User Setup Required

**External services require manual configuration before running the bot:**

- `DISCORD_TOKEN` — bot token from Discord Developer Portal (Applications > Bot > Token)
- Create a Discord bot application at https://discord.com/developers/applications
- Invite bot to a test guild with `applications.commands` scope via OAuth2 URL Generator
- Add `DISCORD_TOKEN=<your-token>` to `.env` in project root

The bot will not connect without `DISCORD_TOKEN` (logs an error and exits cleanly).

## Next Phase Readiness

- Bot skeleton is ready — LetterLeagueBot can connect to Discord gateway with `python -m src.bot.bot`
- All embed formatters are in place for Plan 04-02 slash command handlers
- Plan 04-02 will add AdvisorCog with /analyze, /setdifficulty, /setmode, /info commands and uncomment the `add_cog` call in setup_hook
- 107 existing tests all pass — no regressions

---
*Phase: 04-discord-advisor-mode*
*Completed: 2026-03-25*
