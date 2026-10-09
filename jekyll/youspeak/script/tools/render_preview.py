#!/usr/bin/env python3
"""Render YOUSPEAK glyphs + canon words as SVG previews.

Produces two kinds of output:

1. `script/glyphs/preview/all-glyphs.svg` — every morpheme glyph in a
   labelled grid. Human-viewable directly in any browser or macOS
   Preview app. No font installation required.

2. `script/glyphs/preview/canon-words.svg` — each of the 16 canon
   words rendered by composing its morpheme-glyphs in sequence,
   with Latin-transliteration beneath each word.

3. `script/glyphs/preview/demo.html` — a single HTML page that
   displays both SVG rendering AND font-rendering (via @font-face),
   so the difference is visible side-by-side.

Usage:
    /tmp/ys-font-env/bin/python3 script/tools/render_preview.py
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
GLYPHS_DIR = SCRIPT_DIR / "glyphs"
PREVIEW_DIR = GLYPHS_DIR / "preview"

sys.path.insert(0, str(GLYPHS_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "tools"))
from glyph_specs import GLYPHS, STROKE_WIDTH, load_codepoint_map  # noqa: E402
from transliterate import CANONICAL_DECOMPOSITIONS  # noqa: E402


def glyph_to_svg(latin: str, spec: dict, size: int = 80) -> str:
    """Render a single morpheme glyph as inline SVG.

    Coordinates: strokes and polygons are in 1000-unit EM space (y
    increasing upward in font convention); SVG uses y-increasing-down,
    so we flip-y on render. Output is a <g> element suitable for
    composition into a larger SVG.
    """
    # SVG y increases down; font y increases up. Flip via transform.
    parts = [f'<g transform="translate(0 {size}) scale({size/1000} {-size/1000})">']

    stroke_w = STROKE_WIDTH
    for stroke in spec.get("strokes", []):
        x1, y1, x2, y2 = stroke
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="currentColor" stroke-width="{stroke_w}" stroke-linecap="square"/>'
        )
    for poly in spec.get("polygons", []):
        if not poly:
            continue
        pts = " ".join(f"{p[0]},{p[1]}" for p in poly)
        parts.append(f'<polygon points="{pts}" fill="currentColor"/>')
    parts.append("</g>")
    return "".join(parts)


def render_single_glyph_svg(latin: str, spec: dict, size: int = 160) -> str:
    """Render one glyph as a standalone SVG file with label."""
    content = glyph_to_svg(latin, spec, size=size)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size + 30}" width="{size}" height="{size + 30}">
  {content}
  <text x="{size/2}" y="{size + 22}" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#666">{latin}</text>
</svg>"""


def render_all_glyphs_grid(size: int = 100, cols: int = 8) -> str:
    """Grid of all YOUSPEAK glyphs with labels."""
    items = sorted(GLYPHS.items())
    rows = (len(items) + cols - 1) // cols
    cell_w = size + 30
    cell_h = size + 50
    width = cols * cell_w + 40
    height = rows * cell_h + 80
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" style="font-family: sans-serif; color: #1a1a1a;">',
        f'<rect width="{width}" height="{height}" fill="#fafaf7"/>',
        f'<text x="{width/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold" fill="#222">'
        f'YOUSPEAK — morpheme glyphs ({len(items)} designs)</text>',
        f'<text x="{width/2}" y="50" text-anchor="middle" font-size="12" fill="#666">'
        f'rendered as SVG — no font required</text>',
    ]
    for i, (latin, spec) in enumerate(items):
        row = i // cols
        col = i % cols
        x = 20 + col * cell_w + 15
        y = 70 + row * cell_h
        parts.append(f'<g transform="translate({x} {y})">')
        parts.append(glyph_to_svg(latin, spec, size=size))
        parts.append(
            f'<text x="{size/2}" y="{size + 20}" text-anchor="middle" '
            f'font-size="13" fill="#444">{latin}</text>'
        )
        parts.append("</g>")
    parts.append("</svg>")
    return "\n".join(parts)


def render_canon_words_svg(glyph_size: int = 80) -> str:
    """Render each canon word as a sequence of morpheme-glyphs."""
    cp_map = load_codepoint_map()

    # Only the canon words from the CANONICAL_DECOMPOSITIONS table
    canon_list = [
        ("doxakallos",        "the uncreated beauty-quality of GoD"),
        ("kallodoxa",         "the glory-quality of divine beauty"),
        ("orthophanes",       "the rightness-made-visible"),
        ("doxalgia",          "the ache at beholding"),
        ("anagnoristasis",    "recognition standing still"),
        ("metastrophesis",    "the turning-kept"),
        ("athaumasma",        "the no-longer-wondered trace"),
        ("synophora",         "shared-witness"),
        ("kallophanes",       "beauty-specific appearing"),
        ("dokimance",         "testing-that-makes-real"),
        ("artiance",          "pre-domain luminous-rightness"),
        ("verisleight",       "truth that produces false conclusions"),
        ("candence",          "warm clarity"),
        ("complerescence",    "mutual right-placement event"),
        ("diplosemy",         "engineered-duality of meaning"),
        ("veriseem",          "truth-seeming without truth-substance"),
    ]

    row_h = 110
    width = 1400
    height = 80 + len(canon_list) * row_h + 40
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" style="font-family: sans-serif; color: #111;">',
        f'<rect width="{width}" height="{height}" fill="#fafaf7"/>',
        f'<text x="{width/2}" y="35" text-anchor="middle" font-size="22" font-weight="bold">'
        f'The YOUSPEAK Canon — 16 standing words</text>',
        f'<text x="{width/2}" y="58" text-anchor="middle" font-size="12" fill="#666">'
        f'each word composed of its morpheme-glyphs; Latin transliteration beneath</text>',
    ]

    y0 = 90
    for idx, (word, gloss) in enumerate(canon_list):
        decomp = CANONICAL_DECOMPOSITIONS.get(word, [])
        y = y0 + idx * row_h
        # Render each morpheme-glyph in sequence
        x = 100
        for m in decomp:
            # Strip prefix/suffix hyphens to look up in GLYPHS
            key = m.strip("-")
            if key in GLYPHS:
                parts.append(f'<g transform="translate({x} {y})">')
                parts.append(glyph_to_svg(key, GLYPHS[key], size=glyph_size))
                parts.append("</g>")
                x += glyph_size + 8  # small gap between glyphs
        # Word name (Latin) and gloss
        parts.append(
            f'<text x="700" y="{y + 35}" font-size="18" font-weight="500" fill="#222">{word}</text>'
        )
        parts.append(
            f'<text x="700" y="{y + 60}" font-size="13" fill="#666" font-style="italic">{gloss}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def render_demo_html(font_relative_path: str = "../../fonts/youspeak.otf") -> str:
    """HTML page that shows both SVG + font rendering for comparison."""
    glyph_grid_svg = render_all_glyphs_grid(size=80, cols=8)
    canon_svg = render_canon_words_svg(glyph_size=70)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>YOUSPEAK — first look</title>
<style>
@font-face {{
  font-family: 'YOUSPEAK';
  src: url('{font_relative_path}') format('opentype');
}}
body {{
  font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  max-width: 1500px;
  margin: 40px auto;
  padding: 0 20px;
  background: #fafaf7;
  color: #222;
  line-height: 1.5;
}}
h1 {{ font-size: 32px; margin-bottom: 8px; }}
h2 {{ font-size: 22px; margin-top: 40px; color: #333; border-bottom: 1px solid #ddd; padding-bottom: 4px; }}
p.lede {{ color: #666; font-size: 14px; margin-top: 0; }}
.ys-font {{ font-family: 'YOUSPEAK', monospace; font-size: 36px; line-height: 1.4; color: #222; }}
.ys-word {{ display: inline-block; margin-right: 40px; margin-bottom: 16px; }}
.ys-word .latin {{ display: block; font-family: sans-serif; font-size: 12px; color: #888; margin-top: 4px; }}
.comparison {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; padding: 20px; margin: 20px 0; }}
.comparison table {{ width: 100%; border-collapse: collapse; }}
.comparison th {{ text-align: left; padding: 8px 12px; background: #f4f4ee; font-size: 12px; color: #555; border-bottom: 1px solid #ddd; }}
.comparison td {{ padding: 10px 12px; border-bottom: 1px solid #eee; }}
.comparison td:nth-child(1) {{ font-family: sans-serif; font-size: 15px; color: #666; width: 200px; }}
.comparison td:nth-child(2) {{ font-family: 'YOUSPEAK', monospace; font-size: 32px; color: #222; }}
.comparison td:nth-child(3) {{ font-family: sans-serif; font-size: 14px; color: #555; width: 400px; }}
code {{ background: #f4f4ee; padding: 2px 6px; border-radius: 3px; font-size: 90%; }}
.callout {{ background: #fff3e0; border-left: 3px solid #e79c3a; padding: 12px 16px; border-radius: 3px; margin: 20px 0; font-size: 14px; }}
</style>
</head>
<body>
<h1>YOUSPEAK — first look</h1>
<p class="lede">A discipline of compressed linguistic meaning, visualised for the first time.</p>

<h2>1 · The morphemes (SVG rendering)</h2>
<p>Each glyph encodes one morpheme. This image renders directly as SVG — no font installation required. It is what the font designer will vectorize properly in the next production step.</p>

{glyph_grid_svg}

<h2>2 · The Canon (SVG rendering)</h2>
<p>Each of the 16 canonical words, composed of its morpheme-glyphs in sequence. Latin transliteration labels each word; the glosses explain the meaning.</p>

{canon_svg}

<h2>3 · Font rendering (requires install)</h2>
<p>Below, the same canon words rendered using the YOUSPEAK OTF font file via <code>@font-face</code>. This is what displays in applications after you install <code>script/fonts/youspeak.otf</code>. If the font is not installed, this section will show Latin transliteration as fallback.</p>

<div class="comparison">
<table>
<thead>
  <tr><th>Word (Latin)</th><th>YOUSPEAK glyphs</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>doxakallos</td><td class="ys-font">&#xE100;&#xE101;</td><td>the uncreated beauty-quality of GoD</td></tr>
<tr><td>kallodoxa</td><td class="ys-font">&#xE101;&#xE100;</td><td>the glory-quality of divine beauty</td></tr>
<tr><td>orthophanes</td><td class="ys-font">&#xE102;&#xE103;</td><td>the rightness-made-visible</td></tr>
<tr><td>doxalgia</td><td class="ys-font">&#xE100;&#xE104;</td><td>the ache at beholding</td></tr>
<tr><td>synophora</td><td class="ys-font">&#xE10A;&#xE10B;</td><td>shared-witness</td></tr>
<tr><td>dokimance</td><td class="ys-font">&#xE10D;&#xE142;</td><td>testing-that-makes-real</td></tr>
<tr><td>artiance</td><td class="ys-font">&#xE10E;&#xE146;</td><td>pre-domain luminous-rightness</td></tr>
<tr><td>verisleight</td><td class="ys-font">&#xE10F;&#xE11E;</td><td>truth-as-deception</td></tr>
<tr><td>candence</td><td class="ys-font">&#xE10C;&#xE144;</td><td>warm clarity</td></tr>
<tr><td>diplosemy</td><td class="ys-font">&#xE111;&#xE112;&#xE14C;</td><td>engineered-duality of meaning</td></tr>
<tr><td>veriseem</td><td class="ys-font">&#xE10F;&#xE11F;</td><td>truth-seeming without truth</td></tr>
</tbody>
</table>
</div>

<div class="callout">
<strong>If the middle column looks identical to the first column</strong> (Latin instead of glyphs), the font isn't installed yet. Install <code>script/fonts/youspeak.otf</code> to see the real rendering. Installation instructions: open the file in Font Book, click Install; or drop it into <code>~/Library/Fonts/</code>.
</div>

<h2>4 · Try it</h2>
<p>A mixed-language sentence. Everything outside canon words stays Latin; the three YOUSPEAK words render as glyphs when the font is installed.</p>

<p class="ys-font">The &#xE10D;&#xE142; guards against &#xE10F;&#xE11E;. &#xE100;&#xE101; appears in &#xE102;&#xE103;.</p>

<p style="color: #666; font-size: 14px;"><em>Latin fallback:</em> The dokimance guards against verisleight. Doxakallos appears in orthophanes.</p>

</body>
</html>
"""


def main() -> int:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    grid_path = PREVIEW_DIR / "all-glyphs.svg"
    grid_path.write_text(render_all_glyphs_grid())
    print(f"wrote {grid_path}")

    canon_path = PREVIEW_DIR / "canon-words.svg"
    canon_path.write_text(render_canon_words_svg())
    print(f"wrote {canon_path}")

    demo_path = PREVIEW_DIR / "demo.html"
    demo_path.write_text(render_demo_html())
    print(f"wrote {demo_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
