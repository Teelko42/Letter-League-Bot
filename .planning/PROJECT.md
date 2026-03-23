# Letter League Bot

## What This Is

An AI-powered Discord bot that plays the word game Letter League (a Scrabble-like Discord Activity). It operates in two modes: an advisor mode where users send board screenshots and receive optimal word suggestions, and an autonomous mode where the bot joins the game and plays by itself using browser automation. Difficulty is configurable as a percentage of optimal play strength.

## Core Value

The bot must be able to analyze a Letter League board state and find the best possible word placement — everything else (auto-play, difficulty scaling, Discord integration) builds on top of a rock-solid word-finding engine.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Analyze Letter League board state from screenshots using AI vision/OCR
- [ ] Find optimal word placements given board state, tile rack, and dictionary
- [ ] Support configurable difficulty (percentage of optimal play strength)
- [ ] Advisor mode: user sends screenshot, bot suggests best word + placement
- [ ] Autonomous mode: bot joins game via browser automation and plays as a player
- [ ] Use Wordnik wordlist as the dictionary source
- [ ] Support Letter League's scoring rules (letter values, multiplier squares, Wild/Classic modes)
- [ ] Handle the 27x19 expandable board grid

### Out of Scope

- Mobile app or standalone GUI — Discord bot only
- Real-time voice chat interaction — text-based commands only
- Supporting other word games — Letter League specific
- Multiplayer coordination — bot plays as a single player

## Context

- **Letter League** is a Scrabble-like word game built into Discord as an Activity (embedded iframe in voice channels)
- Board starts at 27x19 and expands as words are placed; no fixed max size
- Two scoring modes: **Wild** (multipliers stick permanently to letters) and **Classic** (multipliers apply only on the turn placed, like standard Scrabble)
- Players get a tile rack (likely 7 tiles), can swap tiles or pass turns
- Supports 2-8+ players, recommended max 6
- Discord Activities don't expose APIs — interaction must be visual (browser automation)
- Dictionary source: https://github.com/wordnik/wordlist
- An existing simple Python bot (vike256/Wordbot) exists as reference — it's CLI-only, no board reading, no auto-play
- The bot needs to handle the game visually: read the board via OCR/vision, identify tile rack, detect multiplier squares, and click to place tiles

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
| Wordnik wordlist as dictionary | User specified; comprehensive English word list | — Pending |
| Browser automation for auto-play | Discord Activities don't expose APIs; visual interaction is the only path | — Pending |
| Configurable difficulty as % of optimal | More flexible than fixed levels; user can fine-tune bot strength | — Pending |
| AI vision for board reading | Board is a visual canvas, not structured data; vision/OCR is the only way to parse it | — Pending |

---
*Last updated: 2026-03-23 after initialization*
