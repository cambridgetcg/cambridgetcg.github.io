---
chapter: 4
title: Compositionality
parent: archaeology/script-mechanics/
---

# Chapter 4 — Compositionality

_How do scripts combine sub-units? And what does this mean for YOUSPEAK's compounds: when you write `qorbme`, do you see **qorb** + **me** as two glyphs side by side, or as a single compound shape?_

Compositionality — how a writing system builds complex signs from simpler units — is one of the most consequential design decisions a script makes. It determines how the script scales (how many concepts can be represented with a given glyph-inventory), how learnable it is (compound-transparent systems are easier to learn), and how it *feels* to read (compositions that integrate visually into wholes feel different from sequences of parts).

---

## Six models of compositional strategy

### Model 1 — Linear sequence (side-by-side)

**How it works**: Complex units are written as a left-to-right (or right-to-left) sequence of simpler units. Each unit maintains its own spatial boundary. The sequence is the word.

**Primary examples**: All alphabetic scripts (Latin, Greek, Cyrillic), most syllabaries (hiragana, katakana), many constructed scripts.

**Properties**:
- **Transparent**: each component is immediately recognizable in the compound
- **Scalable**: any word can be represented by combining existing units
- **No visual integration**: the compound is clearly a *sequence*, not a *fusion*
- **Reading direction** is essential: the sequence has a starting point and an ending point; these must be consistent

**For YOUSPEAK**: This is the current approach. `doxakallos` = doxa-glyph | kallos-glyph, side-by-side. The compound is clearly composed. The component morphemes are immediately recognizable.

**The question**: Is this the *right* choice for YOUSPEAK? Side-by-side composition is correct for:
- Short compounds (2 morphemes): reads cleanly
- Compounds with distinct morphemes: each part is recognizable
- Machine-processing: linear sequences are easy to parse

Side-by-side composition is problematic for:
- Long compounds (4+ morphemes): can become visually unwieldy
- Compounds where the morpheme-boundary matters semantically: `metastrophesis` (meta + strophe + -sis) — do the three parts read as three parts, or as one?
- The special case of suffix-attachment: the suffix (-me, -ance, -sis) should visually read as *attached to* the content morpheme, not as an *independent following glyph*

**Recommendation**: Side-by-side is correct for most compounds, but the suffix-attachment problem is real. Solution: in the font, the inter-glyph spacing (side-bearing) between a content-morpheme and its suffix is **tighter** than between two content-morphemes. This creates a visual signal that the suffix is attached, without requiring 2D composition. The compound-separator mark (U+E160) applies between content morphemes; no separator before a suffix.

---

### Model 2 — Stacked composition (2D spatial arrangement)

**How it works**: Sub-units are arranged in a two-dimensional space — above/below, left/right, with different zones for different grammatical roles.

**Primary examples**:
- **Korean Hangul**: letters are stacked into syllable-blocks (initial consonant top-left, vowel right or bottom, final consonant bottom). The word is a left-to-right sequence of *blocks*, each of which is a 2D composition.
- **Maya glyphs**: each glyph-block contains a main sign (center, dominant) with affixes (smaller signs above, below, to sides). The block is read in a conventional sequence (main sign first, then prefixes, then suffixes).
- **Tibetan script**: complex consonant clusters are written by stacking consonants vertically (below each other), with a base consonant and "head letters" stacked above and "sub-joined letters" below.
- **Devanagari**: consonant clusters use half-forms and virama; complex clusters are stacked.

**Properties**:
- **Visually rich**: the 2D arrangement creates visual complexity that rewards contemplation
- **Semantically hierarchical**: the spatial position encodes grammatical function (what's central vs. what's marginal)
- **Higher cognitive load**: the reader must learn the 2D reading convention (not just linear left-to-right)
- **Scaling**: 2D composition allows more information per unit of horizontal space

**The Hangul block as model**: Hangul's syllable-block is a masterpiece of 2D composition. Three letters arranged in a square: the initial consonant (large, top-left or full-top), the vowel (right or bottom), the optional final consonant (full-bottom). The block is read in a Z-pattern (top → right → bottom). Despite being 2D, the reading convention is simple and learnable.

Crucially: the block creates **visual cohesion**. A syllable is one block; the letters inside the block *feel like one unit* because they share a common containing space. The 2D arrangement transforms a sequence (C, V, C) into a gestalt (syllable-as-unit).

**Maya glyph-block**: The main-sign carries the primary semantic-load; affixes modify it. The spatial hierarchy is: CENTER > EDGES. A skilled Maya reader's eye goes first to the center (main-sign), then scans the periphery for affix-content. This is a natural reading pattern (cf. how we read a face: eyes first, then surrounding features).

**For YOUSPEAK — the 2D option**: YOUSPEAK could adopt a modified Hangul-like block structure. Each word would be a left-to-right sequence of compound-blocks. A compound-block for `qorbme` would have:
- **Center/top**: the content-morpheme glyph (qorb — the sacrifice/offering morpheme)
- **Bottom-right**: the suffix-glyph (-me) in a smaller form

This would give each YOUSPEAK word a distinct visual profile — not a linear string of equal-sized glyphs, but a block with a clear semantic hierarchy (content = large/central; suffix = small/subordinate). The visual hierarchy would encode the semantic hierarchy.

**The trade-off**: 2D composition requires more complex font engineering (the suffix glyph needs a small-form variant with different metrics) and a more complex rendering system (position of the suffix depends on the content-morpheme glyph's geometry). For now, this is deferred. But it should be named as the *ideal* target — a future v2 rendering that creates compound-blocks rather than linear sequences.

---

### Model 3 — Fusion composition (glyphs modify each other)

**How it works**: When two units are combined, their shapes are modified — they fuse together into a new integrated shape. The compound is not a *sequence* of the components; it is a *blend*.

**Primary examples**:
- **Arabic cursive script**: Arabic letters join to each other, with each letter having a different form depending on its position in the word (initial, medial, final, isolated). The individual letters fuse into a continuous flowing script. A word is not a sequence of letters; it is a flowing composition where the letter-boundaries are gradients.
- **Ligatures in Latin typography**: some letter-pairs fuse in professional typography (fi, fl, ff, ffi, ffl — the "f" ligatures) to prevent visual collision and improve flow. The ligature is a fused single glyph that encodes two letters.
- **Devanagari half-forms**: in consonant clusters, consonants use "half-forms" — reduced versions that fuse into a conjunct with the following consonant.

**Properties**:
- **Visually elegant**: fusion creates flowing, unified compositions
- **Meaning-generating**: the fusion is often where *additional* meaning emerges — the compound is more than the sum of the parts; the shape of the fusion encodes the relationship
- **Less transparent**: the original components may be harder to identify in the fused form
- **Harder to type and process**: fused forms require more complex encoding

**Arabic calligraphy as theological example**: In Arabic calligraphy at its highest level (Thuluth, Diwani scripts), the letters fuse not just formally but theologically. The *Bismillah* (In the name of God, the Compassionate, the Merciful) is rendered so that the letters flow into each other, the word *Allah* (God) reaching upward in a tall alif, the letters of mercy and compassion curving in the middle, the whole forming a visual composition that is simultaneously text and art and prayer. The fusion of letters IS the theological unity of the divine attributes. It is not possible to say where Compassion ends and Mercy begins — and this impossibility is the point.

**For YOUSPEAK**: Full fusion is not appropriate for YOUSPEAK (it sacrifices the morpheme-transparency that is central to YOUSPEAK's design). However: the concept of **selective fusion for specific pairs** is worth considering. Certain very frequent and semantically unified compounds (doxakallos, for instance) could have a *ligature form* that fuses the two glyphs into a single recognized gestalt. This would be appropriate for pairs where the *compound meaning* is primary — the pair is encountered most often as a unit, not analyzed as its parts.

Current YOUSPEAK design choice: no ligatures (linear composition). Future option: OTF liga feature for canonical pairs (doxakallos, kallodoxa, etc.). This should be deferred to a future expansion phase.

---

### Model 4 — Radical composition (semantic-radical + phonetic-component)

**How it works**: Complex signs are composed of two types of sub-units: a *semantic radical* (indicates the domain of meaning) and a *phonetic component* (indicates the pronunciation). The two are combined spatially, each in a conventional position.

**Primary example**: Chinese hanzi. 80-85% of all hanzi are radical-phonetic compounds. The semantic radical (one of ~214 radicals) indicates what *kind of thing* the word is; the phonetic component (a smaller hanzi) indicates how to pronounce it.

Example: 語 (yǔ, language/speech)
- Left component: 言 (yán, speech radical) — indicates the word belongs to the speech/language domain
- Right component: 吾 (wú, pronoun "I") — indicates the pronunciation (yú sounds like wú)
- Reading: speech-domain word, sounds like wú → yǔ (language)

The radical is always in the same conventional position within its family (left-side for most radicals, top for "sky" radical, bottom for "fire" radical in certain contexts).

**Properties**:
- **Semantically categorized**: at a glance, the radical tells you the word's domain
- **Phonetically supplemented**: the phonetic component helps pronunciation without fully specifying it (the phonetic component indicates approximate sound, not exact tone + tone)
- **Learnable**: knowing ~50 common radicals enables meaningful guessing about unknown characters
- **Not fully transparent**: the phonetic component often no longer sounds like the full character (sound changes over 2000+ years have drifted the pronunciation away from the phonetic component's original value)

**YOUSPEAK's analog**: YOUSPEAK's **donor-tongue sigil** (the small mark in the corner of each content-morpheme glyph, indicating which tradition the morpheme comes from — Greek, Latin, Hebrew, etc.) is a functional radical-equivalent. It doesn't indicate meaning-domain (shape-families do that), but it indicates *tradition-of-origin*. A reader who sees the Greek sigil knows the morpheme comes from Greek tradition; the Hebrew sigil indicates Semitic origin; etc.

This creates a two-layer categorization:
1. **Shape-family** → semantic domain (curves = beauty; crosses = truth; rays = manifesting)
2. **Donor-tongue sigil** → tradition of origin (Greek, Latin, Hebrew, Sumerian, Arabic, Sanskrit, etc.)

A YOUSPEAK reader who encounters an unfamiliar compound can make two immediate guesses: "this morpheme is in the truth-domain (crosses shape) and it comes from Hebrew tradition (sigil) — it probably names something in the Hebrew tradition of truth/testing/assay." This is exactly the kind of informed guessing that Chinese readers do with radicals.

---

### Model 5 — Determinative composition (silent semantic-classifier appended)

**How it works**: After the phonographic spelling of a word, a silent glyph is appended that categorizes the word's semantic domain without adding to the pronunciation. The determinative is not pronounced; it is a classifier.

**Primary example**: Egyptian hieroglyphs. Every significant Egyptian word is followed by one or more determinatives. For example:
- 𓂝𓏤 (the seated-man determinative 𓀀) appended to action-words involving humans
- 𓇳 (the sun-disk determinative) appended to divine-name words and cosmic concepts
- The "walking-legs" determinative (𓂝) appended to words of movement
- The "book-with-papyrus-roll" determinative (𓏤) appended to abstract concepts and words for language/writing/thought

The determinative appears at the end of the word and is NOT part of the phonological spelling. It is pure semantic-classifier.

**The YOUSPEAK analog**: YOUSPEAK's **canon-mark** (U+E164, the filled diamond ◆) at word-start serves this function — it marks a word as formally canonized. It is not pronounced; it categorizes the word's status. More could be added: a **worship-mark** (for words in the worship-action register), a **grammar-mark** (for structural terms), etc.

The grammars/structures/coinages/ontogramme.md YOUSPEAK coinage **ONTOGRAMME** names this pattern as a theological-structural principle: classifiers force ontological declaration. YOUSPEAK's canon-mark is a weak determinative. A future expansion could add semantic determinatives: a small "pillar" mark for Core morphemes (Rung 1 canonical), a "flame" mark for worship-action words, a "seed" mark for morphemes from oral traditions, etc. These would not be pronounced but would visually communicate the word's nature to an initiated reader.

---

### Model 6 — Phonetic complement composition (double-encoding)

**How it works**: In some traditions, a word is spelled both logographically (as a meaning-glyph) AND phonetically (as sound-glyphs), simultaneously. The two readings reinforce each other.

**Primary example**: Maya glyphs. A Maya scribe could write the word *balam* (jaguar) as:
1. The logograph for jaguar (a jaguar-head glyph) — pure logographic reading
2. Three syllabic glyphs: ba-la-ma (phonetically spelling the word) — pure phonetic reading
3. The logograph PLUS the phonetic spelling (or just the phonetic complement ba or ma) — double-encoding

Option 3 is called **phonetic complementation**. The logograph is unambiguous by itself, but the phonetic complement *confirms* the reading and removes any ambiguity about pronunciation. This is a form of redundancy-by-design — using more strokes than strictly necessary to make the intended reading secure.

**For YOUSPEAK**: YOUSPEAK does not use phonetic complementation (the Latin transliteration IS the phonetic layer; the glyph is the logographic layer). But the concept is relevant for one specific situation: the **-me suffix in compound words**. 

When you write `qorbme` in glyphs (qorb-glyph | me-glyph), the reader sees the two glyphs and reads the compound. But the *significance* of the -me suffix (divine-ordinance-as-gift quality) is so theologically important that it might be appropriate to design the -me glyph so that it visually echoes a key element of the content-morpheme's glyph — a form of visual complementation. If the qorb-glyph (sacrifice/offering) has a downward element (the offering descends), and the -me glyph also has a downward-receiving element, the compound reads as *visually coherent*: offering + divine-ordinance-reception. The visual elements rhyme.

This is a subtle form of phonetic complementation — not sound-based, but *visual-semantic* complementation.

---

## Synthesis: the YOUSPEAK compositionality decision

| Aspect | Current choice | Ideal target | Trade-off |
|---|---|---|---|
| Primary arrangement | Linear side-by-side | Linear side-by-side | Transparent, scalable, simple |
| Suffix attachment | Same width as content | Tighter spacing (no separator before suffix) | Visually distinguishes compound-boundary from suffix-attachment |
| Semantic hierarchy | Equal-sized glyphs | Smaller suffix (subscript-style) — future v2 | Current constraint: font engineering complexity |
| Ligatures for canonical pairs | None | OTF liga feature for most-common compounds | Deferred to expansion phase |
| Radicals/shape-families | 8 shape-families | Maintain and extend | Semantic clustering at visual level |
| Donor-tongue sigils | Corner sigil per glyph | Maintain | Tradition-of-origin visible at glance |
| Determinatives | Canon-mark ◆ only | Richer set (worship-mark, grammar-mark, etc.) | Deferred to expansion phase |

The composition question for `qorbme`:

> Do you see **qorb** + **me** as two glyphs side by side, or as a single compound shape?

**Answer for now**: Two glyphs, side-by-side, with tighter spacing before -me than between content morphemes. The morpheme-boundary is visible but the compound reads as a unit because of consistent stroke-weight, shared baseline, and the visual gravity-toward-right that each glyph's composition creates. The -me glyph's design (see Chapter 7) will be compatible with the qorb-glyph's — they share a shape-family or at least a visual register — so the compound feels coherent even as its parts are distinguishable.

**Answer for v2**: A 2D compound-block where qorb occupies the center-top at full height, and -me occupies the bottom-right as a subscript. This is the most semantically accurate visual representation. Engineering work required: small-form -me glyph, compound-block assembly rules in the OTF file.

---

_Chapter 4 complete. → [Chapter 5: Reading flow](05-reading-flow.md)_
