# Pitfalls Research

**Domain:** Discord word game AI bot (vision + browser automation + Scrabble-like AI)
**Researched:** 2026-03-23
**Confidence:** MEDIUM (domain-specific knowledge synthesized from Playwright, discord.py, OCR, and Scrabble AI sources; Letter League has sparse public technical documentation)

---

## Critical Pitfalls

### Pitfall 1: Using Playwright's Sync API Inside discord.py's Async Event Loop

**What goes wrong:**
Playwright has both sync and async Python APIs. discord.py runs entirely on an asyncio event loop. If you instantiate or call Playwright using the sync API anywhere inside a discord.py coroutine or event handler, Python throws `RuntimeError: This event loop is already running` and the bot either crashes or deadlocks. This is one of the most frequently hit integration bugs in Python async projects.

**Why it happens:**
Developers familiar with Playwright from testing contexts use `sync_playwright()` without realizing discord.py already owns the event loop. Playwright's sync API internally creates its own event loop, which conflicts with the running one.

**How to avoid:**
Use `playwright.async_api` exclusively throughout the project. Initialize with `async with async_playwright() as p:` inside async functions. Never call `sync_playwright()` anywhere in the codebase. Structure the autonomous mode as a long-lived async Playwright session managed alongside the bot's async lifecycle.

**Warning signs:**
- `RuntimeError: This event loop is already running` in logs
- `RuntimeError: No running event loop` when called from threads
- Bot freezes after triggering autonomous mode

**Phase to address:**
Browser automation foundation phase — verify the async Playwright integration works end-to-end before building any game logic on top of it.

---

### Pitfall 2: Canvas Element Screenshot Gaps in Playwright

**What goes wrong:**
Letter League renders its game board as a canvas element inside an iframe. Playwright has a documented bug where `<canvas>` elements do not appear in screenshots taken via `page.screenshot()` — the canvas renders blank even though the page appears normal in a real browser. This means the screenshot-then-OCR pipeline silently captures nothing useful.

**Why it happens:**
Canvas rendering in headless Chromium has timing and compositing differences from headed mode. The browser may not have fully composited the canvas frame before the screenshot is taken. This is a known Playwright GitHub issue (#19225).

**How to avoid:**
- Use `page.screenshot()` with `{ fullPage: false }` and explicitly wait for canvas-specific render signals (e.g., wait for a known UI element that only appears after the board fully loads)
- Test screenshots in headed mode first to verify canvas content is visible
- Consider using `element.screenshot()` directly on the canvas element rather than the full page
- Evaluate whether injecting JavaScript to extract canvas pixel data (`canvas.toDataURL()`) is more reliable than page-level screenshots

**Warning signs:**
- Screenshots show the UI chrome (buttons, rack) but the board area is blank or a solid color
- OCR pipeline returns empty results or only captures text from outside the board
- Works in headed mode, fails in headless

**Phase to address:**
Browser automation foundation phase — validate canvas screenshot capture produces usable images before building any vision or OCR pipeline.

---

### Pitfall 3: Vision LLM Board State Hallucination on Ambiguous Tiles

**What goes wrong:**
AI vision models (Claude, GPT-4o) hallucinate tile identities when tiles are ambiguous, partially occluded, share visual similarity (e.g., `I` vs `l` vs `1`, `O` vs `0`, `W` vs `M` rotated), or when the canvas rendering is at low DPI. A vision model may confidently return a board JSON that contains 1-2 wrong tiles, which the word-finding engine then uses to generate invalid or sub-optimal plays. The error is silent — no exception is raised.

**Why it happens:**
VLMs optimize for plausible output, not pixel-perfect accuracy. Game tiles in Letter League use a stylized custom font with decorative serifs and tile backgrounds that confuse character recognition. Hallucination rates for structured visual extraction tasks remain 6-48% depending on model (as of 2025 benchmarks), worse for fine-grained spatial layout tasks.

**How to avoid:**
- Request structured JSON output from the vision model with explicit per-tile coordinates, not just a flat board string
- Ask the model to flag tiles it is uncertain about (confidence < threshold) rather than always committing
- Cross-validate: after OCR/vision extraction, verify the result is internally consistent (all placed words are valid dictionary words at their reported positions)
- Build a verification step that re-prompts with a cropped region when a tile is uncertain
- Compare two independent extractions and flag disagreements

**Warning signs:**
- Bot plays invalid words that were not in the dictionary
- Scoring calculations are consistently off by small amounts
- Board positions of words drift over successive turns despite no new plays

**Phase to address:**
Vision/board-reading phase — must include extraction accuracy validation with ground-truth test screenshots before connecting to the word-finding engine.

---

### Pitfall 4: Board State Drift Between Turns (Stale State Problem)

**What goes wrong:**
The bot maintains an internal representation of the board built from successive OCR/vision reads. Over time, a small per-turn error (one misread tile, one missed multiplier square) compounds. After 10-15 turns the bot's internal board model diverges significantly from the real game board. The bot then evaluates moves against a wrong board, producing invalid plays or missing high-value opportunities.

**Why it happens:**
Developers treat board reading as "good enough" on a per-turn basis without implementing any reconciliation. Each turn's read has ~95%+ accuracy, but accumulated over 20 turns with a 5% error rate per read, the board model becomes unreliable. The expandable board (grows beyond 27x19) also means the coordinate system must be recalculated as the board grows, and a missed expansion invalidates all future absolute coordinates.

**How to avoid:**
- Treat every turn's vision output as the authoritative board state — do NOT accumulate delta updates; always re-extract the full board each turn
- Implement a consistency check: the newly read board must contain all tiles from the previous read (tiles never disappear); if they don't, flag as a read error and retry
- Track board dimensions separately; detect when new rows/columns appear and adjust coordinate mapping
- Never store board state across a bot restart; always re-read from a screenshot

**Warning signs:**
- Moves that the bot calculates as valid are rejected by the game (word not connected, tile collision)
- Bot's score estimate for a play doesn't match what the game awards
- Increased error frequency in later turns of the same game

**Phase to address:**
Board state management (within the vision phase) — design state as ephemeral-per-turn from the start, not as an accumulated model.

---

### Pitfall 5: Self-Bot TOS Violation — Automating a User Account

**What goes wrong:**
Discord Activities (including Letter League) require a human user account to join a voice channel and start the activity. A naive implementation uses Playwright to log in as a real user account and automate it — this is a "selfbot" and is explicitly prohibited by Discord's Terms of Service. Discord actively detects selfbot behavior and permanently bans the user account used. The entire autonomous mode becomes non-functional.

**Why it happens:**
Discord Activities don't expose a bot API — bots cannot join voice channels as players or interact with Activities via the Discord API. The only automation path that's obvious is to automate a user account via browser. Developers implement this without realizing the TOS implications.

**How to avoid:**
- Use a dedicated, isolated Discord account for automation — never a personal account
- Keep automated interactions human-paced (1-3 second delays between clicks, no burst actions)
- Do not use discord.py or any Discord API client alongside browser automation on the same account (mixing API calls + browser automation is a strong selfbot signal)
- Accept the risk: this is a design constraint of the project. Document the TOS risk clearly and instruct users to use a throwaway account
- For advisor mode (screenshot analysis only), there is zero TOS risk — the bot never touches Discord programmatically; users submit screenshots manually

**Warning signs:**
- Discord prompts for verification (phone/captcha) during automated login
- Account receives a "suspicious login" email
- Account is temporarily locked or permanently suspended

**Phase to address:**
Autonomous mode implementation phase — flag the TOS risk explicitly in documentation before shipping; build advisor mode first as it has zero TOS risk.

---

### Pitfall 6: iframe Cross-Origin Blocking Playwright Interaction

**What goes wrong:**
Letter League runs as an embedded iframe inside Discord's Electron/web client. Playwright can screenshot the outer Discord page, but interacting with elements inside a cross-origin iframe (different domain from `discord.com`) requires special handling. Without it, Playwright cannot locate or click game elements, and element locators return null or throw frame-not-found errors.

**Why it happens:**
Browsers enforce the Same-Origin Policy. Discord's Activity iframe loads the game from a different origin (not `discord.com`), so direct element access fails. Developers write selectors against the main page context and are confused when they find nothing, because the game elements live in a separate frame context.

**How to avoid:**
- Use Playwright's `frame_locator()` to explicitly scope all game interaction to the iframe context
- Identify the correct frame by URL pattern or name attribute rather than position (position-based frame indexing breaks when Discord adds/removes other iframes)
- Test frame access separately from game logic — confirm you can click a known static button before building dynamic move execution
- Canvas-based interaction (clicking board positions) requires coordinate-based clicks relative to the canvas element's bounding box; semantic selectors do not exist inside a canvas

**Warning signs:**
- `ElementHandle: target closed` errors
- Locators find 0 elements that visually exist on screen
- Works when tested against the game's standalone URL but fails inside Discord

**Phase to address:**
Browser automation foundation phase — validate iframe navigation and element access before any game logic is implemented.

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcode 27x19 board dimensions | Simplifies coordinate math | Breaks on any board expansion; game is designed to grow | Never — board expansion is a core mechanic |
| Use Tesseract OCR instead of vision LLM for board reading | Cheaper, faster, no API cost | Custom game font likely requires model retraining; ~80% accuracy on stylized fonts is too low for correct play | Only as a fallback with accuracy benchmarking |
| Accumulate board state as deltas between turns | Lower per-turn API cost | Errors compound; after 10+ turns model is unreliable | Never for the canonical board model; acceptable for a debug/diff view |
| Use Playwright sync API in a thread alongside discord.py | Avoids async complexity | Creates thread-safety issues, event loop conflicts, and unpredictable crashes | Prototype only; must be refactored before any real use |
| Generate all possible moves and pick highest score (greedy) | Simple to implement | Misses strategic rack management, ignores opponent scoring opportunities | Acceptable for MVP; document as known limitation |
| Use `time.sleep()` in discord.py handlers | Easy to write | Blocks the event loop; bot stops responding to all events during sleep | Never — use `asyncio.sleep()` |
| Store bot token in source code or .env committed to repo | Convenient | Token exposure leads to bot compromise and Discord account ban | Never |

---

## Integration Gotchas

Common mistakes when connecting to external services.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Discord API (discord.py) | Calling `message.channel.send()` in a tight loop without rate limit awareness | Use discord.py's built-in rate limit handling; space out messages; never send more than one message per command response |
| Discord API | Treating the 3-second interaction token window as generous | Defer the interaction immediately with `interaction.response.defer()` before doing any async work; vision + word-finding takes seconds |
| Playwright (iframe) | Using `page.locator()` for elements inside the game iframe | Use `page.frame_locator('[src*="discord.com/activities"]').locator(...)` to scope to the correct frame |
| Vision LLM (Claude/GPT) | Sending a full 1920x1080 screenshot for board extraction | Crop to the board area first; full screenshots include irrelevant Discord UI that confuses the model and inflates token cost |
| Vision LLM | Expecting pixel-perfect tile coordinate output | Always request a bounding-box grid + tile letter separately; validate against expected board dimensions |
| Wordnik wordlist | Assuming the wordlist covers all Letter League valid words | Letter League may use a proprietary dictionary subset; words in Wordnik may not be valid in-game, and vice versa. Test a known-valid word set against the game |
| Wordnik wordlist (file) | Loading the full word list into memory as a Python list for lookups | Use a set or DAWG/GADDAG structure; list membership check is O(n), which is unusable at 200k+ words under real-time move generation |

---

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Linear word search in Python list | Move generation takes 30+ seconds per turn | Load dictionary into a `set` for O(1) lookup; build GADDAG for full move generation | At 170k+ word dictionary with 7-tile rack, naive generation tries millions of combinations |
| Generating all valid moves without pruning | Bot uses 100% CPU for 10+ seconds per turn | Implement anchor-square-based pruning (GADDAG); only generate moves connected to existing board tiles | Any real game with >5 words on board |
| Calling the vision LLM API synchronously in a discord.py handler | Bot stops responding to all other commands during board analysis | Use `asyncio.create_task()` or `executor` to run vision analysis without blocking the event loop | Every single turn if not handled |
| Taking full-page screenshots (1920x1080+) and sending raw to vision API | High token cost, slow response, worse accuracy | Crop to board region before sending; target ~512x512 or use tile-level crops for uncertain regions | First time you check the API bill |
| Re-downloading/re-parsing the Wordnik wordlist on every bot startup | 10-30 second startup time, network dependency | Parse once, serialize to a binary format (pickle, SQLite, or DAWG binary); load the compiled structure at startup | Fine for dev; breaks in any production restart scenario |

---

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Storing Discord bot token in plaintext in code or committed .env | Token theft allows full bot impersonation, spamming all servers the bot is in | Use environment variables; never commit tokens; rotate immediately if exposed |
| Logging full screenshots to disk without sanitization | Discord screenshots may contain other users' private messages visible in the background | Log only the cropped board region; never log full Discord client screenshots |
| Using a personal Discord account for autonomous mode automation | Permanent personal account ban if Discord detects selfbot behavior | Use a dedicated throwaway account; document this requirement prominently |
| Exposing the bot's vision API key in client-side code or logs | API key misuse, unexpected billing | Store keys server-side only; never include in any message or log output |
| No input validation on screenshot uploads (advisor mode) | Malformed images could crash the vision pipeline or trigger unexpected LLM behavior | Validate file type and size before sending to vision API; cap image dimensions |

---

## UX Pitfalls

Common user experience mistakes in this domain.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Bot suggests a word that is valid in the dictionary but invalid in Letter League | User plays the word, it's rejected, turn is wasted, trust in bot is destroyed | Clearly document that the bot uses Wordnik as a proxy for Letter League's dictionary, which may diverge; label suggestions as "estimated valid" |
| Advisor mode response takes 15+ seconds with no feedback | User thinks the bot is broken or the command failed | Always acknowledge the command immediately ("Analyzing board..."), then edit/follow up with results |
| Difficulty percentage produces no visible behavioral difference between 40% and 60% | Users can't calibrate bot strength; feature feels broken | Implement difficulty as a deterministic suboptimal move selector with measurable play quality differences; test that 40% produces a meaningfully lower average score than 60% |
| Bot plays legal but low-value words when at "beginner" difficulty | Users beat the bot too easily at low difficulty and conclude it's a bad bot | At low difficulty, prefer words that are "plausibly human" — common 3-4 letter words, not obscure legal words that score near-optimally |
| No indication of what the bot "sees" in the board before it plays | Users can't verify the board was read correctly; bot plays a move on the wrong position | In advisor mode, return a text representation of the parsed board alongside the suggestion so users can spot misreads |

---

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Board reading pipeline:** Often missing multiplier square detection — verify that DL/TL/DW/TW squares are correctly identified and factored into scoring, not just the tile letters
- [ ] **Word finder:** Often missing blank/wild tile handling — verify the engine correctly tries all 26 letter substitutions for wild tiles and doesn't score them with letter values
- [ ] **Move generator:** Often missing the bingo/all-tiles bonus check — verify that a 7-tile play receives the correct bonus if Letter League implements one
- [ ] **Autonomous mode:** Often looks done after a single successful test game — verify it handles edge cases: opponent disconnects mid-game, game ends unexpectedly, board screenshot timing issues during opponent's turn
- [ ] **Difficulty scaling:** Often "works" by just selecting a random move vs. the best move with no graduation — verify the full range 0%-100% produces measurably different average scores across many simulated games
- [ ] **Scoring engine:** Wild Mode vs Classic Mode scoring is implemented correctly and tested separately — a shared code path with an if/else is not enough; requires independent test cases
- [ ] **Dictionary loading:** The word set used for validation matches what the move generator uses — a mismatch means the generator finds words the validator rejects, or vice versa
- [ ] **Canvas capture:** Works in headless mode (not just headed) — canvas screenshot issues are headless-specific; always test in the deployment environment

---

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Board state drift detected mid-game | LOW | Force a full board re-read from screenshot; discard internal state entirely; log the delta for debugging |
| Vision LLM returns malformed or empty board | LOW | Retry with a fresh screenshot; if 3 retries fail, respond with error in Discord and skip the turn |
| Playwright canvas screenshot captures blank canvas | MEDIUM | Switch to JavaScript injection (`canvas.toDataURL()`) as fallback; rebuild screenshot pipeline |
| Discord account banned for selfbot behavior | HIGH | Create new account; redesign autonomous mode with more human-like timing; accept that this is an inherent risk of the approach |
| Playwright iframe interaction fails (frame not found) | MEDIUM | Re-probe for the correct frame each turn rather than caching the frame reference; Discord may reinitialize the iframe on reconnects |
| Word generator produces no valid moves | LOW | Implement pass/swap turn fallback; log the board state and rack for debugging; never let the bot hang indefinitely |
| Wordnik wordlist missing Letter League valid words | MEDIUM | Build a supplementary list from observed valid in-game words; treat Wordnik as the base, not the exclusive authority |

---

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Playwright sync vs async conflict | Browser automation foundation | Integration test: discord.py bot command triggers Playwright action; bot remains responsive throughout |
| Canvas screenshot blank in headless | Browser automation foundation | Screenshot test: capture Letter League canvas headless and headed; compare pixel content |
| Vision LLM hallucination on tiles | Board vision/OCR phase | Accuracy test: 20+ ground-truth screenshots with known boards; measure per-tile error rate |
| Board state drift | Board vision/OCR phase | Consistency test: re-read same board 5 times; verify identical output; check accumulation over simulated multi-turn sequence |
| TOS selfbot violation | Autonomous mode design (pre-implementation) | Documentation review: autonomous mode docs explicitly warn users to use dedicated accounts |
| iframe cross-origin blocking | Browser automation foundation | Smoke test: confirm `frame_locator()` successfully targets the game canvas before any game logic |
| Linear word search performance | Word-finding engine phase | Performance test: move generation completes in <2 seconds for any valid board state with 7-tile rack |
| Multiplier square misidentification | Board vision/OCR phase | Unit test: extract multiplier layout from known screenshot; compare against documented Letter League board layout |
| Wild tile scoring error | Scoring engine phase | Unit test: blank tile in optimal position scores 0 letter points but benefits from word multipliers correctly |
| Difficulty scaling non-differentiable | Difficulty implementation phase | Statistical test: run 100 simulated games at 0%, 50%, 100%; verify average scores are statistically distinct |

---

## Sources

- [Discord Rate Limits official documentation](https://docs.discord.com/developers/topics/rate-limits) — rate limiting behavior, Retry-After header, invalid request thresholds
- [Discord Automated User Accounts (Self-Bots) official policy](https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots) — TOS prohibition on selfbots
- [Discord Platform Manipulation Policy](https://discord.com/safety/platform-manipulation-policy-explainer) — enforcement and ban policy
- [discord.py FAQ — Blocking vs Non-Blocking](https://discordpy.readthedocs.io/en/stable/faq.html) — event loop blocking patterns, asyncio.sleep vs time.sleep
- [Playwright Python async API docs](https://playwright.dev/python/docs/library) — async API usage, event loop requirements
- [Playwright GitHub issue #19225 — canvas elements missing from screenshots](https://github.com/microsoft/playwright/issues/19225) — documented canvas screenshot bug
- [Playwright iframe handling guide](https://www.testmuai.com/learning-hub/handling-iframes-in-playwright/) — frame_locator usage, cross-origin iframe patterns
- [GADDAG Wikipedia](https://en.wikipedia.org/wiki/GADDAG) — Scrabble move generation data structure, performance characteristics
- [Gordon 1994 — A Faster Scrabble Move Generation Algorithm](https://ericsink.com/downloads/faster-scrabble-gordon.pdf) — GADDAG vs DAWG performance analysis
- [Coding the World's Fastest Scrabble Program in Python (Medium)](https://medium.com/@aydinschwa/coding-the-worlds-fastest-scrabble-program-in-python-2aa09db670e3) — Python implementation pitfalls
- [Tesseract OCR accuracy on game screenshots](https://groups.google.com/g/tesseract-ocr/c/ZsYvAIHWumA) — custom font failure modes, OCR on game boards
- [PyTesseract guide — OCR limits and alternatives (2025)](https://www.extend.ai/resources/pytesseract-guide-ocr-limits-alternatives) — ~80% real-world accuracy, preprocessing requirements
- [Wordnik wordlist GitHub repository](https://github.com/wordnik/wordlist) — dictionary format, coverage scope
- [Letter League Discord FAQ](https://support-apps.discord.com/hc/en-us/articles/26502196674583-Letter-League-FAQ) — board size (27x19 expandable), Wild vs Classic scoring modes
- [Letter League — TheLinuxCode guide](https://thelinuxcode.com/what-is-letter-league-in-discord/) — board expansion mechanics, multiplier squares
- [Wordbot reference implementation](https://github.com/vike256/Wordbot) — CLI-only, no board reading, no auto-play; confirms scope gap this project fills
- [Discord Activity iframe CSP compliance](https://dev.to/waveplay/patch-your-discord-activitys-network-requests-for-smooth-csp-compliance-432c) — cross-origin CORS and CSP issues with Activities
- [Anti-patterns in Playwright (Medium)](https://medium.com/@gunashekarr11/anti-patterns-in-playwright-people-dont-realize-they-re-doing-00f84cd7dff0) — coordinate-based clicking, brittle selectors
- [Playwright iFrame and Shadow DOM Automation (Automate The Planet)](https://www.automatetheplanet.com/playwright-tutorial-iframe-and-shadow-dom-automation/) — cross-origin iframe interaction patterns

---
*Pitfalls research for: Discord word game AI bot (Letter League)*
*Researched: 2026-03-23*
