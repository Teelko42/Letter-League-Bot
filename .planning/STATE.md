---
gsd_state_version: 1.0
milestone: v1.1
milestone_name: Browser Automation + Autonomous Play
status: unknown
last_updated: "2026-03-26T17:54:04Z"
progress:
  total_phases: 2
  completed_phases: 2
  total_plans: 4
  completed_plans: 4
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-03-25)

**Core value:** Analyze a Letter League board state and find the best possible word placement
**Current focus:** Phase 7 — Tile Placement (plan 1 of 2 complete)

## Current Position

Phase: 7 of 8 (Tile Placement)
Plan: 1 of 2 complete
Status: In progress
Last activity: 2026-03-26 — 07-01 CoordMapper, TilePlacer, and calibration script built

Progress: [██████░░░░] 60% (phases 1-6 complete; phase 7 plan 1 done)

## Performance Metrics

**Velocity (v1.0):**
- Total plans completed: 6
- Average duration: ~7 min
- Total execution time: ~41 min

**Velocity (v1.1):**
- Total plans completed: 4
- Average duration: ~3.5 min
- Total execution time: ~14 min

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1. Word Engine | 4 | ~28 min | ~7 min |
| 2. Difficulty System | 2 | ~13 min | ~6.5 min |
| 3. Vision Pipeline | 2 | ~6 min | ~3 min |
| 4. Discord Advisor Mode | 2 | ~8 min | ~4 min |
| 5. Browser Foundation | 3/3 | ~8 min | ~2.7 min |
| 6. Turn Detection | 1/2 | ~2 min | ~2 min |
| 7. Tile Placement | 1/2 | ~3 min | ~3 min |

**Recent Trend:**
- Last 4 plans: ~3 min, ~3 min, ~4 min, ~4 min
- Trend: Stable

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
v1.0 decisions archived — see `.planning/milestones/v1.0-ROADMAP.md`.
v1.1 decisions archived — see `.planning/milestones/v1.1-ROADMAP.md`.

v1.2 decisions so far:
- Use `patchright 1.58.2` (drop-in Playwright fork) — patches CDP fingerprint leaks Discord uses for bot detection
- Single asyncio event loop shared by discord.py and patchright — never use sync Playwright API
- All new code in `src/browser/`; vision/engine/difficulty untouched
- Dedicated throwaway Discord account for Playwright session (separate from bot token)
- First-run detection via `Default/Cookies` file check (not directory existence)
- Login completion detected by `[data-list-id="guildsnav"]` selector, 5-minute timeout
- Viewport: 1280x800 for consistent canvas screenshot dimensions
- capture_canvas() and extract_board_state() kept separate — entry-point script chains them (capture stays reusable)
- Primary canvas capture uses FrameLocator.screenshot(); falls back to frame.evaluate(canvas.toDataURL())
- is_non_blank() uses np.std() threshold of 5.0 for pixel-variance blank detection pre-check
- game_over evaluated before my_turn in classify_frame to prevent post-game infinite polling
- Quiet logging pattern: only log on turn state-change transitions, not every poll cycle
- Fractional ROI constants (BANNER_ROI_FRAC) rather than absolute pixel coordinates — resolution-independent
- All HSV turn-detection constants are placeholders; Plan 02 calibrates from live screenshots
- All tile-placement fractional constants expressed as FRAC fractions of canvas bbox; operator calibrates once via calibrate_placement.py
- Pixel-diff threshold 1.0 MAE chosen for placement verification (conservative; catches any tile landing)
- One retry on placement failure before raising PlacementError — keeps automation moving
- Rack tiles sorted by col (H) or row (V) before dragging — ensures word spells in board-natural order

### Pending Todos

None.

### Blockers/Concerns

- Phase 5: Discord Activity iframe selector is undocumented — confirm via live DevTools inspection before writing navigator code (expected pattern: `[src*="discordsays.com"]`)
- Phase 5: Canvas screenshot may be blank in headed+Xvfb mode (Playwright issue #19225) — spike must test `canvas.screenshot()` and `canvas.toDataURL()` fallback
- Phase 6: Turn-detection visual signal unknown until live gameplay observed — time-box observation spike at 4 hours; commit to screenshot-diff fallback if no reliable signal found
- Phase 7: Tile placement fractional constants in ARCHITECTURE.md are placeholders — must be measured from live game screenshots; budget for iteration

## Session Continuity

Last session: 2026-03-26
Stopped at: Completed 07-01-PLAN.md — CoordMapper, TilePlacer, calibrate_placement.py built; Plan 02 adds confirmation + rejection recovery
Resume file: None
