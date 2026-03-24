# Architecture Research

**Domain:** Discord word game AI bot (Letter League — Scrabble variant)
**Researched:** 2026-03-24 (updated for v1.1 milestone)
**Confidence:** HIGH for integration patterns; MEDIUM for Discord Activity iframe interaction specifics (no public prior art for Playwright + Discord Activities)

---

## Standard Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        Discord Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │  /analyze    │  │  on_message  │  │  /autoplay /stop      │  │
│  │ slash command│  │ (attachment) │  │  /difficulty commands │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬────────────┘  │
└─────────┼─────────────────┼─────────────────────┼───────────────┘
          │                 │                      │
          ▼                 ▼                      ▼
┌──────────────────────────────────────────────────────────────────┐
│                      Orchestrator Layer                          │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                   Game Session Controller                 │    │
│  │   - Routes input to vision or automation pipeline        │    │
│  │   - Manages mode (advisor vs autonomous)                 │    │
│  │   - Holds difficulty setting and session state           │    │
│  └───────────┬───────────────────────────┬──────────────────┘    │
└──────────────┼───────────────────────────┼──────────────────────┘
               │                           │
     ┌─────────▼──────────┐   ┌────────────▼───────────┐
     │   Vision Pipeline  │   │  Browser Automation     │
     │  (Advisor Mode)    │   │  (Autonomous Mode)      │
     │                    │   │                         │
     │  Screenshot bytes  │   │  Playwright → Discord   │
     │      ↓             │   │  Activity iframe        │
     │  Claude Vision API │   │      ↓                  │
     │  (structured JSON) │   │  page.screenshot()      │
     │      ↓             │   │      ↓                  │
     │  BoardState        │   │  Claude Vision API      │
     └────────┬───────────┘   │      ↓                  │
              │               │  BoardState             │
              │               └────────────┬────────────┘
              │                            │
              └────────────┬───────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                  EXISTING: Word Engine Layer (v1.0)              │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  src/engine/GameEngine (PUBLIC API)                     │     │
│  │  - find_moves(rack) → list[Move]                        │     │
│  │  - best_move(rack) → Move | None                        │     │
│  │  - play_move(move) → None  [updates board state]        │     │
│  │  - is_valid_word(word) → bool                           │     │
│  └──────────┬───────────────────────┬──────────────────────┘     │
│             │                       │                             │
│  ┌──────────▼──────┐   ┌────────────▼─────────────────────┐     │
│  │  src/engine/    │   │  src/difficulty/DifficultyEngine  │     │
│  │  gaddag.py      │   │  - select_move(moves, difficulty) │     │
│  │  board.py       │   │    → Move | None                  │     │
│  │  moves.py       │   │  - freq: FrequencyIndex           │     │
│  │  scoring.py     │   └──────────────────────────────────┘     │
│  │  models.py      │                                             │
│  └─────────────────┘                                             │
└─────────────────────────────────────────────────────────────────┘
```

---

### Existing Code: What v1.0 Shipped

The engine package lives under `src/` (not `letter_league/` — the project uses `src/engine/` and `src/difficulty/`).

**`src/engine/` — Core word engine (zero I/O, pure Python)**
- `gaddag.py` — GADDAG dictionary; `GADDAG.from_wordlist(path, cache_path)`, pickle cache
- `board.py` — 27x19 grid, multiplier layout, `Board.place_tile()`, `Board.is_empty()`
- `moves.py` — `find_all_moves(board, rack, gaddag, mode) → list[Move]`
- `scoring.py` — Classic and Wild mode scoring
- `models.py` — `Move`, `TileUse`, `Cell`, `MultiplierType`, `ScoreBreakdown` dataclasses
- `tiles.py` — `TILE_VALUES`, `ALPHABET`
- `__init__.py` — `GameEngine` class (the public API)

**`src/difficulty/` — Difficulty system**
- `engine.py` — `DifficultyEngine.select_move(moves, difficulty)` — alpha-blended scoring
- `frequency.py` — `FrequencyIndex` wrapping wordfreq
- `__init__.py` — exports `DifficultyEngine`, `FrequencyIndex`

**`GameEngine` public API (from `src/engine/__init__.py`)**
```python
engine = GameEngine(wordlist_path, cache_path=Path('cache/gaddag.pkl'))
moves = engine.find_moves(['C', 'A', 'R', 'D', 'S', 'E', 'B'])
best = engine.best_move(['C', 'A', 'R', 'D', 'S', 'E', 'B'])
engine.play_move(best)   # mutates board state for subsequent turns
```

The engine is stateful across turns via `play_move()`. One `GameEngine` instance per game session.

---

### Component Responsibilities

| Component | Responsibility | Status |
|-----------|----------------|--------|
| `src/engine/GameEngine` | Stateful word engine: find moves, score, apply to board | BUILT (v1.0) |
| `src/difficulty/DifficultyEngine` | Select move at target difficulty via frequency blending | BUILT (v1.0) |
| `src/engine/models.{Move,Cell,Board,TileUse}` | Core data types shared across all components | BUILT (v1.0) |
| `src/vision/extractor.py` | Screenshot bytes → BoardState via Claude Vision API | TO BUILD (Phase 3) |
| `src/vision/models.py` | BoardState dataclass: grid, rack, scoring_mode | TO BUILD (Phase 3) |
| `src/vision/prompt.py` | System prompt + JSON schema for structured extraction | TO BUILD (Phase 3) |
| `bot/main.py` | discord.py Bot setup, Cog registration, event loop entry point | TO BUILD (Phase 4) |
| `bot/cogs/advisor.py` | Slash command handler, image attachment → vision → engine → reply | TO BUILD (Phase 4) |
| `bot/session.py` | Per-channel GameSession: difficulty, mode, GameEngine instance | TO BUILD (Phase 4) |
| `bot/cogs/autoplay.py` | /autoplay command, game loop orchestration | TO BUILD (Phase 6) |
| `src/automation/browser.py` | Playwright lifecycle: persistent context, reconnect | TO BUILD (Phase 5) |
| `src/automation/navigator.py` | Navigate Discord → voice channel → Activity iframe | TO BUILD (Phase 5) |
| `src/automation/placer.py` | Click rack tiles + board squares to place a word | TO BUILD (Phase 6) |

---

## Recommended Project Structure

The structure that fits the existing `src/` layout:

```
(project root)
├── src/
│   ├── __init__.py
│   ├── engine/                  # EXISTING — zero changes for v1.1
│   │   ├── __init__.py          # GameEngine public API
│   │   ├── gaddag.py
│   │   ├── board.py
│   │   ├── moves.py
│   │   ├── scoring.py
│   │   ├── models.py
│   │   └── tiles.py
│   ├── difficulty/              # EXISTING — zero changes for v1.1
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   └── frequency.py
│   ├── vision/                  # NEW — Phase 3
│   │   ├── __init__.py
│   │   ├── extractor.py         # screenshot bytes → BoardState (Claude Vision API)
│   │   ├── models.py            # BoardState dataclass (the contract)
│   │   └── prompt.py            # system prompt + Pydantic schema for structured output
│   └── automation/              # NEW — Phase 5
│       ├── __init__.py
│       ├── browser.py           # Playwright lifecycle, persistent context
│       ├── navigator.py         # Discord login, voice channel, Activity iframe
│       └── placer.py            # tile click sequences to place a word
│
├── bot/                         # NEW — Phase 4
│   ├── __init__.py
│   ├── main.py                  # Bot instantiation, Cog loading, bot.run()
│   ├── cogs/
│   │   ├── __init__.py
│   │   ├── advisor.py           # AdvisorCog: /analyze + on_message image attach
│   │   └── autoplay.py          # AutoplayCog: /autoplay, /stop, /difficulty
│   └── session.py               # GameSession: mode, difficulty, GameEngine instance
│
├── tests/                       # EXISTING — extend with new tests
│   ├── conftest.py
│   ├── test_board.py
│   ├── test_gaddag.py
│   ├── test_moves.py
│   ├── test_scoring.py
│   ├── test_engine.py
│   ├── test_difficulty.py
│   ├── test_vision.py           # NEW — Phase 3: mock VLM responses
│   └── test_session.py          # NEW — Phase 4: session state
│
├── data/
│   └── browser_state/           # NEW — Playwright persistent context (gitignored)
│
├── cache/
│   └── gaddag.pkl               # EXISTING — GADDAG pickle cache
│
├── config.py                    # NEW — ANTHROPIC_API_KEY, DISCORD_TOKEN, defaults
└── .env                         # NEW — secrets (gitignored)
```

### Structure Rationale

- **`src/engine/` and `src/difficulty/` are untouched.** The v1.0 engine becomes a dependency of the new layers, not a subject of modification. 94 passing tests protect it.
- **`src/vision/`** is isolated from Discord. `extractor.py` takes `bytes`, returns `BoardState`. Testable without a Discord connection.
- **`src/automation/`** is isolated from both Discord and the vision pipeline. It only takes `Move` objects as input for the `placer.py` layer.
- **`bot/`** is the only layer with discord.py imports. Cogs are thin translators: Discord event → domain call → formatted reply.
- **`bot/session.py`** holds the `GameEngine` instance per channel. This is where the stateful engine lives across turns.

---

## Architectural Patterns

### Pattern 1: Thin Cog, Fat Engine

**What:** Discord Cogs contain only event wiring and Discord-specific formatting. All game logic lives in `src/engine/`, `src/vision/`, and `src/automation/`, which have zero discord.py imports.

**When to use:** Always. This is the only correct structure.

**Trade-offs:** Slightly more indirection at call sites. The payoff is that the entire engine stack is testable without a Discord connection or live browser.

**Example:**
```python
# bot/cogs/advisor.py
import discord
from discord import app_commands
from discord.ext import commands
from src.vision.extractor import extract_board_state
from src.vision.models import BoardState
from src.engine import GameEngine
from src.difficulty import DifficultyEngine
from bot.session import GameSession

class AdvisorCog(commands.Cog):
    def __init__(self, bot: commands.Bot, sessions: dict[int, GameSession]):
        self.bot = bot
        self.sessions = sessions  # keyed by channel_id

    @app_commands.command(name="analyze", description="Analyze a board screenshot")
    async def analyze(
        self,
        interaction: discord.Interaction,
        screenshot: discord.Attachment,
    ) -> None:
        await interaction.response.defer()  # avoid timeout while processing
        image_bytes = await screenshot.read()
        channel_id = interaction.channel_id
        session = self.sessions.setdefault(channel_id, GameSession())

        board_state = await extract_board_state(image_bytes, session.scoring_mode)
        session.sync_board(board_state)  # apply extracted board to engine

        moves = session.engine.find_moves(board_state.rack)
        chosen = session.difficulty_engine.select_move(moves, session.difficulty)
        await interaction.followup.send(format_move_response(chosen, moves))
```

### Pattern 2: BoardState as the Contract Between Vision and Engine

**What:** `BoardState` is a new dataclass in `src/vision/models.py` that the vision pipeline produces and the engine consumes. It must map cleanly to the existing `Board` and `Move` types.

**When to use:** Anywhere vision output is handed to the engine or automation layer.

**The existing engine already has `Board` and `Cell` in `src/engine/models.py`. The new `BoardState` is vision-side only — it carries what the VLM extracted. After extraction, the bot syncs this into the `GameEngine.board` object.**

**Example:**
```python
# src/vision/models.py
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class ExtractedCell:
    """Single cell as returned by vision extraction."""
    letter: Optional[str]        # None = empty square
    multiplier: Optional[str]    # "DL", "TL", "DW", "TW", or None
    is_blank: bool               # True if blank tile assigned this letter

@dataclass(frozen=True)
class BoardState:
    """Vision pipeline output — the contract between VLM and engine."""
    grid: tuple[tuple[ExtractedCell, ...], ...]   # [row][col]
    rack: tuple[str, ...]                          # player tiles; "?" = blank
    scoring_mode: str                              # "wild" | "classic"
    confidence: float                              # 0.0–1.0
    turn_number: Optional[int] = None
```

### Pattern 3: Claude Vision API with Structured Output

**What:** Use `anthropic.Anthropic().messages.parse()` with a Pydantic model to get guaranteed-schema JSON from the screenshot. Image sent as base64 (discord attachment bytes → base64 encode in extractor).

**When to use:** Phase 3 vision pipeline. Do not use `client.messages.create()` + manual JSON parsing — `parse()` gives type-safe output and automatic schema validation.

**Confidence:** HIGH — verified against official Anthropic docs (2026-03-24).

**Key constraints from official docs:**
- Max image size: 5 MB via API
- Supported formats: JPEG, PNG, GIF, WebP
- Optimal resolution: ≤1568px on longest edge, ≤1.15 megapixels
- Image tokens ≈ (width × height) / 750; ~1,600 tokens for a 1092×1092 screenshot
- `parse()` uses `output_format=PydanticModel` parameter

**Example:**
```python
# src/vision/extractor.py
import base64
import anthropic
from pydantic import BaseModel
from src.vision.models import BoardState
from src.vision.prompt import BOARD_EXTRACTION_PROMPT

class _VisionResponse(BaseModel):
    """Pydantic schema that Claude will conform its response to."""
    grid: list[list[dict]]   # [{letter, multiplier, is_blank}]
    rack: list[str]
    scoring_mode: str        # "wild" | "classic"
    confidence: float

_client = anthropic.Anthropic()  # loaded once at module import

async def extract_board_state(image_bytes: bytes, hint_mode: str = "classic") -> BoardState:
    """Send screenshot to Claude Vision API, return structured BoardState."""
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    # Determine media type from bytes header (PNG: b'\x89PNG', JPEG: b'\xff\xd8')
    media_type = "image/png" if image_bytes[:4] == b'\x89PNG' else "image/jpeg"

    response = _client.messages.parse(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {"type": "base64", "media_type": media_type, "data": b64},
                    },
                    {"type": "text", "text": BOARD_EXTRACTION_PROMPT},
                ],
            }
        ],
        output_format=_VisionResponse,
    )
    raw = response.parsed_output
    return _build_board_state(raw, hint_mode)
```

**Note on async:** The `anthropic` SDK's `messages.parse()` is synchronous by default. For use inside discord.py's async event loop, either use `anthropic.AsyncAnthropic()` client or wrap with `asyncio.get_event_loop().run_in_executor(None, ...)`. Use `AsyncAnthropic` — cleaner.

### Pattern 4: discord.py Cog with Privileged Message Content Intent

**What:** The bot must declare `message_content` as a privileged intent to read image attachments in DMs and non-slash interactions. Slash command attachments (`discord.Attachment` parameter) do NOT require this intent.

**When to use:** Bot startup in `bot/main.py`. Also requires enabling the intent in Discord Developer Portal.

**Confidence:** HIGH — verified against discord.py official docs and Discord developer support articles (2026-03-24).

**Example:**
```python
# bot/main.py
import discord
from discord.ext import commands
from bot.cogs.advisor import AdvisorCog
from bot.cogs.autoplay import AutoplayCog

intents = discord.Intents.default()
intents.message_content = True   # required for on_message attachment reading

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    sessions = {}
    await bot.add_cog(AdvisorCog(bot, sessions))
    await bot.add_cog(AutoplayCog(bot, sessions))
    await bot.tree.sync()   # register slash commands with Discord
    print(f"Logged in as {bot.user}")

bot.run(DISCORD_TOKEN)
```

### Pattern 5: Persistent Playwright Context Sharing the discord.py Event Loop

**What:** Playwright's async API (`playwright.async_api`) shares discord.py's asyncio event loop. The persistent context is launched once on `/autoplay` and reused for all turns. On Windows, ensure `ProactorEventLoop` is used (Python 3.11 default on Windows).

**When to use:** Phase 5 browser automation foundation. Never use `playwright.sync_api` inside async discord.py code — it raises `RuntimeError: This event loop is already running`.

**Confidence:** HIGH — Playwright async API and discord.py both use asyncio. Verified against Playwright Python docs (2026-03-24).

**Example:**
```python
# src/automation/browser.py
from playwright.async_api import async_playwright, BrowserContext, Playwright

_playwright: Playwright | None = None
_context: BrowserContext | None = None

async def get_context(user_data_dir: str) -> BrowserContext:
    """Launch or reattach persistent Chromium context. Call once per session."""
    global _playwright, _context
    if _context is not None:
        return _context
    _playwright = await async_playwright().start()
    _context = await _playwright.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,          # Activities may not render in headless; test first
        args=["--disable-blink-features=AutomationControlled"],
        viewport={"width": 1280, "height": 900},
    )
    return _context

async def close_context() -> None:
    global _playwright, _context
    if _context:
        await _context.close()
        _context = None
    if _playwright:
        await _playwright.stop()
        _playwright = None

async def capture_screenshot(page) -> bytes:
    """Capture full page screenshot as PNG bytes."""
    return await page.screenshot(full_page=False)
```

### Pattern 6: Discord Activity iframe Navigation

**What:** Discord Activities run as embedded iframes inside the Discord desktop/web client. Playwright can navigate to Discord, click into a voice channel, and then use `page.frame_locator()` to address the Activity iframe content.

**When to use:** Phase 5 navigator. This is the highest-uncertainty area — no public prior art confirms exact selectors or iframe structure.

**Confidence:** MEDIUM — Playwright iframe chaining is well-documented. Discord Activity iframe specifics are unverified without live testing.

**Key consideration:** Discord Activities run under a restrictive Content Security Policy with all requests routed through `<app_id>.discordsays.com`. The iframe content is a web app, so standard Playwright iframe interaction applies — but the exact Activity URL, iframe selector, and turn-detection DOM signals require empirical testing against a live Letter League game.

**Example (speculative — requires validation in Phase 5):**
```python
# src/automation/navigator.py
async def navigate_to_activity(page, voice_channel_url: str):
    """Navigate browser to Discord voice channel and find Letter League Activity."""
    await page.goto("https://discord.com/app")
    # Wait for Discord to load (check for sidebar or known element)
    await page.wait_for_selector('[class*="sidebar"]', timeout=15_000)
    # Navigate to specific voice channel
    await page.goto(voice_channel_url)
    # Click "Open Activity" button (selector needs empirical validation)
    await page.click('[aria-label="Letter League"]')  # placeholder
    # Access the Activity iframe content
    activity_frame = page.frame_locator('iframe[src*="discordsays.com"]')
    return activity_frame
```

### Pattern 7: GameSession as Per-Channel State Container

**What:** One `GameSession` per Discord channel holds the `GameEngine` instance (which tracks board state), difficulty setting, and mode. Multiple users can interact with the same session (same channel = same game).

**When to use:** Advisor mode from the first turn. Session must persist across multiple `/analyze` calls in a channel.

**Example:**
```python
# bot/session.py
from dataclasses import dataclass, field
from pathlib import Path
from src.engine import GameEngine
from src.difficulty import DifficultyEngine

WORDLIST_PATH = Path("data/wordnik_wordlist.txt")
GADDAG_CACHE = Path("cache/gaddag.pkl")

@dataclass
class GameSession:
    """Owns engine state for one channel's game."""
    difficulty: int = 80              # 0-100
    scoring_mode: str = "classic"     # "classic" | "wild"
    engine: GameEngine = field(default_factory=lambda: GameEngine(
        WORDLIST_PATH,
        cache_path=GADDAG_CACHE,
    ))
    difficulty_engine: DifficultyEngine = field(
        default_factory=DifficultyEngine
    )

    def sync_board(self, board_state) -> None:
        """Apply vision-extracted board state to the engine's Board.

        Rebuilds the engine's internal board from the extracted grid.
        Called after each vision extraction to keep engine in sync.
        """
        # Reset board and replay all placed tiles from extracted grid
        self.engine.board = _rebuild_board(board_state, self.scoring_mode)
```

---

## Data Flow

### Advisor Mode Flow (Phase 3 + 4)

```
User: /analyze [screenshot attachment]
    ↓
AdvisorCog.analyze(interaction, screenshot: discord.Attachment)
    ↓
await interaction.response.defer()        [prevent 3-sec timeout]
    ↓
image_bytes = await screenshot.read()     [discord.Attachment.read()]
    ↓
board_state = await extract_board_state(image_bytes)
    │  [src/vision/extractor.py]
    │  1. base64-encode image_bytes
    │  2. POST to Claude Vision API (messages.parse, Pydantic schema)
    │  3. Parse structured JSON → BoardState
    ↓
session.sync_board(board_state)           [bot/session.py]
    │  Rebuilds engine.board from extracted grid
    ↓
moves = session.engine.find_moves(board_state.rack)
    │  [src/engine/__init__.py — GameEngine.find_moves()]
    │  Returns list[Move] sorted by score descending
    ↓
chosen = session.difficulty_engine.select_move(moves, session.difficulty)
    │  [src/difficulty/engine.py — DifficultyEngine.select_move()]
    ↓
await interaction.followup.send(format_move_response(chosen))
    [Discord reply with word, position, score]
```

### Autonomous Mode Flow (Phase 5 + 6, per turn)

```
User: /autoplay [voice-channel-url]
    ↓
AutoplayCog.autoplay(interaction)
    ↓
context = await get_context(USER_DATA_DIR)   [src/automation/browser.py]
    ↓
page = context.pages[0] or await context.new_page()
    ↓
activity_frame = await navigate_to_activity(page, voice_channel_url)
    │  [src/automation/navigator.py]
    │  Discord → voice channel → Letter League iframe
    ↓
[Game loop — runs via discord.ext.tasks background task]
    │
    ├── screenshot_bytes = await capture_screenshot(page)
    │   [src/automation/browser.py]
    │
    ├── board_state = await extract_board_state(screenshot_bytes)
    │   [src/vision/extractor.py — same as advisor mode]
    │
    ├── moves = session.engine.find_moves(board_state.rack)
    │   chosen = session.difficulty_engine.select_move(moves, session.difficulty)
    │
    ├── await place_word(activity_frame, chosen, board_state)
    │   [src/automation/placer.py]
    │   1. Click each rack tile letter
    │   2. Click target board square(s)
    │   3. Click confirm/submit button
    │
    └── await wait_for_next_turn(activity_frame)
        [poll for turn indicator change, timeout if stuck]
```

### Component Communication (async boundaries)

```
discord.py event loop (asyncio)
    │
    ├── bot/cogs/ (async Cog methods)
    │       │
    │       ├── src/vision/ (async) — AsyncAnthropic HTTP call
    │       │     extractor.extract_board_state() → awaited
    │       │
    │       ├── src/engine/ (SYNC — pure CPU, no I/O)
    │       │     GameEngine.find_moves() — called directly
    │       │     DifficultyEngine.select_move() — called directly
    │       │     Note: Phase 1 testing shows <10ms per call for
    │       │     27×19 board. run_in_executor NOT needed.
    │       │
    │       └── src/automation/ (async) — Playwright awaited calls
    │             browser.get_context() → awaited
    │             placer.place_word() → awaited
    │
    └── discord.ext.tasks @tasks.loop
          Background game loop for autonomous mode.
          Avoids blocking the main event loop.
```

---

## New vs Modified Components

### New Components (build from scratch)

| Component | Phase | Depends On |
|-----------|-------|------------|
| `src/vision/models.py` | 3 | nothing |
| `src/vision/prompt.py` | 3 | nothing |
| `src/vision/extractor.py` | 3 | `src/vision/models.py`, `anthropic` SDK |
| `bot/session.py` | 4 | `src/engine/GameEngine`, `src/difficulty/DifficultyEngine` |
| `bot/main.py` | 4 | `discord.py`, `bot/cogs/` |
| `bot/cogs/advisor.py` | 4 | `src/vision/extractor.py`, `bot/session.py` |
| `src/automation/browser.py` | 5 | `playwright.async_api` |
| `src/automation/navigator.py` | 5 | `src/automation/browser.py` |
| `src/automation/placer.py` | 6 | `src/automation/navigator.py`, `src/engine/models.Move` |
| `bot/cogs/autoplay.py` | 6 | `src/automation/`, `bot/session.py` |

### Modified Components (existing code that must change)

| Component | Change Required | Risk |
|-----------|----------------|------|
| `src/engine/board.py` | May need a `Board.reset()` or `Board.from_grid()` factory to allow vision to rebuild board state | LOW — additive only |
| `src/engine/__init__.py` (GameEngine) | May need `engine.board = new_board` to allow session sync from extracted BoardState | LOW — board is already a public attribute |
| `tests/conftest.py` | Add fixtures for mock VLM responses, test screenshots | LOW |

### Existing Components That Need No Changes

- `src/engine/gaddag.py` — zero changes
- `src/engine/moves.py` — zero changes
- `src/engine/scoring.py` — zero changes
- `src/engine/models.py` — zero changes (BoardState uses existing Cell/MultiplierType)
- `src/engine/tiles.py` — zero changes
- `src/difficulty/engine.py` — zero changes
- `src/difficulty/frequency.py` — zero changes

---

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Claude Vision API (Anthropic) | `anthropic.AsyncAnthropic().messages.parse()` with Pydantic model + base64 image | Use `AsyncAnthropic` (not sync) for discord.py compatibility. Model: `claude-opus-4-6`. Max 5MB image, 1568px. `parse()` returns typed `parsed_output`. |
| Discord Gateway | `discord.py` WebSocket; slash commands via `app_commands`, images via `Attachment.read()` | Privileged `message_content` intent required for non-slash DMs. Enable in Dev Portal + code. Slash command attachments bypass this requirement. |
| Playwright / Chromium | `playwright.async_api.async_playwright()` with `launch_persistent_context(user_data_dir)` | Must use async API inside discord.py. `headless=False` likely required for Discord Activity rendering. Windows: ProactorEventLoop (Python 3.11 default). |

### Internal Boundaries

| Boundary | Communication | Interface |
|----------|---------------|-----------|
| `vision/extractor.py` → `engine/GameEngine` | `BoardState.grid` + `BoardState.rack` used to reset engine state | `session.sync_board(board_state)` — rebuilds `engine.board` |
| `bot/cogs/advisor.py` → `src/vision/` | Passes `bytes` in, receives `BoardState` out | `await extract_board_state(image_bytes)` |
| `bot/cogs/advisor.py` → `src/engine/` | Calls `engine.find_moves()`, `difficulty.select_move()` synchronously | Direct call; engine is sync |
| `bot/cogs/autoplay.py` → `src/automation/` | Passes `Move` to placer; receives completion signal | `await place_word(frame, move, board_state)` |
| `src/automation/browser.py` → `src/vision/` | Passes `bytes` from `page.screenshot()` | Same path as advisor mode |
| `src/automation/placer.py` → `src/engine/models` | Reads `Move.tiles_used` to derive click coordinates | `Move.rack_tiles_consumed()` returns `list[TileUse]` with row/col |

---

## Suggested Build Order

Dependencies between components dictate strict ordering. Earlier steps protect later steps.

**Phase 3: Vision Pipeline (build first — highest risk)**

1. `src/vision/models.py` — `ExtractedCell`, `BoardState` dataclasses. No dependencies.
2. `src/vision/prompt.py` — System prompt and Pydantic schema. Iterate until VLM returns clean JSON from real screenshots.
3. `src/vision/extractor.py` — Wire up `AsyncAnthropic().messages.parse()`. Test: real Letter League screenshots → correct BoardState.
4. Validate: board sync path — `BoardState` → `GameEngine.board` → `find_moves()` returns expected moves.

**Phase 4: Discord Advisor Mode (build second — closes the MVP loop)**

5. `bot/session.py` — `GameSession` with `GameEngine` + `DifficultyEngine`. Test: session state persists across calls.
6. `bot/main.py` — `discord.py` bot with intents. Run locally, confirm bot comes online.
7. `bot/cogs/advisor.py` — Wire `/analyze` slash command. Test: end-to-end with real screenshot.
8. Manual integration test: user sends screenshot, bot replies with move.

**Phase 5: Browser Automation Foundation (build third — isolated engineering spike)**

9. `src/automation/browser.py` — Playwright persistent context. Test: manual launch, Discord login, persist state to disk.
10. `src/automation/navigator.py` — Navigate to Discord app, find voice channel, capture Activity iframe. This is the highest-uncertainty step — expect empirical iteration on selectors.
11. Validation: capture non-blank screenshot of Letter League game canvas from within iframe.

**Phase 6: Autonomous Play (build last — depends on everything)**

12. `src/automation/placer.py` — Click rack tiles and board squares. Requires coordinate mapping from `Move.tiles_used` row/col to pixel positions.
13. `bot/cogs/autoplay.py` — `discord.ext.tasks` background loop. Wire `/autoplay`, `/stop`, `/difficulty`.
14. Full autonomous integration test: bot joins game, detects turn, places word, submits.

---

## Scaling Considerations

This is a single-server bot. Scaling is not the primary concern.

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 1 server, 1 game | Default: one `GameSession`, one Playwright context, one process |
| 1 server, multiple concurrent games | Per-channel `GameSession` dict (already designed this way); separate Playwright pages per game (one context, multiple pages); VLM calls are independent |
| Multiple servers | Not in scope. Would require per-guild session store and likely a worker queue for VLM rate limits. |

### First Bottleneck

Claude Vision API latency (typically 2–6 seconds per screenshot call). This is acceptable for a turn-based game with 60–120 second turns. Do not try to optimize — this is an external API.

### Second Bottleneck

Playwright turn-detection polling in autonomous mode. Poll at a fixed interval (2–5 seconds) rather than continuously, to avoid Discord rate-limiting and unnecessary CPU burn.

---

## Anti-Patterns

### Anti-Pattern 1: Putting Game Logic in Discord Cogs

**What people do:** Write board parsing, move generation, and scoring directly inside Cog methods.

**Why it's wrong:** Untestable without a live Discord connection. The 94-test engine suite becomes unreachable.

**Do this instead:** Cogs call `src/engine/` and `src/vision/` functions. Zero discord.py imports in those packages.

### Anti-Pattern 2: Using Playwright Sync API Inside discord.py

**What people do:** `from playwright.sync_api import sync_playwright` then call `page.screenshot()` from an async handler.

**Why it's wrong:** Playwright's sync API internally manages its own event loop. Inside discord.py's asyncio loop this raises `RuntimeError: This event loop is already running`.

**Do this instead:** Use `from playwright.async_api import async_playwright`. All Playwright calls become `await`-able and share the bot's event loop cleanly.

### Anti-Pattern 3: Re-launching the Browser Every Turn

**What people do:** Start a new Playwright browser, navigate to Discord, find the game, take screenshot, close browser — every turn.

**Why it's wrong:** Browser launch takes 2–5 seconds. Discord navigation takes 3–8 seconds. Total overhead of 10+ seconds per turn is unacceptable and risks triggering Discord's anti-automation detection.

**Do this instead:** `launch_persistent_context(user_data_dir)` once on `/autoplay`. Keep the browser alive for the duration of the game session. Close only on `/stop` or game end.

### Anti-Pattern 4: Using sync `anthropic.Anthropic()` in async discord.py handlers

**What people do:** Instantiate `anthropic.Anthropic()` and call `client.messages.create()` directly inside an async Cog method without wrapping.

**Why it's wrong:** The sync Anthropic SDK client blocks the asyncio event loop during the HTTP request (typically 2–6 seconds). Discord events pile up and the bot appears frozen.

**Do this instead:** Use `anthropic.AsyncAnthropic()` and `await client.messages.parse(...)`. The async client integrates with asyncio natively.

### Anti-Pattern 5: Treating Vision Output as Ground Truth Without Validation

**What people do:** Take the VLM-parsed `BoardState` directly and call `find_moves()` without sanity-checking.

**Why it's wrong:** Claude Vision will occasionally hallucinate tiles, misread letters, or miss multiplier squares. The engine will generate legal-looking moves from wrong state. In autonomous mode, the bot will attempt to place non-existent tiles and error.

**Do this instead:** Validate `BoardState` after parsing: rack length 1–7, letters in `A-Z` or `?`, grid dimensions within expected bounds (27×19 max), `confidence >= 0.7`. Log and skip turns where validation fails. Report failures to Discord as a "couldn't read board" message rather than silently acting on bad state.

### Anti-Pattern 6: Creating a New GameEngine Per Turn

**What people do:** Instantiate `GameEngine(wordlist_path)` for every `/analyze` call.

**Why it's wrong:** `GameEngine.__init__` loads and builds the GADDAG from the wordlist (or unpickles it). This takes 0.5–2 seconds on first call and loads the GADDAG into memory again unnecessarily.

**Do this instead:** One `GameEngine` per `GameSession` per channel. The `GameSession` is stored in the `sessions` dict in the Cog, keyed by `channel_id`. The GADDAG is built once at bot startup and reused across all turns.

---

## Sources

- Claude Vision API official docs (verified 2026-03-24): https://platform.claude.com/docs/en/build-with-claude/vision
- Claude Structured Outputs official docs (verified 2026-03-24): https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Anthropic Python SDK `messages.parse()` with Pydantic: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- discord.py Cogs documentation: https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
- discord.py Privileged Intents (message_content): https://support-dev.discord.com/hc/en-us/articles/6205754771351-How-do-I-get-Privileged-Intents-for-my-bot
- discord.py background tasks (`discord.ext.tasks`): https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html
- Playwright Python async API: https://playwright.dev/python/docs/api/class-playwright
- Playwright persistent context (`launch_persistent_context`): https://playwright.dev/python/docs/api/class-browsertype
- Playwright iframe handling (`frame_locator`): https://playwright.dev/python/docs/frames
- Discord Activities architecture: https://docs.discord.com/developers/activities/overview
- Playwright async + discord.py event loop: asyncio `run_coroutine_threadsafe` pattern — discord.py FAQ: https://discordpy.readthedocs.io/en/stable/faq.html

---

*Architecture research for: Discord word game AI bot (Letter League) — v1.1 Vision + Discord Integration*
*Researched: 2026-03-24*
