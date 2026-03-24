# Phase 2: Difficulty System - Context

**Gathered:** 2026-03-23
**Status:** Ready for planning

<domain>
## Phase Boundary

Configurable play strength filtering layered on the move engine. Given a difficulty percentage (0-100%), the system selects a move calibrated to that strength level. The word engine (Phase 1) generates all valid moves; this phase filters and ranks them to match the target difficulty. No UI, no Discord integration — pure engine layer.

</domain>

<decisions>
## Implementation Decisions

### Difficulty Curve
- Smooth linear mapping from 0-100% — 50% difficulty produces roughly 50th-percentile strength
- Single percentage input controls all difficulty dimensions (no separate knobs)
- Output is consistent at a given difficulty level — no randomness/variance
- 0% difficulty plays the worst valid move available

### Word Commonality
- Use English word frequency data to rank words from common to obscure
- Frequency data is a bundled static file shipped with the bot (no external API)
- At lower difficulty, common words are softly preferred (weighted), not hard-filtered — obscure words can still appear but are deprioritized
- At 100% difficulty, commonality is ignored entirely — pure score optimization

### Strategy Variation
- Strategy variation comes from vocabulary filtering and score targeting only
- No board positional awareness at any difficulty level (no defensive/aggressive play)
- No word length bias — length is not a factor in difficulty
- No premium square avoidance — difficulty doesn't affect square targeting
- DIFF-03 is satisfied by the combination of vocabulary commonality weighting and score percentile selection producing meaningfully different word choices at different difficulty levels

### Move Selection
- Score percentile method — difficulty percentage maps to a target percentile of all valid move scores
- Word frequency and raw score are blended into a single "difficulty-adjusted score" (combined ranking, not two-stage pipeline)
- Tiebreaker among similarly-scored moves: prefer the more commonly known word
- Bot always plays a valid word — never passes/skips as a difficulty behavior

### Claude's Discretion
- Exact blending formula for combining frequency and raw score
- Word frequency data source selection (Google Ngrams, COCA, etc.)
- How to handle words not found in the frequency dataset
- Internal data structures for frequency lookup

</decisions>

<specifics>
## Specific Ideas

No specific requirements — open to standard approaches

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 02-difficulty-system*
*Context gathered: 2026-03-23*
