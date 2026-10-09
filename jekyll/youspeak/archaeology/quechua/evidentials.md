---
tongue: Southern Quechua (primary reference: Cuzco-Collao; adjacent: Aymara, Ayacucho)
semantic_field: evidentiality — grammatical marking of knowledge-source
excavated: 2026-04-24
civilization: Andean pyramid-builders, Caral-Supe (~2600 BCE), Moche (~100-800 CE), Inca (~1400-1533 CE)
status: live; foundation for grammars/evidentials/ chapter
---

# Quechua — the Evidentiality System

_What English cannot say in one syllable: how-you-know. Andean pyramid-heirs encoded every assertion with a knowledge-source marker, so every utterance is automatically marked for whether the speaker witnessed it directly, heard it from elsewhere, or inferred it from evidence. This is not politeness-marking (like Japanese registers) — it is an epistemological grammar. Every sentence declares its basis._

---

## The three primary evidentials

Southern Quechua attaches evidentiality as verbal/clausal suffixes (-mi / -si / -chu). Every assertive statement must pick one; the grammar refuses unmarked assertions.

| Evidential | Quechua form | Source of claim |
|---|---|---|
| **Direct** | **-mi** | Speaker personally witnessed or directly experienced |
| **Reported** | **-si** | Speaker heard from another or read it (hearsay) |
| **Inferential / Conjectural** | **-chu** (with interrogative register) or **-chá** | Speaker inferred from evidence; did not witness |

Examples (schematic):

- *Paqarin para-nqa-**mi*** — "It will rain tomorrow (I observe signs directly)"
- *Paqarin para-nqa-**si*** — "It will rain tomorrow (I was told)"
- *Paqarin para-nqa-**chá*** — "It will rain tomorrow (I infer from weather)"

The three utterances are LEXICALLY IDENTICAL except the evidential. Three different knowledge-bases. English needs a whole parenthetical clause to achieve the same.

## Why this aligns with YOUSPEAK's foundations

- **SAPHE** (clarity): evidential-marked assertions are always clearer about their epistemic basis than unmarked ones
- **PRAGMA** (grounded): evidentiality forces grounding; a speaker cannot make an ungrounded claim
- **HARMONE** (coherent): evidentiality fits cleanly as an optional morpheme-system without disrupting existing YOUSPEAK grammar
- **ANAKALYPSE** (unfolding): English bundles "I know X" into one verb; evidentials unfold three distinct knowledge-relations

This is load-bearing for **Zerone/dokimance-context**: dokimance itself is a testimony-structure. Evidentials make that structure grammatically explicit.

## The Aymara variant

Aymara (the sister Andean language) has a richer evidential system — up to 4-6 distinctions including "personal experience that affected the speaker vs. distant witnessing." For YOUSPEAK-level fidelity, the 3-way Quechua system is sufficient; Aymara's extended set can be a future refinement.

## What YOUSPEAK gets

Evidentials fit as **optional sentence-level suffixes** to YOUSPEAK-canonical assertions. They don't replace English syntax; they augment it in register-specific (dokimance-context, Zerone-claims) use.

Proposed integration:
- **-mi** → direct witness (I saw / I did)
- **-si** → reported (I heard / I was told)
- **-chu** → inferred (I deduced from evidence)

In dokimance-context usage:
- "The dokimance succeeded-**mi**" — I witnessed the verification
- "The dokimance succeeded-**si**" — I was told the verification succeeded
- "The dokimance succeeded-**chu**" — I inferred success from outcome

This unlocks dokimance's full semantic potential. A dokimance-claim can now declare its own evidence-source as part of the grammar.

## Donor forms for YOUSPEAK

As grammatical morphemes in YOUSPEAK's suffix repertoire:

| YOUSPEAK form | Source | Meaning |
|---|---|---|
| **-mi** | Quechua -mi | direct witness |
| **-si** | Quechua -si | reported |
| **-chu** | Quechua -chu / -chá | inferred |

PUA codepoints will be assigned in the grammatical-suffix range (U+E14D-U+E14F), consistent with the existing -ance, -sis, -mance grammatical morphemes.

## The broader Andean contribution

Beyond evidentials, Quechua offers:

- **Regular agglutinative morphology** — almost no irregularity; validates YOUSPEAK's similarly-regular structure
- **Honorific/respect registers** — not selected for integration (register system would be substantial work)
- **Spatial-deictic grammar** — 5-way this/that/yonder system; interesting but not YOUSPEAK-priority

## Proposed integration — grammars/evidentials/

Create a new grammar chapter:
- `grammars/evidentials/manifesto.md` — the doctrine
- `grammars/evidentials/markers.md` — the three evidential suffixes with examples and codepoints
- Update morphemes.json with three new suffixes (U+E14D-E14F)
- Document usage-contexts (primarily dokimance-claims, Zerone-work, any assertion-heavy register)

See `grammars/evidentials/manifesto.md`.

---

_Quechua archaeology excavated 2026-04-24. The Andean pyramid-builders' epistemological grammar — evidentiality as default grammatical feature. Adopted as optional YOUSPEAK suffix-system._
