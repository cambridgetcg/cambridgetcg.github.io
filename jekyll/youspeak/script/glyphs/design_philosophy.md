---
title: YOUSPEAK Glyph Design Philosophy (v1)
opened: 2026-04-24
context: engineered after v0 delivered functional glyphs; v1 optimises for human legibility + LLM LoRA fine-tuning compatibility
supersedes: the ad-hoc design notes in glyphs/README.md (kept as v0 reference)
---

# Glyph Design Philosophy — v1

_What a glyph is, what it must carry, why each design decision is what it is. This document is the specification any font artist works from when refining the glyphs for canonical-quality production._

---

## The eight dimensions of a YOUSPEAK word

Every canonical YOUSPEAK word carries eight dimensions of meaning:

1. **Identity** — which morpheme(s) compose the word
2. **Donor tongue** — which linguistic tradition each morpheme comes from (Greek / Latin / Hebrew / Arabic / Sanskrit / English / Egyptian / PIE)
3. **Semantic domain** — which conceptual territory the morpheme lives in (beauty / truth / ache / appearing / time / form / relation / space / structure / act / wonder / testing / deception)
4. **Morpheme class** — content morpheme / grammatical prefix / grammatical suffix / structural mark
5. **Compound position** — whether this morpheme is head, modifier, or standalone in the compound
6. **Canon status** — canon (weighted ≥7.5) / refine (5.0–7.4) / archive (<5.0)
7. **Diplosemy membership** — whether the word has an engineered pair-sibling (Anastrophance, etc.)
8. **Axis strength** — the 5-axis weighted assessment score

A glyph that encodes all eight dimensions would be dense but legible if the encoding is principled. The challenge is orchestrating the encoding without clutter.

## The two audiences and their opposing pull

Every glyph serves two readers:

**Humans** want feature-richness. The more the glyph visually reveals (donor-tongue lineage, semantic family resemblance, morpheme class), the faster learning proceeds and the deeper comprehension goes. Hangul's design — where the glyph's shape *encodes articulatory phonology* — is the canonical case of feature-rich success.

**LLMs (especially fine-tuned via LoRA)** want tokenizer-stability. Each morpheme should map to ONE token. Splitting a morpheme into multiple visual-feature-tokens (one for donor-mark, one for class-mark, one for core-shape) multiplies the vocabulary by 3-5x, scatters the learning signal across too many tokens, and destroys the semantic-density benefit that motivated the whole YOUSPEAK project.

**These pull in opposite directions.** More visual features → richer for humans, catastrophic for naive tokenization.

## The resolution — visual features in the glyph, one codepoint per morpheme

The design decision that unlocks both audiences:

> **Every feature-encoding lives in the glyph's visual composition. The Unicode codepoint stays one-per-morpheme. The glyph is visually rich; the tokenization is atomic.**

Concretely:

- A YOUSPEAK glyph like `doxa` (U+E100) is ONE codepoint, ONE token (after tokenizer augmentation), ONE character in file systems and data pipelines
- But the VISUAL RENDERING of that codepoint carries multiple feature-marks: a Greek-tongue sigil, a domain-family shape, a content-class positioning
- The font file does the feature-compositing; the text-processing pipeline doesn't see it

This preserves:
- **Token efficiency**: `doxakallos` stays 2 tokens (not 8)
- **LoRA fine-tuning viability**: training signal concentrated per-morpheme
- **Human readability**: each glyph carries rich visual structure
- **Vision-model groundedness**: multimodal LLMs see the feature-rich images and learn richer representations

## The feature-encoding scheme

A YOUSPEAK v1 glyph occupies a 1000×1000 EM square with three concentric zones:

```
       1000 EM wide
  ┌────────────────────────┐ 
  │  ◉    MAIN BODY    ●   │ ← top zone (100 EM): donor-tongue sigil (top-left)
  │     (iconographic       │   and optional canon/pair mark (top-right)
  │      shape family)      │
  │                         │
  │                         │
  │                         │   ← mid zone (750 EM): the iconographic shape
  │                         │     family-conformant per semantic domain
  │                         │
  │                       ▷ │ ← bottom zone (100 EM): morpheme-class mark
  └────────────────────────┘    (bottom-right; absent for content morphemes)
       1000 EM tall
```

### Zone 1 — Top-left: donor-tongue sigil (80×80 EM)

A small, distinct mark indicating which tradition the morpheme was drawn from:

| Tongue | Sigil | Rationale |
|---|---|---|
| Greek | ● filled dot | minimal, classical (Greeks named the first glyphs; the dot is the 'alpha' of marks) |
| Latin | ■ filled square | Roman orthogonality |
| Hebrew | ▽ downward triangle | divine descent (YHWH kabod direction) |
| Arabic | ○ open circle | the One, the unbounded (tawhid) |
| Sanskrit | ⋮ three vertical dots | Trimurti / three-gunas |
| English | (no sigil) | default; absence-is-English |
| Egyptian | □ empty square | sacred geometry (Ma'at's precision) |
| PIE (Proto-Indo-European) | ≡ three horizontal lines | grandmother root — the base tradition from which others branched |

For hybrid morphemes (e.g., *arti* draws from Latin *artis*, Greek *arete/artios*, and PIE *\*h₂ert-*), the sigil marks the **primary donor** with a secondary indicator in the stroke-pattern.

### Zone 2 — Top-right: canon/pair mark (100×100 EM region)

Reserved for word-level metadata. Because this is a morpheme-glyph zone not a word-glyph zone, the markers are applied by the transliterator at **word boundaries**, not per-glyph. They are:

- **◆ canon mark** — appears above a word that is in the Canon (filled diamond)
- **↔ pair mark** — appears above a word that has a diplosemic-sibling
- **◇ refine mark** — empty diamond for words held in Forge at refine-verdict

These are rendered by the transliterator as additional glyphs in a combining-mark codepoint range (U+E165+), positioned above the word. They don't live in the base-morpheme glyph.

### Zone 3 — Main body (800×800 EM)

The iconographic core. Shape-language is **constrained by semantic domain** — this is the key v1 innovation:

| Domain | Shape Language | Why |
|---|---|---|
| Beauty | curves opening upward (wings, petals) | beauty *draws forth*; opening-upward evokes the beheld summoning the beholder |
| Rightness / truth | balanced crosses, symmetric axes | truth is structurally balanced; symmetry is its visual form |
| Appearing / light | radiating lines from a central point | shining-forth has exactly this shape in every tradition |
| Ache / pressure | bent lines, stress-marked joints | ache IS structural bend under load; the glyph shows the bend |
| Act / event | directional wedges (arrows) | events are directional; the wedge has an unmistakable arrow-semantics |
| Relation / between | two shapes interacting | between-ness needs two forms; a single form cannot express relation |
| Space / enclosure | closed forms with clear interior | enclosure has a topology |
| Time / process | spirals, flowing forms | time moves; spirals are temporally-directional |
| Wonder / recognition | eye-like, symmetric | recognition is visual; the eye is the recognition-organ |
| Testing / forging | vessel shapes (cup, crucible) | testing assays in a container |
| Deception / illusion | crossed or doubled forms | deception shows one thing while being another |
| Structure / quality (meta) | centered / contained forms | structure-itself has no motion but has containment |

A new reader, after learning the shape-family-to-domain mapping, can often guess a glyph's domain on first sight. This is the **featural payoff** Hangul also achieves.

### Zone 4 — Bottom-right: morpheme-class mark (60×60 EM)

- **Content morpheme**: (no mark) — the default; majority of glyphs
- **Grammatical prefix**: ◁ (small left-pointing triangle; "begins")
- **Grammatical suffix**: ▷ (small right-pointing triangle; "ends")
- **Structural mark**: ◆ (small diamond; marks a mark-of-marks)

### Zone 5 — Word-level markers (applied by transliterator)

Rendered ABOVE the word as superscript-combining-marks. Not part of individual glyphs.

- **Canon mark** — ◆ above canonical words
- **Pair mark** — ↔ above Anastrophance-members
- **Diplosemic-compound indicator** — a subtle overline spanning multi-morpheme diplosemic words

## Stroke conventions (for production font)

For the font-artist working from these specs:

- **EM square**: 1000 units (standard)
- **Main body**: 200–850 y-axis (650 EM tall); 150–850 x-axis (700 EM wide)
- **Stroke width**: 80 units (heavier than v0's 60; better legibility at 10-12pt)
- **Optical thickness correction**: diagonals thickened to 90 units (correcting for perceived thinness at 45°)
- **Joints**: mitered at 90° intersections; rounded at ≤60° to avoid ink-traps
- **Dot diameter**: 100 units (larger than v0's 80; readable at body text)
- **Sigil position** (top-left donor mark): 50 EM from left, 900 EM from bottom (i.e., top-left quadrant)
- **Class-mark position** (bottom-right): 850 EM from left, 100 EM from bottom
- **Advance width**: 1000 EM (square-bodied); consistent across all glyphs so compound-words align vertically

## Side-bearings and compound rendering

Each glyph has:
- **LSB (left side-bearing)**: 100 EM
- **RSB (right side-bearing)**: 100 EM
- **Effective body width**: 800 EM

In a compound word, adjacent glyphs separated by their natural side-bearings give a visible gap (200 EM = 20% of glyph-width). This gap is the **morpheme boundary indicator** — no explicit separator needed.

For very-long compounds (e.g., `anagnoristasis` = 3 glyphs), OpenType *contextual alternates* could compress the side-bearings slightly to fit. Deferred for v2.

## Canonical status markers — placement

A canonical word like `doxakallos` is rendered as:

```
      ◆     ← canon mark (combining character above word-center)
    ___ ___
   |   |   |   ← two glyphs composing the word
   |dox|kal|
   |__a|los|
```

A diplosemic-pair word like `doxakallos` (which has `kallodoxa` as Anastrophance-sibling) gets an additional above-mark:

```
    ↔ ◆      ← pair arrow + canon mark
    ___ ___
   |dox|kal|
   |__a|los|
```

These above-marks are rendered by the transliterator when it recognises the word and its status. They live in the structural-mark codepoint range (U+E165+) and are inserted as additional codepoints in the rendered output.

## LoRA fine-tuning optimisations

Every design choice above was made with LLM fine-tuning in mind. Concretely:

### One codepoint per morpheme → one token per morpheme

After tokenizer augmentation (see `script/llm/lora/tokenizer.py`), every YOUSPEAK morpheme is added to the tokenizer's vocabulary as a single special token. This means:

- `doxakallos` tokenises as 2 tokens (was 3-5 as raw Latin-compound)
- `synophora` tokenises as 2 tokens
- The training signal per-morpheme is concentrated (not scattered across sub-word pieces)
- LoRA learns a small, focused adaptation

### Visual-feature information available for vision-enabled models

Multimodal models (Claude with vision, GPT-4o, Gemini) can see glyph images and learn from them. The feature-encoding means:

- The donor-tongue sigil gives the model a visual prior on etymology
- The shape-family gives a prior on domain
- The class-mark gives a prior on grammatical role
- A vision-LoRA can learn to generate appropriate glyphs given textual description

### Dataset construction (see `script/llm/lora/dataset.py`)

Training pairs are synthesised from existing YOUSPEAK artifacts:

1. **Canon entries** → (word, meaning) pairs
2. **Experiments** → (gap, coinage, score) triples
3. **Forge documents** → (concept, candidates, selection-narrative)
4. **Archaeology** → (tongue, semantic-field, donor-morphemes)
5. **Diplosemy exemplars** → (pair, correlation-score, use-case)

These feed a LoRA adapter that learns:
- What YOUSPEAK words mean (canon entries)
- How to forge new coinages (experiment patterns)
- How to assess coinages (5-axis rubric application)
- How to compose diplosemic pairs (Anastrophance, etc.)

### Training-target layers

LoRA applies to:
- **Embedding matrix** (for new token embeddings of YOUSPEAK morphemes)
- **Attention layers of first 4 transformer blocks** (for morpheme-level semantics)
- **Attention + MLP of last 4 blocks** (for YOUSPEAK-native generation)

Rank: 32. Alpha: 32. Typical parameter count: ~50M for Llama-3-8B. Trainable on Apple Silicon via MLX.

## The why — summarised

Every design choice resolves a concrete tension:

1. **Feature-encoding in shape, not codepoints** → serves both human readers (rich visual cues) and LLMs (atomic tokenization)
2. **Shape-family by semantic domain** → helps human learning via family resemblance; helps vision-LLMs learn semantic priors
3. **Donor-tongue sigil in corner** → makes etymology visible at glance; doesn't dominate the main iconography
4. **Class mark as small bottom-right element** → grammatical role visible but not intrusive
5. **Canon/pair markers as above-word additions** → word-level metadata doesn't clutter individual glyphs; rendered by tooling
6. **Stroke weight 80 EM** → legible at body text size (10-12pt); heavier than v0's 60 EM
7. **1000 EM square body, consistent advance-width** → compound words align visually; font metrics predictable
8. **One codepoint per morpheme** → LoRA training signal per-morpheme is atomic; no tokenizer fragmentation

## What v1 changes from v0

- All strokes heavier (60 → 80 EM)
- Added donor-tongue sigils (top-left) to all content morphemes
- Added class-marks (bottom-right) to grammatical morphemes
- Redesigned shape-families to conform per semantic domain (curves for beauty, crosses for truth, rays for appearing, etc.)
- Added word-level markers (canon ◆, pair ↔) via transliterator
- Established consistent metrics (advance-width, side-bearings, baseline)
- Font file: `script/fonts/youspeak-v1.otf` (v0 kept as `youspeak.otf` for backward-compat)

## What is still deferred

- **Compound-position markers** (head vs modifier) — could add stroke-weight variation; defer until reader-feedback shows it's needed
- **Axis-strength indicators** (5-axis scoring visibility) — defer to word-metadata rendering rather than glyph encoding
- **Variant forms** (formal/cursive/liturgical registers) — OpenType stylistic alternates; future expansion
- **Ligatures for frequent compounds** — the pair `doxakallos` could have a ligature-form; defer
- **Directionality and tone marks** — scale-up for Cadences/ organ (ASCENT Level 3) when we reach that work

---

_Design philosophy v1 — 2026-04-24. This document is the brief the font artist works from. Implementation in `glyph_specs_v1.py`; font produced at `fonts/youspeak-v1.otf`._
