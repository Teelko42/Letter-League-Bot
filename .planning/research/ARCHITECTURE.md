# Architecture Research

**Domain:** Browser automation + autonomous game play integrated into existing async Discord bot
**Researched:** 2026-03-24
**Confidence:** HIGH (event loop mechanics, Playwright async API) / MEDIUM (Discord Activity iframe selectors — require empirical validation)

---

## Context: Existing Architecture

The v1.1 codebase is a single-process Python 3.10 application running one asyncio event loop owned by discord.py. All heavy work is already handled correctly:

- CPU-bound engine calls use `asyncio.to_thread()`
- Vision API calls use `AsyncAnthropic` (native coroutines)
- `setup_hook` loads GADDAG before the READY event fires
- Per-channel state lives in `ChannelStore` on the `LetterLeagueBot` instance

The v1.2 milestone adds Playwright into this same process and event loop. The core architectural question is whether `async_playwright` can share discord.py's event loop.

**Answer: Yes.** On Python 3.10 + Windows with ProactorEventLoop (the default since Python 3.8), `async_playwright` runs as native asyncio coroutines and shares the event loop cleanly with discord.py. The ProactorEventLoop incompatibility with discord.py was a Python 3.6 bug, fixed in Python 3.7. Python 3.10 is unaffected. (HIGH confidence — verified against Playwright docs and discord.py issue #859.)

---

## System Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                     Single asyncio Event Loop                         │
│                (discord.py + async_playwright share it)               │
│                                                                        │
│  ┌─────────────────┐   ┌──────────────────────┐   ┌────────────────┐ │
│  │   AdvisorCog    │   │    AutonomousCog      │   │LetterLeagueBotI│ │
│  │  /analyze       │   │  /autoplay start|stop │   │  setup_hook    │ │
│  │  /setdifficulty │   │  /autoplay status     │   │  close()       │ │
│  │  /setmode       │   │                       │   └────────────────┘ │
│  └────────┬────────┘   └──────────┬────────────┘                      │
│           │                       │                                    │
│  ┌────────▼───────────────────────▼──────────────────────────────┐    │
│  │               Shared Resources (attributes on bot)            │    │
│  │   gaddag   difficulty_engine   channel_store   browser_manager│    │
│  └────────┬──────────────────────────────┬────────────────────────┘   │
│           │                              │                             │
│  ┌────────▼───────────┐      ┌──────────▼───────────────────────┐    │
│  │   Vision Pipeline  │      │         BrowserManager            │    │
│  │   src/vision/      │      │         src/browser/manager.py    │    │
│  │                    │      │  Playwright async_playwright       │    │
│  │  preprocess_screen │      │  launch_persistent_context        │    │
│  │  call_vision_api   │      │  (one context per bot lifetime)   │    │
│  │  validate_extract  │      └──────────┬────────────────────────┘   │
│  └────────┬───────────┘                 │                             │
│           │                   ┌─────────▼──────────────────────┐     │
│  ┌────────▼───────────┐      │           GameLoop              │     │
│  │    Engine Layer    │      │    src/browser/game_loop.py      │     │
│  │    src/engine/     │◄─────│  @tasks.loop(seconds=4)         │     │
│  │  find_all_moves    │      │  turn detect → screenshot        │     │
│  │  select_move       │      │  → vision → engine → place       │     │
│  └────────────────────┘      └──────────┬──────────────────────┘     │
│                                          │                             │
│                               ┌──────────▼──────────────────────┐    │
│                               │          TilePlacer              │    │
│                               │   src/browser/tile_placer.py     │    │
│                               │  Move → pixel clicks on canvas   │    │
│                               └──────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
           │                                    │
 ┌─────────▼──────────┐             ┌──────────▼──────────────┐
 │  Anthropic API     │             │    Chromium Browser      │
 │  Claude Vision     │             │  Discord web client      │
 │  (AsyncAnthropic)  │             │  Letter League iframe    │
 └────────────────────┘             │  canvas element          │
                                    └─────────────────────────-┘
```

---

## New Components

### 1. BrowserManager (`src/browser/manager.py`)

**Responsibility:** Own the entire Playwright lifecycle. One `Playwright` instance, one persistent browser context, for the full lifetime of the bot.

**Why persistent context:** `launch_persistent_context(user_data_dir=...)` stores cookies, localStorage, and IndexedDB across bot restarts. Discord login survives restarts without re-authenticating. (HIGH confidence — Playwright official docs.)

```python
from pathlib import Path
from playwright.async_api import async_playwright, Playwright, BrowserContext

class BrowserManager:
    def __init__(self, user_data_dir: Path) -> None:
        self._user_data_dir = user_data_dir
        self._pw: Playwright | None = None
        self._context: BrowserContext | None = None

    async def start(self) -> None:
        """Called from bot.setup_hook — starts Playwright and browser."""
        self._pw = await async_playwright().start()
        self._context = await self._pw.chromium.launch_persistent_context(
            user_data_dir=str(self._user_data_dir),
            headless=False,  # Discord detects headless Chromium; must stay headed
            args=["--disable-blink-features=AutomationControlled"],
            viewport={"width": 1280, "height": 900},
        )

    async def close(self) -> None:
        """Called from bot.close() override — tears down browser and Playwright."""
        if self._context:
            await self._context.close()
        if self._pw:
            await self._pw.stop()

    @property
    def context(self) -> BrowserContext:
        assert self._context is not None, "BrowserManager not started"
        return self._context
```

**Key detail:** `async_playwright().start()` (not the `async with` context manager form) is used so the instance persists beyond a single block. `stop()` is called explicitly in teardown.

**Wiring into bot.py:**
```python
# In LetterLeagueBot.setup_hook():
self.browser_manager = BrowserManager(Path("data/browser_profile"))
await self.browser_manager.start()

# In LetterLeagueBot.close() override:
await self.browser_manager.close()
await super().close()
```

---

### 2. DiscordNavigator (`src/browser/navigator.py`)

**Responsibility:** Navigate the Discord web client to a specific voice channel and locate the Letter League Activity iframe. Stateless — takes a `BrowserContext`, returns `(Page, Frame)`.

```python
from playwright.async_api import BrowserContext, Page, Frame

async def navigate_to_activity(
    context: BrowserContext,
    guild_id: str,
    channel_id: str,
) -> tuple[Page, Frame]:
    """Navigate to the Letter League activity iframe.

    Returns (page, frame) where frame is the Letter League game iframe.
    Raises NavigationError if the iframe is not found within timeout.
    """
    page = await context.new_page()
    url = f"https://discord.com/channels/{guild_id}/{channel_id}"
    await page.goto(url, wait_until="networkidle")
    frame = await _wait_for_activity_frame(page)
    return page, frame

async def _wait_for_activity_frame(page: Page) -> Frame:
    """Poll page.frames until a frame whose URL matches the activity pattern."""
    # Discord Activities are iframes; src URL contains the activity CDN domain.
    # Exact URL pattern requires empirical validation during implementation.
    async def find_frame():
        for frame in page.frames:
            if "letter" in frame.url.lower() or "discordsays.com" in frame.url:
                return frame
        return None

    for _ in range(30):  # 30 * 1s = 30 second timeout
        frame = await find_frame()
        if frame:
            return frame
        await page.wait_for_timeout(1000)

    raise NavigationError("Letter League Activity iframe not found within 30s")
```

**Canvas screenshot from iframe:**
```python
# Frame.locator("canvas") finds the game canvas within the iframe
canvas = frame.locator("canvas")
screenshot_bytes = await canvas.screenshot()
# Returns PNG bytes — compatible with existing preprocess_screenshot() unchanged
```

(MEDIUM confidence on exact selectors — Discord Activity iframe URLs and canvas selectors require empirical discovery during Phase 1 of the build.)

---

### 3. GameLoop (`src/browser/game_loop.py`)

**Responsibility:** Poll for the bot's turn, capture a screenshot, run the full existing pipeline (vision → engine → difficulty), then place tiles. Runs as a `discord.ext.tasks` loop.

**Turn detection strategy:** Capture a canvas screenshot every 4 seconds. The simplest reliable approach is pixel-hash comparison — if the screenshot differs significantly from the last one, the board state changed (likely a new turn). A more targeted approach checks whether the tile rack area has changed (rack tiles disappear when it is the other player's turn in some implementations).

```python
import asyncio
from discord.ext import tasks
from loguru import logger
from src.vision import extract_board_state
from src.engine.moves import find_all_moves
from src.browser.tile_placer import place_move

class GameLoop:
    def __init__(self, bot) -> None:
        self.bot = bot
        self._frame = None
        self._channel_id: int | None = None
        self._last_screenshot_hash: int | None = None

    @tasks.loop(seconds=4.0)
    async def poll_turn(self) -> None:
        if self._frame is None:
            return
        screenshot_bytes = await self._capture_canvas()
        current_hash = hash(screenshot_bytes)

        if current_hash == self._last_screenshot_hash:
            return  # no change — not our turn yet

        self._last_screenshot_hash = current_hash

        if await self._is_my_turn(screenshot_bytes):
            await self._execute_turn(screenshot_bytes)

    @poll_turn.before_loop
    async def before_poll(self) -> None:
        await self.bot.wait_until_ready()

    @poll_turn.after_loop
    async def after_poll(self) -> None:
        logger.info(
            "Game loop stopped — cancelled={}",
            self.poll_turn.is_being_cancelled(),
        )

    async def _capture_canvas(self) -> bytes:
        canvas = self._frame.locator("canvas")
        return await canvas.screenshot()

    async def _execute_turn(self, screenshot_bytes: bytes) -> None:
        state = self.bot.channel_store.get(self._channel_id)

        # Step 1: Vision pipeline (async — awaited directly on event loop)
        board, rack = await extract_board_state(screenshot_bytes, mode=state.mode)

        # Step 2: Engine (CPU-bound — must use thread)
        moves = await asyncio.to_thread(
            find_all_moves, board, rack, self.bot.gaddag, state.mode
        )
        if not moves:
            logger.info("No valid moves found — passing turn")
            return

        # Step 3: Difficulty selection (CPU-bound — thread)
        move = await asyncio.to_thread(
            self.bot.difficulty_engine.select_move, moves, state.difficulty
        )

        # Step 4: Place tiles (Playwright — awaited on event loop, NOT in thread)
        canvas_bbox = await self._frame.locator("canvas").bounding_box()
        await place_move(self._frame, move, canvas_bbox)
```

---

### 4. TilePlacer (`src/browser/tile_placer.py`)

**Responsibility:** Translate a `Move` object into Playwright mouse clicks. Owns the coordinate mapping from game-grid positions to canvas pixel coordinates.

**Click pattern:**
1. Click the tile in the rack (by its index position in the rack row)
2. Click the target board cell (by computed row/col pixel position)
3. Repeat for each tile in the word
4. Click the confirm/submit button

```python
from playwright.async_api import Frame
from src.engine.models import Move

# Fractional offsets from canvas bounding box — requires empirical calibration.
# These are placeholders; measure from actual gameplay screenshots.
RACK_Y_FRACTION = 0.92        # rack row is ~92% down the canvas height
RACK_TILE_WIDTH_FRACTION = 0.035  # each rack tile is ~3.5% of canvas width
RACK_FIRST_TILE_X_FRACTION = 0.15  # first rack tile starts at ~15% from left

GRID_ORIGIN_X_FRACTION = 0.03    # board grid left edge
GRID_ORIGIN_Y_FRACTION = 0.02    # board grid top edge
CELL_WIDTH_FRACTION = 0.034       # one board cell width
CELL_HEIGHT_FRACTION = 0.049      # one board cell height

async def place_move(frame: Frame, move: Move, canvas_bbox: dict) -> None:
    """Place all tiles for a move and confirm by clicking the submit button."""
    cx = canvas_bbox["x"]
    cy = canvas_bbox["y"]
    cw = canvas_bbox["width"]
    ch = canvas_bbox["height"]

    for i, tile_use in enumerate(move.tile_uses):
        # Click rack tile by index
        rack_x = cx + (RACK_FIRST_TILE_X_FRACTION + i * RACK_TILE_WIDTH_FRACTION) * cw
        rack_y = cy + RACK_Y_FRACTION * ch
        await frame.mouse.click(rack_x, rack_y)

        # Click board cell by row/col
        cell_x = cx + (GRID_ORIGIN_X_FRACTION + tile_use.col * CELL_WIDTH_FRACTION) * cw
        cell_y = cy + (GRID_ORIGIN_Y_FRACTION + tile_use.row * CELL_HEIGHT_FRACTION) * ch
        await frame.mouse.click(cell_x, cell_y)

    # Click confirm button (selector needs empirical validation)
    await _click_confirm(frame, canvas_bbox)
```

**Critical note:** The fractional constants above are placeholders. Actual values must be measured from real game screenshots and calibrated by testing against a live game. This is the highest-uncertainty component of v1.2.

---

### 5. AutonomousCog (`src/bot/autonomous_cog.py`)

**Responsibility:** Slash commands to start/stop autonomous play for a specific voice channel. Manages a `GameLoop` instance.

Commands:
- `/autoplay start channel:<voice_channel>` — navigate browser to activity, attach `GameLoop._frame`, start loop
- `/autoplay stop` — stop loop, close page
- `/autoplay status` — report loop state (running, stopped, last turn time)

---

## Component Responsibilities Summary

| Component | Responsibility | New or Modified |
|-----------|---------------|-----------------|
| `src/bot/bot.py` | Add `browser_manager` attribute, `close()` override | Modified (additive) |
| `src/browser/manager.py` | Own Playwright + persistent context lifecycle | New |
| `src/browser/navigator.py` | Navigate Discord web to voice channel + locate Activity iframe | New |
| `src/browser/game_loop.py` | `@tasks.loop` polling: turn detection → full play pipeline | New |
| `src/browser/tile_placer.py` | Map `Move` → pixel clicks on canvas | New |
| `src/browser/errors.py` | `NavigationError`, `PlacementError` | New |
| `src/bot/autonomous_cog.py` | Slash commands to start/stop/status autonomous play | New |
| `src/vision/` | No changes — `extract_board_state(bytes, mode)` works as-is | Unchanged |
| `src/engine/` | No changes — `find_all_moves(board, rack, gaddag, mode)` unchanged | Unchanged |
| `src/difficulty/` | No changes — `select_move(moves, difficulty)` unchanged | Unchanged |

---

## Recommended Project Structure

```
src/
├── bot/
│   ├── bot.py                  # Modified: add browser_manager, close() override
│   ├── channel_state.py        # Unchanged
│   ├── cog.py                  # Unchanged (AdvisorCog)
│   ├── autonomous_cog.py       # NEW: /autoplay start|stop|status commands
│   └── formatter.py            # Unchanged
├── browser/                    # NEW package
│   ├── __init__.py
│   ├── manager.py              # BrowserManager: Playwright + persistent context
│   ├── navigator.py            # navigate Discord web → voice channel → iframe
│   ├── game_loop.py            # GameLoop: @tasks.loop turn detection + execute
│   ├── tile_placer.py          # place_move(): Move → pixel click sequence
│   └── errors.py               # NavigationError, PlacementError
├── vision/                     # Unchanged
├── engine/                     # Unchanged
└── difficulty/                 # Unchanged

data/
└── browser_profile/            # NEW: Playwright user_data_dir (gitignored)
```

---

## Data Flow: Turn Detection to Tile Placement

```
[GameLoop.poll_turn fires every 4s]
          │
          ▼
[canvas.screenshot() → bytes]           ~50ms, awaited on event loop
          │
          ▼
[hash comparison to last screenshot]
          │
     no change──────────────────────▶ [wait for next tick]
          │ changed
          ▼
[_is_my_turn(screenshot_bytes)]
          │
     not our turn────────────────────▶ [wait for next tick]
          │ our turn
          ▼
[extract_board_state(bytes, mode)]       4-15s, awaited on event loop
          │
          ├── preprocess_screenshot()   sync, ~20ms
          ├── call_vision_api()         async, 4-15s (Claude API)
          ├── validate_extraction()     sync, <1ms
          └── Board + rack
          │
          ▼
[asyncio.to_thread(find_all_moves, ...)] ~100ms in thread pool
          │
          ▼
[asyncio.to_thread(select_move, ...)]    <1ms in thread pool
          │
          ▼
[place_move(frame, move, canvas_bbox)]   ~500ms, awaited on event loop
          │
          ├── click rack tile [0]
          ├── click board cell [row0, col0]
          ├── ... repeat for each tile
          └── click confirm button
```

**Timing budget per turn:**
- Canvas screenshot: ~50ms
- Turn detection: ~10ms
- Vision pipeline: 4-15s (Claude API latency dominates)
- Engine move generation: ~100ms
- Tile placement: ~500ms

Total turn execution: 5-16 seconds. At 4-second polling, the bot detects its turn within one cycle and responds within ~16 seconds maximum — well within any Letter League turn timer.

---

## Architectural Patterns

### Pattern 1: Shared Event Loop — No Threads for Playwright

**What:** `async_playwright` runs as native asyncio coroutines on the same event loop as discord.py. No separate threads, no `nest_asyncio`, no `asyncio.run_coroutine_threadsafe`.

**When to use:** Always on Python 3.10+. ProactorEventLoop (Windows default since Python 3.8) supports both discord.py's gateway WebSocket and Playwright's subprocess driver.

**Trade-offs:** Simple and debuggable. The one hard constraint: Playwright's API is not thread-safe. Never pass `Page`, `Frame`, or `BrowserContext` objects into `asyncio.to_thread()`. Only pure Python data (bytes, strings, dataclasses) crosses the thread boundary.

```python
# CORRECT: Playwright stays on event loop, only pure data crosses to threads
screenshot_bytes = await canvas.screenshot()              # on event loop
board, rack = await extract_board_state(screenshot_bytes) # on event loop
moves = await asyncio.to_thread(find_all_moves, board, rack, gaddag, mode)  # thread ok
```

---

### Pattern 2: Persistent Context for Login State

**What:** Use `launch_persistent_context(user_data_dir=...)` instead of `launch()` + `new_context()`. The bot operator logs in manually once, then the bot reuses the saved session on every subsequent restart.

**When to use:** Always. The alternative — automating Discord login programmatically — triggers bot detection, CAPTCHA, and 2FA prompts. It is fragile and risks account termination.

**Trade-offs:** Requires a one-time manual login step before the first autonomous run. The `user_data_dir` contains session credentials and must be in `.gitignore`.

```python
context = await pw.chromium.launch_persistent_context(
    user_data_dir="data/browser_profile",
    headless=False,
    args=["--disable-blink-features=AutomationControlled"],
)
# Detect session expiry: if the loaded page is the Discord login screen,
# send a bot notification to the operator to re-authenticate manually.
```

---

### Pattern 3: `discord.ext.tasks` Loop for Game Polling

**What:** Use `@tasks.loop(seconds=4.0)` on `GameLoop.poll_turn` rather than a raw `asyncio.create_task` with a `while True` + `asyncio.sleep`. Use `before_loop` and `after_loop` hooks for lifecycle management.

**When to use:** Always for background polling in discord.py. The `tasks.loop` abstraction handles exception logging, reconnection, and graceful stop semantics.

**Trade-offs:** Slightly less flexible than raw tasks. Worth it for the `before_loop` / `after_loop` / `is_being_cancelled()` hooks.

```python
@tasks.loop(seconds=4.0)
async def poll_turn(self) -> None:
    ...

@poll_turn.before_loop
async def before_poll(self) -> None:
    await self.bot.wait_until_ready()  # ensures browser_manager is initialized

@poll_turn.after_loop
async def after_poll(self) -> None:
    logger.info("Game loop stopped — cancelled={}", self.poll_turn.is_being_cancelled())
```

---

### Pattern 4: Stateless Vision and Engine Pipelines

**What:** The existing `extract_board_state(img_bytes, mode)` and `find_all_moves(board, rack, gaddag, mode)` are pure functions over data. The game loop supplies `bytes` from `canvas.screenshot()` — the vision and engine layers are completely unaware of whether those bytes came from a Discord attachment or a Playwright canvas capture.

**When to use:** Always. Do not modify `src/vision/` or `src/engine/` for autonomous mode. They are stable, well-tested, and require no knowledge of Playwright.

---

### Pattern 5: Runtime Canvas Bounding Box for Coordinate Mapping

**What:** Get the canvas element's screen position at click time using `canvas.bounding_box()`, then compute pixel positions as fractions of that bounding box. Store the fractions as constants calibrated from real game measurements.

**When to use:** For all tile placement clicks. Hardcoding absolute pixel coordinates breaks across resolutions and window sizes.

```python
canvas = frame.locator("canvas")
bbox = await canvas.bounding_box()
# bbox = {"x": 120, "y": 80, "width": 900, "height": 650}

# Board cell at (row=5, col=10):
cell_x = bbox["x"] + (GRID_X0 + col * CELL_W) * bbox["width"]
cell_y = bbox["y"] + (GRID_Y0 + row * CELL_H) * bbox["height"]
await frame.mouse.click(cell_x, cell_y)
```

---

## Anti-Patterns

### Anti-Pattern 1: Passing Playwright Objects to `asyncio.to_thread`

**What people do:** Pass `Page` or `Frame` objects into `asyncio.to_thread()` to run browser operations in a background thread.

**Why it's wrong:** Playwright's API is explicitly not thread-safe. Calling any Playwright method from a worker thread while the event loop manages the same object causes race conditions, assertion errors, or silent failures.

**Do this instead:** Keep all Playwright calls (`canvas.screenshot()`, `frame.locator()`, `mouse.click()`) on the event loop as awaited coroutines. Only pure Python data (bytes, integers, dataclasses) is passed to threads.

---

### Anti-Pattern 2: Using `playwright.sync_api` Inside Async Code

**What people do:** Import from `playwright.sync_api` and call sync methods from inside an async function or a discord.py Cog handler.

**Why it's wrong:** The sync API creates its own internal event loop. Calling it from inside discord.py's already-running event loop raises `RuntimeError: This event loop is already running`.

**Do this instead:** Always import from `playwright.async_api`. Every Playwright call must be `await`ed.

---

### Anti-Pattern 3: Re-launching Browser Per Turn or Per Poll

**What people do:** Create a new `Playwright` + `Browser` + `Page` for each game turn.

**Why it's wrong:** Browser launch takes 2-5 seconds. Navigation takes another 3-8 seconds. The 4-second poll interval would be entirely consumed by setup overhead, and repeated launches raise Discord anti-automation flags.

**Do this instead:** Launch once in `setup_hook`, store `BrowserManager` on the bot, reuse the same `Page` across all turns. Create a new page only when joining a new game session.

---

### Anti-Pattern 4: Automating Discord Login Programmatically

**What people do:** `page.fill('[name="email"]', email)` + `page.fill('[name="password"]', password)` to log in on every restart.

**Why it's wrong:** Discord's auth flow includes CAPTCHA, 2FA, and active bot detection. Automated login is fragile, breaks frequently, and risks account termination.

**Do this instead:** Login manually once in headed mode to populate `user_data_dir`. On restarts, Playwright restores the saved session automatically. Add session-expiry detection: if the browser lands on the login page instead of the Discord app, send a notification to the operator.

---

### Anti-Pattern 5: Hardcoding Absolute Pixel Coordinates

**What people do:** `await frame.mouse.click(450, 820)` with constants measured on one screen.

**Why it's wrong:** Canvas position and size depend on browser window size, Discord zoom level, and screen resolution. Constants measured on one machine break on any other.

**Do this instead:** Get canvas bounding box at runtime via `await canvas.bounding_box()`, then compute positions as fractional offsets of that bounding box's width and height.

---

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Anthropic Claude Vision | `AsyncAnthropic` client — unchanged from v1.1 | Canvas screenshot bytes have same interface as Discord attachment bytes |
| Discord web client | Playwright persistent context, headed Chromium | Login state from `user_data_dir`; `headless=False` required |
| Letter League Activity | `frame.locator("canvas").screenshot()` | Iframe URL pattern needs empirical discovery |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| `bot.setup_hook` → `BrowserManager` | `await browser_manager.start()` | Sequential before READY |
| `AutonomousCog` → `GameLoop` | `game_loop.poll_turn.start()` / `.stop()` | Cog owns GameLoop instance |
| `GameLoop` → `src/vision/` | `await extract_board_state(bytes, mode)` — identical to AdvisorCog | Zero changes to vision |
| `GameLoop` → `src/engine/` | `asyncio.to_thread(find_all_moves, ...)` — identical to AdvisorCog | Zero changes to engine |
| `GameLoop` → `BrowserManager` | `browser_manager.context` → page → frame | Browser access via bot attribute |
| `TilePlacer` → `src/engine/models` | Reads `move.tile_uses[i].row`, `.col` for grid coordinates | `Move` dataclass unchanged |

---

## Suggested Build Order

Dependencies determine the order. Each phase produces a testable artifact before the next begins.

### Phase 1: BrowserManager + Navigator

Build `BrowserManager` and `DiscordNavigator`. Wire `browser_manager` into `bot.setup_hook` and `bot.close()`. Implement `navigate_to_activity()`.

**Test gate:** Bot starts, browser opens headed, navigates to Discord, finds voice channel, locates Letter League iframe, captures a non-blank canvas screenshot.

**Why first:** This is the highest-uncertainty component. Discord Activity iframe selectors are undocumented and require empirical discovery. Validating this before building the game loop avoids rework on a fragile foundation.

---

### Phase 2: Canvas Screenshot through Vision Pipeline

Wire `canvas.screenshot()` bytes through the existing `extract_board_state()`. No code changes to vision.

**Test gate:** Bytes from `canvas.screenshot()` (PNG format — confirmed by Playwright docs) produce a correct `(Board, rack)` tuple through `preprocess_screenshot()` + Claude Vision API.

**Why second:** Validates that the canvas image format is compatible with the existing pipeline before adding game loop complexity.

---

### Phase 3: Turn Detection

Implement `_is_my_turn(screenshot_bytes)`. Start with the simplest viable approach: screenshot hash comparison detects board changes; visual inspection of the "your turn" indicator area (a fixed canvas region) confirms it is the bot's turn.

**Test gate:** Correctly classifies 10 recorded screenshots as "my turn" / "not my turn".

**Why third:** Can be developed with recorded screenshots — no live game needed. Decouples turn detection correctness from tile placement complexity.

---

### Phase 4: TilePlacer and Coordinate Calibration

Measure canvas bounding box from a live or recorded game frame. Derive fractional constants for rack tile positions and board grid cell positions. Implement `place_move()`.

**Test gate:** Bot places a known word (e.g., "CAT" at row 9, col 13) correctly on a live game board.

**Why fourth:** Requires a live game or high-fidelity recordings for calibration. Can't be completed without Phase 1-3 foundation.

---

### Phase 5: AutonomousCog + End-to-End

Implement `/autoplay start|stop|status`. Wire `GameLoop` into `AutonomousCog`. Run a complete game session from turn detection through word placement to confirmation.

**Test gate:** Bot joins a real game, detects its turn, selects a valid word, places tiles correctly, and confirms — without human intervention.

**Why last:** Pure integration glue. Fast to build once Phases 1-4 are solid.

---

## Scaling Considerations

This is a single-server, single-game use case. Scaling is not the primary concern. The relevant operational question is multiple simultaneous games:

| Concern | 1 game | Multiple simultaneous games |
|---------|--------|-----------------------------|
| Browser instances | 1 persistent context, 1 page | 1 context supports multiple pages; one page per active game |
| Vision API calls | Sequential per turn | Concurrent via `asyncio.gather` across game loops; Claude API rate limits apply |
| Event loop blocking | Zero (all awaited) | Zero — non-blocking architecture scales naturally |
| Turn polling loops | 1 `@tasks.loop` instance | 1 loop per channel; `discord.ext.tasks` handles multiple independently |

---

## Sources

- [Playwright Python async API — official docs](https://playwright.dev/python/docs/library) — HIGH confidence; confirms ProactorEventLoop requirement and thread-safety constraints
- [Playwright `launch_persistent_context` — official docs](https://playwright.dev/python/docs/api/class-browsertype) — HIGH confidence; user_data_dir session persistence
- [Playwright Frames — official docs](https://playwright.dev/python/docs/frames) — HIGH confidence; `frame_locator` and `page.frame(url=...)` patterns
- [Playwright Mouse API — official docs](https://playwright.dev/python/docs/api/class-mouse) — HIGH confidence; coordinate-based `page.mouse.click(x, y)` approach
- [discord.ext.tasks — official docs](https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html) — HIGH confidence; `before_loop`, `after_loop`, lifecycle hooks
- [discord.py ProactorEventLoop issue #859](https://github.com/Rapptz/discord.py/issues/859) — HIGH confidence; confirms Python 3.6 bug, fixed in 3.7+, non-issue on Python 3.10
- Playwright not thread-safe — [official docs](https://playwright.dev/python/docs/library) — HIGH confidence; explicit warning in docs
- Discord Activity iframe selectors — MEDIUM confidence; exact URL patterns and canvas layout require empirical validation against live game

---

*Architecture research for: Playwright + discord.py browser automation integration (v1.2)*
*Researched: 2026-03-24*
