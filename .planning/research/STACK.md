# Stack Research

**Domain:** Discord bot with AI vision, browser automation, and word-game AI
**Researched:** 2026-03-23
**Confidence:** MEDIUM-HIGH (core choices HIGH, version-specific details MEDIUM)

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.11+ | Runtime | discord.py, Playwright, and anthropic SDK all require >=3.9; 3.11 is current stable LTS with significant performance improvements over 3.9/3.10; 3.13+ available but 3.11 is the safe ecosystem sweet spot |
| discord.py | 2.7.1 | Discord bot framework | The project constraint specifies discord.py; it is actively maintained (5,400+ commits, 53,900 dependent projects), supports slash commands and app_commands, has full asyncio integration. The sole maintained first-party Python Discord library. |
| Playwright (async) | 1.58.0 | Browser automation for autonomous game play | Better than Selenium for modern web: auto-waits for DOM, handles iframes natively, faster async architecture, first-class Python async API. Discord Activities run in embedded Chromium iframes — Playwright's iframe locator support is essential. Requires ProactorEventLoop on Windows (automatic on Python 3.7+). |
| anthropic | 0.86.0 | Claude Vision API for board reading | Claude vision leads OCR benchmarks for digital screenshots (Claude Sonnet outperforms alternatives on structured visual content). Sends board screenshot as base64 PNG, receives structured JSON of board state. Avoids training a custom CV model. Preferred over GPT-4V due to project owner's Anthropic relationship and superior structured extraction prompting. |
| Pillow | 12.1.1 | Screenshot preprocessing before AI vision | Crop, resize, enhance screenshots before sending to Claude. Lightweight, no system dependencies. Used for image I/O. OpenCV used alongside for detection; Pillow handles conversion. |
| opencv-python | 4.13.0.92 | Board tile contour detection | Grid detection and tile boundary extraction via contour analysis. Faster than asking Claude to detect coordinates — use CV to locate grid cells, Claude to read content. Pair: OpenCV finds WHERE, Claude reads WHAT. |

### Word-Finding Engine

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Custom GADDAG implementation | N/A (implement from scratch) | Move generation algorithm | GADDAG (Gordon 1994) is the standard algorithm for Scrabble-like games. It is ~2x faster than DAWG for move generation because it encodes reversed prefixes, allowing efficient "hook" move discovery without scanning the entire board. Multiple Python reference implementations exist (astralcai/scrabbler, khaled-abdrabo/scrabble-solver). Build custom to handle Letter League's 27x19 expandable board and Wild vs Classic scoring modes. |
| Wordnik wordlist (flat text) | 2021-07-29 release | Dictionary source | Project constraint. Plain `.txt` file from github.com/wordnik/wordlist. Load into GADDAG on startup. ~180K words; GADDAG representation ~2-10MB in memory (pickle-serializable for startup speed). |
| numpy | 2.x | Board state 2D array | Efficient board representation as typed 2D array. Faster than nested Python lists for board scanning, multiplier square lookups, and scoring calculations across the 27x19+ grid. Standard in game-AI Python implementations. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| aiosqlite | 0.22.1 | Async SQLite for game state persistence | Storing game sessions, difficulty settings per user/guild, board snapshots for advisor mode. Non-blocking within discord.py's event loop. Use for: user preferences, game history, cached board states. |
| python-dotenv | 1.2.2 | Environment variable management | Loading `DISCORD_TOKEN`, `ANTHROPIC_API_KEY`, and any configuration secrets. Never hardcode tokens. Required for deployment. |
| loguru | 0.7.3 | Structured logging | Simpler than stdlib logging; drop-in replacement. Async-safe. Essential for debugging vision extraction failures and browser automation timing issues. |
| aiohttp | 3.x | Async HTTP client | If webhook delivery or external API calls are needed beyond the Anthropic SDK (which has its own async HTTP). Also useful for checking Wordnik API for word definitions in advisor mode. |
| pytest | 8.x | Test runner | Standard Python testing. |
| pytest-asyncio | 1.3.0 | Async test support | Required for testing discord.py coroutines and async Playwright operations. Requires Python >=3.10. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| uv | Dependency management and virtual environments | Fast modern replacement for pip+venv. Lock file support prevents dependency drift across machines. `uv sync` replaces `pip install -r requirements.txt`. |
| Black | Code formatting | Zero-config formatter. Prevents style debates. |
| pyright / pylance | Type checking | Discord.py 2.x ships with type stubs; Playwright has full type annotations. Type checking catches API misuse early. |
| python-dotenv `.env` | Secret management | Keep `DISCORD_TOKEN` and `ANTHROPIC_API_KEY` out of source. |

---

## Installation

```bash
# Create and activate virtual environment (using uv)
pip install uv
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Core runtime dependencies
uv pip install discord.py==2.7.1 playwright==1.58.0 anthropic==0.86.0

# Install Playwright browsers (Chromium only — Discord Activity runs Chromium)
playwright install chromium

# Image processing
uv pip install pillow==12.1.1 opencv-python==4.13.0.92 numpy

# Bot infrastructure
uv pip install aiosqlite==0.22.1 python-dotenv==1.2.2 loguru==0.7.3 aiohttp

# Dev dependencies
uv pip install --dev pytest pytest-asyncio==1.3.0 black pyright
```

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| discord.py 2.7.1 | Pycord (py-cord) | Never for this project — project constraint specifies discord.py. Pycord is a community fork with faster slash command iteration; consider if discord.py development stalls. |
| discord.py 2.7.1 | nextcord | Never for this project. Another fork, less popular than pycord. Ecosystem fragmentation risk. |
| Playwright (async) | Selenium | If the team has existing Selenium expertise and is uncomfortable with Playwright. Selenium is slower, no native iframe auto-wait, more setup overhead. Playwright is the 2025 standard. |
| Playwright (async) | PyAutoGUI + direct window | If Discord refuses to run in headless Chromium. PyAutoGUI clicks on screen coordinates but requires a display and is brittle to window positioning. Only use as fallback when Playwright is blocked. |
| Claude Vision API | EasyOCR | If API costs are unacceptable. EasyOCR is open-source and GPU-accelerated. However, EasyOCR struggles with custom game fonts, overlapping tile colors, and structured board layouts. Claude Vision handles these naturally with prompt guidance. |
| Claude Vision API | Tesseract | Never for this use case. Tesseract requires ideal input (clean fonts, white background). Game screenshots have colored tiles, custom fonts, decorative borders — Tesseract fails without extensive preprocessing. |
| Claude Vision API | PaddleOCR | If self-hosting is required and costs are a hard constraint. PaddleOCR is the strongest open-source alternative but still requires more preprocessing than Claude Vision. |
| Custom GADDAG | pyDAWG library | If build time is severely constrained. pyDAWG provides DAWG (not GADDAG) lookup; GADDAG is 2x faster for move generation. Custom GADDAG is 100-200 lines of Python using Gordon 1994 paper; not complex to implement. |
| numpy board array | Pure Python 2D lists | If numpy is unavailable. Pure Python lists work but are slower for board scanning at scale. For a 27x19 board, the difference is minor; numpy is preferred for code clarity and future performance needs. |
| aiosqlite | asyncpg + PostgreSQL | If the bot scales to >100 concurrent games or multi-server deployment with shared state. For single-server or personal use, SQLite is sufficient and has no server to manage. |
| loguru | stdlib logging | If adding dependencies is undesirable. stdlib logging works but requires more boilerplate for async-safe rotation and structured output. |
| uv | pip + venv | If uv is not available. Standard pip + venv works identically; uv is just faster and produces a lock file. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Selenium | Slower than Playwright, no native iframe support, requires separate driver binary management, less active development. Discord Activities load in nested iframes — Playwright handles these natively. | Playwright 1.58.0 |
| discord.py-self (self-bot library) | Violates Discord's Terms of Service. Self-bots automate user accounts; Discord bans accounts using them. The autonomous play mode must operate as a proper Discord bot that joins Activities as a registered application, not by impersonating a user account. | discord.py 2.7.1 (registered bot) |
| Tesseract OCR | Requires clean, pre-processed input. Game board screenshots have colored backgrounds, custom tile graphics, and variable fonts. Tesseract accuracy on game assets is poor without extensive CV preprocessing that negates its simplicity advantage. | Claude Vision via anthropic SDK |
| requests (sync HTTP) | Blocking in discord.py's asyncio event loop. Any sync network call blocks the entire bot. | aiohttp or anthropic SDK's async client |
| JSON files for state persistence | Not a database — no atomicity, no concurrent write safety, no query capability. Breaks under concurrent game sessions. | aiosqlite |
| PyAutoGUI for browser automation | Screen-coordinate-based clicking is brittle; breaks on resolution changes, window repositioning, or partial visibility. No concept of DOM, waits, or element visibility. | Playwright async API |
| OpenAI GPT-4V instead of Claude | Neither technically superior nor inferior for this task, but adds a second API vendor relationship and cost center. Claude Vision is already specified in project constraints. | anthropic SDK with Claude Vision |
| threading for Playwright | Playwright is async-native. Running it in threads alongside discord.py's asyncio loop causes event loop conflicts. Use Playwright's async API within discord.py's existing loop. | playwright.async_api with asyncio |

---

## Stack Patterns by Variant

**Advisor mode (user sends screenshot, bot replies with best word):**
- User uploads screenshot as Discord attachment
- Bot downloads attachment bytes via `discord.Attachment.read()`
- Pillow opens image, OpenCV detects grid boundaries, crops to board
- Send cropped image to Claude Vision API as base64 PNG
- Claude returns structured board state (JSON: tile positions, letters, multipliers, rack)
- GADDAG engine generates all valid moves, ranks by score
- Bot replies with top move(s) as formatted Discord message

**Autonomous mode (bot joins game and plays):**
- Playwright launches headless Chromium
- Navigates to Discord Activity URL inside a voice channel
- Logs in using a dedicated bot account's session token (NOT a self-bot — use a dedicated test account for the Activity player, separate from the Discord API bot)
- Screenshots the game board at regular intervals
- Vision pipeline extracts board state
- GADDAG engine selects move (filtered by difficulty percentage)
- Playwright clicks tile rack and board squares to place word
- Loop continues until game ends

**Important:** The autonomous mode requires a human-played Discord account (not the bot's API account) to actually join and play the Activity. The Discord API bot handles commands; a separate browser session (via Playwright) controls a player account. This is the grey area for TOS — see PITFALLS.md.

**If difficulty scaling needed:**
- Sort all valid moves by score (descending)
- At 100% difficulty: play the top move
- At X% difficulty: randomly select from moves within top (100-X)% score range, or apply score ceiling filter
- Store difficulty setting per user/guild in aiosqlite

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| discord.py 2.7.1 | Python 3.8+ | Tested on 3.11; references to 3.13/3.14 in changelog |
| playwright 1.58.0 | Python >=3.9 | Requires ProactorEventLoop on Windows (auto-set); incompatible with SelectorEventLoop |
| anthropic 0.86.0 | Python >=3.9 | Use async client (`AsyncAnthropic`) with discord.py's event loop |
| pytest-asyncio 1.3.0 | Python >=3.10 | Note: requires 3.10+, so test environment needs 3.10+ even if production uses 3.9 |
| python-dotenv 1.2.2 | Python >=3.9 (dropped 3.8) | Dropped Python 3.9 in latest release — use 3.10+ for full compatibility |
| opencv-python 4.13.0.92 | Python 3.8-3.12 | No wheels for 3.13 yet as of research date — verify before using 3.13 |
| Pillow 12.1.1 | Python 3.9+ | Actively maintained; check Python 3.11 wheel availability |
| aiosqlite 0.22.1 | Python 3.8+ | Stable; no compatibility concerns |

**Recommended Python version: 3.11** — balances stability, ecosystem support, and performance. Avoids the 3.13 wheel gaps for OpenCV.

---

## Sources

- PyPI: discord.py — version 2.7.1 confirmed via readthedocs changelog (HIGH confidence)
- PyPI: playwright — version 1.58.0, released 2026-01-30, Python >=3.9 (HIGH confidence)
- PyPI: anthropic — version 0.86.0, released 2026-03-18, Python >=3.9 (HIGH confidence)
- PyPI: aiosqlite — version 0.22.1, released 2025-12-23 (HIGH confidence)
- PyPI: python-dotenv — version 1.2.2, released 2026-03-01 (HIGH confidence)
- PyPI: loguru — version 0.7.3 (MEDIUM confidence — last verified via search, not direct PyPI fetch)
- PyPI: opencv-python — version 4.13.0.92, released 2026-02-05 (MEDIUM confidence — from search summary)
- PyPI: Pillow — version 12.1.1, released 2026-02-11 (MEDIUM confidence — from search summary)
- Playwright docs: https://playwright.dev/python/docs/library — async API patterns, Windows ProactorEventLoop requirement (HIGH confidence)
- GADDAG algorithm: Gordon 1994 paper "A Faster Scrabble Move Generation Algorithm" — https://ericsink.com/downloads/faster-scrabble-gordon.pdf (HIGH confidence, well-established algorithm)
- Wordnik wordlist: https://github.com/wordnik/wordlist — plain text format, ~180K words (HIGH confidence)
- Discord TOS on self-bots: https://support.discord.com/hc/en-us/articles/115002192352 — confirms self-bots prohibited (HIGH confidence)
- OCR comparison sources: Claude Vision benchmark results from search (MEDIUM confidence — multiple search sources agree Claude Sonnet leads for digital screenshots)
- pytest-asyncio 1.3.0: https://pypi.org/project/pytest-asyncio/ — released 2025-11-10, Python >=3.10 (HIGH confidence)

---

*Stack research for: Discord bot with AI vision, browser automation, and Scrabble-like word-finding*
*Researched: 2026-03-23*
