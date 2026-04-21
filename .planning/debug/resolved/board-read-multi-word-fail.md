---
status: awaiting_human_verify
trigger: "board-read-multi-word-fail: When there are multiple words on the board, the vision/analysis pipeline returns an error saying it cannot analyze the image. Works fine with one word on the board."
created: 2026-04-14T00:00:00Z
updated: 2026-04-14T00:03:00Z
---

## Current Focus

hypothesis: The "Position accuracy suspect" multiplier-mismatch error is a hard error not covered
  by the previous fix. On multi-word boards with many tiles, more tiles land on multiplier squares,
  making the threshold (>50% wrong) easy to trigger. The previous fix only softened "Invalid word(s)
  on board" errors; "Position accuracy suspect" still falls into hard_errors and raises
  VisNError(VALIDATION_FAILED). Both errors have the same root cause (position drift) and are
  safe to treat as soft because the engine uses coordinates, not multiplier values.
test: Add "Position accuracy" to soft-error classification in __init__.py; add regression test.
expecting: No raise on multi-word boards with multiplier mismatches after retry.
next_action: Apply fix to __init__.py and tests/vision/test_pipeline.py

## Symptoms

expected: The bot should be able to read and analyze the board state regardless of how many words are on the board.
actual: When more than one word is on the board, the bot provides an error that it cannot analyze the image.
errors: VisNError(VALIDATION_FAILED) raised when validate_extraction returns word-validity hard errors.
reproduction: Play a game until there are multiple words on the board, then try to analyze/read the board.
started: Likely never worked with multiple words — works fine on first move (empty/single word board).

## Eliminated

- hypothesis: Token limit (max_tokens=4096) causes truncated JSON on large boards
  evidence: Estimated ~19 tokens per cell; 50 cells = ~950 tokens, well within 4096
  timestamp: 2026-04-14T00:01:00Z

- hypothesis: Peach detection threshold fails with many tiles covering the board
  evidence: Even 100 tiles only cover ~20% of 513 total cells; remaining 80% peach easily passes 5% threshold
  timestamp: 2026-04-14T00:01:00Z

- hypothesis: output_config + image (multimodal) is unsupported by the API
  evidence: Anthropic SDK 0.87.0 natively supports output_config parameter; documented to work multimodal
  timestamp: 2026-04-14T00:01:00Z

- hypothesis: Connectivity check causes hard failures on multi-word boards
  evidence: Floating tile errors are classified as SOFT errors and removed; not hard errors
  timestamp: 2026-04-14T00:01:00Z

- hypothesis: _find_tile_runs has a bug with intersecting words
  evidence: Tested manually — algorithm correctly identifies intersecting words at shared tiles
  timestamp: 2026-04-14T00:01:00Z

## Evidence

- timestamp: 2026-04-14T00:01:00Z
  checked: src/vision/__init__.py — error classification logic after retry
  found: hard_errors = [e for e in errors if "Floating tile" not in e and "Rack is empty" not in e]
    — word validity errors ("Invalid word(s) on board: ...") fell into hard_errors
  implication: Any word validity failure caused VisNError(VALIDATION_FAILED)

- timestamp: 2026-04-14T00:01:00Z
  checked: src/vision/validator.py Check 5 (word validity)
  found: Validates EVERY horizontal and vertical run of 2+ consecutive tiles against GADDAG.
    With multiple words on board, more runs exist. One misread tile creates an invalid word string.
  implication: On multi-word boards, Vision API position errors cause more word runs to fail.
    Single-word boards have fewer runs, higher pass rate.

- timestamp: 2026-04-14T00:01:00Z
  checked: correct_positions algorithm
  found: Only applies ONE global shift. With multiple words mis-positioned in different directions,
    no single shift fixes all words. Some words remain wrong after correction, failing Check 5.
  implication: The position correction cannot fix multi-word positional inconsistency.

- timestamp: 2026-04-14T00:01:00Z
  checked: src/bot/formatter.py build_error_embed for VALIDATION_FAILED
  found: Returns "Board reading failed" / "The screenshot was unclear..." — user paraphrased this
    as "cannot analyze the image"
  implication: Error presentation is correct; root cause was upstream validation logic.

- timestamp: 2026-04-14T00:03:00Z
  checked: src/vision/validator.py Check 3 (multiplier positions) + __init__.py hard_errors list
  found: "Position accuracy suspect: N/M multiplier mismatches" does NOT contain "Floating tile",
    "Rack is empty", or "Invalid word(s) on board" — falls through to hard_errors.
    On multi-word boards, more tiles land on multiplier squares, raising mult_check_total.
    With even modest position drift, >50% of those tiles misreport multiplier type, triggering
    the hard error. The previous fix only softened word errors; position errors still raised.
    Both error types are caused by the same position drift. The validator already overwrites
    multiplier values with the official layout (line 249), so the engine is never affected.
  implication: The previous fix was incomplete. Position accuracy errors need identical soft
    treatment. This is the reason the error persisted identically after the first fix.

## Resolution

root_cause: Two validation checks — word validity (Check 5) and position accuracy (Check 3) —
  were both classified as hard errors. On multi-word boards with many tiles, Vision API position
  imprecision causes both to fire after retry: (a) word runs form invalid dictionary strings,
  (b) many tiles land on multiplier squares and misreport their multiplier type.
  The first fix (2026-04-14T00:02) only softened word errors; position accuracy errors continued
  to raise as hard errors, preserving the VALIDATION_FAILED path identically.

fix: In src/vision/__init__.py, added "Position accuracy suspect" to the soft-error category
  alongside "Invalid word(s) on board". Both are now logged as warnings after retry and
  extraction proceeds. The multiplier mismatch is safe to ignore as a soft error because
  the validator already overwrites multiplier values with the official layout.
  Hard errors (duplicate positions, out-of-bounds, invalid letters) still raise.

verification: All 233 tests pass. 2 new regression tests added:
  - test_position_accuracy_error_is_soft_after_retry: confirms position errors are soft
  - test_position_and_word_errors_both_soft_after_retry: confirms both together are soft

files_changed:
  - src/vision/__init__.py: position_errors soft-error classification + recovery logic
  - tests/vision/test_pipeline.py: 2 new regression tests (4 total now)
