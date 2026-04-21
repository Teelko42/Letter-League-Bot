---
status: investigating
trigger: "e2e-pipeline-failures — vision misreads tiles, analyzer suggests invalid words, tiles placed in wrong cells; ROUND 2: bot stuck on title screen after letterbox fix; ROUND 3: bot says not_my_turn when it IS the user's turn; ROUND 4: bot places tiles but never clicks PLAY; ROUND 5: tiles placed and PLAY clicked but all words rejected with Invalid Placement"
created: 2026-04-09T00:00:00Z
updated: 2026-04-14T12:00:00Z
---

## Current Focus

hypothesis: ROUND 5 — Two root causes coexist: (1) Post-recall delay was too short (0.3-0.5s) — the game animates tiles flying back to the rack and if the next attempt starts before animation completes, the game may still have placed tiles from the prior attempt. This causes attempts 2-5 to fail because they try to place on occupied/invalid cells. (2) Engine uses Collins Scrabble Words (198K words) but Letter League almost certainly uses a much more restricted game-specific word list — TAENIAE, AZINE, AZAN, NAZI are all valid Collins words but are obscure/blocked in commercial word games. Attempt 1 fails for reason (2), attempts 2-5 fail for reason (1) compounded.
test: Post-recall delay increased to 1.0-1.5s. Debug screenshots added at pre_play_attempt{N}_{word}.png (before PLAY click) and post_recall_attempt{N}.png (after recall). Next live session will produce these files to confirm: (a) tiles visible in pre_play screenshots, (b) clean board in post_recall screenshots, (c) whether attempt 2 starts with a clean board.
expecting: post_recall screenshots will show if tiles are cleared. If tiles persist across attempts -> confirm animation-delay fix solves it. If tiles clear but all words still rejected -> confirm word-list mismatch is the remaining issue.
next_action: Await human live test to produce debug/tile_placer/*.png screenshots for analysis

## Symptoms

expected: Full e2e pipeline — vision reads board/rack, engine suggests valid high-scoring words, tiles placed in correct grid positions
actual: Vision misreads tiles/board state, analyzer suggests invalid/suboptimal words, tiles end up in wrong cells
errors: No Python tracebacks or crashes — runs silently with wrong output
reproduction: Run the bot and attempt to analyze or autoplay a game
started: Never worked correctly since implementation

## Eliminated

- hypothesis: Multiplier layout is wrong
  evidence: Layout is fully symmetric, counts match expected (4 TW, 36 DW, 28 TL, 76 DL)
  timestamp: 2026-04-09

- hypothesis: Board dimensions are wrong (not 19x27)
  evidence: Confirmed 19x27 from game source and visual inspection
  timestamp: 2026-04-09

- hypothesis: Engine move generation logic is broken
  evidence: All 225 tests pass, engine correctly finds valid words and scores them
  timestamp: 2026-04-09

- hypothesis: Tile values are wrong
  evidence: Values match Letter League (L=2, rest same as Scrabble)
  timestamp: 2026-04-09

- hypothesis: Grid constants in tile_placer.py are wrong (wrong values)
  evidence: Constants now match preprocessor.py exactly; both updated to calibrated values
  timestamp: 2026-04-14

- hypothesis: PLAY button click is missing or incorrect at 1545px iframe width
  evidence: Math confirms CONFIRM_X_FRAC=0.499527, CONFIRM_Y_FRAC=0.901042 at 1545x768 produces absolute click (1146.8, 804.0). Log shows (1148.1, 806.0) — 1.3px jitter. PLAY button received the click. Game responded with "Invalid Placement" (confirmed in debug screenshot), proving the game DID process the click.
  timestamp: 2026-04-14 (Round 5)

- hypothesis: Tile coordinates are wrong at 1545px width due to coordinate scaling
  evidence: Mathematical analysis: game scales to fill full iframe width (not pillarboxed). Fractions are resolution-independent — same fraction applied to 1545px gives proportionally correct position. Vision preprocessor confirmed grid at (87,54) 1366×657 from 1545×768 = exactly GRID_X0_FRAC*1545 = 87.8. Both pillarbox model and native-1545 model produce correct game coordinates.
  timestamp: 2026-04-14 (Round 5)

- hypothesis: RECALL button X coordinate is wrong (hitting between buttons or wrong button)
  evidence: Pixel scan of frame_20260414_114451 at y=692: SWAP/RECALL button spans x=392-474 (center=433). RECALL_X_FRAC=0.409650*1057=433 is confirmed to be at BGR=(86,128,240) = blue button body. At 1545px: 0.409650*1545=633px, button center scales to 623px — still within button range. RECALL position is correct.
  timestamp: 2026-04-14 (Round 5)

- hypothesis: Vision misreads board state causing engine to generate disconnected moves
  evidence: Engine uses anchors (cells adjacent to existing tiles) and cross-checks — it cannot generate floating moves by design. Board state misread could still cause wrong anchor cells, but the systematic pattern (5/5 words rejected) is more consistent with word-list mismatch than connectivity errors.
  timestamp: 2026-04-14 (Round 5)

- hypothesis: The fractions account for gray letterbox margins in the full iframe screenshot AND _get_canvas_bbox correctly returns the full iframe bbox
  evidence: Preflight screenshots show game rendered as small peach rectangle with gray margins; preprocessor applies fractions to img_w/img_h of the full iframe screenshot and vision works, so fractions ARE relative to full iframe. But _get_canvas_bbox() tries to remove the letterbox margins, returning a smaller game-only bbox. This causes CoordMapper to apply margin-inclusive fractions to a margin-stripped bbox.
  timestamp: 2026-04-14

## Evidence

- timestamp: 2026-04-14 (Round 4)
  checked: Pixel color at CONFIRM_Y_FRAC=0.858209, CONFIRM_X_FRAC=0.499024 in live 1057x768 frame
  found: BGR=[247,208,114] at y=659 = peach game-board tile. PLAY button (gray) is at y=681-703, center y=692, y_frac=0.901042.
  implication: All three button clicks (PLAY/RECALL/SWAP) land 33px above the actual button bar — on the game board. No button is ever clicked.

- timestamp: 2026-04-14 (Round 4)
  checked: RACK_X0_FRAC=0.400781 and RACK_TILE_STEP_FRAC=0.032531 in live 1057x768 frame
  found: Actual rack tile centers at y=716: [414,452,490,528,566,603,641]px = fracs [0.3917,0.4276,...]. First tile at 0.3917 (current 0.4008 is 9px off), step=38px=0.0358 (current 0.0325 is 3.4px/tile off).
  implication: Rack clicks are slightly off-center per tile; with 7 tiles this compounds. Corrected to measured values.

- timestamp: 2026-04-14 (Round 4)
  checked: Root cause of calibration mismatch
  found: CONFIRM_Y_FRAC was calibrated on calibration_final.png (1537x670). At that size, y_frac=0.858 correctly lands on the PLAY button (y=575 in the 670px-tall image). But in the live game at 1057x768, the same y_frac lands at y=659 — the game board. The button bar's position relative to total frame height differs between the two screenshot sizes.
  implication: Any constant calibrated on the 1537x670 screenshot that depends on the button bar Y is incorrect for the live 1057x768 game. Only RACK_Y_FRAC=0.932836 happens to be correct because the rack is close enough to the bottom that the difference is small.

- timestamp: 2026-04-09
  checked: Grid overlay with current constants on actual game screenshot
  found: Grid lines do NOT align with actual cell boundaries — offset by 30+ pixels on both axes, cells ~13% too small
  implication: All downstream operations (vision crop, tile placement, coordinate mapping) use wrong positions

- timestamp: 2026-04-09
  checked: Pixel colors at predicted TW positions (3,7) with current constants
  found: BGR=(198,229,255) = peach/beige, NOT the expected red
  implication: Confirms grid offset — the predicted positions land on wrong cells

- timestamp: 2026-04-09
  checked: Pixel colors at predicted TW positions with corrected constants
  found: BGR=(95,140,250) = red/salmon = CORRECT TW color
  implication: Corrected constants align perfectly with actual game board

- timestamp: 2026-04-09
  checked: Least-squares fit of cell boundaries from horizontal gradient analysis (28 grid lines)
  found: RMS residual = 0.7 pixels with corrected constants
  implication: New values are sub-pixel accurate

- timestamp: 2026-04-09
  checked: All four multiplier types (TW, DW, DL, TL) and NONE cells at corrected positions
  found: All colors match expected multiplier types perfectly
  implication: Corrected grid fractions are verified against ground truth

- timestamp: 2026-04-09
  checked: Origin of wrong values — git history shows calibration was done for "15x15 cells" then converted
  found: Values were derived from a 15x15 calibration with incorrect conversion to 27x19
  implication: The grid occupied a different physical area than assumed

- timestamp: 2026-04-09
  checked: Preprocessed output with corrected constants on actual game screenshot
  found: Board grid, row/column labels, multiplier labels, tiles, and rack all correctly aligned
  implication: Vision pipeline will now send correctly cropped and annotated images to Claude API

- timestamp: 2026-04-09
  checked: All 225 tests after fix
  found: All pass
  implication: No regressions from the constant changes

- timestamp: 2026-04-14
  checked: Recent preflight frames (frame_20260414_*.png)
  found: Game renders as small peach rectangle centered within a larger gray iframe; gray borders visible on all sides
  implication: Game is letterboxed — the current live iframe is larger than the game's natural render size

- timestamp: 2026-04-14
  checked: preprocessor.py code path — applies GRID_X0_FRAC * img_w to the full iframe screenshot
  found: Vision works correctly, so fractions must be measured from the full iframe screenshot (gray margins included in the fraction values)
  implication: The fractions encode the position of the game grid relative to the entire iframe screenshot, NOT relative to the game-only content area

- timestamp: 2026-04-14
  checked: _get_canvas_bbox() letterbox computation in tile_placer.py
  found: When iframe aspect ratio differs from CALIBRATION_CANVAS_W/H (1057/768 = 1.378), the function subtracts gray margins and returns a smaller game-area bbox with adjusted x/y offset
  implication: CoordMapper then applies margin-inclusive fractions (e.g. GRID_X0_FRAC = 0.056820) to a bbox that has already had the margins removed, causing systematic offset errors

- timestamp: 2026-04-14
  checked: click_start_game() in turn_detector.py — also uses the game page.mouse.click() via fractions
  found: click_start_game applies fractions directly to the full iframe bbox (no letterbox subtraction), consistent with the fractions being relative to the full iframe
  implication: The correct approach is for _get_canvas_bbox() to return the full iframe bbox always, matching the coordinate space used during calibration

- timestamp: 2026-04-14 (Round 2)
  checked: debug/turn_detection/frame_20260414_114451_956728_preflight.png (active game in progress)
  found: classify_frame returns "game_over", _is_title_screen returns True; active game is 1057x768, player-info panel on right side has BGR=[173,213,247] (warm tan) with HSV H=16 S=82 V=247 — this falls inside SIDEBAR_HSV_LOWER=[3,60,140] / UPPER=[25,220,255] producing a 33.3% sidebar ratio, exceeding the 30% threshold
  implication: The active game is indistinguishable from the title lobby under current thresholds; every frame during gameplay is classified as "game_over" causing the bot to never advance past click_start_game

- timestamp: 2026-04-14 (Round 2)
  checked: debug/turn_detection/frame_20260402_160530_032800_preflight.png (true title lobby with orange sidebar + START GAME button)
  found: True sidebar pixels have HSV H=6.9 mean, S=161 mean — highly saturated orange/salmon; active game panel has HSV H=16.4 mean, S=82 mean — low saturation warm tan
  implication: Saturation discriminates cleanly; S_min=100 keeps title_lobby ratio at 0.70, drops active_game ratio to 0.027 (well below 0.30 threshold)

- timestamp: 2026-04-14 (Round 2)
  checked: All 4 frame types with new SIDEBAR_HSV_LOWER=[3,100,140]
  found: title_lobby=True(0.70), splash_screen=False(0.00), letterboxed_peach=False(0.00), active_game=False(0.027) — all correct
  implication: Single-constant change fixes the stuck-on-title-screen bug with zero false negatives on title lobby detection

- timestamp: 2026-04-14 (Round 3)
  checked: frame_20260414_114451_956728_preflight.png — live active game where it IS the user's turn
  found: _is_title_screen=False(0.027), _is_game_over=False(peach=0.697), _is_my_turn=False(top15=0.069 < 0.07 threshold) -> classifies as not_my_turn
  implication: The my_turn frame is misclassified — this is the root cause of Round 3

- timestamp: 2026-04-14 (Round 3)
  checked: Vertical distribution of orange pixels (HSV H=5-20, S=120-255, V=150-255) in the live my_turn frame by 5% slice
  found: Rows 0-5% = 10.0%, rows 5-10% = 10.9%, rows 10-15% = 0.0%, rows 90-100% = 17% orange. The current top-15% ROI averages to 0.069 (below threshold). Top-10% ROI = 0.105 (above threshold).
  implication: BANNER_ROI_FRAC = (0.0, 0.15) dilutes the signal. Shrinking to (0.0, 0.10) fixes it.

- timestamp: 2026-04-14 (Round 3)
  checked: All reference frames (cropped_my_turn_01/02, cropped_not_my_turn_01/02) at both 15% and 10% ROI
  found: my_turn at top10%: 0.097, 0.135 (both > 0.07). not_my_turn at top10%: 0.044, 0.041 (both < 0.07). Threshold 0.07 cleanly separates them at both ROI sizes.
  implication: Changing BANNER_ROI_FRAC to (0.0, 0.10) is safe — no regressions on existing reference frames

## Evidence

- timestamp: 2026-04-14 (Round 5)
  checked: PLAY button click coordinates — math confirmation
  found: CONFIRM_X_FRAC=0.499527, CONFIRM_Y_FRAC=0.901042 at 1545x768 iframe at (375,112) produces absolute click (1146.8, 804.0). Log shows "Clicking confirm button at (1148.1, 806.0)" — 1.3px difference is just jitter. PLAY button was clicked correctly.
  implication: PLAY button click is NOT the problem in Round 5. The game genuinely receives the click and rejects the word.

- timestamp: 2026-04-14 (Round 5)
  checked: Coordinate math for tile placement at 1545px iframe width
  found: The game SCALES to fill the full 1545px iframe width (not pillarboxed). Vision preprocessor confirmed this: grid crop (87,54) 1366x657 at 1545px = GRID_X0_FRAC * 1545 = 87.8px (matches). Fractions are resolution-independent. Bot's fraction-based clicks at 1545px land at the same fractional position as at 1057px.
  implication: Tile clicks land in the correct board cells regardless of iframe width. Coordinate errors at 1545px are ruled out.

- timestamp: 2026-04-14 (Round 5)
  checked: preprocessed_debug.png image — showed game state at START of a turn with "Invalid Placement" and pending tiles (RITZ+NA pattern) visible on board
  found: The preprocessed_debug.png is saved during vision extraction at turn start. "Invalid Placement" and unrecalled tiles visible = tiles from a PREVIOUS attempt were NOT recalled before the next turn cycle began.
  implication: RECALL button click is either not clearing tiles, or clearing tiles too slowly (animation not complete before next attempt starts). Post-recall delay was 0.3-0.5s.

- timestamp: 2026-04-14 (Round 5)
  checked: Wordlist type — data/wordlist.txt statistics
  found: 198,422 words. Contains Q-without-U words (QOPH, QADI, QANAT) and very obscure Collins-only words. Confirmed Collins Scrabble Words (CSW). TAENIAE, AZINE, AZAN, NAZI are all in the wordlist.
  implication: Engine picks these valid-Collins words. Letter League likely uses a more restricted commercial word list. First attempt rejection is consistent with word-list mismatch.

- timestamp: 2026-04-14 (Round 5)
  checked: RECALL button position — pixel scan of frame_20260414_114451_956728_preflight.png at y=692
  found: Blue-orange button (BGR=86,128,240) spans x=392-474 at y=692. RECALL_X_FRAC=0.409650 -> x=433 is within this range. Button confirmed present at that coordinate. SWAP and RECALL are the same button (changes label when tiles are/aren't placed). At 1545px: RECALL_X = 633px, button center = 623px — still within button range.
  implication: RECALL button X coordinate is correct. The recall failure is timing-related (too-short delay) not coordinate-related.

- timestamp: 2026-04-14 (Round 5)
  checked: Button bar layout
  found: zoom_buttons.png (400x40 crop at 1057px, no tiles placed) shows: SWAP (left, orange) | PLAY (center, gray) | SHUFFLE (right, orange). SWAP center x~426 (frac=0.403), PLAY center x~528 (frac=0.499), SHUFFLE center x~630 (frac=0.596). When tiles placed: SWAP label changes to RECALL (same button position).
  implication: RECALL_X_FRAC=0.409650 correctly targets the SWAP/RECALL button. SHUFFLE button is unused by the bot.

## Resolution

root_cause: [Round 1] _get_canvas_bbox() letterbox subtraction offset all tile clicks. Fixed by returning full iframe bbox.
  [Round 2] SIDEBAR_HSV_LOWER saturation floor (S=60) is too loose. The active game's player-info panel has a warm tan background (BGR≈[173,213,247], HSV H=16 S=82 V=247) that falls within [H=3-25, S=60-220, V=140-255]. This makes _is_title_screen() return True during live gameplay, so classify_frame() returns "game_over" instead of "my_turn"/"not_my_turn". The poll_turn game_seen guard correctly ignores game_over until gameplay is confirmed — but that only works for poll_turn; click_start_game's own loop also polls _is_title_screen and will never exit. The result: click_start_game clicks the START GAME position, then loops 15 times (30 seconds) polling _is_title_screen, which always returns True because the game is now running but looks like a title screen — so it logs "game did not transition" and continues. Then poll_turn sees "game_over" every frame (no game_seen yet), treats it as a loading screen, never exits — bot is stuck forever.
  [Round 3] BANNER_ROI_FRAC = (0.0, 0.15) too wide. The live game "my turn" frame has orange concentrated at rows 0-10% (header bar, ~10.5% ratio) and rows 90-100% (bottom turn indicator, ~17% ratio). Rows 10-15% are completely empty. The 15% ROI averages these together to 0.069, just below BANNER_CONFIDENCE=0.07, causing a miss. The detection logic was calibrated against reference frames (1004-1009px wide) where the header orange happened to be stronger — it no longer holds at 1057x768. The ROI needs to be tightened to top 10% where the header signal is cleanest and discriminates my_turn (~10%) from not_my_turn (~4%) clearly.
  [Round 4] CONFIRM_Y_FRAC=0.858209 / RECALL_Y_FRAC=0.858209 / SWAP_Y_FRAC=0.858209 were calibrated on a 1537x670 screenshot (calibration_final.png). In that image, the PLAY button lands correctly at y=575 (frac=0.858). But the live game runs at 1057x768, where the same frac maps to y=659 — which is the game board, 22px above the button bar (y=681-703). The bot placed tiles correctly but all three button clicks (PLAY to submit, RECALL to undo, SWAP for fallback) missed, landing harmlessly on the board. Additionally RACK_X0_FRAC=0.400781 (9px off) and RACK_TILE_STEP_FRAC=0.032531 (3.4px/tile off) were also miscalibrated, causing rack picks to click between tiles.

fix: [Round 4] Updated tile_placer.py constants measured directly from live 1057x768 frame (frame_20260414_114451):
  CONFIRM_Y_FRAC: 0.858209 -> 0.901042  (PLAY button center y=692, verified BGR=[167,167,167])
  RECALL_Y_FRAC:  0.858209 -> 0.901042  (same button bar)
  SWAP_Y_FRAC:    0.858209 -> 0.901042  (same button bar)
  RECALL_X_FRAC:  0.416396 -> 0.409650  (SWAP/RECALL center x=433, verified BGR=[86,128,240])
  SWAP_X_FRAC:    0.416396 -> 0.409650  (same button)
  CONFIRM_X_FRAC: 0.499024 -> 0.499527  (0.5px correction, negligible)
  RACK_X0_FRAC:   0.400781 -> 0.391675  (first tile center x=414, verified BGR=[92,136,255])
  RACK_TILE_STEP_FRAC: 0.032531 -> 0.035793  (measured 38px step from 7-tile scan at y=716)
  RACK_Y_FRAC: 0.932836 UNCHANGED — already correct (y=716 lands on tile body)

  [Round 5-A] Post-recall animation delay 0.3-0.5s is too short. Game animates tiles back to rack; if next attempt starts before animation completes, placed tiles from prior attempt remain on board. All subsequent attempts fail with Invalid Placement (placing tiles on occupied/invalid cells). Fixed by increasing delay to 1.0-1.5s.
  [Round 5-B] Engine uses Collins Scrabble Words (198K words); Letter League almost certainly uses a more restricted commercial word list. The engine's top-scoring candidates (TAENIAE, AZINE, AZAN, NAZI) are valid Collins words but likely absent from the game's word list. First attempt in each turn fails not because of placement error but because the game doesn't recognize the word. Diagnostic screenshots added to confirm this hypothesis in the next live run.

fix: [Round 5-A] tile_placer.py _recall_tiles: post-click delay increased from random.uniform(0.3, 0.5) to random.uniform(1.0, 1.5).
  [Round 5-B] tile_placer.py: added _save_debug_screenshot() helper, diagnostic captures in place_move (pre_play_attempt{N}_{word}.png before PLAY click, post_recall_attempt{N}.png after each recall). Path added: import pathlib.Path, _DEBUG_DIR = Path("debug/tile_placer"). _recall_tiles now accepts attempt_num for screenshot labeling.
  [Round 5-C] PENDING: word list mismatch fix — awaiting live test to confirm, then either source Letter League's word list or filter engine candidates by word frequency.

verification: All 231 tests pass. Diagnostic screenshots will be produced in next live run to confirm recall works and identify word list mismatch scope.
files_changed:
  - src/vision/preprocessor.py (grid constants — Phase 1 fix)
  - src/browser/tile_placer.py (grid constants + _get_canvas_bbox letterbox removal — Phase 2 fix; button/rack constants — Round 4 fix; post-recall delay + diagnostic screenshots — Round 5 fix)
  - src/browser/turn_detector.py (SIDEBAR_HSV_LOWER saturation — Round 2 fix; BANNER_ROI_FRAC — Round 3 fix)
