# Auto-debug iteration 1

- exit_code: `1`
- duration: 443.2s
- error_signature: `c15f3f6b3caf`
- words placed: 0
- turns skipped (swap/skip — these are FAILURES for the user goal): 2
- terminal marker reached: False

**User goal: the bot must place a word every turn.** A turn that ends in
swap/skip means the placement pipeline failed (vision drift, retries
exhausted, etc.) and the engine fell back to swap. The fix needs to make
more turns end with a placed word, not just keep the run alive longer.

## Recent debug artifacts
- `debug/tile_placer/post_recall_attempt1.png`
- `debug/turn_detection/frame_20260505_173706_713514_pre_start_attempt1.png`
- `debug/preprocessed_debug.png`

## Autoplay log — error region
```
2026-05-05 17:37:47.858 | INFO    | src.engine.rejected_words:_ensure_loaded:49 | Loaded 392 rejected words from C:\Github\Letter-League-Bot\data\rejected_words.txt
2026-05-05 17:37:47.859 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 27 blacklisted candidate(s)
2026-05-05 17:37:48.307 | INFO    | src.browser.tile_placer:place_move:1300 | Word attempt 1/2: 'DUTY' (score=37)
2026-05-05 17:37:48.503 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:535 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-05 17:37:49.468 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 121406 bytes (attempt 1)
2026-05-05 17:37:49.530 | ERROR   | src.browser.tile_placer:place_move:1316 | Coordinate drift on 'DUTY' (attempt 1/2): Pre-flight anchor probe rejected 'DUTY': rack-tile destination (8,13) is already occupied (V_range=140); engine plans to place 'T' here — aborting candidate list to trigger re-vision
2026-05-05 17:37:49.755 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:535 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-05 17:37:49.756 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1282.8, 751.5) (pass 1/9)
2026-05-05 17:37:50.746 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1287.9, 749.1) (pass 2/9)
2026-05-05 17:37:51.562 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1287.1, 750.9) (pass 3/9)
2026-05-05 17:37:52.423 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1285.7, 749.5) (pass 4/9)
2026-05-05 17:37:53.361 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1287.3, 752.5) (pass 5/9)
2026-05-05 17:37:54.186 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1283.0, 748.6) (pass 6/9)
2026-05-05 17:37:55.094 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1287.9, 752.1) (pass 7/9)
2026-05-05 17:37:55.941 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1284.4, 753.7) (pass 8/9)
2026-05-05 17:37:56.779 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1283.9, 748.8) (pass 9/9)
2026-05-05 17:38:00.213 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120616 bytes (attempt 1)
2026-05-05 17:38:00.217 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:1099 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-05-05 17:38:00.218 | WARNING | __main__:_run:326 | No move accepted (candidates=5) — re-vision + swap fallback
2026-05-05 17:38:03.523 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120962 bytes (attempt 1)
2026-05-05 17:38:03.523 | INFO    | src.vision:extract_board_state:292 | Vision pipeline start — mode=wild
2026-05-05 17:38:03.537 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,54) 1366×657 from 1545×768 canvas
2026-05-05 17:38:03.638 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-05-05 17:38:03.689 | INFO    | src.vision:extract_board_state:298 | Preprocessing complete — 376964 bytes
2026-05-05 17:38:03.689 | INFO    | src.vision.extractor:call_vision_api:99 | Calling Claude Vision API — retry=False
2026-05-05 17:38:06.763 | INFO    | src.vision.extractor:call_vision_api:153 | Claude Vision response received — latency=3.07s  input_tokens=2975  output_tokens=129
2026-05-05 17:38:06.765 | INFO    | src.vision:extract_board_state:304 | Extraction complete (first attempt)
2026-05-05 17:38:06.766 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,12)=T[DW] (9,13)=I[DW] (9,14)=E[DW]
2026-05-05 17:38:06.766 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['E', 'U', 'D', 'Y', 'T', 'E', 'U']
2026-05-05 17:38:06.767 | DEBUG   | src.vision.validator:correct_positions:42 | Position auto-correction skipped: all 3 cell(s) report identical multiplier 'DW' — likely highlight artefact, not real layout signal
2026-05-05 17:38:06.767 | INFO    | src.vision:extract_board_state:323 | Validation result — 1 error(s)
2026-05-05 17:38:06.768 | WARNING | src.vision:extract_board_state:349 | Validation failed (1 errors), retrying: ['Position accuracy suspect: 3/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
2026-05-05 17:38:06.769 | INFO    | src.vision.extractor:call_vision_api:99 | Calling Claude Vision API — retry=True
2026-05-05 17:38:10.037 | INFO    | src.vision.extractor:call_vision_api:153 | Claude Vision response received — latency=3.26s  input_tokens=3030  output_tokens=129
2026-05-05 17:38:10.039 | INFO    | src.vision:extract_board_state:355 | Extraction complete (retry)
2026-05-05 17:38:10.039 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,12)=T[DW] (9,13)=I[DW] (9,14)=E[DW]
2026-05-05 17:38:10.039 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['E', 'U', 'D', 'Y', 'T', 'E', 'U']
2026-05-05 17:38:10.040 | DEBUG   | src.vision.validator:correct_positions:42 | Position auto-correction skipped: all 3 cell(s) report identical multiplier 'DW' — likely highlight artefact, not real layout signal
2026-05-05 17:38:10.040 | INFO    | src.vision:extract_board_state:420 | Validation result after retry — 1 error(s)
2026-05-05 17:38:10.041 | WARNING | src.vision:extract_board_state:480 | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 3/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
2026-05-05 17:38:10.044 | INFO    | src.vision:extract_board_state:537 | Vision pipeline complete — 6.52s  tiles=3  rack_size=7
2026-05-05 17:38:10.124 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 27 blacklisted candidate(s)
2026-05-05 17:38:10.127 | INFO    | src.browser.tile_placer:place_move:1300 | Word attempt 1/2: 'DUTY' (score=37)
2026-05-05 17:38:10.383 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:535 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-05 17:38:11.299 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120364 bytes (attempt 1)
2026-05-05 17:38:11.346 | ERROR   | src.browser.tile_placer:place_move:1316 | Coordinate drift on 'DUTY' (attempt 1/2): Pre-flight anchor probe rejected 'DUTY': rack-tile destination (8,13) is already occupied (V_range=140); engine plans to place 'T' here — aborting candidate list to trigger re-vision
2026-05-05 17:38:11.494 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:535 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-05 17:38:11.494 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1288.5, 752.4) (pass 1/9)
2026-05-05 17:38:12.277 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1283.3, 752.3) (pass 2/9)
2026-05-05 17:38:13.294 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1285.9, 749.9) (pass 3/9)
2026-05-05 17:38:14.172 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1284.0, 750.7) (pass 4/9)
2026-05-05 17:38:15.010 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1283.9, 751.5) (pass 5/9)
2026-05-05 17:38:16.057 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1286.5, 752.3) (pass 6/9)
2026-05-05 17:38:16.976 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1287.0, 752.0) (pass 7/9)
2026-05-05 17:38:17.940 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1287.0, 751.7) (pass 8/9)
2026-05-05 17:38:18.858 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1284.8, 751.5) (pass 9/9)
2026-05-05 17:38:21.230 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 120282 bytes (attempt 1)
2026-05-05 17:38:21.233 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:1099 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-05-05 17:38:21.234 | INFO    | __main__:_run:366 | Turn 1: no move accepted (swap/skip)
2026-05-05 17:38:25.159 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119837 bytes (attempt 1)
2026-05-05 17:38:25.336 | DEBUG   | src.browser.turn_detector:_is_my_turn:171 | Banner orange ratio: 0.3945 (threshold 0.10)
2026-05-05 17:38:25.337 | INFO    | src.browser.turn_detector:poll_turn:663 | Turn state changed: None -> my_turn
2026-05-05 17:38:25.465 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:535 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-05 17:38:26.580 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 119277 bytes (attempt 1)
2026-05-05 17:38:26.622 | INFO    | src.browser.tile_placer:clear_stale_placements:1208 | Pre-turn recall click at (1286.4, 753.8) (pass 1/4)
2026-05-05 17:38:27.523 | INFO    | src.browser.tile_placer:clear_stale_placements:1208 | Pre-turn recall click at (1286.2, 753.2) (pass 2/4)
2026-05-05 17:38:28.517 | INFO    | src.browser.tile_placer:clear_stale_placements:1208 | Pre-turn recall click at (1287.9, 750.6) (pass 3/4)
2026-05-05 17:38:29.385 | INFO    | src.browser.tile_placer:clear_stale_placements:1208 | Pre-turn recall click at (1287.4, 750.1) (pass 4/4)
2026-05-05 17:38:33.654 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122437 bytes (attempt 1)
2026-05-05 17:38:33.654 | INFO    | src.vision:extract_board_state:292 | Vision pipeline start — mode=wild
2026-05-05 17:38:33.668 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,54) 1366×657 from 1545×768 canvas
2026-05-05 17:38:33.762 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-05-05 17:38:33.812 | INFO    | src.vision:extract_board_state:298 | Preprocessing complete — 378803 bytes
2026-05-05 17:38:33.812 | INFO    | src.vision.extractor:call_vision_api:99 | Calling Claude Vision API — retry=False
2026-05-05 17:38:37.243 | INFO    | src.vision.extractor:call_vision_api:153 | Claude Vision response received — latency=3.43s  input_tokens=2975  output_tokens=130
2026-05-05 17:38:37.245 | INFO    | src.vision:extract_board_state:304 | Extraction complete (first attempt)
2026-05-05 17:38:37.245 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,12)=T[DW] (9,13)=I[DW] (9,14)=E[DW]
2026-05-05 17:38:37.250 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['T', 'U', 'D', 'Y', 'E', 'U', 'E']
2026-05-05 17:38:37.250 | DEBUG   | src.vision.validator:correct_positions:42 | Position auto-correction skipped: all 3 cell(s) report identical multiplier 'DW' — likely highlight artefact, not real layout signal
2026-05-05 17:38:37.251 | INFO    | src.vision:extract_board_state:323 | Validation result — 1 error(s)
2026-05-05 17:38:37.251 | WARNING | src.vision:extract_board_state:349 | Validation failed (1 errors), retrying: ['Position accuracy suspect: 3/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
2026-05-05 17:38:37.256 | INFO    | src.vision.extractor:call_vision_api:99 | Calling Claude Vision API — retry=True
2026-05-05 17:42:40.807 | WARNING | __main__:_run:275 | Vision attempt 1 failed: [EXTRACTION_FAILED] Error code: 500 - {'type': 'error', 'error': {'type': 'api_error', 'message': 'Internal server error'}, 'request_id': 'req_011CakDxgygHrhjtNoSrJV2X'}
2026-05-05 17:42:44.260 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122226 bytes (attempt 1)
2026-05-05 17:42:44.261 | INFO    | src.vision:extract_board_state:292 | Vision pipeline start — mode=wild
2026-05-05 17:42:44.290 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,54) 1366×657 from 1545×768 canvas
2026-05-05 17:42:44.519 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-05-05 17:42:44.640 | INFO    | src.vision:extract_board_state:298 | Preprocessing complete — 378776 bytes
2026-05-05 17:42:44.641 | INFO    | src.vision.extractor:call_vision_api:99 | Calling Claude Vision API — retry=False
2026-05-05 17:42:48.012 | INFO    | src.vision.extractor:call_vision_api:153 | Claude Vision response received — latency=3.37s  input_tokens=2975  output_tokens=130
2026-05-05 17:42:48.013 | INFO    | src.vision:extract_board_state:304 | Extraction complete (first attempt)
2026-05-05 17:42:48.013 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,12)=T[DW] (9,13)=I[DW] (9,14)=E[DW]
2026-05-05 17:42:48.013 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['T', 'U', 'D', 'Y', 'E', 'U', 'E']
2026-05-05 17:42:48.014 | DEBUG   | src.vision.validator:correct_positions:42 | Position auto-correction skipped: all 3 cell(s) report identical multiplier 'DW' — likely highlight artefact, not real layout signal
2026-05-05 17:42:48.015 | INFO    | src.vision:extract_board_state:323 | Validation result — 1 error(s)
2026-05-05 17:42:48.015 | WARNING | src.vision:extract_board_state:349 | Validation failed (1 errors), retrying: ['Position accuracy suspect: 3/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
2026-05-05 17:42:48.016 | INFO    | src.vision.extractor:call_vision_api:99 | Calling Claude Vision API — retry=True
2026-05-05 17:42:51.190 | INFO    | src.vision.extractor:call_vision_api:153 | Claude Vision response received — latency=3.17s  input_tokens=3030  output_tokens=132
2026-05-05 17:42:51.191 | INFO    | src.vision:extract_board_state:355 | Extraction complete (retry)
2026-05-05 17:42:51.191 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,12)=T[DW] (9,13)=I[DW] (9,14)=E[DW]
2026-05-05 17:42:51.191 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['T', 'U', 'D', 'Y', 'E', 'U', 'E']
2026-05-05 17:42:51.191 | DEBUG   | src.vision.validator:correct_positions:42 | Position auto-correction skipped: all 3 cell(s) report identical multiplier 'DW' — likely highlight artefact, not real layout signal
2026-05-05 17:42:51.192 | INFO    | src.vision:extract_board_state:420 | Validation result after retry — 1 error(s)
2026-05-05 17:42:51.192 | WARNING | src.vision:extract_board_state:480 | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 3/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
2026-05-05 17:42:51.193 | INFO    | src.vision:extract_board_state:537 | Vision pipeline complete — 6.93s  tiles=3  rack_size=7
2026-05-05 17:42:51.217 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 27 blacklisted candidate(s)
2026-05-05 17:42:51.219 | INFO    | src.browser.tile_placer:place_move:1300 | Word attempt 1/2: 'DUTY' (score=37)
2026-05-05 17:42:51.292 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:535 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-05 17:42:51.914 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122931 bytes (attempt 1)
2026-05-05 17:42:51.935 | ERROR   | src.browser.tile_placer:place_move:1316 | Coordinate drift on 'DUTY' (attempt 1/2): Pre-flight anchor probe rejected 'DUTY': rack-tile destination (8,13) is already occupied (V_range=140); engine plans to place 'T' here — aborting candidate list to trigger re-vision
2026-05-05 17:42:52.012 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:535 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-05 17:42:52.012 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1284.5, 752.5) (pass 1/9)
2026-05-05 17:42:52.874 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1286.9, 750.0) (pass 2/9)
2026-05-05 17:42:53.792 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1282.7, 748.4) (pass 3/9)
2026-05-05 17:42:54.712 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1282.8, 752.0) (pass 4/9)
2026-05-05 17:42:55.608 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1286.5, 752.2) (pass 5/9)
2026-05-05 17:42:56.431 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1283.7, 749.0) (pass 6/9)
2026-05-05 17:42:57.177 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1285.7, 753.4) (pass 7/9)
2026-05-05 17:42:58.114 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1288.6, 749.9) (pass 8/9)
2026-05-05 17:42:59.001 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1283.6, 749.0) (pass 9/9)
2026-05-05 17:43:00.354 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 123114 bytes (attempt 1)
2026-05-05 17:43:00.355 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:1099 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-05-05 17:43:00.355 | WARNING | __main__:_run:326 | No move accepted (candidates=5) — re-vision + swap fallback
2026-05-05 17:43:03.694 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122736 bytes (attempt 1)
2026-05-05 17:43:03.695 | INFO    | src.vision:extract_board_state:292 | Vision pipeline start — mode=wild
2026-05-05 17:43:03.710 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:163 | Grid crop: (87,54) 1366×657 from 1545×768 canvas
2026-05-05 17:43:03.822 | DEBUG   | src.vision.preprocessor:preprocess_screenshot:209 | Preprocessed debug image saved → debug\preprocessed_debug.png
2026-05-05 17:43:03.874 | INFO    | src.vision:extract_board_state:298 | Preprocessing complete — 379526 bytes
2026-05-05 17:43:03.875 | INFO    | src.vision.extractor:call_vision_api:99 | Calling Claude Vision API — retry=False
2026-05-05 17:43:07.702 | INFO    | src.vision.extractor:call_vision_api:153 | Claude Vision response received — latency=3.82s  input_tokens=2975  output_tokens=130
2026-05-05 17:43:07.702 | INFO    | src.vision:extract_board_state:304 | Extraction complete (first attempt)
2026-05-05 17:43:07.703 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,13)=T[DW] (9,14)=I[DW] (9,15)=E[DW]
2026-05-05 17:43:07.703 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['U', 'T', 'U', 'E', 'E', 'Y', 'D']
2026-05-05 17:43:07.703 | DEBUG   | src.vision.validator:correct_positions:42 | Position auto-correction skipped: all 3 cell(s) report identical multiplier 'DW' — likely highlight artefact, not real layout signal
2026-05-05 17:43:07.703 | INFO    | src.vision:extract_board_state:323 | Validation result — 1 error(s)
2026-05-05 17:43:07.704 | WARNING | src.vision:extract_board_state:349 | Validation failed (1 errors), retrying: ['Position accuracy suspect: 2/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
2026-05-05 17:43:07.704 | INFO    | src.vision.extractor:call_vision_api:99 | Calling Claude Vision API — retry=True
2026-05-05 17:43:10.852 | INFO    | src.vision.extractor:call_vision_api:153 | Claude Vision response received — latency=3.15s  input_tokens=3030  output_tokens=131
2026-05-05 17:43:10.853 | INFO    | src.vision:extract_board_state:355 | Extraction complete (retry)
2026-05-05 17:43:10.853 | DEBUG   | src.vision:_log_extracted_state:49 | Vision extracted cells: (9,12)=T[DW] (9,13)=I[DW] (9,14)=E[DW]
2026-05-05 17:43:10.853 | DEBUG   | src.vision:_log_extracted_state:50 | Vision extracted rack: ['U', 'T', 'U', 'E', 'E', 'Y', 'D']
2026-05-05 17:43:10.853 | DEBUG   | src.vision.validator:correct_positions:42 | Position auto-correction skipped: all 3 cell(s) report identical multiplier 'DW' — likely highlight artefact, not real layout signal
2026-05-05 17:43:10.853 | INFO    | src.vision:extract_board_state:380 | Retry is a uniform (+0, -1) shift of first attempt — skipping merge to avoid duplicate-tile phantoms.
2026-05-05 17:43:10.854 | INFO    | src.vision:extract_board_state:420 | Validation result after retry — 1 error(s)
2026-05-05 17:43:10.854 | WARNING | src.vision:extract_board_state:480 | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 3/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
2026-05-05 17:43:10.855 | INFO    | src.vision:extract_board_state:537 | Vision pipeline complete — 7.16s  tiles=3  rack_size=7
2026-05-05 17:43:10.886 | DEBUG   | src.engine.rejected_words:filter_moves:90 | rejected_words: filtered 27 blacklisted candidate(s)
2026-05-05 17:43:10.887 | INFO    | src.browser.tile_placer:place_move:1300 | Word attempt 1/2: 'DUTY' (score=37)
2026-05-05 17:43:10.962 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:535 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-05 17:43:11.565 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122884 bytes (attempt 1)
2026-05-05 17:43:11.581 | ERROR   | src.browser.tile_placer:place_move:1316 | Coordinate drift on 'DUTY' (attempt 1/2): Pre-flight anchor probe rejected 'DUTY': rack-tile destination (8,13) is already occupied (V_range=140); engine plans to place 'T' here — aborting candidate list to trigger re-vision
2026-05-05 17:43:11.640 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:535 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-05 17:43:11.640 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1285.8, 751.6) (pass 1/9)
2026-05-05 17:43:12.370 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1284.5, 748.7) (pass 2/9)
2026-05-05 17:43:13.305 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1282.7, 750.4) (pass 3/9)
2026-05-05 17:43:14.086 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1286.1, 749.6) (pass 4/9)
2026-05-05 17:43:15.000 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1288.5, 751.3) (pass 5/9)
2026-05-05 17:43:15.785 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1285.0, 752.2) (pass 6/9)
2026-05-05 17:43:16.674 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1282.7, 749.6) (pass 7/9)
2026-05-05 17:43:17.524 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1285.4, 753.9) (pass 8/9)
2026-05-05 17:43:18.332 | INFO    | src.browser.tile_placer:_recall_tiles:1146 | Clicking recall button at (1285.2, 750.4) (pass 9/9)
2026-05-05 17:43:19.667 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122405 bytes (attempt 1)
2026-05-05 17:43:19.668 | DEBUG   | src.browser.tile_placer:_save_debug_screenshot:1099 | Debug screenshot saved -> debug\tile_placer\post_recall_attempt1.png
2026-05-05 17:43:19.669 | INFO    | __main__:_run:366 | Turn 2: no move accepted (swap/skip)
2026-05-05 17:43:22.983 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122328 bytes (attempt 1)
2026-05-05 17:43:23.033 | DEBUG   | src.browser.turn_detector:_is_my_turn:171 | Banner orange ratio: 0.3629 (threshold 0.10)
2026-05-05 17:43:23.033 | INFO    | src.browser.turn_detector:poll_turn:663 | Turn state changed: None -> my_turn
2026-05-05 17:43:23.096 | DEBUG   | src.browser.tile_placer:_get_canvas_bbox:535 | Using iframe bbox: 1545x768 @ (375,112)
2026-05-05 17:43:23.759 | DEBUG   | src.browser.capture:capture_canvas:155 | Game screenshot captured — 122881 bytes (attempt 1)
2026-05-05 17:43:23.774 | INFO    | src.browser.tile_placer:clear_stale_placements:1208 | Pre-turn recall click at (1283.9, 750.2) (pass 1/4)
```

## Subprocess stderr (tail)
```
[32m17:38:14[0m | [1mINFO   [0m | Clicking recall button at (1284.0, 750.7) (pass 4/9)
[32m17:38:15[0m | [1mINFO   [0m | Clicking recall button at (1283.9, 751.5) (pass 5/9)
[32m17:38:16[0m | [1mINFO   [0m | Clicking recall button at (1286.5, 752.3) (pass 6/9)
[32m17:38:16[0m | [1mINFO   [0m | Clicking recall button at (1287.0, 752.0) (pass 7/9)
[32m17:38:17[0m | [1mINFO   [0m | Clicking recall button at (1287.0, 751.7) (pass 8/9)
[32m17:38:18[0m | [1mINFO   [0m | Clicking recall button at (1284.8, 751.5) (pass 9/9)
[32m17:38:21[0m | [1mINFO   [0m | Turn 1: no move accepted (swap/skip)
[32m17:38:25[0m | [1mINFO   [0m | Turn state changed: None -> my_turn
[32m17:38:26[0m | [1mINFO   [0m | Pre-turn recall click at (1286.4, 753.8) (pass 1/4)
[32m17:38:27[0m | [1mINFO   [0m | Pre-turn recall click at (1286.2, 753.2) (pass 2/4)
[32m17:38:28[0m | [1mINFO   [0m | Pre-turn recall click at (1287.9, 750.6) (pass 3/4)
[32m17:38:29[0m | [1mINFO   [0m | Pre-turn recall click at (1287.4, 750.1) (pass 4/4)
[32m17:38:33[0m | [1mINFO   [0m | Vision pipeline start — mode=wild
[32m17:38:33[0m | [1mINFO   [0m | Preprocessing complete — 378803 bytes
[32m17:38:33[0m | [1mINFO   [0m | Calling Claude Vision API — retry=False
[32m17:38:37[0m | [1mINFO   [0m | Claude Vision response received — latency=3.43s  input_tokens=2975  output_tokens=130
[32m17:38:37[0m | [1mINFO   [0m | Extraction complete (first attempt)
[32m17:38:37[0m | [1mINFO   [0m | Validation result — 1 error(s)
[32m17:38:37[0m | [33m[1mWARNING[0m | Validation failed (1 errors), retrying: ['Position accuracy suspect: 3/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m17:38:37[0m | [1mINFO   [0m | Calling Claude Vision API — retry=True
[32m17:42:40[0m | [33m[1mWARNING[0m | Vision attempt 1 failed: [EXTRACTION_FAILED] Error code: 500 - {'type': 'error', 'error': {'type': 'api_error', 'message': 'Internal server error'}, 'request_id': 'req_011CakDxgygHrhjtNoSrJV2X'}
[32m17:42:44[0m | [1mINFO   [0m | Vision pipeline start — mode=wild
[32m17:42:44[0m | [1mINFO   [0m | Preprocessing complete — 378776 bytes
[32m17:42:44[0m | [1mINFO   [0m | Calling Claude Vision API — retry=False
[32m17:42:48[0m | [1mINFO   [0m | Claude Vision response received — latency=3.37s  input_tokens=2975  output_tokens=130
[32m17:42:48[0m | [1mINFO   [0m | Extraction complete (first attempt)
[32m17:42:48[0m | [1mINFO   [0m | Validation result — 1 error(s)
[32m17:42:48[0m | [33m[1mWARNING[0m | Validation failed (1 errors), retrying: ['Position accuracy suspect: 3/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m17:42:48[0m | [1mINFO   [0m | Calling Claude Vision API — retry=True
[32m17:42:51[0m | [1mINFO   [0m | Claude Vision response received — latency=3.17s  input_tokens=3030  output_tokens=132
[32m17:42:51[0m | [1mINFO   [0m | Extraction complete (retry)
[32m17:42:51[0m | [1mINFO   [0m | Validation result after retry — 1 error(s)
[32m17:42:51[0m | [33m[1mWARNING[0m | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 3/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m17:42:51[0m | [1mINFO   [0m | Vision pipeline complete — 6.93s  tiles=3  rack_size=7
[32m17:42:51[0m | [1mINFO   [0m | Word attempt 1/2: 'DUTY' (score=37)
[32m17:42:51[0m | [31m[1mERROR  [0m | Coordinate drift on 'DUTY' (attempt 1/2): Pre-flight anchor probe rejected 'DUTY': rack-tile destination (8,13) is already occupied (V_range=140); engine plans to place 'T' here — aborting candidate list to trigger re-vision
[32m17:42:52[0m | [1mINFO   [0m | Clicking recall button at (1284.5, 752.5) (pass 1/9)
[32m17:42:52[0m | [1mINFO   [0m | Clicking recall button at (1286.9, 750.0) (pass 2/9)
[32m17:42:53[0m | [1mINFO   [0m | Clicking recall button at (1282.7, 748.4) (pass 3/9)
[32m17:42:54[0m | [1mINFO   [0m | Clicking recall button at (1282.8, 752.0) (pass 4/9)
[32m17:42:55[0m | [1mINFO   [0m | Clicking recall button at (1286.5, 752.2) (pass 5/9)
[32m17:42:56[0m | [1mINFO   [0m | Clicking recall button at (1283.7, 749.0) (pass 6/9)
[32m17:42:57[0m | [1mINFO   [0m | Clicking recall button at (1285.7, 753.4) (pass 7/9)
[32m17:42:58[0m | [1mINFO   [0m | Clicking recall button at (1288.6, 749.9) (pass 8/9)
[32m17:42:59[0m | [1mINFO   [0m | Clicking recall button at (1283.6, 749.0) (pass 9/9)
[32m17:43:00[0m | [33m[1mWARNING[0m | No move accepted (candidates=5) — re-vision + swap fallback
[32m17:43:03[0m | [1mINFO   [0m | Vision pipeline start — mode=wild
[32m17:43:03[0m | [1mINFO   [0m | Preprocessing complete — 379526 bytes
[32m17:43:03[0m | [1mINFO   [0m | Calling Claude Vision API — retry=False
[32m17:43:07[0m | [1mINFO   [0m | Claude Vision response received — latency=3.82s  input_tokens=2975  output_tokens=130
[32m17:43:07[0m | [1mINFO   [0m | Extraction complete (first attempt)
[32m17:43:07[0m | [1mINFO   [0m | Validation result — 1 error(s)
[32m17:43:07[0m | [33m[1mWARNING[0m | Validation failed (1 errors), retrying: ['Position accuracy suspect: 2/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m17:43:07[0m | [1mINFO   [0m | Calling Claude Vision API — retry=True
[32m17:43:10[0m | [1mINFO   [0m | Claude Vision response received — latency=3.15s  input_tokens=3030  output_tokens=131
[32m17:43:10[0m | [1mINFO   [0m | Extraction complete (retry)
[32m17:43:10[0m | [1mINFO   [0m | Retry is a uniform (+0, -1) shift of first attempt — skipping merge to avoid duplicate-tile phantoms.
[32m17:43:10[0m | [1mINFO   [0m | Validation result after retry — 1 error(s)
[32m17:43:10[0m | [33m[1mWARNING[0m | Position accuracy check failed after retry — proceeding with auto-corrected multipliers: ['Position accuracy suspect: 3/3 multiplier mismatches — tile coordinates may be off. Re-count positions using the center star at (9,13) as reference.']
[32m17:43:10[0m | [1mINFO   [0m | Vision pipeline complete — 7.16s  tiles=3  rack_size=7
[32m17:43:10[0m | [1mINFO   [0m | Word attempt 1/2: 'DUTY' (score=37)
[32m17:43:11[0m | [31m[1mERROR  [0m | Coordinate drift on 'DUTY' (attempt 1/2): Pre-flight anchor probe rejected 'DUTY': rack-tile destination (8,13) is already occupied (V_range=140); engine plans to place 'T' here — aborting candidate list to trigger re-vision
[32m17:43:11[0m | [1mINFO   [0m | Clicking recall button at (1285.8, 751.6) (pass 1/9)
[32m17:43:12[0m | [1mINFO   [0m | Clicking recall button at (1284.5, 748.7) (pass 2/9)
[32m17:43:13[0m | [1mINFO   [0m | Clicking recall button at (1282.7, 750.4) (pass 3/9)
[32m17:43:14[0m | [1mINFO   [0m | Clicking recall button at (1286.1, 749.6) (pass 4/9)
[32m17:43:15[0m | [1mINFO   [0m | Clicking recall button at (1288.5, 751.3) (pass 5/9)
[32m17:43:15[0m | [1mINFO   [0m | Clicking recall button at (1285.0, 752.2) (pass 6/9)
[32m17:43:16[0m | [1mINFO   [0m | Clicking recall button at (1282.7, 749.6) (pass 7/9)
[32m17:43:17[0m | [1mINFO   [0m | Clicking recall button at (1285.4, 753.9) (pass 8/9)
[32m17:43:18[0m | [1mINFO   [0m | Clicking recall button at (1285.2, 750.4) (pass 9/9)
[32m17:43:19[0m | [1mINFO   [0m | Turn 2: no move accepted (swap/skip)
[32m17:43:23[0m | [1mINFO   [0m | Turn state changed: None -> my_turn
[32m17:43:23[0m | [1mINFO   [0m | Pre-turn recall click at (1283.9, 750.2) (pass 1/4)
[32m17:43:24[0m | [1mINFO   [0m | Pre-turn recall click at (1287.3, 750.8) (pass 2/4)
[32m17:43:25[0m | [1mINFO   [0m | Pre-turn recall click at (1282.9, 749.3) (pass 3/4)
[32m17:43:26[0m | [1mINFO   [0m | Pre-turn recall click at (1284.2, 753.7) (pass 4/4)
[32m17:43:30[0m | [1mINFO   [0m | Vision pipeline start — mode=wild
[32m17:43:30[0m | [1mINFO   [0m | Preprocessing complete — 378897 bytes
[32m17:43:30[0m | [1mINFO   [0m | Calling Claude Vision API — retry=False
```

## git status --short
```
M data/rejected_words.txt
 M logs/_autoplay_stderr.tmp
 M logs/auto_debug.log
 M logs/auto_debug_console.log
 M logs/autoplay.log
 M src/browser/tile_placer.py
 M src/browser/turn_detector.py
 M tests/test_tile_placer.py
 M tests/test_turn_detector.py
?? CLAUDE.md
?? docs/
?? scripts/extract_info_images.py
?? scripts/tune_occupancy_probe.py
```

## git diff --stat
```
data/rejected_words.txt      |   20 +
 logs/_autoplay_stderr.tmp    | 1334 +++---------------------
 logs/auto_debug.log          |   13 +-
 logs/auto_debug_console.log  |   13 +-
 logs/autoplay.log            | 2348 ++++++++++++++++++++++++++++++++++++++++++
 src/browser/tile_placer.py   |  304 +++++-
 src/browser/turn_detector.py |   37 +-
 tests/test_tile_placer.py    |  288 +++++-
 tests/test_turn_detector.py  |    1 +
 9 files changed, 3117 insertions(+), 1241 deletions(-)
```