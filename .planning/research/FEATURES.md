# Feature Research

**Domain:** Browser automation + autonomous play for Discord word game AI bot (v1.2)
**Researched:** 2026-03-24
**Confidence:** MEDIUM (Playwright patterns: HIGH; Discord Activity canvas specifics: MEDIUM; turn detection heuristics: LOW)

---

## Scope

This document covers **v1.2 features only**: browser automation and autonomous play.

Already shipped and treated as stable dependencies:
- GADDAG word engine + move generation + difficulty system (v1.0)
- Claude Vision board extraction pipeline (v1.1)
- Discord advisor bot with /analyze, /setdifficulty, /setmode (v1.1)

The autonomous mode must reuse the v1.1 vision pipeline exactly — screenshot bytes flow in, BoardState flows out. No second vision implementation.

---

## Feature Landscape

### Table Stakes (Without These, Autonomous Mode Cannot Function)

| Feature | Why Expected | Complexity | Existing Dependency |
|---------|--------------|------------|---------------------|
| Persistent Playwright browser session | Bot must survive restarts without re-login; a fresh browser state on every run makes Discord login interactive — unusable in production | MEDIUM | None — new infrastructure |
| Headless-detection bypass (headed + virtual display) | Discord web reliably detects and rejects headless Chromium; Activities may refuse to load; the PROJECT.md explicitly notes this | LOW | Requires OS-level virtual display (Xvfb on Linux, existing display on Windows) |
| Navigate to Discord web voice channel | Bot must arrive at the correct voice channel URL before the Activity is accessible | MEDIUM | None — DOM navigation |
| Open Letter League Activity (iframe) | Activity exists inside a dynamically injected iframe; it must be triggered to load before any game interaction is possible | HIGH | None — requires clicking Discord UI to launch Activity |
| Wait for Activity iframe to fully load | Canvas does not render instantly; premature screenshots return a blank or loading state; must detect ready state | MEDIUM | Playwright `frame_locator()` + `wait_for_load_state()` |
| Capture non-blank canvas screenshot from iframe | The entire autonomous pipeline starts here — screenshot bytes must be captured from the Activity canvas, not the Discord UI | HIGH | Feeds existing v1.1 vision pipeline unchanged |
| Pass screenshot to existing vision pipeline | v1.1 `extract_board_state()` already handles bytes-in, BoardState-out; must wire Playwright screenshot bytes to this exact call | LOW | Requires v1.1 vision pipeline (already built) |
| Turn detection (visual polling) | The bot must not act on other players' turns; Discord Activities expose no API; must infer "my turn" from visual state | HIGH | None — new problem; no existing component |
| Tile rack click (select tile from rack) | Physical click on a rack tile to select it for placement; coordinates derived from iframe bounding box + rack region offset | HIGH | Requires pixel coordinate mapping (see below) |
| Board cell click (place selected tile) | Physical click on target board cell; coordinates derived from board grid geometry | HIGH | Requires pixel coordinate mapping + move output from engine |
| Play confirmation click | Letter League has a confirm/submit button after tile placement; must be located and clicked | MEDIUM | Visual identification required — no DOM anchor |
| Asyncio-compatible game loop | discord.py and Playwright both require asyncio; the play loop must be async-native and must not block the bot's event loop | MEDIUM | Requires async Playwright API (`async_playwright`) — sync API is incompatible with discord.py's event loop |

### Differentiators (Competitive Advantage)

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Pre-computed pixel coordinate map | Compute board cell pixel positions once at game start by detecting grid lines or board origin; reuse for all subsequent moves without re-computing per turn | HIGH | OpenCV on the captured canvas screenshot can detect grid intersections; store as `dict[(row, col)] -> (x, y)` relative to iframe origin |
| Blank-frame detection before vision call | Detect and skip blank/loading canvas frames before sending to Claude Vision API; avoids wasted API calls during game startup or turn transitions | LOW | Compare mean pixel value of canvas region to a threshold; `numpy.mean(img_array) < 10` catches black/blank frames cheaply |
| Human-like timing jitter on actions | Random delays between action steps (tile select, board click, confirm) make the bot look less mechanical and reduce bot-detection risk | LOW | `asyncio.sleep(random.uniform(0.5, 2.0))` between each click; trivial to add |
| Graceful reconnect on session drop | If the browser session dies or the Activity disconnects, the bot re-navigates and re-joins without manual restart | MEDIUM | Wrap the main game loop in a try/except; on failure, navigate from Discord homepage, re-join voice channel, re-open Activity |
| Tile swap fallback when no good move | When the engine returns no valid moves above a quality threshold, choose the swap action (if available) rather than passing; uses existing difficulty engine | MEDIUM | Check move list; if empty or best score below configurable floor, locate and click the swap UI |
| Separate browser subprocess from bot process | Run the Playwright browser in a subprocess or thread so that a browser crash does not kill the discord.py bot process | MEDIUM | Use `asyncio.create_task()` for the game loop; isolation means the bot stays alive and can report errors to Discord even when the browser fails |

### Anti-Features (Commonly Requested, Often Problematic)

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Selfbot / user-account gateway automation (discord.py-self) | Simpler than browser automation; no need for Playwright | Discord explicitly bans automated user accounts (TOS §4); enforcement is active and results in permanent account termination; confirmed by Discord's own policy page | Playwright controlling Discord web in Chromium is the correct path — it mimics a human using a browser, not an API client |
| Headless Chromium in production | Saves memory; simpler to run on a server | Discord web detects headless fingerprints via JavaScript (`navigator.webdriver`, missing plugins, zero-size screen dimensions); Activities may refuse to load or render blank | Use `headless=False` with a virtual framebuffer (`Xvfb` on Linux, or the existing desktop display on Windows during development) |
| Multiple concurrent autonomous sessions | Play multiple games simultaneously | Each session requires a separate Discord user account and browser context; multiplies TOS risk; Playwright resource cost scales linearly; debugging becomes extremely hard | Hard constraint: one session only for v1.2; document this explicitly |
| DOM scraping for game state | "Query the Activity DOM instead of screenshotting" | Letter League renders its game board on an HTML5 canvas element inside an iframe; there is no DOM tree representing tile positions or the board grid — it is pixel data only | Screenshots + vision pipeline is the only viable path; DOM scraping is not applicable |
| Polling every frame (60fps screenshot loop) | "Maximum responsiveness" | Claude Vision API takes 4-15 seconds per call; screenshot capture at 60fps generates ~60 identical frames per second that all route to the same queue; wastes CPU and API credits with zero benefit | Poll at 1-2 second intervals with blank-frame detection; only invoke the vision pipeline when a visual change is detected |
| Re-implementing vision pipeline for autonomous mode | "Different pipeline for auto-play" | The v1.1 vision pipeline was built and validated for this exact purpose (bytes in, BoardState out); duplicating it creates two code paths to maintain | Wire Playwright screenshot bytes directly into `extract_board_state()` — zero code changes to the vision module |
| Storing canvas state as DOM attributes | "Persist board state between turns without re-screenshotting" | Canvas has no accessible DOM state; JavaScript evaluation can read `canvas.toDataURL()` but this returns the same pixel data the Playwright screenshot captures, with higher complexity | Re-screenshot and re-parse each turn; the 4-15s vision call is within the turn time limit of a word game |
| Click automation via PyAutoGUI or pywin32 | "Simpler than Playwright for clicks" | System-level click automation cannot target iframes inside a specific browser window; would click on whatever is under the cursor globally | Playwright's `page.mouse.click(x, y)` or `locator.click(position=...)` target the browser context directly, no global coordinates needed |

---

## Feature Dependencies

```
[v1.0 Engine: GADDAG, MoveGenerator, DifficultyEngine, Scorer]
    (already built — library dependency)

[v1.1 Vision Pipeline: extract_board_state(bytes) -> (BoardState, RackState)]
    (already built — reused unchanged)

[v1.1 Discord Bot: discord.py process, slash commands, channel state]
    (already built — autonomous mode runs alongside it)

[Persistent Browser Session]
    └──requires──> [Playwright chromium launch_persistent_context]
    └──requires──> [Initial manual Discord login to create session file]
    └──produces──> [Active browser context for all subsequent features]

[Activity Iframe Load]
    └──requires──> [Persistent Browser Session]
    └──requires──> [Navigate to voice channel URL]
    └──requires──> [Click to open Letter League Activity]
    └──produces──> [Accessible iframe with canvas]

[Canvas Screenshot Capture]
    └──requires──> [Activity Iframe Load]
    └──requires──> [Wait for non-blank canvas frame]
    └──produces──> [PNG bytes for vision pipeline]

[Board State Extraction]
    └──requires──> [Canvas Screenshot Capture]
    └──requires──> [v1.1 Vision Pipeline] ← reused unchanged
    └──produces──> [BoardState + RackState]

[Move Selection]
    └──requires──> [Board State Extraction]
    └──requires──> [v1.0 MoveGenerator + DifficultyEngine]
    └──produces──> [Selected Move with word, positions, score]

[Pixel Coordinate Map]
    └──requires──> [Canvas Screenshot Capture] ← built once at game start
    └──requires──> [OpenCV grid detection on canvas image]
    └──produces──> [dict[(row,col)] -> (iframe_x, iframe_y)]

[Tile Placement]
    └──requires──> [Move Selection]
    └──requires──> [Pixel Coordinate Map]
    └──requires──> [Turn Detection (bot is active)]
    └──produces──> [Tiles placed on board, pending confirmation]

[Turn Detection]
    └──requires──> [Canvas Screenshot Capture] ← periodic polling
    └──requires──> [Visual change detection (pixel diff or rack state change)]
    └──produces──> [Signal: my_turn = True/False]

[Play Confirmation]
    └──requires──> [Tile Placement]
    └──requires──> [Confirm button location (visual or DOM)]
    └──produces──> [Word submitted, turn complete]

[Autonomous Game Loop]
    └──requires──> [All above features]
    └──enhances──> [Discord bot] ← loop runs as asyncio task alongside bot
    └──conflicts──> [Selfbot approach] ← mutually exclusive architectures
```

### Dependency Notes

- **Pixel coordinate mapping is the highest-risk new problem.** The game board renders on a canvas; cell positions are pixel-based with no DOM backing. The coordinate map must be computed from the canvas screenshot using grid detection (OpenCV line detection or fixed-offset arithmetic from the detected board origin). This blocks all tile placement.

- **Turn detection has no API.** Discord Activities expose no WebSocket events or DOM mutations that signal "it is now player X's turn." The bot must infer its turn from visual changes — likely: the rack tiles change appearance (become highlighted or active) when it is the bot's turn, or a "your turn" indicator appears. This requires empirical investigation against a live game.

- **The asyncio constraint is hard.** Discord.py runs on an asyncio event loop. Playwright's sync API blocks the event loop. All Playwright calls must use `async_playwright()` and be awaited. The game loop must be `asyncio.create_task()` so it runs concurrently with discord.py's event processing.

- **Vision pipeline is reused without changes.** `extract_board_state(img_bytes, mode=state.mode)` from v1.1 is the exact interface. Autonomous mode captures screenshot bytes from Playwright and passes them directly to this function. No new vision code.

- **Initial login is a one-time manual step.** The `launch_persistent_context(user_data_dir=...)` approach saves the authenticated session to disk. The first run requires a human to log into Discord web in the browser window; subsequent runs load the saved session automatically.

---

## MVP Definition

### Launch With (v1.2 — Autonomous Mode Core)

Minimum viable autonomous play. The bot must complete at least one full turn without human intervention.

- [ ] **Persistent Playwright session** — `launch_persistent_context` with `user_data_dir`; headed mode; saves Discord login across restarts
- [ ] **Voice channel navigation** — navigate to Discord web, join the correct voice channel by URL or name
- [ ] **Activity iframe load** — detect and wait for Letter League iframe to be ready; handle blank-frame state
- [ ] **Canvas screenshot capture** — capture bytes from the Activity canvas region; blank-frame detection before invoking vision
- [ ] **Vision pipeline wire-up** — pass screenshot bytes to existing `extract_board_state()`; no new vision code
- [ ] **Move selection** — pass BoardState + RackState to existing `find_all_moves()` + `DifficultyEngine.select_move()`
- [ ] **Pixel coordinate map** — compute board cell pixel positions from canvas screenshot at game start
- [ ] **Turn detection** — poll canvas screenshot; detect visual change indicating bot's turn (rack highlight or turn indicator)
- [ ] **Tile placement** — click rack tile, click board cell for each letter in the selected word
- [ ] **Play confirmation** — locate and click the confirm/play button
- [ ] **Asyncio game loop** — the full loop runs as an `asyncio.create_task()` concurrent with the discord.py event loop

### Add After Core Loop Validates (v1.2.x)

Once one turn completes end-to-end without error.

- [ ] **Graceful reconnect** — re-navigate and re-join on session drop or Activity disconnect
- [ ] **Tile swap fallback** — when no valid moves exist, click swap UI instead of crashing
- [ ] **Human-like timing jitter** — random delays between actions
- [ ] **Blank-frame retry** — if vision returns an error on a blank canvas, wait and retry before failing
- [ ] **Discord status updates** — bot posts what move it played to a designated channel (for human observers)

### Future Consideration (v2+)

- [ ] **Multi-game session management** — defer; requires multiple Discord accounts and dramatically higher complexity
- [ ] **Adaptive turn detection** — ML-based pixel change detector instead of threshold polling; defer until threshold approach proves insufficient
- [ ] **Tile swap strategy integration with difficulty engine** — swap decisions that account for rack quality and game state; defer until core swap works

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Persistent browser session | HIGH | MEDIUM | P1 |
| Activity iframe load + wait | HIGH | HIGH | P1 |
| Canvas screenshot capture (non-blank) | HIGH | MEDIUM | P1 |
| Vision pipeline wire-up | HIGH | LOW | P1 |
| Pixel coordinate map (board cells) | HIGH | HIGH | P1 |
| Turn detection (visual polling) | HIGH | HIGH | P1 |
| Tile placement (rack + board clicks) | HIGH | HIGH | P1 |
| Play confirmation click | HIGH | MEDIUM | P1 |
| Asyncio game loop | HIGH | MEDIUM | P1 |
| Headed mode + detection bypass | HIGH | LOW | P1 |
| Graceful reconnect | MEDIUM | MEDIUM | P2 |
| Tile swap fallback | MEDIUM | MEDIUM | P2 |
| Human-like timing jitter | LOW | LOW | P2 |
| Discord status updates from autonomous mode | LOW | LOW | P2 |
| Multi-game / multi-session | LOW | VERY HIGH | P3 |

**Priority key:**
- P1: Required for one complete autonomous turn end-to-end
- P2: Required for sustained multi-turn play without human intervention
- P3: Future milestone

---

## Complexity Assessment

| Problem | Complexity | Why | Phase Risk |
|---------|------------|-----|------------|
| Persistent session + headed launch | MEDIUM | Well-documented Playwright API; main risk is Discord detecting the browser | LOW |
| Activity iframe navigation | HIGH | Discord UI is dynamic React; Activity launch sequence must be discovered empirically | HIGH |
| Canvas screenshot capture | MEDIUM | `page.screenshot(clip=...)` or `frame_locator().locator('canvas').screenshot()` — well-supported | MEDIUM |
| Vision pipeline wire-up | LOW | Same bytes-in/BoardState-out API as advisor mode; zero new code | LOW |
| Pixel coordinate mapping | HIGH | No DOM; must compute from pixel grid geometry; brittle to UI scaling changes | HIGH |
| Turn detection | HIGH | No API; pure visual heuristic; must discover what the "your turn" indicator looks like | HIGH |
| Tile placement clicks | HIGH | Depends on coordinate map accuracy; each letter in the word requires two clicks in sequence | HIGH |
| Play confirmation | MEDIUM | Confirm button likely visible in DOM or has a consistent visual; must locate it empirically | MEDIUM |
| Asyncio game loop | MEDIUM | Pattern is well-understood (asyncio.create_task); main risk is blocking calls sneaking in | MEDIUM |

---

## Sources

- [Playwright Python — launch_persistent_context](https://playwright.dev/python/docs/chrome-extensions) — persistent context with user_data_dir saves cookies, localStorage, session tokens across runs; headed mode required for extensions and Discord session. HIGH confidence.
- [Playwright Python — Frames](https://playwright.dev/python/docs/frames) — `page.frame_locator()` for iframe content; `wait_for_load_state()` for load detection; canvas inside iframe has no DOM — requires `evaluate()` or screenshot for state. HIGH confidence.
- [Playwright Python — Screenshots](https://playwright.dev/python/docs/screenshots) — `page.screenshot()` returns bytes without writing file; `clip` parameter for region capture; `locator.screenshot()` for element-specific capture. HIGH confidence.
- [Playwright Tips — Clicking at Offset](https://www.weekly.playwright-user-event.org/tip-11-clicking-at-an-offset-inside-an-element.html) — `locator.click(position={x, y})` for offset clicks within element bounding box; `page.mouse.click(x, y)` for absolute page coordinates. HIGH confidence.
- [Playwright Python — Authentication](https://playwright.dev/docs/auth) — `storageState` for session persistence; `launch_persistent_context(user_data_dir=...)` for full browser profile reuse. HIGH confidence.
- [Discord — Automated User Accounts (Self-Bots)](https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots) — Explicit TOS prohibition; automated user accounts result in permanent account termination. HIGH confidence.
- [Discord — How Activities Work](https://discord.com/developers/docs/activities/how-activities-work) — Activities load in an iframe within Discord; SDK handshake via postMessage; no programmatic API for game state. HIGH confidence.
- [BrowserStack — Playwright Bot Detection](https://www.browserstack.com/guide/playwright-bot-detection) — Headless Chromium exposes `navigator.webdriver`, zero plugins, screen dimension fingerprints; headed mode with real display avoids these signals. MEDIUM confidence.
- [Game automation loop patterns](https://ben.land/post/2021/05/21/automating-computer-games/) — Screenshot-analyze-click loop; decision tree against screen state; VNC virtual desktop for headless-but-not-headless execution. MEDIUM confidence.
- [Playwright — Frame Locator API](https://playwright.dev/python/docs/api/class-framelocator) — `page.frame_locator(selector)` creates auto-waiting iframe locator; strict mode throws if multiple frames match. HIGH confidence.
- [LambdaTest Community — iframe bounding box](https://community.lambdatest.com/t/how-can-you-get-the-bounding-box-of-an-iframe-in-playwright-to-capture-only-that-specific-area-in-a-screenshot/48022) — `elementHandle.boundingBox()` returns iframe position relative to main viewport; use with `page.screenshot(clip=...)` for region capture. MEDIUM confidence.

---

*Feature research for: Browser automation + autonomous play (v1.2)*
*Researched: 2026-03-24*
