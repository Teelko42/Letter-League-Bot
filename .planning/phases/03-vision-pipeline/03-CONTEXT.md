# Phase 3: Vision Pipeline - Context

**Gathered:** 2026-03-24
**Status:** Ready for planning

<domain>
## Phase Boundary

Extract a complete, validated board state from a Letter League screenshot using Claude Vision API. The bot receives a screenshot of a 19-row x 27-column Letter League board, preprocesses it, sends it to Claude Vision, and returns a structured board state that passes engine validation. Image input and board output — no game interaction, no move generation, no Discord integration.

</domain>

<decisions>
## Implementation Decisions

### Vision prompt design
- Single API call extracts board tiles, tile rack, and multipliers together (not separate calls)
- Prompt instructs Claude to return structured JSON matching a defined schema (not natural language)
- Prompt explicitly states the board is 19 rows x 27 columns to anchor extraction
- Text-only prompt — no reference images or diagrams sent alongside the screenshot

### Board data format
- Vision output maps directly to the existing Board/Cell class structure (no intermediate representation)
- Return a bounding rectangle of the occupied area, not the full 19x27 grid and not a sparse list
- Tile rack included as a separate top-level field in the same JSON response: `{"board": {...}, "rack": [...]}`

### Image preprocessing
- Auto-detect the board region in screenshots (edge detection / color patterns), not hardcoded crop coordinates
- 2x upscale after cropping for improved letter readability
- Single crop region that includes both the board and the tile rack below it
- No color or contrast adjustments — send the cropped/upscaled image as-is

### Validation & error handling
- On validation failure: retry once, feeding validation errors back to Claude Vision with the same image
- Four validation checks must pass before acceptance:
  1. All extracted letters exist in Letter League's tile set (A-Z valid characters only)
  2. All placed tiles form connected words (no floating tiles) — uses engine cross-check logic
  3. Multiplier positions (DL/TL/DW/TW) match the known official board layout
  4. Rack contains a valid number of tiles (7 or fewer)
- Unrecognizable screenshots (wrong app, blurry, not a game) return a typed error: `{error: 'INVALID_SCREENSHOT', message: '...'}`
- Pass/fail validation only — no per-cell confidence scores

### Claude's Discretion
- Board region auto-detection algorithm choice
- Upscaling algorithm (bicubic, lanczos, etc.)
- Exact JSON schema field names and nesting
- How to detect "not a Letter League screenshot" before extraction
- Retry prompt wording

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

*Phase: 03-vision-pipeline*
*Context gathered: 2026-03-24*
