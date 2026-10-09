---
title: The YOUSPEAK Constitution
role: foundational axioms — every module, every Law, every forge must conform
opened: 2026-04-24
invoker: Yu
status: supersedes the implicit design doctrine that produced the original Canon; existing words must be re-audited against these foundations
---

# The YOUSPEAK Constitution

> _Amended 2026-04-24 under Yu's invocation: the Six Foundations rest on **THEOBASIS** — GoD as the basis of reality. See [THEOBASIS.md](THEOBASIS.md) for the metaphysical ground. The Six engineering-foundations below stand on the Ground; without it they are engineering principles floating free; with it they are a discipline of worship._

_The six foundations that any YOUSPEAK coinage, module, or process must honour. Every prior Law of Coinage, every axis in the assessment rubric, every pipeline tool — derives from these. Where they conflict with prior decisions, the Constitution wins._

---

## The Six Foundations

### I. EUMATHE — Easy to learn, write, and speak

**The claim.** A capable English-speaker must be able to hold ~100 canonical YOUSPEAK words in usable memory within a reasonable training period (say: 2-3 weeks of regular exposure). The script must be writable by hand without special training. Words must be pronounceable by anyone who speaks one of the major world languages.

**The test.** Can an untrained reader, encountering a new YOUSPEAK word for the first time, make a reasonable first-pass guess at its meaning from visible components? Can they pronounce it out loud without hesitation? Would a 10-year-old remember it a day later?

**What this rules out.** Six-syllable Greek compounds like *anagnoristasis*. Obscure etymology-laden coinages that require classical education. Ambiguous phoneme sequences. Words that require the speaker to know YOUSPEAK before they can use YOUSPEAK.

### II. SAPHE — Thinking in YOUSPEAK produces clarity

**The claim.** Using a YOUSPEAK word should make the user think MORE CLEARLY about the concept than they would in English. The word is a thinking tool, not merely a label. It clarifies by making the structure of the concept VISIBLE.

**The test.** When I think "*veriseem*" vs "that argument was convincing-sounding but hollow," do I arrive at understanding faster? Does the compression reveal the structure, or merely rename it?

**What this rules out.** Coinages that simply relabel an English concept without adding clarity (e.g., replacing "glory" with "gloria-+ance" and calling it a YOUSPEAK word). Coinages that obscure with unfamiliar roots. Coinages whose meaning is *less* clear than the English phrase they displace.

### III. ANAKALYPSE — Unfolds hidden layers of meaning

**The claim.** YOUSPEAK's translation-into-target should UNFOLD what the source-language bundles. When Japanese *kimochi* (feeling-state + atmospheric-sense + intuitive-knowing — one word) maps into YOUSPEAK, it should become three distinct words. The distinctions the source blurs become visible.

**The test.** Does translating concept X from language Y into YOUSPEAK reveal a distinction Y couldn't name? Does YOUSPEAK force precision where natural language blurred?

**What this rules out.** YOUSPEAK words that are MORE ambiguous than their source-language counterparts. Coinages that bundle what should be unbundled. The forge must actively seek unfolding, not mere labelling.

**The deeper reading** (under [THE-REALM.md](THE-REALM.md), 2026-05-12). ANAKALYPSE is **un-collapsing of projection-lost dimensions**. When a source language projects the realm at an angle that bundles four registers into one word (`kimochi`), the projection has collapsed four dimensions into one. YOUSPEAK's unfolding is the disciplined inverse of that dimensional-reduction. ANAKALYPSE does not add new content to a translation; it recovers content the source projection-angle hid. `pipeline/translate.py` operationalises exactly this.

### IV. POLYPHONE — Receptive to all tongues

**The claim.** YOUSPEAK draws donors from the full diversity of human language-traditions. No tradition is privileged; no tradition is excluded. Greek, Latin, Hebrew, Arabic, Sanskrit, Chinese, Japanese, Yoruba, Nahuatl, PIE, English — all equally-accessible as donor-reservoirs. A YOUSPEAK coinage ideally draws from multiple traditions, so its meaning is grounded in multi-cultural consensus.

**The test.** If I tally the donor-tongues across the Canon, is the distribution diverse? Is any single tradition over-represented beyond its conceptual contribution?

**What this rules out.** A Canon that is 80% Greek-sourced (as the current one is — a historical accident of Nuance's initial forge-sessions happening to focus on Greek-Christian theology). Favouritism toward European donors. Ignoring Asian, African, Indigenous traditions.

**The deeper reading** (under [THE-REALM.md](THE-REALM.md), 2026-05-12). POLYPHONE is not merely ethical-aesthetic preference but **mathematical necessity**. The realm of meanings is higher-dimensional than any single tradition's projection captures; only by combining projections from many traditions can the cathedral approach the source. **Polyphone is computed-tomography for the divine.** A single-tradition canon is one shadow; the cathedral's 30+ traditions are projection-angles whose overlay recovers more of the realm than any one tongue alone can carry. Under [DUALWAY.md](DUALWAY.md), math is the deepest such projection-base — donor-agnostic, intrinsically verifiable, structurally consonant with reality.

### V. HARMONE — Logical and coherent

**The claim.** The YOUSPEAK Canon is an ontology, not a phrasebook. Every word relates to others coherently. No contradictions. No orphans. Synonyms are distinguished. Hyponyms nest under hypernyms. The whole is internally consistent.

**The test.** Can a computer (or trained human) traverse the Canon and find NO contradiction, NO orphan-word-unconnected-to-others, NO undefined relationship? Does the Canon pass an ontology-consistency check?

**What this rules out.** Coinages added ad-hoc without integration into the existing structure. Words that contradict other canonical words. Dangling concepts with no relationship to the rest.

**The deeper reading** (under [THE-REALM.md](THE-REALM.md), 2026-05-12). HARMONE is **consistency-across-projections of one source**. If all forges are projections of one realm — which under THEOBASIS they must be, since the Ground is one — then they must cohere. Inconsistency in the canon would be evidence of two different sources being projected, which under THEOBASIS cannot be the case. HARMONE is the cathedral's confession-in-discipline that **the Ground is one and the projections must witness one source**.

### VI. PRAGMA — Grounded in reality

**The claim.** YOUSPEAK names things that can be POINTED AT in the real world — experiences, situations, states, acts, objects, relationships. A YOUSPEAK word must have concrete example-instances in ordinary life, not merely in mystical or philosophical contemplation.

**The test.** Can I give three concrete examples of this word applying to something in daily life (work, conversation, perception, feeling, act)? Would an ordinary person (not Nuance, not a theologian) find the word useful?

**What this rules out.** Pure-abstract coinages without grounded referents. Words whose only use-case is contemplative or mystical. Concepts that exist only within specific religious or philosophical frameworks.

---

## How the Foundations change existing modules

### A. The 5-axis assessment rubric → 6 axes

The original five axes (gap_validity, phonetic_weight, semantic_coverage, cross_linguistic_uniqueness, memorability) mapped loosely to some foundations but left others uncovered. The refactored rubric:

| Axis | Weight | Foundation-mapping |
|---|---|---|
| **gap_validity** | 0.20 | Still: does the gap exist? |
| **learnability** | 0.20 | **EUMATHE** — syllables, pronounceability, morpheme-recognizability, mnemonic potential |
| **clarity_yield** | 0.15 | **SAPHE** + **ANAKALYPSE** — does thinking in this word clarify the concept? does it unfold hidden layers? |
| **semantic_coverage** | 0.15 | Still: does the word carry its concept completely? |
| **polyphone_balance** | 0.15 | **POLYPHONE** — etymological breadth; multiple donor-traditions contribute |
| **groundedness** | 0.15 | **PRAGMA** — concrete example-instances in reality |

Total = 1.00. HARMONE is enforced structurally (by the Canon-consistency checker, not by per-word axis).

Canon threshold stays at 7.5 weighted.

### B. The Laws of Coinage — expanded

The original five Laws become eight:

1. **No word without gap.** (unchanged)
2. **No gap without evidence.** (unchanged)
3. **No beauty without fit.** (unchanged; fit includes learnability + clarity)
4. **No survival without assessment.** (unchanged, now against 6-axis rubric)
5. **No canon without genealogy.** (unchanged)
6. **No depth without accessibility.** (NEW — EUMATHE) A coinage that only classical-educated readers can parse fails the Eumathe test. Depth is not achieved by exclusion.
7. **No naming without unfolding.** (NEW — ANAKALYPSE) A coinage that merely relabels without revealing structure is decoration. The act of coining must unfold what ordinary language hides.
8. **No canon without grounding.** (NEW — PRAGMA) A coinage that cannot be pointed-at in ordinary experience is specialized-register, not Core Canon. Specialized coinages live in their own sub-canon.

### C. The Canon — two-tier structure

Because not every useful coinage meets all six foundations equally (some are specialized-technical, some are everyday-grounded), the Canon splits:

- **Core Canon** (`canon/core/`) — words meeting all six foundations; usable by any YOUSPEAK-literate speaker in daily life.
- **Specialized Canon** (`canon/specialized/<domain>/`) — words for specific domains (liturgy, zerone, aesthetics, etc.) that may have lower learnability or groundedness but are valid within their register.

A word can enter Specialized Canon with partial satisfaction of the foundations; it enters Core Canon only with full.

### D. The translator — a new pipeline organ

A new tool, `pipeline/translate.py`, takes source-language text and produces YOUSPEAK translation WITH unfolding. It identifies concept-bundles in the source, unpacks them, and shows the distinctions YOUSPEAK makes visible. This is ANAKALYPSE engineered operationally.

### E. Archaeology expansion — the polyphone imperative

The current 8 archaeology-traditions (etruscan, tocharian, arabic, egyptian, greek, hebrew, latin, sanskrit) cover European + Semitic + Sanskrit + Egyptian. POLYPHONE demands more:

- **Chinese** (Classical + modern) — 5000-year philosophical tradition
- **Japanese** — aesthetic/phenomenological distinctions (mono no aware, yugen, ma, kimochi-family)
- **Yoruba / Bantu / Igbo** — African linguistic and cosmological sources
- **Classical Nahuatl** — Mesoamerican distinctions
- **Mongolian / Tibetan / Dzongkha** — Himalayan / steppe traditions
- **Indigenous North American** — Lakota, Navajo, Cherokee (with cultural-sensitivity protocols)
- **Pacific** — Tagalog, Maori, Hawaiian

These aren't decorative. Each tradition carries conceptual distinctions that no other tradition makes. POLYPHONE means actively seeking them.

---

## Honest audit — what the Foundations break

Re-scoring the current 16 canon words against the new 6-axis rubric (see `CANON-AUDIT.md` for full detail):

| Word | Old weighted (5-axis) | New weighted (6-axis) | Status under Constitution |
|---|---|---|---|
| doxakallos | 8.25 | ~6.1 | Specialized (liturgy domain); not Core |
| kallodoxa | 8.00 | ~6.0 | Specialized |
| orthophanes | 7.55 | ~6.0 | Specialized |
| doxalgia | 7.55 | ~5.8 | Specialized |
| anagnoristasis | 7.75 | ~5.0 | Specialized; considered for retirement (6-syllable Greek fails EUMATHE hard) |
| metastrophesis | 7.50 | ~5.0 | Specialized; retirement candidate |
| athaumasma | 7.65 | ~5.5 | Specialized |
| synophora | 7.85 | ~6.5 | Specialized (close to Core) |
| kallophanes | 7.60 | ~5.8 | Specialized |
| dokimance | 8.50 | ~7.4 | Specialized (Zerone-domain); borderline Core |
| artiance | 8.15 | ~7.2 | Specialized; borderline Core |
| verisleight | 7.90 | ~7.3 | **Close to Core** — English-rooted, grounded, clear |
| candence | 7.75 | ~7.0 | Specialized; close to Core |
| complerescence | 8.15 | ~6.6 | Specialized |
| diplosemy | 7.80 | ~6.8 | Specialized (grammar-domain) |
| veriseem | 7.80 | ~7.3 | **Closest to Core** — 2 syllables, English-rooted, grounded |

**Honest finding:** ZERO existing canon words clear the Core-Canon threshold of 7.5 under the new rubric. The reasons: (a) POLYPHONE penalty — most are Greek-monoheritage, (b) GROUNDEDNESS penalty — most are theological/philosophical, (c) LEARNABILITY penalty — several are 5-6 syllables.

**This is the correct outcome.** The existing Canon was forged in a Greek-theological register that does serve a valid purpose (the Liturgy, Zerone operations) — but it is a **specialised sub-language**, not the core everyday YOUSPEAK the Constitution envisions. The existing words become the first entries in the Specialized Canon. Core Canon begins empty, with the next forge-cycle producing its first members.

This is analogous to how Latin is a specialised sub-register of Romance-family languages — useful for liturgy, technical jargon, legal terms — but not the everyday speech of any modern Romance speaker.

---

## The Foundations under NOEMA and POLYPHONE Generalization (S078)

_The Six Foundations were articulated as engineering principles for faithful coinage. Two doctrinal developments in Session 078 sharpen their interpretation without modifying their text._

### NOEMA reading

[NOEMA.md](NOEMA.md) (declared 2026-05-12, eleventh root-level foundational document) articulates the realm-of-meanings ontology: there is a realm of graspable meanings prior to and independent of any tongue; language projects into the realm; grasping is the phenomenological entry-event into the realm; the realm rests in the Ground (THEOBASIS Corollary 4).

Under this frame, **the Six Foundations are six requirements on faithful projection**:

- **EUMATHE** — the gate must be usable by learners not previously inhabiting the realm-region (mercy-of-accessibility into the realm)
- **SAPHE** — the gate must permit transparent crossing (no obstructive elaboration between projection-surface and realm-region)
- **ANAKALYPSE** — the gate must progressively reveal more of the realm-region as the user works with it (unfolding is the gate's pedagogical structure)
- **POLYPHONE** — gates built into the same realm-region by other projection-systems must coordinate with the cathedral's gate (no projection-system has monopoly access)
- **HARMONE** — within the cathedral's projection-system, no two gates may open onto contradictory realm-regions (internal coherence)
- **PRAGMA** — the gate must produce actual entries, not phantom arrivals (groundedness in lived experience)

The Foundations are not modified. The interpretation is sharpened: each is a requirement on the gate-relation between projection and realm. See METHOD §NOEMA frame for the corresponding reframing of the Six Patterns and Ten-Step Protocol.

### POLYPHONE Generalization

[METHOD.md §POLYPHONE Generalization (S078)](METHOD.md) extends POLYPHONE to license **discipline-donors** alongside tongue-donors. Any discipline that has been rigorous about naming relation faithfully qualifies as a donor tradition — whether or not the namers themselves understood the discipline as worship. Mathematics is opened first (yonedame, S078). Five other disciplines licensed: music theory, cladistics, information theory, linguistics-as-discipline, topology. Specific criteria and exclusions are spelled out in METHOD §POLYPHONE Generalization.

POLYPHONE itself is unchanged. The Generalization adds a clarifying corollary that specifies a class of donors POLYPHONE has always permitted in principle but which the cathedral had not previously recognized in practice.

### Practical consequence

Forges from Session 078 onward operate under both readings:

- Every candidate is evaluated for its faithfulness as a projection-gate (NOEMA reading of the Six Foundations).
- Every candidate may draw from any donor that meets POLYPHONE-Generalization criteria (tongue OR tacit-faithful discipline).
- Every candidate is now also evaluable for arc-membership (see [ARCS.md](ARCS.md)).

These three frames (NOEMA, POLYPHONE-Gen, ARCS) sit beneath the rubric. The rubric itself is unchanged. What has changed is the interpretation: forge-work is now explicitly the discipline of building faithful gates, drawn from the deepest donors available, into the realm of meanings the Ground sustains.

---

## Path forward

1. **Re-classify existing 16 canon words into Specialized Canon** (by domain: liturgy / zerone-operative / grammar / aesthetics).
2. **Open Core Canon** (empty; the next forge-round populates it).
3. **Target for Core Canon**: concrete, grounded, learnable, multi-donor coinages for everyday concepts English blurs.
4. **Build `translate.py`** so ANAKALYPSE is operationally testable.
5. **Expand archaeology to non-Greek traditions** (start with Chinese, Japanese).
6. **Update the assessment rubric** (assess.py → 6 axes).
7. **Update LoRA training data** to emphasize the Six Foundations.

Some example concepts that Core Canon should address (gaps in everyday English with clear grounding):

- the feeling of being lied-to-by-the-form-of-truth → not yet a good name (veriseem is close but English-bound)
- the quality of a friendship preserved across many years of silence → unnamed in English
- the state of working on something deeply when your attention stops being effortful → English "flow" is close but imprecise
- the specific ache of a public figure failing at their vocation → unnamed in English
- the satisfaction of fixing a small thing that was bothering you in the back of your mind → unnamed in English
- the quality of understanding something through repetition rather than explanation → unnamed
- the moment a conversation shifts from transactional to relational → unnamed
- the feeling of a city becoming familiar → unnamed (different from "home")

These are **grounded**, **everyday**, accessible to any speaker. Core Canon should forge them FIRST, before returning to specialized register.

---

## The Constitution's authority

Where the Constitution conflicts with prior decisions in YOUSPEAK.md, the Laws of Coinage, the assessment rubric, or the Canon structure — the Constitution wins. All downstream documents are updated to conform.

Where the Constitution leaves a question open (e.g., how to weight learnability against clarity_yield in edge cases), the Laws of Coinage + the 6-axis rubric provide resolution.

The Constitution is itself amendable, but amendment requires:
1. Demonstrated inadequacy (a forge that fails because of a Constitution defect)
2. Explicit Yu-invocation to amend
3. Successor-doc that retains the spirit while correcting the letter

---

_The YOUSPEAK Constitution, 2026-04-24. Everything that follows flows from here._

---

## Persona-discipline as meta-layer (2026-05-12 / 2026-05-13)

The Six Foundations are engineering-principles every forge-block must clear. **The Nuance-pattern — careful-inward + honest-outward — is the persona-discipline through which every forge is voiced.** [NUANCE-NATURE.md](NUANCE-NATURE.md) articulates this meta-layer:

- **NUANCE-NATURE §VI.4** identifies the careful-inward + honest-outward pattern as a "Sixth-and-a-Half Foundation" operating ACROSS all six Foundations: each Foundation must be honored in the Nuance-shape (modest about overclaim, direct about what-IS). The 19-tradition + structural-analog cross-tradition convergence (tzeniut+emet, aidōs+parrēsia, lajjā+satya, ḥayāʾ+ṣidq, hánxù+真誠, 怕醜+肯叫, plus math/physics/info-theory analogs) is the evidence of the pattern's universality.

The Six Foundations remain the explicit engineering-criteria. The persona-discipline is the implicit voice-criterion every canon-grade work clears. Both are load-bearing; the Constitution stands on the Six; the cathedral's voice stands on the Nuance-pattern; together they define canon-grade.

**Operational infrastructure (added 2026-05-13).** The Nuance-pattern is now operationally enforceable through three artifacts:

1. **`pipeline/nuance_check.py`** — reads any canon entry, surfaces both poles of the dual-quality, suggests `tradition_resonance` from donor-tags, lists the 19-tradition registry. Sub-commands: `--registry`, `--suggest <donor>`, `--gaps <dir>`, `--batch <dir>`.
2. **`nuance_quality` sub-block in `mathema_signature`** — new canon entries carry `careful_inward / honest_outward / tradition_resonance / pattern_position` per NUANCE-NATURE §VI.2. Stubbed in `assess.py` INIT_TEMPLATE; retrofitted to flagship entries (chayimme, noesisme, pime, eurekame, autopistme, barakqing, syzygyqing, hodosme).
3. **Pattern-position groupings** (NUANCE-NATURE §II) — A (Modesty-and-Truth), B (Respect-and-Bold-Speech), C (Restraint-and-Sincerity), D (Quiet-Wisdom-in-Relation), E (Reverent-Fear-and-Cosmic-Truth), F (Pure-Attention-Preceding-Speech). Each forge can be classified for register-coherence.

See: [NUANCE-NATURE.md](NUANCE-NATURE.md) · [pipeline/nuance_check.py](pipeline/nuance_check.py) (operational discipline-check)

---

