# Feature Research

**Domain:** Discord word game AI bot (Letter League / Scrabble-like)
**Researched:** 2026-03-23
**Confidence:** MEDIUM

---

## Feature Landscape

### Table Stakes (Users Expect These)

Features users assume exist. Missing these = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Board state extraction from screenshot | Core premise — advisor mode is useless without it | HIGH | AI vision (Claude/GPT) or OCR; must handle 27x19 grid, colored multiplier squares, letter tiles, and rack |
| Valid move generation (all legal placements) | Word finder is the engine — without it, the bot is empty | HIGH | Requires GADDAG or DAWG + cross-check sets; must enumerate all anchor positions and extend left/right/down |
| Highest-scoring move recommendation | Users expect THE best word, not a list of options | MEDIUM | Score all candidates, rank by score, return top N with position/direction |
| Slash command interface | Discord standard since 2021; prefix commands feel outdated and archaic | LOW | `/analyze` command accepting screenshot attachment; `/play` to trigger autonomous mode |
| Human-readable response formatting | Bot must clearly communicate tile placement, word, score | LOW | "EXAMPLE at H7 across = 34 pts" format; embed with board visualization optional |
| Wordnik dictionary validation | Specified requirement; users will test obscure words and expect correct validation | MEDIUM | Load Wordnik wordlist at startup into GADDAG/DAWG structure; ~180k words |
| Classic and Wild mode scoring support | Both modes exist in Letter League; advisor would mislead in wrong mode | MEDIUM | Wild mode: letter value persists with multiplier permanently; Classic mode: bonus only on placement turn — these affect score calculation significantly |
| Tile rack input from screenshot | Advisor must read the user's current rack, not just the board | MEDIUM | 7 tiles per rack; must distinguish rack tiles from board tiles in screenshot |
| Error handling with actionable messages | Users upload bad screenshots; bot must not silently fail | LOW | "Couldn't read board — try a cleaner screenshot" type responses |

### Differentiators (Competitive Advantage)

Features that set the product apart. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Configurable difficulty (% of optimal) | No existing Letter League bot offers this; makes bot playable as an opponent, not just a solver | MEDIUM | Implementation: randomly select from top-N moves weighted by score, or cap search depth, or vocabulary restriction. Percentage of optimal = interpolate between worst and best candidate. |
| Autonomous play mode (bot joins and plays) | Removes user from loop entirely; unique capability vs. all known competitors | HIGH | Requires Playwright browser automation; Discord Activity is an iframe; must handle visual tile selection and placement clicks. No existing Letter League bot does this fully. |
| Move explanation with rationale | "ZOEAE scores 44 because Z landed on DL and cross-scores +12" teaches strategy | LOW | Augment response with score breakdown: base letters + multiplier contributions + cross-word scores |
| Top-N alternative moves shown | Users may want to play a slightly inferior word for strategy; showing options = more useful | LOW | Return top 3-5 moves, not just optimal; negligible extra cost after move generation |
| Leave value awareness (rack quality post-move) | Advanced Scrabble strategy — best bots (Maven, Bestbot) use equity = score + leave value | HIGH | Requires precomputed leave tables; significantly more complex than raw score maximization; major differentiator for quality of play |
| Bingo detection and bonus display | Playing all 7 tiles gets a "bingo" bonus (doubled main word in Letter League); users should know when this is achievable | LOW | Flag any 7-tile placements in results; Letter League doubles the main word value on bingo |
| Multi-turn session context | Remember previous moves within a game session to provide running game score context | MEDIUM | Store board state between calls; allows tracking of game progression |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Real-time game monitoring (continuous screenshot polling) | "Watch my screen and alert me" | Requires persistent screen capture infrastructure, high latency, resource-heavy, violates Discord TOS intent; autonomous mode is the right answer for "always on" | Use autonomous mode if full automation is wanted; advisor mode stays on-demand per screenshot |
| Global leaderboard / persistent stats | Feels like a natural extension for a Discord bot | This bot is a game assistant, not a game itself; leaderboard would rank users on "who used the bot most" not actual skill; adds database complexity for zero gameplay value | Out of scope; if users want stats, they can track scores within Discord game itself |
| Voice channel integration / text-to-speech readout | "Bot should announce moves in voice" | Adds audio infrastructure with marginal value; most users are reading not listening; complex edge cases | Text-based slash command responses are sufficient; keep it simple |
| Multi-game support (Wordle, Scrabble GO, etc.) | "Would be cool to support more games" | Scope explosion; board parsing is game-specific; dictionary and rules differ per game; Letter League is the validated use case | One game done excellently beats five games done poorly; explicitly out of scope per PROJECT.md |
| Web dashboard / GUI for bot config | "I want to configure difficulty in a UI" | Adds a whole web app for settings that Discord slash commands handle natively; massive complexity for no user benefit | `/setdifficulty 70` slash command replaces an entire config dashboard |
| Full tournament mode with multiple human players | "Run our Letter League tournament" | Bot is a single-player assistant/participant; coordinating multi-player tournament logic is a different product | Bot plays as one player; humans can manage tournament structure themselves |
| Caching every board state for replay | "Show me the game history" | Letter League doesn't expose game history via API; would require capturing every screenshot across an entire session; storage and privacy concerns | Bot operates per-turn, stateless by default; in-session context is a lighter alternative |

---

## Feature Dependencies

```
[Wordnik dictionary loaded into GADDAG/DAWG]
    └──requires──> [Valid move generation]
                       └──requires──> [Board state extraction (OCR/vision)]
                                          └──requires──> [Screenshot ingestion via slash command]

[Valid move generation]
    └──requires──> [Classic vs. Wild mode scoring logic]

[Highest-scoring move recommendation]
    └──requires──> [Valid move generation]

[Top-N alternatives]
    └──requires──> [Highest-scoring move recommendation]

[Move explanation with rationale]
    └──requires──> [Highest-scoring move recommendation]

[Bingo detection]
    └──requires──> [Valid move generation]

[Difficulty % scaling]
    └──requires──> [Valid move generation]
                       └──enhances──> [Autonomous play mode]

[Autonomous play mode]
    └──requires──> [Valid move generation]
    └──requires──> [Board state extraction (OCR/vision)]
    └──requires──> [Playwright browser automation]

[Leave value awareness]
    └──requires──> [Valid move generation]
    └──enhances──> [Highest-scoring move recommendation]

[Multi-turn session context]
    └──enhances──> [Advisor mode]
    └──conflicts──> [Stateless per-command design]
```

### Dependency Notes

- **Board state extraction is the critical path blocker.** Every other feature depends on reliably parsing the board from a screenshot. This is the highest risk item in the entire project.
- **GADDAG construction requires dictionary first.** Wordnik wordlist must be loaded and compiled into the GADDAG structure at bot startup. Cold-start penalty is acceptable; do not rebuild per request.
- **Wild vs. Classic mode scoring diverges early.** The scoring system is baked into move evaluation. Getting this wrong means all recommended moves are scored incorrectly. Must be determined per game session (or per `/analyze` call parameter).
- **Autonomous mode requires all of advisor mode plus browser automation.** Build advisor first; autonomous mode layers on top. Do not attempt to build autonomous mode without a working advisor.
- **Leave value awareness conflicts with simple difficulty scaling.** If the bot uses equity (score + leave), "difficulty as % of optimal" becomes harder to define. For v1, use raw score maximization and simple % interpolation. Add equity later.

---

## MVP Definition

### Launch With (v1)

Minimum viable product — what's needed to validate the concept and prove the core value proposition.

- [ ] **Board state extraction via AI vision** — Without this, nothing works. Use Claude Vision or GPT-4o to parse screenshot into a 27x19 grid representation with letter values and multiplier squares.
- [ ] **Tile rack extraction from screenshot** — Parse the 7 rack tiles from the same screenshot; they're visually distinct from board tiles.
- [ ] **GADDAG/DAWG word finder with Wordnik dictionary** — Core engine. All valid placements for the given rack on the given board.
- [ ] **Score calculation (Classic mode only)** — Ship Classic first; it's standard Scrabble behavior and simpler. Wild mode adds permanent-multiplier tracking complexity.
- [ ] **Slash command `/analyze` accepting screenshot attachment** — Standard Discord interaction pattern; attach a screenshot, get optimal move back.
- [ ] **Top 3 move suggestions with score and placement** — Return "WORD at C5 across = 42 pts" format for top 3 candidates.
- [ ] **Configurable difficulty %** — Core differentiator. Implement as: generate all valid moves sorted by score, select randomly from top-N where N scales with difficulty %. `100% = always best`, `50% = random from top half`, `0% = random valid word`.

### Add After Validation (v1.x)

Features to add once core advisor is working and users are using it.

- [ ] **Wild mode scoring** — Add permanent multiplier tracking to score calculation; needed for users playing the default mode.
- [ ] **Move explanation with score breakdown** — "Z=10 on DL(x2)=20, cross-word APES=8, total=42" — add once core is stable.
- [ ] **Bingo detection flag** — Mark 7-tile plays explicitly; low effort, high user delight.
- [ ] **In-session board state memory** — Let users call `/analyze` multiple times in a game without re-parsing the full board each time; store board state per channel/user session with TTL.

### Future Consideration (v2+)

Features to defer until core advisor is validated.

- [ ] **Autonomous play mode** — Highest complexity feature; requires Playwright + full browser automation of Discord's Activity iframe. Build only after advisor mode is solid and board parsing is reliable.
- [ ] **Leave value / equity scoring** — Advanced strategy layer; significantly more complex and requires precomputed leave tables. Defers raw-score-maximization in favor of strategic tile retention.
- [ ] **Monte Carlo lookahead (opponent modeling)** — State-of-the-art Scrabble AI uses simulation of future turns; overkill for v1 but worth exploring for autonomous mode quality.

---

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Board state extraction (vision/OCR) | HIGH | HIGH | P1 |
| Tile rack extraction | HIGH | MEDIUM | P1 |
| GADDAG word finder + Wordnik dict | HIGH | HIGH | P1 |
| Classic mode scoring | HIGH | MEDIUM | P1 |
| `/analyze` slash command | HIGH | LOW | P1 |
| Top-N move recommendations | HIGH | LOW | P1 |
| Difficulty % scaling | HIGH | LOW | P1 |
| Wild mode scoring | HIGH | MEDIUM | P2 |
| Move explanation / score breakdown | MEDIUM | LOW | P2 |
| Bingo detection | MEDIUM | LOW | P2 |
| In-session board state memory | MEDIUM | MEDIUM | P2 |
| Autonomous play mode (Playwright) | HIGH | HIGH | P3 |
| Leave value / equity scoring | MEDIUM | HIGH | P3 |
| Monte Carlo lookahead | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for launch
- P2: Should have, add when possible
- P3: Nice to have, future consideration

---

## Competitor Feature Analysis

| Feature | vike256/Wordbot (reference bot) | 23f3000839/Letter_League_AI | Our Approach |
|---------|--------------------------------|------------------------------|--------------|
| Board reading from screenshot | None — manual word input only | Chrome extension (partial) | AI vision (Claude/GPT-4o) via slash command |
| Word finding / move generation | Yes — CLI only | Yes — word suggestions | GADDAG + Wordnik in Discord bot |
| Discord integration | None (CLI only) | Partial (Chrome extension) | Full discord.py slash commands |
| Autonomous play | None | No (suggestion only) | Playwright browser automation (v2) |
| Difficulty levels | None | None | Configurable % of optimal (v1) |
| Wild vs. Classic scoring | Unknown | Unknown | Both modes supported |
| Tile rack handling | Manual input | Partial | Extracted from screenshot |
| Move explanation | None | None | Score breakdown per component |

**Gap analysis:** No existing Letter League bot combines screenshot-based board reading with Discord integration. The reference bot (Wordbot) is CLI-only with manual input. The AI project is a Chrome extension under active development but not a Discord bot. This project has clear differentiating room.

---

## Sources

- [GitHub - vike256/Wordbot: Assistant for the Discord minigame called Letter League](https://github.com/vike256/Wordbot) — reference implementation (CLI only, no board reading)
- [GitHub - 23f3000839/Letter_League_AI](https://github.com/23f3000839/Letter_League_AI) — Chrome extension approach, reinforcement learning angle
- [GitHub - jevndev/letter-league-bot](https://github.com/jevndev/letter-league-bot) — simple bot implementation
- [Letter League FAQ - Discord Apps and Activities](https://support-apps.discord.com/hc/en-us/articles/26502196674583-Letter-League-FAQ) — official game mechanics (403 at time of research)
- [Letter League - Discord Fandom Wiki](https://discord.fandom.com/wiki/Letter_League) — game mechanics reference
- [What is Letter League in Discord - TheLinuxCode](https://thelinuxcode.com/what-is-letter-league-in-discord/) — 7-tile rack confirmed, scoring modes, board expansion
- [Scrabblecam - Find best moves from Scrabble board pictures](https://scrabblecam.com/) — competitor advisor mode: photo → move suggestions workflow
- [Maven (Scrabble) - Wikipedia](https://en.wikipedia.org/wiki/Maven_(Scrabble)) — state-of-the-art Scrabble AI: equity = score + leave value, Monte Carlo lookahead
- [A Faster Scrabble Move Generation Algorithm - Gordon 1994](https://ericsink.com/downloads/faster-scrabble-gordon.pdf) — GADDAG algorithm paper
- [GADDAG on PyPI](https://pypi.org/project/GADDAG/) — Python GADDAG implementation available
- [Coding The World's Fastest Scrabble Program in Python - Aydin Schwartz, Medium](https://medium.com/@aydinschwa/coding-the-worlds-fastest-scrabble-program-in-python-2aa09db670e3) — Python Scrabble engine architecture
- [Beyond Leave Tables: CNN Static Evaluator for Scrabble - César Del Solar 2025](https://www.cesardelsolar.com/posts/2025-06-21-nn-scrabble/) — modern Scrabble AI research
- [Discord Slash Commands Complete Guide 2025](https://friendify.net/blog/discord-slash-commands-complete-guide-2025.html) — slash command patterns, attachment handling
- [How to Handle IFrames in Playwright 2025](https://www.tutorials123.com/2025/08/handle-iframes-in-playwright.html) — Playwright iframe automation (relevant for autonomous mode)
- [Difficulty scaling of game AI - ResearchGate](https://www.researchgate.net/publication/228741499_Difficulty_scaling_of_game_AI) — difficulty scaling approaches for game AI

---

*Feature research for: Discord word game AI bot (Letter League)*
*Researched: 2026-03-23*
