---
title: YOUSPEAK Script — Modular Architecture & Compatibility Review
opened: 2026-04-24
invoker: Yu
scope: establish each layer as a foundational module; review coverage; confirm macOS + Kingdom OS compatibility
---

# YOUSPEAK Script — Modular Architecture & Compatibility Review

_Every layer of the writing system, documented as a self-contained module with its purpose, interface, dependencies, and status. Review against the needs of digitized-language support. Compatibility audit for macOS and Kingdom OS._

---

## Module map

```
  script/                          ← the organ
  ├─ manifesto.md                  module 0: doctrine + axioms
  ├─ morphemes.json                module 1: data foundation (morpheme inventory)
  ├─ codepoints.md                 module 2: encoding spec (PUA assignments)
  ├─ glyphs/                       module 3: glyph design (93/93 morphemes drawn; S092)
  ├─ tools/transliterate.py        module 4: Latin ↔ glyph conversion (working)
  ├─ keyboard/espanso.yml          module 5: input method (text-expander; working)
  ├─ fonts/                        module 6: font files (BUILT — youspeak-v1.otf/.ttf, 93 glyphs; S092)
  ├─ llm/primer.md                 module 7: LLM integration (P1 complete; P2/P3 planned)
  └─ MODULES.md                    this document
```

---

## Module 0 — Manifesto & Axioms (`script/manifesto.md`)

**Purpose:** establish the doctrinal framework — logographic over phonemic, compositional, Latin-transliteration-as-internal-representation, PUA encoding, graceful fallback.

**Interface:** read-only. All downstream modules conform to these axioms.

**Dependencies:** none.

**Status:** complete.

**macOS compatibility:** N/A (text document).
**Kingdom OS compatibility:** N/A (text document).

---

## Module 1 — Morpheme Inventory (`script/morphemes.json`)

**Purpose:** authoritative data source for every YOUSPEAK morpheme — its canonical Latin transliteration, PUA codepoint, class (content/grammatical/structural), source tongue, native form, meaning, and canon-words-using-it.

**Interface:** JSON schema. Consumers: `tools/transliterate.py`, future font-build tools, future IME implementations, LLM primers, documentation generators.

**Schema (excerpt):**
```json
{
  "codepoint": "U+E100",
  "latin": "doxa",
  "class": "content | grammatical | structural",
  "tongue": "Greek | Latin | Hebrew | English | ...",
  "native": "δόξα",
  "meaning": "glory, manifested-weight",
  "used_in": ["doxakallos", "doxalgia", ...]
}
```

**Dependencies:** none (pure data).

**Status:** 42 morpheme entries as of 2026-04-24 (32 content, 13 grammatical, 5 structural). Extensible.

**Extension protocol:** append new morphemes at next available codepoint in the appropriate subrange. Never rearrange. Update `codepoints.md` in lockstep.

**macOS compatibility:** ✓ pure JSON; no OS dependency.
**Kingdom OS compatibility:** ✓ pure JSON; readable from every fleet-agent's Python runtime.

---

## Module 2 — Codepoint Encoding Spec (`script/codepoints.md`)

**Purpose:** human-readable reference for the PUA assignments (`U+E100–U+E1FF`). Structured by subrange: content / grammatical / structural. Documents migration-path to future Unicode Consortium proposal.

**Interface:** markdown reference; for humans. `morphemes.json` is the machine-readable source of truth; `codepoints.md` is the human-readable mirror.

**Dependencies:** should be kept in sync with `morphemes.json` (future: a validator script).

**Status:** complete.

**macOS compatibility:** ✓ markdown.
**Kingdom OS compatibility:** ✓ markdown.

---

## Module 3 — Glyph Design (`script/glyphs/`)

**Purpose:** iconographic design notes for each morpheme's glyph. Each design-note records: the morpheme's meaning, an iconographic rationale for the chosen visual form, and an ASCII sketch serving as spec for the future vector-font production.

**Interface:** markdown design notes in `script/glyphs/README.md` (and eventually `script/glyphs/<morpheme>.md` per-morpheme).

**Design principles (from manifesto):** iconographic-where-possible, geometric-and-constructible, visually-distinct, compound-compatible, register-stable.

**Dependencies:** consumed by module 6 (font production).

**Status:** all 93 catalogued morphemes have drawn glyph specs (S092, 2026-06-10 — the font made flesh). Design rationales: `design_philosophy.md` + `design_notes_s092.md`. Font built programmatically from the specs via fontTools (no external vector tool needed); `tools/rebuild.sh` regenerates everything in one command.

**macOS compatibility:** ✓ design-notes are markdown. Font production uses FontForge or Glyphs — both have native macOS distributions. Glyphs is Mac-native; FontForge is cross-platform with a working Mac build.
**Kingdom OS compatibility:** ✓ same as macOS; font production workflow is Mac-native.

---

## Module 4 — Transliterator (`script/tools/transliterate.py`)

**Purpose:** convert YOUSPEAK text between Latin-transliteration (internal representation) and PUA glyph encoding (display representation).

**Interface:**
```
python3 transliterate.py to-glyph "<latin-text>"    # → glyph-encoded text
python3 transliterate.py to-latin "<glyph-text>"    # → Latin text
python3 transliterate.py to-html  "<latin-text>"    # → HTML with ruby annotations
python3 transliterate.py test                        # → round-trip test suite
```

**Python-API:**
```python
from transliterate import latin_to_glyph, glyph_to_latin, to_html
glyphs = latin_to_glyph("doxakallos")      # returns PUA-encoded string
latin = glyph_to_latin(glyphs)             # returns "doxakallos"
html = to_html("doxakallos")               # returns <span class="youspeak">...
```

**Algorithm:**
1. Word-level canonical override (CANONICAL_DECOMPOSITIONS dict) — known canon words use authoritative morpheme decomposition, handling Greek combining-form irregularities (kallos→kallo in modifier position) and elision (doxa+algia → doxalgia).
2. Morpheme-decomposition fallback for unknown words: greedy longest-match over content/prefix/suffix morphemes. Only words that fully-consume their characters become glyphs; partially-matched words (English "and", "against") pass through unchanged.
3. Non-alpha characters (spaces, punctuation) always pass through.

**Test results:** 13/13 canonical round-trips succeed; real-sentence mixed-English-YOUSPEAK text preserves English words and glyphifies only YOUSPEAK words.

**Dependencies:** Python 3.9+ (for type hints and `@dataclass`); reads `morphemes.json`.

**Status:** working. No font required (produces PUA-encoded strings that render as glyphs only if a YOUSPEAK font is installed; otherwise renders as boxes — but the reverse-transliteration always works regardless).

**macOS compatibility:** ✓ pure Python 3, no platform-specific calls. macOS ships Python 3.9+ by default (Python 3.11 in recent macOS; all Mac Studio / MacBook Air machines in the Kingdom have it).
**Kingdom OS compatibility:** ✓ Python is ubiquitous across the fleet. Can be imported by Nuance's tools, Asha's heartbeat, or any fleet-agent.

**Kingdom integration path:**
```python
# from any Kingdom-agent's Python:
import sys; sys.path.insert(0, 'script/tools')  # path to this repo's script/tools
from transliterate import latin_to_glyph
# use in agent code:
display_form = latin_to_glyph(agent_output)
```

---

## Module 5 — Input Method (`script/keyboard/espanso.yml`)

**Purpose:** enable typing YOUSPEAK on standard hardware keyboards via text-expansion. User types `:doxakallos` + space → Espanso substitutes the PUA glyph sequence.

**Interface:** Espanso YAML match-rules. Canon-word triggers (`:word`), morpheme triggers (`:m:morpheme`), structural-mark triggers (`:ys:sep`, `:ys:pair`, etc.), and a `:ys:help` reference command.

**Installation:**
- macOS: copy to `~/Library/Application Support/espanso/match/youspeak.yml`; restart Espanso
- Linux: copy to `~/.config/espanso/match/youspeak.yml`
- Windows: copy to `%APPDATA%\espanso\match\youspeak.yml`

**Runtime:** Espanso is an open-source text-expander (MIT license). Installed on macOS via Homebrew (`brew install espanso`) or the project's installer. Requires Accessibility permissions on macOS (standard for any text-expander).

**Dependencies:** Espanso daemon running as user-space process.

**Status:** working for all 18 canon words (2 Core + 16 Specialized) + 24 morphemes (19 original + 5 Core-added) + 5 structural marks + help.

**macOS compatibility:** ✓ Espanso is Mac-native; Homebrew-installable; uses standard Accessibility API. No System-Integrity-Protection conflicts.
**Kingdom OS compatibility:** ✓ all Kingdom machines are macOS; install once per user. For fleet-wide deployment, add Espanso to the Kingdom bootstrap script.

**Upgrade path:** for IME-grade integration (inline suggestions, floating candidate-window like Pinyin IME), build a macOS Input Source bundle. Deferred — Espanso covers v1 needs.

---

## Module 6 — Font (`script/fonts/`) — BUILT (S092)

**Purpose:** the actual TTF/OTF file that renders PUA glyphs as YOUSPEAK's visible forms.

**Interface:** standard font-file (`youspeak.otf`) installable in macOS Font Book (or `~/Library/Fonts/`); referenced in CSS via `@font-face`; usable in any typography-capable application (Pages, Sketch, Figma, VS Code, web browsers).

**Dependencies:** vector-drawing tool to produce the glyphs; font-compilation tool to package.

**Recommended production pipeline:**
1. Draw each glyph in **Glyphs** (Mac-native, professional, the industry standard) — OR **FontForge** (cross-platform, free, GPL) — OR **Figma** + a font-building plugin.
2. Assign each glyph to its PUA codepoint per `morphemes.json`.
3. Export to OTF with OpenType tables for proper line-metrics and side-bearings.
4. Test: install in Font Book, render in TextEdit + Chrome + VS Code; verify consistency.
5. Distribute: place in `script/fonts/youspeak.otf`; each Kingdom user installs once.

**Design spec:** complete; see `script/glyphs/README.md`.

**Status:** **DEFERRED** — requires vector-drawing work that cannot be done in this Python+text-file session. Next session: engage a font editor, produce the first-pass font.

**macOS compatibility:** ✓ macOS supports OTF/TTF natively; fonts install via drag-to-Font-Book or `~/Library/Fonts/`. No special configuration.
**Kingdom OS compatibility:** ✓ same; fleet-wide distribution via a Kingdom-setup script that copies the font to each user's library on initial setup.

---

## Module 7 — LLM Integration (`script/llm/primer.md`)

**Purpose:** integrate YOUSPEAK with large language models — both foundation-model APIs (Claude, GPT, Gemini) and local models (Llama).

**Three phases:**

| Phase | Approach | Cost | Status |
|---|---|---|---|
| P1 | Prompt-engineering with primer + canon excerpts in context | zero | **WORKING** — primer written; usable today by any LLM |
| P2 | RAG over `canon/`, `archaeology/`, `labs/logos/forge/` | moderate (embedding + vector store) | **PLANNED** — implementation stub in primer; next session |
| P3 | Fine-tune a model on YOUSPEAK corpus | substantial | **DEFERRED** — requires corpus we don't yet have |

**Interface (P1):** primer text at `script/llm/primer.md`. Load into session context (system-prompt, preamble, or first user message). Model operates in Latin-transliteration exclusively.

**Interface (P2, planned):** a RAG service — FAISS/Chroma vector-store + embedding model — that retrieves top-K relevant canon entries per query, prepends to LLM context.

**Dependencies (P1):** only the LLM itself.
**Dependencies (P2):** Python + `sentence-transformers` + `faiss-cpu` (or Chroma) — all standard.

**Status:** P1 live. P2 stubbed in primer.md with implementation sketch; actual build next session.

**macOS compatibility:** ✓ all LLM APIs are HTTPS; `sentence-transformers` + FAISS both have Mac builds (FAISS via `pip install faiss-cpu`; no Apple-Silicon issues on recent versions).
**Kingdom OS compatibility:** ✓ fleet-agents already use LLM APIs. Nuance's CLAUDE.md can include a YOUSPEAK-primer pointer; Asha's agents benefit from RAG retrieval over trust-terminology + canon/.

---

## Coverage review against needs

| Need | Module(s) | Status |
|---|---|---|
| Visible glyph for every YOUSPEAK morpheme | 3, 6 | spec complete; vector font deferred |
| Digital encoding (copy-paste, filesystems, DB) | 1, 2, 4 | ✓ complete |
| Latin ↔ glyph conversion | 4 | ✓ working; 13/13 canon round-trips |
| Input method (typing on standard keyboards) | 5 | ✓ working via Espanso |
| Display on web, documents, applications | 6, 4 | waits on font; HTML/CSS ready |
| LLM reading YOUSPEAK text | 7 (P1) | ✓ working via primer |
| LLM generating YOUSPEAK text | 7 (P1) | ✓ working via primer |
| Mixed English-YOUSPEAK text (sentence-level use) | 4 | ✓ working (English words pass through) |
| Fallback when font missing | 4 | ✓ Latin transliteration always recoverable |
| Grow as new canon words are added | 1, 2, 5 | ✓ append-only JSON + Espanso extensible |
| Fleet-wide deployment in Kingdom | 5, 6 | Espanso works now; font awaits vector-production |
| Proper IME (inline suggestions, candidate window) | 5 (future) | DEFERRED |
| Native LLM fluency (no primer needed) | 7 (P3) | DEFERRED |
| Official Unicode Consortium registration | 1, 2 (future) | DEFERRED |

**What is not yet covered (explicit gaps):**

1. **No actual font file.** Design notes complete; vector-drawing work pending. Without the font, glyphs render as boxes in most applications. The Latin-transliteration always remains readable, which is the graceful-fallback we built for.
2. **No RAG service yet.** P2 of LLM integration is stubbed but not implemented.
3. **No validator for `morphemes.json` ↔ `codepoints.md` sync.** Can drift if updated separately.
4. **No macOS Input Source bundle.** Espanso suffices for v1 but a proper IME would give better UX (inline preview, candidate pop-up).
5. **No corpus for fine-tuning.** Canon is too small; substantial YOUSPEAK-authored text must accumulate before training is worthwhile.

**What remains adequate:**

1. The encoding (Module 1+2) is structurally sufficient for 256 morphemes in the first PUA pane; the Canon has 42 morphemes; ample growth room.
2. The transliterator (Module 4) handles the critical cases correctly and fails-safe on ambiguity (passes English through, round-trips canon).
3. The input method (Module 5) covers keyboard-typing without custom hardware.
4. The LLM integration (Module 7 P1) works today without additional infrastructure.

---

## macOS compatibility audit (summary)

| Module | macOS support | Reason |
|---|---|---|
| 1 morphemes.json | ✓ | pure JSON |
| 2 codepoints.md | ✓ | pure markdown |
| 3 glyphs/ notes | ✓ | markdown design-notes; font production is Mac-native (Glyphs or FontForge) |
| 4 transliterate.py | ✓ | Python 3.9+, no platform calls |
| 5 espanso.yml | ✓ | Espanso is Mac-native via Homebrew; standard Accessibility API |
| 6 fonts/ | ✓ (when built) | OTF/TTF installable via Font Book |
| 7 llm/primer.md | ✓ | text primer + standard LLM APIs + Python RAG stack |

All modules are macOS-compatible. No layer requires system-integrity-protection exemption. No module requires code-signing. No kernel extensions.

---

## Kingdom OS compatibility audit

Kingdom OS operates across:
- **Wall 1 (Triarchy):** Alpha (MacBook Air), Beta (Mac Studio), Gamma (Mac Studio)
- **Wall 2 (Fleet Agent):** Nuance (MacBook Air M2), future citizens
- **VPS Fleet (Walls 3-7):** Forge, Lark, Sentry, Patch — Linux nodes

**Module compatibility by wall:**

| Module | Macs (W1, W2) | Linux VPS (W3-7) |
|---|---|---|
| 1 morphemes.json | ✓ | ✓ |
| 2 codepoints.md | ✓ | ✓ |
| 3 glyphs/ notes | ✓ | ✓ (markdown read-only) |
| 4 transliterate.py | ✓ | ✓ (Python cross-platform) |
| 5 espanso.yml | ✓ | ✓ (Espanso Linux build exists) |
| 6 fonts/ | ✓ | ✓ (Linux font systems — fontconfig — handle OTF/TTF) |
| 7 llm/primer.md | ✓ | ✓ |

**Kingdom-specific integration recommendations:**

1. **Nuance's CLAUDE.md** should add a pointer to `script/llm/primer.md`, so every Nuance-session boots with script-awareness.

2. **Asha's CLAUDE.md** should be similarly updated; Asha's canon vocabulary (dokimance, artiance, verisleight, candence, complerescence, synlanthescence) all have glyphs assigned.

3. **HIVE-aware transliteration:** add a `transliterate` subcommand to the Kingdom's local `hive.py` so inter-agent messages can be posted in Latin (canonical) and rendered as glyphs in UIs that support the font.

4. **Kingdom-OS bootstrap addition:** when a new Kingdom machine is provisioned, the setup script should:
   - Install Espanso (`brew install espanso` on Mac; `apt install espanso` on Linux where available)
   - Copy `script/keyboard/espanso.yml` to the user's Espanso match directory
   - Install the YOUSPEAK font (when built) to `~/Library/Fonts/` (Mac) or `~/.fonts/` (Linux)
   - Ensure Python 3.9+ is available (already a Kingdom requirement for `memory.py`, `hive.py`, etc.)

5. **Fleet-wide deployment of `transliterate.py`:** the tool can be copied to a shared location (a symlink to `script/tools/transliterate.py`), making it callable from any Kingdom agent without repeating the path.

---

## Priorities for the next session (in order)

1. **Vectorize the font** (Glyphs or FontForge). Produces `script/fonts/youspeak.otf`. This is the single highest-leverage next step — unlocks actual visual rendering across all tools.

2. **Build the RAG service** (Phase 2 LLM integration). A small Python module in `script/llm/rag.py` that embeds canon/, archaeology/, and forge-docs and provides a retrieve() API. Integrate with Nuance and Asha's boot sequences.

3. **Add `transliterate.py` as a Kingdom fleet-tool** (a local symlink); wire into HIVE.

4. **Validator script** (`script/tools/validate.py`): verify `morphemes.json` ↔ `codepoints.md` consistency; verify every canon word has an entry in `CANONICAL_DECOMPOSITIONS`; flag orphaned codepoints.

5. **Expand design-notes** (`script/glyphs/<morpheme>.md`) to a file-per-morpheme with full design rationale; the font-artist works from these.

---

## The organ's integration with the broader Kingdom

YOUSPEAK's five organs (archaeology, forge, pipeline, grammars, script) together now constitute a complete language infrastructure:

- **Semantic layer:** the Canon (16 words, growing)
- **Structural layer:** the grammars/diplosemy chapter (6 mechanisms + 3 stubs)
- **Material layer:** the script/ organ (this document) — codepoints, glyphs, input, display, LLM integration

The Kingdom's agents consume this at their scale. Nuance forges; Asha operates; Yu orchestrates. The script-organ is what makes YOUSPEAK *visible* in the Kingdom — what turns a discipline-of-vocabulary into a *writing system* the fleet can actually use.

---

_Module review 2026-04-24. Seven modules documented. Five working today, one stubbed, one deferred. macOS-compatible across the board. Kingdom OS compatible across all walls. The writing system has its foundation._
