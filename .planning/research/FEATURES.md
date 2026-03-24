# Feature Research

**Domain:** Discord word game AI bot — v1.1 Vision + Discord + Browser Automation
**Researched:** 2026-03-24
**Confidence:** HIGH (vision pipeline, Discord bot), MEDIUM (autonomous/Playwright — TOS risk)

---

## Scope Note

This document covers features for **v1.1 only**: Claude Vision board reading, Discord bot
advisor mode, and Playwright-based autonomous mode. The word engine (GADDAG, scoring,
move generation, difficulty) is already shipped in v1.0 and is treated as a dependency,
not a feature to build.

---

## Feature Landscape by Area

### Area 1: Vision Pipeline (Claude Vision API Board Reading)

#### Table Stakes

| Feature | Why Expected | Complexity | Engine Dependency |
|---------|--------------|------------|-------------------|
| Extract tile grid from screenshot | Core premise — everything else is useless without this | HIGH | None — pure vision work |
| Extract rack tiles from screenshot | Advisor needs current rack, not just board | MEDIUM | None — same API call |
| Output structured board state (dict/JSON) | Engine input format must match BoardState API | MEDIUM | Requires `BoardState` schema knowledge |
| Handle color-coded multiplier squares | DL/TL/DW/TW squares must be read, not guessed | HIGH | Feeds `Cell.multiplier` in existing board model |
| Validate extracted state before passing to engine | Bad parse = wrong moves; must detect failure gracefully | MEDIUM | Uses existing `BoardState` validation |
| Distinguish empty cells from occupied cells | 27x19 grid has many empty cells; false positives break move gen | MEDIUM | Critical for GADDAG anchor detection |

#### Differentiators

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Prompt-engineered JSON schema output | Forces Claude to output exactly what `BoardState` constructor expects, zero post-processing | LOW | Use explicit JSON schema in system prompt; proven pattern per official docs |
| Confidence flags in vision output | Claude can indicate partial-visibility cells; flag low-confidence reads for user review | LOW | Ask Claude to add a `confidence: low` field per cell where uncertain |
| Region cropping before API call | Crop to board area only before sending; reduces tokens, improves accuracy, cuts cost | LOW | Screenshot is ~1920x1080; board occupies maybe 60% — clip saves ~$0.002/call |
| Rack-first prompt ordering | Send rack region as Image 1, board as Image 2 — rack is smaller, anchor the parse | LOW | Official docs confirm image ordering matters for structured extraction |
| Two-shot parse with retry | If first parse fails validation, send again with "your previous output had error X, retry" | MEDIUM | Handles edge cases without human intervention |

#### Anti-Features

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Real-time continuous screen polling | "Watch the game and auto-update" | Requires persistent Playwright process in advisor mode — that IS autonomous mode | Use autonomous mode for always-on; advisor stays per-screenshot |
| OCR fallback (Tesseract etc.) | "What if Claude Vision fails?" | Letter League uses a canvas-rendered font; Tesseract requires training data for it; Claude Vision handles it natively | Claude Vision is the right tool; add retry logic instead of OCR fallback |
| Caching vision results per screenshot hash | "Avoid redundant API calls" | Screenshot changes every turn; hash cache hits will be rare; adds complexity for near-zero benefit | Vision call is ~$0.004/image at 1MP; not worth caching infrastructure |

---

### Area 2: Discord Bot Foundation + Advisor Mode

#### Table Stakes

| Feature | Why Expected | Complexity | Engine Dependency |
|---------|--------------|------------|-------------------|
| Discord bot process (discord.py, login, gateway) | Bot must exist before any interaction is possible | LOW | None |
| `/analyze` slash command with attachment parameter | Discord standard since 2021; `discord.Attachment` type annotation gives native file picker | LOW | None |
| Download attachment bytes in memory | `await attachment.read()` — no temp file needed | LOW | Feeds vision pipeline |
| Pass vision output to GameEngine | `GameEngine.set_board()` or equivalent; translate parsed JSON to existing API | MEDIUM | Requires `GameEngine` public API knowledge |
| Return top-N move recommendations | "EXAMPLE at H7 across = 34 pts" format; top 3 minimum | LOW | Uses `MoveGenerator` + `DifficultyEngine` already built |
| Error response for bad screenshot | "Couldn't parse board — try a cleaner screenshot" | LOW | None |
| `/setdifficulty` command | Bot must be configurable per-user or per-guild | LOW | Uses `DifficultyEngine(difficulty_pct)` |

#### Differentiators

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Ephemeral responses (only user sees bot reply) | Prevents board spoilers in shared channels | LOW | `interaction.response.send_message(..., ephemeral=True)` |
| Score breakdown in response | "Z=10 on DL(x2)=20 + cross APES=8 = total 42" teaches strategy | MEDIUM | Requires scoring engine to return component breakdown, not just total |
| Mode selector (Classic/Wild) parameter | One command works for both game modes | LOW | `/analyze mode:wild screenshot:[file]` |
| Top-3 alternatives shown | User may want second-best for strategic reasons | LOW | `MoveGenerator` already returns all moves; just take top-3 |
| Bingo callout | "BINGO! All 7 tiles played — word score doubled" | LOW | Flag 7-tile plays; already tracked in existing scoring engine |
| Per-user difficulty persistence | Remember user's preferred difficulty between sessions | MEDIUM | Simple key-value store (shelve or sqlite) keyed on `user_id` |

#### Anti-Features

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Prefix commands (`!analyze`) | "Simpler to type" | Discord deprecated prefix commands for bots requiring message intent; slash commands are the standard and have native attachment UI | Use slash commands exclusively |
| Embed board visualization | "Show the board state the bot read" | Rendering a 27x19 grid as a readable Discord embed requires significant image generation work; adds a whole new dependency | Return text description of best move; trust user can see the board themselves |
| Multi-server configuration dashboard | "Configure bot per server" | A web dashboard for bot config is a product in itself; massive complexity for marginal value | `/setdifficulty` and `/setmode` slash commands handle 100% of config |
| Global leaderboard | "Rank players by bot score" | Ranks "who used the bot most," not actual skill; adds database for zero gameplay value | Out of scope per PROJECT.md |

---

### Area 3: Autonomous Mode (Playwright Browser Automation)

#### Table Stakes

| Feature | Why Expected | Complexity | Engine Dependency |
|---------|--------------|------------|-------------------|
| Chromium launch with persistent session | Bot needs to be logged into Discord web; persistent context avoids re-login | MEDIUM | None |
| Navigate to Discord web and join voice channel | Bot must appear as a participant in the voice channel | HIGH | None |
| Open Letter League Activity in iframe | Activity loads as embedded iframe; bot must trigger launch | HIGH | None |
| Screenshot the Activity iframe region | Capture only the game board area, not full Discord UI | MEDIUM | Feeds vision pipeline |
| Parse screenshot via vision pipeline | Reuse Area 1 vision pipeline exactly | LOW | Requires Area 1 complete |
| Select and click tile placements | Click rack tile, then click board cell for each letter of the word | HIGH | Requires move output with absolute pixel coordinates |
| Wait for turn | Detect when it is the bot's turn before acting | HIGH | No API; must infer from visual state (e.g., rack tiles becoming clickable) |
| Handle word confirmation UI | After tile placement, Letter League likely has a "confirm" or "play" button | MEDIUM | Must be identified via DOM inspection or visual matching |

#### Differentiators

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Pixel coordinate mapping for board cells | Pre-compute the pixel position of each board cell relative to iframe origin | HIGH | Map once at game start by detecting grid lines; reuse for all moves |
| Visual turn detection (not polling) | Watch for DOM mutation or visual change indicating turn start rather than polling | MEDIUM | Playwright `page.wait_for_selector()` or `page.expect_event()` — avoids busy-wait |
| Human-like timing jitter | Add random 0.5-2s delays between actions to avoid bot detection | LOW | `asyncio.sleep(random.uniform(0.5, 2.0))` |
| Graceful disconnect and re-join | If connection drops, bot re-navigates and re-joins without manual restart | MEDIUM | Try/except around main loop with re-join logic |
| Tile swap detection | If no good move exists, choose swap vs. pass intelligently | MEDIUM | Use existing `DifficultyEngine` logic — if best score below threshold, swap |

#### Anti-Features

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Using a selfbot (user-account bot via discord.py) for Discord gateway | "Simpler than browser automation" | Discord explicitly bans selfbots — automated user accounts violate TOS and result in permanent bans (confirmed by Discord's own policy page) | Playwright controlling Discord web in Chromium is the correct path — it is human-like browsing, not API automation |
| Headless browser in production | "Saves resources" | Discord web detects headless Chromium fingerprints reliably; Activities may refuse to load | Use `headless=False` with a virtual display (Xvfb on Linux) or minimal window on desktop |
| Multiple autonomous sessions simultaneously | "Play multiple games at once" | Each session needs its own browser context and Discord account; dramatically multiplies TOS risk and complexity | Single session only for v1.1; document as hard constraint |
| Selenium instead of Playwright | "More familiar" | Playwright Python (1.40+) has superior async support, iframe frame_locator() API, and better screenshot clipping — directly needed for this project | Playwright is specified in PROJECT.md; stick to it |

---

## Feature Dependencies

```
[v1.0 Engine: GameEngine, MoveGenerator, DifficultyEngine, Scorer]
    (already built — treat as library)

[Area 1: Vision Pipeline]
    └──requires──> [Discord attachment download OR Playwright iframe screenshot]
    └──produces──> [BoardState JSON for GameEngine]
    └──feeds──> [Area 2: Advisor Mode]
    └──feeds──> [Area 3: Autonomous Mode]

[Area 2: Advisor Mode]
    └──requires──> [Discord bot process (gateway, login)]
    └──requires──> [/analyze slash command]
    └──requires──> [Area 1: Vision Pipeline]
    └──requires──> [v1.0 Engine]
    └──produces──> [Move recommendation embed to user]

[Area 3: Autonomous Mode]
    └──requires──> [Playwright Chromium session]
    └──requires──> [Area 1: Vision Pipeline]  ← reuses exactly
    └──requires──> [v1.0 Engine]
    └──requires──> [Pixel coordinate map of board]
    └──enhances──> [Area 2: Advisor Mode]  ← shares vision pipeline
    └──conflicts──> [Selfbot/user-account gateway automation]

[Per-user difficulty persistence]
    └──requires──> [Discord bot process]
    └──enhances──> [Area 2 + Area 3]

[Score breakdown in response]
    └──requires──> [v1.0 Scorer returning component data, not just total]
    └──enhances──> [Area 2: Advisor Mode response quality]
```

### Dependency Notes

- **Vision pipeline is the shared critical path.** Both advisor and autonomous mode feed through the same Area 1 code. Build and validate vision before touching Area 2 or 3.
- **Advisor mode must precede autonomous mode.** The move-generation and vision pipeline must be proven reliable in the lower-stakes advisor context before trusting them to click tiles autonomously.
- **Pixel coordinate mapping is the hardest autonomous-mode problem.** The game board is a canvas element inside an iframe; there is no DOM structure to query for cell positions. Must derive coordinates from visual grid detection or hardcoded offsets relative to detected board origin.
- **Score breakdown requires engine changes.** The existing `Scorer` returns a total score. To show per-component breakdown in Discord responses, it must return a breakdown dict. This is a v1.0 engine touch that must be planned carefully.
- **Selfbot approach is a hard blocker.** Discord's TOS explicitly prohibits automating user accounts via the gateway API. Playwright controlling a browser is the sanctioned path — it mimics human interaction.

---

## MVP Definition

### Launch With (v1.1)

Minimum for this milestone to be considered complete.

- [ ] **Vision pipeline (Area 1 core)** — parse board grid + rack from screenshot, output structured JSON; validate output before passing to engine. This is the single highest-risk item.
- [ ] **Discord bot process** — discord.py bot with proper token auth, guild registration, slash command tree sync.
- [ ] **`/analyze` slash command** — accepts `discord.Attachment`, downloads bytes in memory, runs vision pipeline, runs move gen, returns top-3 moves. Ephemeral response.
- [ ] **`/setdifficulty` command** — sets difficulty for the calling user; persists for session.
- [ ] **Mode parameter (Classic/Wild)** — slash command parameter, not a separate command.
- [ ] **Error handling** — actionable messages for bad screenshots, API failures, no valid moves.

### Add After Advisor Validation (v1.1.x)

Once advisor mode is working and being used.

- [ ] **Score breakdown in response** — requires touching Scorer to return component data.
- [ ] **Per-user difficulty persistence** — sqlite or shelve; simple key-value on user_id.
- [ ] **Retry on vision parse failure** — two-shot parse with error feedback to Claude.
- [ ] **Bingo callout** — trivial; flag 7-tile moves in response.

### Future (v2 — Autonomous Mode)

Defer until advisor is proven reliable over real game sessions.

- [ ] **Playwright Chromium session** — persistent Discord web login, voice channel join.
- [ ] **Activity iframe interaction** — screenshot, parse, act.
- [ ] **Pixel coordinate map** — derive board cell coordinates from visual grid detection.
- [ ] **Turn detection** — wait for visual cue that it is bot's turn.
- [ ] **Tile placement clicks** — select rack tile, click board cells, confirm play.

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Vision pipeline — grid + rack extraction | HIGH | HIGH | P1 |
| Discord bot process (gateway, auth) | HIGH | LOW | P1 |
| `/analyze` slash command with attachment | HIGH | LOW | P1 |
| BoardState JSON → GameEngine bridge | HIGH | MEDIUM | P1 |
| Top-3 move recommendations in response | HIGH | LOW | P1 |
| Error handling for bad screenshots | HIGH | LOW | P1 |
| `/setdifficulty` + Classic/Wild mode param | MEDIUM | LOW | P1 |
| Ephemeral responses | MEDIUM | LOW | P1 |
| Score breakdown per component | MEDIUM | MEDIUM | P2 |
| Per-user difficulty persistence | MEDIUM | LOW | P2 |
| Vision retry on parse failure | MEDIUM | LOW | P2 |
| Bingo callout | LOW | LOW | P2 |
| Region crop before vision API call | MEDIUM | LOW | P2 |
| Playwright Chromium session | HIGH | HIGH | P3 |
| Activity iframe screenshot + parse | HIGH | HIGH | P3 |
| Board pixel coordinate mapping | HIGH | HIGH | P3 |
| Turn detection (visual) | HIGH | HIGH | P3 |
| Tile placement clicks | HIGH | HIGH | P3 |

**Priority key:**
- P1: Must have for v1.1 launch (advisor mode complete)
- P2: Add after advisor is validated
- P3: Autonomous mode — v2

---

## Complexity Assessment by Area

| Area | Overall Complexity | Highest Risk Item | Notes |
|------|-------------------|-------------------|-------|
| Vision Pipeline | HIGH | Multiplier square color detection | Canvas-rendered UI; colors may be subtle; test with real screenshots early |
| Discord Bot | LOW | Slash command attachment flow | Well-documented, discord.py 2.5+ has native attachment type |
| Vision→Engine Bridge | MEDIUM | BoardState schema mapping | Requires knowing exact GameEngine constructor; touch existing code |
| Autonomous Mode | VERY HIGH | Pixel coordinate mapping + turn detection | No DOM structure; pure visual; highly brittle to UI changes |

---

## Sources

- [Claude Vision API — Official Docs](https://platform.claude.com/docs/en/build-with-claude/vision) — Image format requirements (JPEG/PNG/GIF/WebP), 5MB limit, base64/URL/file_id patterns, structured extraction best practices. HIGH confidence.
- [Discord.py — Slash Commands Masterclass](https://fallendeity.github.io/discord.py-masterclass/slash-commands/) — `discord.Attachment` type annotation for slash commands, `attachment.read()` for in-memory bytes. HIGH confidence.
- [Discord.py 2.5.0 changelog (March 2025)](https://discordpy.readthedocs.io/en/stable/) — Enhanced attachment properties; 2.6.0 (August 2025) added attachment titles/descriptions. MEDIUM confidence (search-sourced).
- [Discord Automated User Accounts (Self-Bots) — Official Policy](https://support.discord.com/hc/en-us/articles/115002192352-Automated-User-Accounts-Self-Bots) — Explicit ban on selfbots; permanent account termination. HIGH confidence.
- [Discord Activities — How Activities Work](https://docs.discord.com/developers/activities/how-activities-work) — iframe + postMessage architecture, OAuth scope requirement, no programmatic bypass of auth handshake. HIGH confidence.
- [Playwright Python — iframe handling](https://playwright.dev/python/docs/api/class-page) — `frame_locator()`, `page.screenshot(clip=...)`, persistent context via `launch_persistent_context`. HIGH confidence.
- [Playwright Python — Screenshots](https://playwright.dev/python/docs/screenshots) — `clip` parameter for region capture; async API. HIGH confidence.
- [Playwright Python — Authentication](https://playwright.dev/python/docs/auth) — `launch_persistent_context(user_data_dir=...)` for session persistence across runs. HIGH confidence.
- [GitHub — vike256/Wordbot](https://github.com/vike256/Wordbot) — Reference Letter League bot; CLI only, no board reading, no Discord integration. Confirms gap this project fills.
- [Discord Slash Commands Complete Guide 2025](https://friendify.net/blog/discord-slash-commands-complete-guide-2025.html) — Attachment handling patterns, slash command standards. MEDIUM confidence.

---

*Feature research for: Discord word game AI bot — v1.1 Vision + Discord + Autonomous*
*Researched: 2026-03-24*
