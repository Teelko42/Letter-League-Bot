# Stack Research

**Domain:** Discord bot with AI vision, browser automation, and word-game AI
**Researched:** 2026-03-24 (v1.2 update — Browser Automation + Autonomous Play)
**Confidence:** HIGH (all new additions verified against PyPI, official Playwright docs, and official sources March 2026)

---

## Scope: What This Document Covers

This file covers the FULL stack for the project. The v1.2 section at the top documents only the NEW additions needed for browser automation. The v1.1 section below it remains the authoritative record for what is already shipped.

---

## v1.2 NEW Additions: Browser Automation Stack

These are the only additions needed for the autonomous play milestone. Everything from v1.0 and v1.1 continues unchanged.

### Core Technologies (NEW in v1.2)

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| `playwright` | `1.58.0` | Chromium browser automation — open Discord web client, navigate to voice channel, interact with Letter League Activity iframe, click canvas tiles | Already specified in project constraints. Async Python API integrates natively with discord.py's asyncio event loop. Auto-wait semantics eliminate manual `time.sleep()` calls. Native `frame_locator()` API handles Discord's nested iframe structure. Required `async_playwright` (not sync) inside discord.py's loop. Released 2026-01-30. Python >=3.9. |
| `patchright` | `1.58.2` | Drop-in Playwright replacement with CDP leak patches — reduces Discord headless detection risk | Discord uses bot detection similar to Cloudflare/DataDome targets. Patchright patches runtime CDP leaks, sets `navigator.webdriver = false`, and avoids HeadlessChrome UA string exposure. Drop-in swap: change `from playwright.async_api import async_playwright` to `from patchright.async_api import async_playwright`. Chromium-only (matches project requirement). Version 1.58.2, released 2026-03-07. LOW overhead for HIGH detection-bypass benefit. |

**Decision on patchright vs vanilla playwright:** Use `patchright` as the Playwright backend. It is a drop-in replacement with one import change. The project requires headed Chromium (PROJECT.md: "Discord detects headless Chromium; use headed with virtual display"), so headless mode is already off — but CDP-level fingerprint leaks persist even in headed mode. Patchright closes those leaks. If patchright introduces any compatibility issues, revert to `playwright` with one line change.

### Supporting Libraries (NEW in v1.2)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `numpy` | `>=1.24` | Convert `page.screenshot()` bytes to ndarray for OpenCV processing — already an implicit dependency of opencv-python | Use when comparing sequential canvas screenshots to detect visual state changes (turn detection). `np.frombuffer(screenshot_bytes, dtype=np.uint8)` then `cv2.imdecode()`. No install needed if opencv-python is present — numpy is already a transitive dependency. |

**Why numpy is listed separately:** It is NOT a new install, but the explicit byte-to-ndarray conversion pattern is new code. Documenting the dependency chain avoids confusion.

**Nothing else needs adding.** The remaining v1.2 features (screenshot capture, canvas analysis, Vision API calls, move generation, difficulty selection) all use the existing stack from v1.1.

---

## v1.2 Integration Patterns

### Pattern 1: Persistent Browser Session

The Playwright browser must live for the duration of a game session (potentially 20–60 minutes). Do NOT use the `async with async_playwright() as p:` auto-close pattern inside discord.py — that closes the browser when the context manager exits.

**Correct pattern — bot-level browser lifecycle:**
```python
# In bot.py setup_hook: launch once, store on bot instance
from patchright.async_api import async_playwright

class LetterLeagueBot(commands.Bot):
    async def setup_hook(self) -> None:
        # ... existing GADDAG/DifficultyEngine setup ...
        self._pw = await async_playwright().start()  # does NOT auto-close
        self.browser = await self._pw.chromium.launch_persistent_context(
            user_data_dir="cache/browser_profile",
            headless=False,  # Discord rejects headless Chromium fingerprint
            channel="chrome",  # use system Chrome if available; else bundled Chromium
        )

    async def close(self) -> None:
        await self.browser.close()
        await self._pw.stop()
        await super().close()
```

**Why `launch_persistent_context` over `storage_state`:**
- `launch_persistent_context(user_data_dir=...)` saves cookies, localStorage, IndexedDB, and cached JS/CSS across restarts — Discord uses all of these for session state
- `storage_state` only captures cookies/localStorage; does NOT preserve Chrome-level session caches, meaning Discord may prompt re-authentication on every bot restart
- Only one process can own the `user_data_dir` at a time — this is fine since the bot runs as a single process
- Source: [Playwright BrowserType docs](https://playwright.dev/python/docs/api/class-browsertype) — confirms `user_data_dir` semantics

**Directory:** `cache/browser_profile/` — add to `.gitignore`, never commit (contains Discord session tokens).

### Pattern 2: Discord Web Client Navigation

Navigate via the standard web URL format. No deep-link protocol or Discord API needed.

```python
# Navigate to voice channel (guild and channel IDs from discord.py event context)
channel_url = f"https://discord.com/channels/{guild_id}/{channel_id}"
page = self.browser.pages[0] if self.browser.pages else await self.browser.new_page()
await page.goto(channel_url, wait_until="networkidle")
```

URL format: `https://discord.com/channels/{guild_id}/{channel_id}` — confirmed standard web client format.

### Pattern 3: Activity iframe Interaction

Discord Activities run inside a nested iframe. Use `frame_locator()` to address elements inside it.

```python
# Letter League Activity iframe (selector TBD — inspect Discord DOM to confirm)
activity_frame = page.frame_locator('iframe[src*="activities"]').first

# Take screenshot of the iframe content region
iframe_element = page.locator('iframe[src*="activities"]').first
bounding_box = await iframe_element.bounding_box()
screenshot_bytes = await page.screenshot(clip={
    "x": bounding_box["x"],
    "y": bounding_box["y"],
    "width": bounding_box["width"],
    "height": bounding_box["height"],
})
```

Note: The exact iframe selector requires DOM inspection of a live Discord session during implementation. The `src*="activities"` pattern is a starting point — confirm during Phase development.

### Pattern 4: Canvas Screenshot Capture (Blank Detection)

The canvas is blank while the game loads. Detect non-blank canvas before passing to the vision pipeline.

```python
import numpy as np
import cv2

async def is_canvas_loaded(page, iframe_clip: dict) -> bool:
    """Return True if canvas has rendered non-trivial content."""
    screenshot_bytes = await page.screenshot(clip=iframe_clip)
    arr = cv2.imdecode(np.frombuffer(screenshot_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    # If more than 95% of pixels share the same dominant color, canvas is blank/loading
    dominant = np.bincount(arr.reshape(-1, 3).dot([1, 256, 65536])).argmax()
    dominant_count = (arr.reshape(-1, 3).dot([1, 256, 65536]) == dominant).sum()
    fill_ratio = dominant_count / arr.size * 3
    return fill_ratio < 0.95
```

Alternative: use `page.evaluate()` to read canvas pixel data directly via JavaScript:
```python
is_blank = await page.evaluate("""() => {
    const canvas = document.querySelector('canvas');
    if (!canvas) return true;
    const ctx = canvas.getContext('2d');
    const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    const first = data[0];
    return data.every((v, i) => i % 4 === 3 || v === first);  // all same color = blank
}""")
```

The screenshot approach is preferred because: (1) canvas `getContext('2d')` may be blocked by the iframe's cross-origin policy when Discord Activity iframes are served from a different origin; (2) screenshot bytes are already needed for the vision pipeline, so capturing once serves dual purpose.

### Pattern 5: Turn Detection

No DOM API exposes turn state. Use visual polling with screenshot comparison.

```python
import asyncio

async def wait_for_turn(page, clip: dict, poll_interval: float = 2.0, timeout: float = 300.0):
    """Poll until visual state changes, indicating a new turn."""
    last_screenshot = await page.screenshot(clip=clip)
    elapsed = 0.0
    while elapsed < timeout:
        await asyncio.sleep(poll_interval)
        current = await page.screenshot(clip=clip)
        if current != last_screenshot:
            return current  # visual change detected — new game state
        elapsed += poll_interval
    raise TimeoutError("Turn wait exceeded timeout")
```

More precise alternative: compare only the rack region (bottom of canvas) rather than full board, to detect tile distribution (turn start) vs board change (opponent play). The exact rack bounding box requires calibration against live screenshots.

### Pattern 6: Tile Placement Clicks

Canvas tiles have no DOM elements. Use `page.mouse.click()` at absolute page coordinates.

```python
# Get canvas element position
canvas_element = activity_frame.locator("canvas").first
canvas_box = await canvas_element.bounding_box()  # relative to main page

# Click at computed tile coordinates (canvas_box offsets + tile grid math)
tile_x = canvas_box["x"] + computed_col_offset
tile_y = canvas_box["y"] + computed_row_offset
await page.mouse.click(tile_x, tile_y)

# Small delay between clicks — Discord Activity canvas may buffer rapid events
await asyncio.sleep(0.1)
```

Note: `locator.click(position={"x": col_offset, "y": row_offset})` is an equivalent alternative that keeps coordinates relative to the element, avoiding the need to add `canvas_box["x"]` manually.

---

## v1.1 Stack (Shipped — Do NOT Re-research)

### Core Technologies (Shipped in v1.1)

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| `discord.py` | `2.7.1` | Discord bot framework — message handling, attachment reads, slash commands, event loop | Project constraint. Actively maintained. v2.x supports native `app_commands` (slash commands) and full asyncio integration. Released 2026-03-03. Only maintained first-party Python Discord library. |
| `anthropic` | `0.86.0` | Claude Vision API client — send board screenshots, receive structured JSON | Official Anthropic SDK. `AsyncAnthropic` client required (sync client blocks asyncio loop). Type safety, automatic retries, rate-limit handling. Python >=3.9. Released 2026-03-18. |

### Claude Model Selection (Shipped in v1.1)

Use **`claude-sonnet-4-6`** for all vision calls.

| Model | Input cost | Speed | Vision | Recommendation |
|-------|------------|-------|--------|----------------|
| `claude-sonnet-4-6` | $3/MTok | Fast | Yes | **Use this** — best cost/speed for structured extraction |
| `claude-haiku-4-5-20251001` | $1/MTok | Fastest | Yes | Only downgrade after accuracy validation on real boards |
| `claude-opus-4-6` | $5/MTok | Moderate | Yes | Overkill; unnecessary cost for board reading |

Haiku 3 (`claude-3-haiku-20240307`) retires April 19, 2026 — do not use.

### Supporting Libraries (Shipped in v1.1)

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `Pillow` | `12.1.1` | Screenshot preprocessing — resize, crop, format convert before Claude API call | Always — resize screenshots to <=1568px per edge before encoding |
| `opencv-python` | `4.13.0.92` | Board tile contour detection and canvas blank detection | Always for vision pipeline; also used in v1.2 turn detection |
| `python-dotenv` | `1.2.2` | Load `DISCORD_TOKEN`, `ANTHROPIC_API_KEY`, and new `DISCORD_PLAYER_TOKEN` from `.env` | Always — never hardcode secrets |
| `aiosqlite` | `0.22.1` | Async SQLite — persist per-channel settings, game session state | Use for settings and game session tracking in v1.2 |
| `loguru` | `0.7.3` | Structured logging | Critical for debugging automation timing and vision extraction failures |

### Development Tools (Shipped in v1.1)

| Tool | Purpose | Notes |
|------|---------|-------|
| `playwright install chromium` | Download Chromium binary | Run once after `pip install patchright` (patchright bundles same Chromium) |
| `pytest-asyncio >=0.23` | Async test support | `asyncio_mode = "auto"` in pytest.ini |
| `pyright` / `pylance` | Type checking | playwright and patchright ship type stubs |

---

## Installation

```bash
# New dependencies for v1.2 (add to existing requirements)
pip install "patchright==1.58.2"

# One-time browser install (Chromium only — patchright uses same binary as playwright)
python -m patchright install chromium

# numpy is already present as a transitive dependency of opencv-python
# Verify: python -c "import numpy; print(numpy.__version__)"
```

**Note on patchright vs playwright install:** If both are installed, they share the same Chromium binary. Only one `install chromium` command is needed. Patchright does not require a separate browser download.

---

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| `patchright 1.58.2` | `playwright 1.58.0` (vanilla) | Use vanilla playwright if patchright introduces async API incompatibilities. The import change is the only difference — rollback is one line. |
| `patchright 1.58.2` | `selenium` | Never for this project. No native async support; brittle with Discord's React SPA; slower startup; requires separate WebDriver binary management. |
| `launch_persistent_context(user_data_dir=...)` | `storage_state` JSON | Use storage_state only if the user_data_dir approach causes file-lock issues on Windows. Tradeoff: storage_state doesn't preserve Chrome-level session caches, so Discord may re-prompt authentication more frequently. |
| `page.mouse.click(x, y)` for canvas | `locator.click(position={...})` | Use `locator.click(position=...)` when a canvas locator is available and coordinates are relative to the canvas element. `page.mouse.click()` is preferred for absolute coordinate math from the vision pipeline output. |
| Screenshot bytes + OpenCV blank detection | `page.evaluate()` canvas pixel read | Use `page.evaluate()` only if the Activity iframe is same-origin (allowing `getContext('2d').getImageData()`). For cross-origin Discord Activity iframes, `getImageData()` throws a SecurityError. Screenshot approach is safe in both cases. |
| `asyncio.sleep()` polling for turn detection | Playwright `expect(locator).to_have_attribute()` | DOM-based waits are cleaner but require a DOM element reflecting turn state. Letter League is canvas-rendered with no such element — screenshot polling is the only option. |

---

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| `playwright.sync_api` inside discord.py | Raises hard runtime error: "It looks like you are using Playwright Sync API inside the asyncio loop." discord.py owns the event loop; sync Playwright tries to create a new one. | `patchright.async_api` with `async_playwright()` throughout |
| `discord-self` / `discum` / any self-bot library | Automating a user account via a bot-token-style API violates Discord TOS. Discord explicitly prohibits self-bots and actively enforces bans. The autonomous play feature uses a **dedicated human account** operated via the browser (not the Discord bot API). | Playwright browser session logged in as a real user account |
| `async with async_playwright() as p:` for long-lived sessions | The context manager calls `playwright.stop()` on exit, closing all browsers. For a game session spanning minutes, the browser would close when the `async with` block ends. | `pw = await async_playwright().start()` + manual `await pw.stop()` in `bot.close()` |
| `threading` with Playwright | Playwright is single-threaded by design. Running Playwright in a thread alongside discord.py's asyncio loop causes `greenlet.error: cannot switch to a different thread`. | `patchright.async_api` natively within discord.py's asyncio loop |
| `PyAutoGUI` for click automation | Screen-coordinate clicking breaks on window repositioning, resolution changes, or partial visibility. No concept of DOM, waits, or element visibility. Requires a real display at known coordinates. | Playwright/patchright `page.mouse.click()` which operates on the browser's internal coordinate system regardless of window position |
| `selenium` | No native async support; brittle with Discord's React SPA; slower startup; requires ChromeDriver binary separate from browser | `patchright 1.58.2` async API |
| `requests` / any sync HTTP inside discord.py | Blocking in asyncio event loop. Halts entire bot during network calls. | `anthropic.AsyncAnthropic`, `aiohttp` |
| Headless mode (`headless=True`) for Discord | Discord's web client and Activity iframes detect headless Chromium via canvas fingerprinting, WebGL renderer string, and navigator properties. Known to trigger "Something went wrong" or blank Activity loads. | `headless=False` with patchright (which additionally patches CDP fingerprint leaks) |
| Committing `cache/browser_profile/` | Contains Discord session cookies and tokens. Exposure = account compromise. | Add `cache/browser_profile/` to `.gitignore` |
| `claude-3-haiku-20240307` (Haiku 3) | Deprecated. Retiring April 19, 2026. | `claude-haiku-4-5-20251001` if cost is the priority |

---

## Stack Patterns by Variant

**Autonomous mode — full browser session lifecycle:**
- `launch_persistent_context(user_data_dir="cache/browser_profile", headless=False)` on bot startup
- Store browser context on `bot` instance; reuse across game sessions
- Log in manually once to populate `cache/browser_profile/`; all subsequent restarts reuse the session
- Navigate with `page.goto(f"https://discord.com/channels/{guild_id}/{channel_id}")`
- Locate Activity iframe with `page.frame_locator('iframe[src*="activities"]')`
- Screenshot loop: capture → blank check → vision pipeline → move gen → click tiles

**Autonomous mode — turn detection loop:**
- Poll `page.screenshot(clip=rack_region)` every 2 seconds
- Compare bytes directly (`current != last`) for fast no-diff case
- On change: run full vision pipeline → select move → place tiles
- No DOM event listener available (canvas-rendered game)

**Development / debugging mode:**
- `headless=False` always (required for Discord)
- `slow_mo=50` in `launch_persistent_context` to slow clicks for visual inspection
- `page.pause()` for interactive Playwright Inspector breakpoints

**If patchright causes compatibility issues:**
- Revert: change `from patchright.async_api import async_playwright` back to `from playwright.async_api import async_playwright`
- No other code changes required

---

## Version Compatibility

| Package | Compatible With | Notes |
|---------|-----------------|-------|
| `patchright 1.58.2` | Python >=3.9 | Python 3.10 (project runtime) fully supported |
| `patchright 1.58.2` | `discord.py 2.7.1` | Both use asyncio; patchright async API runs in discord.py's event loop without conflict |
| `patchright 1.58.2` | `opencv-python 4.13.0.92` | No interaction; both used independently in the automation pipeline |
| `patchright 1.58.2` | Windows ProactorEventLoop | Python 3.10 on Windows auto-uses ProactorEventLoop; required by Playwright/patchright. No manual configuration needed. |
| `discord.py 2.7.1` | Python 3.10 | Fully compatible |
| `anthropic 0.86.0` | Python 3.10 | Fully compatible; `AsyncAnthropic` required |
| `Pillow 12.1.1` | Python 3.10 | No conflicts |
| `opencv-python 4.13.0.92` | Python 3.10 | No conflicts |

---

## Environment Variables (v1.2 additions)

| Variable | Purpose | Notes |
|----------|---------|-------|
| `BROWSER_PROFILE_PATH` | Path to Playwright persistent context user data dir | Default: `cache/browser_profile`. Add to `.gitignore`. |
| `DISCORD_PLAYER_ACCOUNT_EMAIL` | Email for the Discord player account used in auto-play | Only needed for initial manual login setup; not read by the bot at runtime once the profile is saved. |

The bot does NOT read the player account credentials at runtime. Credentials are entered manually during the one-time browser login setup. The persistent context saves the resulting session.

---

## Sources

- [playwright PyPI](https://pypi.org/project/playwright/) — v1.58.0, released 2026-01-30, Python >=3.9 (HIGH confidence)
- [patchright PyPI](https://pypi.org/project/patchright/) — v1.58.2, released 2026-03-07, drop-in Playwright replacement, Chromium-only (HIGH confidence)
- [Playwright Auth docs](https://playwright.dev/python/docs/auth) — `storage_state` vs `launch_persistent_context` tradeoffs (HIGH confidence — official docs)
- [Playwright BrowserType API](https://playwright.dev/python/docs/api/class-browsertype) — `launch_persistent_context` parameters, `user_data_dir` semantics (HIGH confidence — official docs)
- [Playwright FrameLocator API](https://playwright.dev/python/docs/api/class-framelocator) — iframe addressing, `content_frame`, strictness behavior (HIGH confidence — official docs)
- [Playwright Screenshots docs](https://playwright.dev/python/docs/screenshots) — `clip` parameter, bytes return, element screenshots (HIGH confidence — official docs)
- [Playwright Evaluating JS docs](https://playwright.dev/python/docs/evaluating) — `page.evaluate()` API, cross-environment isolation, canvas pixel data pattern (HIGH confidence — official docs)
- [Playwright Locator API](https://playwright.dev/python/docs/api/class-locator) — `click(position=...)`, `bounding_box()`, `page.mouse.click()` (HIGH confidence — official docs)
- [playwright-python issue #1418](https://github.com/microsoft/playwright-python/issues/1418) — confirms single-threaded design; `async_playwright().start()` pattern for long-lived sessions (HIGH confidence)
- [Discord channel URL format](https://support.discord.com/hc/en-us/articles/206346498) — `https://discord.com/channels/{guild_id}/{channel_id}` confirmed standard format (HIGH confidence)
- [Discord Self-Bot TOS Policy](https://support.discord.com/hc/en-us/articles/115002192352) — confirms self-bots prohibited; browser automation of a user account is the required (and risky) approach (HIGH confidence)
- [Patchright vs Playwright comparison — DEV Community](https://dev.to/claudeprime/patchright-vs-playwright-when-to-use-the-stealth-browser-fork-382a) — CDP leak patching, drop-in replacement API (MEDIUM confidence — third-party)

---

*Stack research for: Letter League Bot v1.2 — Browser Automation + Autonomous Play*
*Researched: 2026-03-24*
