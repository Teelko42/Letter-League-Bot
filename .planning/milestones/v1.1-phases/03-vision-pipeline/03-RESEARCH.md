# Phase 3: Vision Pipeline - Research

**Researched:** 2026-03-24
**Domain:** Image preprocessing (Pillow, OpenCV) + Claude Vision API + JSON schema extraction + Board validation
**Confidence:** HIGH

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions

**Vision prompt design:**
- Single API call extracts board tiles, tile rack, and multipliers together (not separate calls)
- Prompt instructs Claude to return structured JSON matching a defined schema (not natural language)
- Prompt explicitly states the board is 19 rows x 27 columns to anchor extraction
- Text-only prompt — no reference images or diagrams sent alongside the screenshot

**Board data format:**
- Vision output maps directly to the existing Board/Cell class structure (no intermediate representation)
- Return a bounding rectangle of the occupied area, not the full 19x27 grid and not a sparse list
- Tile rack included as a separate top-level field in the same JSON response: `{"board": {...}, "rack": [...]}`

**Image preprocessing:**
- Auto-detect the board region in screenshots (edge detection / color patterns), not hardcoded crop coordinates
- 2x upscale after cropping for improved letter readability
- Single crop region that includes both the board and the tile rack below it
- No color or contrast adjustments — send the cropped/upscaled image as-is

**Validation & error handling:**
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

### Deferred Ideas (OUT OF SCOPE)

None — discussion stayed within phase scope
</user_constraints>

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| VISN-01 | User can submit a Letter League screenshot and receive a structured board state extraction (grid cells, letters, positions) | Claude Vision API with `output_config` json_schema returns guaranteed-valid JSON; `VisionPipeline.extract_board_state()` populates existing `Board` via `place_tile()` |
| VISN-02 | User's tile rack is extracted from the screenshot alongside the board | Single API call with `{"board": {...}, "rack": [...]}` schema; rack region included in same crop window as board |
| VISN-03 | Multiplier squares (DL/TL/DW/TW) are detected and mapped to board positions | Prompt anchors Claude to known 19x27 grid; validation check 3 cross-references extracted multiplier positions against the hardcoded `OFFICIAL_MULTIPLIER_LAYOUT` dict |
| VISN-04 | Screenshots are cropped to the board region and upscaled before API processing for accuracy | OpenCV HSV color mask → bounding-rect crop → Pillow `Image.Resampling.LANCZOS` 2x resize → BytesIO → base64; stays under 1568px cap |
| VISN-05 | Extracted board state is validated against engine constraints before being passed to the word engine | Four-check validator: letter set, connectivity (engine cross-check reuse), multiplier layout match, rack count ≤ 7; single retry with error context on failure |
</phase_requirements>

---

## Summary

Phase 3 builds a self-contained module (`src/vision/`) that accepts raw PNG bytes from any source (Discord attachment, Playwright screenshot) and returns a populated `Board` + rack list ready for the existing `GameEngine`. The pipeline has four sequential steps: auto-detect and crop the board region using OpenCV color analysis, upscale 2x with Pillow, send to Claude Vision with a json_schema structured-output constraint, then validate the result against four engine-level checks.

The key technical insight is that Anthropic's structured outputs feature (now GA, no beta header needed) makes JSON parse errors a non-issue for the primary path. Using `output_config.format.type = "json_schema"` with `additionalProperties: false` guarantees the schema is satisfied at the token level — Claude literally cannot produce a response that fails `json.loads()`. The retry path therefore focuses exclusively on semantic validation failures (wrong letters, disconnected tiles, bad multiplier positions), not parse errors.

For board detection, the Letter League board has a visually distinct background color and grid structure. OpenCV's `cv2.inRange()` on an HSV-converted image produces a binary mask; `cv2.findContours()` finds the largest rectangular region, and `cv2.boundingRect()` gives the crop box. This approach is robust to varying screenshot resolutions and UI chrome around the game.

**Primary recommendation:** Implement in three layers — `preprocessor.py` (OpenCV crop + Pillow upscale), `extractor.py` (Claude Vision API call with structured output schema), `validator.py` (four checks + retry orchestration). Keep the public entry point as a single async function `extract_board_state(img_bytes: bytes) -> Board | VisNError`.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `anthropic` | `0.86.0` | `AsyncAnthropic` client for vision API call | Already project stack; async required for discord.py event loop; provides `output_config` for structured JSON |
| `Pillow` | `12.1.1` | In-memory image open, crop, resize, BytesIO encode | Already project stack; `Image.Resampling.LANCZOS` for quality 2x upscale |
| `opencv-python` | `4.13.0.92` | HSV color-based board region detection and bounding rect | Already project stack; `cv2.inRange`, `cv2.findContours`, `cv2.boundingRect` |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `json` | stdlib | Parse `response.content[0].text` after structured-output call | Always — even with json_schema output, the result arrives as a JSON string in `.text` |
| `io.BytesIO` | stdlib | In-memory buffer for Pillow → bytes conversion without temp files | Always — avoids disk I/O in the pipeline |
| `base64` | stdlib | `base64.standard_b64encode` for Claude API image payload | Always — required by Claude base64 image source |
| `loguru` | `0.7.3` | Log validation failures, API latency, retry events | Always — critical for diagnosing vision accuracy issues |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| OpenCV HSV detection | Hardcoded crop coordinates | Hardcoded coords break on different resolutions/DPI scales; OpenCV is 5–10 lines and handles any screenshot size |
| OpenCV HSV detection | PIL `ImageFilter` edge detection | OpenCV has more precise contour-finding primitives; PIL filters are lower-level for this task |
| `output_config` json_schema | Prompt-only JSON + `json.loads()` | Without structured outputs, Claude occasionally wraps JSON in markdown fences or prose; structured outputs guarantee parseable output |
| `output_config` json_schema | `instructor` library | `instructor` is an abstraction on top of the SDK; adds a dep; `output_config` is now native in the SDK |
| Pillow LANCZOS | Pillow BICUBIC | LANCZOS is higher quality for upscaling; BICUBIC is default for resize but LANCZOS preserves letter shapes better |
| `Image.Resampling.LANCZOS` | `Image.LANCZOS` (old constant) | Pillow 10+ deprecated the flat constants; `Image.Resampling.LANCZOS` is the correct form in Pillow 12.x |

**Installation (no new deps — all already in project stack):**

```bash
# All already installed per STACK.md:
# anthropic==0.86.0, Pillow==12.1.1, opencv-python==4.13.0.92, loguru==0.7.3
# No new packages required for Phase 3
```

---

## Architecture Patterns

### Recommended Project Structure

```
src/
├── vision/
│   ├── __init__.py          # Public API: extract_board_state()
│   ├── preprocessor.py      # OpenCV board detection + Pillow crop/upscale
│   ├── extractor.py         # Claude Vision API call + structured output
│   ├── validator.py         # Four validation checks + retry orchestration
│   ├── schema.py            # JSON schema definition + OFFICIAL_MULTIPLIER_LAYOUT
│   └── errors.py            # VisNError, typed error codes (INVALID_SCREENSHOT, etc.)
├── engine/                  # Existing — unchanged
└── difficulty/              # Existing — unchanged
```

### Pattern 1: Structured Output with output_config

**What:** Use `output_config.format` with a JSON schema in the `messages.create()` call. Claude's token generation is constrained to produce only valid schema-compliant JSON. No parse errors, no markdown fences, no explanatory prose.

**When to use:** Whenever Claude must return machine-readable structured data. Eliminates the entire class of "LLM returned JSON wrapped in ```json```" bugs.

**Example:**

```python
# Source: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
import json
import base64
from io import BytesIO
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

BOARD_SCHEMA = {
    "type": "object",
    "properties": {
        "board": {
            "type": "object",
            "description": "Bounding rectangle of occupied cells",
            "properties": {
                "min_row": {"type": "integer"},
                "max_row": {"type": "integer"},
                "min_col": {"type": "integer"},
                "max_col": {"type": "integer"},
                "cells": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "row": {"type": "integer"},
                            "col": {"type": "integer"},
                            "letter": {"type": "string"},
                            "is_blank": {"type": "boolean"},
                            "multiplier": {"type": "string", "enum": ["NONE", "DL", "TL", "DW", "TW"]}
                        },
                        "required": ["row", "col", "letter", "is_blank", "multiplier"],
                        "additionalProperties": False
                    }
                }
            },
            "required": ["min_row", "max_row", "min_col", "max_col", "cells"],
            "additionalProperties": False
        },
        "rack": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Tile rack letters, max 7 tiles"
        }
    },
    "required": ["board", "rack"],
    "additionalProperties": False
}

async def call_vision_api(img_bytes: bytes, system_prompt: str) -> dict:
    img_b64 = base64.standard_b64encode(img_bytes).decode("utf-8")
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": img_b64,
                    },
                },
                {
                    "type": "text",
                    "text": system_prompt
                }
            ]
        }],
        output_config={
            "format": {
                "type": "json_schema",
                "schema": BOARD_SCHEMA
            }
        }
    )
    return json.loads(response.content[0].text)
```

### Pattern 2: OpenCV Board Region Detection

**What:** Convert screenshot to HSV, use `cv2.inRange()` to isolate the board's background color, find contours, select the largest bounding rect, crop with Pillow.

**When to use:** For auto-detecting the board region without hardcoded pixel coordinates. Works across different screenshot resolutions and window sizes.

**Example:**

```python
# Source: OpenCV docs https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def detect_board_region(img_bytes: bytes) -> tuple[int, int, int, int]:
    """Returns (x, y, w, h) bounding rect of the detected board region."""
    # Decode bytes to numpy array (OpenCV format)
    nparr = np.frombuffer(img_bytes, np.uint8)
    bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert to HSV for color-range detection
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    # HSV range for Letter League board background (tune during testing)
    # Board has a distinctive beige/cream color — values need empirical tuning
    lower = np.array([15, 20, 160])
    upper = np.array([35, 80, 240])
    mask = cv2.inRange(hsv, lower, upper)

    # Find contours and select largest
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("No board region detected")
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)
    return x, y, w, h

def crop_and_upscale(img_bytes: bytes, region: tuple[int, int, int, int]) -> bytes:
    """Crop to board region, upscale 2x, return PNG bytes."""
    x, y, w, h = region
    img = Image.open(BytesIO(img_bytes))
    cropped = img.crop((x, y, x + w, y + h))

    # 2x upscale with LANCZOS for quality
    new_size = (cropped.width * 2, cropped.height * 2)
    upscaled = cropped.resize(new_size, Image.Resampling.LANCZOS)

    # Ensure within Claude's 1568px-per-edge limit
    max_edge = 1568
    if max(upscaled.size) > max_edge:
        ratio = max_edge / max(upscaled.size)
        upscaled = upscaled.resize(
            (int(upscaled.width * ratio), int(upscaled.height * ratio)),
            Image.Resampling.LANCZOS
        )

    buf = BytesIO()
    upscaled.save(buf, format="PNG")
    return buf.getvalue()
```

### Pattern 3: Validation + Single Retry

**What:** Run four checks against extracted data. On any failure, build an error-context message and retry once with Claude, passing the same image and describing what failed. On second failure, raise a typed error.

**When to use:** Always after extraction. Never trust Claude's output without validation.

**Example:**

```python
from src.engine.models import MultiplierType
from src.engine.tiles import ALPHABET

OFFICIAL_MULTIPLIER_LAYOUT: dict[tuple[int, int], str] = {
    # Populated during plan wave — requires screenshot analysis of real board
    # Example entries (actual values determined from game screenshots):
    # (0, 0): "TW", (0, 13): "TW", ...
}

def validate_extraction(data: dict) -> list[str]:
    """Returns list of validation error messages (empty = pass)."""
    errors = []

    cells = data["board"]["cells"]
    rack = data["rack"]

    # Check 1: All letters A-Z
    for cell in cells:
        if cell["letter"] not in ALPHABET:
            errors.append(f"Invalid letter '{cell['letter']}' at ({cell['row']}, {cell['col']})")

    # Check 2: Rack size ≤ 7
    if len(rack) > 7:
        errors.append(f"Rack has {len(rack)} tiles (max 7)")

    # Check 3: Multiplier positions match official layout
    for cell in cells:
        pos = (cell["row"], cell["col"])
        expected = OFFICIAL_MULTIPLIER_LAYOUT.get(pos, "NONE")
        if cell["multiplier"] != expected:
            errors.append(
                f"Multiplier mismatch at {pos}: got {cell['multiplier']}, expected {expected}"
            )

    # Check 4: Connectivity (no floating tiles) — deferred to board.find_anchors()
    # A tile is floating if it has no orthogonal neighbor with a letter
    placed = {(c["row"], c["col"]) for c in cells}
    for cell in cells:
        r, c = cell["row"], cell["col"]
        neighbors = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
        if not any(n in placed for n in neighbors) and len(cells) > 1:
            errors.append(f"Floating tile '{cell['letter']}' at ({r}, {c}) — not connected to any other tile")

    return errors
```

### Anti-Patterns to Avoid

- **Hardcoded pixel coordinates for crop:** Breaks on different display resolutions, window sizes, DPI scaling. Always use OpenCV region detection.
- **Raw prompt without output_config:** Without structured output, Claude may wrap JSON in markdown fences, add explanatory text, or produce subtly malformed JSON. Always use `output_config.format.type = "json_schema"`.
- **Using `Image.LANCZOS` (flat constant):** Deprecated in Pillow 10+; use `Image.Resampling.LANCZOS` in Pillow 12.x.
- **Passing full 19x27 grid in schema:** Produces 513 cell objects even when the board is mostly empty. Use bounding-rect sparse representation as locked in CONTEXT.md.
- **Running validation in the extractor:** Keep the four validation checks in `validator.py`, not in `extractor.py`. The extractor's only job is to call the API and parse the JSON.
- **Calling `engine.find_all_moves()` for connectivity check:** This is overkill and expensive. A simple neighbor-set check (O(n) where n = placed tile count) is sufficient for connectivity validation.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JSON schema validation at token level | Custom retry loop for parse errors | `output_config.format.type = "json_schema"` | Parse errors become impossible; structured outputs constrain token generation at the model level |
| Board region detection | Fixed pixel offsets, template matching | `cv2.inRange` + `cv2.findContours` + `cv2.boundingRect` | Color-range detection handles resolution variance; template matching requires a reference template for every screenshot size |
| Upscaling algorithm | Custom interpolation | `Image.Resampling.LANCZOS` | Lanczos produces best quality for 2x upscaling of text/letter tiles |
| In-memory PNG encoding | Temp files on disk | `io.BytesIO` + `Image.save(buf, format="PNG")` | Disk I/O adds latency; BytesIO keeps the whole pipeline in memory |
| OFFICIAL_MULTIPLIER_LAYOUT | Try to extract multipliers purely from vision | Hardcode from known board layout + validate against it | The 19x27 starting layout is fixed by the game; vision confirms, doesn't discover |

**Key insight:** The structured outputs feature (GA as of 2026) eliminates the biggest historical pain point of LLM vision pipelines — JSON parse errors. Design the retry loop for semantic validation failures only, not parse failures.

---

## Common Pitfalls

### Pitfall 1: HSV Range Needs Empirical Calibration

**What goes wrong:** The HSV bounds for board detection are set too narrow or too wide. Too narrow: mask is empty, `findContours` finds nothing, pipeline raises an error. Too wide: mask includes non-board UI elements (Discord toolbar, tile rack background), bounding rect is over-inclusive.

**Why it happens:** Letter League's board color is not documented. The HSV range must be determined empirically from real screenshots. Guessing values leads to unreliable detection.

**How to avoid:** Build a small calibration script that displays the HSV histogram of a sample screenshot. Sample multiple screenshots (different game states, different devices/displays) before finalizing the range. Add a minimum-area threshold — if `cv2.contourArea(largest) < threshold`, raise `INVALID_SCREENSHOT` rather than crop garbage.

**Warning signs:** Crop region is the full screenshot, or crop region is very small (< 100x100px), or contour detection returns 0 contours.

### Pitfall 2: Claude's Spatial Reasoning Limitations on Dense Grids

**What goes wrong:** Claude accurately reads individual letters but maps them to wrong grid coordinates. A 27-column grid is wide; without anchoring, Claude may miscount columns, especially in the middle of the board.

**Why it happens:** Anthropic's official docs explicitly state: "Claude's spatial reasoning abilities are limited. It may struggle with tasks requiring precise localization or layouts." Dense word-game grids are exactly this use case.

**How to avoid:** The prompt must anchor Claude with explicit grid dimensions (19 rows, 27 columns, 0-indexed), state that columns increase left-to-right and rows increase top-to-bottom, and instruct Claude to count from visible grid lines/borders. Test against real screenshots with known board states before gating Phase 3.

**Warning signs:** Validation check 1 passes (letters are valid) but connectivity check fails (tiles are placed but not forming words) — suggests coordinate offset errors rather than letter misreads.

### Pitfall 3: Upscaled Image Exceeds Claude's 1568px Limit

**What goes wrong:** After 2x upscale, the image dimensions exceed 1568px on the long edge. Claude auto-downsamples it, adding latency with no quality benefit, defeating the purpose of upscaling.

**Why it happens:** If the cropped board region is, say, 900px wide, 2x makes it 1800px — above the 1568px threshold.

**How to avoid:** After the 2x resize, clamp: if `max(w, h) > 1568`, resize to fit within 1568px while preserving aspect ratio. This is implemented in the `crop_and_upscale` pattern above.

**Warning signs:** API latency is higher than expected (~4-15s is normal; consistently >20s may indicate auto-downsampling overhead).

### Pitfall 4: OFFICIAL_MULTIPLIER_LAYOUT Not Populated

**What goes wrong:** Validation check 3 always passes or always fails because `OFFICIAL_MULTIPLIER_LAYOUT` is empty or wrong.

**Why it happens:** The multiplier layout for the 19x27 starting board must be mapped from actual game screenshots. The Letter League Info.md contains board images but is too large to read programmatically (164K tokens). This mapping requires manual inspection or a dedicated screenshot analysis pass.

**How to avoid:** Phase 3 Wave 0 must include a task to build the `OFFICIAL_MULTIPLIER_LAYOUT` dict from real screenshots before the validator can use it. Until it's populated, validation check 3 should be skipped (log a warning) rather than producing false failures. The planner should create a Wave 0 task: "Map multiplier layout from screenshots."

**Warning signs:** All boards pass/fail multiplier validation uniformly regardless of what's extracted.

### Pitfall 5: Connectivity Check False-Positives on First Move

**What goes wrong:** On the very first turn, there is exactly one placed word. The connectivity check (check 2) may incorrectly flag single isolated tiles if the implementation checks neighbor count without accounting for tiles that are part of the same word.

**Why it happens:** A single horizontal word like "CAT" at (9, 12), (9, 13), (9, 14) — each tile has one horizontal neighbor but no vertical neighbors. A naive check for "any tile with no neighbor" would falsely flag the endpoints.

**How to avoid:** Connectivity check should use a flood-fill from any placed tile: all placed tiles must be reachable from the first tile via orthogonal moves. A tile having at least one neighbor is not sufficient for general connectivity.

**Warning signs:** Single-word boards fail validation with "floating tile" errors.

### Pitfall 6: Blank Tile Representation

**What goes wrong:** Blank tiles (the `?` tile in the rack) show the letter they've been assigned when placed on the board. Claude will extract the letter, not the blank status. The `is_blank` field in the schema will be set to `false` unless the prompt explicitly instructs Claude to detect blank tiles visually (they typically appear lighter or with a different border color in Letter League).

**Why it happens:** Claude reads the displayed letter. Blank status is a visual distinction that requires an explicit instruction in the prompt.

**How to avoid:** Prompt must explicitly describe how blank tiles appear visually in Letter League (different color/border) and instruct Claude to set `is_blank: true` for those tiles. This is a prompt engineering task, not a schema task.

**Warning signs:** Scoring discrepancies between vision-extracted board and expected scores — blank tiles have 0 point value but vision reports them as regular tiles.

---

## Code Examples

Verified patterns from official sources:

### Complete preprocessor pipeline (bytes in → bytes out)

```python
# Source: Pillow docs https://pillow.readthedocs.io/en/stable/reference/Image.html
#         OpenCV docs https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def preprocess_screenshot(img_bytes: bytes) -> bytes:
    """Detect board region, crop, upscale 2x, return PNG bytes."""
    # Step 1: OpenCV board detection
    nparr = np.frombuffer(img_bytes, np.uint8)
    bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    lower = np.array([15, 20, 160])   # HSV lower — needs calibration
    upper = np.array([35, 80, 240])   # HSV upper — needs calibration
    mask = cv2.inRange(hsv, lower, upper)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("Board region not detected — may not be a Letter League screenshot")

    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < 10000:  # Minimum area threshold
        raise ValueError("Detected region too small — not a valid board")

    x, y, w, h = cv2.boundingRect(largest)

    # Step 2: Pillow crop + 2x upscale
    img = Image.open(BytesIO(img_bytes))
    cropped = img.crop((x, y, x + w, y + h))
    new_w, new_h = cropped.width * 2, cropped.height * 2

    # Clamp to Claude's 1568px limit
    # Source: https://platform.claude.com/docs/en/build-with-claude/vision
    if max(new_w, new_h) > 1568:
        ratio = 1568 / max(new_w, new_h)
        new_w = int(new_w * ratio)
        new_h = int(new_h * ratio)

    upscaled = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)

    buf = BytesIO()
    upscaled.save(buf, format="PNG")
    return buf.getvalue()
```

### Async Claude Vision call with structured output

```python
# Source: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
#         https://platform.claude.com/docs/en/build-with-claude/vision
import json
import base64
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

EXTRACTION_PROMPT = """This is a Letter League game board screenshot.
Letter League uses a 19-row by 27-column grid (row 0 = top, col 0 = left).
Extract all placed tiles, their exact grid coordinates, and the player's tile rack.
For blank tiles (visually distinct — lighter color or different border), set is_blank to true.
Only include cells that have tiles placed on them."""

async def extract_board_state(img_bytes: bytes) -> dict:
    img_b64 = base64.standard_b64encode(img_bytes).decode("utf-8")
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": img_b64,
                    },
                },
                {"type": "text", "text": EXTRACTION_PROMPT}
            ]
        }],
        output_config={
            "format": {
                "type": "json_schema",
                "schema": BOARD_SCHEMA  # defined in schema.py
            }
        }
    )
    return json.loads(response.content[0].text)
```

### Populating Board from extraction result

```python
# Integrates with existing src/engine/board.py and src/engine/models.py
from src.engine.board import Board
from src.engine.models import MultiplierType, Cell

MULT_MAP = {
    "NONE": MultiplierType.NONE,
    "DL": MultiplierType.DL,
    "TL": MultiplierType.TL,
    "DW": MultiplierType.DW,
    "TW": MultiplierType.TW,
}

def populate_board(data: dict, mode: str = "classic") -> tuple[Board, list[str]]:
    """Build a Board from extracted vision data."""
    board = Board(rows=19, cols=27, multiplier_layout=OFFICIAL_MULTIPLIER_LAYOUT_ENGINE_FORMAT)

    for cell_data in data["board"]["cells"]:
        board.place_tile(
            row=cell_data["row"],
            col=cell_data["col"],
            letter=cell_data["letter"],
            is_blank=cell_data["is_blank"],
            mode=mode,
        )

    rack = data["rack"]
    return board, rack
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Prompt-only JSON + regex extraction | `output_config.format.type = "json_schema"` | Nov 2025 (GA by early 2026) | Eliminates JSON parse errors entirely; no need for `json_repair` or retry on malformed output |
| `image_b64` beta header for structured outputs | No beta header needed — use `output_config` directly | Early 2026 (GA) | Simpler implementation; old `output_format` param deprecated but still works during transition |
| `Image.LANCZOS` (flat constant) | `Image.Resampling.LANCZOS` (enum) | Pillow 10.0.0 (2023) | Old constant still works but raises DeprecationWarning in Pillow 12.x |

**Deprecated/outdated:**
- `output_format` parameter: Moved to `output_config.format`; the old parameter continues working during transition but is no longer documented as primary
- `beta_headers: ["structured-outputs-2025-11-13"]`: No longer required; structured outputs are GA

---

## Open Questions

1. **OFFICIAL_MULTIPLIER_LAYOUT exact values**
   - What we know: The Letter League starting board has a fixed 19x27 layout with DL, TL, DW, TW squares. The multiplier layout is deterministic and does not change between games.
   - What's unclear: The exact (row, col) → MultiplierType mapping has not been extracted from the game screenshots. The `Letter League Info.md` file contains board images as embedded base64 PNGs but is 164K tokens — not readable as text.
   - Recommendation: Wave 0 of Phase 3 should include a task to map the multiplier layout by visual inspection of real screenshots or game play. Until mapped, disable validation check 3 (log a warning instead of rejecting).

2. **HSV range calibration for board detection**
   - What we know: OpenCV HSV detection is the right approach. Letter League's board has a distinctive background.
   - What's unclear: The exact HSV range values. These depend on the game's actual color palette and can vary slightly by device display profile.
   - Recommendation: Include a calibration utility in the first implementation task. Use a sample screenshot with known board region, display the HSV histogram in that region, set range from the modal values ± tolerance.

3. **Blank tile visual appearance in Letter League**
   - What we know: Blank tiles display the letter they've been assigned. Standard Scrabble-style games show blank tiles with a lighter color or no point value printed.
   - What's unclear: Whether Letter League renders blank tiles visually differently from regular tiles, and if so, how (color? border? point value display?).
   - Recommendation: Test with a real screenshot containing a placed blank tile. If visually indistinguishable, the `is_blank` field may not be reliably extractable via vision — in that case, document this as a known limitation and default `is_blank: false` for all extracted tiles.

4. **max_tokens for extraction response**
   - What we know: A fully populated 19x27 board could have up to ~500 placed tiles (extreme case). Each cell in the JSON schema is a small object. At 4096 tokens, very dense boards might be truncated.
   - What's unclear: How many tokens a dense Letter League board extraction actually consumes.
   - Recommendation: Start with `max_tokens=4096`. If truncation is observed on large boards, increase to 8192. Monitor `response.usage.output_tokens` to track consumption.

---

## Sources

### Primary (HIGH confidence)

- `https://platform.claude.com/docs/en/build-with-claude/vision` — Image formats (JPEG/PNG/GIF/WebP), 5MB limit, 8000x8000px max, 1568px per-edge threshold, token cost formula, base64 encoding, image-before-text placement, spatial reasoning limitations
- `https://platform.claude.com/docs/en/build-with-claude/structured-outputs` — `output_config.format.type = "json_schema"`, no beta header required (GA), AsyncAnthropic compatibility, `additionalProperties: false` requirement, supported models (all current Claude models)
- `https://pillow.readthedocs.io/en/stable/reference/Image.html` — `Image.Resampling.LANCZOS` enum (Pillow 10+), `crop((left, upper, right, lower))`, `resize(size, resample)` defaults to `Resampling.BICUBIC`, `Image.open(BytesIO(...))`
- `https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html` — HSV colorspace, `cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)`, `cv2.inRange()` for color masking
- Existing `src/engine/models.py`, `src/engine/board.py`, `src/engine/__init__.py` — `Board`, `Cell`, `MultiplierType`, `place_tile()` API confirmed compatible with vision output

### Secondary (MEDIUM confidence)

- `https://getstream.io/blog/anthropic-claude-visual-reasoning/` — Claude Vision structured extraction patterns, image placement best practices (verified against official docs above)
- `https://github.com/JulienPalard/grid-finder` — OpenCV contour-based grid detection patterns (community source, approach consistent with official OpenCV docs)

### Tertiary (LOW confidence)

- Community reports on HSV calibration for game board detection — HSV ranges in code examples are illustrative only; actual values require empirical calibration against real Letter League screenshots

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all four libraries are already in the project stack, confirmed versions in STACK.md (March 2026)
- Architecture: HIGH — Pillow/OpenCV patterns are stable; structured outputs API verified against official docs
- Pitfalls: HIGH (spatial reasoning, 1568px limit) — from official Anthropic docs; MEDIUM (HSV calibration, blank tile detection) — requires empirical validation on real screenshots
- Multiplier layout: LOW — exact (row, col) values not yet determined; must be mapped from real game screenshots in Wave 0

**Research date:** 2026-03-24
**Valid until:** 2026-04-24 (30 days — anthropic SDK is relatively stable; re-verify if anthropic SDK version changes)
