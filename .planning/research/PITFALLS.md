# Pitfalls Research

**Domain:** Browser automation + autonomous play addition to existing Discord bot (Letter League Bot v1.2)
**Researched:** 2026-03-24
**Confidence:** MEDIUM-HIGH (Playwright async/canvas/iframe behaviors verified against official docs and GitHub issues; Discord Activity iframe selectors and turn-detection signals are LOW confidence — require live inspection)

---

## Critical Pitfalls

### Pitfall 1: Playwright Sync API Inside discord.py's Async Event Loop

**What goes wrong:**
Playwright ships two Python APIs: `sync_playwright()` and `async_playwright()`. discord.py owns an asyncio event loop from startup. Any code calling `sync_playwright()` inside a discord.py coroutine or event handler — or in a module imported by one — raises `RuntimeError: This event loop is already running` and freezes or crashes the bot. The bot appears to accept the command but never responds, and all subsequent commands also fail until the process is restarted.

**Why it happens:**
Playwright tutorials and the official Python quickstart default to the synchronous API because it is simpler to demonstrate. Developers who copy those examples into a discord.py bot hit the conflict immediately. The error message (`It looks like you are using Playwright Sync API inside the asyncio loop`) is clear only if the exception propagates; silent hangs are more common when the error is swallowed by a bare `except`. This is documented as the most frequent Python async integration issue in Playwright's GitHub issues (#462, #2053, #2705).

**How to avoid:**
Use `playwright.async_api` exclusively — never import `sync_playwright`. Every Playwright call must live inside `async def` functions using `async with async_playwright() as p:`. Launch the browser once at bot startup and keep the context alive across turns; do not re-launch per command. Use `await asyncio.to_thread()` only for CPU-bound Python work (e.g., word engine calls), not for Playwright — Playwright's async API integrates directly into the event loop without thread offloading.

**Warning signs:**
- `RuntimeError: This event loop is already running` in logs
- Bot accepts a slash command but produces no response and freezes for other commands
- `It looks like you are using Playwright Sync API inside the asyncio loop` exception
- Other bot commands stop responding after the first Playwright interaction

**Phase to address:**
Browser automation foundation — validate a discord.py command successfully triggers a Playwright action (navigate + screenshot) without blocking other concurrently received commands. This is the first test gate before any game logic is built.

---

### Pitfall 2: Canvas Screenshot Blank in Headless Chromium

**What goes wrong:**
Letter League renders the game board as an HTML5 `<canvas>` inside the Discord Activity iframe. In headless Chromium, `page.screenshot()` captures the Discord UI chrome but the canvas area is solid white or solid black. The vision pipeline receives a contentless image and either errors, returns an empty board, or silently returns a hallucinated plausible board. There is no exception — the pipeline appears to succeed.

**Why it happens:**
Canvas content is rendered asynchronously by JavaScript. In headless Chromium without GPU acceleration, the canvas compositing pipeline does not flush before the screenshot is taken. This is a documented and confirmed behavior — Playwright GitHub issue #19225 (reported 2022, still referenced in 2024) confirms the root cause is rendering timing, not a Playwright defect. Playwright v1.49 (November 2024) switched to a new headless Chromium implementation that changes timing behavior and broke previously working canvas tests (issue #33566). Additionally, headless Chromium by default has no GPU; WebGL/Canvas-heavy apps degrade or go blank without `--use-gl=egl` or equivalent flags.

**How to avoid:**
- Do not screenshot immediately after navigation. Wait for a game-specific render signal: a UI element that only appears after board load, a `wait_for_function` that polls `canvas.width > 0` and then waits an additional frame, or visual confirmation via pixel sampling.
- Use `await page.wait_for_load_state("networkidle")` as a baseline, then add a game-specific wait on top — networkidle alone is insufficient for canvas apps that continue rendering after initial load.
- As a primary fallback: inject JavaScript inside the iframe frame to extract the canvas pixel data directly — `await frame.evaluate("document.querySelector('canvas').toDataURL('image/png')")` — and decode the base64 result as a PIL image. This bypasses the screenshot compositing path entirely and is more reliable than screenshot for cross-origin canvas content.
- Launch Chromium with `args=["--use-gl=egl"]` or headed mode (`headless=False`) to enable GPU compositing. On Linux production servers, use Xvfb as a virtual display for headed mode.
- After Playwright v1.49+, test with `channel="chromium"` vs the default build if canvas rendering regresses.

**Warning signs:**
- Screenshots show Discord UI (buttons, sidebar) but the board area is uniformly white or black
- Vision pipeline returns an empty board or claims no tiles exist on an active game
- Canvas capture works in headed mode (`headless=False`) but fails in headless mode
- Bot worked in dev (Windows headed) but fails on production Linux server (headless)

**Phase to address:**
Browser automation foundation — time-box a spike (max 2 days) specifically to prove canvas screenshot captures actual game board content in both headed and headless modes before any further automation is built on it. Accept `canvas.toDataURL()` injection as the primary method if screenshot is unreliable.

---

### Pitfall 3: Discord Activity iframe Selectors Are Undocumented

**What goes wrong:**
Letter League runs as an embedded iframe inside Discord's web client. The iframe's `src` attribute points to a `*.discordsays.com` URL (Discord proxies all Activity traffic through this domain per their developer docs). The exact selector — whether by `src` URL pattern, `title`, `name`, `data-*` attribute, or DOM position — is not publicly documented. Developers who guess a selector ship code that fails silently in production: `page.frame_locator()` returns a locator that matches nothing, all subsequent game element lookups return zero results, and clicks do nothing, with no exception raised until an action is actually attempted.

**Why it happens:**
Discord's web client is a React SPA with dynamically generated class names that change with every client deployment. No public documentation describes the DOM structure of the voice channel Activity container. Developers make assumptions based on how Activities are described conceptually ("it's an iframe"), write `frame_locator('iframe')` which may match the wrong iframe if Discord has multiple iframes in the view, and do not validate the selector against the live client before building game logic.

**How to avoid:**
- Before writing any automation code, open Discord web client in headed Playwright with a real voice channel + Letter League game running. Use `playwright codegen` or browser DevTools to inspect the DOM and find the exact selector for the Letter League iframe — expect it to match on `src` containing `discordsays.com` plus the Letter League application ID.
- Use a URL-pattern selector rather than position: `frame_locator('[src*="discordsays.com"]')` is more stable than `frame_locator('iframe:nth-child(2)')`. If multiple discordsays.com iframes exist, narrow by the Letter League activity application ID.
- Treat this as an explicit spike deliverable: document the confirmed selector string with a screenshot of the DevTools inspection. Gate all subsequent automation work on this confirmed selector.
- Discord deploys the web client frequently. Build in a selector validation check at browser startup: if the iframe frame cannot be located within 10 seconds of Activity launch, log a specific "iframe selector no longer valid" error rather than a generic timeout.

**Warning signs:**
- `page.frame_locator(selector).locator('canvas').count()` returns 0 when the game is visually running
- `FrameDetachedError` or `Target closed` on the first interaction inside the supposed iframe
- Automation works against the game's direct `discordsays.com` URL but fails through `discord.com`
- Canvas click coordinates land completely off-target (wrong element is in scope)

**Phase to address:**
Browser automation foundation — completing the DevTools inspection spike and documenting the confirmed iframe selector is a mandatory precondition for the foundation phase. No game logic code is written until this is verified.

---

### Pitfall 4: Canvas Click Coordinates Use Viewport Space, Not Canvas-Internal Space

**What goes wrong:**
Tile placement requires clicking specific board cells on the canvas. Developers calculate tile positions using board grid math (column index × tile width, row index × tile height) and pass those as absolute viewport coordinates to `page.mouse.click(x, y)`. The clicks land in the wrong location — consistently offset by the iframe origin plus the canvas element's position within the iframe. On high-DPI displays, an additional devicePixelRatio scaling error multiplies the offset.

**Why it happens:**
`page.mouse` operates in CSS pixels relative to the viewport origin. The canvas element is inside a cross-origin iframe, so its visual position is: viewport offset to iframe + iframe offset to canvas + canvas-internal position. Developers who compute only the canvas-internal grid position (the last component) miss the first two offsets entirely. The Playwright docs note that "The Mouse class operates in main-frame CSS pixels relative to the top-left corner of the viewport" (Playwright API class-mouse). This is a known issue tracked in Playwright GitHub issue #3170 (cross-origin iframe coordinate calculation omits iframe offset). Additionally, Discord's web client may be rendered at device pixel ratios other than 1.0 on HiDPI screens, causing an additional 2× coordinate scaling error.

**How to avoid:**
- Use `canvas_element.click(position={"x": tile_x_offset, "y": tile_y_offset})` rather than `page.mouse.click()`. The `position` argument on an element-scoped click is relative to the element's bounding box, automatically accounting for iframe offset. The offset must stay inside the element's bounding box or Playwright raises an error.
- Verify the canvas element's `getBoundingClientRect()` inside the iframe frame to confirm its reported dimensions match the visual size before building the tile coordinate formula.
- Launch the browser with a fixed `device_scale_factor=1` to eliminate HiDPI scaling ambiguity during development. Validate coordinate mapping by clicking a known position (e.g., the exact center of a tile visible in the screenshot) and confirming the game registers that tile as selected.
- Build a coordinate calibration function: given the canvas element's bounding box (width × height) and the current board grid dimensions, derive the cell size and origin offset. Never hardcode pixel offsets from development screenshots.

**Warning signs:**
- Tile clicks register on wrong board cells — consistently offset in one direction by the same amount
- Rack tile selection clicks do nothing or select the wrong tile
- Coordinate math produces correct results when tested against the game's standalone URL but is systematically wrong inside Discord
- Clicks work at devicePixelRatio=1 but are off by 2× on a HiDPI monitor

**Phase to address:**
Browser automation foundation — implement and validate coordinate mapping as an explicit deliverable before turn detection and tile placement logic is written. Test by clicking 5 known tile positions and confirming correct game response.

---

### Pitfall 5: Session Token Expiry and Re-Authentication Handling

**What goes wrong:**
The bot uses a Playwright persistent browser context (`launch_persistent_context`) with a saved Discord login to avoid re-authenticating every run. Discord's session tokens have a finite lifetime. When the token expires — Discord does not publish the expiry duration, but community reports suggest 7-30 days — the next bot restart launches to a Discord login page instead of the Discord client. If there is no expiry detection, the bot silently "navigates" and all subsequent page actions operate against the login page rather than a game, producing opaque errors.

**Why it happens:**
Developers who implement session persistence assume "it will work until I notice it doesn't." The persistent context userDataDir correctly stores cookies and localStorage on first login, but Discord's auth token has a TTL. There is no Playwright API to introspect cookie expiry at startup. The bot runs for weeks, then at an arbitrary restart, begins failing. The error is distant in time from the cause (the session expired days earlier), making diagnosis non-obvious.

**How to avoid:**
- At each bot startup, after loading the persistent context, navigate to `discord.com` and check for a login redirect before proceeding. If the URL ends up at `/login`, trigger a re-authentication routine instead of attempting game navigation.
- Store the timestamp of the last successful login in a sidecar file next to the `userDataDir`. If the session is older than 7 days, proactively refresh it (even if the token hasn't yet expired) by running the login flow.
- Use `launch_persistent_context` (not `browser.new_context(storage_state=...)`) for the automation account: persistent context preserves the full browser profile including session cookies across restarts via the userDataDir on disk. Storage state alone does not persist session storage, which Discord may use.
- Separate the login session file from the bot's source code directory. Add the userDataDir path to `.gitignore`. The session directory contains live Discord tokens.

**Warning signs:**
- Bot starts but navigation fails to reach a game channel after successful startup
- Playwright logs a redirect to `discord.com/login` during startup navigation
- `page.url` is `discord.com/login` when game automation actions begin
- Bot worked the previous week but now produces `ElementNotFound` errors for game-specific elements

**Phase to address:**
Browser automation foundation — implement session validation and re-authentication detection as part of the browser startup routine, before any game navigation code is written.

---

### Pitfall 6: Turn Detection Relies on an Unverified UI Signal

**What goes wrong:**
The bot must know when it is its turn to play. Without a Discord Activity API, turn detection must be done visually: polling screenshots and detecting a state change, observing a DOM element inside the iframe that indicates whose turn it is, or watching for a timer or UI button becoming active. Developers pick a hypothetical signal ("the submit button becomes enabled when it's my turn") and build the entire turn-detection and play loop around it — then discover in live testing that the signal does not exist, is unreliable, or appears identically for other players' turns.

**Why it happens:**
Letter League's UI signals are not documented. Developers assume the game's UI works the same as standard Scrabble implementations they have seen, then find the actual Discord Activity version uses different UI affordances. Turn detection is treated as a design decision that can be figured out later, so it gets deferred until the autonomous play phase — at which point the entire play loop must be reworked.

**How to avoid:**
- Treat turn-detection signal identification as a research spike that must be completed before autonomous play implementation begins. Manually play at least 2 full games with DevTools open and document: what DOM elements change when it becomes your turn; what pixel regions change; what text or button states are unique to "your turn" vs "opponent's turn".
- Implement visual-diff based turn detection as a fallback: take a reference screenshot at the start of each opponent turn; poll for screenshots that differ by more than a threshold; treat a significant change as a turn transition signal. This is less precise but does not rely on a specific UI element.
- Do not hardcode an assumed turn signal — make the detection strategy a configuration parameter so it can be updated without a code rewrite when the signal is confirmed or changes.
- Time-box the spike at 4 hours. If no reliable DOM signal is found, commit to the visual-diff approach and document the limitation.

**Warning signs:**
- Autonomous play loop either never fires (bot doesn't detect its turns) or fires every screenshot poll cycle (bot acts on every state regardless of turn)
- Bot attempts to place tiles during another player's turn and the game rejects the input
- Turn detection worked in early testing but stops working after a Discord client update (UI change)

**Phase to address:**
Autonomous play — turn detection is the highest-risk deliverable in this phase. Do the live observation spike first, before writing any polling or observation code.

---

### Pitfall 7: Headed Browser Detected as Automation (Discord Anti-Bot Measures)

**What goes wrong:**
Discord's login and client flow includes heuristic checks for automation. Headless Chromium is detected immediately (the `navigator.webdriver` property is `true`, the user agent contains "HeadlessChrome", and WebGL renderer strings differ from real browsers). Discord redirects headless sessions to CAPTCHA or phone verification. Even headed Playwright exposes detectable fingerprints via `navigator.webdriver = true`. Discord may lock or ban the automation account for suspicious login patterns.

**Why it happens:**
Playwright by default exposes `navigator.webdriver = true` in all launched browsers — this is a standard WebDriver flag that anti-bot systems check first. Headless Chromium further lacks plugins, has a distinct user-agent, and has unusual screen/window metrics. Discord specifically has been documented by the community to perform these checks on login attempts.

**How to avoid:**
- Always use headed Chromium (`headless=False`). On Linux production, use Xvfb as a virtual framebuffer: `xvfb-run python bot.py` or launch Xvfb programmatically. This is already an established requirement in the project's "out of scope" constraints.
- Use `chromium.launch(args=["--disable-blink-features=AutomationControlled"])` to suppress the `navigator.webdriver` flag. This is the minimal stealth configuration needed.
- Maintain human-paced interaction timing: 1-3 second delay between individual tile placements, 2-5 seconds between major UI state transitions (navigating to voice channel, starting Activity). Burst-clicking is a strong bot signal.
- Do the manual login once with a real browser, save the persistent context `userDataDir`, and use that for all subsequent runs — this avoids triggering the login flow repeatedly from an automation context.
- Use a consistent user-agent string that matches a real Chrome version rather than the Playwright default.

**Warning signs:**
- Discord login page shows a CAPTCHA during automated login
- "Suspicious login from new location" email sent to the automation account
- Account locked with "Verify your account" prompt that requires phone number
- Login completes but immediately redirects to a 2FA or verification page

**Phase to address:**
Browser automation foundation — validate the headed + `--disable-blink-features=AutomationControlled` configuration successfully completes Discord login without triggering CAPTCHA or verification, before any navigation logic is built.

---

### Pitfall 8: iframe Frame Reference Becomes Invalid After Reconnect

**What goes wrong:**
The bot stores a reference to the Letter League iframe frame object (e.g., `frame = page.frame_locator('[src*="discordsays.com"]')`). Discord's voice channel Activity may reload the iframe if the user reconnects, if the voice channel idles, or if Discord's client performs a soft navigation. After reload, the stored frame reference is detached — all subsequent locator operations on it raise `FrameDetachedError`. The error looks like a transient network issue but is actually a stale object reference.

**Why it happens:**
Playwright's `frame_locator()` returns a locator object that lazily re-evaluates the frame on each interaction. However, if developers store the result of `locator.frame_element()` or cache the underlying `Frame` object (rather than the `FrameLocator`), the cached object becomes invalid the moment the iframe's DOM node is replaced. Discord's SPA architecture replaces iframe DOM nodes frequently. This is a documented Playwright issue (GitHub issue #2753, #33674).

**How to avoid:**
- Never cache a `Frame` or `FrameElement` object between turns. Always re-derive the frame locator from `page.frame_locator(selector)` at the start of each action sequence.
- Wrap all iframe-scoped actions in a retry block: catch `FrameDetachedError` and `TargetClosedError`, re-acquire the frame locator, and retry once before raising.
- Add a health-check at the start of each turn: verify the iframe locator resolves to an element before attempting any game action. If it does not resolve within 5 seconds, log "Activity iframe lost — re-navigating" and navigate back to the voice channel to reload the Activity.
- Use `page.frame_locator(selector)` (returns `FrameLocator`) rather than `page.frames` list indexing (returns `Frame`) — `FrameLocator` is designed for lazy re-evaluation and is more resilient to iframe replacement.

**Warning signs:**
- `FrameDetachedError` or `net::ERR_ABORTED; maybe frame was detached?` after a period of inactivity
- Game automation fails midway through a game session but works at session start
- Error frequency increases after Discord voice channel reconnects or network drops
- `page.frames` list length changes between turns

**Phase to address:**
Browser automation foundation — implement re-acquisition retry logic in the iframe access layer before game actions are built. Test explicitly by simulating an Activity reload (manually leave and rejoin the voice channel) during an automated run.

---

### Pitfall 9: Board State Drift From Accumulated Per-Turn Vision Errors

**What goes wrong:**
The autonomous mode maintains a running board model across turns. Each vision read has a small per-tile error rate. When errors accumulate over 15-20 turns, the bot's internal board model diverges from the actual game state. The bot evaluates moves against the wrong board, finds placements that collide with tiles it misread as empty, or misses high-value placements because it believes squares are occupied. Letter League's expandable board adds a second dimension of drift: when the board grows by one row or column and the coordinate system isn't updated, every absolute position shifts by one cell.

**Why it happens:**
Developers treat per-turn board reading as "accurate enough" and track only deltas (new tiles this turn) to save API cost. This works for early turns but compounds. The expanding board dimension is absent from standard Scrabble implementations, so developers don't anticipate it.

**How to avoid:**
- Treat every turn's vision output as the complete authoritative board state. Never accumulate delta updates. Re-read the full board from a fresh screenshot each turn.
- After each read, run a consistency check: every tile from the previous turn's board must appear in the new board (tiles never disappear). If consistency fails, retry the read before accepting the new board state.
- Detect board expansion by comparing reported grid dimensions between turns. When new rows or columns appear, recalculate all coordinate mappings before placing tiles.
- Never persist board state across a bot restart. Always begin with a fresh full-board read.

**Warning signs:**
- Bot recommends moves the game rejects as invalid (collision with an existing tile)
- Bot's calculated score for a move does not match what the game awards
- Move rejection rate increases noticeably in turns 10+ of the same game
- Bot places a tile one row or column off from the intended position

**Phase to address:**
Autonomous play — design the board model as ephemeral-per-turn from the start. Add consistency validation before any tile placement action.

---

### Pitfall 10: Self-Bot TOS Violation — Automating a Discord User Account

**What goes wrong:**
Discord Activities require a human user account to join a voice channel and interact with the game. The only automation path is to drive a user account via Playwright. Discord explicitly prohibits automating user accounts ("self-bots") under its Terms of Service (support article "Automated User Accounts (Self-Bots)"). Discord has actively banned accounts for this since 2017, with enforcement intensifying in 2021-2023. A banned account ends the autonomous mode permanently. If a personal account is used instead of a dedicated throwaway account, the consequences extend to the user's main Discord presence.

**Why it happens:**
Discord Activities do not expose a bot-accessible API. The automated browser path is the only technically viable option for playing the game. Developers implement it without fully registering the TOS risk or the enforcement history.

**How to avoid:**
- Use a dedicated, isolated Discord account created solely for this automation. Never use a personal account for the Playwright-driven player.
- Keep the discord.py bot account (API bot token) and the Playwright-driven user account strictly separate. Combining API automation and browser automation on the same account is a strong detection signal.
- Maintain human-paced timing: 1-3 second delays between tile placements, 2-5 seconds between major navigation steps.
- Document the TOS risk explicitly in the project's setup guide. Anyone deploying autonomous mode must acknowledge they are using a dedicated throwaway account and accept the risk of that account being banned.

**Warning signs:**
- Discord prompts for CAPTCHA or phone verification during automated login
- The automation account receives a "suspicious login" email
- Account is temporarily locked or suspended

**Phase to address:**
Autonomous play design — document and communicate the TOS risk before implementation begins. The project already calls this out in its out-of-scope constraints. Build and test advisor mode independently since it carries zero TOS risk.

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcode iframe selector as `'iframe:nth-child(1)'` | Fast to write | Breaks whenever Discord adds or reorders iframes in the DOM | Never — inspect and use src-pattern selector |
| Cache `Frame` object across turns | Fewer re-lookups per turn | `FrameDetachedError` whenever Discord reloads the Activity iframe | Never — re-derive from `frame_locator()` each turn |
| Hardcode 27x19 board dimensions in coordinate math | Simplifies tile math | Breaks on any board expansion; game is designed to grow | Never — detect dimensions from vision output each turn |
| Accumulate board state as deltas between turns | Cheaper per-turn API cost | Errors compound; model diverges after 10+ turns | Never for canonical board model; delta view for debugging only |
| Use `time.sleep()` inside discord.py coroutines | Easy to write | Blocks event loop; bot goes dark; Discord heartbeat may fail | Never — use `asyncio.sleep()` |
| Launch new Playwright browser per game turn | Avoids lifecycle management code | 3-5 second startup overhead per turn; browser process leaks over time | Never — launch once at bot startup; keep context alive |
| Use fixed sleep delays for canvas rendering | Simple wait implementation | Too short = blank canvas; too long = unnecessary latency every turn | Prototype only — replace with condition-based wait before shipping |
| Store Discord session userDataDir inside the source repo | Convenient for deployment | Live session tokens in source control; exposure leads to account theft | Never — keep userDataDir outside the repo; add to `.gitignore` |

---

## Integration Gotchas

Common mistakes when connecting to external services.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Playwright + discord.py | Using `sync_playwright` in any discord.py coroutine | Use `async_playwright` exclusively; every Playwright call must be `async def` |
| Playwright canvas | Screenshot immediately after page load | Wait for a game-specific canvas-ready signal; use `canvas.toDataURL()` injection as primary fallback |
| Discord Activity iframe | `page.locator()` for game elements | `page.frame_locator('[src*="discordsays.com"]').locator(...)` to scope to the correct frame |
| Discord Activity iframe | Guessing iframe selector without inspection | Run a headed inspection spike with DevTools before writing any selector; document confirmed selector |
| Canvas tile clicks | `page.mouse.click(viewport_x, viewport_y)` with grid-only math | `canvas_element.click(position={"x": offset_x, "y": offset_y})` where offsets are bounding-box-relative |
| Discord session | `storageState` JSON for persistent login | `launch_persistent_context(user_data_dir=...)` for full profile persistence; validate session at startup |
| Discord login | Re-running login flow from Playwright each restart | Do manual first-login once; save `userDataDir`; reuse on all subsequent runs |
| Autonomous play loop | Polling screenshots at fixed 500ms interval | Use condition-based waiting; rapid polling creates detectable usage patterns and wastes Claude Vision API quota |
| Existing word engine | Calling synchronous engine directly in async handler | `await asyncio.to_thread(engine_fn, *args)` to prevent event loop blocking |

---

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Re-launching Playwright browser per turn | 3-5 second startup overhead per turn; browser process accumulation | Launch once at bot startup; keep context alive; restart only on unrecoverable crash | Every turn in autonomous mode |
| Full Discord screenshot to Claude Vision without crop | High token cost ($4-5 per 1080p image); 10-20 second latency; worse tile accuracy | Crop to board region before sending; target under 1.15 megapixels | From first production use |
| Polling screenshots at high frequency for turn detection | Saturates Claude Vision API quota; `OverloadedError` from Anthropic | Detect turn via DOM state change or coarse visual diff at low frequency; call Claude Vision only when turn is confirmed | After ~20 games per day |
| Fixed-sleep wait for canvas rendering | Either too slow (extra latency every turn) or too fast (blank canvas on slow servers) | Condition-based wait: `wait_for_function` polling canvas non-blank + explicit ready indicator | Varies by server load; high-load servers expose this immediately |
| Caching iframe `Frame` reference across sessions | `FrameDetachedError` mid-game after any Discord reconnect | Re-acquire `frame_locator` reference at start of each action sequence | Any voice channel reconnect or Discord client soft-navigation |

---

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Storing Discord session `userDataDir` inside the source repo or committed to git | Live Discord tokens exposed; account takeover | Keep `userDataDir` path outside repo root; add to `.gitignore`; treat like a credentials file |
| Using a personal Discord account for Playwright-driven autonomous mode | Permanent personal account ban if Discord detects self-bot | Use a dedicated throwaway account; never reuse personal accounts for automation |
| Logging full Discord client screenshots to disk | Other users' private messages visible in screenshot background | Log only the cropped board region; never persist full Discord client captures |
| Exposing Anthropic API key in Discord response messages or logs | Key visible to channel members; billing abuse | Never include API keys in embeds, messages, or log lines; use structured logging with credential redaction |
| No file type or size validation on screenshot uploads in advisor mode | Malformed or oversized images crash vision pipeline; adversarial images trigger unexpected LLM behavior | Validate `attachment.content_type` and `attachment.size <= 10_000_000` before processing |

---

## UX Pitfalls

Common user experience mistakes in this domain.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Autonomous mode plays too fast (sub-second between tiles) | Looks robotic; increases detection risk; may trigger Discord rate limiting | Enforce 1-3 second delays between tile placements; vary timing slightly |
| No status feedback while autonomous mode is playing | Users watching don't know if the bot is thinking, stuck, or broken | Post Discord status messages at turn start ("Bot is playing...") and turn end ("Bot played WORD for N points") |
| Bot passes or skips a turn with no explanation | Users see the bot do nothing; assume it crashed | Log the reason for passing (no valid moves found, vision failure, game state uncertain) as a Discord message |
| Advisor mode takes 10-15 seconds with no intermediate feedback | User thinks command failed | Always `defer()` immediately; send a "thinking" indicator; edit with results when ready |
| Difficulty percentage produces no visible effect between 30% and 70% | Feature feels non-functional | Verify statistically different average scores across 0%, 50%, 100% on many simulated boards before shipping |

---

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Canvas screenshot:** Works in headed mode — verify it also works in headless/Xvfb mode with the `--disable-blink-features=AutomationControlled` + `--use-gl=egl` flags; headed dev environment does not guarantee headless production success
- [ ] **iframe access:** `frame_locator()` returns a locator — verify it actually scopes to the Letter League canvas; confirm with `await frame_locator.locator('canvas').count() > 0` on a live game
- [ ] **Session persistence:** Persistent context launches successfully — verify login state is still valid (page URL is not `discord.com/login`) before any game navigation is attempted
- [ ] **Canvas coordinate mapping:** Click code sends coordinates — verify by clicking the center of a known visible tile and confirming the game highlights/selects that tile (not an adjacent one)
- [ ] **Turn detection:** Polling loop fires — verify it fires exactly once per turn and does not fire during opponent turns; test across at least one complete 2-player game
- [ ] **Tile placement sequence:** Individual tile clicks succeed — verify the complete sequence (select rack tile → select board cell → confirm placement) as an atomic action before building multi-tile word placement
- [ ] **Word confirmation:** Tiles placed on board — verify the confirmation button click is correctly targeted and the game registers the move (not silently ignored)
- [ ] **iframe re-acquisition:** Bot completes one turn — verify it also completes a second turn after a manual Discord Activity reconnect without a restart
- [ ] **Board state freshness:** Vision output returns valid JSON — verify each turn starts from a fresh screenshot, not a cached result from the previous turn
- [ ] **TOS account separation:** Bot is running — verify the Playwright session uses a different Discord account than the discord.py bot token; they must be separate accounts

---

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Playwright sync API conflict mid-integration | MEDIUM | Audit entire codebase for `sync_playwright` imports; replace with `async_playwright` + async wrappers; re-test all Playwright code paths |
| Canvas screenshot blank in headless | MEDIUM | Switch to `canvas.toDataURL()` injection via `frame.evaluate()` as the primary capture method; benchmark latency vs. screenshot; rebuild capture pipeline around this approach |
| iframe selector no longer valid after Discord update | LOW | Re-run headed DevTools inspection spike; update selector constant; redeploy |
| Discord session expired at startup | LOW | Bot detects login redirect; triggers re-authentication routine; logs "session expired, re-authenticating" |
| Discord automation account banned | HIGH | Create new account; review click timing patterns (add longer delays); accept that autonomous mode has inherent account ban risk; document for users |
| `FrameDetachedError` mid-game | LOW | Add retry-with-reacquisition to iframe action layer; re-acquire frame from `page.frame_locator()`; retry action once |
| Turn detection signal changes after Discord update | MEDIUM | Re-run live game observation spike; update detection logic; test across 2 full games before re-deploying |
| Board state drift causing wrong moves | LOW | Discard internal model; force full re-read from fresh screenshot; if consistency check still fails, pass the turn and retry next round |

---

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Playwright sync API conflict | Browser automation foundation | Integration test: discord.py slash command triggers Playwright navigate + screenshot; bot stays responsive to concurrent commands |
| Canvas screenshot blank in headless | Browser automation foundation (spike) | Capture test: take Letter League canvas screenshot in headed and headless modes; pixel content must be non-blank in both; or confirm `toDataURL()` method works |
| iframe selector undocumented | Browser automation foundation (pre-code spike) | DevTools inspection deliverable: document confirmed selector string + screenshot of DOM; `frame_locator(selector).locator('canvas').count() >= 1` on live game |
| Canvas coordinate mapping | Browser automation foundation | Click validation: click center of 5 known tile positions; game highlights correct tile in each case |
| Session token expiry | Browser automation foundation | Startup validation test: bot correctly detects expired session; gracefully re-authenticates or reports actionable error |
| Headed browser detection | Browser automation foundation | Login test: automated login completes without CAPTCHA or verification prompt using `--disable-blink-features=AutomationControlled` |
| iframe frame reference stale | Browser automation foundation | Reconnect test: simulate Activity reload mid-session; bot re-acquires frame and completes next action without crash |
| Turn detection on unverified signal | Autonomous play (spike first) | Live observation: identify confirmed DOM/visual turn signal across 2 full games before writing detection code |
| Board state drift | Autonomous play | Consistency test: re-read same board 5 times; verify identical output; simulate 20-turn sequence; measure drift rate |
| Self-bot TOS risk | Autonomous play design (pre-implementation) | Documentation review: setup guide explicitly names TOS risk; dedicated account requirement documented and enforced in configuration |
| TOS account separation | Browser automation foundation | Configuration test: assert Playwright session account != discord.py bot token account at startup |

---

## Sources

- [Discord Automated User Accounts (Self-Bots) official policy](https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots) — explicit prohibition on selfbots; permanent ban consequence confirmed (HIGH confidence)
- [Discord Platform Manipulation Policy](https://discord.com/safety/platform-manipulation-policy-explainer) — enforcement approach and ban history (HIGH confidence)
- [Discord Activities — How Activities Work](https://docs.discord.com/developers/activities/how-activities-work) — Activities run in `*.discordsays.com` iframe; postMessage communication; exact selector undocumented (MEDIUM confidence — iframe src pattern inferred from developer docs, not confirmed by live inspection)
- [Playwright GitHub issue #19225 — canvas elements don't show up in screenshots](https://github.com/microsoft/playwright/issues/19225) — canvas screenshot blank root cause and resolution strategy (HIGH confidence)
- [Playwright GitHub issue #33566 — Changes in Chromium headless in v1.49](https://github.com/microsoft/playwright/issues/33566) — new headless implementation changes timing behavior; November 2024 (HIGH confidence)
- [Playwright GitHub issue #3170 — cross-origin iframe coordinate offset bug](https://github.com/microsoft/playwright/issues/3170) — element positions inside cross-origin iframes may not account for iframe offset (MEDIUM confidence)
- [Playwright GitHub issue #2753 — closing last page in persistent context closes context unexpectedly](https://github.com/microsoft/playwright/issues/2753) — persistent context edge case behavior (MEDIUM confidence)
- [Playwright Python issue #462 / #2053 / #2705 — sync API inside asyncio loop](https://github.com/microsoft/playwright-python/issues/462) — documented as the most frequent Python Playwright integration mistake (HIGH confidence)
- [Playwright Python auth docs](https://playwright.dev/python/docs/auth) — `storageState` does not persist session storage; `launch_persistent_context` for full disk profile persistence (HIGH confidence)
- [Playwright Mouse API docs](https://playwright.dev/docs/api/class-mouse) — operates in main-frame CSS pixels relative to viewport top-left; coordinate implications for iframe-contained canvas (HIGH confidence)
- [createIT — Testing WebGL with Playwright headless](https://www.createit.com/blog/headless-chrome-testing-webgl-using-playwright/) — `--use-angle=gl` / `--use-gl=egl` for headless GPU acceleration; Xvfb for headed virtual display (MEDIUM confidence)
- [discord.py FAQ](https://discordpy.readthedocs.io/en/stable/faq.html) — event loop blocking; `asyncio.sleep` vs. `time.sleep`; `run_in_executor` recommendation (HIGH confidence)
- [Playwright storageState — BrowserStack guide](https://www.browserstack.com/guide/playwright-storage-state) — token expiry causes silent test failures; must plan for re-authentication (MEDIUM confidence)
- [Castle.io — Anti-detect frameworks evolution](https://blog.castle.io/from-puppeteer-stealth-to-nodriver-how-anti-detect-frameworks-evolved-to-evade-bot-detection/) — `navigator.webdriver` detection by anti-bot systems; `--disable-blink-features=AutomationControlled` as mitigation (MEDIUM confidence)

---
*Pitfalls research for: Letter League Bot v1.2 — Playwright browser automation + autonomous play addition*
*Researched: 2026-03-24*
