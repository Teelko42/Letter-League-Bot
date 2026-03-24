# Project Research Summary

**Project:** Letter League Bot v1.1 — Vision + Discord + Browser Automation
**Domain:** Discord word game AI bot extending a shipped Python word engine
**Researched:** 2026-03-24
**Confidence:** HIGH (Vision pipeline, Discord integration, stack), MEDIUM (Playwright autonomous mode — live testing required)

## Executive Summary

Letter League Bot v1.1 adds three capability layers on top of a shipped, validated v1.0 word engine: a Claude Vision pipeline that reads board screenshots, a discord.py advisor bot that responds to user-submitted screenshots with move recommendations, and a Playwright-driven autonomous player that navigates Discord's web client to play games independently. All research converges on the same build order: vision pipeline first (highest risk, shared critical path), then the Discord advisor (closes the MVP loop with zero TOS risk), then browser automation infrastructure, then autonomous play (highest complexity, non-trivial TOS constraints). The v1.0 engine — GADDAG, move generation, scoring, difficulty — is untouched; all new code is additive.

The dominant risk in this milestone is not technical complexity but Discord's Terms of Service. Automating a user account to play Discord Activities ("self-bot") has been actively enforced since 2017, with bans accelerating through 2021-2023. There is no API path for bots to join Activities. The only viable autonomous mode approach is Playwright driving a dedicated, isolated throwaway Discord account in a browser. This is architecturally sound but carries a permanent account ban risk. The advisor mode carries zero TOS risk and delivers core value independently. Research unanimously recommends shipping advisor mode first and treating autonomous mode as a separate, documented-risk feature.

The remaining technical risk is vision accuracy. Letter League renders on an HTML5 canvas inside a cross-origin Discord Activity iframe. At typical Discord resolution, board tiles are 15-25px — below the 200px threshold where Claude Vision quality degrades. The mitigation is to crop and upscale the screenshot to the board region before sending to the API, and to gate the vision phase on achieving less than 2% per-tile error rate across 20 or more ground-truth screenshots before connecting vision output to the word engine.

## Key Findings

### Recommended Stack

All v1.1 new dependencies are verified as of March 2026. The stack adds exactly three major libraries on top of the existing Python 3.11 environment: `discord.py 2.7.1` for bot gateway and slash commands, `anthropic 0.86.0` for the Claude Vision API client (use `AsyncAnthropic` — the sync client blocks discord.py's event loop), and `playwright 1.58.0` for browser automation (use `playwright.async_api` exclusively — the sync API raises a hard `RuntimeError` inside asyncio). Supporting libraries are `Pillow 12.1.1` for screenshot preprocessing, `opencv-python 4.13.0.92` for board grid detection, `aiosqlite 0.22.1` for async state persistence, and `loguru 0.7.3` for structured logging. On Windows (current dev environment), Playwright requires `ProactorEventLoop`, which Python 3.11 sets automatically — no manual configuration needed.

The recommended Claude model is `claude-sonnet-4-6` at approximately $0.004 per 1-megapixel board screenshot. Do not use Haiku 3 — it retires April 19, 2026. Downgrade to `claude-haiku-4-5` only after accuracy validation on real boards.

**Core technologies:**
- `discord.py 2.7.1`: Discord gateway, slash commands, attachment handling — only maintained first-party Python Discord library; v2.x has native `app_commands` and full asyncio integration
- `anthropic 0.86.0`: Claude Vision API client — official SDK with type safety, retry logic, rate-limit handling; use `AsyncAnthropic` for non-blocking use in asyncio; model `claude-sonnet-4-6`
- `playwright 1.58.0`: Chromium browser automation — superior to Selenium for modern SPAs; first-class async API; native `frame_locator()` for cross-origin iframe interaction; required for Discord Activity navigation
- `Pillow 12.1.1`: Screenshot preprocessing — resize and crop before API calls to stay under 1568px and improve token efficiency
- `opencv-python 4.13.0.92`: Board grid boundary detection — separates structural detection (OpenCV) from content reading (Claude Vision)
- `aiosqlite 0.22.1`: Async SQLite for user difficulty persistence and session state — non-blocking within discord.py's event loop

### Expected Features

The feature dependency chain is strict: the vision pipeline must be complete before either the Discord advisor or autonomous mode can function. Vision is the shared critical path. Autonomous mode must not be built until advisor mode has been validated in real game sessions.

**Must have for v1.1 (P1 — advisor mode complete):**
- Vision pipeline: grid + rack extraction from screenshot to structured JSON, with `BoardState` validation before engine handoff
- Discord bot process with proper token auth, guild registration, slash command tree sync
- `/analyze` slash command accepting `discord.Attachment`, returning top-3 move recommendations as an ephemeral response
- `BoardState` JSON to `GameEngine` bridge (`session.sync_board()` rebuilding engine board from extracted state)
- Error handling for bad screenshots, vision API failures, and zero-valid-moves cases
- `/setdifficulty` command with Classic/Wild mode parameter

**Should have after advisor validation (P2):**
- Score breakdown per component (requires minor `Scorer` touch to return a breakdown dict, not just total)
- Per-user difficulty persistence (aiosqlite keyed on `user_id`)
- Two-shot vision retry on parse failure
- Region crop before API call (saves ~$0.002/call, improves accuracy)
- Bingo callout for 7-tile plays

**Defer to autonomous mode phase (P3):**
- Playwright Chromium persistent session and Discord web login
- Activity iframe screenshot capture and parsing (reuses the vision pipeline exactly)
- Board pixel coordinate mapping (no DOM structure; pure visual grid detection)
- Turn detection via visual state change
- Rack tile and board cell click sequences for word placement

### Architecture Approach

The architecture follows a strict layered pattern — "thin cog, fat engine" — where Discord Cogs contain only event wiring and formatting, with zero game logic. All logic lives in `src/` packages (`src/vision/`, `src/engine/`, `src/automation/`) that have no `discord.py` imports and are fully testable without a live bot connection. A `GameSession` per Discord channel holds the `GameEngine` instance (stateful across turns via `play_move()`), difficulty setting, and scoring mode. The `BoardState` dataclass (`src/vision/models.py`) is the explicit contract between the vision pipeline and the word engine: vision produces it, `session.sync_board()` applies it to the engine's board, and `engine.find_moves()` consumes the result.

**Major components:**
1. `src/vision/` (Phase 3) — `extractor.py` takes `bytes`, calls `anthropic.AsyncAnthropic().messages.parse()` with a Pydantic schema, returns typed `BoardState`; `models.py` defines `ExtractedCell` and `BoardState` dataclasses; `prompt.py` holds the structured extraction system prompt. No `discord.py` imports.
2. `bot/` (Phase 4) — `main.py` sets up the bot with `message_content` privileged intent; `cogs/advisor.py` is the `/analyze` handler (always `defer()` before async work); `session.py` owns per-channel `GameEngine` + `DifficultyEngine` state. All Cog methods stay thin.
3. `src/automation/` (Phase 5) — `browser.py` manages Playwright persistent context lifecycle; `navigator.py` navigates Discord to the Activity iframe using `frame_locator()`; `placer.py` clicks rack tiles and board squares using canvas-relative coordinates.
4. `bot/cogs/autoplay.py` (Phase 6) — `discord.ext.tasks` background loop orchestrating the per-turn screenshot → vision → engine → click cycle; `/autoplay`, `/stop`, `/difficulty` commands.

### Critical Pitfalls

1. **Playwright sync API inside discord.py** — raises `RuntimeError: This event loop is already running` and freezes the bot. Use `playwright.async_api` exclusively throughout the entire codebase. Verify in the browser automation foundation phase before any game logic is built on top.
2. **Canvas screenshot blank in headless Chromium** — Letter League renders on an HTML5 canvas; headless mode captures blank output if the screenshot is taken before JavaScript compositing completes. Use `wait_for_load_state("networkidle")` plus a game-specific render signal. Fall back to `canvas.toDataURL()` JavaScript extraction if timing waits are insufficient.
3. **Claude Vision hallucination on small tiles** — at typical Discord resolution, board tiles may be under the 200px quality threshold. Crop the screenshot to the board region and upscale before sending. Request structured Pydantic output (not plain text JSON) to guarantee schema compliance. Gate the vision phase on less than 2% per-tile error rate across 20+ ground-truth screenshots.
4. **Discord interaction timeout** — the slash command acknowledgment window is 3 seconds; the vision API call takes 4-15 seconds. The first line of every handler doing async work must be `await interaction.response.defer()`. Use `interaction.followup.send()` after deferring — never `interaction.response.send_message()`.
5. **Self-bot TOS violation** — automating a Discord user account violates Discord's Terms of Service and results in permanent account bans. Use a dedicated throwaway account for autonomous mode, document the risk explicitly in the setup guide, and build advisor mode first (zero TOS risk).
6. **Word engine blocking the event loop** — the v1.0 GADDAG engine is synchronous and CPU-bound. Wrap all engine calls with `await asyncio.to_thread(engine_fn, *args)` in Discord handlers to avoid freezing the event loop and missing Discord heartbeats.

## Implications for Roadmap

The v1.1 milestone continues phase numbering from v1.0 (which ended at Phase 2). The v1.0 engine (Phases 1-2) is complete and untouched. V1.1 adds four phases:

### Phase 3: Vision Pipeline
**Rationale:** The vision pipeline is the shared critical path for all v1.1 features. Both advisor and autonomous mode feed through the same `extract_board_state()` call. It is also the highest-risk item — small tile size, hallucination risk, canvas rendering. Gating everything else on a validated vision layer is the only defensible order.
**Delivers:** `src/vision/` package — `BoardState` dataclass, structured extraction prompt, `extract_board_state(image_bytes) -> BoardState`, board sync path to existing `GameEngine`. Validated against 20+ ground-truth screenshots with less than 2% per-tile error rate before connecting to the engine.
**Addresses:** Vision pipeline P1 features: grid extraction, rack extraction, multiplier square detection, output validation, graceful failure on bad screenshots.
**Avoids:** Vision hallucination (crop + upscale + Pydantic schema + accuracy gate), board state drift (treat each read as authoritative, never delta-accumulate), `BoardState` contract mismatch (end-to-end integration test: screenshot → vision → engine → valid move list).
**Research flag:** Needs research and iteration — accurate prompt engineering for structured board extraction has no public prior art for Letter League specifically. Plan for multiple prompt iterations against real screenshots.

### Phase 4: Discord Advisor Mode
**Rationale:** Closes the MVP loop with zero TOS risk. Advisor mode is the primary value delivery for v1.1: users get move suggestions by uploading screenshots to Discord. No Playwright needed. Validates the entire vision-to-engine pipeline in real usage before any automation is built.
**Delivers:** `bot/` package — `main.py`, `session.py`, `cogs/advisor.py`, `/analyze` slash command with ephemeral top-3 move response, `/setdifficulty` command, error handling for bad screenshots. Full end-to-end: user uploads screenshot → bot replies with best move.
**Implements:** `GameSession` (per-channel stateful engine), `AdvisorCog` (thin Discord layer), Discord bot process (privileged `message_content` intent, slash command tree sync).
**Avoids:** Interaction timeout (`defer()` as first line of every handler), event loop blocking (`asyncio.to_thread()` for engine calls), image validation gaps (check `content_type` and file size before processing).
**Research flag:** Standard patterns — discord.py slash commands, attachment handling, and Cog structure are well-documented. No research-phase needed.

### Phase 5: Browser Automation Foundation
**Rationale:** Isolated engineering spike to validate that Playwright can navigate Discord's web client, reach a Letter League Activity iframe, and capture a non-blank canvas screenshot. This is the highest-uncertainty phase — no public prior art exists for Playwright + Discord Activities. Must be completed and validated before any game-playing logic is built on top.
**Delivers:** `src/automation/browser.py` (persistent Playwright context lifecycle), `src/automation/navigator.py` (Discord login → voice channel → Activity iframe). Validation gate: non-blank screenshot of Letter League game canvas captured from within the iframe in headless mode.
**Avoids:** Playwright sync API conflict (`async_playwright` throughout), headless canvas blank (wait strategy + `canvas.toDataURL()` fallback), iframe cross-origin blocking (`frame_locator()` scoped to correct iframe by URL pattern, validated empirically), account security (dedicated throwaway account, TOS risk documented before implementation begins).
**Research flag:** Needs research and spiking — Discord Activity iframe structure is undocumented; exact selectors, canvas rendering timing, and headless compatibility all require live testing. Inspect the DOM in headed mode with DevTools before writing automation code.

### Phase 6: Autonomous Play
**Rationale:** Depends on all preceding phases. Requires a validated vision pipeline (Phase 3), a working advisor session model (Phase 4), and proven browser automation infrastructure (Phase 5). Build last; the integration is the combination of all prior work plus tile placement clicks.
**Delivers:** `src/automation/placer.py` (rack tile + board cell click sequences using canvas-relative coordinates), `bot/cogs/autoplay.py` (`discord.ext.tasks` background game loop, `/autoplay`, `/stop`, `/difficulty` commands). Full autonomous flow: bot joins game, detects turn visually, places word, loops until game end.
**Avoids:** Board state drift (full re-read each turn, consistency check against previous state), browser re-launching per turn (persistent context from Phase 5), frame reference caching across reconnects (re-acquire `frame_locator` each turn), self-bot TOS risk (dedicated throwaway account, human-paced timing jitter of 1-3s between tile clicks).
**Research flag:** Needs research — tile placement coordinate mapping (pixel position of each board cell relative to canvas bounding box) must be derived from live visual grid detection or empirically measured. No public prior art for Letter League.

### Phase Ordering Rationale

- **Vision before everything else:** The shared `extract_board_state()` call is the dependency for both advisor and autonomous mode. Validating it independently (no Discord, no Playwright) is the safest path and gives the highest-confidence foundation.
- **Advisor before autonomous:** Advisor mode is the lower-stakes validation environment for the vision-to-engine pipeline. Errors in advisor mode result in a wrong suggestion that the user can ignore; errors in autonomous mode result in the bot placing invalid tiles. The engine must be proven reliable before trusting it to click.
- **Browser automation before autonomous play:** Phase 5 is a pure infrastructure spike. Mixing game-playing logic into an unvalidated automation layer adds debugging surface area. The three Playwright unknowns (canvas in headless, iframe access, persistent session) must be resolved in isolation.
- **Autonomous play last:** It depends on all three prior phases and introduces the TOS risk. Deferring it last ensures the project delivers value even if autonomous mode proves infeasible or too risky.

### Research Flags

Phases needing deeper research or live spiking during planning:
- **Phase 3 (Vision Pipeline):** Prompt engineering for structured board extraction requires iteration on real Letter League screenshots. The 27x19 grid with Wild mode color coding has no public prior art. Test accuracy early and gate phase completion on the error rate target.
- **Phase 5 (Browser Automation Foundation):** Discord Activity iframe selectors, canvas rendering timing in headless Chromium, and anti-automation detection behavior are all undocumented. Treat as an exploratory spike. Empirically inspect the DOM in headed mode before writing any automation code.
- **Phase 6 (Autonomous Play):** Board cell pixel coordinate mapping from canvas bounding box has no reference implementation for Letter League. Requires live measurement or visual grid detection at game start. Budget for significant iteration.

Phases with standard patterns (no research-phase needed):
- **Phase 4 (Discord Advisor Mode):** discord.py slash command attachment handling, Cog structure, `defer()`/`followup` pattern, and `asyncio.to_thread()` for sync engine calls are thoroughly documented. Implementation can proceed directly from architecture plans.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All versions verified against PyPI and official docs March 2026. `anthropic 0.86.0`, `discord.py 2.7.1`, `playwright 1.58.0`. Python 3.11 compatibility confirmed for all. Windows `ProactorEventLoop` confirmed automatic. |
| Features | HIGH | Feature set is well-defined by architecture constraints. P1/P2/P3 priority split is unambiguous. Dependency chain (vision → advisor → autonomous) is hard and enforced by the architecture. |
| Architecture | HIGH (integration patterns), MEDIUM (Activity iframe specifics) | Thin-cog pattern, `BoardState` contract, async boundaries — all verified against official docs. Exact Discord Activity iframe selectors and canvas rendering behavior require live validation. |
| Pitfalls | HIGH (known failure modes), MEDIUM (Letter League-specific behaviors) | Playwright sync/async conflict, canvas blank, interaction timeout, event loop blocking, TOS risk — all sourced from official docs and confirmed issue trackers. Letter League canvas rendering timing and iframe structure require empirical testing. |

**Overall confidence:** MEDIUM-HIGH. The architecture and implementation approach are solid. The two unknowns are (1) vision accuracy on real Letter League screenshots at Discord resolution and (2) whether Playwright can reliably navigate Discord's Activity iframe in headless mode. Both are testable early and gating the subsequent phases on their validation is the right risk mitigation.

### Gaps to Address

- **Vision accuracy on real boards:** No ground-truth screenshots exist yet. The Phase 3 plan must include capturing 20+ screenshots from real games and measuring per-tile error rate before the vision pipeline is considered shippable. Target: less than 2% per-tile error, zero catastrophic misreads (rack tiles reported as board tiles or vice versa).
- **Discord Activity iframe selector:** The exact `src` attribute or CSS selector identifying the Letter League iframe inside Discord's web client is not documented. Requires a manual inspection session using headed Playwright with browser DevTools before navigator code is written.
- **Headless canvas rendering:** Whether the Letter League canvas renders correctly in headless Chromium or requires headed mode (with Xvfb on Linux or a virtual display) is unknown until tested. This affects the deployment model for autonomous mode.
- **Letter League dictionary vs. Wordnik:** The v1.0 engine uses the Wordnik word list. Letter League may use a proprietary dictionary. Suggestions should be labeled "likely valid (Wordnik)" until a known-valid test word set validates the overlap rate.
- **Scorer breakdown API:** The existing `Scorer` returns a total score, not a per-component breakdown. Showing "Z=10 on DL(x2)=20 + cross APES=8 = total 42" in advisor responses requires touching the v1.0 `Scorer`. Plan this explicitly in Phase 4 to avoid unplanned scope creep into the v1.0 engine.
- **Turn detection signal:** The autonomous mode game loop needs a reliable signal for "it is now the bot's turn." The specific UI element or state change that indicates turn handoff in Letter League requires in-game observation during Phase 5.

## Sources

### Primary (HIGH confidence)
- [Anthropic Claude Models Overview](https://platform.claude.com/docs/en/about-claude/models/overview) — model IDs `claude-sonnet-4-6`, `claude-haiku-4-5-20251001`, pricing, vision support, Haiku 3 deprecation April 19, 2026
- [Anthropic Vision Docs](https://platform.claude.com/docs/en/build-with-claude/vision) — image formats, 5MB API limit, base64 encoding, 200px minimum for quality, token cost formula
- [Anthropic Structured Outputs Docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) — `messages.parse()` with Pydantic, schema-guaranteed JSON output
- [discord.py official docs](https://discordpy.readthedocs.io/en/latest/) — `Attachment.read()`, `app_commands`, Cog structure, privileged intents, `ext.tasks`
- [Discord Self-Bot TOS Policy](https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots) — explicit self-bot prohibition, permanent ban consequence
- [Discord Activities Architecture](https://docs.discord.com/developers/activities/how-activities-work) — iframe + postMessage architecture, OAuth scope requirement, no programmatic bypass
- [Playwright Python async API docs](https://playwright.dev/python/docs/api/class-playwright) — `frame_locator()`, `launch_persistent_context()`, screenshot `clip`, `async_playwright()`
- [Playwright GitHub issue #19225](https://github.com/microsoft/playwright/issues/19225) — canvas screenshot blank in headless; resolution is wait strategy
- [Playwright GitHub issue #33566](https://github.com/microsoft/playwright/issues/33566) — new headless Chromium in v1.49+ (November 2024); may affect canvas timing
- [discord.py PyPI](https://pypi.org/project/discord.py/) — v2.7.1 verified March 2026
- [anthropic PyPI](https://pypi.org/project/anthropic/) — v0.86.0 released 2026-03-18
- [playwright PyPI](https://pypi.org/project/playwright/) — v1.58.0 released 2026-01-30
- [discord.py FAQ — Blocking vs. Non-Blocking](https://discordpy.readthedocs.io/en/stable/faq.html) — `run_in_executor` recommendation for sync code in async handlers

### Secondary (MEDIUM confidence)
- [discord.py 2.5.0 changelog](https://discordpy.readthedocs.io/en/stable/) — enhanced attachment properties in 2.5+
- [Discord Platform Manipulation Policy](https://discord.com/safety/platform-manipulation-policy-explainer) — self-bot enforcement history, ban intensity 2021-2023
- [Letter League Discord FAQ](https://support-apps.discord.com/hc/en-us/articles/26502196674583-Letter-League-FAQ) — 27x19 expandable board, up to 8 players per game
- [GitHub vike256/Wordbot](https://github.com/vike256/Wordbot) — CLI-only reference; no board reading or Discord integration; confirms scope gap this project fills

### Tertiary (LOW confidence — requires live validation)
- Discord Activity iframe CSS selectors — must be empirically inspected in headed mode; no public documentation
- Letter League canvas rendering timing signals — must be measured against real game sessions; no prior art
- Letter League word list coverage vs. Wordnik — must be tested against known game-accepted and game-rejected words

---
*Research completed: 2026-03-24*
*Ready for roadmap: yes*
