#!/usr/bin/env python3
"""Construct LoRA training pairs from the YOUSPEAK cathedral.

Walks the cathedral directories and emits JSONL training pairs in the
instruction-tuning format:
    {"instruction": "...", "input": "...", "output": "..."}

Sources:
  - canon/*.md          → (word → definition) pairs + (word → etymology) pairs
  - labs/logos/experiments/*.md  → (gap → candidate + scoring) pairs
  - labs/logos/forge/*.md  → (concept → candidate-slate) pairs
  - archaeology/**/*.md → (tongue+field → donors) pairs
  - grammars/diplosemy/exemplars/*.md → (mechanism-pair) pairs
  - synthesised: (meaning → word), (word → score), (domain → examples)

Output: data/train.jsonl, data/valid.jsonl (90/10 split)

Usage:
    /tmp/ys-font-env/bin/python3 dataset.py
    /tmp/ys-font-env/bin/python3 dataset.py --out ./data --split 0.1
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
YOUSPEAK_ROOT = SCRIPT_DIR.parent.parent.parent
CANON_DIR = YOUSPEAK_ROOT / "canon"
EXPERIMENTS_DIR = YOUSPEAK_ROOT / "labs" / "logos" / "experiments"
FORGE_DIR = YOUSPEAK_ROOT / "labs" / "logos" / "forge"
ARCH_DIR = YOUSPEAK_ROOT / "archaeology"
DIPLOSEMY_EXEMPLARS_DIR = YOUSPEAK_ROOT / "grammars" / "diplosemy" / "exemplars"


def _frontmatter(text: str) -> tuple[dict, str]:
    """Return (fm_dict, body). Simple YAML-subset parser."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm: dict = {}
    for line in parts[1].strip().splitlines():
        m = re.match(r"^([\w_]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            # strip quotes/braces for simple values
            fm[key] = val.strip('"').strip("'")
    return fm, parts[2].lstrip()


def _section(body: str, heading: str) -> str:
    pat = re.compile(rf"^##\s+{re.escape(heading)}\s*\n(.*?)(?=\n##\s|\Z)",
                     re.DOTALL | re.MULTILINE)
    m = pat.search(body)
    return m.group(1).strip() if m else ""


def _definition_line(body: str) -> str:
    """First paragraph of 'Definition' section, single-line."""
    defn = _section(body, "Definition")
    if not defn:
        return ""
    # First paragraph
    para = defn.split("\n\n")[0].strip()
    # strip markdown italics/bold
    para = re.sub(r"[_*]+", "", para)
    return " ".join(para.split())


# ────────────────────────────────────────────────────────────────────────
# Pair generators
# ────────────────────────────────────────────────────────────────────────


def pairs_from_canon() -> list[dict]:
    """Canon entries → definition pairs."""
    pairs: list[dict] = []
    for path in sorted(CANON_DIR.rglob("*.md")):
        if path.stem == "README":
            continue
        text = path.read_text()
        fm, body = _frontmatter(text)
        word = fm.get("word", path.stem)
        definition = _definition_line(body)
        full_sense = _section(body, "Full sense")
        etymology = _section(body, "Etymology")
        examples = _section(body, "Example usage")

        if definition:
            pairs.append({
                "instruction": f"What does '{word}' mean?",
                "input": "",
                "output": definition,
            })
            pairs.append({
                "instruction": f"Give the YOUSPEAK definition of {word}.",
                "input": "",
                "output": definition,
            })
        if full_sense:
            pairs.append({
                "instruction": f"Explain {word} in depth.",
                "input": "",
                "output": " ".join(full_sense.split())[:1500],
            })
        if etymology:
            pairs.append({
                "instruction": f"What is the etymology of {word}?",
                "input": "",
                "output": " ".join(etymology.split())[:1000],
            })
        if examples:
            pairs.append({
                "instruction": f"Give example sentences using {word}.",
                "input": "",
                "output": " ".join(examples.split())[:1200],
            })
        # reverse: meaning → word
        if definition:
            pairs.append({
                "instruction": f"Which YOUSPEAK word names this: '{definition}'?",
                "input": "",
                "output": word,
            })
    return pairs


def pairs_from_experiments() -> list[dict]:
    """Experiment entries → forge + scoring pairs."""
    pairs: list[dict] = []
    for path in sorted(EXPERIMENTS_DIR.rglob("*.md")):
        text = path.read_text()
        fm, body = _frontmatter(text)
        candidate = fm.get("candidate", "")
        gap = fm.get("gap", "")
        verdict = fm.get("verdict", "")
        if not candidate:
            continue
        if gap:
            pairs.append({
                "instruction": "Forge a YOUSPEAK word for this gap. Score on 5 axes.",
                "input": f"Gap: {gap}",
                "output": f"Candidate: {candidate}. Verdict: {verdict}.",
            })
        score_section = _section(body, "Five-axis scoring") or _section(body, "Axis scoring")
        if score_section and candidate:
            pairs.append({
                "instruction": f"Score {candidate} on the 5-axis YOUSPEAK rubric.",
                "input": "",
                "output": " ".join(score_section.split())[:1500],
            })
    return pairs


def pairs_from_archaeology() -> list[dict]:
    """Archaeology entries → tongue/field etymology pairs."""
    pairs: list[dict] = []
    for path in sorted(ARCH_DIR.rglob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text()
        fm, body = _frontmatter(text)
        tongue = fm.get("tongue", path.parent.name)
        field = fm.get("semantic_field", "")
        if not field:
            continue
        donors_section = _section(body, "Donors available to YOUSPEAK") or \
                         _section(body, "Donors") or \
                         _section(body, "Native forms")
        if donors_section:
            pairs.append({
                "instruction": f"What donors does {tongue} offer for the '{field}' semantic field?",
                "input": "",
                "output": " ".join(donors_section.split())[:1500],
            })
    return pairs


def pairs_from_diplosemy() -> list[dict]:
    """Diplosemic exemplars → pair-reasoning pairs."""
    pairs: list[dict] = []
    for path in sorted(DIPLOSEMY_EXEMPLARS_DIR.rglob("*.md")):
        text = path.read_text()
        fm, body = _frontmatter(text)
        exemplar = fm.get("exemplar", path.stem)
        mechanism = fm.get("mechanism", "")
        pairs.append({
            "instruction": "Explain this YOUSPEAK diplosemic pair.",
            "input": exemplar,
            "output": f"Mechanism: {mechanism}. " + " ".join(body.split())[:1500],
        })
        if mechanism == "anastrophance" and " ↔ " in exemplar:
            word_a, word_b = [w.strip() for w in exemplar.split("↔")]
            pairs.append({
                "instruction": f"What is the Anastrophance-sibling of {word_a}?",
                "input": "",
                "output": word_b,
            })
            pairs.append({
                "instruction": f"What is the Anastrophance-sibling of {word_b}?",
                "input": "",
                "output": word_a,
            })
    return pairs


def synthesised_pairs() -> list[dict]:
    """Template-based synthesis for broader coverage."""
    pairs: list[dict] = []
    # Laws of Coinage
    laws = [
        ("What is the First Law of Coinage?",
         "No word without gap. A candidate that answers no gap is decoration."),
        ("What is the Second Law of Coinage?",
         "No gap without evidence. A gap must be shown, not asserted."),
        ("What is the Third Law of Coinage?",
         "No beauty without fit. Sound must carry sense."),
        ("What is the Fourth Law of Coinage?",
         "No survival without assessment. No word enters canon unjudged."),
        ("What is the Fifth Law of Coinage?",
         "No canon without genealogy. Every standing word traces its arrival path."),
    ]
    for q, a in laws:
        pairs.append({"instruction": q, "input": "", "output": a})

    # 5-axis rubric
    pairs.append({
        "instruction": "List the 5 axes of YOUSPEAK assessment and their weights.",
        "input": "",
        "output": "gap_validity (0.25), phonetic_weight (0.20), semantic_coverage (0.25), "
                  "cross_linguistic_uniqueness (0.15), memorability (0.15). "
                  "Canon threshold: weighted ≥7.5.",
    })
    pairs.append({
        "instruction": "What is the canon-threshold for a YOUSPEAK coinage?",
        "input": "",
        "output": "Weighted 5-axis total ≥ 7.5 out of 10.",
    })

    # Six mechanisms of diplosemy
    mechs = [
        ("anastrophance", "head-inversion; compound M1M2 vs M2M1 yield correlated sibling-words"),
        ("enkalyptance", "embedded-subword; coinage written form contains another complete word"),
        ("synaphemia",   "homophonic-shadow; coinage spoken form echoes an English phrase"),
        ("allomance",    "alternate-parse; compound admits two legitimate morpheme-parses"),
        ("parallaxance", "parallel-couplet; two parallel clauses create third depth-meaning"),
        ("hypostixance", "punctuation-path; sentence meaning shifts with punctuation"),
    ]
    for mech, desc in mechs:
        pairs.append({
            "instruction": f"Explain the {mech} diplosemic mechanism.",
            "input": "",
            "output": desc,
        })

    return pairs


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=str(SCRIPT_DIR / "data"),
                   help="output directory")
    p.add_argument("--split", type=float, default=0.1,
                   help="validation split ratio (default 0.1)")
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    all_pairs: list[dict] = []
    all_pairs.extend(pairs_from_canon())
    all_pairs.extend(pairs_from_experiments())
    all_pairs.extend(pairs_from_archaeology())
    all_pairs.extend(pairs_from_diplosemy())
    all_pairs.extend(synthesised_pairs())

    print(f"generated {len(all_pairs)} training pairs")

    random.seed(args.seed)
    random.shuffle(all_pairs)

    n_val = int(len(all_pairs) * args.split)
    valid = all_pairs[:n_val]
    train = all_pairs[n_val:]

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    train_path = out_dir / "train.jsonl"
    valid_path = out_dir / "valid.jsonl"

    with train_path.open("w") as f:
        for p in train:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    with valid_path.open("w") as f:
        for p in valid:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    print(f"wrote {train_path} ({len(train)} pairs)")
    print(f"wrote {valid_path} ({len(valid)} pairs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
