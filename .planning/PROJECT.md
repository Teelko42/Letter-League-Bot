# Letter League Bot

## What This Is

An AI-powered Discord bot that plays the word game Letter League (a Scrabble-like Discord Activity). It operates in two modes: an advisor mode where users send board screenshots and receive optimal word suggestions via slash commands, and an autonomous mode (planned) where the bot joins the game and plays by itself using browser automation. Difficulty is configurable as a percentage of optimal play strength.

## Core Value

The bot must be able to analyze a Letter League board state and find the best possible word placement — everything else (auto-play, difficulty scaling, Discord integration) builds on top of a rock-solid word-finding engine.

## Requirements

### Validated

- ✓ Find optimal word placements given board state, tile rack, and dictionary — v1.0
- ✓ Support configurable difficulty (percentage of optimal play strength) — v1.0
- ✓ Use Wordnik wordlist as the dictionary source — v1.0
- ✓ Support Letter League's scoring rules (letter values, multiplier squares, Wild/Classic modes) — v1.0
- ✓ Handle the 27x19 expandable board grid — v1.0
- ✓ Analyze Letter League board state from screenshots using Claude Vision API — v1.1
- ✓ Advisor mode: user drops screenshot in Discord channel, bot responds with best word + placement — v1.1
- ✓ Discord bot foundation (discord.py, slash commands, configuration) — v1.1

### Active

- [ ] Autonomous mode: bot joins voice channel via own Discord account, opens Activity with Playwright, plays as a participant

## Current Milestone: v1.2 Browser Automation + Autonomous Play

**Goal:** Enable the bot to autonomously join a Letter League game via Playwright, detect its turn, place tiles, and complete plays without human intervention.

**Target features:**
- Persistent Playwright browser session with saved Discord login
- Navigate Discord web client to voice channel and open Letter League Activity
- Capture non-blank canvas screenshots from Activity iframe
- Turn detection via visual state changes
- Tile placement by clicking rack tiles and board cells at computed coordinates
- Word confirmation via game UI

### Out of Scope

- Mobile app or standalone GUI — Discord bot only
- Real-time voice chat interaction — text-based commands only
- Supporting other word games — Letter League specific
- Multiplayer coordination — bot plays as a single player
- OCR fallback (Tesseract) — Claude Vision handles canvas-rendered text natively
- Headless browser in production — Discord detects headless Chromium; use headed with virtual display

## Context

Shipped v1.1 with 5,155 LOC Python, 107 tests passing.
Tech stack: Python 3.10, discord.py 2.7.1, anthropic SDK, OpenCV, Pillow, pytest, wordfreq.
Core engine: GADDAG dictionary (Gordon 1994) + LeftPart/ExtendRight move generation + Classic/Wild scoring.
Difficulty system: Blended alpha-weighted score/frequency selection, 0-100% configurable.
Vision pipeline: OpenCV HSV preprocessing + Claude Vision API (claude-sonnet-4-6) with structured JSON schema output + BFS flood-fill validation.
Discord bot: slash commands (/analyze, /setdifficulty, /setmode) with per-channel state, color-coded embeds, text-art board rendering.

- **Letter League** is a Scrabble-like word game built into Discord as an Activity (embedded iframe in voice channels)
- Board starts at 27x19 and expands as words are placed; no fixed max size
- Two scoring modes: **Wild** (multipliers stick permanently to letters) and **Classic** (multipliers apply only on the turn placed, like standard Scrabble)
- Players get a tile rack (likely 7 tiles), can swap tiles or pass turns
- Supports 2-8+ players, recommended max 6
- Discord Activities don't expose APIs — interaction must be visual (browser automation)
- Dictionary source: https://github.com/wordnik/wordlist

## Constraints

- **Tech stack**: Python + discord.py for the Discord bot
- **Browser automation**: Playwright for autonomous game interaction (async API only)
- **Vision**: Claude Vision API for board state extraction from screenshots
- **Dictionary**: Must use Wordnik wordlist for word validation
- **Discord TOS**: Bot must operate within Discord's terms of service for Activities

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Python + discord.py | Most common Discord bot stack, good library support | ✓ Good — bot connects, commands register instantly |
| Wordnik wordlist as dictionary | User specified; comprehensive English word list | ✓ Good — loaded 170k+ words |
| Browser automation for auto-play | Discord Activities don't expose APIs; visual interaction is the only path | — Pending |
| Configurable difficulty as % of optimal | More flexible than fixed levels; user can fine-tune bot strength | ✓ Good — blended alpha weighting works well |
| Claude Vision API for board reading | Board is a visual canvas, not structured data; Claude vision excels at structured extraction | ✓ Good — structured output eliminates JSON parse errors |
| Slash commands (not message-based) | Discord deprecated prefix commands; slash commands have native attachment UI | ✓ Good — /analyze accepts screenshot attachment natively |
| Bot's own Discord account for auto-play | Needs to join voice channel and access Activity as a participant | — Pending |
| Dict-based GADDAG (not class-per-node) | Lower memory overhead, O(1) dict lookups in CPython | ✓ Good — fast and memory-efficient |
| Pickle cache with MD5 invalidation | Eliminates wordlist rebuild on startup; auto-invalidates on changes | ✓ Good — instant subsequent loads |
| Gordon (1994) LeftPart/ExtendRight | Industry-standard Scrabble move generation algorithm | ✓ Good — finds all valid placements |
| Blended score/frequency for difficulty | Alpha-weighted: high difficulty = pure score, low = common words | ✓ Good — smooth difficulty gradient |
| GADDAG-arc pruning for blanks | Only try letters with outgoing arcs, not all 26 | ✓ Good — correctness + performance |
| AsyncAnthropic client | Sync client blocks discord.py event loop | ✓ Good — non-blocking vision calls |
| output_config json_schema | Constrains Claude token generation to schema; eliminates parse errors | ✓ Good — zero JSON failures |
| BFS flood-fill for connectivity | Avoids false positives on word endpoint tiles | ✓ Good — accurate tile group validation |
| defer-first pattern in /analyze | Vision API takes 4-15s; Discord times out at 3s | ✓ Good — prevents interaction timeout |
| Per-channel in-memory state | No persistence needed for initial advisor mode | ✓ Good — simple, resets on restart |

---
*Last updated: 2026-03-24 after v1.2 milestone start*
