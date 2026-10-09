---
chapter: 5
title: Reading flow
parent: archaeology/script-mechanics/
---

# Chapter 5 — Reading flow

_Direction, spacing, rhythm, and the page as instrument. How does the eye move through a YOUSPEAK text?_

Reading is a physical act. The eye makes saccades (rapid jumps between fixation points), rests at fixation points for 150-500ms, and processes the information captured during each rest. The *architecture* of a writing system — its direction, spacing, line structure, punctuation — determines where the eye rests and how long. This is not trivial: it shapes the *experience* of reading, and for a liturgical language like YOUSPEAK, the reading-experience is part of the theology.

---

## Direction

Writing direction is one of the most fundamental design choices. All major possibilities have been explored historically:

| Direction | Examples | Notes |
|---|---|---|
| Left-to-right, top-to-bottom | Latin, Greek, Cyrillic, Devanagari, Thai | Most common globally; feels "natural" to LTR-trained readers |
| Right-to-left, top-to-bottom | Hebrew, Arabic, Syriac, Persian | Natural for the Semitic-tradition reader |
| Top-to-bottom, right-to-left | Classical Chinese, Japanese (vertical) | Used in literary/ceremonial contexts in East Asia; columns from right to left |
| Top-to-bottom, left-to-right | Some Southeast Asian scripts; Mongolian vertical | Less common |
| Boustrophedon (alternating) | Early Greek inscriptions, Rongo-rongo (Easter Island) | Right-to-left on one line, left-to-right on the next — like an ox plowing |

**Boustrophedon** (Greek: "as the ox turns") is worth examining specifically. It was used in early Greek archaic inscriptions (before the direction was standardized to LTR in the Classical period). The eye follows the same direction as it reads each line; at the end of a line, instead of jumping back to the left margin (a long, cognitively expensive saccade), the eye simply continues in the opposite direction on the next line. Brain imaging suggests this is marginally more efficient for certain types of text. But it requires *mirror-form letters* — on right-to-left lines, the letters must be mirrored. The cognitive load of mirror-letters was apparently acceptable in archaic contexts but was abandoned as literacy spread and standardization became more important.

**For YOUSPEAK**: Left-to-right, top-to-bottom is correct. Reasons:
1. YOUSPEAK runs on screens, websites (index.html, Docsify), keyboards — all LTR-optimized.
2. YOUSPEAK morphemes come from multiple traditions including LTR (Latin, Greek) and RTL (Hebrew, Arabic). A single direction must be chosen; LTR is more interoperable with modern infrastructure.
3. The compound-separator (U+E160) and suffix-attachment logic assumes LTR reading order.

However: there is a tradition of *ceremonial direction reversal* in some script-traditions. In Egyptian hieroglyphs, the human and animal glyphs always *face the beginning of the text* — if the text reads LTR, the animals face left (toward the starting point). A YOUSPEAK liturgical mode that reads right-to-left (reversing the normal direction) could be designed as a special ceremonial variant — writing that goes *against the grain*, like walking backward as an act of reverence. This is speculative and deferred; noted here for future exploration.

---

## Spacing — three levels

**Inter-stroke spacing** (within a single glyph): the space between strokes inside one glyph. For YOUSPEAK, this is defined by the glyph's counter (interior negative space) — handled in glyph design.

**Inter-glyph spacing** (between glyphs in a compound): the space between adjacent glyphs in a word. This is controlled by the glyph's *side-bearings* — the white-space padding built into each glyph's left and right edges.

YOUSPEAK convention:
- Between two **content morphemes**: compound-separator (U+E160) renders as a thin hairline vertical, approximately half-glyph-height, centered on the baseline. Side-bearings are standard (100 EM each, for 200 EM total inter-glyph space on each side of the separator).
- Between a **content morpheme and its suffix** (-me, -ance, -sis, etc.): NO compound-separator; side-bearings are *reduced* (50 EM on content-morpheme right; 25 EM on suffix left = 75 EM total gap). This creates a visual "pull" toward the suffix — the suffix reads as attached, not as a following word.

**Inter-word spacing** (between words in a sentence): for YOUSPEAK running text, a standard word-space (400 EM = 40% of glyph-width). This is wider than typical Latin typography (standard word-space is ~250 EM for proportional type) because YOUSPEAK glyphs are wider than Latin letters on average and each glyph carries more semantic density — more white-space between words gives the eye a clear pause to process the compound before moving on.

---

## Rhythm

Reading has rhythm. The eye's saccade-and-fixation pattern is rhythmic; good typography and script-design creates a rhythm that matches the reader's natural eye-movement.

In alphabetic scripts, rhythm comes from:
- **Word length variation**: long words interrupt short words; the eye adjusts its rhythm
- **Punctuation**: periods, commas, and other marks create rhythmic interruptions of different depths
- **Line ending**: the return saccade (jump back to beginning of next line) creates a major rhythmic interrupt
- **Sentence structure**: syntactic complexity affects reading speed; simple subject-verb-object reads faster than embedded clauses

In logographic scripts (like Chinese), rhythm comes from:
- **Character spacing**: hanzi are written in a grid; every character is the same width; rhythm is completely regular. This is one reason Chinese poetry (especially classical 4-character or 5-character verse) feels metrically exact — the visual rhythm exactly matches the syllabic rhythm.
- **Column structure**: in vertical Chinese text, the columns provide a rhythmic structure; each column is a reading-unit.

**For YOUSPEAK**: YOUSPEAK's rhythm in running text will be driven by:
1. **Compound-length variation**: short compounds (2 morphemes) alternate with longer ones; the eye's fixation pattern varies
2. **Word-boundary white space**: the standard 400 EM word-space creates clear inter-word pauses
3. **The weight of specific glyphs**: some YOUSPEAK morphemes have more visual mass than others (phanes with its radiating rays; doxa with its solid inverted triangle); the eye rests longer at visually complex glyphs

**Liturgical rhythm specifically**: YOUSPEAK is designed for worship-contexts. In liturgical use, the reading is often *slow* and *chanted* — the rhythm of speech matches a canonical musical pattern. The visual rhythm of YOUSPEAK text should support slow, contemplative reading. This means:
- Word-spaces should be generous (the eye pauses between words)
- Each compound-word should be visually complete enough to dwell in (not fragmented into multiple fixation-points)
- Line-breaks should fall at natural phrase-boundaries (not arbitrary line-length wrap)

This last point suggests that for liturgical YOUSPEAK text, **line-breaking should be semantic, not geometric**. A phrase in YOUSPEAK should fit on one line if possible, with the line-break at the phrase-boundary rather than mid-phrase at the right-margin. This is closer to how poetry is typeset than how prose is typeset. For the Docsify site (which uses responsive markdown), this is controlled by the HTML structure rather than by the font — but it should be noted as a design intention.

---

## Punctuation as rhythm-mark

Punctuation is the architecture of prose rhythm. Different writing traditions handle punctuation very differently:

**Latin/Western**: extensive punctuation (comma, semicolon, colon, period, dash, parenthesis, question-mark, exclamation-mark). The system marks every major syntactic boundary.

**Chinese classical text**: minimal punctuation. Classical Chinese texts use white-space and character-count to indicate sentence-structure. Modern Chinese uses Western-derived punctuation (introduced ~1920s). Classical readers were expected to "cut the text" (*duān jù*, 斷句) — finding the sentence-boundaries from syntactic cues alone.

**Hebrew Biblical text**: the *ta'amim* (cantillation marks) serve as a punctuation-equivalent, but they are primarily *musical notation* for chanting rather than syntactic punctuation. The marks divide the text into units (phrases, half-verses, verses) and indicate the melodic-cadence for each unit. They are simultaneously syntactic-boundary markers AND musical scores. This is deeply appropriate for a sacred text designed to be sung.

**Maya glyphs**: no punctuation as such; glyph-blocks are arranged in a grid (read top-to-bottom in pairs of columns, left-to-right across columns). The grid itself creates the rhythm.

**For YOUSPEAK**: The design philosophy does not yet specify a punctuation system. I propose:

| Punctuation mark | YOUSPEAK form | Function |
|---|---|---|
| Phrase-end (equivalent to comma) | A short vertical bar (half-height of glyph) | Minor rhythmic pause |
| Sentence-end (equivalent to period) | A small filled circle (like a Sanskrit daṇḍa (।)) | Major rhythmic pause |
| Sacred-invocation start | The canon-mark (◆) at word-start | Already exists; marks formal register |
| Line of a liturgical passage | No explicit mark; line-break is structural | |
| Question (interrogative) | A small upward-curve mark (like a minimal ?) | |
| Breath-pause in liturgy | A centered dot (·) — the Greek *ano teleia* | |

The **Sanskrit daṇḍa** (|) and the **double daṇḍa** (||) are worth considering as models for YOUSPEAK liturgical punctuation. They are simple vertical bars — visually minimal, directionally neutral (work in any script direction), and carry clear rhythmic force. A single daṇḍa at a phrase-end says: breath here, one beat. A double daṇḍa says: complete thought, longer breath. This is a pure rhythm-notation function.

---

## The page as instrument

The page (or screen) is not a neutral background. It is an instrument with geometry, proportion, and history. How a text is placed on a page communicates something before a single glyph is read.

**Egyptian temple walls**: text flows across vast stone surfaces following the architectural structure. The text is not on a page — it *is* the architecture. The wall IS the page; the building IS the book. The visitor to a temple is surrounded by text, immersed in it, walking through it. Reading is a spatial experience.

**Hebrew Torah scroll**: text on parchment, handwritten by a scribe (sofer) following strict rules. The scroll is held at both ends by wooden rollers (Etz Chaim, "trees of life"). Reading the Torah is done from right to left; the scroll unrolls as reading progresses. The text moves; the reader is stationary. This is the opposite of the book. The scroll "gives itself" to the reader.

**Buddhist sutras**: often written on long palm-leaf manuscripts (pothi), folded and stored in cloth. The text is horizontal; the pages are read in sequence. In Tibetan tradition, the text is read aloud in a low, continuous chant. The physical act of unfolding the manuscript and beginning the chant is itself a ritual act. The page is an object of veneration before it is an object of reading.

**Western codex**: the bound book. Pages are turned. The text is fixed; the reader moves through it in a fixed direction. The codex allows random access (you can open anywhere) in a way that scrolls and palm-leaf manuscripts do not. This was a practical innovation that also changed reading culture: books that could be opened anywhere could be *cited* (by page number); citation made scholarship possible at scale.

**For YOUSPEAK's digital context**: YOUSPEAK currently lives at `http://localhost:4000` as a Docsify site. The page is a screen. The reader scrolls or clicks between pages. This is closest to the codex model — fixed text, reader moving through it. But the digital context adds:
- **Responsive layout**: the "page" changes width depending on the screen; YOUSPEAK glyphs must work at all widths
- **Hyperlinks**: cross-reference navigation that is impossible in physical documents
- **Font-dependent rendering**: if the YOUSPEAK font is not loaded, glyphs render as boxes or fallback characters; the "page" degrades gracefully if the font is missing

**The aspiration**: YOUSPEAK should design its site-display as if the screen were a stone wall or a scroll — not a Wikipedia article. The visual hierarchy (large glyphs, generous spacing, slow rhythm) should create a reading experience that is contemplative, not consumptive. The dashboard.md is already moving in this direction (glyph-first presentation, generous whitespace, reverent tone).

---

## YOUSPEAK reading-flow specifications

Summarizing the design decisions this chapter supports:

| Element | Specification |
|---|---|
| Writing direction | LTR, top-to-bottom |
| Word-space | 400 EM (generous; contemplative reading) |
| Inter-compound space (separator) | 200 EM (thin hairline) |
| Suffix attachment space | 75 EM (tight; suffix "clings" to root) |
| Line-breaking | Semantic (at phrase-boundaries) for liturgical text; standard wrap for running prose |
| Punctuation | Sanskrit daṇḍa-style marks (| for phrase-end, || for sentence-end, · for breath-pause) — to be formally added to the codepoint table |
| Sacred text display | Left-margin indent, one compound per fixation, generous inter-word spacing |
| Dashboard/site rhythm | Glyph-first, large display sizes, white space between entries |

---

_Chapter 5 complete. → [Chapter 6: Cognitive load](06-cognitive-load.md)_
