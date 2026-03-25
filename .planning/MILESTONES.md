# Milestones

## v1.0 Word Engine + Difficulty System (Shipped: 2026-03-24)

**Phases completed:** 2 phases, 6 plans, 0 tasks

**Key accomplishments:**
- GADDAG dictionary with O(word_length) lookup, pickle cache with MD5 invalidation
- Board state management with configurable grid, multiplier layout, anchor/cross-check precomputation
- Classic and Wild mode scoring engine with bingo bonus and perpendicular word scoring
- Gordon (1994) LeftPart/ExtendRight move generation with blank tile optimization
- GameEngine stateful public API wrapping the full word engine pipeline
- DifficultyEngine with blended alpha-weighted score/frequency selection (0-100% difficulty)

**Stats:** 3,505 LOC Python | 94 tests passing | 43 files | 1 day (2026-03-23)
**Git range:** feat(01-01) → feat(02-02)
**Known gaps:** 11 v1 requirements deferred to next milestone (VISN-01..04, DISC-01..04, AUTO-01..03)

---


## v1.1 Vision + Discord Integration (Shipped: 2026-03-25)

**Phases completed:** 2 phases (3-4), 4 plans, 10 tasks

**Key accomplishments:**
- OpenCV HSV board detection + Pillow 2x LANCZOS upscale for screenshot preprocessing
- Claude Vision API extractor with `output_config json_schema` — JSON parse errors eliminated at the token level
- BFS flood-fill validator with four checks (letters, connectivity, multipliers, rack)
- discord.py bot with per-channel state isolation, color-coded embeds, and text-art board renderer
- AdvisorCog with /analyze (full vision+engine pipeline), /setdifficulty, /setmode — human-verified in Discord guild

**Stats:** 5,155 LOC Python | 107 tests passing | 42 files changed | 1 day (2026-03-24)
**Git range:** feat(03-01) → feat(04-02)

**Scope adjustment:** Phases 5-6 (Browser Automation + Autonomous Play, AUTO-01 through AUTO-06) deferred to next milestone.

---

