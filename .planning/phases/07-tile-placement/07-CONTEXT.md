# Phase 7: Tile Placement - Context

**Gathered:** 2026-03-26
**Status:** Ready for planning

<domain>
## Phase Boundary

Translate a chosen word move into a sequence of pixel-level interactions that place tiles from the rack onto the board and submit the play. This phase covers coordinate calibration, drag-and-drop execution, placement verification, and play confirmation. It does NOT cover move selection (Phase 2), board reading (Phase 3), turn detection (Phase 6), or the autonomous game loop (Phase 8).

</domain>

<decisions>
## Implementation Decisions

### Calibration approach
- Vision-driven: use the existing vision pipeline output to compute click targets dynamically each turn
- Recalculate coordinate mapping every turn from a fresh screenshot (no caching)
- Coordinates must be fractional/relative to canvas bounding box, not absolute pixels — the canvas can resize
- Claude to investigate whether existing vision output includes pixel bounding boxes or only grid indices; if only indices, compute click coordinates from canvas bbox + grid math

### Click sequencing
- Drag-and-drop interaction: click-hold on rack tile, drag to board cell, release
- Place tiles in word-spelling order (left-to-right for horizontal, top-to-bottom for vertical)
- When duplicate letters exist in rack, always grab the leftmost available matching tile
- Verify placement after each tile: take a quick screenshot to confirm tile landed, retry once if not

### Confirmation flow
- After all tiles placed, click the confirm/submit button
- Detect acceptance vs rejection via screenshot + vision check (tiles stuck on board, score updated)
- On rejection: clear tiles, try next highest-scoring word from move generator
- Up to 3 retry attempts with different words before falling back to tile swap
- Claude to investigate what the confirm button looks like and where it appears during research

### Click timing & human-likeness
- Random 1-3 second delay between individual tile placements (drag actions)
- Smooth mouse path simulation for drag-and-drop (rack to board arc)
- Teleport (instant move) for non-drag clicks (confirm button, etc.)
- Slight random jitter on click coordinates: +/-2-5px from cell center
- Wait 1-2 seconds after clicking confirm before taking verification screenshot

### Claude's Discretion
- Exact smooth mouse path algorithm (bezier curve, linear interpolation, etc.)
- How to clear tiles after a rejection (undo button, drag back, etc.)
- Tile swap mechanics implementation
- Error handling for unexpected UI states

</decisions>

<specifics>
## Specific Ideas

- The 1-3 second delay between actions aligns with Phase 8's spec for human-like pacing — keep consistent
- Verification after each tile drag is preferred over batch verification for reliability
- The game runs inside a Discord Activity iframe — all coordinates are relative to that canvas

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope

</deferred>

---

*Phase: 07-tile-placement*
*Context gathered: 2026-03-26*
