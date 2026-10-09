---
chapter: glyph design notes
opened: 2026-04-24
status: design-notes phase (no vector-font yet); each morpheme has its iconographic rationale recorded for the font-artist who will eventually draw them
---

# Glyph Design Notes

_Where each YOUSPEAK morpheme receives its visible form. Each glyph design should carry the morpheme's meaning iconographically, not arbitrarily. These notes describe the design-intent and an ASCII sketch; the actual vector-font file is built in the next phase using these notes as the specification._

---

## Design principles

1. **Iconographic where possible** — the glyph's shape visually suggests the morpheme's meaning. *doxa* carries light-weight; its glyph should suggest radiance-plus-gravity.
2. **Geometric and constructible** — glyphs use a small set of primitive strokes (horizontal, vertical, diagonal, circle-arc) so they can be drawn by hand and vectorized consistently.
3. **Visually distinct** — no two morpheme-glyphs should be confusable at small display size.
4. **Compound-compatible** — adjacent glyphs must read cleanly as a compound without visual collision; each glyph has a defined box-width (1em square is the default) and interior negative-space.
5. **Register-stable** — the glyph looks right in liturgical (large, ornate), technical (small, rendered in code), and cursive (handwritten) registers.

## The core set (design notes)

Each entry: morpheme → design rationale → ASCII sketch. ASCII sketches are placeholder; actual glyphs will be smoother in vector form.

### δόξα / doxa (U+E100) — glory, manifested-weight

**Design:** a downward-pointing triangle with a horizontal bar through it. The triangle evokes *weight/gravity*; the horizontal bar evokes *manifestation/showing*. Together: weight-that-manifests, manifestation-that-weights.

```
  ____
  \  /
  _\/_
```

### κάλλος / kallos (U+E101) — beauty-substantive

**Design:** a vertical stroke flanked by two symmetrical curved strokes opening upward. The symmetry evokes *ordered-rightness*; the opening-upward evokes *beauty-as-drawing-forth*.

```
  \_|_/
    |
```

### ὀρθός / ortho (U+E102) — right, straight

**Design:** a simple vertical stroke crossed by a perpendicular horizontal at the top — the most literal "right-angle" glyph. The cross is at the top (not middle) to distinguish from a Latin "+" and evoke "rightness-made-high."

```
  __
  ||
  ||
  ||
```

### φαν- / phanes (U+E103) — appearing, shining-forth

**Design:** three diverging rays from a single point. Clearly suggests radiation/shining.

```
   \|/
    *
```

### ἄλγος / algia (U+E104) — structural ache

**Design:** a vertical stroke bent at the middle with a small mark at the bend-point. The bend evokes *stress under load*; the mark evokes *the ache's local signature*.

```
  |
  |
  \._
   `\
```

### ἀναγνώρισις / anagno (U+E105) — recognition-moment

**Design:** two parallel horizontal strokes connected by a vertical — an equals-sign with a vertical connector. The two parallels evoke *pattern-matching* (two sides that correspond); the connector evokes *the matching-event*.

```
  ====
   ||
  ====
```

### στάσις / stasis (U+E106) — standing-still

**Design:** two short vertical parallels (like Roman numeral II) with a horizontal anchor beneath. Evokes *held-stance*.

```
  | |
  |_|
```

### μετά / meta (U+E107) — after, complete-change

**Design:** a left-pointing arrow-like shape, or a wedge indicating direction of passage. Less static than most glyphs; carries motion.

```
  <--
   \_
```

### στροφή / strophe (U+E108) — turning

**Design:** a spiral — the clearest visual metaphor for turning. Drawn as a simple counterclockwise curl.

```
   _
  (_)
    \
```

### θαῦμα / thauma (U+E109) — wonder, marvel

**Design:** an eye-shape with a small mark at the pupil — evokes the wondering gaze.

```
   .
  (o)
```

### σύν / syn (U+E10A) — together-with

**Design:** two parallel diagonal strokes converging. Clearly suggests *joining*.

```
  \ /
   V
```

### φορά / phora (U+E10B) — carrying

**Design:** a horizontal line with an upward-bend at one end — a carrying-hand or shelf-bracket. Evokes support-from-below.

```
     /
  __/
```

### candor / cand (U+E10C) — luminous-warm-clear-white

**Design:** a circle with three short radiating strokes at the top — a sun-mark, but smaller and softer than phanes (whose radiation is three-ray sharp). Cand's radiation is *warm* and *contained*.

```
  \|/
  (O)
```

### δοκιμ- / dokim (U+E10D) — testing, assaying

**Design:** a crucible-shape — rounded vessel with an opening at the top, possibly with a small flame-mark above. Evokes metallurgical assay.

```
   ||
  \__/
```

### arti (U+E10E) — fitted, skilled-making

**Design:** a pentagon — five sides evoking *fittingness* (five-point symmetry is structurally harmonizing) and the five pre-domain qualities (truth/beauty/justice/skill/order) that artiance names the unity of.

```
   /\
  /  \
  \  /
   \/
```

### veri (U+E10F) — truth

**Design:** a simple vertical line with a centered horizontal crossbar that extends slightly beyond the vertical on both sides. The symmetry and balance evoke *truth*.

```
   |
  -|-
   |
```

### compler / compler (U+E110) — filling-together

**Design:** two half-circles facing each other, nearly-but-not-quite-meeting — evokes *mutual-filling*.

```
  ( )
  ) (
```

### διπλόος / diplos (U+E111) — twofold

**Design:** two parallel vertical strokes. Literal.

```
  | |
  | |
```

### σῆμα / sema (U+E112) — sign, meaning

**Design:** a small square with a dot at center — the abstract sign-glyph.

```
  .--.
  |. |
  `--'
```

### Other morphemes (condensed)

Design-notes for the remaining content and grammatical morphemes follow the same principles. Each gets its own design file as font-production proceeds:

- **anastro (U+E113)** — a clockwise-reverse spiral (mirror of strophē's spiral)
- **kalypt (U+E114)** — a closed box with a dot inside (enclosure)
- **haphe (U+E115)** — two fingertips touching (two short verticals meeting at the top)
- **allos (U+E116)** — a bifurcated Y shape (other-path)
- **parallax (U+E117)** — two parallel horizontal lines with a small offset arrow between them (the shift)
- **hypo (U+E118)** — a horizontal line with a vertical descending from it (under-beneath)
- **stix (U+E119)** — a single dot (the mark-of-stopping)
- **kairos (U+E11A)** — an hourglass (time-layer)
- **morphe (U+E11B)** — a closed geometric-irregular shape (form)
- **klimax (U+E11C)** — a small staircase (scale)
- **lanthes (U+E11D)** — a dashed outline (hidden-but-present)
- **sleight (U+E11E)** — two crossed diagonals (deception-skill)
- **seem (U+E11F)** — a lenticular shape (appearance-as-through-a-lens)

## Structural marks (U+E160+)

- **compound-separator (U+E160)** — a thin vertical hairline, rendered slightly shorter than full-height glyphs
- **reading-annotation open (U+E161)** — `⌜` corner bracket
- **reading-annotation close (U+E162)** — `⌟` corner bracket
- **diplosemic-pair indicator (U+E163)** — small double-arrow ↔ rendered above the pair
- **canon-mark (U+E164)** — small filled diamond ◆ at word start

## Grammatical-morpheme glyphs

Grammatical morphemes (-ance, -sis, -ma, etc.) are typographically lighter than content morphemes. They sit at lower visual weight to signal their functional role:

- **-ance (U+E142)** — a small hook shape
- **-mance (U+E143)** — hook + dot (varies from -ance)
- **-ence (U+E144)** — softer hook (variant of -ance)
- **-sis (U+E141)** — a small vertical with a terminal bar
- **-ma (U+E145)** — a small closed curl (result-of-action)
- **-iance (U+E146)** — hook with upward ray (luminous)
- **-escence (U+E147)** — open-ended hook (becoming)
- **a- privative (U+E140)** — a small circle with a slash (negation)
- **ana- (U+E149)** — upward-arrow (up, back)
- **en- (U+E14A)** — inward-pointing bracket (in, within)
- **com- (U+E14B)** — joining-mark (together)

## Production pipeline

When the font is built:

1. **Sketch** — hand-draw each glyph on graph paper following the design notes
2. **Digitize** — scan and vectorize (Illustrator, Figma, Glyphs, Inkscape)
3. **Metrify** — assign each glyph a standard cell-width (1em) with appropriate side-bearings
4. **Hint** — add TrueType hinting for clean rendering at small sizes
5. **Build** — compile OTF/TTF with codepoint mapping from `morphemes.json`
6. **Test** — render across platforms; verify mac-native, Linux, and web rendering
7. **Distribute** — ship as `youspeak.otf` in `script/fonts/`; install per-user on each Kingdom machine

---

_Design notes 2026-04-24. Vector-font production is the next phase; these notes are the specification._
