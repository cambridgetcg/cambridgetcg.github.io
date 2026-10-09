---
chapter: determinatives
organ: grammars
role: YOUSPEAK's second structural-grammar chapter (after diplosemy)
opened: 2026-04-24
opened_by: integration of Egyptian hieroglyphic class-marker system
status: doctrine + inventory; implementation in script/morphemes.json pending
---

# Determinatives — Class-Markers at Word-End

_What Egyptian hieroglyphic writing gave uniquely: a silent marker at the end of a word that announces its semantic class to the reader at a glance. YOUSPEAK adopts the mechanism: an optional compact glyph appended to a compound, marking its domain (divine / person / act / abstract / perception / relation / hidden / time). The determinative carries no phonetic value; it is a class-tag for rapid semantic parse._

---

## The mechanism

A YOUSPEAK word composed of morpheme-glyphs optionally gains a **determinative** — a small marker at word-end indicating the semantic class. The determinative:

1. Has no phonetic value (not transliterated as Latin)
2. Is optional — omissible in compact writing
3. Is standard in formal and liturgical writing
4. Belongs to a fixed small set (~10-12)
5. Resolves ambiguity where a word's class is not instantly obvious from its morphemes alone

## Why determinatives are a YOUSPEAK-compatible addition

| YOUSPEAK foundation | How determinatives serve it |
|---|---|
| **EUMATHE** | 10-12 fixed markers; learnable in minutes; accelerate reading thereafter |
| **SAPHE** | class visible at first glance; reduces interpretive effort |
| **ANAKALYPSE** | class-channel distinct from lexical channel; both unfold at once |
| **POLYPHONE** | direct Egyptian adoption; first hieroglyphic-tradition integration in YOUSPEAK |
| **HARMONE** | enforces semantic-class consistency; supports ontology coherence |
| **PRAGMA** | each determinative iconographically grounded (person, eye, house, motion, etc.) |

## The inventory (v1, 10 markers)

Each determinative is a structural glyph in the PUA range U+E170–U+E17F (reserved for structural marks). Appending is optional:

| Code | YOUSPEAK label | Icon source | Marks |
|---|---|---|---|
| U+E170 | **DIV** — divine | Egyptian seated-god (simplified) | words of divine register |
| U+E171 | **PER** — person | Egyptian seated-figure (simplified) | human-agent words, beholder-words |
| U+E172 | **ACT** — act/event | Egyptian walking-legs | events, verbal-actions, processes |
| U+E173 | **ABS** — abstract quality | Egyptian papyrus-scroll | pure-quality words, abstract concepts |
| U+E174 | **PER** — perception | Egyptian eye | seeing, knowing, attending |
| U+E175 | **REL** — relation | (YOUSPEAK original: two figures linked) | between-persons, bonds, pairings |
| U+E176 | **HID** — hidden | (YOUSPEAK original: dashed outline) | concealment, latency, deception |
| U+E177 | **TIM** — time | Egyptian hills-over-sun (simplified) | temporal events, durations |
| U+E178 | **PLC** — place | Egyptian house (simplified) | located things, spatial |
| U+E179 | **QNT** — quantity | Egyptian three-strokes (plural) | plural/mass/collection marker |

The v1 set is kept small (10) for learnability. Additional determinatives can be added for specialized domains if usage demands.

## Applied to the Canon

Each canonical word takes at most one determinative:

### Core Canon (2)

| word | determinative | rationale |
|---|---|---|
| **kimance** | PER (perception) | attending-attending-quality |
| **kinqing** | REL (relation) | between-persons bond |

### Specialized Canon — Liturgy (9)

| word | determinative |
|---|---|
| **doxakallos** | DIV (divine) |
| **kallodoxa** | DIV (divine) |
| **orthophanes** | ABS (abstract quality) |
| **doxalgia** | PER (perception / experience) |
| **anagnoristasis** | ACT (held event) |
| **metastrophesis** | ABS (persistent state) |
| **athaumasma** | ABS (structural trace) |
| **synophora** | REL (between-beholders) |
| **kallophanes** | ACT (appearing-event) |

### Specialized Canon — Zerone (5)

| word | determinative |
|---|---|
| **dokimance** | ACT (testing-event) |
| **artiance** | ABS (pre-domain quality) |
| **complerescence** | ACT (placement-event) |
| **verisleight** | HID (truth-structured-to-deceive) |
| **candence** | ABS (attention-quality) |

### Specialized Canon — Grammar (2)

| word | determinative |
|---|---|
| **diplosemy** | ABS (structural-property) |
| **veriseem** | HID (surface-without-substance) |

## How determinatives render

### In script (glyph-stream)

```
<main-morpheme-glyphs> <determinative>
```

The determinative sits slightly smaller and is rendered with reduced stroke-weight, making it visually subordinate to the main word (like Egyptian hieroglyphic practice).

### In Latin transliteration

Determinatives are NOT rendered in Latin transliteration (following Egyptian practice — they are silent in reading). They appear only in glyph-form.

If a reader needs to see the determinative explicitly in Latin, the notation is:
```
kimance.PER
doxakallos.DIV
verisleight.HID
```

The period separates word from class-tag. Pronunciation does not change.

## Engineering rules

1. **One determinative per word** (primary class). If a word has dual-class (event-quality, abstract-place), choose the dominant.

2. **Liturgical/formal register uses determinatives; everyday register often omits them.** Consistent with Egyptian practice (inscriptions use them more than letters).

3. **When introducing a word to a new reader, use the determinative** to anchor its class. Later usage can omit.

4. **Tool-support**: the transliterator should support a `--with-determinatives` flag that appends the appropriate class-glyph to every canonical word in the output.

## Not covered by determinatives (by design)

- Register/formality (separate system; defer)
- Tense/aspect (handled by English host-grammar; defer)
- Evidentiality (separate system — see grammars/evidentials/)
- Number (English plural handles)
- Possession (English apostrophe-s handles)

Determinatives ONLY carry semantic class.

## Egyptian acknowledgment

The determinative system is a direct loan from Middle Egyptian hieroglyphic practice (~2000 BCE and earlier). Egypt is acknowledged as the originating tradition in each determinative's genealogy. This is how POLYPHONE operationalizes: giving explicit credit to donor-traditions in the grammar itself.

## Integration status

- **Archaeology written**: archaeology/egyptian/determinatives.md
- **Manifesto written**: this document
- **Inventory**: 10 v1 determinatives specified
- **Codepoints**: U+E170–U+E179 (next-available structural range)
- **Canon application**: 18 canon words assigned determinatives

**Pending**:
- Add 10 entries to script/morphemes.json (structural class)
- Design the 10 glyph shapes (add to glyph_specs_v1.py)
- Rebuild font with determinative glyphs
- Update transliterator with optional `--with-determinatives` flag
- Add Espanso triggers for `:ys:div`, `:ys:per`, etc.

---

_Determinatives chapter opened 2026-04-24. YOUSPEAK's second grammar organ. The pyramid-builders' oldest text-technology, operational in the cathedral._
