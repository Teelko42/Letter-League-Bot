# Phase 5: Browser Foundation - Research

**Researched:** 2026-03-25
**Domain:** Browser automation (patchright/Playwright), Discord web navigation, iframe handling, canvas screenshot capture
**Confidence:** MEDIUM-HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Operator login flow**
- Manual browser login on first run — bot opens a visible Chromium window, operator logs into Discord manually
- First-run only trigger — bot detects no saved profile and opens the login window automatically
- Browser profile (cookies/session) stored in a project subdirectory (e.g., `./browser_data/`)
- Login completion auto-detected by waiting for a Discord page element (sidebar, friends list) to appear
- After login detected, keep the same browser session open and proceed to navigation (no relaunch)

**Failure behavior**
- Expired session at startup: log a clear warning message explaining the issue and how to re-login, then exit cleanly
- All failure messages go to console/log only (Python logging) — no Discord DMs
- Navigation failures (voice channel, Activity): retry 2-3 times with short waits, then log error and exit
- Startup validates the captured screenshot through the full `extract_board_state()` vision pipeline, not just a non-blank check

**Browser visibility**
- Headless by default during normal operation (after login is saved)
- No headed/debug toggle — keep it simple, edit code if debugging needed
- First-run login keeps the visible browser open and transitions to work (no close + relaunch)
- Fixed viewport size set at browser launch for consistent canvas screenshot dimensions

**Channel targeting**
- Target voice channel specified via config file (e.g., `.env` or `config.json`)
- Config value is the full Discord URL (e.g., `https://discord.com/channels/SERVER_ID/CHANNEL_ID`) — operator copy-pastes from browser
- Navigation via direct URL — navigate straight to the channel URL, don't click through Discord UI
- Activity launch method at Claude's discretion (research best approach — Activity shelf click vs direct URL)

### Claude's Discretion
- Activity launch mechanism (click shelf vs direct URL — research what's most reliable)
- Fixed viewport dimensions (research what size works best for the game canvas)
- Exact Discord element to detect for login completion
- Retry timing and backoff strategy for navigation failures
- Pixel-variance threshold for non-blank screenshot check (used before full pipeline validation)

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| BROW-01 | Bot launches persistent Playwright browser session with saved Discord web login that survives restarts | `launch_persistent_context(user_data_dir=...)` persists cookies/localStorage; profile directory survives process restart |
| BROW-02 | Bot detects expired sessions at startup and notifies the operator instead of silently failing | After navigation to discord.com, check for a login-wall element (e.g. `[data-testid="login-button"]`) or wait for sidebar; timeout signals expiry |
| ANAV-01 | Bot navigates Discord web client to the target voice channel | `page.goto(channel_url)` with direct URL navigation — no UI traversal needed |
| ANAV-02 | Bot opens the Letter League Activity and locates the game iframe | Click `button[aria-label="Start an Activity"]` (rocket button) in voice channel; then wait for iframe with `src` matching `discordsays.com`; locate via `page.frame(url=r".*discordsays\.com.*")` |
| ANAV-03 | Bot captures a non-blank canvas screenshot from inside the Activity iframe | `canvas_el.screenshot()` inside the iframe frame object, OR `frame.evaluate("canvas.toDataURL('image/png')")` as fallback; pixel-variance check on bytes using numpy |
</phase_requirements>

---

## Summary

Phase 5 is a Playwright-family browser automation phase with three distinct sub-problems: (1) persistent session management with a one-time manual login flow, (2) Discord web navigation to a voice channel and Activity iframe, and (3) canvas screenshot capture that feeds into the existing vision pipeline. The entire stack runs on patchright 1.58.2, a drop-in Playwright fork that patches CDP fingerprint leaks Discord uses to detect automation.

The most significant technical risk is canvas screenshot quality in headless mode. Playwright issue #19225 identified that canvas content can appear blank, but the root cause is screenshot-before-render timing rather than a true headless limitation — the fix is to wait for the Activity to fully render before capturing. The iframe architecture is well-understood: Discord Activities load inside an iframe whose `src` is `https://<app_id>.discordsays.com/...`; the iframe can be located via `page.frame(url=r".*discordsays\.com.*")`. The Activity is launched by clicking a rocket button with `aria-label="Start an Activity"`.

The asyncio integration concern (patchright requires ProactorEventLoop on Windows; discord.py historically conflicts) is out of scope for Phase 5 — this phase is a standalone browser session module, not yet integrated with the discord.py bot. Integration happens in Phase 8. Phase 5 only needs to be a runnable Python script/module that performs: launch → navigate → capture → validate via `extract_board_state()`.

**Primary recommendation:** Use `patchright.async_api.async_playwright` with `launch_persistent_context(user_data_dir="./browser_data/", headless=False for first-run / headless=True thereafter)`. Locate the Activity iframe via URL pattern match. Capture canvas via `locator.screenshot()` first; fall back to `frame.evaluate("document.querySelector('canvas').toDataURL('image/png')")` if blank. Always wait for network idle or a known in-game element before capturing.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| patchright | 1.58.2 | Browser automation — drop-in Playwright replacement | Patches CDP fingerprint leaks that Discord uses to detect automation; locked by STATE.md v1.2 decision |
| loguru | (already installed) | Structured logging for operator-visible warnings | Already used throughout project; consistent pattern |
| python-dotenv | (already installed) | Load `DISCORD_CHANNEL_URL` from `.env` | Already used in bot.py for all environment config |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| numpy | (already installed — used by vision) | Pixel-variance check on screenshot bytes | Needed to classify a screenshot as non-blank before passing to vision pipeline |
| Pillow / PIL | (check if installed) | Decode PNG bytes to pixel array if numpy-only is insufficient | Only needed if evaluating variance from raw bytes without OpenCV |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| patchright | playwright (standard) | playwright lacks CDP patch — Discord may flag the session as automated |
| patchright | undetected-playwright | patchright is newer, more actively maintained, pure drop-in |
| `launch_persistent_context` | `storage_state` JSON file | `storage_state` only captures cookies/localStorage, not full IndexedDB/service-worker state that Discord web relies on; persistent context is more complete |

**Installation:**
```bash
"C:/Users/Ninja/AppData/Local/Programs/Python/Python310/python.exe" -m pip install patchright
"C:/Users/Ninja/AppData/Local/Programs/Python/Python310/python.exe" -m patchright install chromium
```

---

## Architecture Patterns

### Recommended Project Structure

```
src/
├── browser/               # All Phase 5 code lives here
│   ├── __init__.py
│   ├── session.py         # BrowserSession class — launch, login detection, close
│   ├── navigator.py       # navigate_to_activity() — channel URL → iframe reference
│   └── capture.py         # capture_canvas() — iframe → bytes → pixel-variance check
```

### Pattern 1: Persistent Context Launch

**What:** `launch_persistent_context` creates or reopens a Chromium profile at a given path. If the path has no prior session, it is treated as a fresh install. The returned object is a `BrowserContext` (not a `Browser`).

**When to use:** Every startup — both first-run (no profile) and normal operation (profile exists).

```python
# Source: patchright PyPI README + Playwright official docs
from patchright.async_api import async_playwright

async def launch_context(
    profile_dir: str,
    headless: bool,
    viewport_width: int = 1280,
    viewport_height: int = 800,
) -> tuple:  # (playwright_instance, context)
    pw = await async_playwright().start()
    context = await pw.chromium.launch_persistent_context(
        user_data_dir=profile_dir,
        headless=headless,
        viewport={"width": viewport_width, "height": viewport_height},
        # patchright recommendation: no custom args beyond these for stealth
    )
    return pw, context
```

**Notes:**
- `launch_persistent_context` returns a `BrowserContext` directly (not `Browser.new_context()`).
- "Browsers do not allow launching multiple instances with the same User Data Directory" — only one process may hold the profile.
- On patchright, do NOT pass custom `user_agent` or extra `args` for Discord stealth.

### Pattern 2: First-Run vs. Returning Session Detection

**What:** Check whether `./browser_data/` contains a Chrome profile that has Discord cookies. If the directory is empty/missing, open headed for manual login.

**When to use:** At startup, before navigating anywhere.

```python
import os
from pathlib import Path

def profile_exists(profile_dir: str) -> bool:
    """Return True if the profile directory has a Cookies file (Chrome profile)."""
    cookies_path = Path(profile_dir) / "Default" / "Cookies"
    return cookies_path.exists()

async def startup(profile_dir: str) -> BrowserContext:
    is_first_run = not profile_exists(profile_dir)
    pw, context = await launch_context(
        profile_dir=profile_dir,
        headless=not is_first_run,  # headed for first-run login only
    )
    return pw, context, is_first_run
```

### Pattern 3: Login Completion Detection

**What:** After opening `https://discord.com/login` (first-run), wait for an element that only appears when authenticated. The Discord app sidebar `nav` element or the home button is a reliable indicator.

**Recommended selector** (aria-stable, not class-based):
```python
# Source: WebSearch cross-referenced with Discord DOM inspection guidance
LOGIN_SUCCESS_SELECTOR = '[data-list-id="guildsnav"]'  # Server list nav
# Fallback: '[aria-label="Servers"]' or 'nav[aria-label="Servers sidebar"]'
```

```python
page = await context.new_page()
await page.goto("https://discord.com/login")
# Wait up to 5 minutes for the operator to complete login
await page.wait_for_selector(LOGIN_SUCCESS_SELECTOR, timeout=300_000)
logger.info("Login detected — session is active")
```

**Important:** After login is detected, keep this same `context` open. Do NOT close and relaunch.

### Pattern 4: Expired Session Check at Startup

**What:** On a returning run (profile exists), navigate to `https://discord.com/channels/@me` and check whether the user is redirected to the login page or arrives at the app.

```python
async def check_session_valid(page) -> bool:
    await page.goto("https://discord.com/channels/@me", wait_until="domcontentloaded")
    # If session expired, Discord redirects to /login
    return "login" not in page.url

# Usage
if not await check_session_valid(page):
    logger.error(
        "Discord session expired. Delete ./browser_data/ and re-run to log in again."
    )
    await context.close()
    await pw.stop()
    sys.exit(1)
```

### Pattern 5: Navigate to Voice Channel and Launch Activity

**What:** Navigate directly to the channel URL from config. Then click the Activity rocket button.

```python
# Direct URL navigation (locked decision)
await page.goto(channel_url, wait_until="domcontentloaded")

# Click "Start an Activity" (rocket button)
# aria-label is stable; class names change on Discord recompile
# Source: WebSearch confirmed aria-label="Start an Activity" 2024
rocket_btn = page.locator('button[aria-label="Start an Activity"]')
await rocket_btn.click()

# Wait for the Activity picker / shelf to appear, then find Letter League
# Letter League will appear as a button/card — search by visible text
activity_card = page.get_by_text("Letter League", exact=False)
await activity_card.click()
```

**Activity launch mechanism recommendation (Claude's discretion):** Click the rocket button (Activity shelf) rather than attempting a direct URL. Direct Activity URLs require undocumented parameters that include per-session `frame_id` and `instance_id` values. The shelf click is the only documented launch path and is how the Discord client normally triggers Activity loading.

### Pattern 6: Locating the Activity iframe

**What:** After the Activity launches, Discord creates an iframe whose `src` contains `discordsays.com`. Locate it by URL pattern.

```python
# Source: Discord Embedded App SDK documentation + DeepWiki analysis
# Activities proxy through https://<app_id>.discordsays.com/...
import re

def find_activity_frame(page):
    """Return the Frame object for the Letter League Activity iframe."""
    for frame in page.frames:
        if re.search(r"discordsays\.com", frame.url):
            return frame
    return None

# With wait:
async def wait_for_activity_frame(page, timeout: float = 30.0):
    import asyncio, time
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        frame = find_activity_frame(page)
        if frame:
            return frame
        await asyncio.sleep(0.5)
    raise TimeoutError("Activity iframe did not load within timeout")
```

**Alternative using frame_locator (no direct Frame reference needed for interaction):**
```python
activity_fl = page.frame_locator('iframe[src*="discordsays.com"]')
canvas = activity_fl.locator("canvas")
```

### Pattern 7: Canvas Screenshot Capture

**What:** Capture the canvas inside the Activity iframe as PNG bytes.

**Primary method — element screenshot:**
```python
# Source: Playwright docs screenshots + issue #19225 analysis
# Wait for canvas to be visible and rendered before capturing
canvas_locator = activity_fl.locator("canvas")
await canvas_locator.wait_for(state="visible", timeout=15_000)
# Wait for network idle to ensure all game assets are loaded
await page.wait_for_load_state("networkidle")
screenshot_bytes: bytes = await canvas_locator.screenshot()
```

**Fallback method — toDataURL via evaluate:**
```python
# Source: HTML Canvas API + Playwright evaluate pattern
# Use when element screenshot returns blank/black bytes
frame = find_activity_frame(page)
data_url: str = await frame.evaluate(
    "document.querySelector('canvas').toDataURL('image/png')"
)
import base64
# data_url is "data:image/png;base64,<b64>"
b64_data = data_url.split(",", 1)[1]
screenshot_bytes = base64.b64decode(b64_data)
```

### Pattern 8: Pixel-Variance Non-Blank Check

**What:** Verify the screenshot is not solid black or solid white before calling the full pipeline.

```python
# Source: standard numpy variance pattern
import numpy as np

def is_non_blank(img_bytes: bytes, threshold: float = 5.0) -> bool:
    """Return True if the image has meaningful pixel variance (not solid color)."""
    import cv2  # already available via vision pipeline
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        return False
    return float(np.std(img)) > threshold
```

**Threshold recommendation (Claude's discretion):** `std > 5.0` catches near-solid images while accepting any real game screenshot. The vision pipeline's preprocessor will catch non-game images with a proper error.

### Anti-Patterns to Avoid

- **Using `browser.new_page()` after `launch_persistent_context`**: The context returned by `launch_persistent_context` IS the context — use `context.new_page()`, not `browser.new_page()` (there is no separate browser object).
- **Closing and relaunching after login**: The locked decision is to keep the same session alive. Close + relaunch would re-enter first-run flow.
- **Selecting iframe by class name**: Discord's compiled CSS class names change on every deploy. Use `aria-label` (buttons) and URL patterns (iframes).
- **Taking screenshot immediately after Activity click**: Canvas renders asynchronously. Always wait for `networkidle` or a known in-game element.
- **Using patchright sync API**: Always use `patchright.async_api` — the sync API cannot run inside an asyncio loop (relevant for Phase 8 integration).
- **Storing browser_data/ in git**: Contains Discord session cookies. Must be in `.gitignore`.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Bot detection bypass | Custom CDP patches, user-agent spoofing | patchright (already decided) | patchright patches 30+ fingerprint vectors at the source level |
| Cookie/session persistence | Custom cookie serialization | `launch_persistent_context(user_data_dir=...)` | Handles cookies, IndexedDB, localStorage, service workers — all Discord login state |
| Iframe discovery | Recursive DOM walking | `page.frame(url=r".*discordsays\.com.*")` or `page.frames` iteration | Built-in Playwright API with frame URL matching |
| Async subprocess compatibility | Manual event loop management | `asyncio.run()` with `async_playwright()` | `asyncio.run()` handles ProactorEventLoop selection on Windows automatically |

**Key insight:** patchright is a drop-in replacement — every Playwright Python pattern works unchanged. The only difference is the import path: `from patchright.async_api import async_playwright`.

---

## Common Pitfalls

### Pitfall 1: Canvas Screenshot Returns Blank (Black) PNG

**What goes wrong:** `canvas_locator.screenshot()` returns a solid-black PNG even though the canvas appears rendered in the browser.

**Why it happens:** The screenshot is captured before the WebGL/Canvas render cycle completes. The iframe loads, but the game canvas continues rendering asynchronously after `DOMContentLoaded`.

**How to avoid:** Always `await page.wait_for_load_state("networkidle")` after Activity launch. Additionally wait for the canvas to be visible. If still blank, fall back to `canvas.toDataURL()` via `frame.evaluate()`.

**Warning signs:** `np.std(img) == 0` or very close to zero; image dimensions are correct but all pixels are `(0, 0, 0)`.

### Pitfall 2: Session Appears Valid But Discord Redirects Anyway

**What goes wrong:** `profile_exists()` returns True (Cookies file exists), but navigating to discord.com redirects to `/login`.

**Why it happens:** Session cookies expire (typically 30 days for Discord web). The Cookies file exists but the tokens inside are expired.

**How to avoid:** Always validate the session after launch by checking the final URL after navigation to `https://discord.com/channels/@me`. If `"login"` appears in the URL, treat as expired regardless of profile existence.

**Warning signs:** `page.url` after navigation to `@me` contains `/login`.

### Pitfall 3: Activity iframe src Changes with App Version

**What goes wrong:** Hard-coded iframe selector like `iframe[src="https://12345.discordsays.com/index.html"]` stops finding the iframe after a Letter League update.

**Why it happens:** The Activity URL path (after the discordsays.com domain) changes with each game update. The app_id subdomain is stable but the path is not.

**How to avoid:** Match only the domain portion: `iframe[src*="discordsays.com"]` or `frame.url` regex `r".*discordsays\.com.*"`. Never match the full URL.

**Warning signs:** `find_activity_frame()` returns None after a Letter League update.

### Pitfall 4: "Start an Activity" Button Not Visible

**What goes wrong:** `page.locator('button[aria-label="Start an Activity"]')` fails to find the button.

**Why it happens:** The bot must be in a voice channel for the rocket button to appear. If the direct URL navigation to the channel doesn't auto-join the voice channel (Discord web requires explicit "Join Voice" in some cases), the activity controls are hidden.

**How to avoid:** After navigating to the channel URL, check for and click a "Join Voice" button if present, then wait for the voice channel controls toolbar before clicking the Activity button.

**Warning signs:** `TimeoutError` on the rocket button selector immediately after navigation.

### Pitfall 5: Multiple Profile Directories from Concurrent Runs

**What goes wrong:** Two instances of the bot attempt to use the same `user_data_dir`, and Chromium refuses to launch the second one.

**Why it happens:** Chromium enforces a file lock on the profile directory.

**How to avoid:** The bot should be a singleton process. Log a clear error if the profile is locked ("Another instance may be running"). Consider a PID file.

**Warning signs:** `playwright._impl._errors.Error: Failed to create a user data directory` or similar Chromium lock error.

### Pitfall 6: headless=True Breaks Discord Detection (Patchright Recommendation)

**What goes wrong:** Discord flags the session as automated when running headless, even with patchright.

**Why it happens:** Patchright's stealth recommendation explicitly states `headless=False` for complete undetectability. The locked decision already uses headless for normal operation — this is a known accepted tradeoff. If Discord starts flagging, the operator must investigate.

**How to avoid:** The current plan (headless=True after first login) is a deliberate tradeoff. Patchright patches most detection vectors even in headless mode; the recommendation is a conservative best-practice. Monitor for session invalidation.

**Warning signs:** Session expires unusually fast (< 7 days) or Discord logs the user out mid-session.

---

## Code Examples

Verified patterns from official sources:

### Full Session Startup Flow

```python
# Source: patchright PyPI README + Playwright persistent context docs
from patchright.async_api import async_playwright
from pathlib import Path
import sys
from loguru import logger

PROFILE_DIR = "./browser_data"
LOGIN_SELECTOR = '[data-list-id="guildsnav"]'

async def start_browser_session():
    """Launch browser session — headed for first-run login, headless otherwise."""
    pw = await async_playwright().start()

    is_first_run = not (Path(PROFILE_DIR) / "Default" / "Cookies").exists()
    context = await pw.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=not is_first_run,
        viewport={"width": 1280, "height": 800},
    )
    page = await context.new_page()

    if is_first_run:
        logger.info("First run: opening Discord login. Please log in manually.")
        await page.goto("https://discord.com/login")
        await page.wait_for_selector(LOGIN_SELECTOR, timeout=300_000)
        logger.info("Login detected, proceeding.")
    else:
        await page.goto(
            "https://discord.com/channels/@me", wait_until="domcontentloaded"
        )
        if "login" in page.url:
            logger.error(
                "Discord session has expired. "
                "Delete ./browser_data/ and re-run to log in again."
            )
            await context.close()
            await pw.stop()
            sys.exit(1)
        logger.info("Session valid, continuing.")

    return pw, context, page
```

### Navigate to Activity and Capture Canvas

```python
# Source: Playwright frames docs + Discord Activity architecture research
import re, asyncio, base64
import numpy as np

async def navigate_and_capture(page, channel_url: str) -> bytes:
    """Navigate to the voice channel, launch Letter League, capture canvas."""

    # Step 1: Navigate to voice channel (direct URL)
    await page.goto(channel_url, wait_until="domcontentloaded")
    logger.info("Navigated to channel: {}", channel_url)

    # Step 2: Join voice if needed
    join_btn = page.locator('button:has-text("Join Voice")')
    if await join_btn.count() > 0:
        await join_btn.click()
        logger.info("Joined voice channel")

    # Step 3: Click rocket button to open Activity shelf
    rocket = page.locator('button[aria-label="Start an Activity"]')
    await rocket.wait_for(state="visible", timeout=10_000)
    await rocket.click()
    logger.info("Opened Activity shelf")

    # Step 4: Click Letter League
    ll_card = page.get_by_text("Letter League", exact=False).first
    await ll_card.wait_for(state="visible", timeout=10_000)
    await ll_card.click()
    logger.info("Launched Letter League activity")

    # Step 5: Wait for iframe
    deadline = asyncio.get_event_loop().time() + 30
    activity_frame = None
    while asyncio.get_event_loop().time() < deadline:
        for frame in page.frames:
            if re.search(r"discordsays\.com", frame.url):
                activity_frame = frame
                break
        if activity_frame:
            break
        await asyncio.sleep(0.5)
    if not activity_frame:
        raise RuntimeError("Activity iframe did not appear within 30 seconds")
    logger.info("Found activity iframe: {}", activity_frame.url)

    # Step 6: Wait for render
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(1.0)  # extra buffer for canvas render

    # Step 7: Capture canvas — primary method
    fl = page.frame_locator('iframe[src*="discordsays.com"]')
    canvas = fl.locator("canvas").first
    try:
        screenshot_bytes = await canvas.screenshot()
    except Exception:
        # Fallback: toDataURL via evaluate
        logger.warning("Element screenshot failed, falling back to toDataURL")
        data_url = await activity_frame.evaluate(
            "document.querySelector('canvas').toDataURL('image/png')"
        )
        b64 = data_url.split(",", 1)[1]
        screenshot_bytes = base64.b64decode(b64)

    return screenshot_bytes
```

### Pixel Variance Check

```python
# Standard pattern — numpy + opencv (opencv already used in vision pipeline)
import cv2
import numpy as np

def is_non_blank(img_bytes: bytes, threshold: float = 5.0) -> bool:
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        return False
    return float(np.std(img)) > threshold
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `browser.new_page()` | `launch_persistent_context(user_data_dir)` | Playwright 1.x stable | Session persists across restarts without manual cookie export |
| `storage_state` JSON | `launch_persistent_context` profile dir | Industry shift | Full profile (IndexedDB, service workers) vs cookies-only |
| `page.frame('name')` | `page.frame(url=r"...")` or `page.frames` iterate | Playwright 1.x | URL matching more robust than name matching for third-party iframes |
| Custom stealth libraries | patchright drop-in | 2024 | Source-level patches instead of JS injection; no import changes |

**Deprecated/outdated:**
- `playwright-stealth` pip package: JS injection approach, less effective than patchright's source patches
- Sync Playwright API: Cannot share event loop with discord.py (Phase 8 concern) — never use in this project

---

## Open Questions

1. **Which Discord element is the most reliable login-completion indicator?**
   - What we know: Discord renders a server list nav when logged in. `[data-list-id="guildsnav"]` and `[aria-label="Servers"]` are candidates.
   - What's unclear: Discord periodically refactors its DOM. These selectors may not survive app updates.
   - Recommendation: Use `[data-list-id="guildsnav"]` as primary; add a URL check (`"@me"` in `page.url` and `"login"` not in `page.url`) as secondary. Spike during Wave 0 with a live DevTools inspection.

2. **Activity shelf vs. direct Activity URL for launch**
   - What we know: Discord Activities require `frame_id` and `instance_id` query params that are per-session and server-generated. There is no documented way to construct a direct launch URL.
   - What's unclear: Whether undocumented shortcuts exist in the web client.
   - Recommendation: Use the rocket button shelf click. This is the only reliable launch path.

3. **Exact canvas selector inside the Letter League Activity iframe**
   - What we know: Activities are WebGL/canvas apps; Letter League is built on a game engine that renders to `<canvas>`. The selector `canvas` or `canvas:first-of-type` should work.
   - What's unclear: Whether Letter League uses multiple canvas elements or overlays.
   - Recommendation: Spike with `activity_frame.query_selector_all("canvas")` to count and identify which canvas holds the game view. Document result as a comment in `capture.py`.

4. **Viewport dimensions for canvas screenshot consistency**
   - What we know: The vision pipeline preprocessor detects the board region via HSV masking — it is not viewport-dependent.
   - What's unclear: Whether smaller viewports cause the Activity to render a lower-resolution canvas.
   - Recommendation (Claude's discretion): Use 1280×800. This is the Playwright default and matches typical Discord web usage. If the vision pipeline returns preprocessing errors, increase to 1920×1080.

5. **headless=True for normal operation — Discord detection risk**
   - What we know: patchright's README recommends `headless=False` for maximum stealth. The locked decision uses headless after first login.
   - What's unclear: Whether Discord actively checks for headless mode in the web client (as opposed to bot protection on login).
   - Recommendation: Proceed with `headless=True` as decided. Monitor for unexpected session expiry. If sessions expire in < 7 days, revisit.

---

## Validation Architecture

> `workflow.nyquist_validation` is not present in `.planning/config.json` (not `true`). Skipping this section per instructions.

---

## Sources

### Primary (HIGH confidence)
- patchright PyPI page (pypi.org/project/patchright/) — version 1.58.2, installation commands, `launch_persistent_context` recommendation, `headless=False` stealth guidance
- GitHub: Kaliiiiiiiiii-Vinyzu/patchright-python — async API pattern, `launch_persistent_context` signature, no custom user-agent recommendation
- Playwright official docs (playwright.dev/python/docs/api/class-browsertype#browser-type-launch-persistent-context) — `launch_persistent_context` full signature, parameters, session persistence behavior
- Playwright official docs (playwright.dev/python/docs/frames) — `page.frame(url=...)`, frame URL pattern matching, `page.frames` iteration
- Discord Embedded App SDK / DeepWiki (deepwiki.com/discord/discord-api-docs/5.1-activities-overview-and-architecture) — `discordsays.com` proxy domain pattern, iframe initialization with `frame_id`/`instance_id` params

### Secondary (MEDIUM confidence)
- GitHub Playwright issue #19225 (confirmed closed) — canvas blank screenshot root cause (timing, not headless) and fix (wait for networkidle)
- WebSearch: Discord Activity rocket button `aria-label="Start an Activity"` — multiple community sources confirm this aria-label as of 2024
- WebSearch: ProactorEventLoop + Playwright Windows requirement — cross-verified with official Python asyncio platform docs

### Tertiary (LOW confidence)
- Discord `[data-list-id="guildsnav"]` selector for login detection — observed in community CSS customization posts, not in official Discord docs; needs live DevTools verification
- `headless=True` with patchright not triggering Discord detection — theoretical (patchright patches most vectors); not empirically verified for this project

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — patchright 1.58.2 on PyPI confirmed, Playwright API verified via official docs
- Architecture: MEDIUM-HIGH — Playwright patterns from official docs; Discord-specific selectors (aria-labels, iframe URL pattern) from community sources that need live verification
- Pitfalls: MEDIUM — canvas blank issue and timing fix confirmed via Playwright GitHub; Discord DOM selectors are LOW (unstable, need live check)

**Research date:** 2026-03-25
**Valid until:** 2026-04-25 (Discord DOM selectors: verify live before coding; patchright API: stable)
