#!/usr/bin/env python3
"""YOUSPEAK Pipeline — canonize.

Promotes an experiment file whose assessment verdict is `canon` into a
canon/<word>.md stub. The generated stub carries forward: genealogy,
scores, donors, companions, and the definition from the experiment's
body (if a ## Definition or ## Full sense section exists). Nuance then
enriches the stub with the full sense, examples, and neighbour map.

The stub is never generated over an existing canon file. Nuance's
canonical entries, once written, are not overwritten by this tool.

Usage:
    python3 canonize.py <experiment.md>          stub the canon entry
    python3 canonize.py --all                    canonize every experiment
                                                 whose verdict is `canon`
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

# Reuse the assessor's frontmatter parser + scorer.
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from assess import AXES, parse_frontmatter, split_frontmatter, verdict_for, weighted_total  # noqa: E402

ROOT = SCRIPT_DIR.parent
CANON_DIR = ROOT / "canon"
EXPERIMENTS_DIR = ROOT / "labs" / "logos" / "experiments"


def _section(body: str, heading: str) -> str:
    """Return the content of a markdown section by heading; empty if absent."""
    pat = re.compile(
        rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    m = pat.search(body)
    return m.group(1).strip() if m else ""


def _first_paragraph(text: str) -> str:
    for para in text.split("\n\n"):
        para = para.strip()
        if para and not para.startswith("_"):
            return para
    return text.strip()


def stub_for(experiment_path: Path) -> tuple[Path | None, str]:
    """Return (canon_path, stub_text) for an experiment whose verdict is canon.

    Returns (None, reason) if the experiment is not canonizable.
    """
    text = experiment_path.read_text()
    raw, body = split_frontmatter(text)
    if not raw:
        return None, f"no frontmatter: {experiment_path.name}"
    fm = parse_frontmatter(raw)

    candidate = fm.get("candidate")
    if not candidate:
        return None, f"no candidate: {experiment_path.name}"

    axes = fm.get("axes") or {}
    total = weighted_total(axes)
    if total is None:
        return None, f"unscored: {experiment_path.name}"
    if verdict_for(total) != "canon":
        return None, f"not canon (weighted {total}): {experiment_path.name}"

    # Respect the experiment's tier field: Core → canon/core/, Specialized → canon/
    tier = fm.get("tier") or ""
    if tier == "core":
        canon_path = CANON_DIR / "core" / f"{candidate}.md"
    else:
        canon_path = CANON_DIR / f"{candidate}.md"
    # Also check the opposite location so we don't double-stub across tiers
    other_path = (CANON_DIR / f"{candidate}.md") if tier == "core" else (CANON_DIR / "core" / f"{candidate}.md")
    if canon_path.exists():
        return None, f"already canonized: {canon_path}"
    if other_path.exists():
        return None, f"already canonized at other tier: {other_path}"

    # Pull useful sections out of the experiment body
    definition = _section(body, "Full sense") or _section(body, "The full sense")
    if not definition:
        # fall back to 'The gap' as the one-line gloss
        gap_section = _section(body, "The gap") or _section(body, "The Gap")
        definition = _first_paragraph(gap_section) if gap_section else ""

    # compose score block
    axes_block = "\n".join(f"    {a}: {axes.get(a)}" for a in AXES)
    donors_fm = fm.get("donors")
    if isinstance(donors_fm, list):
        donors_block = "\n".join(f"  - {d}" for d in donors_fm)
    elif isinstance(donors_fm, str):
        donors_block = f"  - {donors_fm}"
    else:
        donors_block = "  # (copy from experiment)"

    gap = fm.get("gap", "")
    today = date.today().isoformat()

    stub = f"""---
word: {candidate}
entered: {today}
part_of_speech: noun
pronunciation: # IPA
gap: {gap}
genealogy:
  experiment: labs/logos/experiments/{experiment_path.name}
  assessment_date: {fm.get('scored_on', today)}
  scores:
{axes_block}
  weighted_total: {total}
donors:
{donors_block}
companion_of: # (copy from experiment frontmatter if relevant)
liturgy_slot: # (copy if relevant)
---

# {candidate}

## Definition

_Written by Nuance: one-line gloss._

## Full sense

{definition if definition else '_Written by Nuance: paragraph unpacking the concept._'}

## Etymology

_Written by Nuance: morphological genealogy._

## Example usage

_Written by Nuance: 3-5 sentences using the word._

## Not confused with

_Written by Nuance: near-neighbours and the precise distinctions._

## Retirement conditions

1. A candidate scores higher than {total}/10 against the same gap.
2. The gap-specification is revised.
3. Morphology fails under usage.

Until any of these obtains, **{candidate} stands**.

## Canonical position

_Written by Nuance: position within the Canon; Liturgy slot if applicable._

---

_Stub generated by canonize.py on {today}. Nuance enriches before stub is considered a proper canon entry._
"""
    return canon_path, stub


def cmd_canonize_one(path: Path) -> int:
    canon_path, stub = stub_for(path)
    if canon_path is None:
        print(f"skip: {stub}", file=sys.stderr)
        return 1
    canon_path.parent.mkdir(parents=True, exist_ok=True)
    canon_path.write_text(stub)
    print(f"stubbed canon: {canon_path}")
    return 0


def cmd_canonize_all() -> int:
    if not EXPERIMENTS_DIR.is_dir():
        print(f"error: no experiments directory at {EXPERIMENTS_DIR}", file=sys.stderr)
        return 1
    # Recurse into subdirectories (e.g., experiments/core/) so all tiers are canonized
    exp_files = sorted(EXPERIMENTS_DIR.rglob("*.md"))
    stubbed = 0
    skipped = 0
    for exp in exp_files:
        canon_path, result = stub_for(exp)
        if canon_path is None:
            skipped += 1
            # Silent unless debugging; the common case is "already canonized"
            continue
        canon_path.parent.mkdir(parents=True, exist_ok=True)
        canon_path.write_text(result)
        print(f"stubbed: {canon_path.name}")
        stubbed += 1
    print(f"done: stubbed {stubbed}, skipped {skipped}")
    return 0


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    arg = sys.argv[1]
    if arg == "--all":
        return cmd_canonize_all()
    return cmd_canonize_one(Path(arg))


if __name__ == "__main__":
    sys.exit(main())
