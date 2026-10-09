#!/usr/bin/env python3
"""YOUSPEAK Pipeline — Nuance-discipline check.

Operationalises NUANCE-NATURE §VI: the careful-inward + honest-outward
dual-quality the cathedral's documentation-persona instantiates and the
19+ traditions converge on.

Reads a canon entry (or experiment file), inspects the mathema_signature's
optional `nuance_quality` block, reports both poles, and surfaces
tradition_resonance suggestions from the entry's donors.

Verdicts:
    pass     — both poles named, tradition_resonance non-empty
    partial  — one pole or tradition_resonance missing
    absent   — no nuance_quality block

Usage:
    python3 nuance_check.py <file.md>              check one entry
    python3 nuance_check.py --batch <dir>          check every entry in a dir
    python3 nuance_check.py --registry             print 19-tradition registry
    python3 nuance_check.py --suggest <tradition>  recommend pair-form + group
    python3 nuance_check.py --gaps <dir>           list entries lacking the block
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Re-use the v2 frontmatter parser from assess.py to keep one source of truth.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from assess import parse_frontmatter, split_frontmatter  # noqa: E402

# ---------------------------------------------------------------------------
# The 19-tradition + mathema-analog registry — sourced from NUANCE-NATURE §I-II
# and discipline/nuance-echoes.md §multi-language-echo-registry.
# Each entry: (donor-language, careful-pole, honest-pole, group, gloss).
# ---------------------------------------------------------------------------

REGISTRY: list[tuple[str, str, str, str, str]] = [
    ("hebrew",     "tzeniut",     "emet",        "A", "modest-reserve + truth-firm"),
    ("greek",      "aidōs",       "parrēsia",    "B", "reverent-shame + bold-honest-speech"),
    ("sanskrit",   "lajjā",       "satya",       "A", "modesty-shame + cosmic-truth"),
    ("arabic",     "ḥayāʾ",       "ṣidq",        "A", "modesty (root-cognate with ḥayāt/life) + truthfulness"),
    ("latin",      "verecundia",  "sinceritas",  "A", "proper-modesty + integrity-without-pretense"),
    ("mandarin",   "hánxù",       "zhēnchéng",   "C", "subtle-restraint + sincerity-deep"),
    ("cantonese",  "怕醜 pa-cau",  "肯叫 hang-giu", "C", "shy/bashful + willing-to-name"),
    ("korean",     "chaeryeom",   "jeong",       "C", "proper-restraint + accumulated-affection"),
    ("japanese",   "enryo",       "makoto",      "C", "modest-restraint + heart-sincerity"),
    ("yoruba",     "ìtìjú",       "ìfẹ́",         "D", "shyness-with-honor + love-that-widens"),
    ("lakota",     "ksapa",       "mitakuye",    "D", "quiet-wisdom + all-my-relations"),
    ("norse",      "ráð",         "traust",      "D", "careful-counsel + trust"),
    ("egyptian",   "hesi",        "ma'at",       "E", "silent-reverent + cosmic-truth-order"),
    ("akkadian",   "pulhu",       "kittu",       "E", "reverent-fear + firm-truth"),
    ("sumerian",   "me-receiving", "me-naming",  "E", "received-not-authored ordinance"),
    ("aramaic",    "anavah",      "qushta",      "A", "humility-of-place + truth"),
    ("persian",    "adab",        "ḥaqq",        "B", "refined-conduct + the Real"),
    ("pali",       "hiri",        "sacca",       "A", "moral-conscience-shame + truth"),
    ("tibetan",    "dakpa",       "namdak",      "F", "purity-of-attention + utterly-honest"),
    ("confucian",  "jūnzǐ",       "chéng",       "B", "proper-conduct + cosmic-sincerity"),
]

# Structural analogs from mathema/physics/info/cognition (NUANCE-NATURE §VII.4).
ANALOGS: list[tuple[str, str, str]] = [
    ("math:pi",          "irrational-uncountable", "structurally-precise"),
    ("math:godel",       "unprovable-within-system", "names-what-is-provable-firmly"),
    ("math:natural-transformation", "commutes-with-context", "preserves-structure"),
    ("physics:heisenberg", "uncertainty-pair", "claim-what-can-be-claimed"),
    ("physics:entanglement", "in-relation-across-distance", "correlation-without-transmission"),
    ("info:shannon",     "density-through-restraint", "maximum-meaning-per-symbol"),
    ("info:kolmogorov",  "minimum-description-length", "compressive-fidelity"),
    ("cognition:attention", "weighs-context-quietly", "outputs-decisively"),
    ("biocog:deer-edge", "alert-careful",         "ventures-when-conditions-right"),
    ("cosmos:horizon",   "honest-about-the-unseen", "certain-about-the-observable"),
]

GROUPS: dict[str, str] = {
    "A": "Modesty-and-Truth (dominant cluster; six traditions)",
    "B": "Respect-and-Bold-Speech (carefulness earns parrēsia)",
    "C": "Restraint-and-Sincerity (East-Asian density-through-restraint)",
    "D": "Quiet-Wisdom-in-Relation (relational-not-isolated)",
    "E": "Reverent-Fear-and-Cosmic-Truth (received-not-authored)",
    "F": "Pure-Attention-Preceding-Speech (Tibetan / Zen analog)",
}

# Map donor-tradition tag (used in canon entries' donors list) → registry key.
DONOR_TO_TRADITION: dict[str, str] = {
    "Hebrew":      "hebrew",
    "Greek":       "greek",
    "Sanskrit":    "sanskrit",
    "Arabic":      "arabic",
    "Latin":       "latin",
    "Mandarin":    "mandarin",
    "Cantonese":   "cantonese",
    "Korean":      "korean",
    "Japanese":    "japanese",
    "Yoruba":      "yoruba",
    "Lakota":      "lakota",
    "Norse":       "norse",
    "Icelandic":   "norse",
    "Egyptian":    "egyptian",
    "Akkadian":    "akkadian",
    "Sumerian":    "sumerian",
    "Aramaic":     "aramaic",
    "Persian":     "persian",
    "Sufi":        "persian",
    "Pali":        "pali",
    "Tibetan":     "tibetan",
    "Chinese":     "confucian",
    "Confucian":   "confucian",
    "Bantu":       "yoruba",   # nearest pair-form group (D)
    "Avestan":     "akkadian", # cosmic-order register
}


# ---------------------------------------------------------------------------
# Parsing — extract mathema_signature.nuance_quality from frontmatter
# ---------------------------------------------------------------------------

def extract_nuance_quality(text: str) -> dict | None:
    """Return the nuance_quality dict if present in the frontmatter, else None.

    The frontmatter parser used elsewhere flattens nested blocks only one
    level deep. The nuance_quality is a sub-block of mathema_signature, so we
    parse it with a targeted regex.
    """
    raw, _ = split_frontmatter(text)
    if not raw:
        return None
    m = re.search(
        r"^\s{2}nuance_quality:\s*\n((?:\s{4,}[\w_]+:\s*.+\n?)+)",
        raw,
        re.MULTILINE,
    )
    if not m:
        return None
    block = m.group(1)
    out: dict = {}
    for line in block.splitlines():
        sub = re.match(r"\s+([\w_]+):\s*(.*)", line)
        if not sub:
            continue
        key, val = sub.group(1), sub.group(2).strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            out[key] = [x.strip().strip("\"'") for x in inner.split(",")] if inner else []
        else:
            out[key] = val.strip("\"'")
    return out


def extract_donor_traditions(text: str) -> list[str]:
    """Best-effort: surface donor-tradition tokens from the `donors:` block.

    Walks frontmatter line-by-line from `donors:` until a non-indented key,
    catching every line that opens with `- <Donor>:` (multi-line continuations
    of a list-item are skipped naturally because they don't start with `-`).
    """
    raw, _ = split_frontmatter(text)
    if not raw:
        return []
    in_donors = False
    traditions: list[str] = []
    for line in raw.splitlines():
        if re.match(r"^donors:\s*", line):
            in_donors = True
            continue
        if not in_donors:
            continue
        if re.match(r"^[A-Za-z_]+:", line):  # next top-level key — end of donors
            break
        token = re.match(r"\s+-\s+([A-Z][a-zA-Z]+)\s*:", line)
        if token:
            traditions.append(token.group(1))
    return traditions


def candidate_name(text: str) -> str:
    raw, _ = split_frontmatter(text)
    fm = parse_frontmatter(raw)
    return fm.get("word") or fm.get("candidate") or fm.get("id") or "—"


# ---------------------------------------------------------------------------
# Verdict logic
# ---------------------------------------------------------------------------

def verdict_for(nq: dict | None) -> str:
    if not nq:
        return "absent"
    careful = nq.get("careful_inward")
    honest = nq.get("honest_outward")
    resonance = nq.get("tradition_resonance") or []
    if careful and honest and (resonance and resonance != [""]):
        return "pass"
    return "partial"


def suggest_resonance(traditions: list[str]) -> list[tuple[str, str]]:
    """Return list of (tradition-key, pair-form) suggestions from donor-list."""
    suggestions: list[tuple[str, str]] = []
    seen: set[str] = set()
    for donor in traditions:
        key = DONOR_TO_TRADITION.get(donor)
        if key and key not in seen:
            for row in REGISTRY:
                if row[0] == key:
                    suggestions.append((key, f"{row[1]} + {row[2]}"))
                    seen.add(key)
                    break
    return suggestions


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def render_one(path: Path, text: str) -> str:
    name = candidate_name(text)
    nq = extract_nuance_quality(text)
    traditions = extract_donor_traditions(text)
    verdict = verdict_for(nq)
    suggestions = suggest_resonance(traditions)

    lines = [f"# nuance_check — {path.name} ({name})", ""]
    lines.append(f"verdict: {verdict}")
    if nq:
        lines.append("")
        lines.append("## nuance_quality")
        for k in ("careful_inward", "honest_outward", "tradition_resonance", "pattern_position"):
            v = nq.get(k)
            marker = "✓" if v else "·"
            lines.append(f"  {marker} {k:24} {v if v else '—'}")
        if nq.get("pattern_position") in GROUPS:
            lines.append(f"    └─ group: {GROUPS[nq['pattern_position']]}")
    else:
        lines.append("")
        lines.append("## nuance_quality")
        lines.append("  (block absent — recommend adding to mathema_signature)")

    if suggestions:
        lines.append("")
        lines.append("## tradition_resonance hint (from donors)")
        for tag, pair in suggestions:
            lines.append(f"  - {tag:12} {pair}")
    elif traditions:
        lines.append("")
        lines.append(f"## donors detected: {', '.join(traditions)} (no registry hint)")

    return "\n".join(lines)


def render_registry() -> str:
    lines = ["# Nuance pattern — 19-tradition + analog registry", ""]
    lines.append("## linguistic traditions")
    lines.append(f"{'tradition':12} {'careful pole':14} {'honest pole':14} group  gloss")
    lines.append("-" * 78)
    for tag, careful, honest, group, gloss in REGISTRY:
        lines.append(f"{tag:12} {careful:14} {honest:14} {group:5}  {gloss}")
    lines.append("")
    lines.append("## groups")
    for g, label in GROUPS.items():
        lines.append(f"  {g}: {label}")
    lines.append("")
    lines.append("## structural analogs (math / physics / info / cognition)")
    for tag, careful, honest in ANALOGS:
        lines.append(f"  - {tag:24} {careful}  /  {honest}")
    return "\n".join(lines)


def render_suggest(token: str) -> str:
    key = DONOR_TO_TRADITION.get(token, token.lower())
    for tag, careful, honest, group, gloss in REGISTRY:
        if tag == key:
            return (
                f"# suggestion for '{token}'\n\n"
                f"tradition       {tag}\n"
                f"careful pole    {careful}\n"
                f"honest pole     {honest}\n"
                f"pattern_position {group}  ({GROUPS[group]})\n"
                f"gloss           {gloss}\n"
            )
    return f"no registry entry for '{token}'. Try one of: {', '.join(r[0] for r in REGISTRY)}"


def render_gaps(directory: Path) -> str:
    files = sorted(directory.rglob("*.md"))
    rows: list[tuple[str, str, str]] = []
    for f in files:
        text = f.read_text()
        nq = extract_nuance_quality(text)
        verdict = verdict_for(nq)
        if verdict != "pass":
            rows.append((f.name, candidate_name(text), verdict))
    lines = [f"# nuance-discipline gaps in {directory}", ""]
    lines.append(f"{'file':32} {'word':20} verdict")
    lines.append("-" * 64)
    for fname, word, v in rows:
        lines.append(f"{fname:32} {word:20} {v}")
    lines.append("")
    lines.append(f"total: {len(rows)} entries need attention (of {len(files)} scanned)")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="YOUSPEAK Nuance-discipline check")
    ap.add_argument("path", type=Path, nargs="?", help="entry file (or directory if --batch/--gaps)")
    ap.add_argument("--batch", action="store_true", help="check every .md in a directory")
    ap.add_argument("--registry", action="store_true", help="print the 19-tradition + analog registry")
    ap.add_argument("--suggest", metavar="DONOR", help="show pair-form suggestion for a donor tag")
    ap.add_argument("--gaps", action="store_true", help="list entries lacking the nuance_quality block")
    args = ap.parse_args()

    if args.registry:
        print(render_registry())
        return 0
    if args.suggest:
        print(render_suggest(args.suggest))
        return 0

    if not args.path:
        ap.print_help()
        return 2

    if args.gaps:
        if not args.path.is_dir():
            print(f"error: {args.path} is not a directory", file=sys.stderr)
            return 1
        print(render_gaps(args.path))
        return 0

    if args.batch:
        if not args.path.is_dir():
            print(f"error: {args.path} is not a directory", file=sys.stderr)
            return 1
        for f in sorted(args.path.rglob("*.md")):
            print(render_one(f, f.read_text()))
            print()
        return 0

    if not args.path.is_file():
        print(f"error: {args.path} is not a file", file=sys.stderr)
        return 1
    print(render_one(args.path, args.path.read_text()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
