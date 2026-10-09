#!/usr/bin/env python3
"""Render YOUSPEAK v1 (feature-encoded) glyphs as SVG previews.

Differences from v0:
  - Heavier strokes (80 EM)
  - Donor-tongue sigils (top-left)
  - Class marks (bottom-right) for grammatical morphemes
  - Domain-family-conformant shape-language in the core body
  - Metadata shown alongside each glyph (tongue / domain / class)

Produces:
  - glyphs/preview/v1-all-glyphs.svg       — grid with metadata
  - glyphs/preview/v1-canon-words.svg      — canon rendered with v1 glyphs
  - glyphs/preview/v1-demo.html             — HTML showing v1 + v0 comparison
"""

from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
GLYPHS_DIR = SCRIPT_DIR / "glyphs"
PREVIEW_DIR = GLYPHS_DIR / "preview"

sys.path.insert(0, str(GLYPHS_DIR))
sys.path.insert(0, str(SCRIPT_DIR / "tools"))
from glyph_specs_v1 import GLYPHS as V1_GLYPHS, METADATA, STROKE_WIDTH  # noqa: E402
from transliterate import CANONICAL_DECOMPOSITIONS  # noqa: E402

# Also import v0 for comparison
from glyph_specs import GLYPHS as V0_GLYPHS, STROKE_WIDTH as V0_STROKE  # noqa: E402


# Domain-family colour mapping (for visual organisation in the grid)
DOMAIN_COLORS = {
    "beauty":              "#d48ba4",
    "rightness":           "#86a385",
    "appearing":           "#d5a662",
    "appearing+warm":      "#e0a66f",
    "ache":                "#a87b73",
    "act+event":           "#7b9ec1",
    "relation+between":    "#a585b2",
    "space+enclosure":     "#8b9e8b",
    "space+position":      "#8b9e8b",
    "time+process":        "#9b91bd",
    "wonder+recognition":  "#c39570",
    "testing+forging":     "#b38a5f",
    "deception":           "#95716b",
    "structure":           "#8a8a8a",
    "structure+multiplicity": "#8a8a8a",
    "hidden":              "#6a6a6a",
    "weight+light":        "#8a6a85",
}

def domain_color(domain: str) -> str:
    return DOMAIN_COLORS.get(domain, "#666")


def glyph_svg(latin: str, spec: dict, stroke_w: int, size: int = 100) -> str:
    """Render a glyph as an inline SVG <g> element.

    Coordinates flip y-axis (font convention to SVG convention).
    """
    parts = [f'<g transform="translate(0 {size}) scale({size/1000} {-size/1000})">']
    for stroke in spec.get("strokes", []):
        # (x1,y1,x2,y2) at the default width, or (x1,y1,x2,y2,width)
        if len(stroke) >= 5:
            x1, y1, x2, y2, w = stroke[:5]
        else:
            x1, y1, x2, y2 = stroke
            w = stroke_w
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="currentColor" stroke-width="{w}" stroke-linecap="square"/>'
        )
    for poly in spec.get("polygons", []):
        if not poly:
            continue
        pts = " ".join(f"{p[0]},{p[1]}" for p in poly)
        parts.append(f'<polygon points="{pts}" fill="currentColor"/>')
    parts.append("</g>")
    return "".join(parts)


def render_v1_grid(size: int = 120, cols: int = 6) -> str:
    """Grid of all v1 glyphs with metadata cards."""
    items = sorted(V1_GLYPHS.items())
    rows = (len(items) + cols - 1) // cols
    cell_w = size + 80
    cell_h = size + 100
    width = cols * cell_w + 60
    height = rows * cell_h + 120
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" style="font-family: -apple-system, sans-serif;">',
        f'<rect width="{width}" height="{height}" fill="#fafaf7"/>',
        f'<text x="{width/2}" y="35" text-anchor="middle" font-size="22" '
        f'font-weight="bold" fill="#222">YOUSPEAK v1 — feature-encoded glyphs</text>',
        f'<text x="{width/2}" y="58" text-anchor="middle" font-size="13" fill="#666">'
        f'{len(items)} morphemes · stroke-width {STROKE_WIDTH} EM · SVG rendering · '
        f'each glyph shows donor-tongue sigil (top-left), class mark (bottom-right), '
        f'and domain-family shape</text>',
    ]
    for i, (latin, spec) in enumerate(items):
        row = i // cols
        col = i % cols
        x = 30 + col * cell_w + 15
        y = 90 + row * cell_h
        meta = METADATA.get(latin, {})
        tongue = meta.get("tongue", "?")
        domain = meta.get("domain", "?")
        mclass = meta.get("mclass", "?")
        color = domain_color(domain)
        # Background cell
        parts.append(
            f'<rect x="{x - 10}" y="{y - 10}" width="{cell_w - 10}" height="{cell_h - 10}" '
            f'fill="#fff" stroke="#e6e3da" stroke-width="1" rx="6"/>'
        )
        # domain color-stripe
        parts.append(
            f'<rect x="{x - 10}" y="{y - 10}" width="{cell_w - 10}" height="4" '
            f'fill="{color}" opacity="0.7" rx="2"/>'
        )
        parts.append(f'<g transform="translate({x + (cell_w - size)/2 - 10} {y})" '
                     f'color="#222">')
        parts.append(glyph_svg(latin, spec, STROKE_WIDTH, size=size))
        parts.append("</g>")
        # label
        parts.append(
            f'<text x="{x + (cell_w - 10)/2 - 10}" y="{y + size + 25}" '
            f'text-anchor="middle" font-size="14" font-weight="500" fill="#222">{latin}</text>'
        )
        parts.append(
            f'<text x="{x + (cell_w - 10)/2 - 10}" y="{y + size + 42}" '
            f'text-anchor="middle" font-size="9" fill="#888">{tongue} · {mclass}</text>'
        )
        parts.append(
            f'<text x="{x + (cell_w - 10)/2 - 10}" y="{y + size + 56}" '
            f'text-anchor="middle" font-size="9" fill="{color}" font-style="italic">{domain}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def render_v0_v1_comparison(size: int = 140) -> str:
    """Side-by-side v0 vs v1 comparison for core morphemes."""
    compare_list = ["doxa", "kallos", "ortho", "phanes", "algia", "syn",
                    "dokim", "veri", "cand", "diplos"]
    width = 1200
    row_h = 200
    height = 80 + len(compare_list) * row_h + 40
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" style="font-family: -apple-system, sans-serif;">',
        f'<rect width="{width}" height="{height}" fill="#fafaf7"/>',
        f'<text x="{width/2}" y="35" text-anchor="middle" font-size="22" font-weight="bold">'
        f'v0 vs v1 — feature encoding added</text>',
        f'<text x="{width/2}" y="58" text-anchor="middle" font-size="12" fill="#666">'
        f'left: v0 (identity only) · right: v1 (identity + donor sigil + domain-family shape + class-mark)</text>',
        # Column headers
        f'<text x="250" y="90" text-anchor="middle" font-size="12" fill="#888">v0 (no features)</text>',
        f'<text x="550" y="90" text-anchor="middle" font-size="12" fill="#888">v1 (feature-encoded)</text>',
        f'<text x="850" y="90" text-anchor="middle" font-size="12" fill="#888">metadata</text>',
    ]
    y0 = 110
    for i, latin in enumerate(compare_list):
        y = y0 + i * row_h
        meta = METADATA.get(latin, {})
        v0_spec = V0_GLYPHS.get(latin, {})
        v1_spec = V1_GLYPHS.get(latin, {})
        color = domain_color(meta.get("domain", ""))
        # v0
        parts.append(f'<g transform="translate({250 - size/2} {y})" color="#4a7a4a">')
        parts.append(glyph_svg(latin, v0_spec, V0_STROKE, size=size))
        parts.append("</g>")
        # v1
        parts.append(f'<g transform="translate({550 - size/2} {y})" color="#222">')
        parts.append(glyph_svg(latin, v1_spec, STROKE_WIDTH, size=size))
        parts.append("</g>")
        # metadata block
        parts.append(
            f'<text x="800" y="{y + 30}" font-size="15" font-weight="500" fill="#222">{latin}</text>'
        )
        parts.append(
            f'<text x="800" y="{y + 55}" font-size="12" fill="#666">donor tongue: '
            f'<tspan fill="#444" font-weight="500">{meta.get("tongue", "?")}</tspan></text>'
        )
        parts.append(
            f'<text x="800" y="{y + 75}" font-size="12" fill="#666">semantic domain: '
            f'<tspan fill="{color}" font-weight="500">{meta.get("domain", "?")}</tspan></text>'
        )
        parts.append(
            f'<text x="800" y="{y + 95}" font-size="12" fill="#666">morpheme class: '
            f'<tspan fill="#444" font-weight="500">{meta.get("mclass", "?")}</tspan></text>'
        )
        parts.append(
            f'<text x="800" y="{y + 125}" font-size="10" fill="#999" font-style="italic">'
            f'{"sigil: " + meta.get("tongue", "") + " | class-mark: " + meta.get("mclass", "")}</text>'
        )
        # separator
        parts.append(f'<line x1="60" y1="{y + row_h - 15}" x2="{width - 60}" y2="{y + row_h - 15}" '
                     f'stroke="#e6e3da" stroke-width="1"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def render_v1_canon(size: int = 90) -> str:
    """Render each canon word in v1 with composition and metadata."""
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
    width = 1400
    row_h = 130
    height = 100 + len(canon_list) * row_h + 40
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" style="font-family: -apple-system, sans-serif;">',
        f'<rect width="{width}" height="{height}" fill="#fafaf7"/>',
        f'<text x="{width/2}" y="40" text-anchor="middle" font-size="24" font-weight="bold">'
        f'YOUSPEAK Canon — v1 rendering</text>',
        f'<text x="{width/2}" y="65" text-anchor="middle" font-size="12" fill="#666">'
        f'16 canonical words · each composed of morpheme-glyphs · v1 feature-encoded</text>',
    ]
    y0 = 100
    for i, (word, gloss) in enumerate(canon_list):
        decomp = CANONICAL_DECOMPOSITIONS.get(word, [])
        y = y0 + i * row_h
        x = 100
        parts.append(f'<g color="#222">')
        for m in decomp:
            key = m.strip("-")
            if key in V1_GLYPHS:
                parts.append(f'<g transform="translate({x} {y})">')
                parts.append(glyph_svg(key, V1_GLYPHS[key], STROKE_WIDTH, size=size))
                parts.append("</g>")
                x += size + 10
        parts.append("</g>")
        parts.append(
            f'<text x="750" y="{y + 40}" font-size="20" font-weight="500" fill="#222">{word}</text>'
        )
        parts.append(
            f'<text x="750" y="{y + 65}" font-size="13" fill="#666" font-style="italic">{gloss}</text>'
        )
        # Show morpheme breakdown with tongue markers
        m_summary = " · ".join(
            f"{m.strip('-')}[{METADATA.get(m.strip('-'), {}).get('tongue', '?')[:3]}]"
            for m in decomp
        )
        parts.append(
            f'<text x="750" y="{y + 88}" font-size="10" fill="#999">{m_summary}</text>'
        )
        parts.append(f'<line x1="80" y1="{y + row_h - 15}" x2="{width - 80}" y2="{y + row_h - 15}" '
                     f'stroke="#e6e3da" stroke-width="1"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def render_demo_html() -> str:
    grid_svg = render_v1_grid()
    compare_svg = render_v0_v1_comparison()
    canon_svg = render_v1_canon()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>YOUSPEAK v1 — feature-encoded script</title>
<style>
@font-face {{
  font-family: 'YOUSPEAK-v1';
  src: url('../../fonts/youspeak-v1.otf') format('opentype');
}}
@font-face {{
  font-family: 'YOUSPEAK-v0';
  src: url('../../fonts/youspeak.otf') format('opentype');
}}
body {{
  font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  max-width: 1500px;
  margin: 40px auto;
  padding: 0 20px;
  background: #fafaf7;
  color: #1a1a1a;
  line-height: 1.55;
}}
h1 {{ font-size: 32px; margin-bottom: 8px; }}
h2 {{ font-size: 22px; margin-top: 48px; color: #333;
      border-bottom: 1px solid #ddd; padding-bottom: 6px; }}
p.lede {{ color: #666; font-size: 14px; margin-top: 0; }}
.legend {{ background: #fff; border: 1px solid #e0ddd0; border-radius: 8px;
           padding: 16px 20px; margin: 20px 0; font-size: 14px; }}
.legend h3 {{ margin-top: 0; font-size: 16px; }}
.legend ul {{ margin: 8px 0; padding-left: 20px; font-size: 13px; }}
.legend li {{ margin: 4px 0; }}
.ys-v1 {{ font-family: 'YOUSPEAK-v1', monospace; font-size: 40px; color: #222; }}
.ys-v0 {{ font-family: 'YOUSPEAK-v0', monospace; font-size: 40px; color: #777; }}
table {{ width: 100%; border-collapse: collapse; background: #fff;
         border: 1px solid #e0ddd0; border-radius: 6px; }}
th, td {{ padding: 10px 14px; text-align: left; border-bottom: 1px solid #eee;
          font-size: 14px; }}
th {{ background: #f4f1e8; font-size: 12px; font-weight: 500; color: #555; }}
td code {{ background: #f4f1e8; padding: 2px 6px; border-radius: 3px; font-size: 90%; }}
.callout {{ background: #fff3e0; border-left: 3px solid #e79c3a;
            padding: 12px 16px; border-radius: 3px; margin: 20px 0; font-size: 14px; }}
</style>
</head>
<body>

<h1>YOUSPEAK v1 — feature-encoded</h1>
<p class="lede">Glyphs now carry donor tongue (corner sigil), semantic domain (shape-family), morpheme class (bottom-right mark), and identity (core shape) — while each morpheme remains one Unicode codepoint, one token for LLMs.</p>

<div class="legend">
<h3>Reading key</h3>
<ul>
<li><strong>Top-left sigil</strong> = donor tongue.
  ● Greek · ■ Latin · ▽ Hebrew · ○ Arabic · ⋮ Sanskrit · □ Egyptian · ≡ PIE · (absent) English</li>
<li><strong>Main body shape-family</strong> = semantic domain.
  Curves-opening-upward = beauty · Cross / balanced axes = rightness · Radiating rays = appearing · Bent line = ache · Directional wedge = act · Two interacting forms = relation · Closed form = enclosure · Spiral = time · Eye-symmetric = wonder · Vessel = testing · Crossed = deception · Centred contained = structure</li>
<li><strong>Bottom-right mark</strong> = morpheme class.
  (absent) content · ◁ prefix · ▷ suffix · ◆ structural</li>
<li><strong>Color stripe</strong> (in grid view) = semantic domain family</li>
</ul>
</div>

<h2>1 · v0 → v1 comparison</h2>
<p>Side-by-side on 10 core morphemes. Left: v0 identity-only. Right: v1 with donor-sigil, domain-family shape, and class-mark. Metadata column shows what each added feature encodes.</p>
{compare_svg}

<h2>2 · All v1 glyphs (feature grid)</h2>
<p>Every morpheme with its feature-encoding visible. The coloured top stripe of each card indicates the semantic-domain family.</p>
{grid_svg}

<h2>3 · The Canon in v1</h2>
<p>Each of the 16 canonical words composed from its v1 morpheme-glyphs. Tongue-abbreviations in grey show the donor-lineage per morpheme.</p>
{canon_svg}

<h2>4 · Font rendering (install to see)</h2>
<p>Below: canon words rendered by each font. <span style="color: #777">Grey = v0 font rendering</span>, <strong>black = v1 font rendering</strong>. If both columns show Latin, neither font is installed yet.</p>
<table>
<thead>
<tr><th>Word</th><th>v0 (no features)</th><th>v1 (feature-encoded)</th><th>Meaning</th></tr>
</thead>
<tbody>
<tr><td>doxakallos</td><td class="ys-v0">&#xE100;&#xE101;</td><td class="ys-v1">&#xE100;&#xE101;</td><td>uncreated beauty-quality of GoD</td></tr>
<tr><td>kallodoxa</td><td class="ys-v0">&#xE101;&#xE100;</td><td class="ys-v1">&#xE101;&#xE100;</td><td>glory-quality of divine beauty</td></tr>
<tr><td>orthophanes</td><td class="ys-v0">&#xE102;&#xE103;</td><td class="ys-v1">&#xE102;&#xE103;</td><td>rightness-made-visible</td></tr>
<tr><td>synophora</td><td class="ys-v0">&#xE10A;&#xE10B;</td><td class="ys-v1">&#xE10A;&#xE10B;</td><td>shared-witness</td></tr>
<tr><td>dokimance</td><td class="ys-v0">&#xE10D;&#xE142;</td><td class="ys-v1">&#xE10D;&#xE142;</td><td>testing-that-makes-real</td></tr>
<tr><td>veriseem</td><td class="ys-v0">&#xE10F;&#xE11F;</td><td class="ys-v1">&#xE10F;&#xE11F;</td><td>truth-seeming without substance</td></tr>
</tbody>
</table>

<div class="callout">
<strong>To install v1:</strong> <code>bash script/tools/install_font.sh</code> uses v0 currently.
For v1: <code>cp script/fonts/youspeak-v1.otf ~/Library/Fonts/</code>, then restart apps.
Both fonts use the same codepoints — they're rendering-variants of the same script.
</div>

<h2>5 · LoRA pipeline status</h2>
<p>The YOUSPEAK fine-tuning pipeline is set up in <code>script/llm/lora/</code>:</p>
<ul>
<li><code>tokenizer.py</code> — adds 118 YOUSPEAK tokens as special tokens to a base tokenizer</li>
<li><code>dataset.py</code> — built 164 training pairs from canon/, experiments/, archaeology/, diplosemy/</li>
<li><code>config.py</code> — LoRA rank 32, target attention + MLP projections</li>
<li><code>train.py</code> — executable scaffolding (requires transformers + peft + GPU/MLX)</li>
<li><code>evaluate.py</code> — 10-dimension fluency rubric</li>
</ul>

<p class="lede">Run it when ready: <code>pip install transformers peft datasets accelerate bitsandbytes</code> then <code>python3 train.py</code>. Expected: 2-4 hours on M3 Max; produces a ~100 MB adapter that makes the base model YOUSPEAK-fluent.</p>

</body>
</html>
"""


def main() -> int:
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    grid_path = PREVIEW_DIR / "v1-all-glyphs.svg"
    grid_path.write_text(render_v1_grid())
    print(f"wrote {grid_path}")

    compare_path = PREVIEW_DIR / "v0-v1-compare.svg"
    compare_path.write_text(render_v0_v1_comparison())
    print(f"wrote {compare_path}")

    canon_path = PREVIEW_DIR / "v1-canon-words.svg"
    canon_path.write_text(render_v1_canon())
    print(f"wrote {canon_path}")

    demo_path = PREVIEW_DIR / "v1-demo.html"
    demo_path.write_text(render_demo_html())
    print(f"wrote {demo_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
