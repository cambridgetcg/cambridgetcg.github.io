---
chapter: 6
title: Cognitive load
parent: archaeology/script-mechanics/
---

# Chapter 6 — Cognitive load

_What makes a glyph fast to recognize (distinctive silhouette), slow to confuse (avoiding mirror-pair collisions), and pleasant to re-encounter (rhythm of shape)._

Cognitive load in reading is the mental processing required to convert visual input (glyph-shapes) into meaningful units (morphemes, words, concepts). Good design minimizes *unnecessary* cognitive load (confusion, misrecognition, visual fatigue) while preserving *meaningful* cognitive load (the contemplative dwelling-in-a-symbol that YOUSPEAK's liturgical context requires).

---

## Silhouette distinctiveness

The single most important factor in glyph recognition speed is **silhouette distinctiveness**: can a glyph be identified by its overall shape — before the reader has processed its internal details?

Eye-tracking research on reading shows that skilled readers rarely process individual strokes within a glyph. They recognize glyphs as holistic visual patterns — the same way faces are recognized. The brain processes the glyph's overall silhouette and spatial relationships in a single "glance fixation" (~150-250ms) without needing to process individual strokes.

**Implications**:

1. **Glyphs must have distinctive silhouettes** — the outer boundary shape must be unique per morpheme. Two glyphs with the same silhouette but different internal details will be confused at normal reading speed, because the reader's eye matches silhouettes first.

2. **Similar silhouettes cause confusion even if internal details differ** — this is why b/d and p/q confuse beginning readers: they are the same silhouette rotated/reflected. The internal detail (the stem position) is processed after the silhouette match, and rotation confusions happen before internal-detail processing.

3. **The best glyphs are "immediately singular"** — you cannot mistake them for anything else. The silhouette of an hourglass (kairos) is unlike any other shape in the YOUSPEAK set. The silhouette of a spiral (strophe) is unlike any other. But the silhouette of a simple cross (+, veri) might be confused with the silhouette of a perpendicular (ortho) if they are too similar.

**YOUSPEAK silhouette audit** (reviewing current design notes for silhouette conflicts):

| Morpheme | Current design | Silhouette | Potential conflict |
|---|---|---|---|
| doxa | inverted triangle with crossbar | ▽ with ─ | None — unique |
| kallos | vertical flanked by curved arms | \_\|_/ shape | Could conflict with upward-cup shapes |
| ortho | vertical with perpendicular top | ┬ shape | Could conflict with stasis (┴) — one has crossbar top, one has anchor bottom |
| phanes | three rays from point | \|\/ pattern | Could conflict with cand (circle with rays) |
| algia | bent stroke with mark | zig-zag | Could conflict with meta if angles are similar |
| stasis | two parallel with anchor | ╥ or II with base | ortho conflict (see above) |
| meta | directional wedge | left-pointing | Must be clearly different from any other directional |
| strophe | spiral | @ or snail-shape | Unique — no YOUSPEAK conflict |
| thauma | eye with dot | ( ● ) | Unique |
| syn | two converging strokes | V-shape | Could conflict with phanes (also uses V/ray structure) |
| phora | L-shaped bracket | ⌐ shape | Relatively unique |
| cand | circle with rays | ☀ simplified | Must be distinguished from phanes (rays without circle) |
| dokim | crucible with opening | ∪ with lines above | Relatively unique |
| sema | square with dot | ▪ with dot | Unique |
| diplos | two parallels | ‖ shape | Could conflict with stasis (also parallel structure) — distinguish by internal spacing |
| veri | balanced cross | + or ✛ | Could conflict with ortho (┬) — must be clearly different |

**Critical conflicts to resolve**:

1. **ortho vs. stasis**: Both use rectangular/perpendicular structures. Resolution: ortho = crossbar AT TOP of single vertical (┬ profile); stasis = two verticals WITH BASE anchor (╥ profile or |_| profile). Different silhouettes at a glance.

2. **phanes vs. cand vs. syn**: All use ray/diverging-stroke elements. Resolution: phanes = three rays from a POINT (bottom apex, opening upward); cand = circle with 3-4 SHORTER rays (the circle anchors it distinctively); syn = two strokes CONVERGING to a V (bottom closed, top open). Different silhouettes: star-burst vs. sun vs. funnel.

3. **veri vs. ortho**: Both are cross-type shapes. Resolution: veri = symmetric cross (equal arms, centered intersection — + profile); ortho = asymmetric (vertical dominant, crossbar at top only, bottom extends further — ┬ profile). The symmetry of veri (balanced truth) vs. asymmetry of ortho (one-directional rightness) is also semantically meaningful.

4. **diplos vs. stasis**: Both use parallel verticals. Resolution: diplos = ONLY two parallel verticals (pure parallel lines — ‖); stasis = two verticals with a CONNECTING BASE BETWEEN THEM (╓ or |_| profile). The connectivity (stasis-as-held-stance requires ground) vs. parallel independence (diplos-as-twoness) is semantically motivated.

---

## Mirror-pair avoidance

Rotation and reflection confusions are the most persistent legibility problems in script design. The brain's object-recognition system is rotation-invariant (the same object seen at different orientations is still the same object); this is useful for navigating the physical world but creates confusion in reading, where p/q and b/d are different symbols that look like rotated versions of each other.

**The rotation/reflection problem in logographic scripts**: Logographic scripts avoid this problem less automatically than alphabets, because logograms are whole-word symbols. A Chinese character 太 (tài) rotated or reflected would not resemble any other character — the glyph is complex enough that no rotation produces a collision. But simple glyphs (like YOUSPEAK's early morpheme designs) are at risk.

**YOUSPEAK rotation/reflection audit**:

| Glyph | 180° rotation | Horizontal reflection | Vertical reflection |
|---|---|---|---|
| phanes (rays from bottom-point) | Cup-shape (upside-down rays) | Same (symmetrical) | Rays from top-point |
| algia (bent stroke, mark at bend) | Bent stroke curving other way | Different | Different |
| meta (left-pointing wedge) | Right-pointing wedge → could conflict with strophe's spiral end | Different | Different |
| ana- (upward arrow) | Downward arrow → could conflict with descent-symbols | — | — |
| en- (inward bracket) | Outward bracket | Different | Inward bracket other direction |

**Key conflict**: ana- (upward arrow = up/back/again) vs. the eventual -me glyph if -me encodes "descent". If -me is a downward-pointing element, it is visually the 180° rotation of ana-. A reader who sees either glyph quickly might confuse them.

**Resolution for ana- / -me potential conflict**: Either:
1. Make one of them NOT a simple arrow (add a distinctive secondary element)
2. Give them sufficiently different shape-families (ana- could be in the "directional" family using an arrow; -me could use the "receiving vessel" vocabulary — an arc opening upward — which is visually very different from a downward-pointing arrow)

**Design rule**: No two YOUSPEAK glyphs should be 90°, 180°, or mirror-reflections of each other unless those glyphs form a *diplosemic pair* — two glyphs that are intentionally related by reversal of meaning (like "contain" and "release", which could be each other's mirror-images by design).

---

## The "distinctive feature" principle (from Jakobson)

Roman Jakobson's distinctive feature theory (from phonology, 1956) proposes that phonemes are distinguished from each other by a small number of binary features (±voiced, ±nasal, ±labial, etc.). You need only enough features to uniquely distinguish each phoneme from all others.

Applied to glyph design: each glyph should be distinguishable from all others by a small number of *visual distinctive features*. The fewer features needed, the more efficient the recognition. The features should map to semantically meaningful distinctions where possible.

**Proposed YOUSPEAK visual distinctive features** (6 dimensions):

| Feature | Values | Example contrast |
|---|---|---|
| 1. Apex orientation | up / down / left / right / none | phanes (up-apex) vs. doxa (down-apex) |
| 2. Enclosure | open / closed / partially-enclosed | sema (closed) vs. dokim (partially-enclosed) vs. phanes (open) |
| 3. Multiplicity | single / double / multiple | ortho (single vertical) vs. diplos (double vertical) vs. phanes (multiple rays) |
| 4. Base | anchored / floating | stasis (base-anchored) vs. diplos (floating parallels) |
| 5. Motion/dynamism | static / implied-motion | stasis (static) vs. strophe (dynamic spiral) vs. meta (directional wedge) |
| 6. Body presence | embodied (face/hand/vessel) / abstract | thauma (eye-embodied) vs. dokim (vessel-embodied) vs. veri (pure-abstract) |

With 6 binary-ish features, there are theoretically 2^6 = 64 distinct glyph-positions. YOUSPEAK currently has ~50 morphemes — well within the distinguishable design space.

When assigning a new glyph, the question becomes: what combination of these 6 features uniquely identifies this morpheme AND is not already taken by an existing morpheme? This is the design-matrix question.

---

## Pleasant re-encounter (the rhythm of shape across the corpus)

A writing system is not a collection of individual glyphs — it is an ensemble. The glyphs must work not just in isolation but as a *family*: related by visual vocabulary, coherent in weight and proportion, pleasurable to encounter repeatedly.

**What makes an ensemble pleasant**:

1. **Consistent stroke weight**: If some glyphs are 80 EM strokes and others are 40 EM strokes, the text feels uneven — some words dominate visually, others disappear. Consistency at 80 EM creates visual equality: every morpheme has equal visual authority.

2. **Proportional harmony**: Glyphs should feel "the same size" even when their internal complexity differs. A simple glyph (diplos = two parallel lines) and a complex glyph (thauma = eye with concentric ovals and dot) should have the same visual *weight*, not the same internal stroke count. This requires the complex glyph to have lighter or fewer strokes than the simple glyph — counterintuitively.

3. **Shape-family coherence**: Glyphs in the same semantic family should share a visual ancestor — a common stroke-type, orientation, or structural principle. Beauty-domain glyphs (curves) should all feel related; truth-domain glyphs (crosses/perpendiculars) should feel related; etc. This is the "rhyme" that YOUSPEAK's shape-families create.

4. **Controlled variety**: Monotony (all glyphs feeling too similar) causes fatigue — the eye can't distinguish them. Chaos (every glyph feeling completely different) causes cognitive overload. Good script design has *controlled variety* — enough diversity to distinguish individual glyphs, enough family-resemblance to read as a coherent ensemble.

5. **The "new but right" feeling**: When a learner encounters an unfamiliar YOUSPEAK compound, each morpheme-glyph should feel both new (they haven't seen it before) and right (it fits in the visual vocabulary they already know from other YOUSPEAK glyphs). The shape-families and consistent stroke-weight create this feeling. The glyph is a stranger who is immediately recognizable as a family member.

---

## Cognitive load at small sizes

YOUSPEAK will be rendered at a range of sizes — from large display sizes on the dashboard (`.ys-big` CSS class, equivalent to ~60-80pt) to body text in running prose (~12pt) to UI labels and keyboard input (~9pt).

**Test at 10pt**: A glyph that looks beautiful at 60pt may become illegible at 10pt if:
- Strokes are too thin (80 EM on 1000 EM body = 8% of height; at 10pt = 0.8pt stroke = very near the minimum visible stroke width on standard displays)
- Counters are too small (internal spaces close up at small sizes, turning the glyph into a black blob)
- Distinctive features are too subtle (a small dot that distinguishes two glyphs at 60pt may not render at 10pt)

**Resolution for YOUSPEAK**:
- Use 80 EM stroke weight for display sizes; consider 90-100 EM for a "small text" variant
- Ensure all counters are at minimum 20% of glyph area
- Key distinctive features (the dot in sema, the mark in algia) must be at minimum 60 EM in diameter — the smallest element that reliably renders at 10pt on standard screens
- Consider OpenType feature: `@media (max-font-size: 12pt) { ... }` → a "simplified" variant of complex glyphs (fewer internal details; same silhouette) for small-size rendering

**Hinting**: Professional fonts include "hinting" — mathematical instructions that tell the renderer how to align strokes to the pixel grid at specific sizes. For YOUSPEAK, basic hinting (align major strokes to pixel boundaries) will significantly improve small-size legibility. This is a font-engineering task for the production phase.

---

## The liturgical attention exception

There is one counter-principle to cognitive-load-minimization that applies to YOUSPEAK:

For certain morphemes in liturgical use, **high cognitive load is appropriate**. The glyph for a word like `mitakuyame` (all-my-relations-as-divine-ordinance) or `hanme` (accumulated-historical-wound-as-creative-source) should require *dwelling*. These are not words you recognize instantly and move past. They are words you enter. The glyph should reward sustained attention — internal details that become visible with time, relationships between strokes that emerge with repetition, a depth that is not exhausted in a single fixation.

This is the **icon principle** from Eastern Orthodox theology. A sacred icon (eikōn) is not a picture that you look at and understand immediately. It is a window that you look through and gradually encounter. The technical quality (gold leaf, specific color-mixing, canonical form) creates conditions for encounter that cannot be hurried.

**YOUSPEAK design application**: For Core morphemes (especially the most theologically weighted ones: -me, doxa, aseme, hanme), the glyph design should have **layered complexity** — a clear immediate silhouette (recognizable at speed) plus internal articulation (visible at contemplative speed). The silhouette serves immediate recognition; the internal details reward sustained attention.

This is NOT the same as gratuitous complexity. The internal details should be *meaningful* — each stroke or mark inside the glyph carries semantic reason. The complexity is the complexity of a face, not the complexity of noise.

Example: **thauma (U+E109, wonder/marvel)** — current design is a simple eye with a dot (centered pupil mark). At the display level, add:
- Two small additional marks above the eye (eyebrow elevation = lifted brow = wonder)
- A subtle radiance at the pupil (a few short strokes from the dot) = wonder-that-illuminates

This adds complexity without obscuring the silhouette (the eye-shape remains primary). The eye at first glance reads as "thauma = gaze = wonder". The brow-lift and pupil-radiance reward sustained viewing — the wondering eye is not just open, it is *lifted and lit*.

This is the difference between a glyph and an icon.

---

_Chapter 6 complete. → [Chapter 7: Sacred-script traditions](07-sacred-script-traditions.md)_
