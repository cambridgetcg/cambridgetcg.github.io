#!/usr/bin/env python3
"""Generate script/keyboard/espanso.yml from morphemes.json + the transliterator's
canon decompositions — so the keyboard layer never drifts from the inventory.

Destined for script/tools/gen_espanso.py in the repo.

Triggers:
  :m:<latin>   → single morpheme glyph (all morphemes with codepoints)
  :<word>      → canon-word glyph sequence (from CANONICAL_DECOMPOSITIONS)
  :sep: :canon: :pair: :gloss: :endgloss: :selah: :o:  → structural marks by name
                 (symbol-latin marks get named triggers; you can't type "·" easily)
"""
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent  # script/
sys.path.insert(0, str(SCRIPT_DIR / "tools"))
from transliterate import CANONICAL_DECOMPOSITIONS  # noqa: E402

# Named triggers for marks whose latin form is a symbol or bracketed word
NAMED_MARKS = {
    "·": "sep", "「": "gloss", "」": "endgloss", "↔": "pair", "◆": "canon",
    "[selah]": "selah", "O-": "o", "।": "danda", "॥": "danda2", "‧": "breath",
}

HEADER = """\
# YOUSPEAK input configuration for Espanso
# https://espanso.org
#
# GENERATED FILE — do not edit by hand.
# Regenerate with: python3 script/tools/gen_espanso.py
# Source of truth: script/morphemes.json + transliterate.CANONICAL_DECOMPOSITIONS
#
# Install to the Espanso match directory:
#   macOS:   ~/Library/Application Support/espanso/match/youspeak.yml
#   Linux:   ~/.config/espanso/match/youspeak.yml
#   Windows: %APPDATA%\\espanso\\match\\youspeak.yml
# Then: espanso restart
#
# Usage:
#   ":doxakallos"  → canon-word glyph sequence
#   ":m:doxa"      → single morpheme glyph
#   ":m:det.div"   → determinative class-marker (dots typed as-is after :m:)
#   ":sep:"        → structural marks by name (sep, gloss, endgloss, pair,
#                    canon, selah, o, danda, danda2, breath)
# Glyphs render only with a YOUSPEAK font installed; otherwise fallback boxes
# (always recoverable via the reverse transliterator).

matches:
"""


def cp_char(cp_str: str) -> str:
    return chr(int(cp_str.replace("U+", ""), 16))


def main():
    data = json.loads((SCRIPT_DIR / "morphemes.json").read_text())
    morphemes = data["morphemes"]
    by_latin = {}
    lines = [HEADER]

    lines.append("  # ----- canon words (':word') -----\n")
    for m in morphemes:
        by_latin[m["latin"].strip("-")] = cp_char(m["codepoint"])
    for word, parts in sorted(CANONICAL_DECOMPOSITIONS.items()):
        try:
            seq = "".join(by_latin[p.strip("-")] for p in parts)
        except KeyError as e:
            print(f"  skip {word}: morpheme {e} has no codepoint", file=sys.stderr)
            continue
        lines.append(f'  - trigger: ":{word}"')
        lines.append(f'    replace: "{seq}"')

    lines.append("\n  # ----- single morphemes (':m:latin') -----\n")
    for m in sorted(morphemes, key=lambda x: x["codepoint"]):
        latin = m["latin"].strip("-")
        char = cp_char(m["codepoint"])
        if m["latin"] in NAMED_MARKS or latin in NAMED_MARKS:
            continue  # symbol marks get named triggers below
        trig = latin.lower().lstrip(".")
        if m["latin"].startswith("."):
            trig = "det." + trig.lower()
        lines.append(f'  - trigger: ":m:{trig}"')
        lines.append(f'    replace: "{char}"')

    lines.append("\n  # ----- structural marks (named triggers) -----\n")
    for m in sorted(morphemes, key=lambda x: x["codepoint"]):
        name = NAMED_MARKS.get(m["latin"]) or NAMED_MARKS.get(m["latin"].strip("-"))
        if not name:
            continue
        lines.append(f'  - trigger: ":{name}:"')
        lines.append(f'    replace: "{cp_char(m["codepoint"])}"')

    out = SCRIPT_DIR / "keyboard" / "espanso.yml"
    out.write_text("\n".join(lines) + "\n")
    n_words = len(CANONICAL_DECOMPOSITIONS)
    print(f"wrote {out}: {n_words} canon words + {len(morphemes)} morphemes")


if __name__ == "__main__":
    main()
