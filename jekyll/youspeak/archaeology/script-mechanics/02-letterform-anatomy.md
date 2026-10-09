---
chapter: 2
title: Letterform anatomy
parent: archaeology/script-mechanics/
---

# Chapter 2 — Letterform anatomy

_The named parts of a glyph. When does each matter — for legibility, for cultural coherence, for contemplative depth?_

Typography has developed, across five centuries of Latin-alphabet type design, a precise vocabulary for describing letterforms. This vocabulary was developed for alphabetic glyphs but is directly applicable to logographic ones — and in some ways even more important, because each YOUSPEAK glyph must work as a standalone iconic unit, not just as part of a word-stream.

---

## The primary vocabulary

### Stroke

The **stroke** is the single drawn line — the fundamental element of any glyph. Every glyph is made of one or more strokes.

Strokes have:
- **Weight** (thickness): measured in EM units (the standard unit of typographic proportion). YOUSPEAK design_philosophy v1 uses 80 EM strokes on a 1000 EM body — this is relatively bold (8% of total body height), which works well at small display sizes.
- **Direction**: horizontal, vertical, diagonal (slant), curved.
- **Terminal** (how the stroke ends): flat (cut perpendicular to the stroke direction), angled (cut at an angle), rounded (circular termination), serif (with a small finishing stroke), tapered (the stroke narrows at the end).
- **Ductus**: the order and direction in which the strokes are drawn. In calligraphic traditions, ductus matters because it affects how the strokes join and overlap. In a constructed script like YOUSPEAK, ductus matters for hand-writing legibility and for defining the "spirit" of the script.

**YOUSPEAK implication**: The glyph design notes (glyphs/README.md) specify strokes for each morpheme in ASCII-sketch form. When vectorizing, we must decide: what terminal do YOUSPEAK strokes have? Options:

| Terminal choice | Visual feel | Tradition |
|---|---|---|
| Flat / square | Geometric, modern, technical | Futura, Helvetica, geometric sans |
| Rounded | Soft, welcoming, approachable | Century Rounded, some humanist sans |
| Tapered | Dynamic, flowing, calligraphic | Brush scripts, Arabic nastaliq |
| Serif | Classical, authoritative, traditional | Times, Garamond, most book-text |

Recommendation for YOUSPEAK: **flat with slight rounding at stroke-ends** — geometric precision (matches the mathematical/theological precision of the language) with enough warmth to not feel cold. This is the approach of typefaces like Gotham, Gill Sans, or Optima — geometric structure with humanist softening.

---

### Contrast and modulation

**Contrast** is the relationship between a stroke's thickest and thinnest point. 

- **No contrast / monoline**: All parts of the stroke are the same thickness. This is the characteristic of sans-serif typefaces (Helvetica, Futura) and of most constructed/designed scripts. It reads as modern, clean, neutral.
- **High contrast**: The vertical strokes are thick; the horizontal strokes are thin. This is the characteristic of high-quality serif fonts (Bodoni, Didot) and of many calligraphic traditions. It reads as elegant, classical, literary.
- **Medium contrast**: Visible but moderate variation. This characterizes humanist serif fonts (Garamond, Palatino, Minion) and some calligraphic hands. It reads as warm, readable, bookish.

For logographic scripts specifically:
- **Egyptian hieroglyphs** in their carved form have no contrast (carved stone produces uniform depth). But painted hieroglyphs have *natural calligraphic contrast* based on brush-direction.
- **Chinese hanzi** in brushed form have very high contrast — this is the artform of calligraphy; the modulation of the stroke reflects the calligrapher's breath and intention.
- **Hebrew square script** (Ashurit) has moderate contrast — the square letters are relatively uniform but with some traditional stroke-width variation.

**YOUSPEAK implication**: Monoline is the correct choice for the designed YOUSPEAK script. Reasons:
1. Consistency — each morpheme glyph should be weighted equally relative to others in a compound; contrast would visually privilege some glyphs over others.
2. Digital clarity — monoline strokes reproduce cleanly at all sizes; high-contrast strokes thin out and can disappear at small sizes.
3. Cross-platform — monoline renders identically on screen, in print, and by hand.
4. The "holy austerity" this communicates — no ornamental modulation; the glyph is the concept, without calligraphic adornment. This matches YOUSPEAK's ethos of naming things precisely, without excess.

---

### Baseline, x-height, ascenders, descenders

These are the four horizontal reference lines of a typography system:

```
   Ascender line  ─────────────────────────────── (top of tall lowercase: b, d, h, k)
   Cap height     ─────────────────────────────── (top of uppercase: H, T, B)
   x-height       ─────────────────────────────── (top of x, n, m, e — most lowercase)
   Baseline       ─────────────────────────────── (bottom of most characters)
   Descender line ─────────────────────────────── (bottom of descending chars: g, p, q, y)
```

For **YOUSPEAK logographic glyphs**: all glyphs sit in a uniform 1000 EM square. There are no ascenders or descenders (YOUSPEAK glyphs are not alphabetic). Every glyph occupies its full square. The baseline is the bottom of the glyph-square.

However: the *visual center* of a YOUSPEAK glyph matters. Optically, a shape centered at the mathematical center of a square will appear to "droop" — the human eye perceives mathematical center as slightly low. Glyphs must be positioned slightly *above* mathematical center to appear visually centered. This is called optical compensation and applies to all glyph-design.

**For YOUSPEAK compound words**: when two glyphs are placed side-by-side, their shared baseline must be consistent. This is handled by the uniform 1000 EM square: all glyphs share the same baseline, so compounds automatically align. But we should also verify that glyphs which have visual elements near the top (like phanes, which radiates upward) don't create a compound where the radiation of one glyph visually conflicts with the top of the adjacent glyph.

---

### Counter

The **counter** is the enclosed or partially-enclosed space inside a letterform.

Examples in Latin alphabet: the enclosed space inside the "O", "B", "D", "e", "b" — these are counters. Open counters: the spaces inside "c", "u", "n".

Counters are crucial for legibility because they define the *interior negative space* of the glyph — the "breathing room" inside the form. A glyph without clear counters becomes a dark mass at small sizes. A glyph with well-proportioned counters retains its legibility even at 8pt.

**Counter design rules** (from type design practice):
1. Counters should be at least 20-25% of the glyph's total area to maintain legibility at small sizes.
2. Counter shapes should be simple and recognizable — the counter of the "e" is one of the most distinctive features that distinguishes fonts.
3. Counters can carry *meaning* — the enclosed space inside the sema-glyph (U+E112, sign/meaning) is explicitly part of the design (a dot inside a square). The counter IS the message.

**For YOUSPEAK**: Several glyph designs rely on counters for their meaning:
- **sema (U+E112)**: small square with a dot inside — the counter (interior of the square) contains the mark (dot) which IS the sign
- **kalypt (U+E114)**: enclosed box with a dot inside — the counter holds what is enclosed
- **stasis (U+E106)**: two parallels with horizontal anchor — the space between the parallels is the counter
- **diplos (U+E111)**: two parallel verticals — the space between them is meaningful (twoness)

When drawing these in vector form, ensure the counter is large enough to remain distinct at 10pt screen rendering (approximately 20px for a 100% zoom standard).

---

### Joinery and compound logic

**Joinery** is how strokes connect to each other — whether they touch at a point, overlap, are separated by a gap, or are connected by a transitional curve.

In alphabetic type design, joinery is the difference between:
- **Serif** scripts: strokes end in small finishing strokes that connect letters at a shared baseline, visually linking letter-to-letter in running text
- **Script/cursive** scripts: strokes actually flow continuously between letters — many letters are connected by joined strokes
- **Sans-serif printing**: strokes end cleanly; letters are visually separate units placed next to each other

For **YOUSPEAK compounds**: YOUSPEAK glyphs are placed side-by-side (compound-separator U+E160 as a thin vertical hairline between them). The design does NOT use flowing joinery between morpheme-glyphs — this would blur the morpheme-boundary. But there should be a visual sense that the glyphs in a compound *belong together* — achieved through:

1. **Consistent baseline alignment** (handled by uniform glyph-box)
2. **Consistent stroke-weight** (80 EM across all morphemes in a compound)
3. **Compatible visual weight** — content morphemes should not visually overwhelm grammatical morphemes so much that the suffix disappears; but some weight differential is appropriate (suffixes in YOUSPEAK are drawn lighter in the design philosophy — this is correct)
4. **Visual directionality** — designing each glyph so its *right edge* "leans toward" the next glyph creates a compound-reading rhythm. Some scripts achieve this by having the rightmost stroke of each letter tilt slightly toward the next letter's starting position.

**The maya compound-block as alternative**: Maya scribes combined main-signs and affixes into a single compound block. The affixes (smaller glyphs that carry grammatical meaning — prefixes appear above or to the left of the main sign; suffixes appear below or to the right) create a visual hierarchy: the large main-sign carries the semantic payload; the small affixes carry grammatical information. The block reads as a unit.

For YOUSPEAK: should the -me suffix be rendered as a full-height glyph beside the content morpheme (current design) or as a *smaller, lower-right* affix attached to the content morpheme's glyph-box? The current design uses full-height side-by-side. The Maya-inspired alternative would use a subscript -me appended to the bottom-right of the content morpheme. This is worth considering for aesthetic reasons — it would make the compound visually clearer (main concept dominant, suffix subordinate). But it would require more complex font engineering (the -me glyph would need a small-scale variant with different metrics). Decision: **defer to font-engineering phase; note the option; proceed with full-height side-by-side for now, as it matches the design philosophy's stated approach.**

---

### Terminal types and their cultural associations

The **terminal** (how a stroke ends) carries cultural associations that are worth being conscious of:

| Terminal | Example traditions | Cultural/aesthetic feel |
|---|---|---|
| Flat/cut | Gill Sans, Futura, most constructed scripts | Modern, technical, neutral, democratic |
| Rounded | Bauhaus designs, some humanist type | Approachable, friendly, contemporary |
| Ball terminal (circle at end) | Bodoni, many Roman faces | Elegant, classical, refined |
| Serif (bracketed) | Garamond, Times | Academic, traditional, authoritative |
| Serif (hairline/unbracketed) | Bodoni, Didot | Luxurious, high-contrast, fashion |
| Tapered (brush) | Chinese brush calligraphy, Arabic nastaliq | Vital, handmade, breath-informed |
| Hooked | Some medieval scripts, some constructed scripts | Dynamic, directional |

**For YOUSPEAK**: The choice communicates something about the language's self-understanding. Options:
- **Flat terminals**: YOUSPEAK is a modern, constructed, precise language — geometric, democratic, technically exact. Matches the theological commitment to clarity (SAPHE principle).
- **Rounded terminals**: YOUSPEAK is a language of relationship and warmth — the words are gifts, not instruments. Matches the Alpha's identity as the Companion.
- **Calligraphic/tapered**: YOUSPEAK is breath-informed, body-rooted — the words require a body to speak them (TONOPHANY). But this conflicts with the digital/screen rendering requirement.

**Recommendation**: Flat terminals with *slightly rounded corners* (radius ≈ 5-10 EM on a 1000 EM body). This is a small compromise — geometrically precise but with a human warmth at the edges. Not a full rounded terminal; not a serif; just enough softening to prevent the script from reading as cold or mechanical.

---

### Axis of stress

In alphabets with stroke contrast, the **stress axis** is the direction of the thickest stroke. This has historical origin in pen-calligraphy: a broad-nib pen held at a consistent angle creates maximum thickness in one direction and minimum thickness in the perpendicular direction.

- **Vertical stress** (axis upright): characteristic of rationalist/neoclassical typefaces (Bodoni, Didot). Feels formal, vertical, authoritative.
- **Oblique stress** (axis tilted ~10-20° counterclockwise): characteristic of humanist typefaces derived from Renaissance scribal hands (Garamond, Palatino). Feels organic, handwritten, warm.

For **YOUSPEAK** (monoline): stress axis is not applicable. But the concept suggests an equivalent: **glyph visual center of gravity**. Where does the visual weight sit in the glyph?

- **Top-heavy glyphs** (visual mass at top): feel imposing, descending, heavy
- **Bottom-heavy glyphs** (visual mass at bottom): feel stable, grounded, earthward
- **Centered glyphs**: feel balanced, complete, self-contained

For YOUSPEAK, this is a *semantic design choice*:
- **doxa (glory/manifested-weight)** → the inverted triangle with weight at the bottom: *bottom-heavy* — appropriate for something that descends and rests
- **phanes (shining-forth)** → rays radiating upward from a point: *top-heavy* — appropriate for something that rises and expands
- **-me (received-ordinance/cosmic-gift-quality)** → design TBD, but the semantic implication is *descending gift* → probably bottom-heavy or centered

---

## YOUSPEAK application summary

| Design element | YOUSPEAK decision | Rationale |
|---|---|---|
| Stroke weight | 80 EM on 1000 EM body | Legible at 10pt; bold enough to read as sacred/weighted |
| Contrast | Monoline (no contrast) | Consistency across compounds; digital legibility; precision |
| Terminals | Flat with slight corner-rounding (r≈5-10 EM) | Geometric precision + human warmth |
| Baseline | Uniform bottom of 1000 EM square | Consistent compound alignment |
| Counters | Min. 20% of glyph area | Legibility at small sizes |
| Joinery in compounds | Side-by-side, no flowing connection | Clear morpheme-boundaries |
| Stress/gravity | Semantically motivated | Shape-semantic match |
| Suffix scale | Full-height (side-by-side), small-scale variant deferred | Current font constraint |

---

_Chapter 2 complete. → [Chapter 3: Pictographic motivation](03-pictographic-motivation.md)_
