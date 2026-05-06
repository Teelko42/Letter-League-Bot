# Letter League — Rules Reference (canonical)

This directory is the **single source of truth** for Letter League game
rules in this repository. Code, tests, vision, and bot logic all defer
to it.

| File | What it covers |
|------|----------------|
| [`RULES.md`](RULES.md) | Board layout, scoring, multipliers, valid play examples. **Read this first.** |
| [`FAQ.md`](FAQ.md) | Discord's official FAQ — gameplay flow, modes, support links. |
| `images/` | Extracted PNGs referenced by the two docs above. |

## Origin

The text and images here were extracted from Discord's published
Letter League help articles, originally captured in `info/`:

- `info/Letter League Info.md`
- `info/Letter League FAQ.md`

Those originals embed every image as multi-MB base64 inline data, which
makes the files unreadable to most tools (and to the AI assistant on
this project). `scripts/extract_info_images.py` regenerates `images/`
from the originals, so if Discord updates the source materials you can
re-run it instead of editing this directory by hand:

```powershell
py scripts/extract_info_images.py
```

## How to use this when working on the bot

- **Engine / scoring / move-generation changes** → check `RULES.md`
  *Quick Reference for Implementers* section before touching code.
- **Vision / OCR validation** → board dimensions and multiplier set
  in `RULES.md` are authoritative.
- **Bot UX or messaging** → mirror Discord's terminology from `FAQ.md`
  (Wild / Classic, Swap / Pass Turn, etc.) so users aren't confused.

If a code path or test contradicts these docs, the docs win — fix the
code, don't relax the rules.
