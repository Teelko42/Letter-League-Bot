# Project Research Summary

**Project:** Letter League Bot
**Domain:** Discord word game AI bot (AI vision + browser automation + Scrabble-like move engine)
**Researched:** 2026-03-23
**Confidence:** MEDIUM

## Executive Summary

Letter League Bot is a Discord Activity assistant that combines three technically distinct domains: AI vision (to parse game board screenshots), Scrabble-like move generation (to find optimal word placements), and browser automation (to play autonomously). Experts building this type of product follow a strict layered architecture: Discord interactions stay in thin Cog wrappers, computation lives in an isolated pure-Python engine, and external I/O (vision API, browser) is confined to separate pipeline modules. The correct build order starts from the inside out — board data model, then dictionary/engine, then vision pipeline, then Discord integration, and only then autonomous play. Every prior implementation in the public space (vike256/Wordbot, 23f3000839/Letter_League_AI) stops well short of this project's full scope, meaning this bot has genuine differentiation room but also limited prior art to borrow from.

The recommended stack is Python 3.11 with discord.py 2.7.1, Playwright async for browser automation, and the Anthropic Claude Vision API for board reading. A custom GADDAG implementation against the Wordnik wordlist provides the move generation engine. This combination is the only way to support both advisor mode (screenshot upload → top moves) and autonomous mode (bot joins game and plays) without self-hosting an ML model or violating core async architecture constraints. The single largest technical risk is the vision pipeline: AI vision hallucination rates on custom game fonts, combined with Playwright's documented canvas screenshot bug in headless mode, make the board-reading layer the highest-uncertainty component in the entire system.

The primary risk vector is the autonomous mode's reliance on browser automation of a Discord user account — this is a structural TOS grey area that cannot be fully eliminated. The mitigation is to use a dedicated throwaway account, maintain human-paced click timing, and keep the API bot and browser automation accounts strictly separate. Advisor mode carries zero TOS risk and should be built and validated first before autonomous mode is attempted.

---

## Key Findings

### Recommended Stack

The project requires Python 3.11 as the ecosystem sweet spot: OpenCV has no Python 3.13 wheels yet, pytest-asyncio requires 3.10+, and 3.11 provides measurable performance improvements over earlier versions. discord.py 2.7.1 is the mandated framework and is actively maintained with full slash command support. Playwright's async API (1.58.0) is non-negotiable for autonomous mode — the sync API cannot coexist with discord.py's event loop. Claude Vision via the anthropic SDK (0.86.0) outperforms open-source OCR alternatives on styled game screenshots without requiring custom model training.

The word engine departs from off-the-shelf libraries: a custom GADDAG built on the Wordnik wordlist is recommended because GADDAG is ~2x faster than DAWG for move generation, handles the board's anchor/hook structure correctly, and can be adapted for Letter League's 27x19 expandable board. Supporting infrastructure is standard: aiosqlite for session state persistence, loguru for structured logging, numpy for board array representation, and uv for dependency management.

**Core technologies:**
- Python 3.11: runtime — ecosystem sweet spot, avoids 3.13 wheel gaps, best performance
- discord.py 2.7.1: Discord framework — only maintained first-party Python Discord library
- Playwright async 1.58.0: browser automation — only option that works inside discord.py's asyncio loop; native iframe support required for Discord Activities
- anthropic SDK 0.86.0 (Claude Vision): board reading — outperforms Tesseract/EasyOCR on styled game screenshots without custom training
- Custom GADDAG + Wordnik wordlist: move engine — 2x faster than DAWG for move generation; handles board expansion
- OpenCV 4.13.0.92 + Pillow 12.1.1: image preprocessing — OpenCV finds tile boundaries, Claude reads content
- aiosqlite 0.22.1: state persistence — non-blocking SQLite within discord.py's event loop
- numpy 2.x: board representation — typed 2D array for 27x19+ grid operations

### Expected Features

Board state extraction is the foundational critical path: every other feature depends on reliably parsing a screenshot into a structured board representation. The GADDAG engine, slash commands, and scoring logic all depend on this working correctly first. Wild vs. Classic scoring modes diverge at the score-calculation level and must be designed in from the start — they cannot be retrofitted cleanly later.

**Must have (table stakes):**
- Board state extraction via AI vision — without this, nothing works; highest-risk item
- Tile rack extraction from screenshot — required alongside board extraction
- GADDAG word finder with Wordnik dictionary — core move-generation engine
- Classic mode scoring calculation — standard Scrabble behavior, required for advisor mode
- `/analyze` slash command accepting screenshot attachment — standard Discord interaction pattern
- Top 3 move suggestions with score and placement — minimum useful advisor output
- Configurable difficulty % — primary differentiator; interpolate from worst to best valid move

**Should have (competitive):**
- Wild mode scoring — permanent multiplier tracking; many players use this mode
- Move explanation with score breakdown — teaches strategy, low implementation cost
- Bingo detection flag — marks 7-tile plays, high user delight for low effort
- In-session board state memory — avoids full re-parse on each turn within a game

**Defer (v2+):**
- Autonomous play mode — highest complexity feature; Playwright + browser automation; build only after advisor is solid
- Leave value / equity scoring — strategic tile retention; significantly more complex than raw score maximization
- Monte Carlo lookahead — state-of-the-art Scrabble AI; overkill until autonomous mode is working

### Architecture Approach

The architecture is strictly layered with clean boundaries. Discord Cogs are thin event translators only — no game logic lives in Cog methods. The engine package (board model, dictionary, move generator, scorer, difficulty filter) is pure Python with no I/O and no discord.py imports, making it fully unit-testable without a live bot. The vision package is isolated behind a single async function that accepts screenshot bytes and returns a `BoardState` dataclass — swapping VLM providers requires only changing `vision/extractor.py`. The automation package (Playwright lifecycle) is separate from the engine, so autonomous mode can be disabled without touching core logic. `BoardState` is an immutable frozen dataclass that serves as the single contract between all components.

**Major components:**
1. Discord Cog (bot/cogs/) — receives slash commands and image attachments; dispatches to pipelines; formats output
2. Game Session Controller (bot/session.py) — owns mode state, difficulty setting; routes advisor vs. autonomous
3. Vision Pipeline (vision/) — screenshot bytes → BoardState via Claude Vision API; includes validation
4. Word Engine (engine/) — BoardState → ranked Move list; pure CPU, zero I/O; GADDAG + scorer + difficulty filter
5. Browser Automation (automation/) — persistent Playwright Chromium context; canvas screenshot capture; tile placement clicks
6. Persistent Session Store (aiosqlite) — per-user difficulty settings, game history, board state cache with TTL

### Critical Pitfalls

1. **Playwright sync API inside discord.py** — use `playwright.async_api` exclusively throughout the project; `sync_playwright()` raises `RuntimeError: This event loop is already running` inside discord.py's asyncio loop; this is the most commonly hit integration bug
2. **Canvas screenshot blank in headless Chromium** — Playwright has a documented bug (issue #19225) where canvas elements render blank in headless mode; validate canvas capture in headed mode first; fall back to JavaScript `canvas.toDataURL()` injection if needed
3. **Vision LLM hallucination on ambiguous tiles** — VLMs hallucinate tile identities (I/l/1, O/0, W/M); add post-extraction validation (rack length 1-7, letters in A-Z set, grid dimensions within bounds); never propagate unvalidated VLM output to the move engine
4. **Board state drift from accumulated errors** — do NOT accumulate delta updates across turns; always re-extract the full board each turn as the authoritative state; each turn's read supersedes the previous
5. **TOS selfbot violation** — Discord's Activity player account must be a dedicated throwaway account, never a personal account; keep API bot and browser automation accounts strictly separate; use human-paced click timing

---

## Implications for Roadmap

Based on research, the architecture's strict build-order dependency chain (board model → engine → vision → bot integration → automation) maps directly onto roadmap phases. Each phase must be complete and validated before the next begins — this is not a project where phases can overlap significantly.

### Phase 1: Project Foundation and Board Model
**Rationale:** The `BoardState` and `Cell` dataclasses are the contract that every other component depends on. Establishing the data model, project structure, and development tooling first prevents costly interface changes later. Zero external dependencies.
**Delivers:** Project scaffold, `engine/board.py` dataclasses, `config.py`, `.env` setup, uv lockfile, test infrastructure
**Addresses:** Slash command interface foundation (discord.py Cog skeleton), scoring mode design (Wild vs. Classic must be in data model from the start)
**Avoids:** Anti-pattern of putting game logic in Discord Cogs; hardcoding board dimensions (design for 27x19+ expandable from day one)

### Phase 2: Word Engine (Dictionary + Move Generation + Scoring)
**Rationale:** The engine is pure Python with no I/O dependencies — it can be built and exhaustively tested without a Discord bot, browser, or vision API. This is the highest-complexity algorithmic component and the safest to build in isolation. All downstream phases depend on it being correct.
**Delivers:** GADDAG loaded from Wordnik wordlist, anchor-based move generator, Classic and Wild mode scorer, percentile difficulty filter
**Addresses:** Valid move generation (table stakes), highest-scoring move recommendation, Classic + Wild scoring, configurable difficulty %, bingo detection
**Avoids:** Linear word search in Python list (O(n) unusable at 170k+ words); accumulating board state as deltas; building Trie instead of DAWG/GADDAG; using Wordnik list as a Python list for membership checks
**Research flag:** Standard patterns from Appel-Jacobsen 1988 and Gordon 1994 — well-documented; skip phase-level research; unit-test difficulty scaling across 0/50/100% to verify measurable score differences

### Phase 3: Vision Pipeline (Board Reading)
**Rationale:** The vision pipeline is the highest-risk component in the project. It must be validated against real Letter League screenshots with ground-truth boards before connecting to the word engine. A hallucinating board reader will silently produce wrong moves with no error signal. Board-reading accuracy gates everything downstream.
**Delivers:** `vision/extractor.py` with Claude Vision API integration, structured JSON prompt/schema, BoardState validation layer, Pillow/OpenCV preprocessing (crop to board region, enhance contrast)
**Addresses:** Board state extraction (critical path table stake), tile rack extraction, multiplier square detection, error handling with actionable messages
**Avoids:** Sending full 1920x1080 screenshots (inflates tokens, worsens accuracy — crop first); treating VLM output as ground truth without validation; missing multiplier square detection; confusing rack tiles with board tiles
**Research flag:** Needs validation testing — measure per-tile error rate on 20+ ground-truth screenshots before proceeding; this phase has the highest uncertainty in the project

### Phase 4: Discord Advisor Mode Integration
**Rationale:** This is the first end-to-end path and the MVP milestone. Vision pipeline + word engine + Discord slash command wired together. Advisor mode has zero TOS risk and delivers core user value independently of autonomous mode.
**Delivers:** `/analyze` slash command, screenshot attachment ingestion, top-N move response formatting, in-Discord error messages, interaction deferral pattern
**Addresses:** All P1 features from FEATURES.md; `/analyze` slash command; human-readable response formatting; Wild/Classic mode selection per call
**Avoids:** 3-second interaction token timeout (always `defer()` immediately before async work); calling vision API synchronously in handler (use async client); sending raw unvalidated VLM output to users
**Research flag:** Standard discord.py patterns — well-documented; no phase research needed

### Phase 5: Enhanced Advisor Features (v1.x)
**Rationale:** Once advisor mode is validated and users are engaged, add the differentiating polish features. These are low implementation cost against an already-working advisor foundation.
**Delivers:** Move explanation with score breakdown, bingo detection flag, in-session board state memory (per channel/user with TTL), Wild mode if not completed in Phase 3
**Addresses:** All P2 features from FEATURES.md; top-N alternatives; multi-turn session context
**Avoids:** Stateful board accumulation across sessions (use TTL-based cache, not permanent state); leave value / equity scoring complexity (defer to v2)
**Research flag:** Standard patterns; skip phase research

### Phase 6: Browser Automation Foundation
**Rationale:** Autonomous mode requires three separate validated capabilities — canvas screenshot capture, iframe interaction, and persistent session management — before any game logic is layered on. The Playwright canvas bug in headless mode is a critical unknown that must be resolved before building the game loop. Separate from the game logic to allow targeted debugging.
**Delivers:** `automation/browser.py` persistent Chromium context, canvas screenshot validation (headed and headless), `automation/navigator.py` Discord Activity navigation, iframe access via `frame_locator()`
**Addresses:** Browser automation infrastructure, persistent session (no re-auth per run), `.gitignore` for `browser_state/`
**Avoids:** Playwright sync API (use async API throughout); re-launching browser every turn (launch once, keep open); iframe cross-origin blocking (use `frame_locator()` by URL pattern, not position); browser_state committed to git
**Research flag:** Needs exploratory spiking — canvas screenshot bug resolution is unknown until tested against live Letter League; iframe URL pattern for frame_locator requires live investigation

### Phase 7: Autonomous Play Mode
**Rationale:** Highest-complexity feature. Requires all prior phases working. The TOS risk is highest here — design documentation and account separation must precede implementation. Layered on top of working advisor mode (vision + engine) with browser automation (Phase 6) completing the loop.
**Delivers:** `/autoplay` and `/stop` slash commands, `automation/placer.py` tile placement click sequences, game loop with turn detection, end-of-game cleanup
**Addresses:** P3 autonomous play feature; difficulty % scaling in autonomous context
**Avoids:** Selfbot account ban (use dedicated throwaway account, human-paced delays, document TOS risk prominently); board state drift in long game loops (re-read full board each turn); hardcoded board coordinates (canvas coordinates relative to element bounding box, not viewport)
**Research flag:** Highest-risk phase — needs live testing of click coordinate mapping for tile rack and board placement; turn-detection mechanism requires investigation of Letter League's UI signals; plan for the possibility that canvas interaction fails and a fallback approach is needed

### Phase Ordering Rationale

- **Engine before vision:** The word engine is pure Python and testable in isolation. Building it first means the most critical and complex algorithmic component has verified correctness before any visual data is piped through it.
- **Vision before Discord:** Board reading is the project's highest-risk item. Validating it against real screenshots before wiring up Discord commands prevents building on an unreliable foundation.
- **Advisor before autonomous:** All research sources agree on this order. Autonomous mode is advisor mode plus browser automation. Advisory mode is the correct MVP milestone and has zero TOS risk.
- **Automation foundation before game loop:** The three Playwright unknowns (canvas in headless, iframe access, persistent session) must be resolved as isolated engineering problems before game logic is layered on top.

### Research Flags

Phases likely needing deeper research or spiking during planning:
- **Phase 3 (Vision Pipeline):** Accuracy of Claude Vision on Letter League's specific tile font and color scheme is unknown until tested. Multiplier square visual differentiation and rack vs. board tile separation need empirical validation. Plan for iteration.
- **Phase 6 (Browser Automation Foundation):** Playwright canvas screenshot bug resolution on the specific Letter League canvas element is unknown. The iframe URL pattern for `frame_locator()` requires live investigation. This phase should begin with a time-boxed spike.
- **Phase 7 (Autonomous Play):** Tile placement coordinate mapping, turn-detection UI signals, and the overall reliability of headless click automation all require live testing against a real game. Budget for significant iteration.

Phases with standard patterns (skip phase-level research):
- **Phase 1 (Foundation):** discord.py project structure is well-documented; uv tooling is standard.
- **Phase 2 (Word Engine):** GADDAG and Appel-Jacobsen algorithms are fully documented in published papers with Python reference implementations.
- **Phase 4 (Advisor Integration):** discord.py slash commands, attachment handling, and interaction deferral are standard patterns.
- **Phase 5 (Enhanced Advisor):** Additions to working advisor; no new unknown integrations.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Core stack choices verified against PyPI; version numbers confirmed; compatibility matrix documented; only MEDIUM on minor library versions (loguru, OpenCV exact version) |
| Features | MEDIUM | Table stakes and differentiators are clear; Wild vs. Classic scoring details need in-game verification; Wordnik dictionary coverage vs. Letter League's actual wordlist is an unverified assumption |
| Architecture | MEDIUM-HIGH | Core architecture patterns (GADDAG, thin Cog, BoardState contract) are well-established in published Scrabble AI literature; Letter League-specific visual parsing is uncharted territory with no public prior art |
| Pitfalls | MEDIUM | Playwright canvas bug is documented (GitHub issue #19225) but resolution for this specific use case needs empirical testing; TOS risk is confirmed by Discord policy but enforcement behavior is uncertain |

**Overall confidence:** MEDIUM

### Gaps to Address

- **Wordnik vs. Letter League dictionary coverage:** Wordnik is used as a proxy for Letter League's actual dictionary. The game may reject valid Wordnik words or accept words not in Wordnik. Mitigation: build a supplementary observed-words list during testing; label advisor suggestions as "estimated valid."
- **Canvas screenshot in headless mode:** Playwright's canvas rendering in headless Chromium is a documented bug but the fix reliability for this specific application is untested. Phase 6 must begin with a time-boxed spike to validate before committing to the autonomous mode architecture.
- **Wild mode scoring exact rules:** Research confirms Wild mode uses permanent multipliers (bonus bonds to the letter tile permanently), but the exact calculation for cross-words in Wild mode requires in-game verification. Do not ship Wild mode scoring without empirical testing against known game outcomes.
- **Letter League board expansion trigger:** The board is documented as expandable beyond 27x19, but the exact conditions that trigger expansion are not documented in public sources. The vision pipeline must detect grid dimensions dynamically rather than assuming a fixed size.
- **iframe URL pattern for frame_locator:** The exact URL or attribute pattern to identify Letter League's iframe inside Discord's web client is unknown without live testing. Phase 6 requires live investigation before the automation architecture is finalized.
- **Turn detection signal:** The autonomous mode game loop needs a reliable signal for "it is now the bot's turn." The specific UI element or state change that indicates turn handoff in Letter League requires in-game observation.

---

## Sources

### Primary (HIGH confidence)
- PyPI: discord.py 2.7.1, playwright 1.58.0, anthropic 0.86.0, aiosqlite 0.22.1, python-dotenv 1.2.2, pytest-asyncio 1.3.0 — version verification
- Playwright Python official docs — async API, persistent context, ProactorEventLoop requirement
- Gordon 1994 "A Faster Scrabble Move Generation Algorithm" — GADDAG algorithm (https://ericsink.com/downloads/faster-scrabble-gordon.pdf)
- Appel and Jacobsen 1988 "The World's Fastest Scrabble Program" — anchor/cross-check move generation (https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf)
- Wordnik wordlist GitHub — format, word count (~180k words) (https://github.com/wordnik/wordlist)
- Discord TOS on self-bots — explicit prohibition confirmed (https://support.discord.com/hc/en-us/articles/115002192352)
- Playwright GitHub issue #19225 — canvas elements missing from screenshots (documented bug)
- discord.py official docs — Cogs, app_commands, interaction deferral

### Secondary (MEDIUM confidence)
- Letter League Discord Fandom Wiki — board dimensions (27x19 expandable), Wild vs. Classic scoring modes
- TheLinuxCode Letter League guide — 7-tile rack confirmed, board expansion mechanics
- Aydin Schwartz "Coding the World's Fastest Scrabble Program in Python" (Medium) — Python GADDAG implementation patterns
- GitHub vike256/Wordbot — CLI-only reference implementation; confirms scope gap
- GitHub 23f3000839/Letter_League_AI — Chrome extension approach; confirms no existing full Discord bot solution
- OCR comparison benchmarks — Claude Sonnet leads for digital screenshots (multiple search sources agree)

### Tertiary (LOW confidence)
- Letter League FAQ official docs — 403 error at research time; board/scoring details sourced from secondary sources
- Playwright iframe handling for Discord Activities — specific URL patterns and CSP compliance details require live testing

---
*Research completed: 2026-03-23*
*Ready for roadmap: yes*
