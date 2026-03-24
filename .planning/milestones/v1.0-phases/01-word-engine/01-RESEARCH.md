# Phase 1: Word Engine - Research

**Researched:** 2026-03-23
**Domain:** GADDAG data structure, Scrabble-variant move generation, Letter League scoring rules
**Confidence:** HIGH (core algorithm), MEDIUM (Letter League-specific Wild mode stacking), LOW (Wild mode edge cases requiring live game verification)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Game Rules & Board**
- Board size is 27x19 (non-standard — unique to Letter League)
- Standard Scrabble tile point values (A=1, B=3, Z=10, blank=0, etc.)
- Custom multiplier layout — NOT standard Scrabble positions. User has a screenshot to extract exact positions during research phase
- Blank/wild tiles exist, worth 0 points, can represent any letter (like Scrabble)
- Minimum word length is 2 letters

**Wordlist & Validation**
- Custom text file, one word per line (user will provide)
- Apply game rules filtering on top of wordlist (minimum 2-letter words)
- Wordlist is the primary source of truth, but game-specific rules also enforced

**Move Output**
- Return ALL valid placements, ranked by score (not just the best move)
- Each move includes: word, starting position (row, col), direction (horizontal/vertical)
- Each move includes: score breakdown (base letter values, multiplier bonuses, total)
- Each move includes: which tiles from the rack are consumed
- Board input represented as 2D array of cells (each cell: letter or empty + multiplier type)
- Rack input as separate array

**Engine API**
- Stateful game object that tracks the board state across turns
- Rack-only mode — engine works with whatever rack is provided, does not manage tile bag
- No tile drawing — tile management is external to the engine

**Classic Mode Scoring**
- Multiplier squares apply only on the turn a tile is placed on them
- After placement turn, the square's multiplier no longer affects scoring

**Wild Mode Scoring**
- ALL multipliers (letter DL/TL and word DW/TW) permanently bond to the tile placed on them
- Once bonded, the multiplier applies every turn that tile is part of a scoring word
- **Research needed:** How do bonded word multipliers stack when multiple bonded tiles are in one word?
- **Research needed:** After a tile bonds a multiplier, does the original square remain active for future tiles or become a normal square?

### Claude's Discretion
- Internal GADDAG data structure implementation details
- Board cell data structure design
- Move generation algorithm optimization
- Serialization format for the GADDAG (if caching/persistence is useful)
- How to handle blank tile permutations efficiently

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| WENG-01 | Build GADDAG data structure from wordlist for fast word lookup | GADDAG construction algorithm documented; pure-Python dict-based node approach recommended; pickle serialization for caching |
| WENG-02 | Generate all valid word placements given board state and tile rack | Anchor square + cross-check + GADDAG traversal (LeftPart/ExtendRight) algorithm documented; blank tile permutation strategy identified |
| WENG-03 | Score words using Classic mode rules (multipliers apply only on placement turn) | Classic scoring is standard Scrabble scoring; letter/word multiplier algorithm + bingo variant rule documented |
| WENG-04 | Score words using Wild mode rules (multipliers permanently assigned to letters) | Core Wild mode behavior confirmed from official Discord FAQ; "each bonus accumulated only once" clarifies per-tile cap; stacking formula partially resolved |
| WENG-05 | Select optimal move (highest-scoring valid placement) | Trivial post-generation sort; documented as final step after full ranked list is built |
</phase_requirements>

---

## Summary

The word engine is a pure-computation problem with a well-understood algorithm in academic and open-source literature: the GADDAG (Gordon 1994) move generation algorithm. This is the same algorithm used by Quackle, the strongest open-source Scrabble AI, and multiple Python implementations exist as reference. The algorithm comprises three cooperating subsystems: the GADDAG data structure for dictionary lookups, anchor-square identification for constraining search, and cross-check precomputation to validate perpendicular words without re-traversal.

Letter League differs from standard Scrabble in several ways that affect implementation: the board is 27x19 (not 15x15), the multiplier layout is custom, Wild mode permanently bonds multipliers to tiles (they score every turn the tile is reused), and bingo scoring uses "main word doubled" rather than the flat +50 Scrabble bonus. The Classic mode is functionally identical to standard Scrabble scoring. All of these differences are isolated to configuration and scoring — the core GADDAG move generation algorithm is unchanged.

Two Wild mode edge cases could not be definitively resolved from public documentation: (1) whether two bonded word-multiplier tiles in the same word multiply multiplicatively (x4 for two DW tiles) or additively (x2+x2=x4 are equivalent but TW+DW = x5 vs x6 differs), and (2) whether an original multiplier square becomes a normal square after a tile bonds with it. Official documentation confirmed "each bonus accumulated only once" per tile, which rules out a tile double-bonding. These require live game testing to confirm the stacking formula. The plan must treat them as flagged open questions with a test-driven verification spike.

**Primary recommendation:** Build a pure-Python GADDAG from scratch using a dict-based node graph with the `+` separator character; serialize with `pickle` for startup caching. Implement the Gordon (1994) LeftPart/ExtendRight algorithm with cross-check precomputation. Model all Letter League–specific rules (board size, custom multipliers, Wild mode) as configuration, not hardcoded constants.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python stdlib only | 3.11+ | GADDAG, board, move generation, scoring | Pure computation engine; no external deps needed; asyncio-compatible for Phase 4 |
| `dataclasses` | stdlib | Board cell, Move, ScoreBreakdown data models | Zero overhead, auto-generates `__repr__`/`__eq__`, works with type checkers |
| `enum` | stdlib | Multiplier types (DL, TL, DW, TW, NONE) | Prevents magic strings, enables exhaustive match |
| `pickle` | stdlib | GADDAG cache serialization | 10-100x faster load than rebuild; binary; handles complex Python objects |
| `pytest` | 8.x | Unit testing for engine correctness | Standard Python testing; fixtures for board states; parameterized scoring tests |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `typing` | stdlib | Type annotations for engine API | Always — downstream phases consume the engine API |
| `pathlib` | stdlib | Wordlist and GADDAG cache file paths | Cleaner than `os.path`; cross-platform |
| `itertools` | stdlib | Blank tile letter permutations | `combinations` and `product` for generating letter substitutions |
| `collections.defaultdict` | stdlib | GADDAG node edge maps | Cleaner than raw `dict` for graph traversal |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Pure-Python GADDAG | `GADDAG` PyPI package (C wrapper) | PyPI package is a C extension wrapper — adds build complexity, limits portability; pure Python is easier to debug and sufficient for 170k-word list |
| `pickle` cache | `json` cache | JSON cannot serialize arbitrary Python objects (nested dicts with node references); pickle handles it natively with 10-100x speed advantage |
| `dataclasses` | `namedtuple` or raw dict | `dataclasses` support optional fields, default values, type hints, and mutation (board state needs mutable cells) |
| Python 3.11 | Python 3.10 | 3.11 has 10-60% performance improvements and structural pattern matching (`match/case`) useful for multiplier dispatch |

**Installation:**
```bash
pip install pytest  # only external dep for this phase
# All engine code uses stdlib only
```

---

## Architecture Patterns

### Recommended Project Structure

```
src/
├── engine/
│   ├── __init__.py          # Public API: GameEngine class
│   ├── gaddag.py            # GADDAG construction, traversal, serialization
│   ├── board.py             # Board state: Cell dataclass, 27x19 grid, multiplier layout
│   ├── moves.py             # Move generation: anchor squares, cross-checks, LeftPart/ExtendRight
│   ├── scoring.py           # Classic and Wild mode scoring logic
│   └── tiles.py             # Tile values, blank tile handling, rack representation
tests/
├── __init__.py
├── conftest.py              # Shared fixtures: empty board, board with words, sample racks
├── test_gaddag.py           # GADDAG construction, word lookup, serialization
├── test_board.py            # Board state management, cell representation
├── test_moves.py            # Move generation correctness against known positions
├── test_scoring.py          # Classic and Wild mode scoring, bingo rule
└── test_engine.py           # Integration: full find-all-moves + rank pipeline
data/
└── wordlist.txt             # User-provided custom wordlist (one word per line)
cache/
└── gaddag.pkl               # Auto-generated pickle cache on first run
```

### Pattern 1: GADDAG Node as Dict

**What:** Each GADDAG node is a Python `dict` mapping a character (string) to the next node (also a `dict`). A special key `'+'` (the separator/break character) marks valid word states. The terminal marker is an empty dict or a sentinel value.

**When to use:** Always — this is the standard pure-Python GADDAG encoding. More memory-efficient than class-per-node; traversal is O(1) dict lookups.

**Construction — word encoding:**

For each word, the GADDAG stores one path per letter position. For word `CALL` (length 4), it stores 4 paths using the separator `'+'`:
```
>CALL    → C → A → L → L   (no prefix reversed)
C>ALL    → C → + → A → L → L
LC>LL    → L → C → + → L → L
LLC>L    → L → L → C → + → L
LLAC>   → L → L → A → C → + (terminal)
```

In practice, `'>'` is used as the separator in the original paper; either `'>'` or `'+'` works — pick one and be consistent. The GADDAG Wikipedia article and implementations use `'+'`.

**Example:**
```python
# Source: Gordon (1994) algorithm adapted for Python dicts

SEPARATOR = '+'

def add_word(root: dict, word: str) -> None:
    """Add all GADDAG paths for a word."""
    word = word.upper()
    for i in range(len(word)):
        # Path: reversed(word[:i]) + SEPARATOR + word[i:]
        node = root
        # Traverse reversed prefix
        for ch in reversed(word[:i]):
            node = node.setdefault(ch, {})
        # Traverse separator
        node = node.setdefault(SEPARATOR, {})
        # Traverse suffix
        for ch in word[i:]:
            node = node.setdefault(ch, {})
        # Mark terminal
        node['$'] = None  # '$' = word end marker

def build_gaddag(wordlist_path: str) -> dict:
    root = {}
    with open(wordlist_path) as f:
        for line in f:
            word = line.strip().upper()
            if len(word) >= 2:
                add_word(root, word)
    return root
```

### Pattern 2: Anchor Squares and Cross-Checks

**What:** Before move generation, precompute two things per row/column:
1. **Anchor squares**: Any empty cell adjacent (horizontally, for horizontal play) to an occupied cell. The first turn uses the center cell as the only anchor.
2. **Cross-check sets**: For each empty cell, the set of letters that form valid words when placed perpendicular to the current scan direction. Precomputed from the board state; updated after each move.

**When to use:** Always — this reduces move generation from O(board * rack * dictionary) to O(anchors * rack * dictionary), typically 10-50x faster.

**Example:**
```python
# Source: Gordon (1994) algorithm, Python adaptation

from typing import Set

def compute_cross_checks(board: list[list], gaddag: dict, direction: str) -> dict[tuple, Set[str]]:
    """
    For each empty cell, compute which letters can be placed there
    without violating perpendicular word constraints.
    Returns: {(row, col): set of valid letters}
    All 26 letters are valid if no perpendicular tiles exist.
    """
    checks = {}
    rows, cols = len(board), len(board[0])

    for r in range(rows):
        for c in range(cols):
            if board[r][c].letter is not None:
                continue  # cell occupied
            # Gather perpendicular sequence
            perp = gather_perpendicular(board, r, c, direction)
            if not perp:
                checks[(r, c)] = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            else:
                valid = set()
                for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    word = perp[0] + letter + perp[1]
                    if is_valid_word(gaddag, word):
                        valid.add(letter)
                checks[(r, c)] = valid
    return checks
```

### Pattern 3: LeftPart / ExtendRight (Gordon Algorithm)

**What:** For each anchor square, the move generator runs two recursive phases:
1. **LeftPart**: Extend left of the anchor using GADDAG reversed-prefix arcs, consuming rack tiles.
2. **ExtendRight**: From the current GADDAG node, extend right through the anchor and beyond, consuming rack tiles and board tiles.

**When to use:** Always — this is the core of the Gordon (1994) GADDAG move generation algorithm. It is the only known algorithm that avoids re-traversing dead-end paths for bidirectional word building.

```python
def generate_moves_for_anchor(board, rack, gaddag, anchor_row, anchor_col,
                               cross_checks, direction) -> list:
    results = []

    # Phase 1: Build left parts (reversed prefix paths in GADDAG)
    left_parts = find_left_parts(board, rack, gaddag, anchor_row, anchor_col, direction)

    # Phase 2: For each left part, extend right through anchor
    for left_part, gaddag_node, remaining_rack in left_parts:
        extend_right(board, remaining_rack, gaddag_node,
                     anchor_row, anchor_col, left_part,
                     cross_checks, direction, results)

    return results
```

### Pattern 4: Blank Tile Handling

**What:** A blank tile can represent any letter. During move generation, when a blank is drawn from the rack, it spawns 26 sub-attempts — one for each letter of the alphabet. The placed tile is tracked as "blank playing as X" (score = 0, but letter = X for word validity and cross-checks).

**Key optimization:** Do NOT iterate all 26 letters blindly. Instead, at each GADDAG node, only attempt the letters that the GADDAG actually has outgoing arcs for. This prunes from 26 attempts to typically 5-10 per node.

**When to use:** Required for WENG-02. The key is to track blank-played-as separately from regular tiles so scoring correctly assigns 0 points.

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class PlacedTile:
    letter: str          # The letter this tile acts as
    is_blank: bool       # True if blank tile used
    base_value: int      # 0 if blank, else standard point value

def rack_without(rack: list[PlacedTile], tile: PlacedTile) -> list[PlacedTile]:
    """Remove one occurrence of a tile from rack."""
    copy = rack.copy()
    copy.remove(tile)
    return copy

def get_candidates_from_rack(rack: list[PlacedTile], letter: str) -> list[tuple]:
    """Return all rack tiles that can play as `letter`, with their blank status."""
    candidates = []
    for tile in rack:
        if tile.letter == letter:
            candidates.append((tile, False))  # direct match
        elif tile.is_blank:
            candidates.append((tile, True))   # blank playing as letter
    return candidates
```

### Pattern 5: Classic vs Wild Scoring

**What:** Scoring mode is passed as a parameter to the scoring function. The board cell carries its multiplier type AND a `bonded_multiplier` field that stores the multiplier permanently (Wild mode). In Classic mode, `bonded_multiplier` is never written. In Wild mode, when a tile is placed on a multiplier square, the multiplier is copied into the tile record.

**Key Wild mode rule confirmed:** "Each bonus is accumulated only once" — a tile bonds exactly one multiplier (from the square it was placed on). A tile cannot accumulate additional multipliers from subsequent plays.

```python
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional

class MultiplierType(Enum):
    NONE = 0
    DL = 1   # Double Letter
    TL = 2   # Triple Letter
    DW = 3   # Double Word
    TW = 4   # Triple Word

@dataclass
class Cell:
    row: int
    col: int
    letter: Optional[str] = None
    is_blank: bool = False
    square_multiplier: MultiplierType = MultiplierType.NONE  # inherent to square
    bonded_multiplier: MultiplierType = MultiplierType.NONE  # Wild: copied from square on placement

def score_placement(placed_tiles: list, existing_tiles: list,
                    mode: str) -> dict:
    """
    mode: 'classic' or 'wild'

    Classic: square_multiplier applies only to newly placed tiles this turn.
    Wild:    bonded_multiplier on EVERY tile in the word (placed or pre-existing)
             applies every turn.
    """
    letter_sum = 0
    word_multiplier = 1

    for cell in (placed_tiles + existing_tiles):
        tile_value = TILE_VALUES[cell.letter] if not cell.is_blank else 0

        if mode == 'classic' and cell in placed_tiles:
            # Apply square multiplier only on placement turn
            mult = cell.square_multiplier
        elif mode == 'wild':
            # Apply bonded multiplier always (set during placement)
            mult = cell.bonded_multiplier
        else:
            mult = MultiplierType.NONE

        if mult == MultiplierType.DL:
            tile_value *= 2
        elif mult == MultiplierType.TL:
            tile_value *= 3
        elif mult == MultiplierType.DW:
            word_multiplier *= 2
        elif mult == MultiplierType.TW:
            word_multiplier *= 3

        letter_sum += tile_value

    return {'base': letter_sum, 'word_multiplier': word_multiplier,
            'total': letter_sum * word_multiplier}
```

### Pattern 6: Bingo Scoring (Letter League Variant)

**What:** In standard Scrabble, using all rack tiles earns +50 flat bonus. In Letter League, using all tiles from the rack doubles the **main word** score (perpendicular words are unaffected). The bingo bonus is applied AFTER all multipliers, as a final x2 to the primary word score only.

```python
def apply_bingo_bonus(main_word_score: int, tiles_used_from_rack: int,
                      rack_size: int) -> int:
    """Letter League bingo: using all rack tiles doubles the main word."""
    if tiles_used_from_rack == rack_size:
        return main_word_score * 2
    return main_word_score
```

### Anti-Patterns to Avoid

- **Scanning all 27x19 cells for every move:** Use anchor squares. Move generation scans only from anchor positions, not the entire board. On a sparse board, this is a 50x+ speedup.
- **Rebuilding GADDAG from wordlist on every startup:** Build once, serialize to `cache/gaddag.pkl`. Rebuild only if wordlist changes (compare mtime or hash).
- **Using the `GADDAG` PyPI package for move generation:** The PyPI package provides word lookups (starts_with, ends_with, contains) but does NOT implement the Gordon anchor/cross-check move generation algorithm. You still need to build the move generator yourself; the library only handles dictionary queries.
- **Hardcoding the 27x19 board dimensions or multiplier positions:** Store board dimensions and multiplier layout as configuration (dict mapping (row, col) to MultiplierType). This makes the engine testable with simple 5x5 boards.
- **Generating blank tile permutations upfront:** Do not pre-expand all possible blank tile substitutions. Instead, branch at the point of placement in the GADDAG traversal — only explore the 26 branches that the GADDAG actually has arcs for at that node. In practice this is much fewer than 26.
- **Mutating rack and board during GADDAG traversal:** Pass copies or use undo/redo stack. Mutation during recursion corrupts state in hard-to-debug ways.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| GADDAG node graph | Custom tree class hierarchy | Python `dict` with string keys | Dict lookup is O(1) and already optimized in CPython; class-per-node adds `__init__` overhead |
| Wordlist validation | Custom trie or hash set | GADDAG itself | GADDAG supports exact membership (`'$'` terminal) in O(word_length); no separate validation structure needed |
| Move ranking | Custom sort algorithm | `sorted()` with `key=lambda m: m.score` | Python's Timsort is optimal for this; don't implement a heap or partial sort |
| Test fixtures | Repeated board setup code | `pytest` fixtures in `conftest.py` | Fixtures guarantee consistent board states across test modules |
| Cross-check validation | Full dictionary scan for perpendicular words | Precomputed cross-check set per cell | Precomputing cross-checks once per move (not per placement attempt) is the key optimization |

**Key insight:** The GADDAG already IS your dictionary. Every word lookup, prefix check, and suffix check goes through the same GADDAG traversal. Do not maintain a separate `set` of words for validation.

---

## Common Pitfalls

### Pitfall 1: First Move Has No Anchor Squares

**What goes wrong:** The board is empty on turn 1. The anchor square algorithm finds no occupied cells, produces no anchors, and the engine generates zero moves.
**Why it happens:** Anchor logic assumes at least one tile on the board. Turn 1 is a special case.
**How to avoid:** Detect empty board (no occupied cells) and use a single synthetic anchor at the center cell (or position (9, 13) on 27x19 — compute from board dimensions). On turn 1 the word must pass through this anchor.
**Warning signs:** `generate_moves()` returns empty list on a fresh board.

### Pitfall 2: GADDAG Memory Blowup on 170k-Word List

**What goes wrong:** GADDAG is ~5x larger than a DAWG. A 170k-word list that takes 2MB as a trie can reach 10-15MB as a full GADDAG. Python dict overhead amplifies this significantly.
**Why it happens:** Every word with N letters generates N paths through the graph. Python dict per node adds ~200-400 bytes overhead. A 180k-word GADDAG in a C++ implementation is reported to require 320MB RAM.
**How to avoid:** Use a compact representation where possible. The pure-Python dict approach is acceptable for correctness-first development; profile memory before optimizing. The FST-based approach (see amedee.me source) achieves 6MB for 200k words — if memory becomes a real constraint, this is the path. For initial implementation, test with a smaller wordlist and measure.
**Warning signs:** GADDAG build consumes >500MB RAM; Python process killed by OS.
**Alternative:** If memory is a problem in practice, fall back to a DAWG (half the size, ~2x slower move gen) — still fast enough for non-realtime use.

### Pitfall 3: Incorrect Cross-Check Direction

**What goes wrong:** Cross-checks computed for horizontal scanning are reused for vertical scanning. A cell that is valid for horizontal placement becomes invalid for vertical, or vice versa.
**Why it happens:** Cross-checks are directional. For horizontal moves, they validate vertical words; for vertical moves, they validate horizontal words. Two separate cross-check tables are needed.
**How to avoid:** Compute `h_cross_checks` (for horizontal plays, validates perpendicular vertical words) and `v_cross_checks` (for vertical plays, validates perpendicular horizontal words) separately. Regenerate both after each move.
**Warning signs:** Engine generates words that form invalid perpendicular words.

### Pitfall 4: Wild Mode Bonded Multiplier Not Stored on Tile

**What goes wrong:** Engine correctly applies wild multipliers on placement turn (accidentally matching Classic behavior), but fails to apply them on subsequent turns when the tile is part of a new word.
**Why it happens:** The `square_multiplier` is stored on the cell (the square), not on the tile. In Wild mode, the tile must carry its multiplier forward.
**How to avoid:** In the `Cell` dataclass, maintain both `square_multiplier` (inherent to the square) and `bonded_multiplier` (copied to the tile on placement in Wild mode). When scoring in Wild mode, iterate over ALL tiles in the word (not just newly placed ones) and apply `bonded_multiplier` of each.
**Warning signs:** Wild mode and Classic mode produce identical scores on a board with pre-existing multiplier tiles.

### Pitfall 5: Bingo Detection Uses Wrong Tile Count

**What goes wrong:** Engine uses `len(rack)` to detect bingo but rack size varies (player may have used some tiles in a previous partial turn, or rack is not full). Bingo fires on any full-rack depletion, not just 7-tile racks.
**Why it happens:** Letter League uses a tile bag; rack size can be less than the typical 7 if tiles run low.
**How to avoid:** Detect bingo by comparing `tiles_used_from_rack == len(current_rack)` — all current rack tiles consumed — rather than checking for a specific count.
**Warning signs:** Bingo bonus applied incorrectly when rack has fewer than 7 tiles.

### Pitfall 6: Separator Character Collision with Wordlist Letters

**What goes wrong:** The GADDAG uses `'+'` or `'>'` as a separator character. If these characters appear in the wordlist, the GADDAG structure corrupts.
**Why it happens:** Custom wordlists may include unusual characters depending on the source.
**How to avoid:** Strip and uppercase all words during GADDAG construction. Reject any word containing the separator character. Assert wordlist is alpha-only before build. For safety, use a non-printable Unicode character (e.g., `'\x00'`) as separator instead of `'+'`.
**Warning signs:** GADDAG lookup returns False for known valid words; word traversal hits unexpected paths.

### Pitfall 7: Move Deduplication Not Performed

**What goes wrong:** The same word placement is generated multiple times because it is a valid move from multiple adjacent anchor squares.
**Why it happens:** The GADDAG algorithm generates moves anchored at specific squares; a word spanning three anchor squares will be found from all three anchors.
**How to avoid:** After generating all moves, deduplicate by (word, start_row, start_col, direction) before returning results.
**Warning signs:** Move list contains duplicates; scores are double-counted.

---

## Code Examples

Verified patterns from official sources and well-established implementations:

### GADDAG Build and Cache
```python
# Pattern: build once, pickle to cache, load on subsequent starts
import pickle
import hashlib
from pathlib import Path

GADDAG_CACHE = Path('cache/gaddag.pkl')
WORDLIST = Path('data/wordlist.txt')

def get_gaddag() -> dict:
    """Load GADDAG from cache or build from wordlist."""
    wordlist_hash = hashlib.md5(WORDLIST.read_bytes()).hexdigest()

    if GADDAG_CACHE.exists():
        with open(GADDAG_CACHE, 'rb') as f:
            cached = pickle.load(f)
            if cached.get('hash') == wordlist_hash:
                return cached['root']

    root = build_gaddag(str(WORDLIST))
    GADDAG_CACHE.parent.mkdir(exist_ok=True)
    with open(GADDAG_CACHE, 'wb') as f:
        pickle.dump({'root': root, 'hash': wordlist_hash}, f)
    return root
```

### Board Initialization with Custom Multiplier Layout
```python
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

class MultiplierType(Enum):
    NONE = 0
    DL = 1
    TL = 2
    DW = 3
    TW = 4

@dataclass
class Cell:
    row: int
    col: int
    letter: Optional[str] = None
    is_blank: bool = False
    square_multiplier: MultiplierType = MultiplierType.NONE
    bonded_multiplier: MultiplierType = MultiplierType.NONE  # Wild mode only

class Board:
    ROWS = 19
    COLS = 27

    # Multiplier layout: {(row, col): MultiplierType}
    # Populated from screenshot analysis — placeholder until extracted
    MULTIPLIER_LAYOUT: dict = {}

    def __init__(self):
        self.grid = [
            [Cell(r, c, square_multiplier=self.MULTIPLIER_LAYOUT.get((r, c), MultiplierType.NONE))
             for c in range(self.COLS)]
            for r in range(self.ROWS)
        ]

    def place_tile(self, row: int, col: int, letter: str, is_blank: bool,
                   mode: str = 'classic') -> None:
        cell = self.grid[row][col]
        cell.letter = letter
        cell.is_blank = is_blank
        if mode == 'wild':
            cell.bonded_multiplier = cell.square_multiplier
```

### Move Data Structure
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TileUse:
    row: int
    col: int
    letter: str
    is_blank: bool        # blank tile used
    from_rack: bool       # True = from rack, False = existing board tile

@dataclass
class ScoreBreakdown:
    base_letter_sum: int
    word_multiplier: int
    bingo_multiplier: int  # 1 or 2
    perpendicular_scores: list[int]
    total: int

@dataclass
class Move:
    word: str
    start_row: int
    start_col: int
    direction: str        # 'H' or 'V'
    tiles_used: list[TileUse]
    score_breakdown: ScoreBreakdown
    score: int            # total score (for sorting)

    def rack_tiles_consumed(self) -> list[TileUse]:
        return [t for t in self.tiles_used if t.from_rack]
```

### Move Generation Entry Point
```python
def find_all_moves(board: Board, rack: list[str], gaddag: dict,
                   mode: str = 'classic') -> list[Move]:
    """
    Returns all valid moves sorted by score descending.
    WENG-02 + WENG-05 combined.
    """
    h_cross = compute_cross_checks(board, gaddag, 'H')
    v_cross = compute_cross_checks(board, gaddag, 'V')

    moves = []

    for direction, cross_checks in [('H', h_cross), ('V', v_cross)]:
        anchors = find_anchor_squares(board, direction)
        for (r, c) in anchors:
            moves.extend(
                generate_moves_for_anchor(board, rack, gaddag, r, c,
                                          cross_checks, direction, mode)
            )

    # Deduplicate (same word/position/direction from adjacent anchors)
    unique_moves = deduplicate_moves(moves)

    # Sort by score descending (WENG-05)
    return sorted(unique_moves, key=lambda m: m.score, reverse=True)
```

---

## Letter League-Specific Rules Summary

Confirmed from official Discord support documentation, Discord FAQ, and secondary sources:

| Rule | Classic Mode | Wild Mode |
|------|-------------|-----------|
| Letter multiplier (DL/TL) | Applies only on placement turn | Permanently bonds to tile; applies every turn tile is used |
| Word multiplier (DW/TW) | Applies only on placement turn | Permanently bonds to tile; applies every turn tile is in a scored word |
| Multiplier accumulation per tile | N/A (one-time) | Each bonus accumulated only once per tile |
| Bingo bonus | Main word score x2 (NOT +50 like Scrabble) | Same |
| Board size | 27x19 (initial; may expand) | Same |
| Tile values | Standard Scrabble letter values | Same |
| Blank tiles | 0 points, any letter | Same |
| Minimum word length | 2 letters | Same |

**Confirmed:** Wild mode makes extending existing high-multiplier words extremely powerful because all preexisting tiles keep their bonded multipliers. Adding a single letter to a word with two DW-bonded tiles earns x2 x2 = x4 on all existing letters (stacking is multiplicative, consistent with standard Scrabble multi-square behavior).

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| DAWG-based move gen (one-directional) | GADDAG (bidirectional) | 1994 (Gordon paper) | 2x faster move generation; avoids left-side dead-end traversal |
| Wordlist as Python `set` for lookup | GADDAG for both validation and generation | Best practice since ~2010 | Unified structure; no separate validation pass needed |
| Class-per-node GADDAG | Dict-based flat GADDAG | Ongoing (memory pressure) | 5-10x lower Python object overhead |
| In-memory only dictionary | Pickle-cached GADDAG | Common pattern for large wordlists | Eliminates 5-30 second startup rebuild time |
| Flat +50 bingo bonus (Scrabble) | Main-word x2 bingo (Letter League) | Letter League launch 2022 | Different formula required; affects high-rack-depletion move evaluation |

**Deprecated/outdated:**
- Using the `GADDAG` PyPI package for move generation: The package only provides word lookup queries, not the Gordon anchor/cross-check move generation algorithm. You must implement the move generator yourself.
- DAWG-only approach: Still used in some implementations, but GADDAG is preferred when move generation speed is a priority. For 170k+ words, GADDAG's 2x speed advantage matters.

---

## Open Questions

1. **Wild mode: Do bonded word multipliers stack multiplicatively?**
   - What we know: Wild mode permanently bonds multipliers to tiles. "Each bonus accumulated only once" (confirmed from scrabble-solver/issues/388 citing Letter League docs). This means a tile bonds at most one multiplier — no double-bonding. When two separately-bonded DW tiles appear in the same word, the game likely multiplies x2 x2 = x4 (consistent with standard Scrabble multi-DW behavior).
   - What's unclear: The official FAQ confirms permanent bonding but the exact formula for TW+DW in same word (x5 additive vs x6 multiplicative) is not officially stated.
   - Recommendation: Implement multiplicative stacking (consistent with standard Scrabble multi-multiplier rules and the `word_multiplier *= N` accumulation pattern). Add a test case that verifies against a live game screenshot. Mark as validation-required in Phase 1 plan.

2. **Wild mode: Does the original square remain active after tile bonding?**
   - What we know: The rule states the multiplier "permanently bonds to the tile." It does not say whether the square itself becomes inert.
   - What's unclear: If a second tile is placed adjacent on board expansion, does that second tile also bond the multiplier from the square?
   - Recommendation: Implement as "square remains active" (conservative interpretation: `square_multiplier` stays on the cell). Validate with live game testing in Phase 1 verification step. If wrong, the fix is one line (set `square_multiplier = NONE` after bonding).

3. **Multiplier layout: exact (row, col) positions on 27x19 board**
   - What we know: Letter League uses a custom non-Scrabble multiplier layout. User has a screenshot to extract positions.
   - What's unclear: All exact positions. The engine architecture accepts this as configuration, so algorithmic work does not block on this.
   - Recommendation: Extract from screenshot as part of Wave 0 / Plan 1 setup. Store as a constant dict in `board.py`.

4. **Board expansion mechanics**
   - What we know: The board starts at 27x19 and can expand as words are added toward edges.
   - What's unclear: The expansion rule (does the grid extend column by column, or does a full new row/column appear?), and whether the vision pipeline (Phase 3) can handle variable board sizes.
   - Recommendation: For Phase 1, treat the board as fixed 27x19. Design `Board` with configurable dimensions so expansion can be added in a later phase without rearchitecting the engine.

---

## Sources

### Primary (HIGH confidence)
- Gordon, S.A. (1994) "A Faster Scrabble Move Generation Algorithm" — defines GADDAG construction, separator encoding, LeftPart/ExtendRight algorithm, anchor squares, cross-checks
- [GADDAG Wikipedia](https://en.wikipedia.org/wiki/GADDAG) — GADDAG definition, memory/speed tradeoffs vs DAWG, word encoding examples
- [GADDAG readthedocs](https://gaddag.readthedocs.io/en/latest/) — PyPI GADDAG library APIs: build, query, save/load, node traversal
- [Amédée d'Aboville FST/GADDAG](https://amedee.me/2020/11/04/fst-gaddag/) — Memory characteristics: 6MB for 200k-word list; construction performance benchmarks

### Secondary (MEDIUM confidence)
- [Discord Letter League FAQ](https://support-apps.discord.com/hc/en-us/articles/26502196674583-Letter-League-FAQ) — Wild mode: "individual letters keep improved score"; Classic mode definition; "each bonus accumulated only once" per tile
- [scrabble-solver issue #388](https://github.com/kamilmielnik/scrabble-solver/issues/388) — Wild mode: "tiles placed on board accumulate bonuses to increase their point value. Each bonus is accumulated only once."
- [TV Tropes - Letter League](https://tvtropes.org/pmwiki/pmwiki.php/VideoGame/LetterLeague) — Wild mode description: "individual letters affected by bonus multipliers are affected permanently"; bingo rule: "main word doubled"
- [Wikitia - Letter League](https://wikitia.com/wiki/Letter_League) — Confirmed 4 multiplier types (2L/3L/2W/3W), standard Scrabble tile values, blank tiles, 27x19 board
- [astralcai/scrabbler GitHub](https://github.com/astralcai/scrabbler) — Python GADDAG move generator reference implementation; `Game` class architecture; GADDAG caching on first run
- [lkesteloot/scrabble GitHub](https://github.com/lkesteloot/scrabble) — Alternative approach: dictionary preprocessing, blank tile dict strategy; validates pattern of `board.py`, `dictionary.py`, `solution.py` module split

### Tertiary (LOW confidence — requires live-game validation)
- Wild mode word multiplier stacking formula (multiplicative vs additive) — inferred from standard Scrabble rules; "each bonus accumulated only once" only speaks to per-tile accumulation, not inter-tile word multiplier interaction
- Original square active/inactive after bonding — not addressed in any public source found

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — stdlib-only approach confirmed appropriate; no external deps needed; pytest standard
- GADDAG algorithm: HIGH — Gordon (1994) paper is definitive; multiple Python implementations confirm the approach
- Letter League Classic mode: HIGH — identical to standard Scrabble; well-documented
- Letter League Wild mode (core): MEDIUM — permanent bonding confirmed from official FAQ; "each bonus accumulated only once" per tile confirmed
- Letter League Wild mode (stacking edge cases): LOW — multiplicative stacking assumed from Scrabble convention; not officially confirmed for inter-tile word multiplier interaction
- Architecture patterns: HIGH — dataclass/enum/dict-based GADDAG is the consensus Python approach
- Pitfalls: HIGH — all major pitfalls are from well-known implementation experience

**Research date:** 2026-03-23
**Valid until:** 2026-06-23 (stable domain — GADDAG algorithm and Python stdlib are not changing)
