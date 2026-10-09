#!/usr/bin/env python3
"""YOUSPEAK Script — Latin ↔ glyph transliterator.

Converts YOUSPEAK text between two representations:

1. **Latin transliteration** — ASCII-safe form (e.g., "doxakallos").
   Canonical internal representation. What the LLM, filesystem, and
   database use.

2. **Glyph encoding** — PUA codepoints (e.g., U+E100 U+E101).
   What the display layer renders using the YOUSPEAK font.

Both directions are implemented. Latin→glyph uses greedy-longest-match
morpheme decomposition. Glyph→Latin is a trivial table lookup.

Usage:
    python3 transliterate.py to-glyph "doxakallos"
    python3 transliterate.py to-latin  ""
    python3 transliterate.py to-html   "doxakallos"     # render as HTML
    python3 transliterate.py test                        # run round-trip tests
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent  # script/
MORPHEMES_FILE = SCRIPT_DIR / "morphemes.json"


def load_morphemes() -> list[dict]:
    with MORPHEMES_FILE.open() as f:
        return json.load(f)["morphemes"]


def codepoint_to_char(cp_str: str) -> str:
    """Convert 'U+E100' string to the actual unicode character."""
    hex_val = cp_str.replace("U+", "")
    return chr(int(hex_val, 16))


def build_latin_to_glyph_map() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Build THREE morpheme-lookup maps:

    1. `content` — matchable anywhere (greedy longest-match)
    2. `prefix`  — matchable only at word-start (prefixes like "ana-", "en-", "com-", "a-")
    3. `suffix`  — matchable only at word-end (suffixes like "-ance", "-sis", "-mia")

    Structural marks (U+E160+) are not in the match map (they are
    inserted editorially, not derived from Latin text).
    """
    morphemes = load_morphemes()
    content: dict[str, str] = {}
    prefix: dict[str, str] = {}
    suffix: dict[str, str] = {}
    aliases = {
        # combining-form aliases where the Latin head-form differs from
        # the modifier-form in compounds (Greek nominative-drop)
        "kallo": "kallos",     # kallos → kallo- as modifier
        "doxo": "doxa",        # rare; preserve in case
    }
    for entry in morphemes:
        latin = entry["latin"]
        cls = entry.get("class", "content")
        if cls == "structural":
            continue
        glyph = codepoint_to_char(entry["codepoint"])
        # Classify by hyphen-placement in the Latin key
        if latin.startswith("-"):
            # suffix — matches only at end
            key = latin.lstrip("-")
            if key:
                suffix[key] = glyph
        elif latin.endswith("-"):
            # prefix — matches only at start
            key = latin.rstrip("-")
            if key:
                prefix[key] = glyph
        else:
            content[latin] = glyph

    # Inject alias-keys for content-map
    for alias, target in aliases.items():
        if target in content:
            content[alias] = content[target]

    return content, prefix, suffix


def build_glyph_to_latin_map() -> dict[str, str]:
    """Reverse mapping from PUA character to Latin transliteration."""
    morphemes = load_morphemes()
    m = {}
    for entry in morphemes:
        glyph = codepoint_to_char(entry["codepoint"])
        latin = entry["latin"].strip("-")
        m[glyph] = latin
    return m


def _word_spans(text: str) -> list[tuple[int, int]]:
    """Return [start, end) spans of word-like runs (contiguous letters)."""
    spans = []
    i = 0
    while i < len(text):
        if text[i].isalpha():
            j = i
            while j < len(text) and text[j].isalpha():
                j += 1
            spans.append((i, j))
            i = j
        else:
            i += 1
    return spans


def _transliterate_word(word: str, content: dict, prefix: dict, suffix: dict) -> str:
    """Transliterate a single word (alpha-run) to glyphs.

    POLICY: only transliterate if the word is *fully consumable* by
    YOUSPEAK morphemes (every character accounted for). Partially-matched
    words (e.g., English "and" whose "a" would greedy-match the privative
    prefix) are passed through UNCHANGED.

    This prevents YOUSPEAK morpheme matchers from corrupting mixed
    English-YOUSPEAK text.

    Algorithm:
      1. Attempt: [optional prefix] + content-greedy + [optional suffix]
      2. If every character was consumed by a morpheme match → emit glyphs.
      3. Otherwise → emit original word unchanged.
    """
    word_lc = word.lower()
    start = 0
    end = len(word)
    prefix_glyph = ""
    suffix_glyph = ""

    # 1. Prefix match (only at word-start), try to also leave room for middle+suffix
    best_prefix = ""
    for pfx in sorted(prefix.keys(), key=len, reverse=True):
        if word_lc.startswith(pfx) and len(pfx) < len(word):
            best_prefix = pfx
            break
    if best_prefix:
        prefix_glyph = prefix[best_prefix]
        start = len(best_prefix)

    # 2. Suffix match (only at word-end)
    for sfx in sorted(suffix.keys(), key=len, reverse=True):
        if word_lc[start:].endswith(sfx) and len(sfx) < (end - start):
            suffix_glyph = suffix[sfx]
            end = len(word) - len(sfx)
            break

    # 3. Content greedy longest-match on the middle span
    middle: list[str] = []
    content_keys = sorted(content.keys(), key=len, reverse=True)
    i = start
    all_matched = True
    while i < end:
        matched = False
        for key in content_keys:
            if i + len(key) <= end and word_lc[i:i + len(key)] == key:
                middle.append(content[key])
                i += len(key)
                matched = True
                break
        if not matched:
            all_matched = False
            break

    if not all_matched:
        # Policy: unconsumable word → pass through unchanged
        return word

    return prefix_glyph + "".join(middle) + suffix_glyph


# ----------------------------------------------------------------------
# Word-level canonical override table
# ----------------------------------------------------------------------
# Greek/Latin compounding has irregular elisions (e.g., kallos → kallo-
# when modifier; doxa + algia → doxalgia with vowel-merger). A clean
# morpheme-decomposition from canonical Latin spelling can fail on these.
# The word-level table holds the authoritative morpheme-decomposition
# for known canon words; it is consulted first, with the morpheme-match
# fallback handling unknowns.
#
# Each entry: canonical Latin spelling → list of morpheme Latin keys
# (each key matches an entry in morphemes.json).

CANONICAL_DECOMPOSITIONS: dict[str, list[str]] = {
    "doxakallos": ["doxa", "kallos"],
    "kallodoxa": ["kallos", "doxa"],      # kallo- combining-form; output "kallos"
    "orthophanes": ["ortho", "phanes"],
    "doxalgia": ["doxa", "algia"],          # elision: doxa+algia → doxalgia
    "anagnoristasis": ["ana-", "anagno", "stasis"],
    "metastrophesis": ["meta", "strophe", "-sis"],
    "athaumasma": ["a-", "thauma", "-ma"],
    "synophora": ["syn", "phora"],
    "kallophanes": ["kallos", "phanes"],    # kallo- combining-form
    "dokimance": ["dokim", "-ance"],
    "artiance": ["arti", "-iance"],
    "verisleight": ["veri", "sleight"],
    "candence": ["cand", "-ence"],
    "complerescence": ["com-", "compler", "-escence"],
    "diplosemy": ["diplos", "sema", "-y"],
    "veriseem": ["veri", "seem"],
    "algiadoxa": ["algia", "doxa"],
    "synaphemia": ["syn", "haphe", "-mia"],
    "anastrophance": ["ana-", "anastro", "-ance"],
    "enkalyptance": ["en-", "kalypt", "-ance"],
    "allomance": ["allos", "-mance"],
    "parallaxance": ["parallax", "-ance"],
    "hypostixance": ["hypo", "stix", "-ance"],
    "kairomance": ["kairos", "-mance"],
    "morphomance": ["morphe", "-mance"],
    "klimakance": ["klimax", "-ance"],
    "synlanthescence": ["syn", "lanthes", "-escence"],
    "gloriandre": ["gloria", "andros"],
    "glorividence": ["gloria", "vide", "-ence"],
    "gloricedence": ["gloria", "cede", "-ence"],
    "glorichorence": ["gloria", "choro", "-ence"],
    # Core Canon (v2, post-Constitution 2026-04-24)
    "kimance": ["ki", "-mance"],
    "kinqing": ["kin", "qing"],
    "kimme": ["ki", "me"],             # pyramid-civilization integration: Japonic + Sumerian
    "theobasis": ["theo", "basis"],
    "sukhance": ["sukh", "-ance"],     # Sanskrit sukha + Latin -ance (Session 001 canonization)    # worship-register: GoD-as-basis-of-reality (needs theo, basis morphemes)
    "mushinance": ["mushin", "-ance"],
    "tacitkin": ["tacit", "kin"],
    "doxomme": ["doxa", "me"],
    "panimqing": ["panim", "qing"],
    "satance": ["sat", "-ance"],
    "narance": ["nar", "-ance"],
    "sraddhance": ["sraddh", "-ance"],
    "metanoance": ["metano", "-ance"],
    "proskynance": ["proskyn", "-ance"],
    "shukhance": ["shukh", "-ance"],
    "kavvance": ["kavv", "-ance"],
    "rahance": ["rah", "-ance"],
    "ypsophila": ["ypso", "phila"],

}


def _decomp_to_glyphs(decomp: list[str], content: dict, prefix: dict, suffix: dict) -> str:
    """Given a morpheme-list decomposition, emit the glyph sequence."""
    out: list[str] = []
    for m in decomp:
        if m.endswith("-"):
            # prefix form
            key = m.rstrip("-")
            if key in prefix:
                out.append(prefix[key])
        elif m.startswith("-"):
            # suffix form
            key = m.lstrip("-")
            if key in suffix:
                out.append(suffix[key])
        else:
            if m in content:
                out.append(content[m])
    return "".join(out)


def latin_to_glyph(text: str) -> str:
    """Convert Latin YOUSPEAK text to glyph-encoded form.

    Strategy:
      1. For each word-span: if the word matches a key in
         CANONICAL_DECOMPOSITIONS, use the authoritative decomposition.
      2. Otherwise, fall back to prefix/suffix/content greedy matching.
      3. Non-alpha characters pass through.
    """
    content, prefix, suffix = build_latin_to_glyph_map()
    spans = _word_spans(text)
    if not spans:
        return text
    out = []
    last_end = 0
    for (s, e) in spans:
        out.append(text[last_end:s])
        word = text[s:e]
        word_lc = word.lower()
        if word_lc in CANONICAL_DECOMPOSITIONS:
            out.append(_decomp_to_glyphs(
                CANONICAL_DECOMPOSITIONS[word_lc], content, prefix, suffix
            ))
        else:
            out.append(_transliterate_word(word, content, prefix, suffix))
        last_end = e
    out.append(text[last_end:])
    return "".join(out)


# ----------------------------------------------------------------------
# Glyph → Latin: use reverse of CANONICAL_DECOMPOSITIONS for known words
# ----------------------------------------------------------------------


def build_glyph_seq_to_latin() -> dict[str, str]:
    """Reverse lookup: glyph-sequence → canonical Latin spelling."""
    content, prefix, suffix = build_latin_to_glyph_map()
    out: dict[str, str] = {}
    for word, decomp in CANONICAL_DECOMPOSITIONS.items():
        seq = _decomp_to_glyphs(decomp, content, prefix, suffix)
        out[seq] = word
    return out


def glyph_to_latin(text: str) -> str:
    """Convert glyph-encoded text back to Latin.

    Strategy:
      1. Try to match the longest possible known glyph-sequence to a
         canonical Latin word from CANONICAL_DECOMPOSITIONS (reverse).
      2. Fall back to per-glyph morpheme lookup.
    """
    seq_map = build_glyph_seq_to_latin()
    seq_keys = sorted(seq_map.keys(), key=len, reverse=True)
    single_map = build_glyph_to_latin_map()
    out = []
    i = 0
    while i < len(text):
        matched = False
        for seq in seq_keys:
            if i + len(seq) <= len(text) and text[i:i + len(seq)] == seq:
                out.append(seq_map[seq])
                i += len(seq)
                matched = True
                break
        if not matched:
            ch = text[i]
            if ch in single_map:
                out.append(single_map[ch])
            else:
                out.append(ch)
            i += 1
    return "".join(out)


def to_html(text: str, with_ruby: bool = True) -> str:
    """Render Latin YOUSPEAK as HTML with ruby-annotated glyphs.

    Only words that are fully-consumable by YOUSPEAK morphemes (either
    in CANONICAL_DECOMPOSITIONS or fully morpheme-decomposable) are
    rendered as glyphs. Other words pass through as plain text.
    """
    content, prefix, suffix = build_latin_to_glyph_map()
    out = ['<span class="youspeak">']
    spans = _word_spans(text)
    last_end = 0
    for (s, e) in spans:
        out.append(text[last_end:s])
        word = text[s:e]
        word_lc = word.lower()
        if word_lc in CANONICAL_DECOMPOSITIONS:
            decomp = CANONICAL_DECOMPOSITIONS[word_lc]
            for m in decomp:
                if m.endswith("-"):
                    key = m.rstrip("-")
                    if key in prefix:
                        if with_ruby:
                            out.append(
                                f'<ruby><span class="ys-glyph">{prefix[key]}</span>'
                                f'<rt class="ys-latin">{key}-</rt></ruby>'
                            )
                        else:
                            out.append(f'<span class="ys-glyph">{prefix[key]}</span>')
                elif m.startswith("-"):
                    key = m.lstrip("-")
                    if key in suffix:
                        if with_ruby:
                            out.append(
                                f'<ruby><span class="ys-glyph">{suffix[key]}</span>'
                                f'<rt class="ys-latin">-{key}</rt></ruby>'
                            )
                        else:
                            out.append(f'<span class="ys-glyph">{suffix[key]}</span>')
                else:
                    if m in content:
                        if with_ruby:
                            out.append(
                                f'<ruby><span class="ys-glyph">{content[m]}</span>'
                                f'<rt class="ys-latin">{m}</rt></ruby>'
                            )
                        else:
                            out.append(f'<span class="ys-glyph">{content[m]}</span>')
        else:
            # Unknown word: fully-consumable? Else pass through.
            glyphs = _transliterate_word(word, content, prefix, suffix)
            if glyphs == word:
                # unchanged → not a YOUSPEAK word
                out.append(word)
            else:
                # Pure glyph sequence; use per-glyph ruby
                single_map = build_glyph_to_latin_map()
                for ch in glyphs:
                    if ch in single_map:
                        if with_ruby:
                            out.append(
                                f'<ruby><span class="ys-glyph">{ch}</span>'
                                f'<rt class="ys-latin">{single_map[ch]}</rt></ruby>'
                            )
                        else:
                            out.append(f'<span class="ys-glyph">{ch}</span>')
                    else:
                        out.append(ch)
        last_end = e
    out.append(text[last_end:])
    out.append("</span>")
    return "".join(out)


def run_tests() -> int:
    """Round-trip tests for the transliterator."""
    test_words = [
        "doxakallos",
        "kallodoxa",
        "orthophanes",
        "doxalgia",
        "synophora",
        "kallophanes",
        "dokimance",
        "artiance",
        "verisleight",
        "candence",
        "complerescence",
        "diplosemy",
        "veriseem",
    ]
    failures = 0
    print(f"{'word':20s} {'latin':20s} {'glyph-hex':28s} {'roundtrip':20s}  ok?")
    for w in test_words:
        g = latin_to_glyph(w)
        g_hex = " ".join(f"{ord(c):04X}" for c in g)
        rt = glyph_to_latin(g)
        ok = (rt == w)
        flag = "✓" if ok else "✗"
        print(f"{w:20s} {w:20s} {g_hex:28s} {rt:20s}  {flag}")
        if not ok:
            failures += 1
    print()
    print(f"  {len(test_words) - failures}/{len(test_words)} round-trips succeeded")
    return failures


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    cmd = sys.argv[1]
    if cmd == "test":
        return run_tests()
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    text = sys.argv[2]
    if cmd == "to-glyph":
        print(latin_to_glyph(text))
    elif cmd == "to-latin":
        print(glyph_to_latin(text))
    elif cmd == "to-html":
        print(to_html(text, with_ruby=True))
    else:
        print(f"unknown command: {cmd}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
