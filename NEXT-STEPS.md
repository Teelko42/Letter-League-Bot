# Letter League Bot — What's Next

**Generated:** 2026-03-26
**Current State:** Phase 7 in progress (calibration verified, live game placement pending)
**Milestone:** v1.2 Browser Automation + Autonomous Play

---

## Progress Overview

```
Phase 1 (Word Engine)         ✓ Shipped 2026-03-24
Phase 2 (Difficulty System)   ✓ Shipped 2026-03-24
Phase 3 (Vision Pipeline)     ✓ Shipped 2026-03-24
Phase 4 (Discord Advisor)     ✓ Shipped 2026-03-25
Phase 5 (Browser Foundation)  ◆ Code complete — awaiting human verification
Phase 6 (Turn Detection)      ✓ Verified 2026-03-26
Phase 7 (Tile Placement)      ◆ Grid calibrated — live game test pending
Phase 8 (Autonomous Loop)     ○ Not started
```

---

## Step 1: Complete Phase 5 Verification (~30 min)

Phase 5 code is fully built (BrowserSession, navigator, capture) but was never formally verified. Plan 05-02 Task 3 is a human-verify checkpoint that requires a live Discord test.

### 1a. Ensure patchright is installed

```powershell
& "C:\Users\Ninja\AppData\Local\Programs\Python\Python310\python.exe" -m pip install patchright
& "C:\Users\Ninja\AppData\Local\Programs\Python\Python310\python.exe" -m patchright install chromium
```

### 1b. Test first-run login (if browser_data/ doesn't exist yet)

Delete `browser_data/` to force the login flow, then run:

```powershell
$env:PYTHONPATH = "."
& "C:\Users\Ninja\AppData\Local\Programs\Python\Python310\python.exe" -c "import asyncio; from src.browser.session import BrowserSession; s = BrowserSession(); asyncio.run(s.start())"
```

- A headed Chromium window opens to Discord login
- Log in manually with the throwaway Discord account
- Wait for console to print session confirmation
- Close with Ctrl+C

### 1c. Test returning session (headless)

Run the same command again without deleting `browser_data/`:

```powershell
$env:PYTHONPATH = "."
& "C:\Users\Ninja\AppData\Local\Programs\Python\Python310\python.exe" -c "import asyncio; from src.browser.session import BrowserSession; s = BrowserSession(); asyncio.run(s.start())"
```

- Should start headless (no visible browser)
- Console should confirm session is valid
- No login prompt should appear

### 1d. Test full pipeline (requires active Letter League game)

Make sure `.env` has `DISCORD_CHANNEL_URL` set, then:

```powershell
$env:PYTHONPATH = "."
& "C:\Users\Ninja\AppData\Local\Programs\Python\Python310\python.exe" scripts/browser_test.py
```

**Expected:** Bot navigates to voice channel, opens Activity, captures screenshot, passes it through `extract_board_state()`, prints board + rack.

### 1e. Mark Phase 5 complete

Once tests pass, tell Claude:

```
/gsd:execute-phase 5
```

Or manually: describe results so Claude can create `05-VERIFICATION.md` and mark the phase complete.

**Success criteria for Phase 5:**

| # | Criterion | How to verify |
|---|-----------|---------------|
| 1 | Bot launches with saved Discord login across restarts | Steps 1b + 1c |
| 2 | Bot detects expired session and prints warning | Delete cookies from browser_data, re-run |
| 3 | Bot navigates to voice channel and opens Activity iframe | Step 1d |
| 4 | Canvas screenshot is non-blank (pixel variance check) | Step 1d — no "blank screenshot" error |
| 5 | Screenshot parses through extract_board_state() | Step 1d — prints Board + rack |

---

## Step 2: Plan Phase 7 — Tile Placement

**Goal:** Translate a word move into pixel clicks that place tiles on the board.

**Requirements:**
- TILE-01: Compute pixel coordinates for board cells and rack tiles from canvas bounding box
- TILE-02: Click rack tiles and board cells to place a chosen word
- TILE-03: Confirm word placement via game UI

### What you need to do before planning

1. **Capture 3+ screenshots** of a live game at the default 1280x800 viewport
2. **Identify rack tile positions** — where do the 7 tiles sit? Measure x,y offsets as fractions of canvas size
3. **Identify board grid origin** — where is cell (0,0)? What's the cell width/height?
4. **Find the confirm/play button** — is it a DOM element or rendered on the canvas?

### Then run

```
/gsd:plan-phase 7
```

This will research, plan, and verify the phase before execution.

### Key risk

Coordinate calibration is the highest-uncertainty component of v1.2. Fractional offsets must be measured from real gameplay, not guessed. The plan will include a calibration script similar to `calibrate_turn.py`.

---

## Step 3: Execute Phase 7

```
/gsd:execute-phase 7
```

This will likely include a human-verify checkpoint for live coordinate calibration (similar to Phase 6's HSV calibration).

**Expected deliverables:**
- `src/browser/tile_placer.py` — `place_move(frame, move, canvas_bbox)`
- `scripts/calibrate_coords.py` — interactive coordinate measurement tool
- Fractional constants calibrated from live game measurements

---

## Step 4: Plan Phase 8 — Autonomous Game Loop

**Goal:** `/autoplay start` launches a self-sustaining turn loop that reads the board, selects a move, places tiles, and posts status.

**Requirements:**
- LOOP-01: Async game loop concurrent with discord.py (no blocking)
- LOOP-02: `/autoplay start`, `/autoplay stop`, `/autoplay status` commands
- LOOP-03: Human-like timing jitter (1-3s delays between actions)
- LOOP-04: Tile swap fallback when no valid moves exist
- LOOP-05: Discord status message after each turn (word + points)
- BROW-03: Graceful reconnection on Activity disconnect

### Then run

```
/gsd:plan-phase 8
```

---

## Step 5: Execute Phase 8

```
/gsd:execute-phase 8
```

**Expected deliverables:**
- `src/browser/game_loop.py` — async polling loop with turn detection integration
- `src/bot/autonomous_cog.py` — `/autoplay` slash commands
- Full pipeline: capture → vision → engine → difficulty → placement → status

---

## Step 6: Complete Milestone v1.2

After all phases pass verification:

```
/gsd:audit-milestone
/gsd:complete-milestone v1.2
```

---

## Quick Reference

### Commands

| Action | Command |
|--------|---------|
| Check progress | `/gsd:progress` |
| Plan a phase | `/gsd:plan-phase <N>` |
| Execute a phase | `/gsd:execute-phase <N>` |
| Verify work | `/gsd:verify-work <N>` |
| Audit milestone | `/gsd:audit-milestone` |
| Complete milestone | `/gsd:complete-milestone v1.2` |

### Python on this machine

```powershell
& "C:\Users\Ninja\AppData\Local\Programs\Python\Python310\python.exe" <script>
```

Always set `$env:PYTHONPATH = "."` before running scripts.

### Key files

| File | Purpose |
|------|---------|
| `src/browser/session.py` | Persistent browser session (Phase 5) |
| `src/browser/navigator.py` | Discord navigation + iframe discovery (Phase 5) |
| `src/browser/capture.py` | Canvas screenshot + blank validation (Phase 5) |
| `src/browser/turn_detector.py` | Turn state classification + polling (Phase 6) |
| `scripts/browser_test.py` | Full pipeline test (Session → Nav → Capture → Vision) |
| `scripts/calibrate_turn.py` | HSV threshold calibration tool |
| `.planning/v1.2-MILESTONE-AUDIT.md` | Audit report with all gaps |

### Known issues

1. **Phase 5 unverified** — code works but no VERIFICATION.md exists
2. **Frame handoff gap** — `navigate_to_activity` returns Frame that callers discard; `capture_canvas` re-discovers iframe independently (not a blocker, just redundant)
3. **calibrate_turn.py** — live iframe navigation path never succeeded (manual screenshots used as workaround)

---

*Generated from milestone audit and project state analysis*
