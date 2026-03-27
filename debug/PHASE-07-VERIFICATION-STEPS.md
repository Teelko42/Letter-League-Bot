# Phase 7: Tile Placement — Verification Steps

## Prerequisites

- Live Letter League game open in Discord (or a saved canvas screenshot)
- Python: `& "C:\Users\Ninja\AppData\Local\Programs\Python\Python310\python.exe"`
- opencv-python installed

---

## Test 1: Calibrate Coordinates

**Goal:** Get accurate pixel constants so tiles land in the right places.

### Steps

1. **Get a screenshot** of a live game where it's your turn (tiles visible in rack, full board visible). Save as PNG to `debug/calibration.png`.
   - Must be from the **iframe canvas**, not a browser window crop.

2. **Run the calibration script:**

   ```powershell
   & "C:\Users\Ninja\AppData\Local\Programs\Python\Python310\python.exe" scripts/calibrate_placement.py debug/calibration.png
   ```

3. **An OpenCV window opens.** Click these 6 points **in this exact order:**

   | Click | What to click |
   |-------|---------------|
   | 1 | Top-left corner of **board cell (0,0)** — the very first square, top-left of the grid |
   | 2 | Top-left corner of **board cell (0,1)** — one cell to the right |
   | 3 | Top-left corner of **board cell (1,0)** — one cell below (0,0) |
   | 4 | Dead center of the **leftmost rack tile** (first letter in your tray) |
   | 5 | Dead center of the **second rack tile** |
   | 6 | Dead center of the **PLAY button** (confirm button between SWAP and SHUFFLE) |

4. **Copy the output.** The script prints something like:

   ```
   GRID_X0_FRAC           = 0.064000
   GRID_Y0_FRAC           = 0.085000
   CELL_W_FRAC            = 0.056000
   CELL_H_FRAC            = 0.062000
   RACK_X0_FRAC           = 0.380000
   RACK_Y_FRAC            = 0.680000
   RACK_TILE_STEP_FRAC    = 0.045000
   CONFIRM_X_FRAC         = 0.500000
   CONFIRM_Y_FRAC         = 0.620000
   ```

5. **Paste into `src/browser/tile_placer.py`**, replacing lines 24-32 with the new values.

6. **Also calibrate recall and swap buttons** (not covered by the script — eyeball from the screenshot):
   - `RECALL_X_FRAC` / `RECALL_Y_FRAC` (line 35-36) — center of the **SWAP** button (left side of tray bar)
   - `SWAP_X_FRAC` / `SWAP_Y_FRAC` (line 37-38) — center of the tile swap action area
   - In the game UI: SWAP is left (~0.40), PLAY is center (~0.50), SHUFFLE is right (~0.60), Y is roughly ~0.70 of canvas height. Adjust accordingly.

### Pass criteria

- Constants are reasonable fractions (all between 0.0 and 1.0)
- Cell width/height fractions make sense (e.g., ~0.05 = 15 cells across)

---

## Test 2: Place Tiles + Confirm (Acceptance)

**Goal:** Watch the bot drag tiles to the board and confirm a valid word.

### Steps

1. Start a live game, get to your turn.

2. Run a test script (adjust the move to match your actual rack and board):

   ```python
   import asyncio
   from src.browser.tile_placer import TilePlacer
   from src.engine.models import Move, TileUse, ScoreBreakdown

   async def test():
       from src.browser.session import BrowserSession
       session = BrowserSession()
       page = await session.connect()

       placer = TilePlacer(page)

       # Adjust to match your rack and a valid board position
       tiles = [
           TileUse(row=7, col=7, letter='C', is_blank=False, from_rack=True),
           TileUse(row=7, col=8, letter='A', is_blank=False, from_rack=True),
           TileUse(row=7, col=9, letter='T', is_blank=False, from_rack=True),
       ]
       move = Move(
           word='CAT', start_row=7, start_col=7, direction='H',
           tiles_used=tiles,
           score_breakdown=ScoreBreakdown(base=5, multiplier_bonus=0, bingo_bonus=0),
           score=5,
       )

       result = await placer.place_move([move], ['C', 'A', 'T', 'X', 'Y', 'Z', 'Q'])
       print(f"Accepted: {result}")

   asyncio.run(test())
   ```

3. **Watch the game screen for:**
   - Each tile dragged from rack to board with ~1-3 second gaps
   - Slight position jitter (not pixel-perfect, looks human)
   - Confirm button clicked
   - After 1-2 seconds, function returns `True` if accepted

### Pass criteria

- Tiles land on the correct board cells
- Confirm is clicked
- `place_move()` returns `True` after acceptance

---

## Test 3: Rejection + Retry Loop

**Goal:** Verify the bot handles rejected words and falls back to tile swap.

### Steps

1. Same setup as Test 2, but pass **multiple moves** — first one intentionally bad:

   ```python
   result = await placer.place_move([bad_move, good_move], rack)
   ```

2. **Watch for:**
   - First word placed, confirm clicked, rejected (still your turn)
   - Bot clicks **recall** (tiles return to rack)
   - Second word placed, confirm clicked, accepted
   - Function returns `True`

3. **To test tile swap fallback:** pass 3 moves that will all be rejected. After 3 failures:
   - Bot clicks the **swap** button
   - Function returns `False`

### Pass criteria

- Recall clears tiles back to rack on rejection
- Next word is attempted automatically
- After 3 failures, tile swap is used as fallback

---

## Summary

| Test | What it verifies | Pass if | ~Time |
|------|-----------------|---------|-------|
| 1. Calibration | Coordinate constants are accurate | Fractions are reasonable, tiles would land on correct cells | 5 min |
| 2. Place + confirm | End-to-end tile drag and acceptance | Tiles land correctly, word accepted, returns `True` | 5 min |
| 3. Rejection retry | Recall, retry loop, swap fallback | Recall works, next word tried, swap used after 3 fails | 5 min |

**Note:** Tests 2 and 3 require a live game session with patchright connected. They will also be tested naturally during Phase 8 (Autonomous Game Loop).
