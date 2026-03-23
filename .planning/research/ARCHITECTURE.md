# Architecture Research

**Domain:** Discord word game AI bot (Letter League — Scrabble variant)
**Researched:** 2026-03-23
**Confidence:** MEDIUM — core patterns are well-established (Scrabble solvers, discord.py), but Letter League-specific visual parsing is uncharted territory with no public prior art.

---

## Standard Architecture

### System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                        Discord Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │ Slash Command│  │ Image Attach │  │   Game Session Mgmt   │  │
│  │  Handler     │  │  Receiver    │  │   (start/stop/status) │  │
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
     │  Screenshot Input  │   │  Playwright → Discord   │
     │      ↓             │   │  Activity iframe        │
     │  AI Vision (VLM)   │   │      ↓                  │
     │      ↓             │   │  Screenshot Capture     │
     │  BoardState JSON   │   │      ↓                  │
     └────────┬───────────┘   │  AI Vision (VLM)        │
              │               │      ↓                  │
              │               │  BoardState JSON        │
              │               └────────────┬────────────┘
              │                            │
              └────────────┬───────────────┘
                           ▼
┌──────────────────────────────────────────────────────────────────┐
│                       Word Engine Layer                          │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │                   Move Generator                         │     │
│  │  - DAWG dictionary lookup                               │     │
│  │  - Anchor square detection                              │     │
│  │  - Cross-check constraint propagation                   │     │
│  │  - Candidate move enumeration (horizontal + transposed) │     │
│  └──────────────────────┬──────────────────────────────────┘     │
│  ┌──────────────────────▼──────────────────────────────────┐     │
│  │                   Move Scorer                            │     │
│  │  - Letter values + board multipliers                    │     │
│  │  - Wild mode vs Classic mode scoring                    │     │
│  │  - Ranked candidate list                                │     │
│  └──────────────────────┬──────────────────────────────────┘     │
│  ┌──────────────────────▼──────────────────────────────────┐     │
│  │                   Difficulty Filter                      │     │
│  │  - Selects move at percentile N of ranked candidates    │     │
│  │  - 100% = best move, 0% = worst valid move              │     │
│  └──────────────────────┬──────────────────────────────────┘     │
└─────────────────────────┼────────────────────────────────────────┘
                          │
         ┌────────────────▼────────────────┐
         │             Output              │
         │  Advisor Mode: Discord message  │
         │  Auto Mode:  click sequence     │
         │              via Playwright     │
         └─────────────────────────────────┘
```

---

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Discord Cog (Commands) | Receives slash commands (`/analyze`, `/autoplay`, `/difficulty`), dispatches to session controller | `discord.py` Cog class |
| Discord Cog (Events) | Receives image attachments, forwards to vision pipeline | `on_message` handler |
| Game Session Controller | Owns mode state, difficulty setting, routes to advisor or autonomous pipeline | Plain Python class, held in Cog |
| Vision Pipeline | Accepts a screenshot bytes object, sends to VLM API, returns `BoardState` dataclass | Async function, calls Claude/GPT-4o vision API |
| Board State Model | Immutable dataclass representing 2D grid of tiles, rack, multiplier positions, current score mode | Python `dataclass`, grid as `List[List[Cell]]` |
| DAWG Dictionary | In-memory directed acyclic word graph of the Wordnik wordlist | `pyDAWG` or custom DAWG loaded once at startup |
| Move Generator | Finds all legal placements using anchor+cross-check algorithm (Appel-Jacobsen or Gordon GADDAG) | Pure Python, no I/O |
| Move Scorer | Scores each candidate move using Letter League tile values and active scoring mode | Pure Python function |
| Difficulty Filter | Given ranked list, selects a move at the requested percentile | Single function, stateless |
| Browser Automation | Launches persistent Chromium session, navigates to Discord Activity, takes screenshots, clicks tiles | `playwright.async_api`, persistent context |
| Persistent Session Store | Saves Playwright browser storage state to disk so re-auth is not needed each run | JSON file written by `browser_type.launch_persistent_context()` |

---

## Recommended Project Structure

```
letter_league_bot/
├── bot/
│   ├── __init__.py
│   ├── main.py                  # Entry point: creates bot, loads cogs, starts loop
│   ├── cogs/
│   │   ├── advisor.py           # /analyze command + image attachment handling
│   │   └── autoplay.py          # /autoplay, /stop, /difficulty commands
│   └── session.py               # GameSession dataclass: mode, difficulty, state
│
├── vision/
│   ├── __init__.py
│   ├── extractor.py             # screenshot bytes → BoardState via VLM API call
│   └── prompt.py                # system prompt + JSON schema for VLM structured output
│
├── engine/
│   ├── __init__.py
│   ├── dictionary.py            # DAWG load/query; loaded once as module-level singleton
│   ├── board.py                 # BoardState dataclass, Cell dataclass, grid utilities
│   ├── move_generator.py        # anchor detection, cross-checks, candidate enumeration
│   ├── scorer.py                # move scoring: Wild vs Classic modes
│   └── difficulty.py            # percentile selection from ranked candidate list
│
├── automation/
│   ├── __init__.py
│   ├── browser.py               # Playwright lifecycle: launch_persistent_context, reconnect
│   ├── navigator.py             # Discord login check, navigate to voice channel Activity
│   └── placer.py                # click sequence to place a word on the board
│
├── data/
│   ├── wordnik_wordlist.txt     # Wordnik word list (fetched/bundled at setup)
│   └── browser_state/           # Playwright persistent context storage directory
│
└── config.py                    # Discord token, VLM API key, default difficulty, scoring mode
```

### Structure Rationale

- **bot/:** Everything Discord touches. Cogs are thin — they translate Discord events into domain calls, never contain game logic.
- **vision/:** Isolated behind a single async function. Swapping VLM providers only requires changing `extractor.py`.
- **engine/:** Zero I/O, zero async. Pure computation. Independently testable without Discord or a browser running.
- **automation/:** Playwright lifecycle management, kept separate from engine so autonomous mode can be disabled without touching core logic.
- **data/:** Static assets only. Nothing runtime-generated except `browser_state/`.

---

## Architectural Patterns

### Pattern 1: Thin Cog, Fat Engine

**What:** Discord Cogs contain only event wiring and Discord-specific formatting. All decision-making, scoring, and word finding live in `engine/` and `vision/`, which have no discord.py imports.

**When to use:** Always. This is the only correct structure.

**Trade-offs:** Slightly more indirection at call sites, but the engine becomes fully unit-testable without a Discord connection or a live browser.

**Example:**
```python
# bot/cogs/advisor.py
class AdvisorCog(commands.Cog):
    def __init__(self, bot, session: GameSession):
        self.bot = bot
        self.session = session

    @app_commands.command(name="analyze")
    async def analyze(self, interaction: discord.Interaction, screenshot: discord.Attachment):
        await interaction.response.defer()
        image_bytes = await screenshot.read()
        board = await extract_board_state(image_bytes)          # vision/extractor.py
        moves = generate_moves(board, self.session.difficulty)  # engine/
        await interaction.followup.send(format_top_move(moves[0]))
```

### Pattern 2: BoardState as the Contract

**What:** `BoardState` is an immutable dataclass that is the single handoff between every component. Vision produces it. Engine consumes it. Automation reads it to verify its own clicks.

**When to use:** Any time two components need to share the current game state.

**Trade-offs:** All components must agree on the schema. Breaking change in `BoardState` ripples everywhere — but this is desirable because it surfaces contract violations at import time, not runtime.

**Example:**
```python
@dataclass(frozen=True)
class Cell:
    letter: str | None           # None = empty
    multiplier: str | None       # "DL", "TL", "DW", "TW", None
    is_permanent: bool           # Wild mode: True if multiplier bonded to letter

@dataclass(frozen=True)
class BoardState:
    grid: tuple[tuple[Cell, ...], ...]  # [row][col], (0,0) = top-left
    rack: tuple[str, ...]               # player's current tiles, "?" = blank
    scoring_mode: str                   # "wild" | "classic"
    turn_number: int
```

### Pattern 3: Percentile Difficulty Selection

**What:** Move generator returns all valid moves sorted descending by score. Difficulty is a float 0.0–1.0. The selected move index = `floor((1.0 - difficulty) * len(candidates))`, clamped to valid range. 1.0 = best move, 0.0 = worst valid move.

**When to use:** Difficulty setting changes.

**Trade-offs:** Simple and predictable. Does not account for strategic value (blocking opponents, rack balance) — only raw score. Acceptable for v1; strategic heuristics can replace or supplement later.

**Example:**
```python
def select_move(candidates: list[Move], difficulty: float) -> Move:
    # candidates sorted best-first by score
    idx = int((1.0 - difficulty) * (len(candidates) - 1))
    idx = max(0, min(idx, len(candidates) - 1))
    return candidates[idx]
```

### Pattern 4: Persistent Browser Context

**What:** Playwright's `launch_persistent_context()` saves cookies, local storage, and IndexedDB to a directory. On subsequent runs, Discord login state is restored without re-authentication.

**When to use:** Any time the autonomous mode browser is launched.

**Trade-offs:** Sensitive session data stored on disk. Mitigate by storing only in the project's `data/browser_state/` and adding it to `.gitignore`. Manual re-login required if Discord invalidates the session token (typically every 30 days or after suspicious activity).

**Example:**
```python
# automation/browser.py
from playwright.async_api import async_playwright

async def get_browser_context(user_data_dir: str):
    playwright = await async_playwright().start()
    context = await playwright.chromium.launch_persistent_context(
        user_data_dir,
        headless=False,   # Discord Activities require a visible browser or video context
        args=["--disable-blink-features=AutomationControlled"],
    )
    return playwright, context
```

### Pattern 5: Horizontal/Transposed Board for Move Generation

**What:** All word placements are computed as horizontal placements. To find vertical placements, transpose the board grid, run the same horizontal algorithm, then un-transpose the resulting coordinates. This halves the code complexity of the move generator.

**When to use:** Always in the move generator.

**Trade-offs:** Extra transpose step (~negligible for a 27x19 grid). The algorithm from "The World's Fastest Scrabble Program" (Appel and Jacobsen, 1988) establishes this as the canonical approach.

---

## Data Flow

### Advisor Mode Flow

```
User sends /analyze + screenshot attachment
    ↓
AdvisorCog.analyze() — reads attachment bytes
    ↓
vision/extractor.py — POST screenshot to VLM API with JSON schema prompt
    ↓
VLM returns BoardState JSON (grid, rack, scoring_mode)
    ↓
engine/dictionary.py — DAWG already loaded in memory
    ↓
engine/move_generator.py — enumerate all valid placements
    ↓
engine/scorer.py — score each candidate move
    ↓
engine/difficulty.py — select move at requested percentile
    ↓
AdvisorCog — formats top N moves as Discord embed
    ↓
interaction.followup.send() → Discord channel
```

### Autonomous Mode Flow (per turn)

```
AutoplayCog receives /autoplay command
    ↓
automation/browser.py — launch or reattach persistent Chromium context
    ↓
automation/navigator.py — navigate to Discord, open voice channel, start Activity
    ↓
[Game loop — runs until /stop or game ends]
    ↓
automation/browser.py — page.screenshot() → bytes
    ↓
vision/extractor.py — VLM parses screenshot → BoardState
    ↓
engine/ — generate + score + select move (same as advisor mode)
    ↓
automation/placer.py — click tile from rack, click destination squares in sequence
    ↓
automation/placer.py — click "Submit" / confirm button
    ↓
Wait for next turn (poll for turn indicator change)
    ↓
[Repeat loop]
```

### Component Communication

```
discord.py event loop (async)
    │
    ├── Cogs (async) — I/O bound, awaited
    │       │
    │       ├── vision/ (async) — HTTP to VLM API
    │       │
    │       └── automation/ (async) — Playwright awaited calls
    │
    └── engine/ (sync, called with await loop.run_in_executor)
            │
            Note: engine/ is pure CPU-bound Python.
            For a single-game bot this is fast enough to call directly
            in the async loop without executor. Only add run_in_executor
            if profiling shows >100ms move generation latency.
```

---

## Suggested Build Order

Dependencies between components dictate this order:

1. **engine/board.py** — `BoardState` and `Cell` dataclasses. Zero dependencies. Everything else imports this.
2. **engine/dictionary.py** — DAWG loader. Requires only the wordlist file. Test: query known words.
3. **engine/move_generator.py** — Requires `board.py` + `dictionary.py`. Test: generate moves from known board positions.
4. **engine/scorer.py** — Requires `board.py`. Test: score known moves in Wild and Classic modes.
5. **engine/difficulty.py** — Requires `scorer.py` output. Test: percentile selection on dummy candidate lists.
6. **vision/extractor.py** — Requires VLM API credentials + `board.py` schema. Test: real screenshots from Letter League.
7. **bot/cogs/advisor.py** — Requires `vision/` + `engine/`. First end-to-end path. Test: Discord integration test.
8. **automation/browser.py** — Playwright setup, persistent context, screenshot capture. Test: manual capture of Letter League Activity.
9. **automation/navigator.py** — Requires `browser.py`. Test: navigate to a live game.
10. **automation/placer.py** — Requires `navigator.py` + `engine/` output. Test: place a word in a live game.
11. **bot/cogs/autoplay.py** — Wires all automation components. Final integration.

This order means the entire engine can be built and tested before a Discord bot or browser exists. The advisor mode (steps 1–7) provides real value without autonomous mode, and is the correct MVP milestone boundary.

---

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| VLM API (Claude or GPT-4o) | HTTP POST with base64 image + JSON schema prompt, structured output response | Use Anthropic `client.messages.create()` or OpenAI `client.chat.completions.create()` with `response_format`. Claude structured outputs use tool-use pattern. |
| Discord Gateway | discord.py WebSocket; slash commands via `app_commands` tree | Privileged Message Content Intent required to read image attachments in DMs; not needed for slash command attachments. |
| Wordnik Wordlist | Read from file at startup, DAWG constructed in memory once | No runtime network call. Wordlist is static. |
| Playwright / Chromium | `async_playwright()` persistent context; same asyncio event loop as discord.py | On Windows, must use `ProactorEventLoop`. Headless mode may not render Discord Activity canvas fully — test with `headless=False` first. |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Discord Cog ↔ Vision Pipeline | Direct async function call, passes `bytes` in, receives `BoardState` out | No queue needed; one game session at a time. |
| Discord Cog ↔ Engine | Direct sync function call (engine is pure CPU, no I/O) | May add `run_in_executor` if latency becomes visible. |
| Discord Cog ↔ Automation | Direct async function call, passes `Move` in, Playwright performs clicks | The Cog awaits completion before replying to Discord. |
| Vision ↔ Engine | `BoardState` dataclass is the contract; immutable, typed | Schema changes require updating VLM prompt template and all engine consumers. |

---

## Scaling Considerations

This is a single-server tool, not a multi-tenant platform. Scaling is not the primary concern.

| Scale | Architecture Adjustments |
|-------|--------------------------|
| 1 server, 1 game | Default architecture: everything in one process, one Playwright instance |
| 1 server, multiple concurrent games | Add per-game Playwright context (each game = isolated browser context); queue VLM calls to avoid API rate limits |
| Multiple servers | Not in scope. Would require per-guild session isolation and likely a queue/worker pattern. |

### First Bottleneck

VLM API latency (1–5 seconds per screenshot) is the primary constraint. It bounds turn response time. This is acceptable for a turn-based game where players have 60–120 seconds per turn.

### Second Bottleneck

Playwright screenshot → VLM → click loop in autonomous mode. If the bot needs to catch a quick turn window, the round trip must complete in under ~10 seconds. Pre-capture screenshots early in the turn timer rather than waiting for the last moment.

---

## Anti-Patterns

### Anti-Pattern 1: Putting Game Logic in Discord Cogs

**What people do:** Write board parsing, word generation, and scoring directly inside event handlers or Cog methods.

**Why it's wrong:** Untestable without a live Discord connection. Impossible to debug the word engine without triggering Discord events.

**Do this instead:** Cogs call functions from `engine/` and `vision/` packages. The engine has no Discord imports.

### Anti-Pattern 2: Using Playwright Sync API Inside discord.py

**What people do:** Import `playwright.sync_api` and call `page.screenshot()` directly from within an async event handler.

**Why it's wrong:** Playwright's sync API internally manages its own event loop. Calling it from within discord.py's asyncio loop raises `RuntimeError: This event loop is already running`. This is documented behavior.

**Do this instead:** Use `playwright.async_api` with `async_playwright()`. All Playwright calls become awaitable and share the bot's event loop.

### Anti-Pattern 3: Re-launching Playwright Browser Every Turn

**What people do:** Start a new browser, navigate to Discord, find the game, take screenshot, close browser — every turn.

**Why it's wrong:** Browser launch takes 2–5 seconds. Discord login takes additional time if not persisted. Total per-turn overhead of 10+ seconds is unacceptable.

**Do this instead:** Launch once with `launch_persistent_context()`, keep the browser open for the duration of the game, reuse the page object. Only close on `/stop` or game end.

### Anti-Pattern 4: Building a Trie Instead of a DAWG

**What people do:** Load the Wordnik wordlist into a trie for dictionary lookups.

**Why it's wrong:** The Wordnik wordlist contains ~370,000 words. A trie consumes ~12 MB for this. A DAWG consumes ~3.8 MB and is faster to traverse because suffix sharing reduces the number of nodes visited during cross-check validation.

**Do this instead:** Use a DAWG. The `pyDAWG` library provides a ready-made Python implementation. Build the DAWG once from the sorted wordlist at startup (or pre-build and serialize to disk with `dawg.save()`).

### Anti-Pattern 5: Treating Vision Output as Ground Truth Without Validation

**What people do:** Take the VLM-parsed `BoardState` directly and generate moves without sanity-checking the output.

**Why it's wrong:** VLMs hallucinate. A tile might be misidentified, a rack letter wrong, a multiplier square incorrectly classified. The move generator will produce legal-looking but wrong moves. In autonomous mode, the bot will attempt to place non-existent tiles and fail.

**Do this instead:** Add a validation step after VLM parsing: rack length must be 1–7, all tile letters must be in the allowed set (A-Z + blank), grid dimensions must be within expected bounds. Log and skip turns where validation fails rather than propagating bad state.

---

## Sources

- "The World's Fastest Scrabble Program" — Appel and Jacobsen (1988), CMU: https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf
- "A Faster Scrabble Move Generation Algorithm" — Gordon (1994): https://ericsink.com/downloads/faster-scrabble-gordon.pdf (GADDAG paper)
- "Compressing dictionaries with a DAWG" — Steve Hanov: https://stevehanov.ca/blog/?id=115
- "Coding The World's Fastest Scrabble Program in Python" — Aydin Schwartz, Medium: https://medium.com/@aydinschwa/coding-the-worlds-fastest-scrabble-program-in-python-2aa09db670e3
- Playwright Python official docs — async API, persistent context: https://playwright.dev/python/docs/library
- Playwright persistent Discord sessions pattern: https://ray.run/discord-forum/threads/120428-authpersistent-sessionsforever-watching-a-page-for-changes
- discord.py Cogs documentation: https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
- discord.py background tasks: https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html
- Claude structured outputs (tool-use JSON schema): https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Letter League FAQ (board dimensions, scoring modes): https://support-apps.discord.com/hc/en-us/articles/26502196674583-Letter-League-FAQ
- Vike256/Wordbot reference implementation (CLI only, no board reading): https://github.com/vike256/Wordbot
- ScrabbleBot reference (multi-interface Scrabble bot): https://github.com/dbieber/ScrabbleBot

---

*Architecture research for: Discord word game AI bot (Letter League)*
*Researched: 2026-03-23*
