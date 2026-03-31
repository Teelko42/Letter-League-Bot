# Phase 8: Autonomous Game Loop - Context

**Gathered:** 2026-03-31
**Status:** Ready for planning

<domain>
## Phase Boundary

A `/autoplay start` command launches a self-sustaining turn loop that reads the board, selects a move, places tiles, and posts a status update — all concurrent with discord.py — and can be stopped cleanly with `/autoplay stop`. Covers slash command interface, game loop orchestration, resilience/reconnection, and game lifecycle management. Does not cover move generation (Phase 1), vision pipeline (Phase 3), turn detection (Phase 6), or tile placement mechanics (Phase 7) — those are consumed as-is.

</domain>

<decisions>
## Implementation Decisions

### Slash command design
- Single `/autoplay` command with subcommands: `start`, `stop`, `status`
- `/autoplay start` takes no arguments — channel URL from config (.env), difficulty/mode from existing `/setdifficulty` and `/setmode` commands
- No permission restrictions — anyone in the server can start/stop/check status
- Single session only — `/autoplay start` fails with a message if already running (one browser context, one Discord account)

### Status reporting
- Rich embed format for per-turn Discord messages (consistent with existing `/analyze` embeds)
- Post in the same text channel where `/autoplay start` was invoked
- Each turn update shows: word played, score, and turn number (e.g., "Played QUEST across row 5 for 42 pts — turn 7")
- Tile swap turns also get a message: "Swapped tiles (no valid moves) — turn 8"

### Reconnection & resilience
- Activity disconnect: 3 retries with increasing backoff (5s, 15s, 30s), then give up
- On reconnection failure: stop the loop and post a Discord message in the autoplay channel explaining what happened
- Vision pipeline errors (Claude API failures): retry once, then skip the turn cycle and wait for the next poll
- Full browser crash: relaunch BrowserSession, re-navigate to Activity, resume the loop (uses persistent session data)

### Game lifecycle
- `/autoplay start` is fully automatic: launches browser, navigates to channel, opens Activity, starts polling — one command does everything
- Supports joining mid-game — reads current board state and starts playing from wherever the game is
- Game-over detection (from Phase 6's `classify_frame()`): post a final summary embed (game-over notice, total turns played), then cleanly stop the loop and close the browser
- `/autoplay stop`: finishes the current turn if mid-placement (avoid leaving tiles half-placed), then stops gracefully

### Claude's Discretion
- Internal state management approach (dataclass, enum, etc.)
- How /autoplay status displays current state (running/stopped, turn count, uptime)
- Exact embed styling (colors, fields, footer)
- Cog structure (new AutoPlayCog vs extending AdvisorCog)
- Cancellation token pattern for graceful shutdown
- Logging verbosity and format

</decisions>

<code_context>
## Existing Code Insights

### Reusable Assets
- `BrowserSession` (src/browser/session.py): Persistent patchright browser with Discord auth — start() returns Page
- `navigate_to_activity()` (src/browser/navigator.py): Full navigation flow from Page to Activity iframe Frame
- `capture_canvas()` (src/browser/capture.py): Non-blank screenshot capture from iframe — returns PNG bytes
- `poll_turn()` (src/browser/turn_detector.py): Adaptive polling loop returning TurnState ("my_turn" / "not_my_turn" / "game_over")
- `preflight_check()` (src/browser/turn_detector.py): One-frame validation before entering poll loop
- `TilePlacer.place_move()` (src/browser/tile_placer.py): Full placement + confirmation flow — returns True (accepted) or False (tile swap used)
- `extract_board_state()` (src/vision/__init__.py): Async vision pipeline — returns (Board, rack)
- `find_all_moves()` (src/engine/moves.py): Move generation — returns list[Move] sorted by score desc
- `DifficultyEngine.select_move()` (src/difficulty/engine.py): Difficulty-scaled move selection
- `ChannelStore` (src/bot/channel_state.py): Per-channel difficulty/mode state
- Existing embed formatting in `src/bot/formatter.py`

### Established Patterns
- discord.py cog pattern with slash commands (AdvisorCog)
- `asyncio.to_thread()` for CPU-bound engine calls (find_all_moves)
- `asyncio.create_task()` for concurrent work on the shared event loop
- Defer-first pattern for long-running slash command responses
- `bot.start(token)` owns the event loop — all async code shares it
- Quiet logging: only log on state transitions (turn_detector pattern)

### Integration Points
- `bot.gaddag`, `bot.difficulty_engine`, `bot.channel_store` — accessed from cog via `self.bot`
- `setup_hook()` in bot.py registers cogs — new AutoPlayCog would be added here
- Channel URL from `.env` / config (VOICE_CHANNEL_URL or similar)
- TilePlacer constructor takes a patchright Frame object
- place_move() expects list[Move] sorted best-first + rack as list[str]

</code_context>

<specifics>
## Specific Ideas

- The turn loop is: poll_turn() -> capture_canvas() -> extract_board_state() -> find_all_moves() -> select_move() -> place_move() -> post status embed -> repeat
- Phase 7's 1-3s inter-action delay already handles human-like pacing within tile placement; Phase 8 just orchestrates the outer loop
- Game-over state from classify_frame() is the clean exit signal — no separate game-end detection needed
- Browser crash recovery reuses the same BrowserSession.start() + navigate_to_activity() flow that /autoplay start uses initially

</specifics>

<deferred>
## Deferred Ideas

- Post final game score to Discord when game ends — partially covered (summary embed on game-over), but extracting actual score from the game-over screen would be a v2 enhancement (AUTX territory)
- Detect opponent disconnection as a distinct state — handle via existing error recovery if it manifests as an Activity disconnect
- Multi-game support / auto-queue for next game — would need separate phase
- Adaptive ML-based turn detection — deferred to AUTX-02
- Tile swap strategy integration with difficulty engine — deferred to AUTX-03

</deferred>

---

*Phase: 08-autonomous-game-loop*
*Context gathered: 2026-03-31*
