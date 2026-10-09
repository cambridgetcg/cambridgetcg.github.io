#!/usr/bin/env python3
"""YOUSPEAK Pipeline — candidate coinage assessor.

Reads an experiment file (markdown with YAML-ish frontmatter), computes
mechanical phonetic metrics, surfaces the five-axis rubric, and emits a verdict.

Usage:
    python3 assess.py <experiment.md>          grade and report
    python3 assess.py --init <path>            stub a new experiment file
    python3 assess.py --batch <dir>            assess every .md in dir
    python3 assess.py status <agent>           report YOUSPEAK fluency stage
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

#   v2 rubric (post-Constitution, 2026-04-24) — 6 axes mapping to the
#   Six Foundations (EUMATHE, SAPHE, ANAKALYPSE, POLYPHONE, HARMONE, PRAGMA).
#   See CONSTITUTION.md for rationale.
#
#   AXES_V1 is retained for backward-compatible scoring of pre-Constitution
#   experiment files. If the frontmatter has all 5 v1-axes but none of the new
#   ones, the v1 rubric is applied; if 6-axis frontmatter is present, v2 is used.

AXES_V1 = [
    "gap_validity",
    "phonetic_weight",
    "semantic_coverage",
    "cross_linguistic_uniqueness",
    "memorability",
]

WEIGHTS_V1 = {
    "gap_validity": 0.25,
    "phonetic_weight": 0.20,
    "semantic_coverage": 0.25,
    "cross_linguistic_uniqueness": 0.15,
    "memorability": 0.15,
}

AXES_V2 = [
    "gap_validity",
    "learnability",
    "clarity_yield",
    "semantic_coverage",
    "polyphone_balance",
    "groundedness",
]

WEIGHTS_V2 = {
    "gap_validity":      0.20,  # gap exists
    "learnability":      0.20,  # EUMATHE — easy to learn/write/speak
    "clarity_yield":     0.15,  # SAPHE + ANAKALYPSE — clarifies and unfolds
    "semantic_coverage": 0.15,  # word carries its concept
    "polyphone_balance": 0.15,  # POLYPHONE — etymological breadth
    "groundedness":      0.15,  # PRAGMA — can be pointed-at
}

# Primary (current) axes: v2 after 2026-04-24.
AXES = AXES_V2
WEIGHTS = WEIGHTS_V2

VOWEL_CHARS = "aeiouy"


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return "", text
    return parts[1].strip(), parts[2].lstrip()


def _cast(v: str):
    v = v.strip()
    if v.lower() in ("null", "none", ""):
        return None
    if v.lower() == "true":
        return True
    if v.lower() == "false":
        return False
    try:
        return int(v) if "." not in v else float(v)
    except ValueError:
        return v.strip("\"'")


def parse_frontmatter(raw: str) -> dict:
    """Tiny YAML subset: top-level key:value, bracket lists, one-level nested dicts."""
    out: dict = {}
    current_dict: dict | None = None
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith("  ") and current_dict is not None:
            m = re.match(r"\s+([\w_]+):\s*(.*)", line)
            if m:
                current_dict[m.group(1)] = _cast(m.group(2))
            continue
        m = re.match(r"([\w_]+):\s*(.*)", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value == "" or value == "{}":
            out[key] = {}
            current_dict = out[key]
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            out[key] = [x.strip().strip("\"'") for x in inner.split(",")] if inner else []
            current_dict = None
        else:
            out[key] = _cast(value)
            current_dict = None
    return out


def syllable_count(word: str) -> int:
    if not word:
        return 0
    count = 0
    in_vowel = False
    for ch in word.lower():
        is_vowel = ch in VOWEL_CHARS
        if is_vowel and not in_vowel:
            count += 1
        in_vowel = is_vowel
    return max(count, 1)


def vowel_ratio(word: str) -> float:
    letters = [c for c in word if c.isalpha()]
    if not letters:
        return 0.0
    return round(sum(1 for c in letters if c.lower() in VOWEL_CHARS) / len(letters), 2)


def sonority_profile(word: str) -> str:
    return "".join("V" if c.lower() in VOWEL_CHARS else "C" for c in word if c.isalpha())


def mechanical_metrics(candidate: str) -> dict:
    return {
        "length": len(candidate),
        "syllables": syllable_count(candidate),
        "vowel_ratio": vowel_ratio(candidate),
        "profile": sonority_profile(candidate),
    }


def _detect_rubric(axes: dict) -> tuple[list[str], dict]:
    """Return (axes-list, weights-dict) for whichever rubric the frontmatter uses.

    v2 detection: at least 4 of the 6 v2-axes are present and not-null.
    v1 fallback: otherwise use v1 axes.
    """
    v2_present = sum(1 for a in AXES_V2 if axes.get(a) is not None)
    if v2_present >= 4:
        return AXES_V2, WEIGHTS_V2
    return AXES_V1, WEIGHTS_V1


def weighted_total(axes: dict) -> float | None:
    """Compute weighted total using whichever rubric matches the frontmatter."""
    if not axes:
        return None
    active_axes, active_weights = _detect_rubric(axes)
    if any(axes.get(a) is None for a in active_axes):
        return None
    return round(sum(axes[a] * active_weights[a] for a in active_axes), 2)


def weighted_total_v1(axes: dict) -> float | None:
    """Force v1 rubric scoring (for comparison / backward-compat)."""
    if not axes or any(axes.get(a) is None for a in AXES_V1):
        return None
    return round(sum(axes[a] * WEIGHTS_V1[a] for a in AXES_V1), 2)


def weighted_total_v2(axes: dict) -> float | None:
    """Force v2 rubric scoring (for re-audit of pre-Constitution words)."""
    if not axes or any(axes.get(a) is None for a in AXES_V2):
        return None
    return round(sum(axes[a] * WEIGHTS_V2[a] for a in AXES_V2), 2)


def verdict_for(total: float | None) -> str:
    if total is None:
        return "unscored"
    if total >= 7.5:
        return "canon"
    if total >= 5.0:
        return "refine"
    return "archive"


def render_report(path: Path, fm: dict, mech: dict, total: float | None, verdict: str) -> str:
    axes = fm.get("axes") or {}
    lines = [
        f"# assess — {path.name}",
        "",
        f"candidate:  {fm.get('candidate', '—')}",
        f"gap:        {fm.get('gap', '—')}",
        "",
        "## mechanical",
    ]
    for k, v in mech.items():
        lines.append(f"  {k:14} {v}")
    lines += ["", "## axes (0–10)"]
    for a in AXES:
        score = axes.get(a)
        marker = "·" if score is None else "✓"
        lines.append(f"  {marker} {a:32} {score if score is not None else '—'}")
    lines += [
        "",
        f"weighted_total:  {total if total is not None else '—'}",
        f"verdict:         {verdict}",
    ]
    return "\n".join(lines)


INIT_TEMPLATE = """---
id: {stem}
candidate:
gap:
donors: []
axes:
  # v2 rubric (post-Constitution). See CONSTITUTION.md for the 6 axes.
  gap_validity: null      # does the gap exist? (0-10)
  learnability: null      # EUMATHE — easy to learn/write/speak (0-10)
  clarity_yield: null     # SAPHE + ANAKALYPSE — clarifies and unfolds (0-10)
  semantic_coverage: null # the word carries its concept (0-10)
  polyphone_balance: null # POLYPHONE — etymological breadth (0-10)
  groundedness: null      # PRAGMA — can be pointed-at in reality (0-10)
verdict: null
tier: null                # core | specialized | null
domain: null              # for specialized: liturgy | zerone | grammar | aesthetics | ...
nuance_quality:
  # Per NUANCE-NATURE.md §VI.2 — the meta-discipline across all Six Foundations.
  # Both poles required at canonization. Use pipeline/nuance_check.py --suggest <donor>
  # to surface the tradition's pair-form. Optional pre-canon; required for tier=core.
  careful_inward: null      # which careful-pole register (e.g. tzeniut, aidōs, hánxù, hesi)
  honest_outward: null      # which honest-pole register (e.g. emet, parrēsia, zhēnchéng, ma'at)
  tradition_resonance: []   # donor-traditions whose pair-form resonates with this forge
  pattern_position: null    # A | B | C | D | E | F  (see NUANCE-NATURE §II groups)
---

# {stem}

## The Gap
_What unnamed region does this candidate answer?_

## The Forge
_How was the candidate constructed? Which donors? What fusion?_

## Near-neighbours
_What existing words come close but miss? Why do they miss?_

## Trial sentences
_Use the candidate in 3 sentences. Does it hold?_
"""


def cmd_assess(path: Path) -> int:
    text = path.read_text()
    raw, _body = split_frontmatter(text)
    if not raw:
        print(f"error: no frontmatter in {path}", file=sys.stderr)
        return 2
    fm = parse_frontmatter(raw)
    candidate = fm.get("candidate") or ""
    mech = mechanical_metrics(candidate)
    total = weighted_total(fm.get("axes") or {})
    verdict = verdict_for(total)
    print(render_report(path, fm, mech, total, verdict))
    return 0


def cmd_init(path: Path) -> int:
    if path.exists():
        print(f"error: {path} exists", file=sys.stderr)
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(INIT_TEMPLATE.format(stem=path.stem))
    print(f"stubbed {path}")
    return 0


def cmd_status(agent: str) -> int:
    """Report an agent's YOUSPEAK fluency stage.

    Stage = how many of the agent's core vocabulary words are defined in
    DICTIONARY.md. The agent's core words are the bolded entries under the
    "## YOUSPEAK Vocabulary" heading in their identity.md.
    """
    home = Path.home()
    identity = home / "Love" / "instances" / agent / "identity.md"
    dictionary = home / "Love" / "instances" / "nuance" / "youspeak" / "DICTIONARY.md"

    if not identity.exists():
        print(f"error: no identity.md for agent '{agent}' at {identity}",
              file=sys.stderr)
        return 1
    if not dictionary.exists():
        print(f"error: DICTIONARY.md missing at {dictionary}", file=sys.stderr)
        return 1

    id_text = identity.read_text()
    dict_text = dictionary.read_text()

    vocab_match = re.search(
        r"##\s+YOUSPEAK Vocabulary.*?(?=\n##\s|\Z)",
        id_text,
        re.DOTALL,
    )
    if not vocab_match:
        print(f"{agent}: no 'YOUSPEAK Vocabulary' section in identity.md")
        return 0
    core_words = re.findall(r"\*\*([A-Za-z][A-Za-z-]+)\*\*", vocab_match.group(0))
    if not core_words:
        print(f"{agent}: no core vocabulary entries detected")
        return 0

    dict_entries = {
        m.group(1).lower()
        for m in re.finditer(r"^###\s+(\S+)", dict_text, re.MULTILINE)
    }

    defined = [w for w in core_words if w.lower() in dict_entries]
    stage = len(defined)
    total = len(core_words)

    print(f"{agent}: Stage {stage}/{total}")
    print(f"  core vocabulary ({total} words):")
    for w in core_words:
        mark = "+" if w.lower() in dict_entries else "-"
        print(f"    {mark} {w}")
    if stage < total:
        missing = [w for w in core_words if w.lower() not in dict_entries]
        print(f"  next beat: install entry for {missing[0]} in DICTIONARY.md")
    else:
        print(f"  fluent — all core words defined")
    return 0


def cmd_batch(directory: Path) -> int:
    if not directory.is_dir():
        print(f"error: {directory} is not a directory", file=sys.stderr)
        return 1
    # Recurse so core/, specialized/ and any future subdirectories are covered
    files = sorted(directory.rglob("*.md"))
    if not files:
        print(f"(no experiments in {directory})")
        return 0
    for f in files:
        cmd_assess(f)
        print()
    return 0


def main() -> int:
    # `assess.py status <agent>` — YOUSPEAK fluency report for a named agent
    if len(sys.argv) >= 3 and sys.argv[1] == "status":
        return cmd_status(sys.argv[2])

    ap = argparse.ArgumentParser(description="YOUSPEAK candidate assessor")
    ap.add_argument("path", type=Path, help="experiment file (or directory if --batch)")
    ap.add_argument("--init", action="store_true", help="stub a new experiment file")
    ap.add_argument("--batch", action="store_true", help="assess all .md files in a directory")
    args = ap.parse_args()
    if args.init:
        return cmd_init(args.path)
    if args.batch:
        return cmd_batch(args.path)
    return cmd_assess(args.path)


if __name__ == "__main__":
    sys.exit(main())
