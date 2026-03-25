# Phase 4: Discord Advisor Mode - Research

**Researched:** 2026-03-24
**Domain:** discord.py 2.x slash commands, async bot architecture, ephemeral embeds, in-memory channel state
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

#### Response presentation
- Rich Discord embed for all responses (success, error, warnings)
- Top-1 move displayed as a text-art mock board showing letter placement on the grid
- All 3 moves listed with: word, score, position+direction, and which rack tiles are consumed
- Moves #2 and #3 shown as text fields below the board (no separate boards)

#### Difficulty & mode configuration
- Two separate slash commands: `/setdifficulty <0-100>` and `/setmode <classic|wild>`
- Settings scoped per-channel (not per-user)
- In-memory storage only — settings reset on bot restart
- Defaults: 100% strength, Classic scoring mode

#### Interaction flow
- Screenshot input via `/analyze` slash command with attachment only — no channel image listener
- Use Discord's native defer (`interaction.response.defer(ephemeral=True)`) for "Bot is thinking..." indicator
- All responses are ephemeral (only visible to the invoking user)
- If pipeline exceeds Discord's interaction timeout, send a graceful error suggesting retry

#### Error handling
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

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DISC-01 | Discord bot connects to gateway with proper token auth and privileged intents | `discord.py` 2.7.1 `commands.Bot` with `discord.Intents.default()` — no privileged intents needed for slash-command-only advisor mode; token via `python-dotenv` |
| DISC-02 | User can run `/analyze` slash command with a screenshot attachment to receive move suggestions | `@app_commands.command` with `discord.Attachment` parameter; `await attachment.read()` returns bytes; `defer(ephemeral=True)` → `followup.send()` pattern |
| DISC-03 | Bot responds with top-3 move recommendations (word, position, direction, score) as an ephemeral message | `discord.Embed` with color-coding; text-art board in `description` or first field; moves #2 and #3 as inline fields; `followup.send(embed=embed, ephemeral=True)` |
| DISC-04 | User can run `/setdifficulty` to configure bot play strength (0-100%) | `@app_commands.command` with `app_commands.Range[int, 0, 100]` parameter; per-channel dict stored in `Bot` subclass attribute |
| DISC-05 | User can specify Classic or Wild scoring mode as a parameter | `/setmode` slash command with `app_commands.choices` or `Literal["classic", "wild"]`; channel-scoped in-memory dict |
| DISC-06 | Bot returns actionable error messages for bad screenshots, API failures, or zero valid moves | `VisNError` code-switch on `INVALID_SCREENSHOT`/`EXTRACTION_FAILED`/`VALIDATION_FAILED`; red embed with specific guidance; fallback partial move list for zero-moves case |
</phase_requirements>

---

## Summary

Phase 4 wires the completed vision pipeline (Phase 3) and word engine (Phase 1) together into a user-facing Discord bot. The primary challenge is not algorithmic but structural: bridging synchronous CPU-bound engine code and a slow async Vision API into discord.py's single asyncio event loop without freezing the bot.

The standard solution is two-step: (1) call `await interaction.response.defer(ephemeral=True)` as the absolute first line of the `/analyze` handler — this extends the 3-second Discord timeout to 15 minutes; (2) wrap the synchronous `GameEngine.find_moves()` call in `await asyncio.to_thread(...)` to run it off the event loop. The vision pipeline is already async (`extract_board_state` is a coroutine) and needs no wrapping.

Per-channel settings (difficulty, mode) use a plain dict keyed by `interaction.channel_id` stored on the `Bot` subclass. No database is required — settings are explicitly ephemeral per the user's decision. All Discord responses are embeds with color-coded status (green success / yellow warning / red error).

**Primary recommendation:** Build the bot as a single `src/bot/` module. Define a `LetterLeagueBot(commands.Bot)` subclass for state, put commands in a `Cog`, sync commands in `setup_hook`, and expose a standalone `bot.py` entry point. This matches discord.py 2.x best practices and keeps the Discord layer cleanly separated from the engine.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `discord.py` | `2.7.1` | Bot gateway, slash commands, attachment handling, embeds | Project constraint. Active, 5,400+ commits. v2.x has native `app_commands` (slash commands) and full asyncio. Released 2026-03-03. Already in STACK.md. |
| `python-dotenv` | `1.2.2` | Load `DISCORD_TOKEN` and `ANTHROPIC_API_KEY` from `.env` | Already in STACK.md. The `.env` file is gitignored and already partially populated (ANTHROPIC_API_KEY). `DISCORD_TOKEN` must be added. |
| `loguru` | `0.7.3` | Structured logging for command dispatch, errors, timing | Already installed per STATE.md. Consistent with vision pipeline logging. |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `asyncio` (stdlib) | Python 3.11 | `asyncio.to_thread()` for running synchronous engine code off event loop | Always — required to prevent `GameEngine.find_moves()` from blocking the bot |
| `discord.Embed` | discord.py built-in | Structured response formatting with color, fields, title | Always — user decision locked on rich embeds for all responses |
| `app_commands.Range` | discord.py built-in | Native 0–100 range enforcement for `/setdifficulty` parameter | Preferred — enforces constraint in Discord UI, not application code |
| `app_commands.choices` | discord.py built-in | Dropdown for `/setmode classic|wild` parameter | Preferred — limits input to valid options, shown in Discord autocomplete |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| `asyncio.to_thread()` | `loop.run_in_executor(None, fn, *args)` | `to_thread()` is cleaner syntax (Python 3.9+); both are equivalent. Use `to_thread()`. |
| `app_commands.Range[int, 0, 100]` | Manual `if difficulty < 0 or difficulty > 100` check | `Range` enforces in Discord UI before the handler is called; manual check is redundant fallback. |
| In-memory per-channel dict | `aiosqlite` + SQLite | User decision: in-memory only. aiosqlite is for v2 persistence (ADVX-02). |
| `followup.send(embed=...)` | `edit_original_response(embed=...)` | Both work after `defer()`. `followup.send()` is standard; `edit_original_response()` is for modifying the deferred thinking state. Either is acceptable. |

**Installation:**
```bash
# All already specified in STACK.md — no new installs needed for Phase 4.
# Confirm these are present:
pip install "discord.py==2.7.1"
pip install "python-dotenv==1.2.2"
pip install "loguru==0.7.3"
```

Add to `.env`:
```
DISCORD_TOKEN=your_bot_token_here
```

---

## Architecture Patterns

### Recommended Project Structure

```
src/
├── engine/         # v1.0 — unchanged
├── difficulty/     # v1.0 — unchanged
├── vision/         # v1.1 Phase 3 — unchanged
└── bot/
    ├── __init__.py          # exports LetterLeagueBot
    ├── bot.py               # main entry point (bot startup)
    ├── cog.py               # all slash commands as a Cog
    ├── formatter.py         # embed construction + text-art board renderer
    └── channel_state.py     # ChannelState dataclass + in-memory store

bot.py               # top-level runner (main entry point outside src/)
```

### Pattern 1: Bot Subclass with Channel State

**What:** Subclass `commands.Bot` to hold per-channel settings as a `dict[int, ChannelState]`. This makes settings accessible from the `Cog` via `self.bot.channel_settings[channel_id]`.

**When to use:** Always — required for per-channel in-memory state without a database.

**Example:**
```python
# Source: discord.py official docs + project decision
import discord
from discord.ext import commands
from dataclasses import dataclass, field

@dataclass
class ChannelState:
    difficulty: int = 100      # 0-100%, default 100
    mode: str = "classic"      # "classic" or "wild"

class LetterLeagueBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
        self.channel_settings: dict[int, ChannelState] = {}

    def get_channel_state(self, channel_id: int) -> ChannelState:
        """Return channel settings, creating defaults if needed."""
        if channel_id not in self.channel_settings:
            self.channel_settings[channel_id] = ChannelState()
        return self.channel_settings[channel_id]

    async def setup_hook(self) -> None:
        """Called before READY. Load cog and sync commands."""
        await self.add_cog(AdvisorCog(self))
        await self.tree.sync()
```

### Pattern 2: Slash Commands in a Cog

**What:** All three slash commands (`/analyze`, `/setdifficulty`, `/setmode`) defined as methods on a `commands.Cog` subclass. The cog receives the `bot` instance, giving access to `channel_settings` and the loaded engine.

**When to use:** Always — cog pattern is the standard for organizing commands in discord.py 2.x.

**Example:**
```python
# Source: discord.py 2.x documentation + deepwiki verified patterns
from discord.ext import commands
from discord import app_commands
import discord

class AdvisorCog(commands.Cog):
    def __init__(self, bot: LetterLeagueBot) -> None:
        self.bot = bot

    @app_commands.command(name="analyze", description="Analyze a Letter League screenshot")
    @app_commands.describe(screenshot="A screenshot of your Letter League game board")
    async def analyze(
        self,
        interaction: discord.Interaction,
        screenshot: discord.Attachment,
    ) -> None:
        # MUST be first line — extends 3s window to 15 min
        await interaction.response.defer(ephemeral=True)
        # ... analysis logic ...
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="setdifficulty", description="Set bot play strength (0=easy, 100=optimal)")
    @app_commands.describe(strength="Play strength as a percentage (0-100)")
    async def setdifficulty(
        self,
        interaction: discord.Interaction,
        strength: app_commands.Range[int, 0, 100],
    ) -> None:
        state = self.bot.get_channel_state(interaction.channel_id)
        state.difficulty = strength
        await interaction.response.send_message(
            embed=make_info_embed(f"Difficulty set to {strength}%"), ephemeral=True
        )

    @app_commands.command(name="setmode", description="Set scoring mode for this channel")
    @app_commands.describe(mode="Classic: multipliers apply once. Wild: multipliers bond to tiles.")
    @app_commands.choices(mode=[
        app_commands.Choice(name="Classic", value="classic"),
        app_commands.Choice(name="Wild", value="wild"),
    ])
    async def setmode(
        self,
        interaction: discord.Interaction,
        mode: str,
    ) -> None:
        state = self.bot.get_channel_state(interaction.channel_id)
        state.mode = mode
        await interaction.response.send_message(
            embed=make_info_embed(f"Mode set to {mode.capitalize()}"), ephemeral=True
        )
```

### Pattern 3: Defer → Async Work → Followup

**What:** The `/analyze` handler must defer immediately then dispatch async work. The synchronous `find_moves()` engine call must be wrapped with `asyncio.to_thread()` to avoid blocking the event loop.

**When to use:** Every time the handler does work taking more than 3 seconds, and every time a synchronous CPU-bound function is called from an async handler.

**Example:**
```python
# Source: PITFALLS.md verified patterns + discord.py FAQ
import asyncio
from src.vision import extract_board_state, VisNError, INVALID_SCREENSHOT, EXTRACTION_FAILED, VALIDATION_FAILED
from src.engine import GameEngine
from src.difficulty.engine import DifficultyEngine

async def _run_analysis(img_bytes: bytes, state: ChannelState, engine: GameEngine, difficulty_engine: DifficultyEngine):
    """Full analysis pipeline — runs in async context."""
    # Vision pipeline — already async
    board, rack = await extract_board_state(img_bytes, mode=state.mode)

    # CPU-bound engine call — must run in thread to free event loop
    moves = await asyncio.to_thread(engine.find_moves, rack)

    # Difficulty selection — also CPU-bound
    top_move = await asyncio.to_thread(difficulty_engine.select_move, moves, state.difficulty)

    return board, rack, moves, top_move

@app_commands.command(name="analyze", ...)
async def analyze(self, interaction: discord.Interaction, screenshot: discord.Attachment) -> None:
    await interaction.response.defer(ephemeral=True)  # ALWAYS FIRST

    try:
        img_bytes = await screenshot.read()
        board, rack, moves, top_move = await _run_analysis(
            img_bytes,
            self.bot.get_channel_state(interaction.channel_id),
            self.bot.engine,
            self.bot.difficulty_engine,
        )
        embed = build_success_embed(moves[:3], board)
        await interaction.followup.send(embed=embed)

    except VisNError as e:
        embed = build_error_embed(e)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        logger.exception("Unexpected error in /analyze: {}", e)
        await interaction.followup.send(embed=build_error_embed_generic())
```

### Pattern 4: Embed Construction

**What:** All responses use `discord.Embed`. Success = green, warnings = gold, errors = red. The top-1 move renders as a text-art board in the embed description. Moves #2 and #3 go in embed fields.

**Discord embed limits (verified):**
- `description`: 4096 characters max
- Field `value`: 1024 characters max
- Total embed: 6000 characters max
- Max 25 fields

The text-art board for a visible window of the move (not the full 27x19 grid) should stay well within the 4096-character description limit. A 10x10 window with 2-character cells = 200 chars + formatting.

**Example:**
```python
# Source: discord.py built-in + community verified patterns
import discord

def build_success_embed(moves: list, board) -> discord.Embed:
    """Build the success embed with top-3 moves."""
    top = moves[0]
    embed = discord.Embed(
        title="Letter League Analysis",
        color=discord.Color.brand_green(),  # #57F287
    )
    # Text-art board in description — monospace via code block
    board_art = render_text_board(board, top)
    embed.description = f"**Best Move**\n```\n{board_art}\n```"

    # Move 1 summary below board
    embed.add_field(
        name=f"1. {top.word} — {top.score} pts",
        value=format_move_detail(top),
        inline=False,
    )

    if len(moves) > 1:
        embed.add_field(
            name=f"2. {moves[1].word} — {moves[1].score} pts",
            value=format_move_detail(moves[1]),
            inline=True,
        )
    if len(moves) > 2:
        embed.add_field(
            name=f"3. {moves[2].word} — {moves[2].score} pts",
            value=format_move_detail(moves[2]),
            inline=True,
        )
    return embed

def build_error_embed(err: VisNError) -> discord.Embed:
    """Map VisNError codes to user-facing error embeds."""
    messages = {
        INVALID_SCREENSHOT: (
            "Couldn't detect a board",
            "Make sure the full game board is visible and try again."
        ),
        EXTRACTION_FAILED: (
            "Vision API unavailable",
            "The analysis service is temporarily unavailable. Please try again in a moment."
        ),
        VALIDATION_FAILED: (
            "Board reading failed",
            "The screenshot was unclear or the board couldn't be parsed. Try a clearer screenshot."
        ),
    }
    title, description = messages.get(err.code, ("Analysis failed", str(err.message)))
    return discord.Embed(title=title, description=description, color=discord.Color.red())
```

### Pattern 5: Text-Art Board Renderer

**What:** Render a small window around the placed word on the board as monospace ASCII/Unicode. Wraps in triple backtick code block for monospace rendering in Discord.

**Window approach:** Show the word's bounding box ± 2 cells padding, capped at a reasonable size. The full 27x19 grid is too large (27 cols × ~3 chars/cell = 81+ chars per row, Discord wraps at ~80). A windowed view of ~10-15 columns shows context without wrapping.

**Character set (Claude's discretion):**
- Empty cell: `·` or `.`
- Existing board tile: `[X]` where X is the letter
- New tile being placed: `(X)` or `>X<` to highlight placement
- Multiplier squares (empty): `DL`, `TL`, `DW`, `TW` (3-char wide slots)

**Example skeleton:**
```python
def render_text_board(board, move, padding: int = 2) -> str:
    """Render a windowed text-art view of the board around the placed word.

    Window is bounded by the move's extent ± padding, capped to avoid Discord
    line-wrap (max ~26 chars per row for comfortable reading in a code block).
    """
    placed = {(t.row, t.col): t.letter for t in move.tiles_used if t.from_rack}
    existing = {(t.row, t.col): t.letter for t in move.tiles_used if not t.from_rack}

    row_min = max(0, min(t.row for t in move.tiles_used) - padding)
    row_max = min(board.rows - 1, max(t.row for t in move.tiles_used) + padding)
    col_min = max(0, min(t.col for t in move.tiles_used) - padding)
    col_max = min(board.cols - 1, max(t.col for t in move.tiles_used) + padding)

    lines = []
    for r in range(row_min, row_max + 1):
        row_cells = []
        for c in range(col_min, col_max + 1):
            if (r, c) in placed:
                row_cells.append(f"[{placed[(r, c)]}]")
            elif (r, c) in existing:
                row_cells.append(f" {existing[(r, c)]} ")
            elif board.cells[r][c].letter:
                row_cells.append(f" {board.cells[r][c].letter} ")
            else:
                row_cells.append(" · ")
        lines.append("".join(row_cells))
    return "\n".join(lines)
```

### Anti-Patterns to Avoid

- **Calling synchronous engine in async handler directly:** `moves = engine.find_moves(rack)` blocks the event loop. Always use `await asyncio.to_thread(engine.find_moves, rack)`.
- **Sending message before deferring:** Any code before `await interaction.response.defer()` in a slow handler risks the 3-second timeout. Defer is the absolute first line, no exceptions.
- **Using `interaction.response.send_message()` after `defer()`:** This raises `InteractionAlreadyResponded`. After deferring, only `interaction.followup.send()` or `interaction.edit_original_response()` is valid.
- **Syncing commands on every bot startup in production:** `tree.sync()` in `setup_hook` is fine for development. In production, commands should be synced once after deployment, not on every restart (triggers Discord rate limits). For now, sync in `setup_hook` is acceptable.
- **Per-user settings:** User decision locks settings to per-channel scope. Do NOT key on `interaction.user.id`.
- **Hardcoding `DISCORD_TOKEN`:** Never. Load via `os.environ["DISCORD_TOKEN"]` from `.env` (python-dotenv already in project).

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Interaction acknowledgment timing | Custom delay/retry logic | `await interaction.response.defer(ephemeral=True)` | Discord's built-in mechanism; no custom timing needed |
| Parameter range enforcement | `if strength < 0 or strength > 100` validator | `app_commands.Range[int, 0, 100]` | Enforced by Discord UI before handler is called; visible to user in autocomplete |
| Mode option dropdown | Parse free-text "classic" vs "wild" | `@app_commands.choices(...)` | Limits input to valid options; shown as dropdown in Discord UI |
| Command tree management | Custom command registry | `bot.tree` (CommandTree) + `setup_hook` | discord.py provides a complete command tree with guild/global sync |
| Attachment download | Manual HTTP client | `await attachment.read()` | Built into `discord.Attachment`; returns raw bytes directly |
| Embed color constants | RGB tuples | `discord.Color.brand_green()`, `.red()`, `.gold()` | Named constants from discord.py Color; correct Discord palette values |

**Key insight:** discord.py 2.x already handles attachment download, command registration, interaction lifecycle, and parameter validation at the framework level. The application only needs to provide the business logic.

---

## Common Pitfalls

### Pitfall 1: Interaction Token Timeout (3-second window)

**What goes wrong:** The bot receives `/analyze`, starts the vision API call (4-15s), and Discord shows "The application did not respond" before the result arrives.

**Why it happens:** Discord requires an acknowledgment within 3 seconds. The vision pipeline starts after the 3-second window if defer is not called first.

**How to avoid:** `await interaction.response.defer(ephemeral=True)` is the first and only line before any async work in `/analyze`. The defer call itself takes ~200ms and extends the response window to 15 minutes.

**Warning signs:** "The application did not respond" in Discord; works in dev (fast network) but fails in production.

### Pitfall 2: Event Loop Blocking from Synchronous Engine

**What goes wrong:** `engine.find_moves()` is CPU-bound Python (GADDAG traversal, 1-5 seconds on a complex board). Calling it directly in an `async def` handler freezes the entire bot — no commands are processed, Discord heartbeat is blocked, gateway disconnects.

**Why it happens:** The v1.0 engine is a pure synchronous library. Adding Discord integration without wrapping in `asyncio.to_thread()` is the natural mistake.

**How to avoid:** `await asyncio.to_thread(engine.find_moves, rack)` — runs the engine in a thread pool worker. The event loop remains free. The engine itself is stateless per call (board is passed in or on the engine), making thread-safe usage straightforward.

**Warning signs:** `discord.py` logs `Shard ID None heartbeat blocked for more than X seconds`; bot goes unresponsive during analysis.

### Pitfall 3: GameEngine Statefulness in Advisor Mode

**What goes wrong:** `GameEngine` maintains a mutable `board` state across `play_move()` calls. In advisor mode, the bot never "plays" moves — it only analyzes screenshots and returns recommendations. If `play_move()` is called during analysis (incorrectly), the board state diverges from the real game.

**Why it happens:** The engine was designed for stateful autonomous play. Advisor mode uses only `find_moves()` and should never call `play_move()`.

**How to avoid:** In advisor mode, extract the board from the vision pipeline and use `find_all_moves(board, rack, gaddag, mode)` directly rather than going through `GameEngine`. Alternatively, create a fresh `GameEngine`-equivalent per request by passing the vision-extracted `Board` directly to `find_all_moves()`. The bot should NOT maintain a persistent `GameEngine` that accumulates state across multiple `/analyze` calls.

**Resolution:** Build a stateless analysis function:
```python
# Stateless: use the Board returned by vision, don't persist it
moves = await asyncio.to_thread(find_all_moves, board, rack, gaddag, mode)
```

### Pitfall 4: Image Validation — Type and Size

**What goes wrong:** User uploads a PDF, GIF, or oversized file as the screenshot parameter. The `attachment.read()` call succeeds, but the vision pipeline raises a confusing internal error or exceeds the Claude Vision 5 MB limit.

**Why it happens:** Discord's slash command attachment type (`discord.Attachment`) accepts any file — it does not enforce image types by itself.

**How to avoid:** Validate before calling `attachment.read()`:
```python
ALLOWED_TYPES = {"image/png", "image/jpeg", "image/webp"}
MAX_SIZE = 10_000_000  # 10 MB

if attachment.content_type not in ALLOWED_TYPES:
    await interaction.followup.send(embed=build_error_embed_type())
    return
if attachment.size > MAX_SIZE:
    await interaction.followup.send(embed=build_error_embed_size())
    return
```

### Pitfall 5: No Valid Moves — Blank Response

**What goes wrong:** The engine returns an empty moves list. The handler sends an embed with no move data, which appears broken to the user.

**Why it happens:** The vision pipeline may return a valid board but the rack tiles genuinely have no valid placements. Or a vision error resulted in a malformed board.

**How to avoid:** Per user decision: "always show something — surface low-scoring partial options rather than a blank 'no moves' message." When `moves` is empty, query the engine again with relaxed constraints or show the rack and board state with a message like "No valid placements found for this rack and board position." Do NOT return an empty embed.

### Pitfall 6: CommandTree Not Synced

**What goes wrong:** Bot starts, all code is correct, but `/analyze` does not appear in Discord. User cannot invoke the slash command.

**Why it happens:** Slash commands must be synced to Discord via `await self.tree.sync()`. Without this call, Discord doesn't know the commands exist.

**How to avoid:** Call `await self.tree.sync()` in `setup_hook()`. For development speed, optionally use `self.tree.copy_global_to(guild=discord.Object(id=GUILD_ID))` to sync to a test guild first (instant) before global sync (up to 1 hour propagation).

**Warning signs:** No slash commands appear in the Discord UI after bot starts; `@bot.tree.command` decorators are defined but commands are invisible.

---

## Code Examples

Verified patterns from official sources:

### Bot Entry Point (bot.py)
```python
# Source: discord.py 2.x official docs + pythondiscord.com guide
import asyncio
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from src.engine.gaddag import GADDAG
from src.difficulty.engine import DifficultyEngine

load_dotenv()

class LetterLeagueBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)
        self.gaddag: GADDAG | None = None
        self.difficulty_engine: DifficultyEngine | None = None
        self.channel_settings: dict[int, ChannelState] = {}

    async def setup_hook(self) -> None:
        from src.bot.cog import AdvisorCog
        # Load heavy resources before cog registers commands
        self.gaddag = await asyncio.to_thread(GADDAG.from_wordlist, WORDLIST_PATH, CACHE_PATH)
        self.difficulty_engine = DifficultyEngine()
        await self.add_cog(AdvisorCog(self))
        await self.tree.sync()

async def main() -> None:
    bot = LetterLeagueBot()
    async with bot:
        await bot.start(os.environ["DISCORD_TOKEN"])

if __name__ == "__main__":
    asyncio.run(main())
```

### Attachment Validation + Read
```python
# Source: discord.py Attachment docs + PITFALLS.md security section
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp"}
MAX_ATTACHMENT_BYTES = 10_000_000  # 10 MB

async def validate_and_read_attachment(
    attachment: discord.Attachment,
) -> bytes | None:
    """Returns image bytes or None if invalid. Caller sends error embed."""
    ct = attachment.content_type or ""
    if not any(ct.startswith(t) for t in ALLOWED_CONTENT_TYPES):
        return None
    if attachment.size > MAX_ATTACHMENT_BYTES:
        return None
    return await attachment.read()
```

### Full /analyze Handler Skeleton
```python
# Source: Composite of discord.py docs + PITFALLS.md + STATE.md decisions
@app_commands.command(name="analyze", description="Analyze a Letter League screenshot")
@app_commands.describe(screenshot="Attach a screenshot of your Letter League game")
async def analyze(
    self,
    interaction: discord.Interaction,
    screenshot: discord.Attachment,
) -> None:
    await interaction.response.defer(ephemeral=True)  # MUST be first

    state = self.bot.get_channel_state(interaction.channel_id)

    # Validate attachment
    img_bytes = await validate_and_read_attachment(screenshot)
    if img_bytes is None:
        await interaction.followup.send(
            embed=build_error_embed("Invalid file", "Please attach a PNG, JPEG, or WebP screenshot."),
        )
        return

    try:
        # Vision pipeline (async — no wrapper needed)
        board, rack = await extract_board_state(img_bytes, mode=state.mode)

        # Engine (sync CPU-bound — must use to_thread)
        moves = await asyncio.to_thread(find_all_moves, board, rack, self.bot.gaddag, state.mode)

        if not moves:
            await interaction.followup.send(
                embed=build_no_moves_embed(board, rack),
            )
            return

        # Difficulty selection (sync)
        top_moves = moves[:min(3, len(moves))]  # Top 3 by score
        embed = build_success_embed(top_moves, board)
        await interaction.followup.send(embed=embed)

    except VisNError as e:
        await interaction.followup.send(embed=build_visnError_embed(e))
    except Exception:
        logger.exception("Unexpected error in /analyze for channel {}", interaction.channel_id)
        await interaction.followup.send(
            embed=build_error_embed("Unexpected error", "Something went wrong. Please try again."),
        )
```

### Embed Color Constants
```python
# Source: discord.py Color class — discord.py docs + pythondiscord.com
SUCCESS_COLOR = discord.Color.brand_green()   # #57F287
WARNING_COLOR = discord.Color.gold()           # #F1C40F (yellow-gold)
ERROR_COLOR   = discord.Color.red()            # #ED4245
INFO_COLOR    = discord.Color.blurple()        # #5865F2
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `on_message` + prefix commands for attachments | `@app_commands.command` with `discord.Attachment` parameter | discord.py 2.0 (2022) | Native slash command UI, attachment picker, no message parsing |
| `discord.py` v1.x `Cog` with `commands.command` | `app_commands.command` + `commands.Cog` hybrid | discord.py 2.0 | Slash commands are first-class; prefix commands are legacy |
| Manual `asyncio.get_event_loop().run_in_executor()` | `await asyncio.to_thread(fn, *args)` | Python 3.9+ | Cleaner syntax, same behavior; `to_thread` is idiomatic Python 3.9+ |
| Global slash command sync (1 hour propagation) | Guild-specific sync for dev, global for prod | discord.py 2.x best practice | Dev iteration is instant; production commands propagate in 1 hour |

**Deprecated/outdated:**
- `discord.py` v1.x `Cog` with `on_message` + attachment parsing: use `app_commands.command` with `discord.Attachment` parameter instead.
- `commands.slash_command()` from discord-py-slash-command library: that was a separate library before discord.py added native support. Use `@app_commands.command` from discord.py 2.x directly.

---

## Open Questions

1. **GADDAG loading in setup_hook vs. lazy load**
   - What we know: GADDAG.from_wordlist() is slow (several seconds); `setup_hook` runs before READY so loading there delays bot startup but ensures it's ready when commands arrive.
   - What's unclear: Should the bot fail to start if GADDAG loading fails, or start and return an error on first `/analyze`?
   - Recommendation: Load in `setup_hook`, fail loudly on error — a bot that starts without its core resource is misleading. Log and raise if load fails.

2. **Engine statefulness in advisor mode**
   - What we know: `GameEngine` is stateful; advisor mode should never call `play_move()`. The vision pipeline returns a `Board` directly.
   - What's unclear: Should the bot hold a `GameEngine` (for its GADDAG and difficulty references) and only call `find_all_moves(board, rack, gaddag, mode)` directly, bypassing the engine's `board` attribute?
   - Recommendation: Hold a `GADDAG` and `DifficultyEngine` on the bot; call `find_all_moves()` directly with the vision-extracted board. Do not maintain a stateful `GameEngine` in advisor mode.

3. **Text-art board character set and width**
   - What we know: A 3-char-per-cell representation means 27 cols = 81 chars per row, which wraps in Discord. Need a windowed view.
   - What's unclear: Best window size and character set for clarity vs. compactness.
   - Recommendation (Claude's discretion): 3-char cells (`[A]` for placed, ` A ` for existing, ` · ` for empty), window = move extent ± 2 cells. Max ~12 columns shown. Fits in code block without wrap.

4. **Command sync strategy (dev vs. prod)**
   - What we know: `tree.sync()` in `setup_hook` works for dev. Global sync takes up to 1 hour. Guild sync is instant but scope-limited.
   - What's unclear: Is this a personal/single-guild bot or multi-guild?
   - Recommendation: Use guild-scoped sync during development (set `DISCORD_TEST_GUILD_ID` in `.env`). Document how to switch to global sync for deployment. The project is personal use so guild sync is fine permanently.

---

## Validation Architecture

> `workflow.nyquist_validation` is not set in `.planning/config.json` — the key is absent. Treating as false (not required). Skipping Validation Architecture section.

However, the following test gaps exist and the Wave 0 planner should note them:

- No `tests/bot/` directory exists yet — must be created
- `tests/conftest.py` has no Discord fixtures (no `discord.Interaction` mock, no `discord.Attachment` mock)
- discord.py provides no official test utilities; mocking is via `unittest.mock.AsyncMock`

For the bot, unit tests should cover:
- `channel_state.py`: `ChannelState` defaults, state isolation per channel
- `formatter.py`: embed color selection, field count, character limit compliance
- `cog.py`: validate + error path routing (mock VisNError codes → expected embed color/text)

The `/analyze` integration path (vision → engine → embed) is inherently manual-only in testing (requires real Discord credentials and a real screenshot). Automated tests mock the vision and engine calls.

---

## Sources

### Primary (HIGH confidence)
- [discord.py 2.7.1 — Interactions API Reference](https://discordpy.readthedocs.io/en/stable/interactions/api.html) — `defer()` with `ephemeral=True`, `followup.send()` behavior, `Attachment` type
- [discord.py deepwiki app_commands](https://deepwiki.com/Rapptz/discord.py/4.2-application-commands-(app_commands)) — `@app_commands.command`, `discord.Attachment` parameter, `app_commands.choices`, `app_commands.Range`, `setup_hook`/`tree.sync` pattern
- [pythondiscord.com — Discord.py 2.0 changes](https://www.pythondiscord.com/pages/guides/python-guides/app-commands/) — `setup_hook`, `tree.copy_global_to()`, `defer`/`edit_original_response()` pattern, guild vs. global sync
- `.planning/research/STACK.md` — discord.py 2.7.1, anthropic 0.86.0, versions verified March 2026
- `.planning/research/PITFALLS.md` — Pitfall 4 (interaction timeout), Pitfall 5 (event loop blocking), security section (attachment validation)
- `src/vision/__init__.py` — `extract_board_state()` async signature, `VisNError` error codes
- `src/engine/__init__.py` — `GameEngine` API, `find_moves()` sync, `GADDAG`, `DifficultyEngine`
- `.planning/phases/04-discord-advisor-mode/04-CONTEXT.md` — locked user decisions

### Secondary (MEDIUM confidence)
- [discord.py docs — Gateway Intents](https://discordpy.readthedocs.io/en/stable/intents.html) — slash-command-only bot does not require privileged intents (verified: no `members`, `presence`, or `message_content` intent needed)
- [WebSearch: `app_commands.Range` for 0-100 int](https://github.com/discord/discord-api-docs/discussions/3327) — `app_commands.Range[int, 0, 100]` syntax confirmed from multiple search results
- [WebSearch: Discord embed limits](https://www.pythondiscord.com/pages/guides/python-guides/discord-embed-limits/) — description 4096, field value 1024, total 6000 chars, 25 fields max

### Tertiary (LOW confidence)
- None — all critical claims verified with official docs or project's own code

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — discord.py 2.7.1 specified in project STACK.md; all APIs verified via official docs
- Architecture: HIGH — discord.py 2.x cog + `setup_hook` pattern is documented standard; `asyncio.to_thread` is Python 3.9+ stdlib
- Pitfalls: HIGH — all critical pitfalls (timeout, event loop blocking, statefulness) pre-documented in PITFALLS.md and verified from discord.py official FAQ
- Text-art board: MEDIUM — no prior art for 27x19 Letter League grid; windowed approach is reasoning from Discord's known character limits

**Research date:** 2026-03-24
**Valid until:** 2026-04-24 (discord.py 2.7.1 is stable; API patterns are unchanged since 2.0 release in 2022)
