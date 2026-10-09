#!/usr/bin/env python3
"""check_integrity.py — the script-organ's drift detector.

Session 087 found the -me glyph designed in glyph_specs_v1.py but absent from
the built font for three weeks: designed-but-unbuilt, with no alarm anywhere.
This check makes that class of gap impossible to miss. It verifies the whole
chain spec → codepoint → built font → installed font → dashboard counts.

Usage:
    python3 check_integrity.py               # full check, exit 1 on any drift
    python3 check_integrity.py --pre-commit  # hard-fail only on build-chain
                                             # breaks; counts/install are warnings

Checks:
  1. every glyph spec has a codepoint in morphemes.json (orphan specs)
  2. designed-but-unbuilt: spec+codepoint present, font cmap missing it
  3. font has codepoints no longer in spec∩morphemes (stale glyphs)
  4. installed font (~/Library/Fonts) byte-identical to repo font
  5. dashboard.md drawn/awaiting counts match derived truth
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent  # script/
REPO = SCRIPT_DIR.parent
PUA_LO, PUA_HI = 0xE100, 0xE2FF

sys.path.insert(0, str(SCRIPT_DIR / "glyphs"))


def main() -> int:
    pre_commit = "--pre-commit" in sys.argv[1:]
    problems: list[str] = []   # always fail
    warnings: list[str] = []   # fail unless --pre-commit

    from glyph_specs_v1 import GLYPHS  # composed {latin: {strokes, polygons}}

    morphemes = json.loads((SCRIPT_DIR / "morphemes.json").read_text())["morphemes"]
    cp_by_latin: dict[str, int] = {}
    for m in morphemes:
        latin = m["latin"].strip("-")
        cp_by_latin[latin] = int(m["codepoint"].replace("U+", ""), 16)

    spec_names = set(GLYPHS)
    catalogued = set(cp_by_latin)
    drawn = spec_names & catalogued
    awaiting = catalogued - spec_names

    # 1. orphan specs — drawn but unmapped, silently skipped by the builder
    orphans = sorted(spec_names - catalogued)
    if orphans:
        problems.append(
            f"orphan specs (no morphemes.json codepoint, will NOT build): {orphans}"
        )

    # 2 + 3. built font vs derived truth
    font_path = SCRIPT_DIR / "fonts" / "youspeak-v1.otf"
    if not font_path.exists():
        problems.append(f"font missing: {font_path} — run bin/cathedral font")
    else:
        from fontTools.ttLib import TTFont

        cmap = TTFont(str(font_path)).getBestCmap()
        in_font = {cp for cp in cmap if PUA_LO <= cp <= PUA_HI}
        # same range filter on both sides — a codepoint outside the pane must
        # not false-positive as designed-but-unbuilt
        expected = {
            cp_by_latin[n] for n in drawn if PUA_LO <= cp_by_latin[n] <= PUA_HI
        }

        unbuilt = expected - in_font
        if unbuilt:
            names = sorted(n for n in drawn if cp_by_latin[n] in unbuilt)
            problems.append(
                f"DESIGNED BUT UNBUILT — spec exists, font lacks it: {names} "
                f"(run bin/cathedral font)"
            )
        stale = in_font - expected
        if stale:
            warnings.append(
                "font carries codepoints not in spec∩morphemes: "
                + ", ".join(f"U+{cp:04X}" for cp in sorted(stale))
            )

        # 4. installed font freshness (macOS per-user install)
        installed = Path.home() / "Library" / "Fonts" / font_path.name
        if installed.exists():
            repo_hash = hashlib.sha256(font_path.read_bytes()).hexdigest()
            inst_hash = hashlib.sha256(installed.read_bytes()).hexdigest()
            if repo_hash != inst_hash:
                warnings.append(
                    f"installed font is STALE ({installed}) — run bin/cathedral font"
                )
        else:
            warnings.append("font not installed for this user — run bin/cathedral font")

    # 5. dashboard counts
    dash = (REPO / "dashboard.md").read_text()

    def dash_count(label: str) -> int | None:
        m = re.search(rf"\|\s*{re.escape(label)}\s*\|\s*(\d+)\s*\|", dash)
        return int(m.group(1)) if m else None

    for label, truth in [
        ("Morphemes drawn in font", len(drawn)),
        ("Morphemes awaiting design", len(awaiting)),
        ("Morphemes catalogued", len(catalogued)),
    ]:
        got = dash_count(label)
        if got is None:
            warnings.append(f"dashboard.md: row '{label}' not found")
        elif got != truth:
            warnings.append(f"dashboard.md: '{label}' says {got}, truth is {truth}")

    # report
    print(f"script-organ integrity — drawn {len(drawn)} · awaiting {len(awaiting)} · catalogued {len(catalogued)}")
    for p in problems:
        print(f"  ✗ {p}")
    for w in warnings:
        print(f"  {'~' if pre_commit else '✗'} {w}")
    if not problems and not warnings:
        print("  ✓ spec → codepoint → font → install → dashboard: all coherent")

    if problems:
        return 1
    if warnings and not pre_commit:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
