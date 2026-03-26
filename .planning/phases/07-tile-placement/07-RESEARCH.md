# Phase 7: Tile Placement - Research

**Researched:** 2026-03-26
**Domain:** Playwright mouse automation, canvas coordinate mapping, drag-and-drop interaction, play confirmation via screenshot
**Confidence:** HIGH (Playwright mouse API, coordinate math, project architecture) / MEDIUM (exact fractional constants — require live calibration)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Calibration approach**
- Vision-driven: use the existing vision pipeline output to compute click targets dynamically each turn
- Recalculate coordinate mapping every turn from a fresh screenshot (no caching)
- Coordinates must be fractional/relative to canvas bounding box, not absolute pixels — the canvas can resize
- Claude to investigate whether existing vision output includes pixel bounding boxes or only grid indices; if only indices, compute click coordinates from canvas bbox + grid math

**Click sequencing**
- Drag-and-drop interaction: click-hold on rack tile, drag to board cell, release
- Place tiles in word-spelling order (left-to-right for horizontal, top-to-bottom for vertical)
- When duplicate letters exist in rack, always grab the leftmost available matching tile
- Verify placement after each tile: take a quick screenshot to confirm tile landed, retry once if not

**Confirmation flow**
- After all tiles placed, click the confirm/submit button
- Detect acceptance vs rejection via screenshot + vision check (tiles stuck on board, score updated)
- On rejection: clear tiles, try next highest-scoring word from move generator
- Up to 3 retry attempts with different words before falling back to tile swap
- Claude to investigate what the confirm button looks like and where it appears during research

**Click timing & human-likeness**
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

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| TILE-01 | Bot computes pixel coordinates for board cells and rack tiles from canvas bounding box | `canvas.bounding_box()` returns live `{x, y, width, height}`; fractional offset constants map grid indices to pixel coords; board is 19 rows × 27 cols with fixed multiplier layout known from `schema.py` |
| TILE-02 | Bot clicks rack tiles and board cells to place a chosen word move | `page.mouse.down()` + `page.mouse.move(steps=N)` + `page.mouse.up()` drag sequence; rack tile selection by index with leftmost-duplicate rule; `Move.rack_tiles_consumed()` already provides the tile list |
| TILE-03 | Bot confirms word placement via the game's UI confirmation mechanism | Screenshot-based state check after confirm click; `classify_frame()` from Phase 6 can detect board change; retry loop with next-best word on rejection |
</phase_requirements>

---

## Summary

Phase 7 builds `src/browser/tile_placer.py` — the module that translates a `Move` object from the engine into a sequence of patchright mouse interactions that place tiles on the canvas and submit the play. The phase is pure Playwright automation on top of a canvas element with no DOM backing.

The core technical problem is coordinate mapping: the canvas renders the 19×27 board grid and the 7-tile rack at fractional positions that must be derived from the live canvas bounding box. Vision output gives only grid indices (row/col) — no pixel bounding boxes. The planner must budget for a calibration task (Wave 1 or early Wave 2) where fractional constants for the grid origin, cell size, rack row position, and rack tile spacing are measured from a live game screenshot and hardcoded as named constants. The architecture research (ARCHITECTURE.md) already contains placeholder values for these constants; Phase 7 must replace placeholders with calibrated values.

Drag-and-drop is the correct interaction model for tile placement. The Playwright `page.mouse.down()` + `page.mouse.move(steps=N)` + `page.mouse.up()` sequence is confirmed to work on canvas elements. The `locator.drag_to()` convenience method requires two DOM locators with distinct elements — it is not usable for canvas coordinate-to-coordinate drags. The `mouse.*` low-level API is the right tool.

Play confirmation and rejection detection are the second major concern. The confirm button is a UI element that appears after tiles are placed. Since its exact visual appearance and position are not yet empirically known, the plan must include a calibration step using debug screenshots. Post-confirm state validation reuses the existing `classify_frame()` from Phase 6 plus a simple pixel-diff check between pre/post-confirm screenshots.

**Primary recommendation:** Two-wave structure — Wave 1 calibrates constants and builds core drag logic; Wave 2 adds confirmation, placement verification, and retry/rejection handling. All coordinate constants must be derived from live game screenshots, not assumed.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| patchright | 1.58.2 | `page.mouse.down/move/up` for drag-and-drop on canvas; `canvas.bounding_box()` for live coordinate base | Already the project browser backend; all Playwright mouse APIs available unchanged |
| opencv-python | 4.13.0.92 | Decode screenshot bytes for post-placement verification pixel diff | Already installed; same pattern as turn_detector.py |
| numpy | 2.2.6 | `np.std()` / `np.abs(arr1 - arr2).mean()` for pixel comparison in placement verification | Already installed; transitive from opencv |
| asyncio | stdlib | `asyncio.sleep(random.uniform(a, b))` for human-like timing delays between drags | stdlib; already used throughout src/browser/ |
| random | stdlib | `random.uniform()` for jitter, `random.randint()` for delay range | stdlib |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| loguru | 0.7.3 | Debug logging of coordinates, placement attempts, verification outcomes | Already used in all browser modules; same logging pattern |

### No New Installs Required

All libraries are already present in the project. Phase 7 adds zero new dependencies.

---

## Architecture Patterns

### Recommended Project Structure

```
src/browser/
├── tile_placer.py          # NEW — phase 7 deliverable
│                           #   CoordMapper: fractional constants + bounding_box math
│                           #   TilePlacer: drag sequence, placement verify, confirm
├── session.py              # Unchanged
├── capture.py              # Unchanged (capture_canvas reused)
├── navigator.py            # Unchanged
├── turn_detector.py        # Unchanged
└── __init__.py             # Modified: add TilePlacer export

scripts/
├── calibrate_placement.py  # NEW — manual calibration tool (Wave 1)
│                           #   loads a live screenshot, lets user click 4 reference
│                           #   cells, computes fractional constants
└── ...                     # Existing scripts unchanged
```

### Pattern 1: Canvas Bounding Box Coordinate Mapping

**What:** Get the canvas element's live screen position at click time via `canvas.bounding_box()`, then compute pixel positions as fractional offsets. All fractional constants are named module-level constants, calibrated once from real screenshots.

**When to use:** Every drag and every click in this phase. Never hardcode absolute pixel coordinates.

**Key finding:** `canvas.bounding_box()` returns coordinates relative to the viewport (not relative to the page origin). This means the returned `x`, `y` are already what `page.mouse.*` expects — no additional offset math needed.

```python
# Source: Playwright official docs — class-locator#locator-bounding-box
# Returns: {"x": float, "y": float, "width": float, "height": float} or None

async def get_canvas_bbox(page):
    bbox = await page.locator('iframe[src*="discordsays.com"]').locator("canvas").bounding_box()
    # bbox["x"], bbox["y"] are viewport-relative — used directly with page.mouse.*
    return bbox

def board_cell_px(bbox, row: int, col: int) -> tuple[float, float]:
    """Convert grid index to absolute viewport pixel coordinate."""
    x = bbox["x"] + (GRID_X0_FRAC + col * CELL_W_FRAC) * bbox["width"]
    y = bbox["y"] + (GRID_Y0_FRAC + row * CELL_H_FRAC) * bbox["height"]
    return x, y

def rack_tile_px(bbox, tile_index: int) -> tuple[float, float]:
    """Convert rack slot index to absolute viewport pixel coordinate."""
    x = bbox["x"] + (RACK_X0_FRAC + tile_index * RACK_TILE_STEP_FRAC) * bbox["width"]
    y = bbox["y"] + RACK_Y_FRAC * bbox["height"]
    return x, y
```

**Placeholder constants from ARCHITECTURE.md (must be calibrated in Wave 1):**

```python
# All fractions are relative to canvas width or height.
# Canvas observed dimensions: ~1004x632 (from debug screenshots).
# Board is 19 rows × 27 cols. Rack is 7 tiles in a row near bottom.

GRID_X0_FRAC = 0.03     # left edge of board grid as fraction of canvas width
GRID_Y0_FRAC = 0.02     # top edge of board grid as fraction of canvas height
CELL_W_FRAC = 0.034     # one board cell width as fraction of canvas width
CELL_H_FRAC = 0.049     # one board cell height as fraction of canvas height

RACK_Y_FRAC = 0.92      # rack row vertical center as fraction of canvas height
RACK_X0_FRAC = 0.15     # first rack tile horizontal center as fraction of canvas width
RACK_TILE_STEP_FRAC = 0.035  # horizontal distance between rack tile centers (fraction)
```

**Cross-check against known canvas dimensions:**
- Canvas ~1004px wide: cell_w ≈ 1004 × 0.034 = 34.1px — reasonable for 27 cols
- Canvas ~632px tall: cell_h ≈ 632 × 0.049 = 31.0px — reasonable for 19 rows
- Grid full width: 27 × 34.1 = 921px, leaving ~83px margin — plausible
- Grid full height: 19 × 31.0 = 589px, leaving ~43px for rack area below — plausible

These numbers are in the right ballpark but must be confirmed from live game screenshots.

---

### Pattern 2: Drag-and-Drop via Low-Level Mouse API

**What:** Use `page.mouse.move()` → `page.mouse.down()` → `page.mouse.move(steps=N)` → `page.mouse.up()` for each tile drag. This is the canonical pattern for canvas drag interactions in Playwright.

**Why not `locator.drag_to()`:** `drag_to()` requires two distinct element locators. For canvas-to-canvas coordinate drags, there are no DOM elements at the source/target positions — only pixel coordinates. `drag_to()` is not applicable here.

**When to use:** Every rack-tile-to-board-cell placement in this phase.

```python
# Source: Playwright official docs — class-mouse
# Confirmed pattern for canvas drag via mouse API

import asyncio
import random

async def drag_tile(page, from_x, from_y, to_x, to_y, steps: int = 10):
    """Drag from (from_x, from_y) to (to_x, to_y) with smooth interpolated motion.

    steps=10 generates 10 intermediate mousemove events — smooth enough to
    trigger canvas drag handlers without being unrealistically instant.
    """
    await page.mouse.move(from_x, from_y)
    await page.mouse.down()
    await asyncio.sleep(0.05)  # brief pause after mousedown, before moving
    await page.mouse.move(to_x, to_y, steps=steps)
    await page.mouse.up()
```

**Human-likeness:** The CONTEXT.md requires random 1-3 second delays between tile placements and +/-2-5px jitter on coordinates. These are layered on top of the drag function:

```python
import random

def jitter(x: float, y: float, px: int = 3) -> tuple[float, float]:
    """Add uniform random jitter within +/-px pixels to both coordinates."""
    return x + random.uniform(-px, px), y + random.uniform(-px, px)

# Between each tile drag:
await asyncio.sleep(random.uniform(1.0, 3.0))
```

**Bezier curve option (Claude's Discretion):** For even smoother "human-arc" paths, intermediate waypoints can be computed using a quadratic Bézier with a random control point above the straight-line path. The `steps` parameter alone is sufficient for the bot detection level we face (headed patchright already patches CDP leaks), so a simple multi-step linear drag is the recommended starting point. Bezier is available as an upgrade if testing shows it's needed.

```python
import math

def bezier_midpoint(x0, y0, x1, y1, arc_height_px: float = 40) -> tuple[float, float]:
    """Return a control point above the straight path for a slight arc."""
    mx = (x0 + x1) / 2 + random.uniform(-10, 10)
    my = (y0 + y1) / 2 - arc_height_px  # arc upward
    return mx, my

async def drag_tile_arc(page, from_x, from_y, to_x, to_y, steps: int = 15):
    """Drag via a slight arc through a Bezier midpoint."""
    cx, cy = bezier_midpoint(from_x, from_y, to_x, to_y)
    await page.mouse.move(from_x, from_y)
    await page.mouse.down()
    await asyncio.sleep(0.05)
    # Interpolate through midpoint manually
    for i in range(1, steps + 1):
        t = i / steps
        # Quadratic Bezier: B(t) = (1-t)²P0 + 2(1-t)tP1 + t²P2
        bx = (1-t)**2 * from_x + 2*(1-t)*t * cx + t**2 * to_x
        by = (1-t)**2 * from_y + 2*(1-t)*t * cy + t**2 * to_y
        await page.mouse.move(bx, by)
    await page.mouse.up()
```

---

### Pattern 3: Rack Tile Selection with Leftmost-Duplicate Rule

**What:** The vision pipeline returns the rack as `list[str]` (e.g. `['A', 'B', 'A', 'C', 'D', 'E', 'F']`). The engine returns a `Move` with `rack_tiles_consumed()` returning the subset of tiles placed from the rack. To map each consumed tile to a rack slot index, iterate left-to-right and consume each matching letter once.

**Why it matters:** If the rack has two 'A' tiles, always pick index 0 first (leftmost), then index 1 on the second use. This ensures the consumed-tile list is consistent with the rack as rendered.

```python
def assign_rack_indices(rack: list[str], rack_tiles: list[TileUse]) -> list[int]:
    """Map each rack TileUse to the leftmost available rack slot index.

    Args:
        rack: Full rack as returned by extract_board_state (e.g. ['A','B','A',...]).
        rack_tiles: Tiles to place from the rack (from Move.rack_tiles_consumed()).

    Returns:
        List of rack slot indices, one per rack_tile, in placement order.

    Note: Blank tiles in the rack are stored as '?' in the vision output.
          TileUse.is_blank=True means the tile is a blank playing as a letter.
    """
    available = list(enumerate(rack))  # [(0,'A'), (1,'B'), ...]
    result = []
    for tile in rack_tiles:
        letter = '?' if tile.is_blank else tile.letter
        # Find leftmost matching slot
        for i, (slot_idx, slot_letter) in enumerate(available):
            if slot_letter == letter:
                result.append(slot_idx)
                available.pop(i)
                break
        else:
            raise ValueError(f"Tile '{letter}' not found in remaining rack {[s for _,s in available]}")
    return result
```

**Important finding:** Vision output stores rack letters as uppercase strings; blanks are '?' in the rack list. `TileUse.is_blank=True` means the blank is playing as `tile.letter`. The matching must look for '?' in the rack when `tile.is_blank=True`.

---

### Pattern 4: Placement Verification via Screenshot Pixel Diff

**What:** After each tile drag, capture a new screenshot and compare it to the pre-drag screenshot. If the canvas changed (tile landed), proceed. If not, retry the drag once.

**Why per-tile:** The CONTEXT.md requires per-tile verification rather than batch verification for reliability. A failed drag is detectable immediately rather than after all tiles are placed.

```python
async def verify_placement(page, before_bytes: bytes) -> bool:
    """Return True if canvas changed after a tile drag (tile landed).

    Uses mean absolute pixel difference between before and after screenshots.
    Any visible change (tile appearing on board) will exceed the threshold.
    """
    after_bytes = await capture_canvas(page)
    before_arr = cv2.imdecode(np.frombuffer(before_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    after_arr = cv2.imdecode(np.frombuffer(after_bytes, dtype=np.uint8), cv2.IMREAD_COLOR)
    if before_arr is None or after_arr is None:
        return False
    if before_arr.shape != after_arr.shape:
        return True  # shape change = something happened
    diff = float(np.abs(before_arr.astype(int) - after_arr.astype(int)).mean())
    return diff > 1.0  # threshold: 1.0 mean pixel change is easily exceeded by a tile appearing
```

---

### Pattern 5: Play Confirmation — Unknown Visual (Requires Calibration)

**What:** After all tiles are placed, a confirm/submit button appears. Its exact appearance and position are NOT yet known empirically — this is explicitly flagged in STATE.md as a blocker: "Phase 7: Tile placement fractional constants in ARCHITECTURE.md are placeholders — must be measured from live game screenshots."

**What is known from the project context:**
- The game runs inside a Discord Activity iframe (discordsays.com)
- The game is canvas-rendered with no DOM backing for game elements
- The confirm button is likely a canvas-drawn UI element (not a DOM button)
- Based on typical Letter League gameplay observation, the confirm button appears in the lower portion of the canvas after tiles are placed

**Research finding — two possible approaches:**

**Approach A: Fixed fractional coordinate (after calibration)**
If the confirm button appears at a consistent canvas position, store its fractional coordinates and click directly.

```python
CONFIRM_X_FRAC = 0.87  # PLACEHOLDER — calibrate from live screenshot
CONFIRM_Y_FRAC = 0.95  # PLACEHOLDER — calibrate from live screenshot

async def click_confirm(page, bbox: dict) -> None:
    x = bbox["x"] + CONFIRM_X_FRAC * bbox["width"]
    y = bbox["y"] + CONFIRM_Y_FRAC * bbox["height"]
    await page.mouse.click(x, y)
```

**Approach B: HSV detection for confirm button region**
If the confirm button has a distinct color (green checkmark is common in word games), use a small ROI HSV check similar to the turn detector banner check to locate it before clicking.

**Recommendation (Claude's Discretion):** Start with Approach A after calibrating coordinates from a live screenshot. Approach B adds complexity and the same calibration step is needed regardless. If the button position is not fixed, upgrade to Approach B in a follow-up.

---

### Pattern 6: Post-Confirm Acceptance/Rejection Detection

**What:** After clicking confirm and waiting 1-2 seconds, take a screenshot and determine whether the word was accepted (tiles stay on board, score increments) or rejected (tiles snap back to rack, word invalid).

**Detection strategy:**
1. **Score increment check:** Take two screenshots with 1s between them. If the score display changed, acceptance is confirmed.
2. **Board state check:** Re-run `classify_frame()` — if the turn state transitioned to `not_my_turn`, the word was accepted and the turn is over.
3. **Tile-on-board check:** Quick pixel diff between the pre-placement screenshot and the post-confirm screenshot. Accepted play = board changed. Rejected play = board may look similar to pre-placement state.

The simplest reliable check: after 1-2 second wait, if `classify_frame()` returns `not_my_turn` (or `game_over`), the word was accepted and our turn ended. If it still returns `my_turn`, the play was rejected and we must try the next word.

```python
import asyncio
from src.browser.turn_detector import classify_frame

async def wait_for_acceptance(page, timeout_s: float = 5.0) -> bool:
    """Return True if the play was accepted (turn ended), False if rejected."""
    await asyncio.sleep(random.uniform(1.0, 2.0))  # per CONTEXT.md timing spec
    screenshot = await capture_canvas(page)
    state = classify_frame(screenshot)
    return state != "my_turn"
```

---

### Pattern 7: Rejection Recovery — Clear and Try Next Word

**What:** On rejection, tiles must be cleared from the board before attempting the next word. The approach for clearing is Claude's Discretion.

**Options for clearing:**
1. **Undo button/shortcut:** Most word games have an undo or recall button that returns placed tiles to the rack. If Letter League has this, it is the cleanest approach — one click clears all placed tiles.
2. **Drag each tile back to rack:** Requires knowing which tiles are now on the board and where. Complex and error-prone.
3. **Keyboard shortcut (e.g., Escape):** Some games support this for clearing uncommitted tiles.

**Recommendation:** During the calibration task (Wave 1), explicitly look for a "recall" or "clear" button in the game UI when tiles are placed but not yet confirmed. This is the highest-uncertainty element in the rejection recovery flow. Use Approach 1 (undo/recall button) if found; document as a required finding in Wave 1.

---

### Anti-Patterns to Avoid

- **Hardcoding absolute pixel coordinates:** Canvas position shifts with browser window position, Discord sidebar state, and screen DPI. All coordinates MUST be computed from `canvas.bounding_box()` at runtime.

- **Using `locator.drag_to()` for canvas clicks:** Requires two DOM locators; canvas tiles have no DOM representation. Use `page.mouse.*` directly.

- **Running Playwright calls inside `asyncio.to_thread()`:** Playwright is single-threaded by design. All `page.mouse.*` calls must stay on the asyncio event loop, never in a thread. (Pattern confirmed HIGH in ARCHITECTURE.md.)

- **Caching bounding box across turns:** The CONTEXT.md locks "recalculate coordinate mapping every turn from a fresh screenshot." Never cache bbox between turns — always call `canvas.bounding_box()` fresh.

- **Verifying only after all tiles placed:** The CONTEXT.md requires per-tile verification. Catching a failed drag early prevents a cascade of misplaced tiles.

- **Calling `page.mouse.move()` before `page.mouse.down()`:** The mousedown must happen at the source position. Move to source, then down, then drag. Moving after down is the drag. Reversing this sequence fails to initiate a drag.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Smooth mouse movement | Custom interpolation loop | `page.mouse.move(x, y, steps=N)` | Playwright's `steps` parameter generates N intermediate mousemove events natively — no loop needed |
| Canvas screenshot capture | New screenshot logic | `capture_canvas(page)` from `src/browser/capture.py` | Already built in Phase 5 with blank detection and retry |
| Turn state detection for rejection | New vision check | `classify_frame(img_bytes)` from `src/browser/turn_detector.py` | Already calibrated in Phase 6 — reuse directly |
| Coordinate math from bounding box | Custom geometry module | Inline fractional constant math (Pattern 1) | 4 lines of arithmetic — no abstraction needed |

**Key insight:** Phases 5 and 6 built all the capture and classification primitives this phase needs. Phase 7 is pure coordination logic — drag orchestration, coordinate mapping, and retry handling.

---

## Common Pitfalls

### Pitfall 1: Incorrect Canvas Locator Scope

**What goes wrong:** `page.locator("canvas")` finds the canvas in the main page context, not inside the Activity iframe. Clicks land in the wrong place or throw a timeout.

**Why it happens:** The Letter League canvas is inside a `discordsays.com` iframe nested inside the Discord page. The `page.locator()` API traverses only the main frame by default.

**How to avoid:** Always reach the canvas through the iframe chain:
```python
canvas = page.locator('iframe[src*="discordsays.com"]').content_frame.locator("canvas").first
bbox = await canvas.bounding_box()
# Use page.mouse.* with bbox coordinates — bbox is already viewport-relative
```

**Warning signs:** `bounding_box()` returns None, or coordinates produce clicks in wrong UI areas.

**Note on capture.py precedent:** The existing `capture_canvas()` in Phase 5 uses `iframe_locator = page.locator('iframe[src*="discordsays.com"]')` and calls `iframe_locator.screenshot()` (not `canvas.screenshot()`). The tile placer may need to use `iframe_locator.content_frame.locator("canvas")` to get the actual canvas element for `bounding_box()`. This requires live validation during calibration.

---

### Pitfall 2: Blank Tile Letter Mismatch

**What goes wrong:** Rack contains '?' (blank tile). Engine assigns it a letter (e.g., 'E'). The rack-to-slot mapping looks for 'E' in the rack and fails because it's stored as '?'.

**Why it happens:** Vision pipeline stores blanks as '?' in the rack list. TileUse records `is_blank=True` and `letter='E'` (the assigned letter). Without special handling, the lookup fails.

**How to avoid:** In `assign_rack_indices()`, when `tile.is_blank=True`, search for '?' in the rack (not `tile.letter`).

---

### Pitfall 3: Tile Index Drift After Each Drag

**What goes wrong:** After dragging rack tile at slot index 2 to the board, the remaining rack tiles visually shift. The next drag targets the old slot-2 coordinates, which now holds a different tile.

**Why it happens:** Some games shift rack tiles to fill the gap after each tile is removed. Others leave the slot empty. If the game fills gaps, slot indices must be updated after each drag.

**How to avoid:** During calibration, observe whether the rack shifts after a tile is dragged out. Two strategies:
- If rack DOES shift: track which indices have been consumed and recompute remaining slots
- If rack does NOT shift: use the original slot index — the gap stays empty and slot N-of-7 always maps to the same pixel (safest assumption to start with)

**Recommendation:** Assume slots do NOT shift (tiles leave a visible gap) for Wave 1. Calibration will confirm or refute this assumption.

---

### Pitfall 4: Bounding Box Returns None

**What goes wrong:** `canvas.bounding_box()` returns None when the canvas is not visible or not in the DOM.

**Why it happens:** If the Activity iframe is not fully loaded, the canvas element may not yet be rendered.

**How to avoid:** Assert bbox is not None before computing coordinates; raise `PlacementError` with a clear message rather than crashing with `NoneType` arithmetic.

```python
bbox = await canvas.bounding_box()
if bbox is None:
    raise PlacementError("Canvas bounding box is None — Activity not fully loaded")
```

---

### Pitfall 5: Post-Confirmation Race Condition

**What goes wrong:** The acceptance check fires too quickly after the confirm click, before the game UI has finished animating the confirmation result.

**Why it happens:** Canvas-rendered animations may take 500ms-1s before the turn indicator updates.

**How to avoid:** Per CONTEXT.md: wait 1-2 seconds after clicking confirm before taking the verification screenshot. This matches the observed game animation timing.

---

## Code Examples

### Full Tile Placement Sequence (Pseudocode)

```python
# Source: derived from ARCHITECTURE.md Pattern 5, Playwright mouse docs
# Full placement sequence for one word move

async def place_move(page, move: Move, rack: list[str]) -> bool:
    """Place all tiles in move and confirm. Returns True if accepted."""
    # 1. Get live canvas bounding box
    canvas = page.locator('iframe[src*="discordsays.com"]').content_frame.locator("canvas").first
    bbox = await canvas.bounding_box()
    if bbox is None:
        raise PlacementError("Canvas not accessible")

    # 2. Map rack tiles to slot indices
    rack_tiles = move.rack_tiles_consumed()
    slot_indices = assign_rack_indices(rack, rack_tiles)

    # 3. Determine placement order (word-spelling order)
    ordered_placements = sorted(
        zip(rack_tiles, slot_indices),
        key=lambda x: (x[0].col if move.direction == 'H' else x[0].row)
    )

    # 4. Drag each tile
    for tile_use, slot_idx in ordered_placements:
        # Compute source (rack) and target (board) coordinates with jitter
        rx, ry = jitter(*rack_tile_px(bbox, slot_idx))
        bx, by = jitter(*board_cell_px(bbox, tile_use.row, tile_use.col))

        # Capture before-screenshot for placement verification
        before_bytes = await capture_canvas(page)

        # Drag tile to board cell
        await drag_tile(page, rx, ry, bx, by)

        # Verify placement
        placed = await verify_placement(page, before_bytes)
        if not placed:
            # Retry once
            before_bytes = await capture_canvas(page)
            await drag_tile(page, rx, ry, bx, by)
            if not await verify_placement(page, before_bytes):
                raise PlacementError(f"Tile {tile_use.letter} failed to place at ({tile_use.row},{tile_use.col})")

        # Human-like delay between tile placements
        await asyncio.sleep(random.uniform(1.0, 3.0))

    # 5. Click confirm button
    cx, cy = jitter(
        bbox["x"] + CONFIRM_X_FRAC * bbox["width"],
        bbox["y"] + CONFIRM_Y_FRAC * bbox["height"],
        px=3
    )
    await page.mouse.click(cx, cy)

    # 6. Wait and check acceptance
    return await wait_for_acceptance(page)
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `page.drag_and_drop(source, target)` string selectors | `page.mouse.down/move/up` with coordinate arithmetic | N/A — canvas tiles have no DOM selectors | `drag_and_drop` cannot target canvas pixel positions; mouse API is required |
| Fixed absolute pixel coordinates | `canvas.bounding_box()` fractional offsets | Phase 5 architecture decision | Handles window resizing, different screen DPIs |
| `locator.drag_to()` for drag ops | `page.mouse.*` low-level API | N/A — same reason as above | `drag_to` needs two locators |

**Note:** `page.mouse.move(x, y, steps=N)` is fully documented and stable in patchright 1.58.2 (same as Playwright 1.58.0 base). The `steps` parameter generates N interpolated mousemove events — confirmed in official docs (HIGH confidence).

---

## Open Questions

1. **Confirm button appearance and location**
   - What we know: A confirm/submit button appears after tile placement; it is a canvas-rendered UI element
   - What's unclear: Exact pixel location, color, shape — whether it's in a consistent canvas-relative position
   - Recommendation: Capture a debug screenshot during Wave 1 calibration with tiles placed but not confirmed; measure button position from that screenshot. Budget ~30 min for this observation.

2. **Rack tile shifting after drag**
   - What we know: After dragging a tile to the board, the remaining rack tiles may shift or leave a gap
   - What's unclear: Whether Letter League fills gaps by shifting tiles left
   - Recommendation: Observe during calibration. If shifting: implement a "consumed slots" tracker that recomputes remaining rack tile positions after each drag. If no shifting: slot indices are stable for the entire turn.

3. **Clear/undo mechanism on rejection**
   - What we know: On word rejection (invalid play), placed tiles return to the rack or must be recalled
   - What's unclear: How to trigger this — undo button, recall button, keyboard shortcut, or automatic
   - Recommendation: Observe during calibration. Note any UI button that appears after tile placement alongside the confirm button. If an undo/recall button exists at a fixed canvas position, add `RECALL_X_FRAC` / `RECALL_Y_FRAC` constants alongside the confirm button constants.

4. **iframe canvas locator chain**
   - What we know: `capture_canvas()` uses `page.locator('iframe[src*="discordsays.com"]').screenshot()` (iframe-level screenshot); tile placement needs the canvas `bounding_box()` which requires the canvas locator inside the iframe
   - What's unclear: Whether `page.locator('iframe[src*="discordsays.com"]').content_frame.locator("canvas")` is the correct locator chain in patchright, or whether `.frame_locator("iframe[src*='discordsays.com']").locator("canvas")` is preferred
   - Recommendation: Test both in Wave 1. `frame_locator()` is the Playwright-recommended API for addressing content inside iframes (HIGH confidence from Playwright docs); `content_frame` is valid but requires an element handle. Use `frame_locator()` approach first.

   ```python
   # Preferred pattern per Playwright iframe docs:
   canvas = page.frame_locator('iframe[src*="discordsays.com"]').locator("canvas").first
   bbox = await canvas.bounding_box()
   ```

---

## Validation Architecture

> `workflow.nyquist_validation` is not present in `.planning/config.json` — this project uses manual verification checkpoints, not automated test gating. Validation architecture section is omitted.

---

## Sources

### Primary (HIGH confidence)
- Playwright Python docs — `class-mouse` — `move(x, y, steps=N)`, `down()`, `up()` for drag; `steps` generates interpolated mousemove events
  https://playwright.dev/python/docs/api/class-mouse
- Playwright Python docs — `class-locator#locator-bounding-box` — returns viewport-relative `{x, y, width, height}`; returns None when not visible
  https://playwright.dev/python/docs/api/class-locator#locator-bounding-box
- Playwright Python docs — `class-locator#locator-drag-to` — requires two locators; not applicable to canvas coordinate-to-coordinate drags
  https://playwright.dev/python/docs/api/class-locator#locator-drag-to
- Playwright Python docs — `class-framelocator` — recommended API for addressing elements inside iframes
  https://playwright.dev/python/docs/api/class-framelocator
- Project ARCHITECTURE.md — TilePlacer pattern 5, fractional constant approach, placeholder values — HIGH confidence (authored by project)
- Project src/engine/models.py — `Move.rack_tiles_consumed()`, `TileUse` fields — confirmed from source
- Project src/browser/turn_detector.py — `classify_frame()` for post-confirm acceptance detection — confirmed from source
- Project src/browser/capture.py — `capture_canvas()` reusable for per-tile verification — confirmed from source
- Project debug/turn_detection/ — canvas dimensions confirmed ~1004×632 from real game screenshots

### Secondary (MEDIUM confidence)
- Playwright github issue #1461 — canvas drag via `page.mouse.*` confirmed as the correct approach; `drag_and_drop()` does not work for canvas coordinate targets (MEDIUM — GitHub issue, cross-verified with official docs)
- WebSearch: `playwright python mouse.down mouse.move bezier curve smooth drag` — confirms `steps` param approach; humanization libraries (humanization-playwright, ghost cursor) use bezier internally but all wrap the same `page.mouse.*` primitives (MEDIUM — multiple sources agree)

### Tertiary (LOW confidence)
- Confirm button visual appearance: no empirical data yet — requires live game observation during Wave 1 calibration (LOW — unknown, flagged as open question)
- Rack tile gap-or-shift behavior after drag: no empirical data yet — requires live game observation (LOW — unknown, flagged as open question)

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — no new dependencies; all libraries confirmed present and in use
- Architecture patterns: HIGH — mouse API confirmed from official docs; coordinate math is straightforward geometry; patterns follow ARCHITECTURE.md precedent
- Fractional constants: MEDIUM — placeholder values are plausible from canvas dimension analysis; must be calibrated from live game screenshots
- Confirm button + rejection handling: LOW — visual appearance unknown; empirical calibration required

**Research date:** 2026-03-26
**Valid until:** 2026-04-25 (stable Playwright API; game UI unlikely to change; constants valid until game UI update)
