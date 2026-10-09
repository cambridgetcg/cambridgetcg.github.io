#!/usr/bin/env python3
"""YOUSPEAK lift — the inverse of translate.py.

Lifts a YOUSPEAK word UP into target-language rendering. Given a YOUSPEAK
canonical word, walks its donor-morphemes, gathers tradition-specific frame-
data from `morphemes.json`, and produces a three-level rendering:

  1. Compositional gloss   — literal morpheme-by-morpheme decomposition
  2. Idiomatic paraphrase  — target-natural-language version (from canon definition)
  3. Frame-fragment notes  — each donor tradition's specific contribution

This is the operational inverse of ANAKALYPSE: where `translate.py` unfolds an
external word into components and routes each to canon-or-gap, `lift.py` unfolds
a YOUSPEAK word into its donor-traditions and shows what each contributes. The
two tools compose into a round-trip diagnostic (the planned `round_trip.py`).

Usage:
    python3 lift.py kimme                    # lift one canon word
    python3 lift.py walkekin                 # show all three rendering levels
    python3 lift.py --list-canon             # list every canon entry by tier
    python3 lift.py --tradition tocharian    # canon words drawing on a tradition

Architecture:
  - canon/**/*.md          — primary source (frontmatter + ## Definition + body)
  - script/morphemes.json  — donor-morpheme enrichment (codepoint, native script, meaning)
  - output                 — a lifting-report on stdout

The tool does NOT auto-translate beyond the structural rendering. A human
discerner uses the report when writing for non-YOUSPEAK readers, when sanity-
checking that a forge actually unfolds back to its claimed components, or when
auditing donor-coverage across the canon.

See TRANSLATION.md Section VIII for the architectural context.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
YOUSPEAK_ROOT = SCRIPT_DIR.parent
CANON_DIR = YOUSPEAK_ROOT / "canon"
MORPHEMES_FILE = YOUSPEAK_ROOT / "script" / "morphemes.json"

sys.path.insert(0, str(SCRIPT_DIR))
from assess import split_frontmatter, parse_frontmatter  # noqa: E402


# ---------------------------------------------------------------------------
# Donor-block parsing (the frontmatter parser in assess.py does not handle
# YAML list-style entries, so we walk the raw frontmatter for the donors block)
# ---------------------------------------------------------------------------

_DONOR_LINE_RE = re.compile(
    r"""^\s*-\s*
        (?P<tradition>[A-Za-z][A-Za-z0-9/_-]*)
        \s*:\s*
        (?P<morpheme>[^(\s]+)
        (?:\s*\(\s*(?P<note>.+)\)\s*)?
        \s*$""",
    re.VERBOSE,
)


def parse_donor_block(raw_frontmatter: str) -> list[dict]:
    """Walk the frontmatter text and extract the donors: list.

    Handles multi-line list items — a list item begins with `  - ` and continues
    across subsequent more-indented non-list lines (a common pattern for long
    parenthetical notes that wrap).
    """
    donors: list[dict] = []
    lines = raw_frontmatter.splitlines()
    in_donors = False
    current_item = ""

    def flush() -> None:
        nonlocal current_item
        text = current_item.strip()
        current_item = ""
        if not text:
            return
        # _DONOR_LINE_RE expects the leading "- " preserved
        m = _DONOR_LINE_RE.match("- " + text[2:] if text.startswith("- ") else "- " + text)
        if m:
            donors.append({
                "tradition": m.group("tradition"),
                "morpheme": m.group("morpheme"),
                "note": (m.group("note") or "").strip(),
            })
        else:
            raw = text[2:] if text.startswith("- ") else text
            donors.append({"tradition": "", "morpheme": raw, "note": ""})

    for line in lines:
        stripped = line.strip()
        if not in_donors:
            if re.match(r"^donors:\s*$", line):
                in_donors = True
            continue
        if not (line.startswith(" ") or line.startswith("\t")):
            flush()
            in_donors = False
            continue
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            flush()
            current_item = stripped
        else:
            if current_item:
                current_item = current_item.rstrip() + " " + stripped
    flush()
    return donors


# ---------------------------------------------------------------------------
# Canon discovery
# ---------------------------------------------------------------------------

def _read_canon_frontmatter(path: Path) -> tuple[dict, str, str]:
    """Return (frontmatter_dict, raw_frontmatter_text, body_text)."""
    text = path.read_text()
    raw, body = split_frontmatter(text)
    return parse_frontmatter(raw), raw, body


def _word_of(fm: dict) -> str:
    """Some canon entries use `word:`, some (worship-action/) use `candidate:`."""
    return str(fm.get("word") or fm.get("candidate") or "").strip()


def find_canon_file(word: str) -> Path | None:
    """Locate the canon entry whose declared word/candidate matches."""
    word_l = word.lower()
    for md in CANON_DIR.rglob("*.md"):
        if md.name == "README.md":
            continue
        try:
            fm, _, _ = _read_canon_frontmatter(md)
        except Exception:
            continue
        if _word_of(fm).lower() == word_l:
            return md
    return None


def list_canon_entries() -> list[tuple[str, str, Path]]:
    """Return [(word, tier, path)] for every canon entry that declares a word."""
    out: list[tuple[str, str, Path]] = []
    for md in CANON_DIR.rglob("*.md"):
        if md.name == "README.md":
            continue
        try:
            fm, _, _ = _read_canon_frontmatter(md)
        except Exception:
            continue
        word = _word_of(fm)
        if not word:
            continue
        try:
            rel = md.relative_to(CANON_DIR)
            tier = rel.parts[0] if len(rel.parts) >= 2 else "(top-level)"
        except ValueError:
            tier = "(unknown)"
        out.append((word, tier, md))
    return sorted(out)


# ---------------------------------------------------------------------------
# Section extraction from canon body
# ---------------------------------------------------------------------------

_ITALIC_STUB_RE = re.compile(r"^_Written by Nuance:.+_\s*$", re.MULTILINE)


def extract_section(body: str, heading: str) -> str:
    """Return the text under `## <heading>`, until the next `## ` or end."""
    pat = re.compile(
        rf"^##\s+{re.escape(heading)}\s*\n(.+?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    m = pat.search(body)
    if not m:
        return ""
    content = m.group(1).strip()
    return content


def first_meaningful_paragraph(text: str) -> str:
    """First paragraph that isn't a stub-placeholder or comment."""
    if not text:
        return ""
    for block in re.split(r"\n\s*\n", text):
        b = block.strip()
        if not b:
            continue
        if _ITALIC_STUB_RE.match(b):
            continue
        if b.startswith("<!--"):
            continue
        return b
    return ""


# ---------------------------------------------------------------------------
# Morpheme enrichment from script/morphemes.json
# ---------------------------------------------------------------------------

def load_morphemes() -> list[dict]:
    if not MORPHEMES_FILE.exists():
        return []
    try:
        with MORPHEMES_FILE.open() as f:
            data = json.load(f)
    except Exception:
        return []
    return data.get("morphemes", [])


def enrich_donor(donor: dict, morphemes: list[dict]) -> dict:
    """If the donor's morpheme matches morphemes.json, attach codepoint et al."""
    morpheme = donor.get("morpheme", "").lower()
    if not morpheme:
        return donor
    for m in morphemes:
        if m.get("latin", "").lower() == morpheme:
            return {
                **donor,
                "codepoint": m.get("codepoint"),
                "native_script": m.get("native"),
                "morpheme_meaning": m.get("meaning"),
                "morpheme_tongue": m.get("tongue"),
                "used_in_words": m.get("used_in", []),
            }
    return donor


# ---------------------------------------------------------------------------
# Lifting — the three levels of rendering
# ---------------------------------------------------------------------------

def lift(word: str) -> dict:
    path = find_canon_file(word)
    if path is None:
        return {
            "word": word,
            "status": "not-in-canon",
            "suggestion": (
                f"No canon entry found for '{word}'. Check spelling, or look in "
                "labs/logos/experiments/ for unforged candidates."
            ),
        }

    fm, raw, body = _read_canon_frontmatter(path)
    donors = parse_donor_block(raw)
    morphemes = load_morphemes()
    donors_enriched = [enrich_donor(d, morphemes) for d in donors]

    definition = first_meaningful_paragraph(extract_section(body, "Definition"))
    full_sense = first_meaningful_paragraph(extract_section(body, "Full sense"))
    etymology = first_meaningful_paragraph(extract_section(body, "Etymology"))
    not_confused = extract_section(body, "Not confused with")

    gap = str(fm.get("gap", "")).strip()

    # Level 1 — Compositional gloss
    if donors_enriched:
        parts = []
        for d in donors_enriched:
            piece = f"{d.get('tradition') or '?'}:{d.get('morpheme', '')}"
            meaning = d.get("morpheme_meaning") or d.get("note")
            if meaning:
                piece += f" ({meaning})"
            parts.append(piece)
        compositional = " + ".join(parts)
    else:
        compositional = "(no donors recorded in canon frontmatter — check the experiment file in genealogy.experiment)"

    # Level 2 — Idiomatic paraphrase
    idiomatic = definition or full_sense or gap or "(canon body not yet written; gap-line is the only source)"

    # Level 3 — Frame-fragment notes
    frame_notes: list[str] = []
    for d in donors_enriched:
        bits: list[str] = []
        if d.get("tradition"):
            head = f"**{d['tradition']}** *{d.get('morpheme', '')}*"
        else:
            head = f"*{d.get('morpheme', '')}*"
        bits.append(head)
        if d.get("native_script"):
            bits.append(f"({d['native_script']})")
        if d.get("morpheme_meaning"):
            bits.append(f"— {d['morpheme_meaning']}")
        elif d.get("note"):
            bits.append(f"— {d['note']}")
        if d.get("codepoint"):
            bits.append(f"[{d['codepoint']}]")
        if d.get("used_in_words"):
            others = [w for w in d["used_in_words"] if w.lower() != word.lower()]
            if others:
                bits.append(f"also in: {', '.join(others)}")
        frame_notes.append(" ".join(bits))

    return {
        "word": word,
        "status": "lifted",
        "canon_file": str(path.relative_to(YOUSPEAK_ROOT)),
        "pronunciation": str(fm.get("pronunciation", "")).strip(),
        "part_of_speech": str(fm.get("part_of_speech", "")).strip(),
        "gap": gap,
        "definition": definition,
        "full_sense": full_sense,
        "etymology": etymology,
        "not_confused_with": not_confused,
        "donors": donors_enriched,
        "compositional_gloss": compositional,
        "idiomatic_paraphrase": idiomatic,
        "frame_fragments": frame_notes,
    }


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def render_report(result: dict) -> str:
    if result.get("status") == "not-in-canon":
        return (
            f"Not in canon: {result['word']}\n"
            f"  {result['suggestion']}"
        )

    lines: list[str] = [f"# Lifting: {result['word']}", ""]
    meta: list[str] = []
    if result["pronunciation"]:
        meta.append(f"**Pronunciation:** {result['pronunciation']}")
    if result["part_of_speech"]:
        meta.append(f"**Part of speech:** {result['part_of_speech']}")
    meta.append(f"**Canon entry:** `{result['canon_file']}`")
    lines.extend(meta + [""])

    if result["gap"]:
        lines.extend(["## Gap (what is named)", "", result["gap"], ""])

    lines.extend([
        "## Level 1 — Compositional gloss",
        "",
        result["compositional_gloss"],
        "",
    ])

    lines.extend([
        "## Level 2 — Idiomatic paraphrase",
        "",
        result["idiomatic_paraphrase"],
        "",
    ])

    lines.extend(["## Level 3 — Frame-fragments", ""])
    if result["frame_fragments"]:
        for n in result["frame_fragments"]:
            lines.append(f"- {n}")
    else:
        lines.append("_(no donor frame-data — donors not recorded in canon frontmatter)_")
    lines.append("")

    if result["etymology"]:
        lines.extend(["## Etymology (from canon)", "", result["etymology"], ""])

    if result["not_confused_with"]:
        lines.extend(["## Not confused with", "", result["not_confused_with"], ""])

    return "\n".join(lines)


def render_list_canon() -> str:
    entries = list_canon_entries()
    by_tier: dict[str, list[str]] = {}
    for word, tier, _ in entries:
        by_tier.setdefault(tier, []).append(word)
    lines = [f"# Canon inventory ({len(entries)} entries across {len(by_tier)} tiers)", ""]
    for tier in sorted(by_tier):
        words = sorted(by_tier[tier])
        lines.append(f"## {tier}/  ({len(words)})")
        lines.append("")
        for w in words:
            lines.append(f"- {w}")
        lines.append("")
    return "\n".join(lines)


def render_by_tradition(tradition: str) -> str:
    tradition_l = tradition.lower()
    hits: list[tuple[str, list[dict]]] = []
    for word, _tier, path in list_canon_entries():
        try:
            _, raw, _ = _read_canon_frontmatter(path)
        except Exception:
            continue
        donors = parse_donor_block(raw)
        matches = [d for d in donors if d.get("tradition", "").lower() == tradition_l]
        if matches:
            hits.append((word, matches))
    if not hits:
        return f"No canon entries draw on tradition: {tradition}"
    lines = [f"# Canon entries drawing on {tradition} ({len(hits)} entries)", ""]
    for word, matches in sorted(hits):
        for m in matches:
            note = f" ({m['note']})" if m.get("note") else ""
            lines.append(f"- **{word}** ← {tradition}:{m['morpheme']}{note}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="Lift a YOUSPEAK word UP into target-language rendering (inverse of translate.py)."
    )
    p.add_argument("word", nargs="?", help="YOUSPEAK canonical word to lift")
    p.add_argument("--list-canon", action="store_true", help="list all canon entries by tier")
    p.add_argument("--tradition", metavar="NAME",
                   help="list every canon entry drawing on the named donor-tradition")
    p.add_argument("--with-bridge", action="store_true",
                   help="also include cross-project bridge-state (TRUE-LOVE operational-home, "
                        "Forgotten-Way status, partnership draft); uses syzygy.py per SYNDESMOS.md")
    args = p.parse_args()

    if args.list_canon:
        print(render_list_canon())
        return 0
    if args.tradition:
        print(render_by_tradition(args.tradition))
        return 0
    if not args.word:
        p.print_help()
        return 2

    result = lift(args.word)
    print(render_report(result))

    if args.with_bridge:
        # Cross-project augmentation per Yu's "go deeper into nesting" invocation.
        # Lift the word in cathedral-and-partnership together; syzygy.py provides
        # the render-fragment that nests partnership-state into the lift-output.
        try:
            from syzygy import render_bridge_state_summary
            bridge_fragment = render_bridge_state_summary(args.word)
            if bridge_fragment:
                print()
                print(bridge_fragment)
        except ImportError:
            pass  # syzygy.py absent — graceful degradation; lift still works

    return 0 if result.get("status") == "lifted" else 1


if __name__ == "__main__":
    sys.exit(main())
