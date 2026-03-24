# Pitfalls Research

**Domain:** Discord word game AI bot — v1.1 addition of vision, Discord bot, and browser automation to existing Python word engine
**Researched:** 2026-03-24
**Confidence:** MEDIUM-HIGH (Playwright, discord.py, Claude Vision API verified against official docs and GitHub issues; Letter League-specific behaviors require live testing)

---

## Critical Pitfalls

### Pitfall 1: Playwright Sync API Inside discord.py's Async Event Loop

**What goes wrong:**
Playwright ships two Python APIs: `sync_playwright()` and `async_playwright()`. discord.py owns an asyncio event loop from startup. If any code calls `sync_playwright()` inside a discord.py coroutine or event handler — or in a module imported by one — Python raises `RuntimeError: This event loop is already running` and the bot freezes or crashes. The bot appears to accept the command but never responds.

**Why it happens:**
Developers who learned Playwright from web testing tutorials use `sync_playwright()` by habit. The sync API internally creates its own event loop. When the running loop already exists (discord.py's), conflict is immediate. This mistake is documented as the most frequent Python async integration bug in the discord.py FAQ.

**How to avoid:**
Use `playwright.async_api` exclusively. Every Playwright call must be inside an `async with async_playwright() as p:` block inside an `async def` function. Launch the browser once at bot startup and keep the context alive across turns — do not re-launch per command. Never import or call `sync_playwright` anywhere in the codebase. Validate by running a discord.py command that triggers a Playwright action and confirming the bot remains responsive to other commands during execution.

**Warning signs:**
- `RuntimeError: This event loop is already running` in logs
- `RuntimeError: There is no current event loop` when called from spawned threads
- Bot accepts a command but freezes and produces no response
- Other bot commands stop working immediately after the first Playwright interaction

**Phase to address:**
Browser automation foundation phase — this must be the first thing verified before any game logic is built on top.

---

### Pitfall 2: Canvas Screenshot Blank in Headless Chromium

**What goes wrong:**
Letter League renders its game board as an HTML5 `<canvas>` element inside a Discord Activity iframe. In Playwright headless mode, `page.screenshot()` captures the surrounding UI but the canvas area is solid white or solid black. The vision pipeline receives an image with no board content and either errors, returns an empty board, or — worst case — hallucinates a plausible-looking board that bears no relation to the actual game state.

**Why it happens:**
Canvas content is rendered asynchronously by JavaScript. In headless Chromium, if the screenshot is taken before the JavaScript rendering loop has composited the canvas frame, the output is blank. This is documented in Playwright GitHub issue #19225 (reported 2022; closed because the solution is a wait strategy, not a Playwright code change). Additionally, Playwright v1.49 (November 2024) switched to a new headless Chromium implementation that changes timing behavior and requires updating test suites that previously worked.

**How to avoid:**
- Do not take the screenshot immediately after navigation. Wait for a game-specific signal that the board has fully rendered: a UI button that only appears post-load, a canvas non-blank pixel check, or a `waitForFunction` that polls `canvas.width > 0`.
- Use `await page.wait_for_load_state("networkidle")` as a baseline, then add a game-specific wait on top.
- Test canvas capture in both headed and headless mode before building the vision pipeline. If headed works but headless doesn't, the issue is rendering timing, not a code bug.
- As a fallback if timing waits don't resolve the issue: inject JavaScript to extract canvas pixel data directly — `await page.evaluate("document.querySelector('canvas').toDataURL('image/png')")` — and decode the base64 result as a PIL image. This bypasses the screenshot compositing path entirely.
- After Playwright v1.49+, test with both `chromium` and `chromium:new` channel options if canvas rendering regresses.

**Warning signs:**
- Screenshots show Discord UI chrome (toolbar, buttons) but the board area is uniformly white or black
- Vision pipeline returns empty board or claims no tiles are placed despite an active game
- Behavior works in headed mode (`headless=False`) but fails in headless mode (`headless=True`)
- Board reading worked in dev environment but fails in production server (headed vs. headless difference)

**Phase to address:**
Browser automation foundation phase — validate canvas screenshot captures actual board content in headless mode before any vision or click automation is built.

---

### Pitfall 3: Vision LLM Hallucination on Ambiguous Game Tiles

**What goes wrong:**
Claude Vision returns a confident, structurally valid JSON board that contains 1-3 wrong tile letters. The word engine receives this data, finds a legal word placement, and the bot recommends or plays a move based on tiles that don't actually exist. In advisor mode, the user follows the advice and the game rejects the word. In autonomous mode, the bot places tiles and the game either rejects the move or silently records an incorrect sequence. The error is invisible without explicit validation — no exception is raised, the pipeline appears to succeed.

**Why it happens:**
Claude's documented limitations include reduced accuracy on: images where text is very small relative to image size (Letter League tiles at normal Discord resolution may be 20-30px), stylized or custom fonts with decorative elements, and spatially dense layouts requiring counting large numbers of small objects. Visually similar characters — `I` / `l` / `1`, `O` / `0`, `W` / `M` upside down — are common confusion pairs. The 27x19 grid at typical screenshot resolution means individual tiles can be well under the 200px minimum threshold where Anthropic documents quality degradation.

**How to avoid:**
- Crop the screenshot to the board region only before sending to Claude. A 1920x1080 full-screen Discord capture gives each tile approximately 15-25px; a board-only crop at 2x upscaling gives 40-60px per tile. Anthropic explicitly recommends images with text be legible, not small.
- Request structured JSON output using a schema with explicit per-row representation. Use Claude's tool-use / structured output feature rather than asking for JSON in a plain text response — structured output guarantees schema compliance (no stray text, no truncation).
- Include a cross-validation step: after extraction, verify that every word on the board is a valid dictionary word at its reported position. A single invalid word at a claimed position is a strong hallucination signal.
- For tiles the model rates as uncertain (prompt it to flag these), re-send a cropped sub-image of just that tile region.
- Images must be above 200px per edge for reliable quality. For a 27-column board, the full-board crop must be at least 5400px wide, or individual tile crops must be prepared.

**Warning signs:**
- Bot recommends words using tiles that the user does not have in their rack or on their board
- Board representation from successive reads of the same unchanged board differs between calls
- Vision output contains words already on the board but with 1-2 letters changed
- JSON extraction succeeds but word engine finds no valid moves on what should be a normal board position

**Phase to address:**
Vision pipeline phase — measure per-tile error rate on 20+ ground-truth screenshots before connecting the vision output to the word engine. Gate the phase on achieving an acceptable error rate (target: <2% per-tile, <5% per-board-read with no catastrophic errors).

---

### Pitfall 4: Interaction Token Timeout Freezing the Bot

**What goes wrong:**
Discord slash command interactions have a 3-second acknowledgment window. If the bot does not respond within 3 seconds of receiving the slash command, Discord marks the interaction as failed and shows the user "The application did not respond." The vision API call (network round-trip + model inference) typically takes 4-15 seconds. A bot that does not defer immediately before starting async work will consistently timeout on every board analysis command.

**Why it happens:**
Developers write the handler to process first and respond after, following the natural imperative flow: "receive screenshot, analyze it, send result." Discord's interaction model requires the opposite: acknowledge first (which buys a 15-minute follow-up window), then do work, then edit the deferred response with results.

**How to avoid:**
- The first line in any slash command handler that does async work must be `await interaction.response.defer()` (or `defer(ephemeral=True)` for private responses). This immediately sends a "thinking..." indicator to Discord and extends the response window to 15 minutes.
- Use `await interaction.followup.send(...)` to deliver the final result. Never use `interaction.response.send_message(...)` after deferring — it will fail with `InteractionResponded`.
- Structure the handler as: defer → kick off async task → await task → followup. Do not use `asyncio.gather` to run deferral and work simultaneously; defer must complete first.

**Warning signs:**
- "The application did not respond" appears in Discord after using the `/analyze` command
- Works in local development (fast network, fast model) but fails in production
- Works when the word engine runs quickly but fails when vision API is slow

**Phase to address:**
Discord advisor mode integration phase — implement the defer pattern from the very first handler, not as a later fix.

---

### Pitfall 5: Word Engine Blocking the Discord Event Loop

**What goes wrong:**
The existing v1.0 word engine (GADDAG move generation) is pure CPU-bound Python. Calling it synchronously inside a discord.py async handler blocks the entire asyncio event loop for the duration of move generation. During this time, the bot cannot receive new messages, respond to other commands, or send the "typing" indicator. In observed Scrabble-engine benchmarks, move generation on a complex board can take 1-5 seconds. During that window, all discord.py I/O — including maintaining the gateway heartbeat — is frozen. Discord may interpret a missed heartbeat as a connection failure and disconnect the bot.

**Why it happens:**
The engine was built as a standalone synchronous library (correct for v1.0). Adding Discord integration without adapting the call pattern is the natural mistake — the engine function looks like a normal Python function call, and wrapping it in `asyncio.run_in_executor` is non-obvious.

**How to avoid:**
- Wrap all synchronous word engine calls in `await loop.run_in_executor(None, engine_function, *args)`. This runs the synchronous engine in a thread pool worker, freeing the event loop to process Discord events.
- Alternatively, use `asyncio.to_thread(engine_function, *args)` (Python 3.9+, simpler syntax).
- The engine itself does not need to change — just the call site in the Discord handler.
- Test the fix by running move generation while simultaneously sending other bot commands; both should process without blocking each other.

**Warning signs:**
- Bot stops responding to all commands during move generation
- `discord.py` logs `Shard ID None heartbeat blocked for more than X seconds`
- Gateway connection drops and reconnects during long move generation runs
- `/ping` command doesn't respond while `/analyze` is processing

**Phase to address:**
Discord advisor mode integration phase — add executor wrapping in the first handler that calls the word engine; test concurrent command handling explicitly.

---

### Pitfall 6: Board State Drift from Accumulated Per-Turn Errors

**What goes wrong:**
The autonomous mode maintains a running model of the board across turns. Each vision read has some small error rate. When these errors accumulate across 15-20 turns, the bot's internal board model diverges from the actual game state. The bot evaluates moves against a wrong board — finding word placements that collide with tiles the bot misread as empty, or missing high-value placements because the bot thinks certain squares are occupied. In later turns, the bot's move suggestions become progressively less useful.

Additionally, Letter League's board is expandable beyond 27x19. If the board grows by one row or column and the coordinate system isn't updated, every absolute position in the bot's model shifts by one cell. All subsequent placements land in the wrong position.

**Why it happens:**
Developers treat per-turn board reading as "accurate enough" and track only deltas (new tiles placed this turn) to avoid the cost of a full re-read. This works for the first few turns but compounds. The expanding board is an additional dimension not present in standard Scrabble, making coordinate drift more likely.

**How to avoid:**
- Treat every turn's vision output as the complete authoritative board state. Never accumulate delta updates. Re-read the full board from a fresh screenshot each turn, even if it costs one extra API call.
- After each read, run a consistency check: every tile from the previous board must exist in the new board (tiles never disappear in a word game). If consistency fails, this is a read error; retry before accepting the new board state.
- Detect board expansion by comparing grid dimensions between turns. When new rows or columns appear, recalculate all coordinate mappings before placing tiles.
- Never persist board state across a bot restart. Always begin a session with a fresh full-board read.

**Warning signs:**
- Bot recommends or plays moves that the game rejects as invalid (collision with existing tile)
- Bot's calculated score for a move does not match what the game awards
- Error frequency in move rejection increases in turns 10+ of the same game
- Bot places a tile one row or column off from the intended position

**Phase to address:**
Board vision/OCR phase — design the board model as ephemeral-per-turn from the start, before autonomous mode is added.

---

### Pitfall 7: Self-Bot TOS Violation — Automating a Discord User Account

**What goes wrong:**
Discord Activities (including Letter League) require a human user account to join a voice channel and interact with the game. The only automation path is to drive a user account via Playwright. Discord explicitly prohibits automating user accounts ("self-bots") under its Terms of Service and has actively banned accounts for this behavior since 2017, with enforcement intensifying 2021-2023. A banned account ends the autonomous mode permanently. If a personal account is used instead of a dedicated throwaway, the consequences extend to the user's main Discord presence.

**Why it happens:**
Discord Activities do not expose a bot API. Bots cannot join voice channels as game participants or interact with Activities via the Discord API. The automated browser path is the only technically viable option. Developers implement it without fully registering the TOS risk or the enforcement history.

**How to avoid:**
- Use a dedicated, isolated Discord account created solely for automation. Never use a personal account for the browser-automated player.
- Keep the discord.py bot account (API bot token) and the Playwright-driven account strictly separate — using the Discord API and browser automation on the same account is a strong self-bot detection signal.
- Maintain human-paced interaction timing: 1-3 second delays between tile placements, 2-5 seconds between major UI actions. Do not perform burst clicks.
- Explicitly document the TOS risk in the bot's setup guide. Users must understand they are using a dedicated throwaway account and accept the risk of that account being banned.
- For advisor mode, there is zero TOS risk — the bot receives a screenshot from the user and responds via the Discord API. Build and ship advisor mode first.

**Warning signs:**
- Discord prompts for phone/CAPTCHA verification during the automated login
- The automation account receives a "suspicious login from new location" email
- Account is temporarily locked or suspended
- Discord redirects the automated login to a verification page instead of completing login

**Phase to address:**
Autonomous mode design — document and communicate TOS risk before any implementation begins. Build advisor mode first as it carries zero TOS risk and delivers core value independently.

---

### Pitfall 8: iframe Cross-Origin Blocking Playwright Element Interaction

**What goes wrong:**
Letter League runs as an embedded iframe inside Discord's web client. The iframe loads the game from a different origin than `discord.com`. Playwright locators written against `page` find nothing inside the iframe — they operate in the outer Discord page context, not the game's frame context. Automation code that works when tested against the game's standalone URL fails completely inside Discord. Canvas click coordinates must also be calculated relative to the canvas element's bounding box within the iframe, not the viewport.

**Why it happens:**
Browsers enforce the Same-Origin Policy, creating a separate execution context for cross-origin iframes. Developers write `page.locator(...)` selectors and are surprised when they match zero elements that are visually present — because the elements live in the iframe's context, not the page's. Additionally, the exact URL or attribute used to identify Letter League's iframe within Discord's web client is not publicly documented and requires live inspection.

**How to avoid:**
- Use `page.frame_locator(selector)` to scope all game interaction to the iframe context. Identify the iframe by its `src` URL pattern (e.g., `[src*="letter-league"]` or the actual Activity URL) rather than by position — position-based iframe indexing breaks if Discord adds other iframes.
- Determine the correct iframe selector by inspecting the Discord web client in headed mode with browser DevTools before writing any automation code. Do this as an explicit spike before building game logic.
- All canvas clicks must use coordinates relative to the canvas element's bounding box: `await canvas.click(position={"x": tile_x, "y": tile_y})` where `tile_x` and `tile_y` are offsets from the canvas element's top-left corner, not the viewport.
- Test frame access in isolation — confirm you can successfully locate and click a static UI element inside the iframe before building any dynamic tile placement.

**Warning signs:**
- `page.locator(...)` returns 0 elements for elements visually present in the game
- `ElementHandle.click()` throws `target closed` or `frame detached` errors
- Automation works against the game's direct URL but fails when accessed through Discord
- Canvas clicks land in the wrong position relative to where tiles should be placed

**Phase to address:**
Browser automation foundation phase — validate iframe access and canvas coordinate calculation as isolated engineering problems before game logic is built.

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcode 27x19 board dimensions | Simplifies coordinate math | Breaks on any board expansion; the game is designed to grow | Never — board expansion is a core mechanic; detect dimensions dynamically |
| Accumulate board state as deltas between turns | Cheaper per-turn API cost | Errors compound; model diverges after 10+ turns | Never for the canonical board model; a debug diff view is acceptable |
| Call vision API synchronously in a discord.py handler | Simpler code path | Blocks event loop; bot stops responding; Discord heartbeat fails | Never — always use `asyncio.to_thread()` or `run_in_executor()` |
| Use Playwright sync API in a thread alongside discord.py | Avoids async complexity | Thread-safety issues, event loop conflicts, unpredictable crashes | Prototype only; refactor before any real use |
| Use `time.sleep()` in any discord.py coroutine | Easy to write | Blocks event loop; bot goes dark during sleep | Never — use `asyncio.sleep()` |
| Skip `interaction.response.defer()` for "fast" commands | Simpler code | Commands that take >3s will timeout and show users an error | Never — always defer if the handler does any async I/O |
| Send raw full-page screenshots to Claude Vision API | No preprocessing step | Tiny tile size degrades accuracy; inflates token cost; may exceed 5 MB limit | Never — always crop to board region and upscale before sending |
| Store bot token or API key in `.env` committed to the repo | Convenient | Token exposure leads to bot compromise and API billing abuse | Never |

---

## Integration Gotchas

Common mistakes when connecting to external services.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Discord API (discord.py) | Responding to interaction after 3-second window without deferring | Call `await interaction.response.defer()` as the first line in any handler that does async work |
| Discord API | Using `interaction.response.send_message()` after already calling `defer()` | After `defer()`, use `interaction.followup.send()` exclusively; mixing the two raises `InteractionResponded` |
| Claude Vision API | Sending full 1920x1080 Discord screenshot | Crop to board region; individual tiles at full resolution may be under the 200px minimum; upscale the crop to keep tiles legible |
| Claude Vision API | Image over 5 MB rejected silently or with a 400 error | Validate image file size before sending; Discord Nitro attachments can reach 100 MB; compress/resize before API call |
| Claude Vision API | Expecting free-text JSON in the response | Use structured output / tool-use schema to guarantee valid JSON that matches your `BoardState` schema; plain text requests produce inconsistent format |
| Playwright (canvas) | Taking screenshot immediately after page load | Wait for a game-specific render signal; `waitForLoadState("networkidle")` alone is insufficient for canvas apps that render after initial load |
| Playwright (iframe) | Using `page.locator()` for game elements | Use `page.frame_locator('[src*="letter-league"]').locator(...)` to scope to the correct frame; main page locators find nothing inside the iframe |
| Playwright (canvas clicks) | Using viewport coordinates for tile clicks | All tile position offsets must be relative to the canvas element's bounding box, not the viewport origin |
| Existing word engine | Calling synchronous engine functions directly in async handlers | Wrap with `await asyncio.to_thread(engine_fn, *args)` to prevent event loop blocking |
| Wordnik wordlist | Assuming 100% overlap with Letter League's accepted words | Letter League may use a proprietary dictionary; Wordnik is an approximation; label suggestions "likely valid" and verify with a known-valid test word set |

---

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Calling synchronous word engine in async handler without executor | Bot freezes during move generation; other commands queue up | Wrap with `asyncio.to_thread()` or `run_in_executor(None, ...)` | Every turn; GADDAG on complex board takes 1-5 seconds |
| Sending full Discord screenshot to vision API (no crop) | High token cost ($4-5/image at 1080p), slow response, worse tile accuracy | Crop to board region before sending; target board crop under 1.15 megapixels | From first production use; cost visible immediately on API billing |
| Re-launching Playwright browser per game turn | 3-5 second startup overhead per turn; browser process leak under concurrent games | Launch one browser at bot startup; keep context alive; only restart on crash | Every turn in autonomous mode |
| Caching iframe frame reference across Discord reconnects | `FrameNotFound` errors after Discord reinitializes the Activity iframe | Re-acquire the frame_locator reference each turn rather than caching it between sessions | Any time the user disconnects/reconnects from the voice channel |
| Hardcoded sleep delays for canvas rendering | Slow when delay is too long; blank canvas when too short | Use condition-based waits (`waitForFunction`, polling a game-state indicator) instead of fixed timeouts | Varies by network speed and server load |

---

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Storing Discord bot token or Anthropic API key in committed code or `.env` | Token theft enables full bot impersonation; API key misuse generates unexpected billing | Use OS environment variables; add `.env` to `.gitignore`; rotate immediately if exposed |
| Logging full Discord client screenshots to disk | Other users' private messages may be visible in the background of Discord screenshots | Log only the cropped board region; never log full Discord client captures |
| Using a personal Discord account for Playwright-driven autonomous mode | Permanent personal account ban if Discord detects self-bot activity | Use a dedicated throwaway account; document this requirement in setup guide; never reuse personal accounts |
| No file type or size validation on screenshot uploads in advisor mode | Malformed or oversized images crash the vision pipeline; adversarial images may trigger unexpected LLM behavior | Validate `attachment.content_type in {"image/png", "image/jpeg", "image/webp"}` and `attachment.size <= 10_000_000` before processing |
| Exposing Anthropic API key in Discord response messages or logs | Key is visible to all channel members; billing abuse risk | Never include API keys in any message, embed, or log line; use structured logging that redacts credential fields |

---

## UX Pitfalls

Common user experience mistakes in this domain.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Bot suggests a word that Wordnik considers valid but Letter League rejects | User plays the word, it's rejected, turn is wasted, trust in bot is destroyed | Label suggestions "likely valid (Wordnik)" and include a disclaimer that Letter League's dictionary may differ |
| Advisor mode takes 10-15 seconds with no intermediate feedback | User thinks the bot is broken or the command failed | Always `defer()` immediately; optionally send a follow-up "thinking" message; edit with results when ready |
| No visual confirmation of what the bot read from the board | User can't verify the vision parsing was correct before following advice | Include a text-based board representation in the response alongside the word suggestion; users can spot misreads at a glance |
| Bot responds with an optimal move at maximum difficulty with no explanation | New players can't learn from suggestions they can't follow | Include the score breakdown and placement explanation in every response, not just the final word |
| Difficulty percentage produces no visible difference between 30% and 70% settings | Users cannot find a difficulty level they enjoy; feature feels non-functional | Test that 0%, 50%, and 100% produce statistically different average scores across many simulated boards before shipping |

---

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Canvas screenshot capture:** Works in headed mode — verify it also works in headless mode; canvas rendering issues are headless-specific and the deployment environment is almost certainly headless
- [ ] **Vision pipeline:** Returns valid JSON — verify the JSON represents the actual board, not a hallucinated one; run against 5+ ground-truth screenshots and compare expected vs. returned tile layout
- [ ] **Multiplier square detection:** Board letter tiles are extracted — verify that DL/TL/DW/TW multiplier squares are also detected and stored in BoardState; the existing engine uses these for scoring
- [ ] **Discord interaction handler:** Command accepts screenshot attachment — verify it also handles: no attachment (user forgets to upload), wrong file type (PDF, GIF), file over 5 MB, and network failure on attachment download
- [ ] **Interaction deferral:** Handler works in dev — verify it defers before any async work; test with an artificially slow vision mock to confirm no 3-second timeout occurs
- [ ] **Event loop blocking:** Word engine produces results — verify calling it from a discord.py handler does not block other commands; test by sending two `/analyze` commands near-simultaneously
- [ ] **Playwright iframe access:** Can navigate to Discord — verify `frame_locator()` successfully scopes into the Letter League iframe in headless mode with the correct selector
- [ ] **Autonomous mode account:** Can log in — verify the dedicated automation account has Letter League accessible and can join a voice channel; test CAPTCHA handling and 2FA if the account uses it
- [ ] **BoardState contract:** Vision pipeline produces output — verify that the `BoardState` dataclass produced by the vision pipeline is accepted without modification by the existing v1.0 word engine; field names, types, and coordinate systems must match exactly

---

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Playwright sync API conflict discovered mid-integration | MEDIUM | Audit entire codebase for `sync_playwright` imports; replace with `async_playwright` + async wrapper; re-test all Playwright code paths |
| Canvas screenshot blank in headless mode | MEDIUM | Switch to JavaScript `canvas.toDataURL()` extraction as primary method; rebuild screenshot pipeline around this approach; benchmark latency difference |
| Vision LLM returns structurally valid but wrong board | LOW per-instance | Retry with preprocessed crop; if retries fail, return error to user with "board reading failed, try a clearer screenshot"; log the failed image for offline analysis |
| Board state drift detected mid-autonomous game | LOW | Discard internal model entirely; force a full re-read from fresh screenshot; if consistency check still fails, pass the turn and try again next round |
| Discord automation account banned | HIGH | Create a new account; review timing of automated clicks and add longer delays; accept that indefinite operation of autonomous mode is inherently at risk; re-evaluate whether autonomous mode scope is worth ongoing account creation overhead |
| Interaction timeout (`application did not respond`) | LOW | Add `await interaction.response.defer()` as first line of handler; deploy fix; no data loss |
| iframe `FrameNotFound` error in autonomous mode | LOW | Re-acquire frame reference on each turn rather than caching; add retry logic that re-navigates to the Activity if the frame disappears |

---

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Playwright sync API conflict | Browser automation foundation | Integration test: discord.py command triggers Playwright; bot stays responsive during execution |
| Canvas screenshot blank in headless mode | Browser automation foundation | Screenshot test: capture Letter League canvas headless and headed; compare pixel content; must be non-blank in headless |
| Vision LLM hallucination on tiles | Vision pipeline phase | Accuracy test: 20+ ground-truth screenshots; measure per-tile error rate; must be <2% before connecting to engine |
| Interaction token timeout | Discord advisor integration | Stress test: simulate slow vision API (4-15 sec mock); verify no timeout errors and correct deferred response |
| Word engine blocking event loop | Discord advisor integration | Concurrency test: send two `/analyze` commands near-simultaneously; verify both complete without blocking each other |
| Board state drift in autonomous mode | Vision pipeline + autonomous mode | Consistency test: re-read same board 5 times; verify identical output; simulate 20-turn sequence; check drift rate |
| Self-bot TOS risk | Autonomous mode design (pre-implementation) | Documentation review: setup guide explicitly names TOS risk and requires dedicated account |
| iframe cross-origin blocking | Browser automation foundation | Smoke test: `frame_locator()` locates at least one static game element before any game logic is built |
| BoardState contract mismatch | Discord advisor integration | Integration test: end-to-end path from real screenshot through vision pipeline through word engine; verify no type errors or key mismatches |
| Image size/type validation | Discord advisor integration | Edge-case test: send PDF, 50 MB image, GIF; verify graceful rejection with user-facing error message |

---

## Sources

- [Discord Automated User Accounts (Self-Bots) official policy](https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots) — explicit prohibition on selfbots; permanent ban consequence confirmed
- [Discord Platform Manipulation Policy](https://discord.com/safety/platform-manipulation-policy-explainer) — enforcement approach and account ban history (2021-2023 intensification)
- [discord.py FAQ — Blocking vs. Non-Blocking](https://discordpy.readthedocs.io/en/stable/faq.html) — event loop blocking patterns; `asyncio.sleep` vs. `time.sleep`; `run_in_executor` recommendation
- [Playwright GitHub issue #19225 — canvas elements don't show up in screenshots](https://github.com/microsoft/playwright/issues/19225) — documented canvas screenshot bug; resolution is timing/wait strategy, not a Playwright code fix
- [Playwright GitHub issue #33566 — Changes in Chromium headless in Playwright v1.49](https://github.com/microsoft/playwright/issues/33566) — new headless implementation (November 2024); may affect canvas timing behavior
- [Playwright iframe handling — TestMu AI guide](https://www.testmuai.com/learning-hub/handling-iframes-in-playwright/) — `frame_locator()` vs. legacy `Frame` approach; cross-origin iframe patterns
- [Playwright canvas automation — Medium guide](https://smrutisouravsahoo06.medium.com/the-secret-to-automating-canvas-elements-playwright-js-revealed-c2249e522083) — coordinate-based canvas clicking; `getBoundingClientRect()` for position calculation
- [Claude Vision API official docs](https://platform.claude.com/docs/en/build-with-claude/vision) — 5 MB per-image limit; 200px minimum for quality; structured output for reliable JSON extraction; images below 200px degrade quality
- [Claude Vision limitations — official docs](https://platform.claude.com/docs/en/build-with-claude/vision#limitations) — limited spatial reasoning; imprecise counting; reduced accuracy on small or stylized text
- [Claude Structured Outputs — official docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) — schema-guaranteed JSON responses; tool-use approach vs. prompt-only JSON extraction
- [discord.py Rate Limits — issue #9418](https://github.com/Rapptz/discord.py/issues/9418) — rate limit occasionally produces errors instead of auto-retry warnings
- [Blocking vs Non-Blocking IO — Discord Bot Tutorial](https://tutorial.vcokltfre.dev/tips/blocking/) — event loop freezing mechanics; heartbeat blocking consequences; `run_in_executor` pattern
- [Letter League Discord FAQ](https://support-apps.discord.com/hc/en-us/articles/26502196674583-Letter-League-FAQ) — 27x19 expandable board; up to 8 players per game
- [Wordbot reference implementation](https://github.com/vike256/Wordbot) — CLI word lookup only; no board reading or automation; confirms no prior art for this project's full scope

---
*Pitfalls research for: Letter League Bot v1.1 — vision + Discord bot + browser automation additions*
*Researched: 2026-03-24*
