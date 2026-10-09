# script · the writing-system organ

The cathedral's fifth organ. Each YOUSPEAK morpheme is assigned a glyph via PUA codepoints (U+E100–U+E1FF). Latin transliteration is the internal representation; glyphs are the display layer.

## Read first

→ [manifesto.md](manifesto.md) — doctrine and axioms

## What lives here

- **[manifesto.md](manifesto.md)** — script doctrine: separation of representation and display
- **[codepoints.md](codepoints.md)** — encoding spec (human-readable)
- **[morphemes.json](morphemes.json)** — morpheme inventory (machine-readable)
- **[MODULES.md](MODULES.md)** — full modular architecture
- **`glyphs/`** — iconographic design notes per morpheme
- **`fonts/`** — OTF/TTF font files: `youspeak-v1.otf` + `youspeak-v1.ttf` (93 glyphs — complete morpheme coverage as of S092; `youspeak.otf` is the v0 relic)
- **`keyboard/`** — text-expander input — see [`keyboard/espanso.yml`](keyboard/espanso.yml)
- **`llm/`** — LLM integration (P1 prompt-engineering live; P2 RAG planned; P3 fine-tune deferred). See [`llm/primer.md`](llm/primer.md).
- **`tools/`** — Python utilities for font building, glyph rendering, and transliteration; `rebuild.sh` runs the whole pipeline (fonts → previews → tests → keyboard layer) in one command, `--install` to install the font

## How to type in YOUSPEAK

Install `keyboard/espanso.yml` (cross-platform). Then `:doxakallos` in any text field expands to the glyph.

## See also

- [../grammars/](../grammars/) — structural mechanisms (chapter on script-as-theology lives in chapter 5)
- [../canon.md](../canon.md) — every Core word listed alongside its assigned glyph
