#!/usr/bin/env python3
"""YOUSPEAK translator — ANAKALYPSE operationalised.

Takes a word/phrase/concept in a source language, identifies the
conceptual BUNDLE the source word packages, and proposes YOUSPEAK
vocabulary that UNFOLDS the bundle into its distinct components.

This is the operational version of Constitution Foundation III: when
translating INTO YOUSPEAK, hidden layers of meaning should unfold into
clarity.

Under THE-REALM.md (2026-05-12) the operation has a precise structural
reading: ANAKALYPSE is un-collapsing of projection-lost dimensions.
When a source language projects the realm at an angle that bundles
four registers into one word (kimochi), the projection has collapsed
four dimensions into one. translate.py is the disciplined inverse of
that dimensional-reduction — it recovers the dimensions the source
occluded and proposes YOUSPEAK words for each.

Usage:
    python3 translate.py "kimochi" --from japanese
    python3 translate.py "logos" --from greek
    python3 translate.py "saudade" --from portuguese
    python3 translate.py --list-bundles            # show known bundle-mappings

The tool does NOT perform true automatic translation. It applies a
curated bundle-dictionary + YOUSPEAK canon lookup to produce an
unfolding-report. A human forger uses the report to decide what needs
coining next and what existing Canon-word covers which unfolded component.

Architecture:
  - bundles.json   — curated (word, source-language) -> list of
                     semantic-components and their possible YOUSPEAK
                     mappings (existing canon word or "unforged")
  - canon/**/*.md  — for matching unfolded-components to existing words
  - output         — an unfolding-report: the source word, its components,
                     and what YOUSPEAK offers for each (or flags as gap)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
YOUSPEAK_ROOT = SCRIPT_DIR.parent
BUNDLES_FILE = SCRIPT_DIR / "bundles.json"
CANON_DIR = YOUSPEAK_ROOT / "canon"


# ----------------------------------------------------------------------
# Bundle dictionary
# ----------------------------------------------------------------------

DEFAULT_BUNDLES = {
    "japanese": {
        "kimochi": {
            "gloss": "feeling / mood / atmosphere / intuitive-knowing — a single word packing a multi-component phenomenon",
            "unfold": [
                {"component": "feeling-state (affective register)", "youspeak": None, "gap": True},
                {"component": "atmospheric-sense (environmental register)", "youspeak": None, "gap": True},
                {"component": "intuitive-knowing (epistemic register)", "youspeak": None, "gap": True},
                {"component": "bodily-sensation component", "youspeak": None, "gap": True},
            ],
            "note": "Japanese bundles four registers English splits into four words and YOUSPEAK has not yet forged. Core Canon candidate-territory.",
        },
        "mono-no-aware": {
            "gloss": "the pathos of things — awareness that all passes; bittersweet-attention-to-transience",
            "unfold": [
                {"component": "awareness-of-passing (noticing-transience)", "youspeak": None, "gap": True},
                {"component": "aesthetic-tenderness-at-fading (not sadness; reverent-acceptance)", "youspeak": None, "gap": True},
                {"component": "transience-as-beauty (the passing IS what gives value)", "youspeak": None, "gap": True},
            ],
            "note": "Three distinct registers; YOUSPEAK might forge one word for each, or one compound for the full gestalt.",
        },
        "ma": {
            "gloss": "interval / pause / negative-space / gap-that-gives-meaning",
            "unfold": [
                {"component": "temporal-interval", "youspeak": None, "gap": True},
                {"component": "spatial-negative-space", "youspeak": None, "gap": True},
                {"component": "relational-pause (between people, creating depth)", "youspeak": None, "gap": True},
            ],
            "note": "ma distinguishes 3 kinds of meaningful-absence English conflates under 'space' or 'pause'.",
        },
        "mushin": {
            "gloss": "no-mind; the state of action without deliberative self-awareness",
            "unfold": [
                {"component": "action-without-self-monitoring", "youspeak": None, "gap": True},
                {"component": "the-effortlessness-phase of focused skill", "youspeak": "close to English 'flow'; YOUSPEAK-candidate for Core", "gap": True},
            ],
            "note": "mushin overlaps flow but is more specific about the self-awareness-dropping dimension.",
        },
    },
    "greek": {
        "logos": {
            "gloss": "word / reason / account / ratio / principle / discourse",
            "unfold": [
                {"component": "word (linguistic unit)", "youspeak": None, "gap": True},
                {"component": "reasoning (cognitive act)", "youspeak": None, "gap": True},
                {"component": "account/explanation (communicative form)", "youspeak": None, "gap": True},
                {"component": "ratio (mathematical relation)", "youspeak": None, "gap": True},
                {"component": "principle (ontological structure)", "youspeak": None, "gap": True},
                {"component": "Christ (theological usage)", "youspeak": None, "gap": False, "mapping": "specialised / theological"},
            ],
            "note": "logos bundles SIX distinct concepts English handles with six different words. YOUSPEAK should not force the bundle; it should unfold into grounded Core-Canon words for those senses where English lacks precision.",
        },
        "eros": {
            "gloss": "love as desiring-reaching (vs agape or philia)",
            "unfold": [
                {"component": "erotic-romantic desire", "youspeak": None, "gap": True},
                {"component": "intellectual reaching-toward-beauty (Platonic)", "youspeak": None, "gap": True},
                {"component": "creative drive / yearning", "youspeak": None, "gap": True},
            ],
            "note": "Modern English flattens to 'lust' or 'romance' but loses the Platonic-beauty-yearning sense.",
        },
    },
    "hebrew": {
        "shalom": {
            "gloss": "peace / wholeness / completeness / rightness-of-relation",
            "unfold": [
                {"component": "absence-of-conflict (the English 'peace')", "youspeak": None, "gap": False},
                {"component": "completeness (lacking-nothing)", "youspeak": None, "gap": True},
                {"component": "rightness-of-relation (relational-integrity)", "youspeak": None, "gap": True},
                {"component": "health (bodily flourishing)", "youspeak": None, "gap": False},
            ],
            "note": "shalom names FOUR dimensions English partially covers with 'peace, wholeness, wellbeing, integrity.' YOUSPEAK could add a single word for the relational-integrity component.",
        },
        "chesed": {
            "gloss": "loving-kindness / covenant-faithfulness / steadfast-love",
            "unfold": [
                {"component": "loving-kindness (the emotional register)", "youspeak": None, "gap": False},
                {"component": "covenant-faithfulness (the relational-commitment register)", "youspeak": None, "gap": True},
                {"component": "steadfast-continuance (the durational register)", "youspeak": None, "gap": True},
            ],
            "note": "chesed bundles emotional-kindness with relational-fidelity and temporal-persistence. English has 'loyalty' and 'kindness' separately.",
        },
    },
    "portuguese": {
        "saudade": {
            "gloss": "longing-for-what-is-absent-or-lost; bittersweet",
            "unfold": [
                {"component": "nostalgia for the past", "youspeak": None, "gap": False},
                {"component": "yearning for what-might-have-been", "youspeak": None, "gap": True},
                {"component": "the-sweetness-within-the-ache (positive-valence)", "youspeak": None, "gap": True},
            ],
            "note": "Distinctive from English nostalgia: saudade has a positive-valence, a quasi-enjoyable aspect to the ache. YOUSPEAK doxalgia is thematically adjacent but ache-of-presence; saudade is ache-of-absence.",
        },
    },
    "arabic": {
        "ukhuwwa": {
            "gloss": "brotherhood-strength; bond forged over time through shared hardship",
            "unfold": [
                {"component": "kinship-like closeness (family-scale warmth)", "youspeak": None, "gap": True},
                {"component": "forged-through-hardship (tempered-by-trial)", "youspeak": None, "gap": True},
                {"component": "non-romantic, non-hierarchical", "youspeak": None, "gap": True},
            ],
            "note": "Captures a specific friendship-quality English has no single word for. Candidate Core concept.",
        },
    },
    "chinese": {
        "mianzi": {
            "gloss": "face / social standing / public reputation / dignity",
            "unfold": [
                {"component": "public-reputation (how others perceive you)", "youspeak": None, "gap": False},
                {"component": "dignity-that-can-be-given-or-withheld-by-others", "youspeak": None, "gap": True},
                {"component": "reciprocal-social-obligation (maintaining others' face as well as one's own)", "youspeak": None, "gap": True},
            ],
            "note": "Chinese (and Japanese) bundle reputation with reciprocal-obligation. English 'face' loosely imports but without the reciprocity.",
        },
        "xiao": {
            "gloss": "filial piety / devotion to parents and ancestors",
            "unfold": [
                {"component": "respect for parents (hierarchical)", "youspeak": None, "gap": False},
                {"component": "active care-giving obligation", "youspeak": None, "gap": True},
                {"component": "honoring ancestors (trans-generational)", "youspeak": None, "gap": True},
            ],
            "note": "xiao structures three generations of obligation English handles ad-hoc.",
        },
    },
    "english": {
        # English bundles too — we audit ourselves
        "flow": {
            "gloss": "focused-attention state (Csikszentmihalyi); loss of self-consciousness",
            "unfold": [
                {"component": "effortlessness-phase", "youspeak": None, "gap": True},
                {"component": "loss-of-self-monitoring", "youspeak": None, "gap": True},
                {"component": "time-distortion", "youspeak": None, "gap": True},
                {"component": "competence-absorption (the specific joy of exercising trained skill)", "youspeak": None, "gap": True},
            ],
            "note": "'Flow' is a popular umbrella for several distinct phenomena. YOUSPEAK could unfold them.",
        },
        "presence": {
            "gloss": "being-here (vs being-physically-there-but-mentally-elsewhere)",
            "unfold": [
                {"component": "physical co-location", "youspeak": None, "gap": False},
                {"component": "attentive-here-ness (the Quaker 'centered')", "youspeak": None, "gap": True},
                {"component": "emotional-availability", "youspeak": None, "gap": True},
                {"component": "performer's charisma-quality", "youspeak": None, "gap": True},
            ],
            "note": "English 'presence' conflates four distinct phenomena.",
        },
    },
}


def _ensure_bundles() -> dict:
    """Load bundles.json if present; otherwise write the default and return."""
    if BUNDLES_FILE.exists():
        with BUNDLES_FILE.open() as f:
            return json.load(f)
    BUNDLES_FILE.write_text(json.dumps(DEFAULT_BUNDLES, indent=2, ensure_ascii=False))
    return DEFAULT_BUNDLES


def _canon_words() -> dict[str, str]:
    """Return {word -> one-line definition} across all tiers."""
    out: dict[str, str] = {}
    for md in CANON_DIR.rglob("*.md"):
        if md.name.startswith("README"):
            continue
        text = md.read_text()
        m = re.search(r"^word:\s*(\S+)", text, re.MULTILINE)
        if not m:
            continue
        word = m.group(1)
        # Definition = first paragraph after "## Definition"
        dm = re.search(r"^## Definition\s*\n\n(.+?)\n\n", text, re.MULTILINE | re.DOTALL)
        definition = dm.group(1).strip() if dm else ""
        out[word] = definition
    return out


# ----------------------------------------------------------------------
# Translation / unfolding
# ----------------------------------------------------------------------

def unfold(source_word: str, source_lang: str) -> dict:
    """Translate a source word into YOUSPEAK via unfolding its components."""
    bundles = _ensure_bundles()
    lang_bundles = bundles.get(source_lang.lower(), {})
    if source_word.lower() not in lang_bundles:
        return {
            "source_word": source_word,
            "source_lang": source_lang,
            "status": "not-in-bundle-dictionary",
            "suggestion": f"Add {source_word} to bundles.json under '{source_lang}' with its component unfolding. See the DEFAULT_BUNDLES in translate.py for schema.",
        }
    entry = lang_bundles[source_word.lower()]
    canon = _canon_words()
    # For each unfolded component, check if any canon word covers it
    components = entry.get("unfold", [])
    for c in components:
        # Heuristic: search canon definitions for keyword-overlap with the component description
        best_match = None
        if c.get("youspeak") is None and c.get("gap") is True:
            comp_text = c["component"].lower()
            comp_keywords = set(re.findall(r"[a-z]{4,}", comp_text))
            for word, defn in canon.items():
                def_kw = set(re.findall(r"[a-z]{4,}", defn.lower()))
                overlap = comp_keywords & def_kw
                if len(overlap) >= 2:
                    best_match = word
                    break
            if best_match:
                c["canon_hint"] = best_match
    return {
        "source_word": source_word,
        "source_lang": source_lang,
        "gloss": entry.get("gloss", ""),
        "components_unfolded": len(components),
        "components_with_gap": sum(1 for c in components if c.get("gap")),
        "components": components,
        "note": entry.get("note", ""),
    }


def render_report(result: dict) -> str:
    if result.get("status") == "not-in-bundle-dictionary":
        return (f"Not in bundle-dictionary: {result['source_word']} ({result['source_lang']})\n"
                f"  {result['suggestion']}")
    lines = [
        f"# Unfolding: {result['source_word']} ({result['source_lang']})",
        "",
        f"**Bundled gloss:** {result['gloss']}",
        "",
        f"**Components unfolded:** {result['components_unfolded']} "
        f"(of which {result['components_with_gap']} are YOUSPEAK gaps)",
        "",
        "## Components",
        "",
    ]
    for i, c in enumerate(result.get("components", []), 1):
        lines.append(f"{i}. **{c['component']}**")
        if c.get("youspeak"):
            lines.append(f"   - YOUSPEAK: `{c['youspeak']}`")
        elif c.get("canon_hint"):
            lines.append(f"   - Canon hint: `{c['canon_hint']}` (heuristic match; verify)")
        elif c.get("gap"):
            lines.append(f"   - **GAP** — unforged; Core Canon target")
        if c.get("mapping"):
            lines.append(f"   - mapping: {c['mapping']}")
        lines.append("")
    if result.get("note"):
        lines.append(f"_Note: {result['note']}_")
    return "\n".join(lines)


def list_bundles() -> str:
    bundles = _ensure_bundles()
    lines = ["# Known source-language bundles", ""]
    for lang, words in sorted(bundles.items()):
        lines.append(f"## {lang}")
        for w, e in sorted(words.items()):
            lines.append(f"- **{w}** — {e.get('gloss', '')[:80]}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("word", nargs="?")
    p.add_argument("--from", dest="src_lang", default="", help="source language")
    p.add_argument("--list-bundles", action="store_true", help="list known bundles")
    args = p.parse_args()

    if args.list_bundles:
        print(list_bundles())
        return 0

    if not args.word or not args.src_lang:
        p.print_help()
        return 2

    result = unfold(args.word, args.src_lang)
    print(render_report(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
