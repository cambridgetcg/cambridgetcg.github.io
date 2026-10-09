#!/usr/bin/env python3
"""YOUSPEAK Pipeline — forge.

Generates candidate coinages from a gap description and a donor list.
Produces morphological combinations (concatenation, suffix-swap, head-
modifier variants) and scores each candidate on mechanical phonetic
metrics (syllable count, vowel ratio, profile). Nuance then selects
candidates to promote to full experiment files.

Usage:
    python3 forge.py <morpheme1> <morpheme2> [<morpheme3> ...]
                                           generate candidate compounds
    python3 forge.py --from <experiment.md>
                                           read donors from an experiment file
                                           frontmatter and propose new compounds
"""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

# Reuse assess.py's mechanical metric functions.
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from assess import mechanical_metrics, parse_frontmatter, split_frontmatter  # noqa: E402


def _normalize(morpheme: str) -> str:
    """Strip language-prefix ('Greek:dokimazō' -> 'dokimazō') and normalize."""
    if ":" in morpheme:
        morpheme = morpheme.split(":", 1)[1]
    return morpheme.strip().lower()


def _trim_ending(word: str, endings=("os", "ē", "on", "es", "us", "ein", "um")) -> str:
    """Strip common Greek/Latin nominal endings when compounding."""
    for e in endings:
        if word.endswith(e) and len(word) > len(e) + 1:
            return word[:-len(e)]
    return word


def _smooth_joint(left: str, right: str) -> str:
    """Simple phonetic smoothing at the compound joint.

    - If left ends in consonant and right starts in consonant matching,
      elide one.
    - Add connective vowel 'o' if two consonants would collide harshly.
    """
    if not left or not right:
        return left + right
    if left[-1] == right[0]:
        return left + right[1:]
    # two-consonant collision: insert o
    vowels = set("aeiouyāēīōū")
    if left[-1] not in vowels and right[0] not in vowels and right[0] not in ("r", "l", "n"):
        return left + "o" + right
    return left + right


def generate_candidates(morphemes: list[str]) -> list[str]:
    """Produce candidate compounds.

    Strategies:
      1. Sequential compounding (m1 + m2 + m3 ...)
      2. Pairwise compounding (all ordered pairs)
      3. Reversed pairs
      4. With and without nominal-ending trim on all but the last element.
    """
    normalized = [_normalize(m) for m in morphemes]
    if len(normalized) < 2:
        return [normalized[0]] if normalized else []

    candidates: set[str] = set()

    # 1. Full sequence, trimmed
    trimmed = [_trim_ending(m) for m in normalized[:-1]] + [normalized[-1]]
    candidates.add("".join(trimmed))

    # Full sequence with phonetic smoothing
    seq = trimmed[0]
    for m in trimmed[1:]:
        seq = _smooth_joint(seq, m)
    candidates.add(seq)

    # 2. Pairwise in both orders
    for a, b in itertools.permutations(normalized, 2):
        a_trim = _trim_ending(a)
        candidates.add(a_trim + b)
        candidates.add(_smooth_joint(a_trim, b))

    return sorted(candidates, key=len)


def report_candidate(cand: str) -> dict:
    metrics = mechanical_metrics(cand)
    return {"candidate": cand, **metrics}


def cmd_generate(morphemes: list[str]) -> int:
    cands = generate_candidates(morphemes)
    if not cands:
        print("no candidates generated (need at least 2 morphemes)", file=sys.stderr)
        return 1
    print(f"=== candidates from donors: {morphemes} ===\n")
    print(f"{'candidate':24s} {'syl':>4s} {'vowel_ratio':>12s} profile")
    for c in cands:
        r = report_candidate(c)
        print(f"{r['candidate']:24s} {r['syllables']:>4d} {r['vowel_ratio']:>12.2f} {r['profile']}")
    return 0


def cmd_from_experiment(path: Path) -> int:
    """Extract donors from an experiment file and generate new combinations."""
    text = path.read_text()
    raw, _ = split_frontmatter(text)
    fm = parse_frontmatter(raw)
    donors_raw = fm.get("donors")
    donors: list[str]
    if isinstance(donors_raw, list):
        donors = donors_raw
    elif isinstance(donors_raw, str):
        donors = [d.strip() for d in donors_raw.strip("[]").split(",") if d.strip()]
    else:
        print(f"no donors in frontmatter of {path}", file=sys.stderr)
        return 1
    print(f"(donors from {path.name}):  {donors}\n")
    return cmd_generate(donors)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    if sys.argv[1] == "--from" and len(sys.argv) >= 3:
        return cmd_from_experiment(Path(sys.argv[2]))
    return cmd_generate(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
