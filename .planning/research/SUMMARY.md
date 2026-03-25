# Project Research Summary

**Project:** Letter League Bot v1.2 — Browser Automation + Autonomous Play
**Domain:** Discord bot with Playwright browser automation, Canvas vision pipeline, and word-game AI
**Researched:** 2026-03-24
**Confidence:** MEDIUM (browser automation patterns: HIGH; Discord Activity iframe specifics and turn-detection signals: LOW — require live inspection)

## Executive Summary

Letter League Bot v1.2 adds autonomous game play to the already-shipped advisor bot (v1.1). The bot must drive a real Discord user account through Chromium to join a voice channel, open the Letter League Activity, read the canvas board via the existing vision pipeline, select a move with the existing engine, and click tiles to play — all without human intervention and without violating discord.py's asyncio event loop ownership. The v1.0 GADDAG engine, v1.1 vision pipeline, and existing Discord bot are fully reusable; all new work lives in a new `src/browser/` package. This is a narrow integration milestone, not a ground-up build.

The recommended approach is a single-process architecture where `patchright` (a drop-in Playwright fork with CDP fingerprint leak patches) shares discord.py's asyncio event loop natively. A `BrowserManager` owns one `launch_persistent_context` for the bot's lifetime, a `GameLoop` using `discord.ext.tasks` polls the canvas every 4 seconds, and `TilePlacer` converts engine `Move` objects to pixel clicks via runtime canvas bounding-box fractions. The critical discipline: Playwright objects never cross thread boundaries; only pure Python data (bytes, dataclasses) goes into `asyncio.to_thread()` for the CPU-bound engine calls.

The top risk is that three foundational decisions depend on live Discord inspection that cannot be completed before implementation begins: the exact Activity iframe selector, the visual signal that marks "my turn," and the fractional pixel constants for rack and board cell positions. These three unknowns are discovery spikes that must be time-boxed and gate subsequent work. A secondary structural risk is Discord's Terms of Service: automating a user account is explicitly prohibited and enforced. The project already accounts for this by requiring a dedicated throwaway account separate from the discord.py bot token; that constraint must be documented and enforced at setup.

## Key Findings

### Recommended Stack

The v1.2 addition requires only one new package: `patchright==1.58.2` (drop-in Playwright replacement with CDP fingerprint leak patches). `numpy` is already a transitive dependency of `opencv-python` and requires no install. Everything else — `discord.py 2.7.1`, `anthropic 0.86.0`, `opencv-python 4.13.0.92`, `aiosqlite 0.22.1`, `loguru 0.7.3` — is already shipped in v1.1. See `STACK.md` for the full version table.

**Core technologies (v1.2 additions only):**
- `patchright 1.58.2`: Browser automation — patches `navigator.webdriver`, suppresses HeadlessChrome UA string, eliminates CDP fingerprint leaks Discord uses for bot detection. Drop-in swap: one import change from `playwright.async_api`. Revert in one line if compatibility issues arise.
- `numpy >= 1.24` (transitive, no install): Byte-to-ndarray conversion for canvas blank detection — already present as an `opencv-python` dependency.
- `claude-sonnet-4-6` (unchanged from v1.1): Vision model for board extraction. Best cost/speed balance. Do not downgrade to Haiku without accuracy validation. Haiku 3 (`claude-3-haiku-20240307`) retires April 19, 2026 — do not use.

**Installation:**
```bash
pip install "patchright==1.58.2"
python -m patchright install chromium
```

### Expected Features

The autonomous mode must complete a full turn end-to-end without human intervention. Every P1 item is a hard dependency; none can be deferred.

**Must have (P1 — required for one complete autonomous turn):**
- Persistent Playwright session (`launch_persistent_context` with `user_data_dir`) — Discord login must survive bot restarts
- Activity iframe load and ready detection — selector must be confirmed via live DevTools inspection before any automation code is written
- Non-blank canvas screenshot capture — blank-frame detection gates the vision call; avoids wasted API credits
- Vision pipeline wire-up — pass `canvas.screenshot()` bytes directly to existing `extract_board_state()`; zero new vision code
- Pixel coordinate map — compute board cell positions from canvas bounding box at game start; gates all tile placement
- Turn detection — visual polling for "my turn" signal; must be discovered empirically from live gameplay
- Tile placement — rack click + board cell click per letter in the selected word
- Play confirmation click
- Asyncio game loop running as `asyncio.create_task()` concurrent with discord.py's event loop

**Should have (P2 — sustained multi-turn play without intervention):**
- Graceful reconnect on session drop or Activity disconnect
- Tile swap fallback when no valid moves exist
- Human-like timing jitter (random 1-3 second delays between actions)
- Discord status updates (what word was played and for what score)

**Defer (v2+):**
- Multi-game / multi-session (requires multiple Discord accounts; dramatically higher complexity)
- Adaptive ML-based turn detection (defer until threshold polling proves insufficient)
- Tile swap strategy integration with difficulty engine

### Architecture Approach

The v1.2 architecture is a single asyncio event loop shared by discord.py and `async_playwright`. No separate threads or processes for Playwright. Five new modules are added under `src/browser/`. `BrowserManager` owns the Playwright lifecycle. `DiscordNavigator` navigates to the voice channel and locates the Activity iframe. `GameLoop` runs as a `@tasks.loop(seconds=4.0)`, polling for turn changes and executing the full play pipeline. `TilePlacer` translates `Move` objects to pixel clicks. `AutonomousCog` exposes `/autoplay start|stop|status` commands. `src/vision/`, `src/engine/`, and `src/difficulty/` are completely unchanged. See `ARCHITECTURE.md` for the full system diagram and per-turn data flow (screenshot → vision → engine → placement: total 5-16 seconds, well within any turn timer).

**Major components:**
1. `BrowserManager` (`src/browser/manager.py`) — owns `async_playwright().start()` and `launch_persistent_context`; started in `setup_hook`, torn down in `close()`; `user_data_dir` must be gitignored
2. `DiscordNavigator` (`src/browser/navigator.py`) — stateless; takes `BrowserContext`, navigates to `discord.com/channels/{guild}/{channel}`, returns `(Page, Frame)` for the Letter League iframe
3. `GameLoop` (`src/browser/game_loop.py`) — `@tasks.loop(seconds=4)` polling; screenshot hash comparison for change detection; calls `_is_my_turn()` then `extract_board_state()` → `asyncio.to_thread(find_all_moves)` → `asyncio.to_thread(select_move)` → `place_move()`
4. `TilePlacer` (`src/browser/tile_placer.py`) — runtime `canvas.bounding_box()` + fractional offset constants (calibrated from live measurements) → `frame.mouse.click()` for each tile and confirmation
5. `AutonomousCog` (`src/bot/autonomous_cog.py`) — `/autoplay start|stop|status` slash commands; owns one `GameLoop` instance per active session

**Key invariant:** Playwright objects (`Page`, `Frame`, `BrowserContext`) never enter `asyncio.to_thread()`. Only pure data (bytes, Move dataclasses) crosses the thread boundary.

### Critical Pitfalls

1. **Playwright sync API inside discord.py** — causes `RuntimeError: This event loop is already running` and freezes the entire bot. Use `playwright.async_api` exclusively. Verify at the start of Phase 1 that a discord.py slash command can trigger a Playwright action without blocking concurrent commands.

2. **Canvas screenshot blank in headless Chromium** — canvas compositing does not flush before the screenshot in headless mode; screenshot returns solid black or white. Always use `headless=False`. On production Linux, use Xvfb. If still unreliable, fall back to `frame.evaluate("canvas.toDataURL('image/png')")` as the primary capture path (bypasses compositing entirely).

3. **Discord Activity iframe selector is undocumented** — Discord's React SPA uses dynamic class names; the exact iframe selector is not public. Run a headed DevTools inspection spike before writing any automation code. Expected pattern: `[src*="discordsays.com"]`. Gate all subsequent automation on the confirmed selector.

4. **Canvas click coordinates use wrong space** — grid-only pixel math misses the iframe origin and canvas bounding box; clicks land consistently offset. Use `canvas_element.click(position={"x": offset_x, "y": offset_y})` for bounding-box-relative coordinates, or get `canvas.bounding_box()` at runtime. Never hardcode absolute pixel coordinates.

5. **iframe frame reference becomes stale after Discord reconnect** — cached `Frame` objects detach when Discord's SPA reloads the Activity iframe, causing `FrameDetachedError`. Always re-derive from `page.frame_locator(selector)` at the start of each action sequence; wrap in retry-with-reacquisition on detach.

6. **Turn detection relies on an unverified UI signal** — no API exists to determine whose turn it is. The visual signal must be discovered empirically. Do not write detection code until the signal is confirmed via live gameplay observation (time-box: 4 hours). Fall back to screenshot-diff polling if no reliable DOM signal is found.

7. **Self-bot TOS risk** — Discord permanently bans accounts that automate user interactions. Use a dedicated throwaway account. Never use a personal account. Document this risk explicitly before implementation begins. The discord.py bot token and the Playwright user account must be separate accounts.

## Implications for Roadmap

Based on the dependency chain in `FEATURES.md` and the pitfall-to-phase mapping in `PITFALLS.md`, a 5-phase build order is recommended. Each phase has a concrete test gate that must pass before the next begins. The architecture's `ARCHITECTURE.md` "Suggested Build Order" sections align exactly with this structure.

### Phase 1: Browser Foundation + Discovery Spikes

**Rationale:** All subsequent phases depend on three unknowns that require live Discord inspection: the iframe selector, the canvas screenshot method reliability, and session validation behavior. These must be resolved as explicit spike deliverables before any game logic is written. This phase also proves that Playwright does not block discord.py's event loop — the most common integration mistake in this domain.

**Delivers:** `BrowserManager` wired into `bot.setup_hook`/`bot.close()`; confirmed iframe selector string (documented with DevTools screenshot); proof that `canvas.screenshot()` captures non-blank board content in headed mode; session expiry detection at startup (detects `discord.com/login` redirect and notifies operator); `--disable-blink-features=AutomationControlled` validated against Discord login without CAPTCHA; frame re-acquisition retry logic proven against a simulated Activity reload.

**Addresses (from FEATURES.md):** Persistent browser session, headless-detection bypass, Activity iframe load and ready detection.

**Avoids (from PITFALLS.md):** Pitfalls 1 (sync API), 2 (blank canvas), 3 (undocumented iframe selector), 4 (wrong coordinate space), 5 (stale frame reference), 7 (bot detection).

**Research flag:** HIGH — iframe selector, canvas blank behavior in headed+virtual-display mode, and bot-detection bypass effectiveness all require live validation. Cannot be pre-researched further from documentation alone.

---

### Phase 2: Canvas Screenshot through Vision Pipeline Wire-Up

**Rationale:** Validates format compatibility between `canvas.screenshot()` PNG bytes and the existing `preprocess_screenshot()` + Claude Vision API before adding game loop complexity. Cheap to validate now; expensive to discover a format mismatch after the full loop is built.

**Delivers:** End-to-end proof that `canvas.screenshot()` bytes flow through `extract_board_state(img_bytes, mode)` and return a correct `(Board, rack)` tuple. Zero new vision code written; pure wire-up validation.

**Addresses (from FEATURES.md):** Vision pipeline wire-up, canvas screenshot capture (non-blank).

**Avoids (from PITFALLS.md):** Pitfall 9 (board state drift) — establishes that a full re-read each turn produces correct output before the game loop is built around it.

**Research flag:** LOW — the interface (`bytes` in, `(Board, rack)` out) is defined and validated in v1.1. This is integration confirmation, not new research.

---

### Phase 3: Turn Detection

**Rationale:** Turn detection is the highest-uncertainty feature in the milestone. It must be validated with recorded screenshots before tile placement is built, so that placement logic is not wired to a broken or incorrectly assumed detection strategy.

**Delivers:** `_is_my_turn(screenshot_bytes)` that correctly classifies at least 10 recorded game screenshots across both "my turn" and "not my turn" states. Turn-detection signal documented from live gameplay observation (2+ full games watched with DevTools open).

**Addresses (from FEATURES.md):** Turn detection (visual polling).

**Avoids (from PITFALLS.md):** Pitfall 6 (unverified turn signal) — observation spike is the first deliverable of this phase, not the last.

**Research flag:** HIGH — the turn-detection visual signal must be discovered by playing real games. Time-box the live observation spike at 4 hours. If no reliable DOM signal is found, commit to screenshot-diff polling as the primary strategy and document the limitation.

---

### Phase 4: TilePlacer and Coordinate Calibration

**Rationale:** Tile placement requires calibrated fractional constants that can only be measured from live game screenshots. Phases 1-3 provide the foundation; this phase completes the mechanical play capability.

**Delivers:** `place_move(frame, move, canvas_bbox)` placing a known word correctly on a live board. Fractional constants for rack tile positions and board grid cell positions calibrated from live measurements. Click validation: 5 known tile positions clicked and confirmed by correct game response (tile highlights in expected position).

**Addresses (from FEATURES.md):** Pixel coordinate map, tile placement (rack + board clicks), play confirmation.

**Avoids (from PITFALLS.md):** Pitfall 4 (wrong coordinate space) — uses `canvas.bounding_box()` + element-relative clicks, not absolute viewport coordinates. Never hardcodes pixel constants measured on one screen.

**Research flag:** MEDIUM — fractional constants in `ARCHITECTURE.md` (`RACK_Y_FRACTION = 0.92`, `CELL_WIDTH_FRACTION = 0.034`, etc.) are placeholders only. Actual values must be measured from live game screenshots and may differ significantly from the estimates.

---

### Phase 5: AutonomousCog + End-to-End Integration

**Rationale:** Pure integration glue. Fast to build once Phases 1-4 are solid. This phase wires `GameLoop` into `AutonomousCog` and runs a complete game session from turn detection through word confirmation.

**Delivers:** `/autoplay start|stop|status` slash commands; `GameLoop` running as `@tasks.loop(seconds=4)` concurrent with the discord.py event loop; at least one complete autonomous turn from board read through word placement and confirmation without human intervention. P2 features (graceful reconnect, swap fallback, timing jitter, status messages) added only after the core loop validates.

**Addresses (from FEATURES.md):** Asyncio game loop, graceful reconnect, tile swap fallback, human-like timing jitter, Discord status updates from autonomous mode.

**Avoids (from PITFALLS.md):** Pitfall 8 (stale frame reference) — tested explicitly by simulating an Activity reload mid-session during validation.

**Research flag:** LOW — integration patterns (`@tasks.loop`, `asyncio.create_task`, Cog structure) are well-documented. Primary risk is timing and coordination, not unknown APIs.

---

### Phase Ordering Rationale

- **Foundation spikes must precede game logic** because three critical unknowns (iframe selector, turn signal, pixel coordinates) block every downstream phase. Discovering these late causes rework on already-built game logic.
- **Vision wire-up (Phase 2) precedes turn detection (Phase 3)** because the game loop depends on both; validating vision compatibility first avoids compound debugging when the loop is built.
- **Turn detection (Phase 3) precedes tile placement (Phase 4)** because a correct turn signal is a precondition for correct tile placement — acting on the wrong turn corrupts the game state.
- **End-to-end integration (Phase 5) is last** because it is fast when all components are proven. Building integration before components are stable multiplies debugging surface area.

### Research Flags

Phases needing deeper research or live inspection during planning:
- **Phase 1:** Discord Activity iframe selector (confirmed only by live DevTools inspection); canvas screenshot reliability in headed+Xvfb mode; bot-detection bypass effectiveness against Discord. Cannot be resolved without a live Discord session.
- **Phase 3:** Turn-detection visual signal must be observed from 2+ real games. Do the observation spike before writing any polling code. Time-box at 4 hours.
- **Phase 4:** Tile click fractional constants must be measured from live game screenshots. ARCHITECTURE.md constants are placeholders only; budget for calibration iteration.

Phases with standard, well-documented patterns (skip deep research):
- **Phase 2:** Pure wire-up of existing interfaces; no new patterns.
- **Phase 5:** `discord.ext.tasks` + asyncio integration; well-documented in discord.py official docs; no novel patterns.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All packages verified on PyPI; versions confirmed; `patchright 1.58.2` drop-in swap verified; async Playwright + ProactorEventLoop on Python 3.10 confirmed against official docs and discord.py issue tracker |
| Features | MEDIUM | P1 feature set is clear and complete; turn-detection and pixel-coordinate features are HIGH complexity with LOW confidence in their specific implementation until live inspection confirms signals and measurements |
| Architecture | HIGH (event loop mechanics) / MEDIUM (iframe selectors, coordinate constants) | Playwright async sharing discord.py's event loop: HIGH confidence. Discord Activity DOM structure: MEDIUM — requires empirical discovery. Fractional coordinate constants: placeholder values only. |
| Pitfalls | MEDIUM-HIGH | Playwright async/canvas/iframe behaviors verified against official docs and GitHub issues (#19225, #33566, #3170, #2753, #462); Discord Activity iframe selectors and turn-detection signals are LOW confidence — require live inspection |

**Overall confidence:** MEDIUM

### Gaps to Address

- **Discord Activity iframe selector** — Pattern `[src*="discordsays.com"]` is inferred from Discord developer docs; the exact selector must be confirmed via live DevTools inspection before any frame automation is written. Gate Phase 1 completion on this deliverable.
- **Turn-detection visual signal** — Unknown until live games are observed. Phase 3 starts with an observation spike, not code. Time-box at 4 hours; commit to screenshot-diff fallback if no reliable DOM signal is found.
- **Tile placement fractional constants** — ARCHITECTURE.md values are educated guesses. Must be calibrated from live game screenshots during Phase 4. Budget for significant measurement iteration.
- **Canvas screenshot vs `canvas.toDataURL()` reliability** — The screenshot approach is preferred but may fail for cross-origin Activity iframes (SecurityError on `getImageData()`). The `toDataURL()` injection fallback must be tested and ready during Phase 1 spike.
- **Bot detection effectiveness** — Community sources confirm `--disable-blink-features=AutomationControlled` is necessary; `patchright` adds CDP leak patches. Effectiveness against Discord specifically is MEDIUM confidence. Phase 1 includes a live login test to validate before any game logic is built on it.
- **Board expansion coordinate drift** — Letter League's board can expand (27x19 baseline). When new rows or columns appear, all coordinate mappings shift. Phase 4 must detect dimension changes from vision output and recalculate before placing tiles.

## Sources

### Primary (HIGH confidence)
- [Playwright Python official docs](https://playwright.dev/python/docs) — async API, `launch_persistent_context`, `frame_locator`, screenshots, mouse clicks, auth, thread-safety
- [patchright PyPI](https://pypi.org/project/patchright/) — v1.58.2, drop-in Playwright replacement, CDP leak patches, Chromium-only, released 2026-03-07
- [discord.ext.tasks official docs](https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html) — `@tasks.loop`, `before_loop`, `after_loop`, lifecycle hooks
- [Playwright BrowserType API](https://playwright.dev/python/docs/api/class-browsertype) — `launch_persistent_context` parameters, `user_data_dir` semantics
- [discord.py issue #859](https://github.com/Rapptz/discord.py/issues/859) — ProactorEventLoop + asyncio compatibility confirmed fixed Python 3.7+
- [Discord Self-Bot TOS policy](https://support.discord.com/hc/en-us/articles/115002192352) — explicit prohibition; permanent ban enforcement confirmed
- [Playwright Python issue #462/#2053/#2705](https://github.com/microsoft/playwright-python/issues/462) — sync API inside asyncio loop: documented as most frequent Python Playwright integration mistake
- [Playwright GitHub issue #19225](https://github.com/microsoft/playwright/issues/19225) — canvas screenshot blank in headless; root cause and remediation strategies
- [Playwright GitHub issue #33566](https://github.com/microsoft/playwright/issues/33566) — headless Chromium timing change in v1.49 (November 2024)
- [Playwright Mouse API docs](https://playwright.dev/docs/api/class-mouse) — operates in main-frame CSS pixels relative to viewport top-left; coordinate implications for iframe-contained canvas

### Secondary (MEDIUM confidence)
- [Discord Activities developer docs](https://docs.discord.com/developers/activities/how-activities-work) — Activities use `*.discordsays.com` iframe; exact selector inferred, not confirmed
- [Playwright GitHub issue #3170](https://github.com/microsoft/playwright/issues/3170) — cross-origin iframe coordinate offset edge case
- [BrowserStack — Playwright bot detection](https://www.browserstack.com/guide/playwright-bot-detection) — headless fingerprint signals; headed mode mitigation
- [Playwright storageState guide — BrowserStack](https://www.browserstack.com/guide/playwright-storage-state) — token expiry causes silent auth failures
- [Castle.io — anti-detect frameworks](https://blog.castle.io/from-puppeteer-stealth-to-nodriver-how-anti-detect-frameworks-evolved-to-evade-bot-detection/) — `navigator.webdriver` detection; `--disable-blink-features=AutomationControlled` mitigation
- [Patchright vs Playwright — DEV Community](https://dev.to/claudeprime/patchright-vs-playwright-when-to-use-the-stealth-browser-fork-382a) — CDP leak patching details

### Tertiary (LOW confidence — requires live validation)
- Discord Activity iframe DOM structure — no public documentation; must inspect live Discord client in headed mode
- Letter League turn-detection visual signals — must observe from real gameplay; no prior art documented
- Tile placement fractional pixel constants — must measure from live game screenshots

---
*Research completed: 2026-03-24*
*Ready for roadmap: yes*
