"""One-shot helper: pulls base64-encoded images out of info/*.md and
writes them to docs/rules/images/ as PNG files.

Run from repo root: `python scripts/extract_info_images.py`
"""

from __future__ import annotations

import base64
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "info": ROOT / "info" / "Letter League Info.md",
    "faq": ROOT / "info" / "Letter League FAQ.md",
}
OUT_DIR = ROOT / "docs" / "rules" / "images"

INFO_NAMES = {
    1: "board",
    2: "rules-overview",
    3: "rules-letters",
    4: "rules-multipliers",
    5: "rules-bonus",
}
FAQ_NAMES = {
    1: "faq-author-avatar",
    2: "faq-lobby",
    3: "faq-game-settings",
    4: "faq-tile-placement",
    5: "faq-multiplier-squares",
    6: "faq-swap-pass",
    7: "faq-winner",
    8: "faq-game-info",
}

REF_PATTERN = re.compile(
    r"^\[image(?P<idx>\d+)\]:\s*<?data:image/png;base64,(?P<data>[A-Za-z0-9+/=]+)>?\s*$"
)


def extract(source_key: str, path: Path, name_map: dict[int, str]) -> list[Path]:
    written: list[Path] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = REF_PATTERN.match(line.strip())
        if not m:
            continue
        idx = int(m.group("idx"))
        data = m.group("data")
        slug = name_map.get(idx, f"{source_key}-image{idx}")
        out = OUT_DIR / f"{slug}.png"
        out.write_bytes(base64.b64decode(data))
        written.append(out)
    return written


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written = extract("info", SOURCES["info"], INFO_NAMES)
    written += extract("faq", SOURCES["faq"], FAQ_NAMES)
    for p in written:
        print(f"wrote {p.relative_to(ROOT)} ({p.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
