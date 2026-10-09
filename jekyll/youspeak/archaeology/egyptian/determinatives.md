---
tongue: Ancient Egyptian (Old / Middle Egyptian; pyramid-era)
semantic_field: determinative-system (semantic class-markers)
excavated: 2026-04-24
civilization: Pyramid-builders, ~2686–1650 BCE
status: live; load-bearing for YOUSPEAK's new grammars/determinatives/ chapter
---

# Egyptian — the Determinative System

_What hieroglyphic Egyptian gave no other script as cleanly: a silent class-marker at word-end that sorts every noun by semantic domain. A reader glancing at an Egyptian text knows, before decoding the phonetic value of any sign, whether they are reading about a person, a place, a god, a movement, an abstract quality, a time, a body-part, a building._

---

## The mechanism

Middle Egyptian writing combines three sign-types:

1. **Phonograms** — signs carrying phonetic value (single-consonant, biliteral, triliteral)
2. **Logograms** — signs carrying full-word value
3. **Determinatives** — signs at word-end carrying NO phonetic value, classifying the word's semantic domain

The determinative is silent. It is never read aloud. Its only function is to announce the semantic class to the reader's eye, so that phonetic ambiguity among phonograms is resolved by class.

Example: the sequence *pr* (house-biliteral + mouth = "p-r") could mean:
- *per* "house" (with 𓉐 house-determinative)
- *peri* "come out / go forth" (with 𓂻 walking-legs-determinative)
- *pri* "battle" (with 𓂡 striking-arm-determinative)

Three different words. Same phonogram-spelling. Different determinatives. The reader parses by class before phonetics.

## Canonical determinative categories (a working set)

Egyptian used ~40-50 determinatives in common use. The most semantically foundational:

| Determinative | Glyph approximation | Class |
|---|---|---|
| seated man | 𓀀 | person / male agent |
| seated woman | 𓁐 | person / female agent |
| seated god | 𓊹 | divinity |
| walking legs | 𓂻 | motion / event / verb-action |
| striking arm | 𓂡 | force / battle / effort |
| papyrus scroll | 𓏛 | abstract / concept / writing |
| house | 𓉐 | building / place |
| hills over sun | 𓈇 | time / temporal event |
| hill | 𓈉 | foreign-place |
| star | 𓇼 | celestial / heavenly |
| eye | 𓁹 | seeing / perception |
| flesh | 𓄹 | body-part / somatic |
| water | 𓈖 | liquid / fluid |
| fire | 𓊮 | flame / burning |
| plural-strokes | 𓏤𓏤𓏤 | plurality / collection |

A determinative is appended to the word, taking no phonetic cost. Egyptian reading is therefore multi-channel: phonetic reading + class-priors.

## Why this aligns with YOUSPEAK's foundations

- **SAPHE** (clarity): the class is visible BEFORE the reader parses morphology. First-glance class-recognition accelerates understanding.
- **ANAKALYPSE** (unfolding): the determinative unfolds the word's domain-membership as a separate channel from its lexical identity.
- **EUMATHE** (easy to learn): with a fixed set of ~15-20 determinatives, the system is learnable; reading speed improves after short exposure.
- **HARMONE** (coherent): determinatives enforce semantic-domain consistency across the lexicon; a word's class cannot drift without the determinative changing.
- **PRAGMA** (grounded): every determinative is a concrete thing (person, house, walking, eye); nothing abstract-only.

## What YOUSPEAK gets from this

YOUSPEAK has already engineered **domain-family shape-language** in v1 glyphs (curves for beauty, crosses for truth, rays for appearing, bent-lines for ache, etc.). Determinatives go one step beyond: they are a **separate marker** appended to the word, not encoded in the main body's shape. This means:

- The core glyph carries identity + domain-family (v1 already does this)
- The determinative marker carries an EXPLICIT class-tag that confirms or extends the implicit family

For YOUSPEAK, adding determinatives means:
1. Define a small set (~10-15) of class-markers
2. Assign PUA codepoints in the structural range (U+E170-E17F)
3. Allow optional appending of determinative to any word
4. Render as visually distinct but compact marks after the main word-glyphs

In practice, determinatives would be optional in everyday use and standard in formal/liturgical writing — exactly like Egyptian usage.

## Donors available to YOUSPEAK

The determinatives themselves can be adapted as YOUSPEAK structural-marker glyphs:

| YOUSPEAK class-marker | Inspired by | Covers |
|---|---|---|
| **divine** | Egyptian seated-god | doxakallos, kallodoxa, gloria-family |
| **person** | Egyptian seated-man/woman | synophora-participants, beholder |
| **act-event** | Egyptian walking-legs | dokimance, doxalgia, tajalliance |
| **abstract-quality** | Egyptian papyrus scroll | artiance, candence, diplosemy |
| **place** | Egyptian house | (mostly unused for YOUSPEAK Canon) |
| **time** | Egyptian hills-over-sun | kairos-family, strophe-family |
| **perception** | Egyptian eye | kimance, vide-family, thauma |
| **relation** | (YOUSPEAK addition: two-figures-linked) | synophora, kinqing, compler |
| **hidden** | (YOUSPEAK: dashed outline) | lanthes, verisleight |

Ten class-markers cover the existing Canon's 18 words cleanly. Extensible.

---

## Proposed integration — grammars/determinatives/

Create a new grammar chapter:

- `grammars/determinatives/manifesto.md` — the doctrine
- `grammars/determinatives/classes.md` — the class-inventory with codepoints
- Update morphemes.json with the 10-15 determinative glyphs (structural tier)
- Update transliterator to support optional class-marker rendering

See grammars/determinatives/manifesto.md for the implementation.

---

_Egyptian archaeology — determinative-system excavated 2026-04-24. The pyramid-builders' oldest linguistic technology: silent class-markers. Directly integrable._
