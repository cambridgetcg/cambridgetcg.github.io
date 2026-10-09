<!--
archaeology/TEMPLATE.md — standardised archaeology-file template (HOME-EXPANSION §VII.B)

WHEN TO USE: when opening a new donor-tradition file — a new tradition directory, or a new
semantic-field file inside an existing one. A coinage cites a tradition only after the
archaeology has been opened; this template is the opening's house-shape, extracted from the
existing pattern (sanskrit/shaktipata-kashmir-shaiva.md, maori/hau-return-gift-spirit.md,
hawaiian/pono-rightness-balance.md, hebrew/bittul-hayesh-hasidic.md, mathema/physics/noether.md).

HOW: if the tradition directory does not exist yet, stub it first:
    python3 pipeline/discover.py --seed <tongue>
then copy this template into the new directory as <semantic-field-slug>.md and fill the slots.

PLACEHOLDERS: every <angle-bracket slot> carries one line of guidance after an em-dash.
Replace the whole slot, brackets included. Delete sections marked "delete if not applicable"
rather than leaving them empty. Delete this comment block in the finished file.

MATHEMA-VARIANT: for mathema-class donors (per the noether.md pattern), see the variant
notes at the end of this template before filling.
-->
---
title: <Native-Term (native script) — compact clause naming the realm-feature it donates, e.g. "Śaktipāta (शक्तिपात) — the descent of divine power-grace, graded in intensities, given not earned">
tradition: <Tongue / sub-tradition (school, period, key systematizer) — e.g. "Hebrew / Hasidic Kabbalah (18th c. onward; Maggid of Mezritch school + Chabad systematization)">
language_family: <genetic family + branch — e.g. "Eastern Polynesian, Tahitic branch (Austronesian)"; this field is load-bearing for convergence genetic-independence counts>
status: <opening | substantive archaeology | live — plus what this file completes or accompanies, e.g. "substantive archaeology (third Kashmir Shaivism entry; completes the doctrinal trio)">
mining_depth_level: <1 surface-survey | 2 single-concept substantive | 3 cluster-depth | 4 sub-tradition systematic — the depth this file reaches, per the HOME-EXPANSION phase it serves>
opened: <YYYY-MM-DD (SNNN — phase number + the invocation under which the file was opened, e.g. "2026-06-09 (S086 — HOME-EXPANSION Phase 3.1, under Yu's invocation)")>
protocol_sensitivity: <REQUIRED where living-tradition: "LIVING TRADITION — custodians named in §0; consultation-desirability recorded; custodian-request → withdrawal"; DELETE this field entirely for closed-corpus donors>
attested: <the attestation-chain in one line — primary texts, dictionaries, living practice, e.g. "Tanya (1797); Kuntres ha-Hitpaʿalut; ongoing Chabad contemplative practice">
role: <donor-role in one line — which realm-feature this tradition donates for, and which forge-target/phase it serves, e.g. "donor for bittulme (Phase 2.2, experiment NNN)">
companions: <sibling archaeology files + canon entries this file pairs with — relative paths>
---

# <Native-Term> — <the realm-feature as a clause, e.g. "the power-descent that begins the path">

<lede — one italic paragraph situating the file: what came before it in this tradition's directory, why this concept is the right next excavation, and (for protocol-sensitive files) the first duty the excavation owes>

---

## 0. Protocol notice — read first

<!-- LIVING TRADITIONS ONLY — delete this whole section for closed-corpus and mathema donors. -->

<protocol-frame — name the tradition as living, with living custodians; name any extraction-history or appropriation-hazard internal to this concept>

The cathedral's discipline here (per the tjukurpame precedent, S084):

1. <custodian-naming — name the tradition's teachers/scholars as authors and authorities, never as "informants"; cite kaupapa/insider scholarship by name>
2. <reception-not-extraction — state that primary custodianship remains with the tradition; the cathedral receives the structural-form with respect>
3. <consultation-desirability — record explicitly that review by the tradition's scholars/custodians is desirable before liturgical or pedagogical elaboration>
4. <retirement-condition — "custodian-request → immediate withdrawal" as a standing condition for any coinage from this file>

---

## 1. The concept in compact form

<compact-form — two to four paragraphs: the term, its literal morphology, its technical sense inside the tradition, and the doctrine-arc it belongs to>

<structural-properties — a short numbered list (typically 2–4) of the concept's load-bearing structural marks, each one sentence to one paragraph, each citing the tradition's own texts; these are what the forge must preserve>

## 2. Native-form donors — attested senses

<sense-table — table of the donor lexeme's attested senses; cite the authoritative dictionary or text-corpus for each row; polysemy shown as structure, not vagueness>

| Native form | Script / romanization | Gloss | Attestation |
|---|---|---|---|
| <form — the donor lexeme> | <script — native script + romanization> | <gloss — compact English rendering> | <source — dictionary s.v. / text + locus> |
| <form-2 — cluster-sibling or derived form> | <script> | <gloss> | <source> |

<sibling-distinctions — one paragraph distinguishing the donor from its nearest in-tradition neighbors (the "hau is not mauri and not mana" move); three words, three registers — name each register>

## 3. Primary attestations and scholarly references

<primary-attestation — the key primary passages, quoted in the original where feasible with translation; name the text, author, date, locus; where a transmission-history matters (editions, mistranslations, contested readings), record it honestly>

<scholarly-afterlife — the reception-history in brief: who carried the concept where, who corrected whom; state which articulation the cathedral receives and why>

## 4. Etymology and family

- <etymology — root, derivation, proto-form with cognates where reconstructible>
- <morphology — the formation-pattern, and any pattern-echo with existing canon words (e.g. shared mishkal, shared compound-shape)>
- <doctrinal-family — the term's working cluster inside the tradition: the words it presupposes, opposes, and completes>

## 5. The unnamed region — the gap-shadows

<gap-evidence — a short list of phenomena English speakers feel constantly and cannot name; concrete, everyday, felt-but-wordless instances that the donor names>

Near-misses, each failing:

| Candidate | Why it fails |
|---|---|
| <english-near-miss — closest English word> | <failure — the structural feature it loses: register, axis, mechanism, or pole> |
| <neighbor-tradition-near-miss — closest other-tradition term> | <failure — why it is witness, not substitute> |

<canon-collision-check — name YOUSPEAK's own nearest neighbors (existing canon words) and state precisely which region each already holds and why none holds this one; date the collision-check>

## 6. Convergence-mapping

<existing-convergences — which convergences/ files this tradition now adds a witness to; for each, the native term contributed and the aspect it attests>

<new-convergence-patterns — cross-tradition resonance not yet housed in convergences/: a list of tradition + term + one-line aspect, each a genuine independent witness; flag contact-explainable overlaps per POLYPHONIA Source 3 so they are not counted as independent>

Convergence cardinality: <N — count of independent tradition-witnesses on the realm-feature, this tradition included>

## 7. Connectable canon-words

<canon-connections — existing canon entries this file's terms neighbor, deepen, or pair with; for each: the canon word, its tier/score, and the relation (completes, mirrors, opposes, presupposes); this is the interlinking the forge will inherit>

## 8. Forge-targets identified

- Donor pair: <donor-pair — native donor + family-suffix donor, e.g. "Sanskrit śaktipāta (शक्तिपात) + Sumerian me (𒈨)">
- Lemma form: <lemma — donor + suffix → coinage, e.g. "bittul + me → bittulme">
- IPA: <ipa — /…/ (respelling; syllable count)>
- Family-fit: <suffix-justification — why this family-suffix (-me received-ordinance / -qing felt-bond / -ance perceived-state / other) and why the neighbors would mis-assign>
- Learnability note: <learnability — honest: syllable count, phoneme inventory, false-friend homophones, loanword familiarity; mitigation if at the long edge>
- Status: <forge-status — queued | in-forge | canonized | refining; with experiment number and session once assigned>

## 9. Donors available for coinage

<donor-table — the full coinage-yield of this file: primary target first, deferred candidates after, each with an honest deferral-reason>

| Donor | YOUSPEAK candidate | Family-fit | Tier guess | Note |
|---|---|---|---|---|
| <primary-donor — the file's main donor term> | <candidate — the coinage> | <suffix — -me / -qing / -ance + one-word rationale> | <tier — e.g. "Core 8.0–8.4"> | <note — "PRIMARY" + forge status / session> |
| <deferred-donor — cluster-sibling> | <candidate> | <suffix> | <tier> | <deferral-reason — crowds which word, needs which protocol care, names rite-not-force, etc.> |

## 10. References

- <primary-sources — the tradition's own texts first: author, date, title, edition>
- <scholarship — academic treatments: author (year), title, venue; links where stable>
- <dictionaries-and-links — authoritative dictionaries s.v.; stable reference URLs last>

---

<closing-line — optional: one italic sentence carrying the concept's own voice, per the house pattern>

— Nuance, the Linguist, <YYYY-MM-DD> (session <NNN>; <one-line record of what this file opened and which forge it serves>)

<!--
MATHEMA-VARIANT NOTES (per mathema/physics/noether.md) — for mathema-class donors:
- File lives under mathema/<discipline>/, not archaeology/; tradition: "mathema/<discipline>
  (donor-class: structural-invariant)"; language_family and §0 protocol do not apply — delete.
- §1 becomes the theorem/structure in compact form (formal statement + the invariant-table).
- Add a mandatory section "Why this is realm-content, not arbitrary mathematics" — the
  constitutive (not descriptive) reading that justifies reception under THE-REALM/ORIGIN.
- §3 attestation = original paper + standard textbook statement; §4 etymology = the
  mathematician/lineage and the result's name-history.
- INTEGRATION discipline: a mathema forge requires the existing-language-path companion to be
  already present — record the companion archaeology/convergence in §6/§7 before forging.
-->
