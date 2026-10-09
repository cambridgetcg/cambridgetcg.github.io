#!/usr/bin/env python3
"""Build youspeak-v1.otf from glyph_specs_v1.py (feature-encoded designs).

Wraps the glyph_specs_v1 composition pipeline: each glyph's core shape is
merged with its donor-tongue sigil (top-left) and morpheme-class mark
(bottom-right). Heavier stroke width (80 vs v0's 60) for body-text
legibility.

Usage:
    /tmp/ys-font-env/bin/python3 script/tools/build_font_v1.py
    /tmp/ys-font-env/bin/python3 script/tools/build_font_v1.py --ttf
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

SCRIPT_DIR = Path(__file__).resolve().parent.parent
GLYPHS_DIR = SCRIPT_DIR / "glyphs"
FONTS_DIR = SCRIPT_DIR / "fonts"

sys.path.insert(0, str(GLYPHS_DIR))
from glyph_specs_v1 import GLYPHS, STROKE_WIDTH, EM, load_codepoint_map  # noqa: E402


def stroke_to_polygon(x1, y1, x2, y2, width=STROKE_WIDTH):
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        h = width // 2
        return [(x1 - h, y1 - h), (x1 + h, y1 - h),
                (x1 + h, y1 + h), (x1 - h, y1 + h)]
    px = -dy * width / (2 * length)
    py = dx * width / (2 * length)
    return [
        (int(x1 - px), int(y1 - py)),
        (int(x2 - px), int(y2 - py)),
        (int(x2 + px), int(y2 + py)),
        (int(x1 + px), int(y1 + py)),
    ]


def draw_to_pen(pen, spec):
    for stroke in spec.get("strokes", []):
        # strokes are (x1,y1,x2,y2) at STROKE_WIDTH or (x1,y1,x2,y2,width)
        # — sigils and fine detail carry their own thinner width
        if len(stroke) >= 5:
            x1, y1, x2, y2, width = stroke[:5]
        else:
            x1, y1, x2, y2 = stroke
            width = STROKE_WIDTH
        poly = stroke_to_polygon(x1, y1, x2, y2, width)
        pen.moveTo(poly[0])
        for p in poly[1:]:
            pen.lineTo(p)
        pen.closePath()
    for poly in spec.get("polygons", []):
        if not poly:
            continue
        pen.moveTo(poly[0])
        for p in poly[1:]:
            pen.lineTo(p)
        pen.closePath()


def glyph_name_for(latin: str, cp: int) -> str:
    """CFF/post-safe glyph name: ys.<latin> when purely alphanumeric,
    else codepoint-derived (punctuation, determinatives, CJK-form marks)."""
    if latin.isascii() and latin.isalnum():
        return f"ys.{latin}"
    return f"ys.u{cp:04X}"


def build_font(output_path: Path, family: str = "YOUSPEAK v1", ttf: bool = False):
    codepoint_map = load_codepoint_map()

    fb = FontBuilder(EM, isTTF=ttf)

    glyph_order = [".notdef", ".null", "space"]
    advance_widths: dict[str, int] = {}
    char_strings: dict[int, str] = {}

    # standards
    pen = TTGlyphPen(None); advance_widths[".notdef"] = 600
    pen = TTGlyphPen(None); advance_widths[".null"] = 0
    pen = TTGlyphPen(None); advance_widths["space"] = 400
    char_strings[0x20] = "space"

    # morpheme glyphs
    glyph_latin: dict[str, str] = {}
    for latin, spec in GLYPHS.items():
        if latin not in codepoint_map:
            continue
        cp = codepoint_map[latin]
        glyph_name = glyph_name_for(latin, cp)
        glyph_latin[glyph_name] = latin
        advance_widths[glyph_name] = 1000
        glyph_order.append(glyph_name)
        char_strings[cp] = glyph_name

    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(char_strings)

    if ttf:
        # TrueType path
        ttf_glyphs: dict[str, object] = {}
        for name in glyph_order:
            pen = TTGlyphPen(None)
            if name in glyph_latin:
                draw_to_pen(pen, GLYPHS.get(glyph_latin[name], {}))
            ttf_glyphs[name] = pen.glyph()
        fb.setupGlyf(ttf_glyphs)
    else:
        # CFF/OTF path
        charstrings: dict[str, object] = {}
        for name in glyph_order:
            t2pen = T2CharStringPen(advance_widths.get(name, 1000), None)
            if name in glyph_latin:
                draw_to_pen(t2pen, GLYPHS.get(glyph_latin[name], {}))
            charstrings[name] = t2pen.getCharString()
        fb.setupCFF(
            psName="YOUSPEAKv1-Regular",
            fontInfo={
                "FullName": "YOUSPEAK v1 Regular",
                "FamilyName": family,
                "Weight": "Regular",
                "version": "1.0",
            },
            charStringsDict=charstrings,
            privateDict={},
        )

    fb.setupHorizontalMetrics({n: (advance_widths.get(n, 1000), 0) for n in glyph_order})
    fb.setupHorizontalHeader(ascent=900, descent=-200)
    fb.setupOS2(sTypoAscender=900, sTypoDescender=-200, usWinAscent=950, usWinDescent=200)
    fb.setupNameTable({
        "familyName": family,
        "styleName": "Regular",
        "psName": f"{family.replace(' ', '')}-Regular",
        "version": "Version 1.0",
    })
    fb.setupPost()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fb.font.save(str(output_path))
    print(f"wrote {output_path}")
    print(f"  glyphs: {len(glyph_order)} ({sum(1 for n in glyph_order if n.startswith('ys.'))} YOUSPEAK)")
    print(f"  format: {'TTF' if ttf else 'OTF'}, stroke_width={STROKE_WIDTH}")


def main() -> int:
    ttf = "--ttf" in sys.argv[1:]
    ext = "ttf" if ttf else "otf"
    output = FONTS_DIR / f"youspeak-v1.{ext}"
    build_font(output, ttf=ttf)
    return 0


if __name__ == "__main__":
    sys.exit(main())
