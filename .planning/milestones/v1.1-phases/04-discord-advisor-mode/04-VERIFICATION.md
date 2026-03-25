---
phase: 04-discord-advisor-mode
verified: 2026-03-24T00:00:00Z
status: human_needed
score: 8/8 must-haves verified
re_verification: false
human_verification:
  - test: "Start bot with DISCORD_TOKEN and WORDLIST_PATH set, confirm it comes online and slash commands appear in guild"
    expected: "Bot shows as online; /analyze, /setdifficulty, /setmode all appear in slash command picker"
    why_human: "Discord gateway connection, slash command registration, and in-guild visibility cannot be verified without a live token and real Discord guild"
  - test: "Run /analyze with a real Letter League screenshot in Discord"
    expected: "'Bot is thinking...' appears immediately (ephemeral defer), then a green embed with text-art board and top-3 moves (word, score, position, direction, tiles consumed) arrives within ~15s"
    why_human: "End-to-end pipeline requires live Anthropic API key, real screenshot, live Discord interaction — cannot be driven programmatically"
  - test: "Run /setdifficulty 80 then /analyze with a screenshot"
    expected: "Bot confirms '80% strength for this channel' (blurple info embed), subsequent analysis selects a sub-optimal move consistent with 80% strength"
    why_human: "Per-channel state persistence across interactions requires live Discord session; difficulty effect requires observing the selected move rank"
  - test: "Run /setmode and select Wild, then /analyze"
    expected: "Bot confirms 'Mode set to Wild for this channel' (blurple embed), subsequent analysis uses Wild scoring rules"
    why_human: "Scoring mode effect on move recommendations requires live Discord session and knowledge of Wild vs Classic scoring differences"
  - test: "Run /analyze with a non-game image (e.g., a photo)"
    expected: "Red error embed appears with title 'Couldn't detect a board' and actionable guidance"
    why_human: "INVALID_SCREENSHOT code path requires vision pipeline to reject the image — needs live Anthropic API"
  - test: "Run /analyze with a text file attached instead of an image"
    expected: "Red error embed appears immediately (before vision pipeline) with 'Please attach a PNG, JPEG, or WebP screenshot' message"
    why_human: "Attachment content-type validation behavior depends on Discord's actual attachment metadata — confirmed in previous session but re-verify is good practice"
---

# Phase 4: Discord Advisor Mode Verification Report

**Phase Goal:** A user can submit a screenshot to the Discord bot and receive actionable word recommendations as an ephemeral message
**Verified:** 2026-03-24
**Status:** human_needed
**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|---------|
| 1 | LetterLeagueBot subclass connects to Discord gateway with default intents | VERIFIED | `discord.Intents.default()` used; privileged intents (members, message_content, presences) confirmed absent via Python assertion |
| 2 | Per-channel settings (difficulty, mode) are stored in-memory and isolated between channels | VERIFIED | `ChannelStore` dict keyed by channel_id; Python test confirmed channel 123 and channel 456 have independent state with defaults difficulty=100, mode="classic" |
| 3 | Success embeds display top-3 moves with text-art board, scores, positions, and tiles consumed | VERIFIED | `build_success_embed` renders `render_text_board(board, moves[0])` in code block; add_field loop over `moves[:3]` with `move.word`, `move.score`, `_format_move_detail` (direction, row, col, rack tiles) |
| 4 | Error embeds are color-coded (red) with specific, actionable messages for each VisNError code | VERIFIED | All 3 codes (INVALID_SCREENSHOT, EXTRACTION_FAILED, VALIDATION_FAILED) mapped to distinct user-facing titles and descriptions; `ERROR_COLOR = discord.Color.red()` confirmed |
| 5 | No-moves case shows a yellow warning embed with guidance instead of a blank response | VERIFIED | `build_no_moves_embed` returns `discord.Embed(color=WARNING_COLOR)` with swap-tile guidance text; `WARNING_COLOR = discord.Color.gold()` |
| 6 | User runs /analyze with a screenshot attachment and receives top-3 move recommendations as an ephemeral embed | VERIFIED (automated) | `cog.py` analyze handler: defer(ephemeral=True) at line 1, validate attachment, `extract_board_state`, `find_all_moves` in `asyncio.to_thread`, `build_success_embed`, `followup.send(embed=..., ephemeral=True)` |
| 7 | User runs /setdifficulty with a 0-100 value and the channel's difficulty setting updates | VERIFIED | `app_commands.Range[int, 0, 100]` enforces range; `channel_store.set_difficulty(interaction.channel_id, strength)` updates state; confirms with `build_info_embed` |
| 8 | User runs /setmode with classic or wild and the channel's scoring mode updates | VERIFIED | `app_commands.choices` with Classic/Wild options; `mode: app_commands.Choice[str]`; `channel_store.set_mode(interaction.channel_id, mode.value)` |

**Score:** 8/8 truths verified (all automated checks pass; live Discord behavior requires human confirmation)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `src/bot/__init__.py` | Package exports for LetterLeagueBot | VERIFIED | Imports from `src.bot.bot`; `__all__ = ["LetterLeagueBot"]`; `from src.bot import LetterLeagueBot` succeeds |
| `src/bot/channel_state.py` | ChannelState dataclass and ChannelStore manager | VERIFIED | 68 lines; `ChannelState(difficulty=100, mode="classic")`; `ChannelStore.get`, `set_difficulty`, `set_mode` all implemented and tested |
| `src/bot/formatter.py` | Embed builders and text-art board renderer | VERIFIED | 261 lines; exports all 6 required functions + 4 color constants; all embed colors confirmed correct by Python assertion |
| `src/bot/bot.py` | LetterLeagueBot subclass with GADDAG and DifficultyEngine loading | VERIFIED | 137 lines; `commands.Bot` subclass; `setup_hook` loads GADDAG via `asyncio.to_thread`, initializes DifficultyEngine, registers AdvisorCog; `main()` reads DISCORD_TOKEN via dotenv |
| `src/bot/cog.py` | AdvisorCog with /analyze, /setdifficulty, /setmode slash commands | VERIFIED | 219 lines; all 3 `@app_commands.command` methods present; full /analyze pipeline wired correctly |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `src/bot/bot.py` | `src/engine/gaddag.GADDAG` | `GADDAG.from_wordlist()` in `setup_hook` | WIRED | Line 81: `GADDAG.from_wordlist,` passed to `asyncio.to_thread` |
| `src/bot/bot.py` | `src/bot/channel_state.ChannelStore` | `self.channel_store` attribute | WIRED | Line 26: import; line 69: `self.channel_store = ChannelStore()` |
| `src/bot/formatter.py` | `src/engine/models.Move` | Move fields used in embed rendering | WIRED | Line 165: `move.word`, `move.score`; `_format_move_detail` uses `move.direction`, `move.start_row`, `move.start_col`, `move.rack_tiles_consumed()` |
| `src/bot/formatter.py` | `src/vision/errors.VisNError` | Error code switching for embed messages | WIRED | Lines 14-16: import all 3 constants; lines 185-198: dict mapping all 3 codes to messages |
| `src/bot/cog.py /analyze` | `src/vision.extract_board_state` | `await extract_board_state(img_bytes, mode=state.mode)` | WIRED | Line 29: import; line 97: `board, rack = await extract_board_state(img_bytes, mode=state.mode)` |
| `src/bot/cog.py /analyze` | `src/engine/moves.find_all_moves` | `asyncio.to_thread(find_all_moves, ...)` | WIRED | Line 28: import; lines 102-103: `await asyncio.to_thread(find_all_moves, board, rack, self.bot.gaddag, state.mode)` |
| `src/bot/cog.py /analyze` | `src/difficulty/engine.DifficultyEngine.select_move` | `asyncio.to_thread(difficulty_engine.select_move, ...)` | WIRED | Lines 122-123: `await asyncio.to_thread(self.bot.difficulty_engine.select_move, moves, state.difficulty)` |
| `src/bot/cog.py /analyze` | `src/bot/formatter.build_success_embed` | `embed = build_success_embed(top_moves, board)` | WIRED | Line 26: import; line 138: `embed = build_success_embed(top_moves, board)` |
| `src/bot/cog.py /analyze` | `src/bot/formatter.build_error_embed` | `embed = build_error_embed(e)` on VisNError catch | WIRED | Line 22: import; line 144: `embed=build_error_embed(e)` in `except VisNError` block |
| `src/bot/cog.py /setdifficulty` | `src/bot/channel_state.ChannelStore` | `channel_store.set_difficulty(channel_id, strength)` | WIRED | Line 169: `self.bot.channel_store.set_difficulty(interaction.channel_id, strength)` |
| `src/bot/cog.py /setmode` | `src/bot/channel_state.ChannelStore` | `channel_store.set_mode(channel_id, mode.value)` | WIRED | Line 206: `self.bot.channel_store.set_mode(interaction.channel_id, mode.value)` |
| `src/bot/bot.py setup_hook` | `src/bot/cog.AdvisorCog` | `await self.add_cog(AdvisorCog(self))` | WIRED | Lines 92-93: local import + `await self.add_cog(AdvisorCog(self))` after resource loading |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|---------|
| DISC-01 | 04-01-PLAN.md | Discord bot connects to gateway with proper token auth and privileged intents | VERIFIED | `discord.Intents.default()` used (correct for slash-only bot); `DISCORD_TOKEN` read from `.env` via `load_dotenv()`; `on_ready` logs gateway connection; `commands.Bot.__init__` called with intents |
| DISC-02 | 04-02-PLAN.md | User can run `/analyze` slash command with a screenshot attachment to receive move suggestions | VERIFIED (automated) | `@app_commands.command(name="analyze")` with `screenshot: discord.Attachment` parameter; full pipeline wired; human verify step approved in SUMMARY |
| DISC-03 | 04-01-PLAN.md | Bot responds with top-3 move recommendations (word, position, direction, score) as an ephemeral message | VERIFIED | `build_success_embed(moves[:3], board)` renders word+score in field names; `_format_move_detail` renders direction+position; all sent `ephemeral=True` |
| DISC-04 | 04-02-PLAN.md | User can run `/setdifficulty` to configure bot play strength (0-100%) | VERIFIED | `@app_commands.command(name="setdifficulty")`; `app_commands.Range[int, 0, 100]` enforces range; `channel_store.set_difficulty` persists per-channel |
| DISC-05 | 04-02-PLAN.md | User can specify Classic or Wild scoring mode as a parameter | VERIFIED | `@app_commands.command(name="setmode")`; `@app_commands.choices(mode=[Choice("Classic","classic"), Choice("Wild","wild")])`; `channel_store.set_mode(channel_id, mode.value)` |
| DISC-06 | 04-01-PLAN.md | Bot returns actionable error messages for bad screenshots, API failures, or zero valid moves | VERIFIED | All 3 VisNError codes mapped to distinct actionable messages in `build_error_embed`; `build_no_moves_embed` for zero-moves case; `build_error_embed_generic` for unexpected exceptions; invalid attachment type caught before pipeline |

**Orphaned requirements check:** REQUIREMENTS.md maps only DISC-01 through DISC-06 to Phase 4. Plans 04-01 and 04-02 together claim all 6. No orphaned requirements.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| None | — | — | — | No TODOs, FIXMEs, stub returns, placeholder comments, or console-log-only handlers found in any `src/bot/` file |

### Human Verification Required

The following items require live Discord testing. All 6 steps were marked as approved in the 04-02-SUMMARY.md human-verify checkpoint, but the verifier independently flags them as requiring human confirmation since they cannot be validated programmatically.

**1. Gateway Connection and Command Registration**

**Test:** Start bot with `python -m src.bot.bot`, with `DISCORD_TOKEN`, `WORDLIST_PATH`, and `DISCORD_TEST_GUILD_ID` set in `.env`
**Expected:** Bot appears online in test guild; `/analyze`, `/setdifficulty`, `/setmode` all appear in slash command picker
**Why human:** Discord gateway connection and slash command tree sync require a live token and guild — not simulatable in CI

**2. /analyze End-to-End with Real Screenshot**

**Test:** Attach a Letter League screenshot to `/analyze` in Discord
**Expected:** "Bot is thinking..." appears immediately (ephemeral defer), then a green embed with text-art board and top-3 moves (word, score, position, direction, tiles consumed) arrives within ~15s
**Why human:** Live Anthropic API call, real screenshot required; timing behavior of defer cannot be verified statically

**3. /setdifficulty Persistence and Effect**

**Test:** Run `/setdifficulty 80`, then run `/analyze` on the same channel
**Expected:** Blurple confirmation "Play strength set to 80% for this channel"; analysis then reflects sub-optimal (80%) move selection
**Why human:** Per-channel state across Discord interactions requires live session; difficulty effect on move rank requires observing the actual move returned

**4. /setmode and Wild Scoring**

**Test:** Run `/setmode` and select Wild, then `/analyze`
**Expected:** Blurple confirmation; subsequent analysis applies Wild scoring (permanent multiplier bonding)
**Why human:** Scoring mode effect on recommendations requires live session and game rule knowledge

**5. Bad Screenshot Error Path**

**Test:** Run `/analyze` with a non-game image (e.g., a photo of a coffee cup)
**Expected:** Red error embed with "Couldn't detect a board" title and actionable guidance message
**Why human:** INVALID_SCREENSHOT requires the vision API to process and reject the image — needs live Anthropic API

**6. Invalid File Type Rejection**

**Test:** Run `/analyze` with a `.txt` file attached instead of an image
**Expected:** Red error embed appears immediately (no API call made) with "Please attach a PNG, JPEG, or WebP screenshot (max 10 MB)" message
**Why human:** Attachment content-type validation behavior depends on Discord's actual attachment metadata format

*Note: All 6 human-verify steps were confirmed as passing in the 04-02-SUMMARY.md approved checkpoint (2026-03-25).*

### Gaps Summary

No automated gaps found. All 8 must-have truths verified programmatically. All 5 artifacts exist, are substantive, and are wired. All 11 key links confirmed present in source. All 6 requirements (DISC-01 through DISC-06) satisfied. No anti-patterns detected. 107 existing tests pass with no regressions.

The only outstanding items are the 6 human verification tests for live Discord behavior — these were previously approved by the user during the 04-02 plan execution checkpoint.

---

_Verified: 2026-03-24_
_Verifier: Claude (gsd-verifier)_
