---
organ: script
role: YOUSPEAK's fifth organ — the writing system
opened: 2026-04-24
opened_by: Yu's invocation to engineer the foundational character for building the language
status: foundation layer (morpheme inventory + PUA codepoints + transliterator + espanso input) in this session; font + IME + LLM fine-tune deferred
---

# Script — the Writing System Organ

_Where YOUSPEAK's words acquire visible form. A compositional-logographic script in which each glyph represents one canonical morpheme, words are composed linearly, and the Latin transliteration remains the canonical internal-representation for machines while glyphs serve human readers._

---

## The five organs, positioned

1. **archaeology/** — where semantic fields are exhumed from dead tongues
2. **labs/logos/experiments/** — where candidates are forged and scored
3. **pipeline/** — the tooling-nervous-system
4. **grammars/** — where structural operations are named (diplosemy chapter complete)
5. **script/** — where YOUSPEAK acquires its visible form (this chapter)

## The design axioms

1. **Logographic over phonemic.** Each glyph represents one morpheme, not one sound. This matches YOUSPEAK's compound-heavy grammar and enables semantic density.

2. **Compositional.** Words are sequences of morpheme-glyphs. No atomic glyphs for full words; the glyph for *doxakallos* is `<doxa-glyph><kallos-glyph>`.

3. **Linear left-to-right.** For interoperability. No 2D stacking.

4. **Latin-transliteration is the internal representation.** LLMs, databases, filesystems, APIs all work in Latin. Glyphs are purely a **display layer** — a visual affordance for human readers when a font is present.

5. **Unicode PUA encoding.** U+E100–E1FF reserved. Extensible to U+E200+ as the morpheme inventory grows.

6. **Graceful fallback.** When the font is missing, Latin-transliteration renders. The script never blocks meaning.

## The stack

| Layer | Artifact | Location |
|---|---|---|
| 1. Morpheme inventory | `script/morphemes.json` — canonical list of morphemes, their Latin-transliteration, PUA codepoint, etymology | here |
| 2. Encoding table | `script/codepoints.md` — PUA assignments (U+E100–E1FF) | here |
| 3. Glyph designs | `script/glyphs/*.md` — design-notes per morpheme; iconographic rationale; ASCII sketches | here |
| 4. Transliterator | `script/tools/transliterate.py` — Latin ↔ glyphs conversion | here |
| 5. Input method | `script/keyboard/espanso.yml` — text-expander rules for typing on standard keyboards | here |
| 6. Font | `script/fonts/youspeak.otf` — not built in this session; requires font editor | deferred |
| 7. LLM primer | `script/llm/primer.md` — how to prompt an LLM for YOUSPEAK fluency; RAG setup path | here |

## What exists after this session

- **[Morpheme inventory](morphemes.json)** — 40+ canonical morphemes with codepoints
- **[Codepoint table](codepoints.md)** — PUA assignments documented
- **[Transliterator](tools/transliterate.py)** — Latin ↔ PUA-encoded glyphs conversion (usable today if a YOUSPEAK font exists; also produces display-ready HTML)
- **[Espanso input config](keyboard/espanso.yml)** — text-expansion rules: type `:doxa` → glyph. Cross-platform (macOS/Windows/Linux).
- **[LLM primer](llm/primer.md)** — instruction-template for any LLM to read/write YOUSPEAK correctly (using Latin-transliteration; glyph-handling is a separate concern addressed by the display layer)
- **[Glyph design notes](glyphs/)** — one note per core morpheme: what the glyph represents, its iconographic rationale, an ASCII sketch. Actual font-file construction deferred.

## What remains deferred

- **The actual font file.** Requires FontForge, Glyphs, or equivalent font editor. Design notes exist; vectorization is the next step.
- **Proper IME integration** — macOS Input Source bundle, Windows IME DLL, Linux IBus/fcitx engine. Espanso suffices for v1.
- **LLM fine-tuning** — requires corpus (not yet large enough) and training infrastructure. Prompt-engineering and RAG cover the near-term.
- **Unicode Consortium proposal** — a multi-year path requiring script-documentation substantially more complete than what exists. PUA is sufficient for private and institutional use.

## Why this foundation matters

The writing system is not decoration. It is the bridge between YOUSPEAK's semantic architecture (morphemes, canonical words, diplosemy) and human perception. Without a script, YOUSPEAK is a spoken-and-transliterated tradition — legitimate but limited. With a script, YOUSPEAK becomes a full textual-visual language: its compounds are visible-at-glance, its morphology is read-at-glyph-boundaries, its diplosemy (especially Enkalyptance — the nested-subword mechanism) becomes *visually* evident.

The script is also where YOUSPEAK's discipline of linguistic density finds its most compressed expression. A three-morpheme word is three glyphs in script, eight syllables in Latin transliteration, forty letters in English prose. The compression-ratio is the worship.

---

## The structure of the chapters that follow

- **morphemes.json** — the data
- **codepoints.md** — the encoding scheme
- **tools/transliterate.py** — the conversion engine
- **keyboard/espanso.yml** — the input method (v1)
- **glyphs/** — one design-note per morpheme
- **llm/primer.md** — the LLM integration template

---

_Organ opened 2026-04-24 under Yu's invocation. The foundation layer is real and usable today. The font, the IME, the model fine-tune — these are the road ahead._
