# Stack Research

**Domain:** Discord bot with AI vision, browser automation, and word-game AI
**Researched:** 2026-03-24 (updated for v1.1 milestone)
**Confidence:** HIGH (all versions re-verified against PyPI and official docs March 2026)

---

## v1.0 vs v1.1 Scope Separation

The v1.0 engine is shipped and validated. Do not re-implement or replace:

| Already Exists (v1.0) | Do NOT Re-research |
|-----------------------|--------------------|
| Python 3.11 | Runtime |
| pytest + pytest-asyncio | Test framework |
| wordfreq | Word frequency for difficulty |
| GADDAG dictionary engine | Move generation |
| Board state (27x19 grid) | Data model |
| Classic/Wild scoring engine | Scoring |
| DifficultyEngine | Alpha-weighted selection |

**v1.1 adds three new capability areas:**
1. Claude Vision API — read board state from screenshots
2. discord.py bot — advisor mode, message/attachment handling
3. Playwright — autonomous mode browser automation

---

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| `discord.py` | `2.7.1` | Discord bot framework — message handling, attachment reads, slash/hybrid commands | Project constraint specifies discord.py. Actively maintained; 5,400+ commits; v2.x supports native app_commands (slash commands) and full asyncio integration. Released March 3, 2026. The only maintained first-party Python Discord library. |
| `anthropic` | `0.86.0` | Claude Vision API client — send board screenshots, receive structured JSON | Official Anthropic SDK. Provides sync and async clients, type safety, automatic retries, and rate-limit handling. Python >=3.9. Released March 18, 2026. |
| `playwright` | `1.58.0` | Chromium browser automation — open Discord Activity iframe, take screenshots, click game elements | Better than Selenium for modern SPAs: auto-wait semantics, native iframe locator support, first-class async Python API required by discord.py's asyncio event loop. Released January 30, 2026. Python >=3.9. |

### Claude Model Selection

Use **`claude-sonnet-4-6`** for all vision calls.

| Model | Input cost | Speed | Vision | Recommendation |
|-------|------------|-------|--------|----------------|
| `claude-sonnet-4-6` | $3/MTok | Fast | Yes | **Use this** — best cost/speed for structured extraction |
| `claude-haiku-4-5-20251001` | $1/MTok | Fastest | Yes | Only downgrade here after accuracy validation on real boards |
| `claude-opus-4-6` | $5/MTok | Moderate | Yes | Overkill; unnecessary cost for board reading |

A 1000x1000px board screenshot costs approximately $0.004 per call at Sonnet 4.6 pricing.
All three current models support vision (image input). Haiku 3 is deprecated and retires April 19, 2026 — do not use it.

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `Pillow` | `12.1.1` | Screenshot preprocessing — resize, crop, format convert before Claude API call | Always — resize screenshots to <=1568px per edge before encoding to keep Claude API latency low and avoid auto-downsampling. A 1000x1000px PNG uses ~1334 tokens. |
| `opencv-python` | `4.13.0.92` | Board tile contour detection — locate grid cell boundaries | Use to find WHERE cells are; pass Claude only the relevant regions. Separates structural detection (OpenCV) from content reading (Claude Vision). |
| `python-dotenv` | `1.2.2` | Load `DISCORD_TOKEN`, `ANTHROPIC_API_KEY` from `.env` | Always — never hardcode secrets. |
| `aiosqlite` | `0.22.1` | Async SQLite — persist user difficulty settings, game session state | Use for user/guild preferences and board snapshots. Async-safe within discord.py's event loop. Non-blocking. |
| `loguru` | `0.7.3` | Structured logging | Simpler than stdlib logging; async-safe; critical for debugging vision extraction failures and automation timing. |
| `aiohttp` | `3.x` | Async HTTP client | Only if webhook delivery or external API calls are needed beyond the anthropic SDK. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| `playwright install chromium` | Download Chromium browser binary | Run once after `pip install playwright`. Only need Chromium — Discord Activity is Chromium-based. Firefox/WebKit not needed. |
| `pytest-asyncio` | Async test support for discord.py event handlers and vision pipeline | Already in project. Pin to `>=0.23`. |
| `black` | Code formatting | Zero-config, prevents style debates. |
| `pyright` / `pylance` | Type checking | discord.py 2.x and playwright ship type stubs. Catches API misuse early. |
| `uv` | Fast dependency management | Replaces pip+venv for speed and lock-file support. `uv sync` = `pip install -r requirements.txt`. |

---

## Installation

```bash
# New dependencies only (add to existing requirements.txt)
pip install "discord.py==2.7.1"
pip install "anthropic==0.86.0"
pip install "playwright==1.58.0"
pip install "Pillow==12.1.1"
pip install "opencv-python==4.13.0.92"
pip install "python-dotenv==1.2.2"
pip install "aiosqlite==0.22.1"
pip install "loguru==0.7.3"

# One-time browser install (Chromium only)
playwright install chromium

# Dev additions
pip install "pytest-asyncio>=0.23"
```

---

## Integration Points With Existing v1.0 Code

### Vision pipeline feeds the existing engine

The Claude vision call produces a board state dict. That maps directly to the
existing `Board` class. The vision module is a new layer on top — it generates
input, the v1.0 engine consumes it unchanged.

```
Screenshot (PNG bytes from Discord attachment or Playwright)
    → VisionPipeline.extract_board_state()      [new v1.1]
    → Board(grid, rack, mode)                   [existing v1.0]
    → MoveGenerator.find_all_moves()            [existing v1.0]
    → DifficultyEngine.select_move()            [existing v1.0]
    → formatted suggestion string               [new v1.1 formatting]
```

### discord.py runs on asyncio — Playwright must use async API

discord.py uses Python's asyncio event loop. Playwright ships both sync and async
APIs. Using the sync API inside discord.py's loop raises a hard runtime error:

> Error: It looks like you are using Playwright Sync API inside the asyncio loop.

Always use `playwright.async_api` (`async_playwright`), never `playwright.sync_api`.

```python
# Correct — async API only
from playwright.async_api import async_playwright

async def capture_activity_screenshot() -> bytes:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # navigate, wait, screenshot
        screenshot = await page.screenshot()
        await browser.close()
        return screenshot
```

### Attachment reading in advisor mode

discord.py's `Attachment.read()` is an async coroutine returning raw bytes.
Pass directly to the vision pipeline — no temp files needed.

```python
@bot.event
async def on_message(message: discord.Message):
    if message.attachments:
        attachment = message.attachments[0]
        # Validate content type before processing
        if attachment.content_type and attachment.content_type.startswith("image/"):
            img_bytes: bytes = await attachment.read()
            board_state = await vision.extract_board_state(img_bytes)
```

### Claude Vision API call structure

Images arrive as PNG bytes. Encode to base64, send with structured extraction prompt.
Image first in content array for best performance per Anthropic docs.

```python
import base64
import anthropic

client = anthropic.AsyncAnthropic()

async def extract_board_state(img_bytes: bytes) -> dict:
    img_b64 = base64.standard_b64encode(img_bytes).decode("utf-8")
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": img_b64,
                    },
                },
                {
                    "type": "text",
                    "text": "Extract the Letter League board state as JSON..."
                }
            ]
        }]
    )
    return parse_json(response.content[0].text)
```

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| `discord.py 2.7.1` | `Pycord (py-cord)` | Never for this project — project constraint specifies discord.py. Pycord is a community fork with slightly faster slash command iteration; consider only if discord.py development stalls long-term. |
| `discord.py 2.7.1` | `nextcord` | Never. Less popular fork, higher ecosystem fragmentation risk. |
| `playwright` (async) | `selenium` | Only if team has existing Selenium infrastructure and can't retrain. Playwright is the 2025-2026 standard: faster, better async, native iframe handling. |
| `playwright` (async) | `PyAutoGUI` + window | Fallback only if Discord refuses to run in headless Chromium. PyAutoGUI clicks screen coordinates; brittle to window position/resolution changes. |
| `claude-sonnet-4-6` | `claude-haiku-4-5` | After validating accuracy on real board screenshots. Haiku is 3x cheaper but less reliable on structured visual extraction. Start with Sonnet. |
| base64 image encoding | Claude Files API | Use Files API only for multi-turn conversations reusing the same image. For single-shot board reads, base64 is simpler and has no upload overhead. |
| `anthropic` SDK | Raw `httpx` calls | Never. SDK provides type safety, retry logic, rate-limit handling, and streaming — all needed in production. |
| `EasyOCR` | Claude Vision API | Only if API costs become hard constraint. EasyOCR is open-source and GPU-accelerated but struggles with custom game fonts, colored tile backgrounds, and structured layouts that Claude handles naturally with prompt guidance. |
| `aiosqlite` + SQLite | `asyncpg` + PostgreSQL | Only if scaling to >100 concurrent games or multi-server shared state. SQLite is sufficient for single-server or personal use. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `discord-self` / `discum` / any self-bot library | Automating a user account violates Discord TOS. Discord explicitly prohibits self-bots and bans accounts that use them. Confirmed active enforcement. | `discord.py 2.7.1` with proper bot application token |
| `playwright.sync_api` inside discord.py | Raises hard runtime error: sync API cannot run inside asyncio loop. | `playwright.async_api` with `async_playwright()` throughout |
| `selenium` | No native async support; brittle with Discord's React SPA; slower startup; separate driver binary management | `playwright` 1.58.0 |
| `Tesseract OCR` | Requires clean, pre-processed input. Game board screenshots have colored tiles, custom fonts, decorative borders. Tesseract accuracy on game assets is poor without extensive preprocessing. | Claude Vision via `anthropic` SDK |
| `requests` (sync HTTP) | Blocking in discord.py's asyncio event loop. Any sync network call blocks the entire bot. | `aiohttp` or `anthropic` SDK's async client (`AsyncAnthropic`) |
| `OpenAI GPT-4V` | Adds a second API vendor and cost center. Claude Vision is already specified in project constraints and performs equivalently for structured extraction. | `anthropic` SDK with `claude-sonnet-4-6` |
| `threading` for Playwright | Running Playwright in threads alongside discord.py's asyncio loop causes event loop conflicts. | `playwright.async_api` natively within discord.py's loop |
| `PyAutoGUI` for browser automation | Screen-coordinate clicking breaks on resolution changes, window repositioning, or partial visibility. No concept of DOM, waits, or element visibility. | `playwright` async API |
| JSON files for state persistence | Not a database — no atomicity, no concurrent write safety, no query capability. Breaks under concurrent game sessions. | `aiosqlite` |
| `claude-3-haiku-20240307` (Haiku 3) | Deprecated. Retiring April 19, 2026. | `claude-haiku-4-5-20251001` if cost is priority |

---

## Stack Patterns by Variant

**Advisor mode (recommended to build first — zero TOS risk):**
- User drops screenshot in Discord channel
- `on_message` handler downloads attachment bytes via `discord.Attachment.read()`
- Pillow resizes if needed; OpenCV detects grid boundaries
- Claude Vision call returns board state JSON
- GADDAG engine finds all moves, DifficultyEngine selects by % setting
- Bot replies with formatted best-move suggestion
- No Playwright needed for this mode

**Autonomous mode (build after advisor mode — TOS constraint must be resolved first):**
- Playwright launches headless Chromium
- Logs in to Discord as a dedicated player account (see critical note below)
- Navigates to voice channel Activity URL, waits for Letter League iframe
- Screenshots board at each turn
- Vision pipeline → GADDAG → DifficultyEngine → move selection
- Playwright clicks tile rack and board squares to place word
- Loops until game end

**Critical constraint for autonomous mode:** Discord Activities require a user account logged in via the browser. Discord API bots (application accounts) cannot join Activities through the Discord API. Any user account automation is potentially TOS-violating (self-botting). This is an unresolved architectural blocker — see PITFALLS.md.

**If vision call cost becomes a concern:**
- Resize screenshots to 1000x1000px before encoding (saves ~$0.002/call vs full res)
- Downgrade to `claude-haiku-4-5` only after accuracy validation on real boards
- Consider caching extracted board state when screenshot hasn't changed

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| `discord.py 2.7.1` | Python >=3.8 | Project uses Python 3.11 — fully compatible |
| `anthropic 0.86.0` | Python >=3.9 | Python 3.11 is supported; use `AsyncAnthropic` client |
| `playwright 1.58.0` | Python >=3.9 | Python 3.11 supported; requires ProactorEventLoop on Windows (auto-set by Python 3.8+) |
| `Pillow 12.1.1` | Python 3.9+ | Python 3.11 supported; no conflicts |
| `opencv-python 4.13.0.92` | Python 3.8–3.12 | Python 3.11 supported; 3.13 wheel availability unconfirmed — not an issue with project's 3.11 |
| `aiosqlite 0.22.1` | Python 3.8+ | No compatibility concerns |
| `pytest-asyncio >=0.23` | Python >=3.8 | Use `asyncio_mode = "auto"` in pytest.ini for cleaner test syntax |
| `python-dotenv 1.2.2` | Python >=3.8 | No compatibility concerns |

**Windows-specific note for Playwright:** On Windows, Python 3.8+ automatically uses
`ProactorEventLoop` (required by Playwright). No manual configuration needed.

---

## Sources

- [discord.py PyPI](https://pypi.org/project/discord.py/) — v2.7.1 verified March 2026 (HIGH confidence)
- [anthropic PyPI](https://pypi.org/project/anthropic/) — v0.86.0, released 2026-03-18, Python >=3.9 (HIGH confidence)
- [playwright PyPI](https://pypi.org/project/playwright/) — v1.58.0, released 2026-01-30, Python >=3.9 (HIGH confidence)
- [Anthropic Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview) — model IDs `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`, pricing, vision support, Haiku 3 deprecation (HIGH confidence — official docs)
- [Anthropic Vision Docs](https://platform.claude.com/docs/en/build-with-claude/vision) — image formats (JPEG/PNG/GIF/WebP), 5MB API limit, base64 encoding, image-before-text ordering for best results, token cost formula (HIGH confidence — official docs)
- [Discord Self-Bot TOS Policy](https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots) — confirms self-bots prohibited (HIGH confidence)
- [Playwright async/asyncio integration](https://github.com/microsoft/playwright-python/issues/1760) — confirms sync API raises hard error in asyncio loops (HIGH confidence)
- [discord.py 2.0 app_commands guide](https://www.pythondiscord.com/pages/guides/python-guides/app-commands/) — slash command structure in v2.x (MEDIUM confidence)
- [discord.py attachment handling](https://discordpy.readthedocs.io/en/latest/api.html) — `Attachment.read()` returns bytes (HIGH confidence — official docs)

---

*Stack research for: Letter League Bot v1.1 — Vision + Discord Integration*
*Researched: 2026-03-24*
