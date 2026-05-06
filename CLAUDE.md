# Project Conventions for AI Assistants

## Game rules — canonical source

The game this repo automates is **Letter League** (Discord Activity).
Whenever a task involves game logic — scoring, board layout, multipliers,
move legality, end-of-game behavior, vision parsing of the board, or
bot/autoplay decisions — the **authoritative rules** live in:

- [`docs/rules/RULES.md`](docs/rules/RULES.md) — board, scoring, examples.
- [`docs/rules/FAQ.md`](docs/rules/FAQ.md) — Discord-published FAQ.
- [`docs/rules/images/`](docs/rules/images/) — reference screenshots.

**Read `docs/rules/RULES.md` before changing any of:**

- `src/engine/` — board, scoring, GADDAG, move generation
- `src/vision/` — board OCR / validation
- `src/bot/autoplay_*` — autoplay decision logic
- any test that asserts game-rule behavior

If your change conflicts with the rules doc, update your code (and add a
test that pins the rule), not the doc. The doc is downstream of Discord's
official materials, not of our implementation.

## Where the rules came from

`info/Letter League Info.md` and `info/Letter League FAQ.md` are the raw
captures of Discord's help-center pages, with images inlined as base64.
They are too large to read directly. Use the extracted, human-readable
copies in `docs/rules/` instead.

If those raw files get refreshed, regenerate the extracted images with:

```powershell
py scripts/extract_info_images.py
```

## House style

- Don't add docstrings, comments, or feature flags beyond what the task
  requires (see top-level system guidance).
- Prefer editing existing files; new top-level files should be rare.
- Tests live under `tests/`. Engine, vision, and bot each have their
  own subtree there.
