#!/usr/bin/env python3
"""Build youspeak.otf from glyph_specs.py using fontTools.

Each glyph's strokes are converted into closed polygon contours
(rectangles along each stroke-axis) and bundled into an OTF font file
with the correct Unicode PUA codepoint mapping.

Usage:
    python3 build_font.py                 # builds script/fonts/youspeak.otf
    python3 build_font.py --ttf           # also build youspeak.ttf

Run with the fontTools-enabled Python interpreter:
    /tmp/ys-font-env/bin/python3 script/tools/build_font.py

(Or install fontTools globally: `pip install fonttools`.)
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

SCRIPT_DIR = Path(__file__).resolve().parent.parent  # script/
GLYPHS_DIR = SCRIPT_DIR / "glyphs"
FONTS_DIR = SCRIPT_DIR / "fonts"

# Import the glyph-specs module
sys.path.insert(0, str(GLYPHS_DIR))
from glyph_specs import GLYPHS, STROKE_WIDTH, EM, load_codepoint_map  # noqa: E402


def stroke_to_polygon(x1: int, y1: int, x2: int, y2: int, width: int) -> list[tuple[int, int]]:
    """Convert a line segment into a rectangular polygon (4 corners).

    The rectangle is centered on the line-axis with the given perpendicular
    width. For purely horizontal or vertical strokes, this produces an
    axis-aligned rectangle; for diagonals, a rotated rectangle.
    """
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        # degenerate: return a tiny square at the point
        h = width // 2
        return [(x1 - h, y1 - h), (x1 + h, y1 - h),
                (x1 + h, y1 + h), (x1 - h, y1 + h)]
    # perpendicular unit vector scaled by half-width
    px = -dy * width / (2 * length)
    py = dx * width / (2 * length)
    return [
        (int(x1 - px), int(y1 - py)),
        (int(x2 - px), int(y2 - py)),
        (int(x2 + px), int(y2 + py)),
        (int(x1 + px), int(y1 + py)),
    ]


def polygon_contour(pen: TTGlyphPen, points: list[tuple[int, int]]) -> None:
    """Add a closed contour (filled polygon) to the glyph pen."""
    if not points:
        return
    pen.moveTo(points[0])
    for p in points[1:]:
        pen.lineTo(p)
    pen.closePath()


def build_glyph_outline(spec: dict) -> object:
    """Convert a glyph spec into a TrueType glyph with contours."""
    pen = TTGlyphPen(None)
    # Each stroke becomes one closed polygon contour
    for stroke in spec.get("strokes", []):
        x1, y1, x2, y2 = stroke
        poly = stroke_to_polygon(x1, y1, x2, y2, STROKE_WIDTH)
        polygon_contour(pen, poly)
    # Additional polygon contours (dots, custom shapes)
    for poly in spec.get("polygons", []):
        polygon_contour(pen, poly)
    return pen.glyph()


def build_font(output_path: Path, family: str = "YOUSPEAK", ttf: bool = False) -> None:
    codepoint_map = load_codepoint_map()

    # fontTools FontBuilder setup: EM=1000, 'cff ' table for OTF
    fb = FontBuilder(EM, isTTF=ttf)

    # Glyph name for each Unicode codepoint
    glyph_order = [".notdef", ".null", "space"]
    glyph_names: dict[int, str] = {}
    glyphs: dict[str, object] = {}
    advance_widths: dict[str, int] = {}
    char_strings: dict[int, str] = {}

    # Standard glyphs
    pen = TTGlyphPen(None)
    glyphs[".notdef"] = pen.glyph()
    advance_widths[".notdef"] = 600
    pen = TTGlyphPen(None)
    glyphs[".null"] = pen.glyph()
    advance_widths[".null"] = 0
    pen = TTGlyphPen(None)
    glyphs["space"] = pen.glyph()
    advance_widths["space"] = 400
    char_strings[0x20] = "space"

    # YOUSPEAK morpheme glyphs
    for latin, spec in GLYPHS.items():
        if latin not in codepoint_map:
            continue
        cp = codepoint_map[latin]
        # Unique glyph name: use the Latin for clarity
        glyph_name = f"ys.{latin}"
        glyphs[glyph_name] = build_glyph_outline(spec)
        advance_widths[glyph_name] = 1000
        glyph_order.append(glyph_name)
        char_strings[cp] = glyph_name
        glyph_names[cp] = glyph_name

    # Build the font
    fb.setupGlyphOrder(glyph_order)
    fb.setupCharacterMap(char_strings)
    fb.setupGlyf(glyphs) if ttf else None
    if not ttf:
        # CFF (OTF) path: convert glyphs to Type2 CharStrings via ufo2ft or directly
        # fontTools' FontBuilder supports setupCFF for OTF construction.
        # For simplicity with TTGlyphPen output, build as TTF and rename.
        # Alternatively, use Type2CharStringPen + setupCFF.
        from fontTools.pens.t2CharStringPen import T2CharStringPen
        charstrings: dict[str, object] = {}
        for name in glyph_order:
            t2pen = T2CharStringPen(advance_widths.get(name, 1000), None)
            if name in glyphs:
                # Re-draw from the same spec into T2 pen
                if name == ".notdef" or name == ".null" or name == "space":
                    # empty
                    charstrings[name] = t2pen.getCharString()
                    continue
                latin = name.removeprefix("ys.")
                spec = GLYPHS.get(latin, {})
                for stroke in spec.get("strokes", []):
                    x1, y1, x2, y2 = stroke
                    poly = stroke_to_polygon(x1, y1, x2, y2, STROKE_WIDTH)
                    t2pen.moveTo(poly[0])
                    for p in poly[1:]:
                        t2pen.lineTo(p)
                    t2pen.closePath()
                for poly in spec.get("polygons", []):
                    if not poly:
                        continue
                    t2pen.moveTo(poly[0])
                    for p in poly[1:]:
                        t2pen.lineTo(p)
                    t2pen.closePath()
            charstrings[name] = t2pen.getCharString()
        fb.setupCFF(
            psName="YOUSPEAK-Regular",
            fontInfo={
                "FullName": "YOUSPEAK Regular",
                "FamilyName": family,
                "Weight": "Regular",
                "version": "0.1",
            },
            charStringsDict=charstrings,
            privateDict={},
        )
    fb.setupHorizontalMetrics({
        name: (advance_widths.get(name, 1000), 0) for name in glyph_order
    })
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupOS2(sTypoAscender=800, sTypoDescender=-200, usWinAscent=850, usWinDescent=200)
    fb.setupNameTable({
        "familyName": family,
        "styleName": "Regular",
        "psName": f"{family}-Regular",
        "version": "Version 0.1",
    })
    fb.setupPost()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fb.font.save(str(output_path))
    print(f"wrote {output_path}")
    print(f"  glyphs: {len(glyph_order)} (of which {len(glyphs) - 3} YOUSPEAK morphemes)")
    print(f"  format: {'TTF' if ttf else 'OTF'}")


def main() -> int:
    ttf = "--ttf" in sys.argv[1:]
    ext = "ttf" if ttf else "otf"
    output = FONTS_DIR / f"youspeak.{ext}"
    build_font(output, ttf=ttf)
    return 0


if __name__ == "__main__":
    sys.exit(main())
