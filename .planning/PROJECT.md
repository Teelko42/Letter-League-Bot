# Letter League Bot

## What This Is

An AI-powered Discord bot that plays the word game Letter League (a Scrabble-like Discord Activity). It operates in two modes: an advisor mode where users send board screenshots and receive optimal word suggestions, and an autonomous mode where the bot joins the game and plays by itself using browser automation. Difficulty is configurable as a percentage of optimal play strength.

## Core Value

The bot must be able to analyze a Letter League board state and find the best possible word placement — everything else (auto-play, difficulty scaling, Discord integration) builds on top of a rock-solid word-finding engine.

## Requirements

### Validated

- ✓ Find optimal word placements given board state, tile rack, and dictionary — v1.0
- ✓ Support configurable difficulty (percentage of optimal play strength) — v1.0
- ✓ Use Wordnik wordlist as the dictionary source — v1.0
- ✓ Support Letter League's scoring rules (letter values, multiplier squares, Wild/Classic modes) — v1.0
- ✓ Handle the 27x19 expandable board grid — v1.0

### Active

- [ ] Analyze Letter League board state from screenshots using AI vision/OCR
- [ ] Advisor mode: user sends screenshot, bot suggests best word + placement
- [ ] Autonomous mode: bot joins game via browser automation and plays as a player

### Out of Scope

- Mobile app or standalone GUI — Discord bot only
- Real-time voice chat interaction — text-based commands only
- Supporting other word games — Letter League specific
- Multiplayer coordination — bot plays as a single player

## Context

Shipped v1.0 with 3,505 LOC Python, 94 tests passing.
Tech stack: Python 3.11, pytest, wordfreq.
Core engine: GADDAG dictionary (Gordon 1994) + LeftPart/ExtendRight move generation + Classic/Wild scoring.
Difficulty system: Blended alpha-weighted score/frequency selection, 0-100% configurable.

- **Letter League** is a Scrabble-like word game built into Discord as an Activity (embedded iframe in voice channels)
- Board starts at 27x19 and expands as words are placed; no fixed max size
- Two scoring modes: **Wild** (multipliers stick permanently to letters) and **Classic** (multipliers apply only on the turn placed, like standard Scrabble)
- Players get a tile rack (likely 7 tiles), can swap tiles or pass turns
- Supports 2-8+ players, recommended max 6
- Discord Activities don't expose APIs — interaction must be visual (browser automation)
- Dictionary source: https://github.com/wordnik/wordlist

## Constraints

- **Tech stack**: Python + discord.py for the Discord bot
- **Browser automation**: Playwright or Selenium for autonomous game interaction
- **Vision/OCR**: AI vision (Claude/GPT) or OCR library for board state extraction
- **Dictionary**: Must use Wordnik wordlist for word validation
- **Discord TOS**: Bot must operate within Discord's terms of service for Activities

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Python + discord.py | Most common Discord bot stack, good library support | — Pending |
| Wordnik wordlist as dictionary | User specified; comprehensive English word list | ✓ Good — loaded 170k+ words |
| Browser automation for auto-play | Discord Activities don't expose APIs; visual interaction is the only path | — Pending |
| Configurable difficulty as % of optimal | More flexible than fixed levels; user can fine-tune bot strength | ✓ Good — blended alpha weighting works well |
| AI vision for board reading | Board is a visual canvas, not structured data; vision/OCR is the only way to parse it | — Pending |
| Dict-based GADDAG (not class-per-node) | Lower memory overhead, O(1) dict lookups in CPython | ✓ Good — fast and memory-efficient |
| Pickle cache with MD5 invalidation | Eliminates wordlist rebuild on startup; auto-invalidates on changes | ✓ Good — instant subsequent loads |
| Gordon (1994) LeftPart/ExtendRight | Industry-standard Scrabble move generation algorithm | ✓ Good — finds all valid placements |
| Blended score/frequency for difficulty | Alpha-weighted: high difficulty = pure score, low = common words | ✓ Good — smooth difficulty gradient |
| GADDAG-arc pruning for blanks | Only try letters with outgoing arcs, not all 26 | ✓ Good — correctness + performance |

---
*Last updated: 2026-03-23 after v1.0 milestone*
