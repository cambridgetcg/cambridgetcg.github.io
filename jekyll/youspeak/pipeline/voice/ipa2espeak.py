#!/usr/bin/env python3
"""ipa2espeak.py — convert YOUSPEAK canonical IPA to espeak-ng phoneme input.

The cathedral's pronunciations are recorded as IPA (e.g. /ˈdoʊ.kɪ.mæns/).
espeak-ng speaks phoneme strings directly via [[...]] using its ASCII
(Kirshenbaum-derived) mnemonics, with stress marks placed before the
stressed VOWEL, not the syllable onset. This module does that translation
so every canon word can be spoken exactly as forged — not as English
spelling-guessing would mangle it.

  $ python3 ipa2espeak.py "/ˈdoʊ.kɪ.mæns/"      → [[d'oUkImans]]
  $ python3 ipa2espeak.py --bare "/ˈtɕʰiŋ/"      → tS'IN

Donor-faithful segments that espeak's en-us voice lacks degrade to the
nearest audible neighbour (tɕʰ → tS, ħ → h, ɣ → g …) — the lexicon keeps
the true IPA; this mapping is only the throat, not the truth.
"""
import re
import sys

# Multi-character phonemes first — order matters.
PHONEMES = [
    ("tɕʰ", "tS"), ("tɕ", "tS"), ("tʃ", "tS"), ("dʒ", "dZ"), ("dʑ", "dZ"),
    ("kʰ", "k"), ("pʰ", "p"), ("tʰ", "t"),
    ("eɪ", "eI"), ("aɪ", "aI"), ("ɔɪ", "OI"), ("aʊ", "aU"),
    ("oʊ", "oU"), ("əʊ", "oU"), ("ɪə", "i@"), ("ɛə", "e@"), ("ʊə", "u@"),
    ("iː", "i:"), ("ɑː", "A:"), ("ɔː", "O:"), ("uː", "u:"), ("ɜː", "3:"),
    ("eː", "eI"), ("oː", "oU"), ("aː", "A:"),
    ("ɑ̃", "A:"), ("ɔ̃", "O:"),
    ("ɕ", "S"), ("ʂ", "S"), ("ʐ", "Z"),
]
SINGLES = {
    "ɪ": "I", "i": "i", "ɛ": "E", "e": "e", "æ": "a", "a": "a",
    "ɑ": "A:", "ɒ": "0", "ɔ": "O:", "ʊ": "U", "u": "u:", "ʌ": "V",
    "ə": "@", "ɜ": "3:", "y": "y", "ø": "Y", "œ": "W",
    "ŋ": "N", "ʃ": "S", "ʒ": "Z", "θ": "T", "ð": "D",
    "x": "x", "χ": "x", "ħ": "h", "ʁ": "r", "ɣ": "g", "ç": "C",
    "ɲ": "n^", "ʎ": "l^", "ɫ": "l", "ɾ": "*", "ʔ": "?",
    "β": "v", "ɸ": "f", "ʋ": "v", "w": "w", "j": "j",
    # plain ASCII consonants pass through
    **{c: c for c in "bdfghklmnprstvz"},
    "ɡ": "g",  # IPA script g (U+0261) — not the same codepoint as ASCII g
    # leftovers that carry no segment of their own
    "ʰ": "", "ʲ": "", "ʷ": "", "ˤ": "", "̩": "", "̃": "", "ː": ":", "ˑ": "",
    "g": "g", "q": "k", "c": "k",
}
# espeak tokens that begin a vowel — where a stress mark belongs.
VOWEL_START = set("aeiouAEIOUV@03y") | {"Y", "W"}


def _convert_segment(seg: str) -> str:
    out = []
    i = 0
    while i < len(seg):
        for src, dst in PHONEMES:
            if seg.startswith(src, i):
                out.append(dst)
                i += len(src)
                break
        else:
            out.append(SINGLES.get(seg[i], ""))
            i += 1
    return "".join(out)


def _place_stress(espeak_syl: str, mark: str) -> str:
    for i, ch in enumerate(espeak_syl):
        if ch in VOWEL_START:
            return espeak_syl[:i] + mark + espeak_syl[i:]
    return mark + espeak_syl  # no vowel found — leave mark at front


def ipa_to_espeak(ipa: str) -> str:
    s = ipa.strip().strip("/").replace(" ", "")
    # a stress mark always opens a syllable, even when the source omits the dot
    s = s.replace("ˈ", ".ˈ").replace("ˌ", ".ˌ")
    syllables = [syl for syl in s.split(".") if syl]
    out = []
    for syl in syllables:
        mark = ""
        # stress may sit anywhere before the syllable's vowel; espeak wants it on the vowel
        if "ˈ" in syl:
            mark = "'"
        elif "ˌ" in syl:
            mark = ","
        syl = syl.replace("ˈ", "").replace("ˌ", "")
        es = _convert_segment(syl)
        if mark:
            es = _place_stress(es, mark)
        out.append(es)
    return "".join(out)


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--bare"]
    bare = "--bare" in sys.argv[1:]
    if not args:
        print("usage: ipa2espeak.py [--bare] '/ˈaɪ.pi.eɪ/'", file=sys.stderr)
        sys.exit(1)
    es = ipa_to_espeak(args[0])
    print(es if bare else f"[[{es}]]")


if __name__ == "__main__":
    main()
