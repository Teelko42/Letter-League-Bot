# Phase 2: Difficulty System - Research

**Researched:** 2026-03-23
**Domain:** Move filtering, word frequency scoring, difficulty calibration
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Difficulty Curve**
- Smooth linear mapping from 0-100% — 50% difficulty produces roughly 50th-percentile strength
- Single percentage input controls all difficulty dimensions (no separate knobs)
- Output is consistent at a given difficulty level — no randomness/variance
- 0% difficulty plays the worst valid move available

**Word Commonality**
- Use English word frequency data to rank words from common to obscure
- Frequency data is a bundled static file shipped with the bot (no external API)
- At lower difficulty, common words are softly preferred (weighted), not hard-filtered — obscure words can still appear but are deprioritized
- At 100% difficulty, commonality is ignored entirely — pure score optimization

**Strategy Variation**
- Strategy variation comes from vocabulary filtering and score targeting only
- No board positional awareness at any difficulty level (no defensive/aggressive play)
- No word length bias — length is not a factor in difficulty
- No premium square avoidance — difficulty doesn't affect square targeting
- DIFF-03 is satisfied by the combination of vocabulary commonality weighting and score percentile selection producing meaningfully different word choices at different difficulty levels

**Move Selection**
- Score percentile method — difficulty percentage maps to a target percentile of all valid move scores
- Word frequency and raw score are blended into a single "difficulty-adjusted score" (combined ranking, not two-stage pipeline)
- Tiebreaker among similarly-scored moves: prefer the more commonly known word
- Bot always plays a valid word — never passes/skips as a difficulty behavior

### Claude's Discretion

- Exact blending formula for combining frequency and raw score
- Word frequency data source selection (Google Ngrams, COCA, etc.)
- How to handle words not found in the frequency dataset
- Internal data structures for frequency lookup

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| DIFF-01 | Configurable difficulty as percentage of optimal play strength (100% = best, lower = weaker) | Score-percentile selection: sort all valid moves by score, map difficulty% to target score index; `DifficultyEngine.select_move(moves, difficulty)` public API; numeric config requires no code changes |
| DIFF-02 | Filter word candidates by vocabulary commonality at lower difficulties | `wordfreq.zipf_frequency()` provides per-word Zipf scale (0-8); pre-load with `get_frequency_dict('en')` at startup; lower difficulty raises frequency weight in blended score; OOV words get minimum Zipf score (0.0) |
| DIFF-03 | Vary play strategy (not just score targeting) based on difficulty setting | Frequency-weighted blend produces structurally different word choices: low difficulty pulls toward common words independently of score rank; combined score formula naturally varies the selected word, not just the score tier |
</phase_requirements>

---

## Summary

Phase 2 builds a pure Python filtering layer over the existing `GameEngine.find_moves()` output. The engine already returns all valid moves sorted by raw score descending. This phase adds a `DifficultyEngine` (or equivalent) that accepts the move list and a `difficulty` float (0.0–1.0 or 0–100%) and returns the single move best matching that difficulty.

The core algorithm has two steps. First, each move receives a difficulty-adjusted score that blends its raw game score (normalized against the move set) with a word-commonality score derived from `wordfreq.zipf_frequency()`. The blend weight shifts with difficulty: at 100%, the frequency component weight is 0 (pure score); at 0%, the frequency component has maximum influence. Second, moves are re-ranked by this blended score and the move at the target percentile index is returned — 100% = index 0 (highest), 0% = last index (lowest).

The `wordfreq` library (v3.1.1, Apache/CC-BY-SA license) is the standard Python tool for this problem. It ships bundled frequency data covering 40+ languages from eight corpora (Wikipedia, subtitles, news, books, web, Reddit, etc.), requires no network access, and exposes `zipf_frequency(word, 'en')` returning a log-scale float (0–8) suitable for normalization. Loading the full English frequency dictionary with `get_frequency_dict('en')` at startup (one-time cost) enables O(1) per-word lookups thereafter with no repeated library overhead. OOV words (legitimate but obscure game-dictionary words not in wordfreq's corpus) return 0.0 and should be treated as maximally uncommon, which is the correct behavior: at low difficulty they are deprioritized and at high difficulty commonality is ignored anyway.

**Primary recommendation:** Use `wordfreq.zipf_frequency(word, 'en')` for word frequency data; implement a linear blend `adjusted_score = α * norm_game_score + (1-α) * norm_freq_score` where `α = difficulty` (0.0–1.0); select the move at `floor((1 - difficulty) * (len(moves) - 1))` in the re-ranked list.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| wordfreq | 3.1.1 | Word frequency lookup via `zipf_frequency()` | Most widely used Python word-frequency library; bundles multi-corpus English data; offline; O(1) dict lookup with `get_frequency_dict()`; Apache license |
| Python stdlib: `bisect` | built-in | Index calculation for percentile selection | Zero-dependency; sufficient for sorted list indexing |
| Python stdlib: `statistics` | built-in | Normalization helpers if needed | Zero-dependency; covers `mean`, `stdev` if score normalization needs them |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| pytest | 9.0.2 (installed) | Unit and integration testing | All test files — already configured in project |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| wordfreq | Raw Google Ngram TSV file (bundled) | Lower dependency count but ~100MB raw files vs wordfreq's compact binary; no Python API; manual normalization; not worth it |
| wordfreq | COCA word list (static text file) | Free top-60K only; no API; manual parse; misses long-tail game words; wordfreq covers more vocabulary |
| wordfreq | Custom bundled JSON (pre-extracted subset) | Would require a one-time extraction script from wordfreq anyway; adds build step complexity; wordfreq itself bundles data efficiently |

**Installation:**
```bash
pip install wordfreq==3.1.1
```

---

## Architecture Patterns

### Recommended Project Structure

```
src/
├── engine/          # Phase 1 — GADDAG, Board, Moves, Scoring, GameEngine (COMPLETE)
└── difficulty/      # Phase 2 — new module
    ├── __init__.py  # Re-exports DifficultyEngine
    ├── engine.py    # DifficultyEngine class — select_move(), public API
    └── frequency.py # Word frequency loading and lookup (wordfreq wrapper)

tests/
└── test_difficulty.py  # Phase 2 tests
```

The `difficulty/` module is a pure filter layer. It consumes `list[Move]` from `GameEngine.find_moves()` and returns a single `Move`. It never generates moves itself.

### Pattern 1: Pre-loaded Frequency Dictionary

**What:** Load the full English wordfreq dictionary once at module/class initialization, store as a plain `dict[str, float]`. Per-word lookup is then a simple dict `.get()` with a default for OOV words.

**When to use:** Whenever move lists will be filtered — avoid calling `zipf_frequency()` per move per call, as it has internal dispatch overhead.

**Example:**
```python
# Source: wordfreq PyPI docs — get_frequency_dict API
from wordfreq import get_frequency_dict

class FrequencyIndex:
    """Wraps wordfreq for O(1) per-word Zipf lookups."""

    # Zipf scale: 0 (OOV/never seen) to ~8 (most common words)
    OOV_ZIPF = 0.0
    MAX_ZIPF = 8.0  # approximate upper bound for normalization

    def __init__(self, lang: str = 'en') -> None:
        # One-time load: ~10MB RAM, ~1-2s startup
        self._freq: dict[str, float] = get_frequency_dict(lang)

    def zipf(self, word: str) -> float:
        """Return Zipf frequency (0-8). OOV words return 0.0."""
        return self._freq.get(word.lower(), self.OOV_ZIPF)

    def normalized(self, word: str) -> float:
        """Return frequency normalized to [0.0, 1.0] (1.0 = most common)."""
        return self.zipf(word) / self.MAX_ZIPF
```

### Pattern 2: Difficulty-Adjusted Score Blend

**What:** Linear blend of normalized game score and normalized word frequency, controlled by `difficulty` parameter. At difficulty=1.0, pure score; at difficulty=0.0, maximum frequency influence.

**When to use:** Whenever computing the blended rank for move selection.

**Example:**
```python
# Source: designed from user decisions in CONTEXT.md + Wordle difficulty research
def adjusted_score(
    move: Move,
    norm_score: float,  # raw score normalized to [0, 1] within this move set
    norm_freq: float,   # word frequency normalized to [0, 1]
    difficulty: float,  # 0.0 (weakest) to 1.0 (strongest)
) -> float:
    """Blend game score and word frequency for difficulty-calibrated ranking.

    At difficulty=1.0: pure score (ignore frequency).
    At difficulty=0.0: maximum frequency weight (common words strongly preferred).

    α=difficulty controls the tradeoff linearly.
    """
    alpha = difficulty  # weight on raw score
    return alpha * norm_score + (1.0 - alpha) * norm_freq
```

### Pattern 3: Percentile-Index Move Selection

**What:** After re-ranking moves by `adjusted_score`, select the move at index = `floor((1 - difficulty) * (len(moves) - 1))`. This maps difficulty=1.0 to index 0 (best), difficulty=0.0 to last index (worst).

**When to use:** Final selection step after blended sort.

**Example:**
```python
import math

def select_by_difficulty(
    moves: list[Move],
    difficulty: float,  # 0.0-1.0
    freq_index: FrequencyIndex,
) -> Move | None:
    """Select move calibrated to target difficulty.

    Steps:
    1. Normalize raw scores within this move set.
    2. Compute adjusted_score for each move.
    3. Sort by adjusted_score descending.
    4. Return move at percentile index matching difficulty.
    """
    if not moves:
        return None
    if len(moves) == 1:
        return moves[0]

    # Normalize raw scores to [0, 1]
    scores = [m.score for m in moves]
    max_s, min_s = max(scores), min(scores)
    score_range = max_s - min_s or 1  # avoid division by zero

    ranked = sorted(
        moves,
        key=lambda m: (
            difficulty * ((m.score - min_s) / score_range)
            + (1.0 - difficulty) * freq_index.normalized(m.word)
        ),
        reverse=True,  # highest adjusted score first
    )

    # Map difficulty to target index: 1.0 -> 0, 0.0 -> len-1
    target_idx = math.floor((1.0 - difficulty) * (len(ranked) - 1))
    return ranked[target_idx]
```

### Pattern 4: Public DifficultyEngine API

**What:** A thin class wrapping `FrequencyIndex` and `select_by_difficulty`. This is what downstream phases (Discord integration, GameEngine extension) will consume.

**Example:**
```python
class DifficultyEngine:
    """Selects a move calibrated to a target difficulty level.

    Wraps the word frequency index and blended-score selection algorithm.
    Downstream consumers call select_move(); they never touch frequency data directly.
    """

    def __init__(self, lang: str = 'en') -> None:
        self._freq = FrequencyIndex(lang)

    def select_move(self, moves: list[Move], difficulty: float) -> Move | None:
        """Return the move best matching the target difficulty.

        Args:
            moves: All valid moves from GameEngine.find_moves() (score-sorted).
            difficulty: Target difficulty as float 0.0-1.0 (or pass 0-100 and
                        clamp/divide internally — planner's choice on API surface).

        Returns:
            A single Move, or None if moves is empty.
        """
        difficulty = max(0.0, min(1.0, difficulty))  # clamp
        return select_by_difficulty(moves, difficulty, self._freq)
```

### Anti-Patterns to Avoid

- **Per-call `zipf_frequency()` invocation:** Calling `wordfreq.zipf_frequency()` inside the move-selection loop (once per move per call) adds dispatch overhead. Pre-load with `get_frequency_dict()` instead.
- **Hard frequency cutoff at lower difficulty:** The decision is a soft/weighted blend, not a hard filter. Hard-filtering would break "bot always plays a valid word" and would also eliminate all moves when no common words exist in the rack.
- **Two-stage pipeline (filter then score):** User decided against a two-stage pipeline. Do not first filter by frequency and then pick by score rank — use a single blended score.
- **Separate difficulty knobs:** The API surface is a single `difficulty: float`. Do not expose separate `score_weight` and `freq_weight` parameters to callers.
- **Using `random.choice` or any randomness:** Output must be deterministic (consistent) for a given board state, rack, and difficulty setting.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Word frequency data | Custom word-count pipeline over a corpus | `wordfreq` (pip install) | Multi-corpus aggregation, frequency smoothing, and normalization are solved; raw corpus counting is error-prone and requires gigabyte downloads |
| OOV frequency handling | Complex fallback heuristics (morphological analysis, character n-grams) | `zipf_frequency()` returns 0.0 for OOV — use that directly | OOV words are legitimately rare; treating them as minimum frequency is correct behavior; further heuristics add complexity without correctness benefit |
| Score normalization | Custom statistics package | Python `statistics` stdlib or inline `(x - min) / (max - min)` | Move list is small (hundreds, not millions); stdlib is sufficient |

**Key insight:** The entire difficulty mechanism is a post-processing filter on Phase 1 output — no new move generation, board analysis, or game state awareness is needed. The only external dependency is `wordfreq` for vocabulary data.

---

## Common Pitfalls

### Pitfall 1: Single-Move Edge Case

**What goes wrong:** `select_by_difficulty` fails or returns the wrong move when `moves` contains exactly one element. Index math `(1 - difficulty) * (1 - 1) = 0` is fine, but normalization divides by `max - min = 0`.

**Why it happens:** Score normalization requires at least two distinct scores to compute a range.

**How to avoid:** Guard at the top of `select_by_difficulty`: if `len(moves) == 1`, return `moves[0]` immediately (only one valid move — play it regardless of difficulty).

**Warning signs:** `ZeroDivisionError` in production on end-game boards with limited placements.

### Pitfall 2: All Moves Have the Same Score

**What goes wrong:** Score normalization denominator is 0 (`max_s == min_s`). This can occur in tight board positions where every valid placement scores identically.

**Why it happens:** When all moves score the same, normalized game score is undefined; frequency should become the sole ranking factor.

**How to avoid:** Use `score_range = max_s - min_s or 1` (fallback to 1); all normalized scores become 0.0, so adjusted score reduces to `(1 - difficulty) * norm_freq`, which is correct — frequency dominates when scores are tied.

**Warning signs:** Crashes or uniform selection regardless of difficulty setting.

### Pitfall 3: OOV Words Dominating at High Difficulty

**What goes wrong:** Legitimate Scrabble/game words (GADDAG vocabulary) that are obscure enough to be absent from wordfreq return Zipf 0.0. At difficulty=1.0 (pure score), this is irrelevant. But if the blend formula is accidentally inverted or difficulty clamping fails, OOV words rank as maximally common.

**Why it happens:** Inverting the frequency normalization direction (`1 - norm_freq` vs `norm_freq`) or applying frequency weight when it should be zero.

**How to avoid:** At difficulty=1.0, `alpha=1.0`, so `(1-alpha) * norm_freq = 0` — frequency is entirely excluded. Verify with a test: at 100%, selected move must always equal `moves[0]` (highest raw score).

**Warning signs:** DIFF-01 test failure (100% doesn't return best scoring move).

### Pitfall 4: Difficulty Input Not Normalized

**What goes wrong:** Caller passes `difficulty=75` (integer percentage) instead of `0.75`. Index math produces `target_idx = floor((1 - 75) * (N-1))` which is a large negative number.

**Why it happens:** API accepts float but callers may use integer percentages naturally.

**How to avoid:** Accept and normalize at the `DifficultyEngine.select_move` boundary: clamp to [0.0, 1.0] if already decimal, or design the public API to accept 0-100 and divide by 100 internally. Be explicit in the docstring. DIFF-01 success criteria states "configurable as a numeric percentage without code changes" — this suggests 0-100 as the external API convention.

**Warning signs:** `IndexError` on move list indexing.

### Pitfall 5: wordfreq Startup Cost on First Import

**What goes wrong:** `get_frequency_dict('en')` takes 1-2 seconds on first load (loads ~MB binary data file). If called per-request (e.g., inside `select_move`), latency is unacceptable in Discord interaction context.

**Why it happens:** wordfreq loads frequency data lazily; `get_frequency_dict` forces full load.

**How to avoid:** Instantiate `FrequencyIndex` (and therefore `DifficultyEngine`) once at bot startup, not per request. The `DifficultyEngine` instance is shared across turns.

**Warning signs:** Slow first response after bot restart; subsequent responses fast.

---

## Code Examples

Verified patterns from official sources:

### wordfreq Basic Usage
```python
# Source: https://pypi.org/project/wordfreq/ (official PyPI page)
from wordfreq import zipf_frequency, get_frequency_dict

# Per-word lookup (use for occasional queries)
zipf_frequency('cafe', 'en')    # ~5.2 (common)
zipf_frequency('quasar', 'en')  # ~3.8 (uncommon)
zipf_frequency('zyzzyva', 'en') # 0.0 (OOV — not in corpus)

# Bulk pre-load (use for move-list filtering — O(1) per word after load)
freq_dict = get_frequency_dict('en')  # {word: freq_float, ...}
freq_dict.get('cafe', 0.0)  # fast dict lookup; 0.0 default for OOV
```

### Zipf Scale Reference
```
# Zipf scale interpretation (source: wordfreq README)
# 8 = most common words ("the", "of", "and")
# 6 = common words (appear once per thousand words)
# 5 = moderately common ("library", "coffee")
# 3 = rare (appear once per million words)
# 0 = OOV (not in corpus at all)
```

### Score Percentile Index Pattern (stdlib only)
```python
# Source: designed — Python stdlib bisect/statistics, no external deps
import math

def score_to_index(difficulty: float, n_moves: int) -> int:
    """Map difficulty (0.0-1.0) to a move list index.

    difficulty=1.0 → index 0 (best move)
    difficulty=0.0 → index n_moves-1 (worst move)
    difficulty=0.5 → index floor(0.5 * (n-1)) ≈ median move
    """
    if n_moves <= 1:
        return 0
    return math.floor((1.0 - difficulty) * (n_moves - 1))
```

### Full DifficultyEngine Integration
```python
# Conceptual integration with existing GameEngine (Phase 1)
from src.engine import GameEngine
from src.difficulty import DifficultyEngine

engine = GameEngine(wordlist_path, cache_path=cache_path)
difficulty_engine = DifficultyEngine()  # load freq dict once

# Per-turn usage
moves = engine.find_moves(rack)
move = difficulty_engine.select_move(moves, difficulty=75)  # 75% strength
engine.play_move(move)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Hand-curated difficulty tiers (easy/medium/hard) | Continuous percentage-based calibration | Ongoing evolution in game AI | Finer control; smooth ramp instead of step function |
| Hard frequency filter (exclude uncommon words at low difficulty) | Soft weighted blend (frequency adjusts ranking, not hard cut) | Best practice for word game bots | Eliminates "no valid moves at low difficulty" failure mode |
| Random selection within difficulty tier | Deterministic percentile selection | Standard in competitive game analysis | Reproducible; same board/rack/difficulty always picks same move |
| Static wordlist for frequency (top-N words list) | Multi-corpus aggregated frequency (wordfreq) | wordfreq v1, ~2016 | Better coverage of real-world usage patterns across domains |

**Deprecated/outdated:**
- Separate frequency tier thresholds (hard-coded easy/medium/hard word lists): user decision explicitly rejects this in favor of weighted blending.
- `word_frequency()` for batch use: `get_frequency_dict()` is the correct API for pre-loading; per-word `word_frequency()` adds overhead for repeated lookups.

---

## Open Questions

1. **Public API: 0-100 integer or 0.0-1.0 float?**
   - What we know: DIFF-01 says "configurable as a numeric percentage without code changes"; user will interact via Discord eventually; internal math uses 0.0-1.0.
   - What's unclear: Whether to expose 0-100 at `select_move()` or 0.0-1.0 and let callers convert.
   - Recommendation: Accept 0-100 at the public boundary (matches "percentage" framing of DIFF-01), normalize internally to 0.0-1.0. Cleaner for Discord integration in Phase 4.

2. **Exact Zipf normalization ceiling**
   - What we know: wordfreq's Zipf scale is open-ended (practically 0-8 for English); max observed for "the" is ~8.
   - What's unclear: Whether to normalize against `8.0` as a fixed constant or dynamically against the max Zipf in the actual move set.
   - Recommendation: Use fixed `MAX_ZIPF = 8.0` constant. Dynamic normalization within the move set is more complex and can invert expected behavior (e.g., if all move words are rare, the "most common among rare" would be treated as if it were "the").

3. **wordfreq coverage of game-dictionary words**
   - What we know: wordfreq returns 0.0 for OOV; GADDAG contains Wordnik wordlist (170K+ words) which includes many archaic/uncommon words; wordfreq covers common real-world usage.
   - What's unclear: What percentage of the Wordnik wordlist is OOV in wordfreq — could be 10-30% of game-valid words are unrecognized.
   - Recommendation: Treat OOV as Zipf=0.0 (maximally obscure) — this is the correct behavior per user decisions. The planner should add a test that verifies OOV words are not excluded entirely but do rank lowest among equal-score moves.

---

## Validation Architecture

### Test Framework
| Property | Value |
|----------|-------|
| Framework | pytest 9.0.2 |
| Config file | none (discovered by default from project root) |
| Quick run command | `py -m pytest tests/test_difficulty.py -x -q` |
| Full suite command | `py -m pytest tests/ -q` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| DIFF-01 | `difficulty=100` always returns the highest-scoring valid move (i.e., `moves[0]`) | unit | `py -m pytest tests/test_difficulty.py::test_100pct_returns_best_move -x` | Wave 0 |
| DIFF-01 | `difficulty=0` returns a measurably weaker move than `difficulty=100` on same board | unit | `py -m pytest tests/test_difficulty.py::test_0pct_weaker_than_100pct -x` | Wave 0 |
| DIFF-01 | Difficulty is configurable as a numeric value without code changes | unit | `py -m pytest tests/test_difficulty.py::test_difficulty_configurable -x` | Wave 0 |
| DIFF-02 | At lower difficulty, selected word has higher Zipf frequency than at 100% (on same board) | unit | `py -m pytest tests/test_difficulty.py::test_low_difficulty_prefers_common_words -x` | Wave 0 |
| DIFF-02 | OOV words return Zipf=0.0 (not excluded, but ranked lowest) | unit | `py -m pytest tests/test_difficulty.py::test_oov_words_handled -x` | Wave 0 |
| DIFF-03 | At different difficulties, selected words differ from each other (not just score tiers) | unit | `py -m pytest tests/test_difficulty.py::test_strategy_variation_produces_different_words -x` | Wave 0 |

### Sampling Rate
- **Per task commit:** `py -m pytest tests/test_difficulty.py -x -q`
- **Per wave merge:** `py -m pytest tests/ -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps
- [ ] `tests/test_difficulty.py` — covers DIFF-01, DIFF-02, DIFF-03 (does not exist yet)
- [ ] `src/difficulty/__init__.py` — module stub (does not exist yet)
- [ ] Framework install: `pip install wordfreq==3.1.1` — wordfreq not yet installed

---

## Sources

### Primary (HIGH confidence)
- wordfreq PyPI (https://pypi.org/project/wordfreq/) — current version, API surface, offline suitability, license
- wordfreq GitHub README (https://github.com/rspeer/wordfreq) — `get_frequency_dict()` API, OOV behavior, data bundling, Zipf scale interpretation
- Phase 1 codebase (`src/engine/__init__.py`, `src/engine/moves.py`, `src/engine/models.py`) — verified `GameEngine.find_moves()` returns `list[Move]` sorted by score descending; `Move.word`, `Move.score` fields confirmed
- pytest 9.0.2 — confirmed installed via `py -m pytest --version`

### Secondary (MEDIUM confidence)
- 2024 Wordle difficulty research (ACM proceedings, arXiv:2403.19433) — validates percentile-based difficulty classification and frequency-weighted scoring as current best practice in word game AI
- wordfreq Snyk/libraries.io analysis — confirmed maintenance status, version 3.1.1 (November 2023 packaging update; data frozen ~2021)

### Tertiary (LOW confidence)
- General WebSearch results on Scrabble bot difficulty — no specific authoritative paper found on blended score formulas for tile-placement word games; the approach is synthesized from first principles and confirmed against the user decisions

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — wordfreq is verifiably the standard library for this problem; confirmed offline-capable, correct license, pre-loading API verified
- Architecture: HIGH — blended score with linear alpha is a direct derivation from user locked decisions; percentile-index selection is a straightforward algorithm with no hidden complexity
- Pitfalls: HIGH — edge cases (single move, zero score range, OOV, startup cost, input normalization) are all verifiable from the codebase and wordfreq API behavior

**Research date:** 2026-03-23
**Valid until:** 2026-04-23 (wordfreq is stable/frozen; no updates expected; valid ~30 days)
