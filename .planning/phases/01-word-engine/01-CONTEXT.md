# Phase 1: Word Engine - Context

**Gathered:** 2026-03-23
**Status:** Ready for planning

<domain>
## Phase Boundary

GADDAG dictionary structure + move generation + Classic/Wild scoring for Letter League. Given any board state and tile rack, the engine finds and ranks all valid word placements with correct scores. This is a pure computation engine with no I/O — downstream phases consume its API.

</domain>

<decisions>
## Implementation Decisions

### Game Rules & Board
- Board size is 27x19 (non-standard — unique to Letter League)
- Standard Scrabble tile point values (A=1, B=3, Z=10, blank=0, etc.)
- Custom multiplier layout — NOT standard Scrabble positions. User has a screenshot to extract exact positions during research phase
- Blank/wild tiles exist, worth 0 points, can represent any letter (like Scrabble)
- Minimum word length is 2 letters

### Wordlist & Validation
- Custom text file, one word per line (user will provide)
- Apply game rules filtering on top of wordlist (minimum 2-letter words)
- Wordlist is the primary source of truth, but game-specific rules also enforced

### Move Output
- Return ALL valid placements, ranked by score (not just the best move)
- Each move includes: word, starting position (row, col), direction (horizontal/vertical)
- Each move includes: score breakdown (base letter values, multiplier bonuses, total)
- Each move includes: which tiles from the rack are consumed
- Board input represented as 2D array of cells (each cell: letter or empty + multiplier type)
- Rack input as separate array

### Engine API
- Stateful game object that tracks the board state across turns
- Rack-only mode — engine works with whatever rack is provided, does not manage tile bag
- No tile drawing — tile management is external to the engine

### Classic Mode Scoring
- Multiplier squares apply only on the turn a tile is placed on them
- After placement turn, the square's multiplier no longer affects scoring

### Wild Mode Scoring
- ALL multipliers (letter DL/TL and word DW/TW) permanently bond to the tile placed on them
- Once bonded, the multiplier applies every turn that tile is part of a scoring word
- **Research needed:** How do bonded word multipliers stack when multiple bonded tiles are in one word? (e.g., two DW-bonded tiles → x4?)
- **Research needed:** After a tile bonds a multiplier, does the original square remain active for future tiles or become a normal square?

### Claude's Discretion
- Internal GADDAG data structure implementation details
- Board cell data structure design
- Move generation algorithm optimization
- Serialization format for the GADDAG (if caching/persistence is useful)
- How to handle blank tile permutations efficiently

</decisions>

<specifics>
## Specific Ideas

- User will provide a screenshot of the board for extracting the exact multiplier layout during the research phase
- The wordlist file will be provided as a custom .txt file (not from Wordnik API or standard tournament lists)
- Engine must support both Classic and Wild scoring modes on the same board state

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 01-word-engine*
*Context gathered: 2026-03-23*
