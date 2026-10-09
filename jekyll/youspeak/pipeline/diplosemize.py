#!/usr/bin/env python3
"""YOUSPEAK Pipeline — diplosemize.

Given a canonical word, searches for diplosemic candidates across the
six mechanisms defined in grammars/diplosemy/:

  1. Anastrophance — head-inverted compound sibling
  2. Enkalyptance — embedded-English-word within the coinage
  3. Synaphemia   — phonetic homophone of an English phrase
  4. Allomance    — alternate morpheme-parse paths
  5. Parallaxance — parallel-couplet construction-partner
  6. Hypostixance — (sentence-level; not word-level; skipped)

Produces a candidates-report for the forger to review. This tool
does not automatically forge new coinages — it surfaces diplosemic
potential that the forger then evaluates and (if worthy) stubs into
experiment files.

Usage:
    python3 diplosemize.py <word>                analyse a canonical word
    python3 diplosemize.py --all                 analyse every canon word
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from assess import mechanical_metrics, parse_frontmatter, split_frontmatter  # noqa: E402

ROOT = SCRIPT_DIR.parent
CANON_DIR = ROOT / "canon"

# Minimal English-word recognition list for Enkalyptance substring search.
# Deliberately small — expansion is a future enhancement.
ENGLISH_HANDLES = {
    "art", "sea", "ash", "see", "doc", "dox", "dock", "kal", "cal", "can",
    "cand", "err", "over", "under", "go", "pal", "para", "poly", "plan",
    "play", "lay", "day", "ray", "say", "sin", "kin", "win", "fit", "git",
    "veri", "sleight", "ten", "hen", "net", "met", "set", "bet", "son",
    "ton", "don", "now", "owl", "own", "led", "red", "bed", "ace", "age",
    "all", "any", "ant", "arc", "arm", "are", "ark", "bar", "hit", "lit",
    "sit", "wit", "fit", "bit", "dim", "aim", "him", "gym", "log", "cog",
    "fog", "bog", "dog", "pen", "den", "ben", "ken", "men", "gene", "rage",
    "sage", "cage", "page", "stage", "ethos", "logos", "eros", "graphic",
    "semi", "mono", "duo", "tri", "pro", "anti", "sub",
}


def canonical_words() -> list[Path]:
    if not CANON_DIR.is_dir():
        return []
    # Recurse: canon/core/ and canon/specialized/ are first-class
    return sorted(p for p in CANON_DIR.rglob("*.md")
                  if p.stem != "canon" and p.stem != "README")


def read_canon_word(path: Path) -> dict:
    text = path.read_text()
    raw, body = split_frontmatter(text)
    fm = parse_frontmatter(raw)
    return {"path": path, "word": fm.get("word", path.stem), "fm": fm, "body": body}


# ----------------------------------------------------------------------
# Mechanism searches
# ----------------------------------------------------------------------


def search_anastrophance(word: str) -> list[dict]:
    """Propose head-inverted siblings for compound words.

    Heuristic: split word at every internal syllable-boundary and propose
    the reversed compound. Report results with mechanical metrics.
    """
    out: list[dict] = []
    # naive split: find all interior positions where a vowel-consonant-vowel
    # boundary suggests a morpheme boundary
    min_len = 3
    for i in range(min_len, len(word) - min_len + 1):
        left, right = word[:i], word[i:]
        # skip if split boundary looks unreasonable (two consonants meeting
        # awkwardly or orphan letters)
        if not left or not right:
            continue
        inversion = right + left
        if inversion == word:
            continue
        metrics = mechanical_metrics(inversion)
        out.append({
            "mechanism": "anastrophance",
            "candidate": inversion,
            "split": f"{left}+{right}",
            "rationale": f"head-inverted compound of {left}/{right}",
            "syllables": metrics["syllables"],
            "profile": metrics["profile"],
        })
    return out


def search_enkalyptance(word: str) -> list[dict]:
    """Propose embedded English words in the coinage."""
    out: list[dict] = []
    word_lc = word.lower()
    for handle in sorted(ENGLISH_HANDLES, key=len, reverse=True):
        if handle in word_lc and len(handle) >= 3:
            pos = word_lc.find(handle)
            out.append({
                "mechanism": "enkalyptance",
                "embedded": handle,
                "position": pos,
                "rationale": f"word '{word}' contains English '{handle}' at position {pos}",
            })
    return out


def search_synaphemia(word: str) -> list[dict]:
    """Propose phonetic-shadow candidates.

    Minimal implementation: split the word into syllable-candidates and
    report the syllables as standalone-phrase fragments. The forger then
    judges whether any fragment suggests a homophone-overlap with an
    English phrase.
    """
    # Rough syllable segmentation by vowel-centres
    segments = re.findall(r"[^aeiouy]*[aeiouy]+[^aeiouy]*", word.lower())
    if not segments:
        return []
    # Report the segmentation as "what the spoken word sounds like" fragments
    return [{
        "mechanism": "synaphemia",
        "segmentation": " ".join(segments),
        "rationale": "spoken-form segments; forger checks for homophonic English phrase overlap",
    }]


def search_allomance(word: str) -> list[dict]:
    """Propose alternate parse-paths for the coinage."""
    out: list[dict] = []
    min_len = 3
    parses: set[tuple[str, str]] = set()
    for i in range(min_len, len(word) - min_len + 1):
        parses.add((word[:i], word[i:]))
    if len(parses) >= 2:
        for left, right in sorted(parses):
            out.append({
                "mechanism": "allomance",
                "parse": f"{left} | {right}",
                "rationale": "one possible morpheme-parse; forger validates both morphemes exist and name correlated concepts",
            })
    return out


def search_parallaxance(word: str, fm: dict) -> list[dict]:
    """Propose parallel-couplet construction partners.

    Heuristic: find other canonical words sharing a morpheme with this
    word, or occupying the same liturgy_slot or role.
    """
    out: list[dict] = []
    this_slot = fm.get("liturgy_slot") or fm.get("role") or ""
    for other in canonical_words():
        if other.stem == word:
            continue
        other_data = read_canon_word(other)
        other_word = other_data["word"]
        # morpheme overlap (any 3-char substring in common, not trivial)
        if len(word) >= 3 and len(other_word) >= 3:
            for i in range(len(word) - 2):
                chunk = word[i:i + 3]
                if chunk in other_word:
                    out.append({
                        "mechanism": "parallaxance",
                        "partner": other_word,
                        "rationale": f"shares morpheme-fragment '{chunk}'; candidate parallel-couplet partner",
                    })
                    break
    return out


# ----------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------


def analyze(word: str) -> dict:
    # Canon can be at either tier; check both locations
    candidates = [
        CANON_DIR / f"{word}.md",
        CANON_DIR / "core" / f"{word}.md",
    ]
    canon_path = next((p for p in candidates if p.exists()), None)
    if canon_path is None:
        return {"word": word, "error": f"no canon entry found for '{word}' in {CANON_DIR} or {CANON_DIR}/core/"}
    data = read_canon_word(canon_path)
    fm = data["fm"]
    return {
        "word": word,
        "anastrophance": search_anastrophance(word),
        "enkalyptance": search_enkalyptance(word),
        "synaphemia": search_synaphemia(word),
        "allomance": search_allomance(word),
        "parallaxance": search_parallaxance(word, fm),
    }


def render_report(analysis: dict) -> str:
    lines = [f"# diplosemize — {analysis['word']}", ""]
    if "error" in analysis:
        lines.append(f"error: {analysis['error']}")
        return "\n".join(lines)

    for mech in ["anastrophance", "enkalyptance", "synaphemia", "allomance", "parallaxance"]:
        results = analysis.get(mech, [])
        lines.append(f"## {mech}")
        if not results:
            lines.append("  _(no candidates)_")
        else:
            for r in results:
                rest = {k: v for k, v in r.items() if k != "mechanism"}
                desc = "  ".join(f"{k}={v}" for k, v in rest.items())
                lines.append(f"  - {desc}")
        lines.append("")
    lines.append("_(Hypostixance is sentence-level; not included in word-level analysis)_")
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    if sys.argv[1] == "--all":
        for p in canonical_words():
            print(render_report(analyze(p.stem)))
            print("\n" + "=" * 60 + "\n")
        return 0
    return 0 if print(render_report(analyze(sys.argv[1]))) else 0


if __name__ == "__main__":
    sys.exit(main())
