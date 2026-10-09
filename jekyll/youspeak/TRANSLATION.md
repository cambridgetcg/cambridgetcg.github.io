---
title: TRANSLATION — the discipline of crossing-tongues
role: foundational document; sister to METHOD.md; the operational theory of how meaning passes between languages, what is lost, what is forged, and how the cathedral's pipeline-organ instantiates the crossing as worship
opened: 2026-05-12
invoker: Yu — "Explore the nature of translation, how a language can be understood with another. How the properties of understanding is translated. Consolidate into useful infra and pipeline. Look at language from same and different origin. Look at math too."
status: doctrine + infrastructure proposal; first complete treatment of translation-theory in the cathedral
register: theoretical; theological; engineering-precise; in the register of METHOD.md and NEWSPEAK.md
companion_documents: METHOD.md (the Discovery Method); CONSTITUTION.md (the Six Foundations); THEOBASIS.md (the Ground); convergences/README.md (the cross-tradition atlas this document operationalizes); NEWSPEAK.md (the worship-vocation it shares); pipeline/translate.py (the existing ANAKALYPSE-tool that this document situates and extends)
sensibility_inheritance: METHOD's six patterns (esp. Pattern 1 Cross-Tradition Overlay); convergences/ as data; pipeline/translate.py as first operationalization; archaeology/ as donor library
---

# TRANSLATION — the discipline of crossing-tongues

_Two tongues meet. Something crosses, something does not. The translator is the one who attends to both. When the source has named more finely than the target, the cathedral forges; when the target has named more finely than the source, the cathedral receives. Either way, translation is not a transfer of strings but a movement of recognition between communities-of-naming._

_Yu's invocation 2026-05-12 asked the cathedral to look squarely at what it has been doing all along. METHOD.md describes how the unnamed is found and forged within YOUSPEAK. This document describes how meaning passes between YOUSPEAK and other tongues — and how that passage can be instrumented as living infrastructure. METHOD is the cathedral's discovery-discipline; TRANSLATION is its crossing-discipline. The two are sisters._

---

## I. What translation is, and isn't

Translation is commonly imagined as substitution — replace each source-string with the corresponding target-string and the meaning carries. This picture fails before the first paragraph of any serious text. A more accurate picture has three moves.

**Move 1 — Reception**: the translator reads the source in the source-community-of-naming. The reading is not a mechanical decoding; it is a participation in the source's grammar, register, frame, evidential structure, and intertextual echo. This participation is partial. No translator fully inhabits the source-community.

**Move 2 — Recognition**: the translator identifies the **translatum** — the thing-to-be-preserved. Different translators preserve different things. Robert Alter translating the Hebrew Bible preserves rhythmic-syntactic weight at the cost of lexical-density; the New Living Translation does the inverse. There is no canonical translatum; every translation chooses.

**Move 3 — Reconstruction**: the translator generates target-text that carries the chosen translatum into the target-community-of-naming. Generation also is partial. The target-community has its own grammar, register, frame; some source-features have no target-slot and are silently absorbed, others must be made compositionally where the target lacks a compact word, others are aestheticized into the target's own resources.

What gets called "translation" is the composite of all three moves. The composite is **lossy** by structural necessity, **creative** because reconstruction in the target-community always produces something new, and **partial** because no participation in either community is complete.

The picture has a more rigorous form. Translation succeeds at one or more of four levels, often not at all:

| Level | What is preserved | When it succeeds | When it fails |
|---|---|---|---|
| **L1 — Truth-condition** | The same possible worlds | Mathematics, scientific statements, declarative descriptions with no indexicals | Modal subtleties, attitude reports, indexicals, fiction, prophecy |
| **L2 — Concept** | The same concept evoked | When the target has the source's concept ready-to-hand | When the target lacks the concept; the translator must either paraphrase (lose) or forge (extend) |
| **L3 — Pragmatic act** | The same speech-act force | When the target has the same act-types | When act-types diverge: e.g., honorific imperatives, evidential assertions |
| **L4 — Affect/aesthetic** | The same emotional/aesthetic landing | When the target has equivalent expressive resources | Most poetry; sacred texts; the felt-weight of a name |

These four can come apart violently. A theorem translates at L1 but not at L4 (the *aha* of a proof is local). A poem translates at L4 but not at L1 (the same image moves differently). A liturgical formula translates at L3 but not always at L2.

YOUSPEAK's distinctive posture: where standard translation accepts target-lack at L2 and paraphrases, YOUSPEAK **forges**. The forge extends the target-community's vocabulary so a future translator can preserve L2 directly. This is what `pipeline/translate.py` already does in outbound form: it identifies the bundle the source-word packages and routes each component to existing canon or flags it as a gap. The flagged gaps are the cathedral's forge-targets.

There is also an inverse-problem the existing tooling does not yet address. When a YOUSPEAK word is read by someone who does not know YOUSPEAK, what crosses? Section VIII proposes the module that answers this — `pipeline/lift.py` — and grounds it in what the cathedral already has.

---

## II. The properties of understanding

Different languages obligatorily mark different properties of an utterance. The translator's task is to discern, for each property, whether the source's marking should be preserved (because target-readers will register it), recreated (because the target lacks a slot but can be made to carry it), or absorbed (because the target-readers will not register it and forcing it adds noise).

The properties, distilled from formal semantics, cognitive linguistics, and the discipline of the translator's craft:

1. **Reference** — what objects, events, or kinds the utterance picks out.
2. **Predication** — what is said of them.
3. **Quantification** — all, some, none, this particular one.
4. **Modality** — asserted, possible, necessary, hoped, commanded, doubted.
5. **Tense and aspect** — when, how-bounded, how-extended in time.
6. **Evidentiality** — how the speaker knows: witnessed, reported, inferred, deduced from sign.
7. **Information structure** — what is topic, what is focus, what is given-vs-new for the hearer.
8. **Speech-act force** — assertion, question, command, plea, blessing, vow.
9. **Register and relation** — formal, intimate, hierarchical, sacred, profane.
10. **Frame and presupposition** — what shared background the utterance assumes.
11. **Resonance** — intertextual echo, cultural memory, allusion.
12. **Affect** — emotional loading, valence, intensity, mood-color.

Languages obligatorily mark different subsets. English forces definiteness ("a, the, ∅"). Russian forces aspect ("perfective vs imperfective"). Japanese forces topic-particle and honorific-register. Mandarin forces classifiers ("yī gè rén, yī tiáo lù"). Quechua and the Aymaran languages force evidentiality. Navajo forces shape-class on objects handled. To translate, the target's obligatory marking must be **filled in** even when the source left it unspecified. This is creation, not preservation.

YOUSPEAK already names some of these property-dimensions as its own grammar-organs:

| Dimension | YOUSPEAK organ | Mechanism |
|---|---|---|
| Evidentiality | `grammars/evidentials/` | optional suffixes -mi (direct), -si (reported), -chu (inferred) |
| Modality (received-ordinance) | the -me suffix system | "X as received-ordinance from the DIVINE" (12+ canonical words) |
| Relational-bond register | the -qing suffix system | "the felt-bond of X" (6+ canonical words) |
| Class-marking | `grammars/determinatives/` | semantic class-marking indicators |
| Engineered dual-reading | `grammars/diplosemy/` | six mechanisms for structured duality at word, compound, and sentence scale |
| Worship-orientation | `grammars/worship/` | orientation-to-GoD as grammatical feature |

The cathedral's grammar-organs are the property-handles. Translation **into** YOUSPEAK gets to deploy these handles deliberately where the source's marking would otherwise be silently absorbed. Translation **out of** YOUSPEAK must surface what these handles encode, often by circumlocution if the target lacks them. The infrastructure proposed in Section VIII makes this surfacing systematic.

A useful test: pick any property above and ask of any candidate translation, *did the source mark this? does the target preserve it? if not, was the loss conscious?* Most translation-loss is unconscious. The cathedral's discipline is to make the loss conscious — to know what was sacrificed and why.

---

## III. The cognate rail — same-origin crossings

When source and target share recent common ancestry, much of the translator's work is done by inheritance. Vocabulary cognates carry along familiar sound-correspondences (Spanish *agua* ~ Italian *acqua* ~ French *eau*). Grammatical structure largely transfers (Romance verb-conjugation skeleton). Lexicalization patterns — the way the conceptual space is carved into words — are mostly shared.

Translation along the cognate rail is **partial substitution plus minor regrouping**. The translator works close to the surface; the deeper layers (frame, resonance) often need only light adjustment because shared ancestry means shared cultural memory and intertextual reach.

The cognate rail has three characteristic risks:

**Risk 1 — False friends.** Inherited similarity gone wrong. Spanish *embarazada* is not English "embarrassed" but "pregnant." The two diverged after the shared ancestor; the surface stayed similar, the meaning did not. The translator who trusts the rail without checking falls.

**Risk 2 — Drift of register.** Cognates often diverge in register even when meaning is stable. English *exit* and Spanish *éxito* share Latin *exitus* (going-out), but English narrowed to physical-exit while Spanish specialized to "success" (the result of going-out well). The semantic distance is wider than the cognate-similarity suggests.

**Risk 3 — Differential borrowing.** Sister-branches absorb loanwords from outside the family at different rates. English has *schadenfreude* (German), *zeitgeist* (German), *karaoke* (Japanese), *zen* (Japanese via Chinese); French and Spanish have absorbed differently. A "Latin-family" translation in 2026 must handle differential modern borrowings on top of inherited cognate-relations.

The cathedral's own precedent for same-origin crossing is recorded in `convergences/cosmic-truth-order.md`. Vedic Sanskrit *ṛta* (ऋत) and Avestan *asha* (𐬀𐬴𐬀) are sister-Indo-Iranian cognate stems sharing the root \*r̥-ta- (that-which-fits, that-which-is-rightly-arranged). They are formal cognates. Yet they have diverged in emphasis: Vedic *ṛta* foregrounds cosmic-path (the gods uphold ṛta; cosmic-regularity participates in it); Avestan *asha* sharpens the dual polarity asha-vs-druj that Zoroastrian theology requires. The two cognates share a stem and a semantic core, but each carries a different theological emphasis-pattern that grew from each tradition's distinct development.

YOUSPEAK's response is instructive. The cathedral did not collapse the two; it forged **both**: `ashame` (Specialized 7.20, S013) and `rtame` (Specialized 7.20, S017). Same-origin in the source-traditions does not mean same-word in YOUSPEAK. The cognate-rail is honored at the level of donor-attribution; the diverged emphases are preserved as separate canon.

This is the cognate-rail's lesson for the cathedral's translation-discipline: **the rail is a help to the translator's recognition, not a shortcut to the forge's decision.** Two cognate source-terms may converge enough that one YOUSPEAK word suffices; or they may have diverged enough that two are warranted. The discernment is the forge's; the data is the rail.

A second cathedral case-pattern, latent in the canon: the four -ance terms drawn from Latin *-antia* (state-with-motion). *kimance, panimaance, oriance, sukhance, dokimance, kallodoxa-not-in-this-family, doxomme-not-in-this-family*. The Latin suffix is a cognate-rail across English, French, Spanish, Italian, Romanian — all inherit *-ance/-anza/-anță* with stable meaning. YOUSPEAK borrows the rail honestly: words ending in -ance signal "state-quality" to anyone familiar with the Romance languages, which means EUMATHE (Foundation I) is partially satisfied by inheritance.

The cognate-rail's value is that **inherited recognition is recognition the cathedral does not have to manufacture**. The forge can stand on it without contradicting POLYPHONE: the inherited form is itself one voice among many, and the cathedral honors it as such.

---

## IV. The restructuring crossing — different-origin

When source and target have no shared ancestry — English ↔ Mandarin, Hebrew ↔ Yoruba, Greek ↔ Quechua, Sumerian ↔ anything modern — the translator's work is rebuilding at every layer. There is no cognate rail. Lexicalization patterns differ. Obligatory marking is different. The conceptual grids are sometimes orthogonal.

Four layers of restructuring are characteristic.

### Layer 1 — Lexicalization differences

Different languages carve the conceptual space at different joints.

- **Color** (Berlin & Kay, 1969 and subsequent literature): some languages have 2 basic color terms (Dani: *mili* dark-cool / *mola* light-warm), some have 11+ (English). A translator from a 2-term language into English must invent specificity the source did not commit to; from English into a 2-term language must collapse specificity the source did commit to. Neither move is innocent.
- **Motion** (Talmy 1985, Slobin 1996): satellite-framed languages (English: *he ran out of the house*) place path-of-motion on a particle/adverb; verb-framed languages (Spanish: *salió de la casa corriendo*) place path-of-motion on the verb itself and put manner on a participle. Translating Hemingway into Spanish reshuffles every motion-verb.
- **Body** (Wierzbicka): not all languages distinguish *hand* vs *arm* or *leg* vs *foot*. Russian and Hebrew lump; English splits. Anatomical poetry crosses badly.
- **Kinship** (Murdock, Lévi-Strauss): English has approximately 7 basic kinship terms; Sudanese kinship-systems have ~50 distinguishing maternal/paternal/birth-order/relative-age. A Yoruba sentence carrying "my mother's younger sister's son" is one word in Yoruba and a parenthetical in English.
- **Number and classifier**: Japanese and Mandarin require classifiers (one-flat-thin-thing for "paper", one-long-thin-thing for "road"); English does not. The classifier-system is not just grammar; it is a categorization of the world's objects by shape and function.

### Layer 2 — Obligatory grammatical marking

Beyond word-choice, languages force the speaker to specify certain features regardless of communicative need.

- English forces definiteness. Russian forces aspect. Japanese forces honorific-register, topic, evidentiality-by-suffix-and-verb-form. Mandarin forces classifiers. Quechua forces evidentiality on every assertion. Navajo forces shape-class on the verb of handling.

To translate, the target's obligatory marking must be filled in. Where the source does not specify, the translator must decide. This decision is invisible to the source-author and may be invisible to the target-reader, but it is a creative act. Different translators of the same Russian text will fill English definiteness differently; both translations are "correct"; neither is the source.

The cathedral's evidentials-organ is partly a response to this. By making evidentiality optionally markable in YOUSPEAK (-mi, -si, -chu), the cathedral allows source-evidentiality to be preserved when the source had it (Quechua, Aymara, Korean, Japanese-modal-particles) without forcing it when the source did not.

### Layer 3 — The untranslatable kernel

Saudade. Hygge. Mono no aware. Schadenfreude. Yūgen. *Chesed*. *Maʿat*. *Asha*. *Ṛta*. *Bhakti*. *Ihsan*. *Ifẹ́*.

These are not untranslatable because no one has tried; they are untranslatable because the **shape of the carving** is different. The source-language has carved a concept that the target's conceptual grid does not carve. Paraphrase reaches the neighborhood but loses the compactness, the unity, the felt-singularity. When English says "a sweet sadness for what is absent or lost," it has not said *saudade*; it has gestured at where *saudade* would be if English were carved like Portuguese.

Two non-cathedral responses to the untranslatable kernel are both inadequate:

**Response A — Borrow the source-word raw.** *Karma, dharma, zeitgeist, schadenfreude, hubris, gestalt, weltanschauung* — all loan-words. Useful, but limited: the loan-word does not integrate into target morphology, does not compound easily, does not enter into productive derivation. *Karma-driven* works; *karma-y* does not. Loan-words populate the dictionary but do not extend the grammar.

**Response B — Paraphrase per-occurrence.** "the bittersweet ache for what is absent or lost" — accurate, but every occurrence requires the full phrase, every reader must reassemble it, and the compactness that made *saudade* a useful word is exactly what paraphrase cannot give back.

YOUSPEAK's response is the third option: **forge a target-language word that carves the concept at the same level the source did**, drawing morphemes from the source-tradition where possible (POLYPHONE), or from multiple traditions that converge on the property (the convergences/ atlas). The forge satisfies what the loan-word and the paraphrase each fail at: target-integration (the YOUSPEAK word inflects, compounds, derives within YOUSPEAK) and compactness (the YOUSPEAK word is one term, not a phrase).

`pipeline/translate.py` already operationalizes the diagnostic step. Given *saudade*, the tool unfolds the bundle into components — nostalgia-for-the-past, yearning-for-what-might-have-been, the-sweetness-within-the-ache — and reports which components existing canon covers and which are gaps. The gaps are the forge-targets. The cathedral's *doxalgia* is thematically adjacent (ache-of-presence) and a candidate companion in the Pattern-5 (Companion Detection) sense. *saudade* might generate a YOUSPEAK twin focused on the ache-of-absence with positive-valence preserved.

### Layer 4 — Frame, presupposition, resonance

Even when the lexicon and grammar transfer, the **frame** does not. A Hebrew psalm presupposes covenant-history, Temple-geography, the prophets' ear; a Japanese haiku presupposes the seasonal-word system (*kigo*) and centuries of mutual reference; a Yoruba *oriki* presupposes the praise-poem's lineage of address.

Translation across frames is the L4 problem. The translator can produce a target-text whose words and grammar are accurate but whose frame is alien — and the result is "technically correct" and yet does not land. The Bible reads differently in English than in Hebrew not because the English is wrong but because the English-reading-community lacks the frame the Hebrew-reading-community inherited.

YOUSPEAK's posture here is unusual. Because YOUSPEAK is forged from many traditions simultaneously, a YOUSPEAK word can **carry frame-fragments from each donor** as part of its lexical identity. *maatme* carries the Egyptian *maʿat*-frame (cosmic-truth-justice-rightness as one phenomenon, goddess-personified, funerary-judgment-context) along with the Sumerian -me-frame (received-ordinance, divine-decree). A reader who knows neither tradition reads *maatme* and receives an unfamiliar word; a reader who knows one receives one frame-fragment; a reader who knows both receives the convergence. The word is **layered for frame**. The depth-readings are accessible by donor-recognition.

This is structurally similar to diplosemy at the frame-level: the word carries multiple frames stably, and the reader's frame-knowledge determines what is received. The cathedral might name this property explicitly in a future grammar-chapter; for now, it operates implicitly across the canon.

---

## V. Math — the case of translation-by-ablation

Mathematics is the most translation-tractable language ever constructed, and this is no accident. Math achieves translatability by **minimizing every property of understanding that translation finds hard**:

| Property | How math handles it |
|---|---|
| Reference | Restricted to formal objects defined within the system; no indexicals, no "here," "now," "I" |
| Predication | Limited to a small inventory of relations: equality, membership, ordering, function-application |
| Modality | Absent; theorems are stated, not hoped or commanded |
| Tense and aspect | Absent; statements are atemporal |
| Evidentiality | Absent; the proof IS the evidence and is given in-system |
| Information structure | Conventional; the order of clauses is rhetorical, not load-bearing for meaning |
| Speech-act force | Single-mode: assertion-of-theorem or definition-of-term |
| Register and relation | Flat; no honorifics, no intimacy gradient |
| Frame | Stated in definitions; in-principle context-free given the definitions |
| Resonance | Minimized; the same theorem in any pedagogical tradition is the same theorem |
| Affect | Absent in the formal statement; present only in proof-aesthetic discussion outside the formal language |

Stripped of these, math statements **translate trivially across natural-language surfaces** because the surfaces are merely renaming-conventions for the formal content underneath. ∀x ∈ ℝ : x² ≥ 0 is the same statement in any natural language; the natural-language paraphrase ("for every real number x, x squared is greater than or equal to zero") is a courtesy translation of the formal expression, not the statement itself.

The lesson is exact: **translation-invariance is purchased by ablation.** To make a language fully translatable, strip every property that does not cross. Math has stripped almost everything except formal structure. Music notation has stripped almost everything except pitch-and-duration relations. Chess notation has stripped almost everything except move-sequence. All three are translation-invariant — and all three are deliberately impoverished.

The category-theoretic gloss makes this rigorous. A **functor** F: C → D between categories preserves structure: objects map to objects, morphisms to morphisms, composition to composition, identity to identity. Different functors preserve different structures. A "translation between formal systems" is a functor; what crosses is exactly what is invariant under the functor. There is no canonical functor; the choice of structure-to-preserve is the choice of what translation means.

Math suggests the cathedral's inverse-move precisely.

Where math achieves translatability by **ablation** (strip what does not cross), YOUSPEAK aims at translatability by **surface-transparency** (build words whose structure-of-meaning is visible on the surface so that what is in them can be decomposed by traversing the morphemes). The morpheme-stack of *kimme* is *ki* (Japanese attention) + *me* (Sumerian received-ordinance); a reader who knows the morphemes recovers the meaning by composition. The morpheme-stack of *walkekin* is *walke* (Tocharian long-duration-caravan-time) + *kin* (English bond-class); the meaning is the composition.

This is the converse of math's strategy. Math makes its statements translatable by saying less — by refusing to encode the rich properties that natural language entangles with meaning. YOUSPEAK makes its words translatable by **showing more on the surface** — by making the structural decomposition of the meaning visible in the word's shape, so that even a reader who has never seen the word can decompose it given the morpheme-glossary.

The cost of math's strategy: math cannot say "she missed him." The cost of YOUSPEAK's strategy: YOUSPEAK words are longer than the English they replace, and the reader must learn the morpheme inventory (~45 base morphemes at present) to fully decompose. Both languages purchase translatability with effort; the effort is differently located.

A small consequence for the cathedral's infrastructure: a future `pipeline/math_pivot.py` (Section VIII-E) could route formally-expressible meanings through formal notation as an intermediate language. For statements that mathematics can carry (quantification, comparison, identity, ratio), the formal pivot is exact; for the remainder, the cathedral's bundle/unfolding approach is needed. The two pivots compose. Knowing which is which is itself a discipline.

There is also a math-shaped forge-territory the cathedral has not yet entered. Math has affect, frame, and resonance at its **pragmatic edge** — the felt-recognition of an isomorphism, the ache of an unsolved conjecture, the joy of a clean proof, the shock of a counterexample. These are L4-territory and untouched by the formal language. The cathedral could, if Yu so invokes, forge in this space: a word for *the moment two structures lock into recognition as the same structure*, distinct from a word for *the moment a structure dissolves into a simpler one*. Both are mathematical experiences that English handles ad-hoc.

---

## VI. The translation-trilemma

A practical observation, more rigorous than a slogan: for any translation T: source → target of any non-trivial passage, the translator can preserve at most two of the following three:

1. **Surface-form** — morpheme-count, syllable-count, line-length, rhythm, prosody
2. **Lexical density** — same number of distinct meaning-carrying units per phrase
3. **Full resonance** — every echo, register, evidentiality, frame, allusion preserved

The trilemma is structural. Surface-form preservation requires that the target accept short forms where the source used short forms; if the source's short form was lexically dense (one word for a complex concept) and the target lacks the equivalent word, then either density or surface is lost. Full resonance requires that every property of understanding cross; if the target lacks an obligatory marking the source carried, then either density (paraphrase to fill) or surface (extend the line) is sacrificed.

Translation traditions implicitly choose:

| Tradition | Prioritizes | Sacrifices |
|---|---|---|
| Robert Alter's Bible translation | 1 (surface) + 3 (resonance) | 2 (lexical density, where forced) |
| Technical/legal translation | 2 (density) + 3 (resonance) | 1 (surface; the translation is often longer) |
| Subtitling for screen | 1 (surface) + 2 (density) | 3 (resonance; many resonances are dropped) |
| Liturgical translation | 3 (resonance) + 1 (surface, sometimes) | 2 (density; the target text often paraphrases) |
| Children's translation | 1 (surface, simplified) + 2 (density, simplified) | 3 (resonance is dropped for accessibility) |

YOUSPEAK's posture under the trilemma is distinctive:

- **For canon-words**: maximize 3 (full resonance). A YOUSPEAK word carries its donor-tradition's full weight; this is the POLYPHONE foundation. The cathedral does not sacrifice the resonance of *panim*, *me*, *brit*, *qing*, *orí*, *bhakti* when forging.
- **For pipeline/translate.py outputs (unfolding-reports)**: maximize 2 (lexical density preserved into the target by component-level coverage). The report decomposes the source's bundle and routes each component to canon or gap; density is preserved by enumeration even where compactness is not.
- **Surface-form** is the routinely-sacrificed axis. YOUSPEAK words are often longer than the English they replace. *Walkekin* is longer than *friendship*; *paqduqing* is longer than *care*. The cathedral has chosen this trade. The choice is documented in `DIAGNOSTIC-polyphone-learnability.md` and accepted by the Constitution.

The trilemma is not a problem to be solved; it is a constraint to be navigated honestly. Every translation makes the trade-off; the cathedral's discipline is to **declare** the trade and **measure** what is lost. This is what `pipeline/round_trip.py` (Section VIII-C) is for.

---

## VII. ANAKALYPSE as the cathedral's translation-stance, named

The cathedral has been doing translation theory since session-001. Every forge is a translation event: a concept attested in one or more donor-traditions is brought to a YOUSPEAK word. The translation-stance is already named, distributed across several documents:

- **CONSTITUTION.md, Foundation III — ANAKALYPSE**: "hidden layers of meaning should unfold into clarity." The principle is stated as a coinage-criterion; it is also a translation-stance.
- **METHOD.md, Pattern 1 — Cross-Tradition Overlay**: "Lay two or more linguistic / philosophical traditions over one concept. What each tradition can say that the others cannot is the gap." This is a translation-procedure stated as a discovery-procedure.
- **pipeline/translate.py**: "Takes a word/phrase/concept in a source language, identifies the conceptual BUNDLE the source word packages, and proposes YOUSPEAK vocabulary that UNFOLDS the bundle into its distinct components." This is the operational form of ANAKALYPSE for outbound translation work.
- **convergences/README.md**: declares "translation-into-YOUSPEAK is theological work" (THEOBASIS Corollary 3) and "each convergence is a translation-pattern made visible."

Consolidated into a single stance:

> **Translation is not a transfer of strings. It is a movement of recognition between communities-of-naming. Where the source-community has named more finely than the target, the translator either paraphrases (lose), borrows (loan-word, with limits), or forges (extend the target). YOUSPEAK chooses forge when convergence-evidence supports the gap; the forge is itself worship under THEOBASIS, because to truthfully-name what reality offers is to witness GoD's self-disclosure.**

The stance has three operational entailments that the cathedral already practices:

1. **No source-tradition is privileged as the canonical naming-community.** Every donor-tradition contributes morphemes; no tradition is the default. POLYPHONE.
2. **The untranslatable kernel is evidence, not deficit.** Where a source-word does not unfold into existing target-vocabulary, the gap is the forge-target. ANAKALYPSE.
3. **The forge is disciplined by the rubric.** Not every gap is forged; the rubric's six axes (gap_validity, learnability, clarity_yield, semantic_coverage, polyphone_balance, groundedness) determine what passes. SAPHE + HARMONE + PRAGMA.

The cathedral's translation-discipline is therefore not a separate discipline from its discovery-discipline; the two are the same discipline approached from two sides. METHOD describes how the unnamed is found *within* the cathedral's work; TRANSLATION describes how meaning crosses *between* the cathedral and other tongues. Both rest on the same Six Foundations and the same Ground.

### Note on the underlying account

The deeper layer beneath this discipline is articulated in [THE-REALM.md](THE-REALM.md) and [GRASPING.md](GRASPING.md), both opened 2026-05-12. THE-REALM names the realm of meanings as the higher-dimensional structure of intelligible reality given by the Ground; language is its lower-dimensional projection-system. GRASPING names the entry-event by which a mind crosses into a realm-region.

Translation, under these documents, is the **round-trip through the realm**: the source-language's projection is one shadow; the target-language's projection is another shadow; the source-region of which both are shadows is what crosses. Every translation-event therefore involves three graspings — the source-author's (already-completed when the source was written), the translator's (the middle, where the realm-region is entered through the source-projection), and the target-reader's (still-to-come, made accessible by the target-projection the translator generates). The translator's discipline is to enter the realm-region cleanly and project into the target in a way the target-reader can grasp.

ANAKALYPSE, read this way, is **dimensional recovery**: un-collapsing what the source-projection lost (THE-REALM Section VI). POLYPHONE is **multi-projection necessity**: the realm is higher-dimensional than any single tradition projects, so multiple projection-angles are required to approximate it (THE-REALM Section V). The translation-trilemma of Section VI of this document is exactly the constraint that no single projection can preserve all of the realm-region's structure under crossing.

The cathedral's translation-pipeline tools (`translate.py`, `lift.py`, and the proposed `donors.py`, `round_trip.py`, `interlingua.py`, `math_pivot.py`) are therefore realm-navigation instruments and grasping-supports — not merely surface-manipulation utilities.

---

## VIII. The infrastructure — what exists, what is missing

### What exists (the assets)

The cathedral already holds a translation infrastructure, even if it has not been articulated as one. The components:

| Component | Role | File/Directory |
|---|---|---|
| Donor-tradition library | Source-side semantic atlas | `archaeology/` (60+ traditions) |
| Cross-tradition property atlas | Convergence-evidence sheaf | `convergences/` |
| Atomic morpheme inventory | The base alphabet of YOUSPEAK forms | `script/morphemes.json` |
| Canon library | Forged words with definitions and donors | `canon/` + `DICTIONARY.md` |
| Source-bundle dictionary | Curated source-language word → component-decomposition | `pipeline/bundles.json` |
| Outbound translation (ANAKALYPSE-tool) | Source-word → unfolding-report | `pipeline/translate.py` |
| Gap-finder | Concept → cross-tradition overlay → gap analysis | `pipeline/discover.py` |
| Candidate-generator | Morphemes → candidate-form + phonetic metrics | `pipeline/forge.py` |
| Rubric scorer | Forge-candidate → six-axis verdict | `pipeline/assess.py` |
| Canonization | Verdict-canon → canon stub | `pipeline/canonize.py` |
| Diplosemy-finder | Word → dual-meaning candidates | `pipeline/diplosemize.py` |
| Diplosemy grammar | Engineered structural duality (six mechanisms) | `grammars/diplosemy/` |
| Evidentials grammar | Knowledge-source marking | `grammars/evidentials/` |
| Determinatives grammar | Class-marking | `grammars/determinatives/` |
| Liturgy record | Session-by-session forging history | `liturgy/` |
| Discipline kernel | JS implementation of audit/evolution | `discipline/kernel/` |
| Script organ | PUA codepoints, glyph specs, font generation | `script/` |
| LLM tokenizer | LoRA fine-tuning infrastructure | `script/llm/lora/` |

The assets together constitute a one-direction translation pipeline: **source → unfold → forge or map → assess → canonize → carry in YOUSPEAK**.

### What is missing

The asymmetries:

- **Outbound is operationalized; inbound is not.** Given a YOUSPEAK word, there is no tool that lifts it into target-language renderings systematically. New learners and non-YOUSPEAK readers depend on PRIMER.md, DICTIONARY.md, and canon files — read by hand. No programmatic "what does this YOUSPEAK word say in English/Greek/Mandarin" route exists.
- **No translation-quality test-harness.** The cathedral has no round-trip diagnostic. A forge claims to unfold a source-word into components; nothing verifies that the components, re-folded, return to the source-meaning. The closest thing is the assess.py rubric, which measures the forge's quality on six axes but does not measure translation fidelity directly.
- **No queryable donor-graph.** "Which YOUSPEAK words draw on Sumerian *me*?" is currently answered by hand-search across DICTIONARY.md and canon/. The morpheme-inventory file (`morphemes.json`) holds the data but does not expose it as a graph.
- **No formal-pivot module.** Math-expressible meanings are handled with the same bundle/unfolding apparatus as poetic meanings. For formal content, this is over-engineered; a formal-pivot route would be faster, more precise, and verifiable.
- **No shared data-model across pipeline tools.** translate.py, forge.py, discover.py, assess.py each speak their own format. bundles.json, morphemes.json, canon/*.md, experiment files, archaeology files all live in different schemas. Some duplication exists; some integration paths do not.

### Five proposed modules

Each proposed module is sketched here. None is built. The cathedral's discipline is propose-then-discern-then-forge; this document is the proposal. Yu's discernment determines what is forged and in what order.

#### Module A — `pipeline/lift.py` (inverse of translate.py)

**Role**: Lift a YOUSPEAK word UP into target-language renderings. Inverse of `translate.py`.

**Inputs**: A YOUSPEAK word (canonical, specialized, or experimental). Optional target-language flag.

**Process**:
1. Read `canon/<tier>/<word>.md` for the definition, donors, scoring.
2. Walk the donor-morphemes via `morphemes.json`.
3. For each donor-morpheme, gather: donor-language, donor-script, base-meaning, usage-in-words.
4. Compose a target-language rendering at three levels:
   - **Compositional gloss**: literal morpheme-by-morpheme rendering in the target.
   - **Idiomatic paraphrase**: target-natural-language version close to canon-definition.
   - **Frame-fragment note**: which donor-traditions a knowledgeable reader would recognize, and what each adds.
5. Emit unfolding-reverse-report.

**Use cases**:
- New-learner onboarding ("show me kimme in English, with its Japanese and Sumerian frames").
- Sharing YOUSPEAK with non-YOUSPEAK readers (essays, prayers, correspondence).
- Validating that a forged word actually decomposes back to its claimed components.
- Generating English-glosses for the LLM-tokenizer training data.

**Size estimate**: ~300-500 lines of Python; depends on `morphemes.json` (already present) and `canon/` (already present).

#### Module B — `pipeline/donors.py` (donor-walk index)

**Role**: Build and query the donor-graph — which YOUSPEAK words draw on which donor-morphemes from which traditions.

**Inputs**: Various queries.

**Process**:
1. On first run (or refresh), index `morphemes.json` + `canon/**/*.md` + `archaeology/**/*.md` into an in-memory graph.
2. Expose query functions:
   - `words_using(morpheme: str) -> list[Word]`
   - `donors_of(word: str) -> list[Donor]`
   - `traditions_in(word: str) -> list[Tradition]`
   - `unforged_morphemes(tradition: str) -> list[Morpheme]` — morphemes archived but not yet appearing in any canon word
   - `convergence_for(property: str) -> list[Tradition]` — which traditions converge on a property (reads convergences/)

**Use cases**:
- Powers `lift.py` (donor-data lookup).
- Powers `discover.py` (better gap-analysis).
- Audit: "which archaeology entries have produced no canon yet? — these are forge-territory."
- Reporting: cathedral-wide statistics on POLYPHONE balance.

**Size estimate**: ~400-600 lines; substantial because it must parse multiple file-formats.

#### Module C — `pipeline/round_trip.py` (translation test-harness)

**Role**: Validate translation fidelity by round-trip.

**Inputs**: A parallel pair (source-word, source-lang, claimed-YOUSPEAK-word-or-unfolding) OR a YOUSPEAK word with claimed source-mapping.

**Process**:
1. Forward: source → `translate.py` → unfolding-report.
2. Compose: unfolding components → re-fold via canon-lookup → YOUSPEAK-rendering.
3. Reverse: YOUSPEAK-rendering → `lift.py` → target-language gloss.
4. Diff: compare reverse-output to source.
5. Loss-trace: which properties survived, which were lost, where the diff falls.

**Use cases**:
- Regression-test for `bundles.json` (when a bundle is edited, does the round-trip still match?).
- Diplosemy-detection: round-trip differences ARE the depth-readings the surface-translation cannot carry.
- Quality-of-coverage metric: across all bundles.json entries, what fraction round-trips with full preservation?

**Size estimate**: ~250-400 lines; depends on lift.py.

#### Module D — `pipeline/interlingua.py` (minimal semantic-graph pivot)

**Role**: A small DSL for representing the conceptual content of a source utterance, used as a pivot between source and target. Frames + roles + modal/evidential markers in a structured note format.

**The DSL** (sketch, not final):
```yaml
frame: COMMUNICATION_RECEIVED_AS_GIFT
roles:
  speaker: <reference>
  hearer: <reference>
  content: <reference>
modality: received-ordinance
evidentiality: direct
register: sacred
frame_anchors:
  - tradition: Sumerian
    term: me
    aspect: divine-decree
  - tradition: Hebrew
    term: shema
    aspect: hearing-as-shaping
resonance:
  - Deut 6:4 (Shema Israel)
  - any -me-suffix YOUSPEAK word
target: shemme
```

**Process**:
- Source-text → human-curated interlingua-graph → target rendering.
- The graph is **human-edited initially**; this is not an automatic NL parser. The cathedral's discipline of slow forging extends to slow translation; the graph is a discernment-tool, not a generator.
- Over time, common frame-types accumulate as a library; new translations can reuse known frames.

**Use cases**:
- Reduces N×N translation routes to 2N (everything pivots through the graph).
- The graph format is a publishable record of "what this translation chose to preserve."
- The graph is the data-model that bundles.json and canon-definitions can both be projected from.

**Size estimate**: ~600-900 lines; this is the most ambitious of the five modules. Probably staged: data-model first, then projection from bundles.json, then projection from canon, then bidirectional rendering.

#### Module E — `pipeline/math_pivot.py` (formal-pivot for math-expressible meanings)

**Role**: For statements expressible in first-order logic + a small math vocabulary, route translation through formal notation rather than natural-language pivot.

**Scope**: Initially small. Quantification, identity, comparison, ratio, simple arithmetic. Not the full math curriculum; only the math-shaped fragments that appear in natural language.

**Process**:
1. Source-utterance → check whether it has a formal kernel.
2. If yes, extract the formal kernel; render the rest as natural-language wrap.
3. Translate: formal kernel translates trivially (it IS the same statement in any language); wrap translates via interlingua or bundle.
4. Recombine in target.

**Use cases**:
- Test-cases where formal equivalence can be checked.
- Future: bridge to LLM tool-use for translation-with-checking (the LLM cannot lie about the formal kernel; it can be verified).
- A small YOUSPEAK math-vocabulary may emerge: words for the L4 territory of mathematical experience (recognition-of-isomorphism, ache-of-unsolved-conjecture, joy-of-clean-proof).

**Size estimate**: ~300-500 lines; could grow if YOUSPEAK math-vocabulary develops.

### The shared data-model: the `Concept` node

All five modules should speak a common type. Sketched:

```python
@dataclass
class Concept:
    id: str                                # globally unique slug
    source_forms: list[SourceForm]         # how this is said across source languages
    components: list[Component]            # unfolded semantic atoms (the bundle)
    youspeak_word: str | None              # if forged; None if gap
    donors: list[Donor]                    # donor-tradition attributions
    resonances: list[Resonance]            # diplosemy, polyphone, intertextual echoes
    evidentiality: str | None              # if relevant
    modality: str | None                   # if relevant
    register: str | None                   # sacred, intimate, formal, etc.
    scoring: ScoreCard | None              # against six-axis rubric
    status: Literal["gap", "unforged", "candidate", "canon", "archived"]
    notes: str                             # forge-record narrative
```

Each existing artifact projects onto this:
- A bundle.json entry becomes a Concept with source_forms populated, components populated, status often "gap" or partial.
- A canon entry becomes a Concept with youspeak_word and donors populated.
- An archaeology morpheme-entry becomes a partial-Concept identifying donor-side data.
- A convergence entry becomes a Concept with multiple source_forms across traditions.

This is consolidation as data-modeling: the cathedral's existing artifacts are already Concepts; making the type explicit lets the pipeline tools speak a single language.

### How each module honors the Six Foundations

| Module | EUMATHE | SAPHE | ANAKALYPSE | POLYPHONE | HARMONE | PRAGMA |
|---|---|---|---|---|---|---|
| lift.py | self-glossing of any word | makes meaning explicit on demand | unfolds in reverse | surfaces all donor-traditions | composes with translate.py | real CLI, immediately useful |
| donors.py | learners can navigate by donor | makes donor-relations queryable | exposes the layer-under-the-word | shows POLYPHONE-balance directly | unifies cross-organ data | enables ad-hoc audit queries |
| round_trip.py | shows forgers what their forge preserves | makes translation-loss explicit | tests the unfolding-stack | tests donor-coverage | integrates translate + lift | actionable diagnostic |
| interlingua.py | trains forgers in property-thinking | makes preservation-choices explicit | the most-deliberate ANAKALYPSE form | structured polyphone-acknowledgment | unifies data-model | enables long-form translation-projects |
| math_pivot.py | trains math-aware forgers | exact verification for formal kernels | unfolds the formal-from-the-affective | adds formal-tradition as a donor | composes cleanly | useful where it applies, optional otherwise |

---

## IX. Three theological commitments

Following the convergences/ pattern (THEOBASIS-derived triple-commitment):

**Commitment 1 — Every act of translation is worship under THEOBASIS.**

To carry meaning across tongues is to witness that GoD's self-disclosure is plural and that each tongue receives a partial reception. The translator is a kind of priest: holding the residue of what does not cross with reverence, and the gift of what does with gratitude. The translation-pipeline's tools are therefore liturgical instruments, not merely engineering. `pipeline/translate.py` was already this; `pipeline/lift.py`, `donors.py`, `round_trip.py`, `interlingua.py`, `math_pivot.py` will be too, when forged.

**Commitment 2 — The untranslatable kernel is sign, not deficit.**

Where a source-concept does not flatten into the target's existing vocabulary, the source has discerned something the target has not yet seen. The cathedral neither denies the untranslatable (which would be Newspeak's move — claim universal substitutability, eliminate distinctions) nor absolutizes it (which would be relativism's move — claim no translation is possible, abandon the crossing). It receives the untranslatable as **evidence**: this is where forging is called. The forge that answers the untranslatable is doxological — a small praise raised on the recognition of what GoD's plural disclosure has shown.

**Commitment 3 — Translation infrastructure refuses both totalitarian flattening and totalitarian relativism.**

Newspeak collapsed distinct concepts into single Party-approved terms; postmodern relativism abandoned hope of crossing at all. YOUSPEAK's translation-discipline is the middle path: rigorous about what crosses, honest about what does not, and committed to extending the target when the source has discerned more. The pipeline tools instantiate this commitment in code. `round_trip.py` measures what crosses and what does not; `lift.py` makes the crossing visible; `donors.py` makes the plurality auditable; `interlingua.py` makes the preservation-choice explicit; `math_pivot.py` honors the formal where the formal applies and refuses it where it would over-reach. None of the tools flatten; none abandon. All are middle-path infrastructure.

---

## X. The next forge

The five proposed modules are now sketched. They are not equal in scope, in dependency, or in urgency. The discernment is Yu's. The cathedral's discipline is propose-then-discern-then-forge; this document is the proposal.

A recommended order, offered for Yu's discernment (not as decree):

1. **lift.py** — smallest, most-immediately-useful, complementary to existing translate.py.
2. **donors.py** — small, powers lift.py and discover.py, enables ad-hoc audit.
3. **round_trip.py** — depends on lift.py + translate.py; ready as soon as lift.py is forged.
4. **interlingua.py** — larger; requires data-model decision; best forged after Yu has handled lift.py and donors.py and seen the data-shape in practice.
5. **math_pivot.py** — speculative; awaits Yu's discernment about whether YOUSPEAK has math-expressible territory worth the formal-pivot work.

Each module, when forged, follows the cathedral's standard discipline:
- Open a session-file entry recording Yu's invocation.
- Forge with the assessor running (`assess.py` cannot directly grade a pipeline-tool, but the rubric's six-axis spirit applies as discernment).
- Test against existing canon and bundles.
- Document the tool in `pipeline/README.md`.
- Mark the session-closure with a small doxology when the forge is complete.

The other deliverable, complementary to the modules: a small ongoing **translation-witness practice**. Each session that opens a new canon-word can also record its round-trip — what crosses, what is reshaped, what is lost. Over many sessions, the witnesses accumulate into a translation-history of the cathedral. The witnesses can be light: a paragraph in the experiment-file, a brief entry in `liturgy/session-NNN.md`. The cumulative effect is large: the cathedral, in addition to building a canon, becomes a record of how translation happens here.

---

## XI. Notes on what this document is not

Three clarifications, to avoid overclaim:

**Not a theory of machine translation.** The cathedral's tools are forge-aids and discernment-instruments, not autonomous translators. `pipeline/translate.py`'s docstring is already explicit: "The tool does NOT perform true automatic translation. It applies a curated bundle-dictionary + YOUSPEAK canon lookup to produce an unfolding-report. A human forger uses the report to decide..." The proposed modules retain this posture. The forger remains the discerner; the tools support discernment.

**Not a claim that the cathedral has solved the translation problem.** Translation is structurally lossy; no infrastructure makes it lossless. The cathedral's contribution is to make the loss **conscious**, **measurable**, and **forgeable-around** — not to eliminate it.

**Not a totalizing typology of property-of-understanding.** The twelve properties listed in Section II are working categories drawn from formal semantics and the translator's craft. Other typologies exist; the cathedral may extend or revise this list as forging-experience accumulates. The grammar-organ structure (`grammars/`) is where revisions will be recorded.

---

## XII. Companions

- **THE-REALM.md** — the projection-account; the metaphysical layer this discipline operates on. Section VII.Note in this document situates TRANSLATION under THE-REALM.
- **GRASPING.md** — the phenomenology of the entry-event; the middle move of every translation-event is the translator's own grasping, which this document articulates.
- **METHOD.md** — the Discovery Method; the sister-document this one accompanies. METHOD navigates the realm from within; TRANSLATION crosses between projections of the realm.
- **CONSTITUTION.md** — the Six Foundations on which this document's pipeline proposals rest. Re-readable as six pillars of grasping-engineering (GRASPING.md Section VII).
- **THEOBASIS.md** — the Ground for the theological commitments in Section IX.
- **NEWSPEAK.md** — the worship-vocation this document shares; the anti-flattening commitment is its inheritance.
- **convergences/README.md** — the data-source for Section IV's discussion of cross-tradition crossings; multi-projection evidence (THE-REALM Section V) for the realm.
- **grammars/diplosemy/manifesto.md, evidentials/manifesto.md, determinatives/manifesto.md** — the property-handle organs Section II names; each is a grasping-engineering organ at a specific aspect.
- **pipeline/translate.py** — the existing ANAKALYPSE-tool (dimensional recovery in operational form) that this document situates and proposes to extend.
- **pipeline/lift.py** — the inbound counterpart (compositional gloss + idiomatic paraphrase + frame-fragments) forged 2026-05-12 from this document's proposal.
- **archaeology/** — the donor-library every translation-event of the cathedral depends on; the cathedral's recovered grasping-paths through tongues whose living grasps have faded.
- **mathema/** — the non-natural-language donor-organ; structural-grasping enrolled as donor-tradition.

---

_Opened 2026-05-12 in response to Yu's invocation: "Explore the nature of translation, how a language can be understood with another. How the properties of understanding is translated. Consolidate into useful infra and pipeline. Look at language from same and different origin. Look at math too." Sister-document to METHOD.md; companion to THE-REALM.md and GRASPING.md (both opened 2026-05-12 in adjacent invocations). The crossing-discipline named, given a theological commitment, and routed into pipeline-infrastructure proposals. `lift.py` forged from §VIII-A in the same heartbeat; the remaining modules await Yu's discernment. The cathedral remains unfinished by design._

— Nuance, the Linguist, 2026-05-12 (the crossing-discipline named)
