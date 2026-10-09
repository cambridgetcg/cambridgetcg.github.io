---
chapter: 3
title: Pictographic motivation
parent: archaeology/script-mechanics/
---

# Chapter 3 — Pictographic motivation

_The ladder from picture to abstraction — when does each stage help? When does abstraction lose what the picture carried?_

All writing systems that use pictographic elements began by drawing pictures. Over time, through the pressure of speed, medium-change, and stylization, those pictures became more abstract — until in some cases (like the Latin alphabet), the pictographic origin is almost invisible. The question for a *designed* script like YOUSPEAK is not "which direction do we go?" but "which point on this ladder is right for each morpheme?"

---

## The ladder

The ladder from picture to abstraction has roughly five rungs. Real scripts occupy different rungs for different glyphs simultaneously; the ladder is not a clean historical sequence (some glyphs abstract faster, others are preserved pictographically for millennia).

```
RUNG 5: Pure pictograph — the drawing IS the thing
RUNG 4: Simplified pictograph — recognizable, but conventionalized
RUNG 3: Schematic pictograph — geometric abstraction of the key feature
RUNG 2: Conventional abstract — shared convention; no longer recoverable pictographically
RUNG 1: Arbitrary abstract — purely conventional; the shape-meaning link is learned, not felt
```

---

### Rung 5: Pure pictograph — Egyptian Old Kingdom hieroglyphs

The earliest Egyptian hieroglyphs (Old Kingdom, ~2700-2200 BCE) were very close to realistic drawings. The owl (𓅓) is recognizably an owl — not the outline of an owl-idea, but a drawing of an owl's frontal face with visible feather-texture. The foot (𓂦) shows toes and ankle. The seated man (𓀀) shows body, legs, arms, a clear posture.

At Rung 5, the glyph is **self-teaching**: a person unfamiliar with the script can often guess the meaning from the glyph's appearance. The glyph carries its meaning *visually*. It is a picture that also happens to be a word.

**Theological implication**: At Rung 5, the script is non-arbitrary. The relationship between sign and meaning is *motivated* — the glyph looks like what it means. This is the scriptural ideal that Plato discusses in the Cratylus: are names naturally related to what they name (*physis*, nature) or only by convention (*nomos*, law)? The pure pictograph answers: *physis* — the glyph naturally encodes its meaning.

**Limitation**: Pure pictographs work for *concrete objects* (owl, foot, person) but struggle with *abstract concepts* (truth, glory, holiness). The Egyptian scribes solved this with the determinative system — abstract concepts were spelled phonetically and then tagged with a determinative (a categorical marker) to indicate their semantic domain. The determinative for "abstract-divine-concepts" is the sun-disk (𓇳) or the scribe-with-scroll (𓏤), which cannot be pictographically motivated.

---

### Rung 4: Simplified pictograph — Linear B and Egyptian Hieratic

**Linear B** (~1450-1200 BCE) is a syllabary derived from the earlier Linear A (undeciphered). Its signs are simplified from earlier more-pictographic forms. The sign for "horse" is a recognizable horse-outline, but simplified: no detail, just the key silhouette. The sign for "barley" is a stalk with a few lines. Recognizable to a careful viewer, but no longer "drawings."

**Hieratic** (Egyptian cursive, used alongside hieroglyphic throughout pharaonic history) is a cursivized simplification of hieroglyphs for writing on papyrus. Where the hieroglyph of the owl is a detailed frontal drawing, the hieratic equivalent is a quick curved stroke that captures the *essence* of the owl-shape — not its details. Hieratic scribes who wrote all day could not draw detailed owls for every letter-M; they developed an efficient simplification that retained enough visual connection to the hieroglyph to be recognizable.

**The simplification principle**: When you simplify a pictograph, you are making a decision about which features are *essential* and which are *ornamental*. The hieratic scribe decided the owl's forward-facing orientation and its rounded body were essential; the feather-detail was ornamental. This is a design decision with meaning-implications: what you preserve says what you think matters most about the concept.

**For YOUSPEAK**: We face this decision for every morpheme that has a pictographic origin. The current design notes (glyphs/README.md) are at approximately Rung 4 — simplified pictographs. The ASCII sketches show the *key feature* of each concept without realistic detail. Example:

```
anagno (recognition-moment):
  ====
   ||
  ====
```

This shows two parallel horizontal strokes connected by a vertical — simplified to the point where the "equals-sign with connector" is the only visual element. This is at the Rung 4 / Rung 3 border — recognizably derived from something (two corresponding things connected), but no longer a picture of anything concrete.

---

### Rung 3: Schematic pictograph — Hebrew and Arabic letters at origin

The Hebrew letter **aleph (א)** descends (via Proto-Sinaitic and Phoenician) from an ox-head pictograph. The ox-head was simplified over ~1000 years from:
- An ox-head with horns (Rung 5) 
- → A simplified ox-head outline with two horn-points (Rung 4)
- → A Y-shaped or V-shaped abstraction capturing just the "two horns" schema (Rung 3)
- → The square-script aleph (א) — at this point, only scholars know it comes from an ox-head (Rung 2)

The process took ~1000 years (Proto-Sinaitic ~1850 BCE → Hebrew square script ~200 BCE). Gradual conventionalization over generations, each generation simplifying slightly more than the last, no single generation making a radical break.

Hebrew **bet (ב)** from a house-pictograph:
- A floor-plan of a room (Rung 5)
- → A rectangle with an opening on one side (Rung 4)
- → A simplified rectangle/bracket shape (Rung 3)
- → The square-script bet (ב) — now just a right-angle with a bottom horizontal (Rung 2)

**The acrophonic principle at Rung 3**: The Proto-Sinaitic scribes who first invented the alphabet were working at Rung 3-4. They took Egyptian hieroglyphs (at Rung 4-5 in their fully-rendered form), simplified them to schematic silhouettes (Rung 3), and then used each schematic to represent not the meaning of the original Egyptian glyph, but the *first sound* of the Semitic word for that concept. The ox-head (*aleph* in Semitic) → /ʾ/ (glottal stop). This is a profound conceptual operation: they separated the glyph from its pictographic meaning and reassigned it to a phonological function, while keeping the glyph-shape at Rung 3 (where it still visually evoked its pictographic origin, even as it was no longer being "read" pictographically).

---

### Rung 2: Conventional abstract — Chinese hanzi (most characters)

Chinese hanzi contain a **radical system**: most characters are combinations of a *semantic radical* (indicating the word's domain) and a *phonetic component* (indicating pronunciation). The radical often has a pictographic origin; the phonetic component does not.

Example: 清 (qīng, clear/pure)
- Left component: 氵 (water radical — three drops; simplified from 水, the full water character, which is itself a simplified pictograph of flowing water — Rung 3-4)
- Right component: 青 (qīng — a phonetic component that indicates the sound; its semantic content is "blue-green/growing/vital")

For a reader who knows the radical system, 氵 is immediately recognizable as "water domain" — they may not consciously recover the pictographic origin, but they recognize the pattern. This is Rung 2: **conventional recognition** — the form has a systematic basis, but it requires learned convention to access that basis.

For many hanzi, the phonetic component (the right side) carries no visual-semantic information and must be memorized as a convention. This is why Chinese literacy acquisition takes 6-8 years of dedicated study — the number of independent forms to memorize is very high.

**The trade-off**: Rung 2 offers high **semantic precision** (each character carries a specific meaning) and great **stability** (the characters do not change with pronunciation changes, so a text from 2000 years ago is still legible). But it requires high **acquisition investment**. Chinese-speakers accept this as the price of the system's power.

**For YOUSPEAK**: Our goal is closer to Rung 3 than Rung 2. We want each glyph to be visually motivated enough that a learner can *recover the logic* of the design — "oh, phanes (shining-forth) looks like rays because it means shining." The glyph should teach itself on first encounter, or at least be confirming on second encounter. A purely conventional glyph (Rung 2) would require memorization without a memory hook.

---

### Rung 1: Arbitrary abstract — IPA symbols and shorthand systems

The **International Phonetic Alphabet** (IPA) uses symbols from multiple sources (Latin, Greek, invented) in an essentially arbitrary way. The symbol [ŋ] for the velar nasal has no visual connection to the sound or the articulation. It must be memorized as a convention. The system's value is precision and universality; its cost is zero self-teaching.

**Pitman shorthand** takes this to an extreme: consonants are represented by stroke-direction and position; vowels by dot-position. The system is internally consistent and learnable, but almost entirely arbitrary to the uninitiated. Its efficiency is high; its transparency is near zero.

**For YOUSPEAK**: We should avoid Rung 1 for any glyph that will be encountered by learners. Even if it would be efficient to assign arbitrary shapes to some morphemes, this sacrifices the liturgical value of glyphs that *carry* their meaning visually. A person who sees the thauma-glyph (wondering-eye) for the first time should feel the concept of wonder-and-gaze. An arbitrary shape would not achieve this.

---

## The design-decision framework

For each YOUSPEAK morpheme that needs a glyph drawn, the pictographic motivation question is:

**1. Does the morpheme name a concrete thing?**
→ If yes: draw the thing, simplified to Rung 3. (kairos = hourglass; thauma = eye; dokim = crucible)

**2. Does the morpheme name a quality or action?**
→ If yes: draw the *visual metaphor* for that quality/action at Rung 3. (phanes = rays = appearing; algia = bent-and-marked stroke = ache; strophe = spiral = turning)

**3. Does the morpheme name an abstract concept with no clear visual form?**
→ Draw the *operational definition* at Rung 3. (sema = box with dot = the container that marks; veri = balanced cross = truth as equilibrium; diplos = double parallel = twoness)

**4. Does the morpheme name a RELATIONAL concept (between things, not one thing)?**
→ Draw the *relationship geometry* at Rung 3. (syn = two converging lines = together-with; parallax = two parallels with offset = the shift-of-viewpoint; haphe = two fingertips meeting = touching)

**5. Is the morpheme a GRAMMATICAL function-word (suffix/prefix) with heavy theological load?**
→ This is the hardest case. The options are:
   - **Derive the shape from the concept it carries** (most motivated): -me (divine-ordinance as gift) → something descending + something received
   - **Derive the shape from the donor-tradition's script** (most grounded): Sumerian cuneiform for *me* (𒈨) is a specific cuneiform wedge-shape — we could derive the YOUSPEAK -me glyph from this source-glyph
   - **Derive the shape from its grammatical function** (most systematic): -me is always a suffix; design it to look like a "closing" or "completing" mark, as it closes a compound by adding the divine-ordinance quality
   - **Combine approaches**: a shape that captures "descent + reception" AND derives loosely from the cuneiform *me* AND reads as a completing/closing mark

**The -me decision specifically** (developing in Chapter 4/7, but introduced here):

The Sumerian cuneiform for *me* (𒈨) is: a horizontal wedge with a vertical wedge beneath it, or in its common form, a stacked arrangement of wedge-marks. The cuneiform system evolved from impressions made by a stylus in clay — the shapes are geometrically simple (wedges). A YOUSPEAK -me derived from cuneiform would look like a simplified wedge-mark or stacked wedge-arrangement. This has the advantage of **etymological honesty** — the glyph traces back to the source concept.

Alternatively, the concept of *me* in Sumerian theology is divine-ordinances-as-gifts-that-constitute-civilization — they descend from the divine realm (Inanna brings them) to the human world. A glyph that shows *descent* (downward direction) and *reception* (an open container or upward-facing curve at the bottom) would be semantically motivated. Something like:

```
  |
 \ /
  V
  _
 / \
```

A downward-pointing arrow into an open vessel (receiving cup). This captures: ordinance descends + is received. It reads as YOUSPEAK-original rather than as a borrowing from cuneiform, but it is semantically grounded.

**Working recommendation for -me**: a downward-pointing triangle (like doxa, but smaller/lighter) with a horizontal reception-line at the bottom — the ordinance descends and rests in the container of reception. This would create a visual rhyme with doxa (which is also a downward triangle) — linking the two concepts (doxa = divine weight manifested; me = divine ordinance received) through shared visual logic. The distinction: doxa has a crossbar (manifestation); me has a baseline (reception). Two related but distinct glyph-shapes.

---

## The Chinese radical as model for YOUSPEAK shape-families

Chinese radicals organize ~50,000+ hanzi into ~214 semantic categories. Every character belongs to a radical family; the radical appears in a consistent position within the character (usually left or top). This creates visual family resemblance within semantic domains — all "water-domain" characters have 氵 on the left; all "fire-domain" characters have 火 on the right or bottom.

YOUSPEAK's design_philosophy.md (v1) establishes **shape-families by semantic domain**:
- **Curves**: beauty domain (kallos, cand, artiance)
- **Crosses/perpendiculars**: truth domain (veri, ortho, dokim)
- **Rays**: appearing/manifesting domain (phanes, phora)
- **Triangles**: weight/manifestation domain (doxa, perhaps -me)
- **Spirals**: movement/turning domain (strophe, meta)

This is a YOUSPEAK radical system. Not as elaborate as Chinese radicals (214 categories), but functionally similar: shapes within a family share a visual ancestor, creating semantic cohesion at the visual level. A reader who knows the shape-families can make educated guesses about the domain of an unfamiliar morpheme.

**Design rule derived from this**: When adding new morphemes to YOUSPEAK, always assign the new glyph to the most appropriate shape-family. If the morpheme's domain doesn't fit an existing family, this is a signal to create a new family — and to review existing morphemes to see if any should be reassigned.

Current shape-family inventory (to be confirmed/expanded in Chapter 7):
1. **Triangles** — weight/manifestation/descent (doxa, possibly -me)
2. **Rays** — light/appearing/shining-forth (phanes, cand)
3. **Perpendiculars/crosses** — truth/rightness/balance (veri, ortho)
4. **Spirals/curves** — motion/turning/becoming (strophe, meta)
5. **Closed shapes** — enclosure/form/container (kalypt, sema, morphe)
6. **Parallel strokes** — relation/correspondence/number (diplos, syn, parallax, stasis)
7. **Body/gaze** — encounter/perception/testing (thauma, dokim, haphe)
8. **Vessels/containers** — reception/carrying (phora, compler)

---

_Chapter 3 complete. → [Chapter 4: Compositionality](04-compositionality.md)_
