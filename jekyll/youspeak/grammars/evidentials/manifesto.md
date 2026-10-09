---
chapter: evidentials
organ: grammars
role: YOUSPEAK's third structural-grammar chapter
opened: 2026-04-24
opened_by: integration of Quechua/Andean evidentiality system
status: doctrine + inventory; implementation in script/morphemes.json pending
---

# Evidentials — How-You-Know as Grammar

_What Andean pyramid-heirs encoded as default and English has no syllable for: the knowledge-source marker. Every assertion declares its evidential basis — direct witness, reported, or inferred. YOUSPEAK adopts this as an optional sentence-level suffix system, load-bearing specifically for dokimance-contexts where the distinction matters._

---

## The mechanism

A YOUSPEAK sentence making an assertion can optionally carry a suffix marking HOW the speaker knows. The three primary evidentials:

| Evidential | YOUSPEAK form | Source | Quechua origin |
|---|---|---|---|
| **Direct** | **-mi** | Speaker witnessed / did / directly experienced | Quechua -mi |
| **Reported** | **-si** | Speaker heard / read / was told | Quechua -si |
| **Inferred** | **-chu** | Speaker deduced from evidence; did not witness | Quechua -chá / -chu |

Application: append to a sentence-final verb phrase or to a YOUSPEAK-canonical noun-claim.

## Examples

### Direct (-mi)

> *The dokimance succeeded-mi.*

I personally performed or witnessed the dokimance succeeding.

### Reported (-si)

> *The dokimance succeeded-si.*

I was told or read that the dokimance succeeded. I did not witness it.

### Inferred (-chu)

> *The dokimance succeeded-chu.*

I did not witness it; I infer success from the outcome pattern.

The three forms make EXPLICIT what English requires a parenthetical to convey:
- "The dokimance succeeded (I was there)."
- "The dokimance succeeded (I heard)."
- "The dokimance succeeded (I infer)."

## Why evidentials align with YOUSPEAK's foundations

| Foundation | How evidentials serve it |
|---|---|
| **EUMATHE** | Three short suffixes; learnable in one exposure; regular application |
| **SAPHE** | Every assertion declares its basis; ambiguity about sourcing is impossible |
| **ANAKALYPSE** | Unfolds English's undifferentiated "I know" into three distinct knowledge-relations |
| **POLYPHONE** | Andean/Quechua integration — Pre-Columbian Americas joining the YOUSPEAK donor-set |
| **HARMONE** | Suffix system integrates cleanly with existing grammatical morphemes (-ance, -sis, etc.) |
| **PRAGMA** | Grounded in actual knowledge-source distinctions everyone makes mentally; now grammatical |

## Load-bearing for Zerone

**dokimance** (Asha's primary word) names the testing-that-makes-real. Every dokimance-assertion has a knowledge-source. With evidentials:

- Witness-validators on the chain post *-mi*-assertions
- Replicators / downstream-observers post *-si* when reporting others' dokimance-events
- Auditors post *-chu* when inferring historical dokimance from present evidence

This unlocks dokimance's full semantic potential: every claim carries its evidence-basis in its grammar. The chain becomes self-documenting about how-it-knows.

## Integration with existing YOUSPEAK grammar

Evidentials are **optional** — they don't replace English syntax for general prose. They are standard in:

1. **Zerone/dokimance contexts** — every assertion on the chain
2. **Testimonial speech** — when credibility of source matters
3. **Scholarly/research YOUSPEAK** — every claim traces its basis
4. **Liturgical YOUSPEAK** — witness-reports vs tradition-reports

In everyday YOUSPEAK-English mixed prose, evidentials can be omitted; English's rhetorical conventions handle it.

## Codepoint assignment

The three evidentials are grammatical suffixes. Assigned in the grammatical-suffix range:

| Code | Latin | Meaning |
|---|---|---|
| U+E14D | -mi | direct witness |
| U+E14E | -si | reported |
| U+E14F | -chu | inferred |

These extend the existing grammatical-morpheme range (U+E140–U+E14C) with three Andean suffixes.

## Engineering rules

1. **Evidentials attach to the main verb or to the YOUSPEAK-canonical noun-claim**, not to individual morphemes within a compound.
   - Correct: "The doxakallos appeared-**mi**"
   - Correct: "I witnessed dokimance-**mi** today"
   - Wrong: "doxa-**mi**-kallos" (attaching to a morpheme)

2. **Only one evidential per clause.** Mixed knowledge-sources require separate clauses.

3. **Absence of evidential = register-normal** (i.e., the speaker is not marking epistemic basis). This is not the same as direct witness; absence is unmarked, direct-witness is *-mi*-marked.

4. **Questions and negations can carry evidentials.**
   - "Did the dokimance succeed-**si**?" = "Are you reporting that it succeeded?"
   - "The dokimance did not succeed-**chu**" = "I infer (from evidence) that it did not succeed"

## Extended set (v2 candidates, not yet integrated)

Aymara has a richer evidential system. Possible future additions:

| Candidate | Aymara form | Meaning |
|---|---|---|
| -ta | -taynawa | personal-past experience (I experienced it then) |
| -sa | -yapi | counterfactual (it would have been) |
| -ch | -chitanwa | dubitative (I doubt it) |

These are deferred pending usage-evidence that the three-way (-mi/-si/-chu) is insufficient.

## Quechua acknowledgment

The three primary evidentials are direct Quechua loans, with the following transformations:
- *-mi*: preserved exactly
- *-si*: preserved exactly
- *-chu*: preserved (Quechua has *-chá* in some dialects for inferential; we take *-chu* as the standard form for phonetic simplicity)

Quechua is acknowledged as the originating tradition. This is POLYPHONE in action.

## Integration status

- **Archaeology written**: archaeology/quechua/evidentials.md
- **Manifesto written**: this document
- **Inventory**: 3 evidentials at U+E14D-E14F
- **Canon-compatibility**: all 18 canon words compatible (evidentials attach at sentence level, not morpheme level)

**Pending**:
- Add 3 entries to script/morphemes.json (grammatical class)
- Design the 3 glyph shapes (short-suffix conventions)
- Rebuild font with evidential glyphs
- Update LLM primer with evidential usage-examples
- Add Espanso triggers for `:ys:mi`, `:ys:si`, `:ys:chu`

---

_Evidentials chapter opened 2026-04-24. YOUSPEAK's third grammar organ. The Andean pyramid-heirs' epistemological grammar, operational for dokimance-register writing._

---

## Note: evidentials under the projection-account

Under [NOEMA.md](../../NOEMA.md), [THE-REALM.md](../../THE-REALM.md), and [GRASPING.md](../../GRASPING.md) (all opened 2026-05-12), evidentials receive a sharper reading. An evidential suffix marks **the epistemic position from which the speaker entered the realm-region the assertion projects**.

- `-mi` (direct) — the speaker's grasping was first-hand (the speaker entered the region by direct witness or doing).
- `-si` (reported) — the speaker's grasping was mediated through another's projection (the speaker stands-in the region because someone else's report opened the gate to them).
- `-chu` (inferred) — the speaker reached the region by inference from signs (the speaker's grasping was deductive rather than first-hand).

The three suffixes are therefore **grasping-source markers**: they tell the hearer how the speaker reached the realm-region they are asserting. In Zerone/dokimance contexts where dokimance-testing-as-real depends on knowing how a claim arrived, evidentials make the grasping-path visible on the surface. The hearer can then weigh the assertion by its access-path. The cathedral's commitment to honest assertion (SAPHE) is partly the commitment to not collapse these three grasping-sources into an undifferentiated "I know."

Evidentials are grasping-engineering at the epistemic aspect (GRASPING.md Section VII names this).
