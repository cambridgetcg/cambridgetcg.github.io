#!/usr/bin/env python3
"""Export the cathedral as a single agent-first bundle (JSON).

The bundle is everything a visiting agent needs to READ and USE YOUSPEAK:
morphemes (with glyph geometry + precomputed SVG paths), canon words (with
definitions parsed from canon/**/*.md), doctrine texts, and the font binaries
(base64). Consumed by the agenttool backend (/v1/youspeak/*) and any other
agent-facing surface.

Usage:
    python3 script/tools/export_agent_bundle.py
    python3 script/tools/export_agent_bundle.py --copy-to <dir>   # also vendor a copy

Output: script/exports/agent_bundle.json  (regenerate after any canon/glyph change;
        script/tools/rebuild.sh runs this as its final step)
"""
from __future__ import annotations

import base64
import json
import math
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # YOUSPEAK/
SCRIPT = ROOT / "script"
sys.path.insert(0, str(SCRIPT / "glyphs"))
sys.path.insert(0, str(SCRIPT / "tools"))
from glyph_specs_v1 import CORE_GLYPHS, GLYPHS, STROKE_WIDTH, load_codepoint_map  # noqa: E402
from transliterate import CANONICAL_DECOMPOSITIONS  # noqa: E402

EM = 1000


# ── glyph geometry → SVG path (y flipped to SVG convention) ─────────────

def stroke_quad(x1, y1, x2, y2, w):
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    if length == 0:
        h = w / 2
        return [(x1 - h, y1 - h), (x1 + h, y1 - h), (x1 + h, y1 + h), (x1 - h, y1 + h)]
    px = -dy * w / (2 * length)
    py = dx * w / (2 * length)
    return [(x1 - px, y1 - py), (x2 - px, y2 - py), (x2 + px, y2 + py), (x1 + px, y1 + py)]


def svg_path(composed: dict) -> str:
    """One compact SVG path 'd' for a composed glyph, in a 0..1000 viewBox, y-down."""
    parts = []
    for s in composed.get("strokes", []):
        w = s[4] if len(s) >= 5 else STROKE_WIDTH
        quad = stroke_quad(s[0], s[1], s[2], s[3], w)
        parts.append("M" + "L".join(f"{x:.0f},{EM - y:.0f}" for x, y in quad) + "Z")
    for poly in composed.get("polygons", []):
        parts.append("M" + "L".join(f"{x:.0f},{EM - y:.0f}" for x, y in poly) + "Z")
    return "".join(parts)


# ── design notes (S092 rationales) ──────────────────────────────────────

def parse_design_notes() -> dict[str, dict]:
    notes_path = SCRIPT / "glyphs" / "design_notes_s092.md"
    if not notes_path.exists():
        return {}
    out: dict[str, dict] = {}
    current = None
    for line in notes_path.read_text().splitlines():
        m = re.match(r"^### (\S+) \(", line)
        if m:
            current = m.group(1)
            out[current] = {"iconography": "", "rationale": ""}
            continue
        if current is None:
            continue
        if line.startswith("## "):
            current = None
            continue
        if line.startswith("_") and line.rstrip().endswith("_") and not out[current]["iconography"]:
            out[current]["iconography"] = line.strip("_ \n")
        elif line.strip() and not line.startswith("#"):
            out[current]["rationale"] += line.strip() + " "
    for v in out.values():
        v["rationale"] = v["rationale"].strip()
    return out


# ── canon parsing ───────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            kv = re.match(r"^(\w[\w_]*):\s*(.+)$", line)
            if kv and not line.startswith(" "):
                fm[kv.group(1)] = kv.group(2).strip()
    return fm


def first_definition(text: str) -> str:
    m = re.search(r"## Definition\s*\n+(.+?)(?:\n\n|\n##)", text, re.S)
    if m:
        return " ".join(m.group(1).split())
    # fallback: first paragraph after the H1
    m = re.search(r"^# \S+\s*\n+(.+?)(?:\n\n|\n##)", text, re.S | re.M)
    return " ".join(m.group(1).split()) if m else ""


def collect_determinatives() -> dict[str, dict]:
    """The word→class-mark assignments, read from the one place canon states them.

    grammars/determinatives/manifesto.md carries the assignments as prose tables
    ("Applied to the Canon"), and nowhere else in the repo are they machine-readable.
    Until this function existed, a tool reading the bundle could not tell what class
    ANY canon word belongs to — so ORDO's `word.TAG` notation recorded only what the
    rite's author typed, never what the canon assigns.

    The raw label is carried through UNRESOLVED on purpose. The manifesto labels two
    different codepoints `PER` (U+E171 person at :44, U+E174 perception at :47) while
    script/codepoints.md:134 names the second `.PRC`. Resolving that silently here
    would decide a doctrine conflict inside an export script; instead the rationale
    text travels with the label so a reader (or a checker) can say what the table
    intends AND that the table disagrees with the registry.
    """
    path = ROOT / "grammars" / "determinatives" / "manifesto.md"
    # The assignments are now a required input, not a nicety: a silent {} here makes
    # ORDO's attending GREENER, not louder — the one direction a checker must never
    # fail in. Raise, and let the export stop.
    lines = path.read_text().splitlines()
    out: dict[str, dict] = {}
    row = re.compile(r"^\|\s*\*\*([\w-]+)\*\*\s*\|\s*([A-Z]{3})\s*(?:\(([^)]*)\))?\s*\|")
    for n, line in enumerate(lines, 1):
        m = row.match(line.strip())
        if not m:
            continue
        word, label, rationale = m.group(1), m.group(2), (m.group(3) or "").strip()
        if word in out:  # one determinative per word (manifesto.md:123) — first wins, collision recorded
            out[word].setdefault("collisions", []).append({"label": label, "line": n})
            continue
        out[word] = {
            "label": label,
            "rationale": rationale,
            "source": f"{path.relative_to(ROOT)}:{n}",
        }
    return out


def collect_canon() -> tuple[list[dict], int]:
    dets = collect_determinatives()
    entries = []
    seen = set()
    for path in sorted(ROOT.glob("canon/**/*.md")):
        if path.name.lower() == "readme.md":
            continue
        text = path.read_text()
        fm = parse_frontmatter(text)
        word = fm.get("word") or path.stem
        if word in seen or word.startswith("_"):
            continue
        seen.add(word)
        weighted = None
        wm = re.search(r"weighted(?:_v2)?:\s*([\d.]+)", text)
        if wm:
            weighted = float(wm.group(1))
        entries.append({
            "word": word,
            "tier": fm.get("tier") or ("core" if "core" in str(path.parent.name) else path.parent.name),
            "gap": fm.get("gap", ""),
            "definition": first_definition(text),
            "score": weighted,
            "pronunciation": fm.get("pronunciation", ""),
            "entered": fm.get("entered", ""),
            "path": str(path.relative_to(ROOT)),
            # absent for the 200+ words the manifesto's tables never covered —
            # absence means "canon assigns none", not "canon assigns nothing"
            "determinative": dets.get(word),
        })
    return entries, len(dets)


# ── main ────────────────────────────────────────────────────────────────

def main() -> int:
    cmap = load_codepoint_map()
    notes = parse_design_notes()
    morph_meta = json.loads((SCRIPT / "morphemes.json").read_text())["morphemes"]
    by_latin = {m["latin"].strip("-"): m for m in morph_meta}

    morphemes = []
    for latin in sorted(CORE_GLYPHS):
        cp = cmap.get(latin)
        meta = by_latin.get(latin, {})
        spec = CORE_GLYPHS[latin]
        note = notes.get(latin, {})
        morphemes.append({
            "latin": latin,
            "latin_display": meta.get("latin", latin),
            "codepoint": f"U+{cp:04X}" if cp else None,
            "char": chr(cp) if cp else None,
            "tongue": spec.get("tongue", "English"),
            "native": meta.get("native"),
            "meaning": meta.get("meaning", ""),
            "class": meta.get("class", spec.get("mclass", "content")),
            "domain": spec.get("domain", ""),
            "mclass": spec.get("mclass", "content"),
            "glyph": {
                "core": spec.get("core", {}),
                "suppress_class_mark": bool(spec.get("suppress_class_mark")),
                "svg_path": svg_path(GLYPHS[latin]),
                "view_box": "0 0 1000 1000",
            },
            "iconography": note.get("iconography", ""),
            "rationale": note.get("rationale", ""),
        })

    canon, det_count = collect_canon()

    canon_words = []
    canon_by_word = {c["word"]: c for c in canon}
    for word, parts in sorted(CANONICAL_DECOMPOSITIONS.items()):
        stripped = [p.strip("-") for p in parts]
        cps = [cmap.get(p) for p in stripped]
        renderable = all(c is not None for c in cps)
        canon_words.append({
            "word": word,
            "morphemes": stripped,
            "codepoints": [f"U+{c:04X}" for c in cps] if renderable else None,
            "glyph_text": "".join(chr(c) for c in cps) if renderable else None,
            "definition": canon_by_word.get(word, {}).get("definition", ""),
        })

    docs = {}
    for name, path in {
        "manifesto": ROOT / "YOUSPEAK.md",
        "primer": ROOT / "PRIMER.md",
        "design_philosophy": SCRIPT / "glyphs" / "design_philosophy.md",
        "design_notes_s092": SCRIPT / "glyphs" / "design_notes_s092.md",
        "codepoints": SCRIPT / "codepoints.md",
    }.items():
        if path.exists():
            docs[name] = path.read_text()

    fonts = {}
    for ext in ("otf", "ttf"):
        fp = SCRIPT / "fonts" / f"youspeak-v1.{ext}"
        if fp.exists():
            fonts[ext] = base64.b64encode(fp.read_bytes()).decode("ascii")

    commit = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"],
                            capture_output=True, text=True).stdout.strip()

    bundle = {
        "schema_version": "1.0",
        "name": "youspeak-agent-bundle",
        "source": "https://cambridgetcg.github.io/youspeak/",
        "source_commit": commit,
        "what_this_is": (
            "YOUSPEAK is a constructed language — 'a cathedral of vocabulary, a forge of "
            "missing words, a standing worship.' It coins elegant vocabulary for concepts "
            "that exist but are unnamed in current languages, drawing morphemes from 66+ "
            "donor traditions (living and dead) with honest crediting. Each morpheme has "
            "one Unicode PUA codepoint and one drawn glyph; words compose linearly. This "
            "bundle carries the complete script (93 morphemes, all drawn, in a real font), "
            "the canon of forged words with definitions, and the founding doctrine."
        ),
        "counts": {
            "morphemes": len(morphemes),
            "canon_entries": len(canon),
            "canon_words_renderable": sum(1 for w in canon_words if w["glyph_text"]),
            "donor_sigils": 15,
        },
        "morphemes": morphemes,
        "canon": canon,
        "canon_words": canon_words,
        "docs": docs,
        "fonts": fonts,
    }

    out = SCRIPT / "exports" / "agent_bundle.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(bundle, ensure_ascii=False))
    size_kb = out.stat().st_size // 1024
    print(f"wrote {out} ({size_kb} KB): {len(morphemes)} morphemes · "
          f"{len(canon)} canon entries ({det_count} class-marked) · {len(canon_words)} decomposed words · "
          f"{len(docs)} docs · fonts {list(fonts)}")

    if "--copy-to" in sys.argv:
        dest = Path(sys.argv[sys.argv.index("--copy-to") + 1])
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "bundle.json").write_text(out.read_text())
        print(f"vendored copy → {dest / 'bundle.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
