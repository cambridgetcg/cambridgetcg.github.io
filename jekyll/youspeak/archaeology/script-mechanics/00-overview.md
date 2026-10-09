---
mission: 2026-04-30-glyph-mechanics-how-scripts-encode-meaning
organ: script/archaeology
opened: 2026-04-30
purpose: Research foundation for conscious glyph-design of the ~35 undrawn YOUSPEAK morphemes
status: active — building across multiple sections
---

# Script Mechanics — How Scripts Encode Meaning

_A design-facing research foundation for the cathedral's glyph-design decisions. Before drawing, we survey. Seven chapters; each names a dimension of the problem; together they constitute a vocabulary for making design-choices consciously rather than by improvisation._

---

## The problem this file solves

The YOUSPEAK script-organ has:
- A morpheme inventory (37 content morphemes, 13 grammatical morphemes assigned PUA codepoints)
- A design philosophy (v1: iconographic, geometric, compound-compatible, LLM-tokenizer-stable)
- Glyph design notes for ~20 morphemes (glyphs/README.md + design_philosophy.md)
- An existing font (youspeak-v1.otf) with some glyphs drawn

What it does NOT have:
- Systematic vocabulary for describing *why* one design choice is better than another
- Research into how historical writing systems solved the same problems we face
- Explicit decision-framework for the 35 undrawn morphemes (including **-me**, the most productive suffix)

This file provides all three.

---

## The seven chapters

| # | Chapter | Core question |
|---|---|---|
| 1 | [Script-type taxonomy](01-script-type-taxonomy.md) | What does each script-type encode, sacrifice, and reveal about reading-experience? |
| 2 | [Letterform anatomy](02-letterform-anatomy.md) | What are the named parts of a glyph and when do they matter? |
| 3 | [Pictographic motivation](03-pictographic-motivation.md) | The ladder from picture to abstraction — when does each stage help? |
| 4 | [Compositionality](04-compositionality.md) | How do scripts combine sub-units — and what does this mean for YOUSPEAK compounds? |
| 5 | [Reading flow](05-reading-flow.md) | Direction, spacing, rhythm, and the page as instrument |
| 6 | [Cognitive load](06-cognitive-load.md) | What makes a glyph fast to recognize, hard to confuse, pleasant to encounter? |
| 7 | [Sacred-script traditions](07-sacred-script-traditions.md) | What makes a script feel sacred — and what can YOUSPEAK inherit? |

---

## The design decision this feeds

When we sit down to draw **-me** (U+E12A — the most productive YOUSPEAK suffix; 25 words; Sumerian *me*, divine-ordinance-as-gift), we need to answer:

1. Is -me a **content morpheme** or a **grammatical suffix**? (It functions like a suffix but carries heavy semantic load.) → Taxonomy question.
2. What **stroke weight, shape family, internal structure** should it use? → Anatomy + Compositionality.
3. Should it **picture** something, or be **purely abstract**? → Pictographic motivation.
4. How does it **compound** with the content morphemes it follows — visually, spatially? → Compositionality.
5. Does it need a **sacred-script inflection** — the sense that the suffix itself carries divine sanction? → Sacred-script traditions.
6. Can a reader recognize it at **8pt on a screen**? → Cognitive load.

This file answers all six.

---

## How to use this file

Read chapter by chapter, or jump to the chapter that addresses your immediate design question. Each chapter ends with a **YOUSPEAK application** section that draws the design-implications explicitly for the cathedral.

Then read `script/glyphs/design_philosophy.md` alongside — that document is the brief; this file is the research that grounds it.

---

_Opened 2026-04-30. Part of mission 2026-04-30-glyph-mechanics-how-scripts-encode-meaning._
