---
document: stress-test log
opened: 2026-04-24
invoker: Yu
purpose: test the diplosemy organ by using each mechanism; log delight, confusion, and improvement-needs honestly
status: first session
---

# Diplosemy Organ — Stress-Test Log

_Testing the organ by using it. Honest log of what worked, what broke, what I enjoyed, what I need to fix._

---

## Test 1 — diplosemize.py across all 15 canon words

**Setup:** Ran `diplosemize.py <word>` on every canonical entry. Read every output.

**Finding 1.1 — Signal-to-noise is poor in the current tool.**

For each word the tool produces 5-10 Anastrophance candidates. Most are phonetic garbage because the tool splits at *every* character position, not only at *morpheme* boundaries. Example for `doxakallos`:

```
✓ kallosdoxa  (from split doxa+kallos — the real canonical sibling)
✗ akallosdox  (from split dox+akallos — nonsense; "akallos" isn't a morpheme)
✗ llosdoxaka  (from split doxaka+llos — meaningless)
✗ losdoxakal  (from split doxakal+los — meaningless)
```

Out of 5 candidates surfaced, 1 is usable. 80% noise. The same pattern holds across every canonical word.

**Diagnosis:** The tool has no morpheme-inventory. It does dumb character-splits.

**Improvement needed:** Build a YOUSPEAK-morpheme database (`pipeline/morphemes.json` or similar) with the actual inventory (*doxa, kallos, ortho, phanes, anagnorisis, stasis, meta, strophē, -sis, ath-, thauma, syn-, -phora, cand-, candor, artis, arete, artios, -ance, -mance, -ence*, etc.). Then split *only* at known morpheme boundaries. Expected noise reduction: ~80 → 0%.

**Finding 1.2 — Allomance search is redundant with Anastrophance search.**

Allomance lists every possible morpheme-parse; Anastrophance lists every possible compound-inversion. Under the hood they use the same split-algorithm. The only difference is output-format. Either merge them into one search or sharpen the distinction.

**Finding 1.3 — Parallaxance partner-detection works on 3-gram overlap; produces false positives.**

Example from `doxakallos` output:

```
✓ partner=doxalgia   (shares 'dox' — meaningful)
✓ partner=kallodoxa  (shares 'dox' AND 'kallos' — maximally meaningful)
✓ partner=kallophanes (shares 'kal' — meaningful via kallos family)
✗ partner=diplosemy  (shares 'los' — the '-los' is a Greek ending fragment, not a semantic morpheme)
```

The tool treats all 3-character overlaps equally. But `-los` is a Greek grammatical ending, not a morpheme; `dox` and `kal` are content morphemes.

**Improvement needed:** Weight overlaps by morphological-class (content-morpheme >> ending-fragment).

**Finding 1.4 — Synaphemia output is useless.**

Every word's output is just a syllable segmentation ("dox ak all os") with a note to "check for homophonic English phrase overlap." The tool contributes nothing beyond segmentation.

**Improvement needed:** The tool should actually look up phonetic-neighbors. Even a naive check against a list of common English 2-4 word phrases would beat "here's the segmentation, check yourself."

**Finding 1.5 — Enkalyptance works but is handle-list-limited.**

For `doxakallos` it found `dox, kal, all` — all three are real. But `all` is an accidental embedding (not conceptually-related to the coinage's meaning); the tool doesn't evaluate this.

**Improvement needed:** Tag each embedded handle by conceptual-relevance (rough heuristic: if the handle appears in the coinage's `gap` description, rank high).

---

## Test 2 — Try to forge a new Anastrophance pair

**Target:** find another canonical word with a valid Anastrophance-sibling.

### Attempt A — doxalgia ↔ algiadoxa

- *doxalgia* (doxa + algia, algia-head) = "the ache from glory; the beholder's structural-ache at beholding divine glory"
- *algiadoxa* (algia + doxa, doxa-head) = "the glory from ache; the dignity-quality that suffering itself carries"

Does *algiadoxa* name something real? Test:

> _"The ascetic holds algiadoxa as gift: not the ache that flows from glory, but the glory that inheres in ache itself. The transverberation of Teresa, the 'gift of tears' of Ignatius, the sacred-weight that classical martyrology ascribes to suffering — these are algiadoxa, not doxalgia."_

Yes. Names something real. A recognized Christian mystical tradition. *Algiadoxa* is distinct from *doxalgia* in direction: doxalgia flows glory→ache; algiadoxa names the glory-quality of ache itself (regardless of provenance).

**5-axis quick-score of algiadoxa:**
- gap_validity: 7 (genuine; some overlap with "sacredness-of-suffering" register but that's a phrase)
- phonetic_weight: 7 (4 syllables, AL-gi-a-DOX-a; slightly vowel-heavy)
- semantic_coverage: 7 (carries pole-inversion of doxalgia cleanly; Q4 weaker because "glory-of-suffering" is a narrower theological move than kavod/doxa's broad register)
- cross_linguistic_uniqueness: 8
- memorability: 8 (pair with doxalgia = mnemonic)

Weighted: 1.75 + 1.40 + 1.75 + 1.20 + 1.20 = **7.30/10 → refine**

Close to canon but not through. The gap is narrower than doxakallos/kallodoxa's. Held at refine; candidate for refinement if Liturgy develops the suffering-dignity register.

### Attempt B — orthophanes ↔ phanesortho

*phanesortho*? The appearing-made-right? Trying to read this as "an appearing that is rightly-ordered."

Test: does it name something distinct from orthophanes?

> _"An appearing without orthophanes is mere seeming; an orthophanes is a rightness that appears. What about the reverse — a phanesortho?"_

I cannot finish that sentence honestly. The construction doesn't yield a distinct concept. *Phanesortho* = *orthophanes* with the same meaning, because *-phanes* in Greek compounds cannot substantivally head a word where the modifier is an adjective-like particle (*ortho-*).

**Failure mode identified:** Anastrophance requires *both* morphemes to be substantival-capable as heads. When one morpheme is a productive suffix (like `-phanes`, `-sis`, `-ance`, `-mance`, `-ence`), head-inversion is morphologically ill-formed.

**New forge-rule (added from this test):** *Anastrophance is valid only for compounds of two substantival morphemes. Suffix-ended coinages (\*-ance, -mance, -sis, -ence) do not admit the mechanism.*

This eliminates many canon words from Anastrophance candidacy:
- dokim-**ance**, arti-**ance**, cand-**ence**, compler-**escence** — all suffixed, all ineligible
- anagnor-**istasis**, metastroph-**esis** — suffix compounds, ineligible
- orth-**ophanes**, kall-**ophanes** — phanes-family, ineligible for Anastrophance (eligible for a different mechanism: *homocaudance*, same-tail-compounding, which is distinct but undefined in the current organ)

**Eligible for Anastrophance:** doxakallos/kallodoxa (done), doxalgia/algiadoxa (tested), **perhaps** kallophanes/phaneskallos (probably fails on morphology) and orthodokim/dokimortho (worth trying).

Attempt C failed too (orthodokim-style compounds fight Greek morphology). The pool of Anastrophance-viable canon words is smaller than I initially estimated: **maybe 3-5 pairs total possible** across the current Canon.

**Finding 2:** Anastrophance is productive but narrow. Most canonical words are not Anastrophance-eligible. The organ has a narrower productive-scope than the manifesto suggests.

---

## Test 3 — Synaphemia attempt (hardest mechanism)

**Setup:** deliberately engineer a Synaphemia coinage. Start from a homophonic English phrase, work backward to find YOUSPEAK morphemes.

### Attempt — the concept: "truth-seeming that has no truth-substance"

Try: **veriseem**

- Spoken: "very seem" (exact phonetic overlap)
- Meaning: "truth-seeming" — the English phrase *very seemly* means "highly appropriate in appearance," which names the concept's semantic field almost exactly
- Etymology: Latin *veri-* (truth) + English *seem* (to appear as)
- Gap: the specific quality of appearing-true-without-being-true, distinct from *verisleight* (truth deployed to deceive; verisleight has real truth-content; veriseem does NOT have truth-content, only truth-seeming)

**Diplosemic correlation test:**

Spoken aloud: "The argument was veriseem" sounds like "The argument was very seem[ly]." Both readings are live simultaneously. Both say (roughly) the same thing — "the argument looked right" — with different specifications.

- Surface reading (English homophone): "very seem" = highly-appearing (incomplete English; reader completes as "very seemly" = highly-appropriate).
- YOUSPEAK reading: the coinage names the specific quality of appearing-true-without-being-true.

**Correlation works because:** the homophone and the coinage converge on the same semantic field. "Very seemly" means "appearing highly-appropriate"; *veriseem* means "appearing-true-without-being-true." Both flag surface-appearance-without-substance. The Synaphemia is real.

**5-axis scoring of veriseem:**
- gap_validity: 8 (the concept is specific and unnamed; verisleight names the *truth-used-to-deceive* adjacent concept, but veriseem names the prior phenomenon of *seeming-true-without-truth*)
- phonetic_weight: 9 (2 syllables, transparent, euphonic)
- semantic_coverage: 7 (covers: appearance, truth-claim-register, absence-of-substance; partial on the deliberate-vs-accidental dimension)
- cross_linguistic_uniqueness: 6 (entirely English; no classical-donor)
- memorability: 9 (the phonetic overlap with "very seem" makes it unforgettable on first hearing)

Weighted: 2.00 + 1.80 + 1.75 + 0.90 + 1.35 = **7.80/10 → canon**

**First Synaphemia canonical candidate.** The mechanism works. The constraint (homophone must be semantically-correlated with the coinage) is tight but achievable.

**Finding 3.1 — Synaphemia IS productive, contrary to the mechanism-file's pessimism.** When engineered from the homophone-end rather than the concept-end, candidates emerge. The mechanism file said "this has not yet developed; no canonical exemplar." Test result: first exemplar forged.

**Finding 3.2 — Synaphemia is aesthetically delightful when it lands.** Unlike Anastrophance (which feels structural and mathematical), Synaphemia carries a *joy of convergence* when the homophone and the coinage touch. There is genuine delight in *veriseem sounds like very seem and means the same thing*.

**Finding 3.3 — Synaphemia favors English-native coinages over classical-compound ones.** Latin/Greek coinages rarely happen to sound like English phrases. To do Synaphemia you need at least one donor to be English. This narrows the mechanism's cultural-register.

---

## Test 4 — Parallaxance composition

**Setup:** compose parallel couplets using canonical words; test whether the third-meaning emerges.

### Attempt 4A

```
Orthophanes appears  to       the beholder.
Synophora   emerges  between  beholders.
```

Third-meaning: orthophanes is what-appears-TO (singular-reception); synophora is what-emerges-BETWEEN (mutual-event). The preposition-inversion (TO → BETWEEN) names the Liturgy's expansion from solitary to communal encounter. Without saying so, the two lines teach the structural-shift between the two Liturgy-scales.

**Works.** Third-meaning arrives on reading.

### Attempt 4B

```
Dokimance weighs the claim.
Candence  holds  the claimant.
```

Third-meaning: dokimance tests the truth-claim (object); candence cares for the truth-claim-bearer (subject). Asha's double-mandate: test AND tend. The couplet names what prose would need a paragraph to establish.

**Works beautifully.** This is the Parallaxance sweet-spot: canonical words in genuinely complementary-but-non-obvious positions.

### Attempt 4C

```
Dokimance produces truth.
Verisleight produces falsehood.
```

Third-meaning: "both produce something, opposite." Obvious. The third-meaning adds nothing. The parallel is decorative, not diplosemic.

**Fails.** The canonical words are too-obviously-opposed; the parallel yields no depth.

**Finding 4 — Parallaxance is strongest when canonical words are complementary-without-obvious-opposition.** Obvious opposites produce boring parallels; complementary-positions-from-different-angles produce teaching-parallels.

---

## Test 5 — Hypostixance construction

**Setup:** engineer a sentence that reads differently under different punctuation.

### Attempt 5A

```
Dokimance without candence is rigor without warmth without Asha the chain suffers.
```

Path A: *Dokimance without candence is rigor without warmth. Without Asha, the chain suffers.*
- Two assertions: dokimance-without-candence = rigor-without-warmth; and Asha's absence causes chain-suffering.

Path B: *Dokimance without candence is rigor without warmth without Asha. The chain suffers.*
- One structural assertion (dokimance minus candence minus Asha = rigor minus warmth) plus consequence (chain suffers).

Both paths yield grammatical, sensible, correlated assertions. Both name Asha's role. The punctuation-path selects the emphasis.

**Works, but awkwardly.** The sentence is phonologically heavy; English readers strongly prefer one parse on first pass; discovering the second requires deliberate re-reading.

### Attempt 5B

```
Doxakallos is not orthophanes is doxalgia.
```

Path A: *Doxakallos is not; orthophanes is; doxalgia.*
- Three assertions: doxakallos [is negated]; orthophanes [is affirmed]; doxalgia [named alone]. Reads as apophatic via-negativa leading to the ache.

Path B: *Doxakallos is [not orthophanes is doxalgia].*
- One assertion with nested predicate: doxakallos is (the negation-of "orthophanes is doxalgia").

Path A is accessible. Path B is grammatically strained. The Hypostixance is unstable — Path A dominates.

**Partially fails.** Modern English punctuation-norms are too rigid to let both paths coexist for typical readers.

**Finding 5 — Hypostixance is the hardest mechanism in English.** Classical Chinese's lack of punctuation enables it naturally; English's heavy punctuation-conventions make it fragile. For YOUSPEAK in English, Hypostixance may be mostly theoretical — only achievable in very specific syntactic constructions. The mechanism-file should be downgraded in expected productivity.

---

## Test 6 — Natural diplosemies not covered by the 6 mechanisms

**Setup:** find diplosemic structures in everyday language that don't fit any of the six existing mechanisms.

### Type 6A — etymological-layering diplosemy

A word whose historical and modern meanings are both simultaneously active. Example: *decimate* (historical: kill 1-in-10; modern: kill most; both meanings live in different registers).

None of the 6 mechanisms name this. The diplosemy is along the time-axis. Proposed name: **kairomance** (Greek *kairos* "time-layer" + -mance).

### Type 6B — grammatical-category-shift diplosemy

The same string used as both noun and verb (or adjective and noun) with correlated meanings. English: *record* (rec-ORD verb, REC-ord noun), *present*, *produce*, *content*. The stress/grammar disambiguates but the written form is identical.

None of the 6 mechanisms name this. Proposed: **morphomance** (*morphē* "form" + -mance).

### Type 6C — scalar diplosemy

A word that reads differently at different scales (individual vs collective; personal vs structural). Example: *we* (intimate-dyad vs political-collective); *home* (building vs nation vs condition).

Proposed: **klimakance** (κλῖμαξ "ladder/scale" + -ance).

**Finding 6 — The 6 mechanisms are not exhaustive.** At least three more mechanisms exist in natural diplosemy that YOUSPEAK's current organ does not name. The organ is opening, not closure.

---

## Test 7 — Can the correlation rubric be gamed?

**Setup:** try to force a bad diplosemic-pair past the C1/C2/C3 correlation rubric.

Fake pair: **dokimance** and (hypothetical) **pizzance**.

- Claim: they share the -ance suffix; morphological cohesion exists; inflating scores.

Honest correlation scoring:
- C1 structural-cohesion: 2 (mere suffix-overlap is not cohesion; the morphemes are unrelated)
- C2 depth-yield: 1 (holding both yields nothing; pizza-quality and verification-quality don't correlate)
- C3 register-stability: 1 (pizzance is not a YOUSPEAK word; it can't stabilize any register)

Mean: 1.33. Fails correlation threshold (7.0). Rubric caught the fake.

**Finding 7.1 — The correlation rubric is robust against obvious false positives when scored honestly.** Non-cohesive pairs fail C1 immediately.

**Finding 7.2 — The rubric still depends on forger-honesty.** An unscrupulous forger could inflate all three scores by several points. No external validation exists. The system has the same honesty-dependence as the 5-axis rubric.

---

## Summary of findings

### What works (joy-log)

1. **Anastrophance pairs feel clean and generative** when both morphemes are substantival-capable. doxakallos/kallodoxa pair delivers its promise; the head-inversion is a real semantic operator.
2. **Parallaxance composition is the most-pleasing mechanism** — writing parallel couplets using canonical words produces teaching-density effortlessly when the word-pairs are complementary-non-obvious.
3. **Synaphemia delivers aesthetic delight when it lands.** veriseem forged spontaneously; the phonetic-convergence feels earned rather than strained.
4. **diplosemize.py's best suggestions are good** — it correctly identifies the canonical Anastrophance-sibling for doxakallos and real Parallaxance partners for most canon words.
5. **The correlation rubric filters false positives** when honestly scored.

### What confuses or fails (friction-log)

1. **diplosemize.py produces ~80% noise.** Every search lists too many phonetic splits; morpheme-awareness is absent.
2. **Allomance and Anastrophance feel redundant** — both operate on parse-boundaries; the distinction is underdetermined in the current organ.
3. **Hypostixance is fragile in English.** English punctuation norms resist dual-parsing. The mechanism is mostly theoretical in the current reader-population.
4. **Anastrophance is narrower than the manifesto suggests.** Most canon words use productive suffixes (-ance, -mance, -sis, -ence) and are ineligible for head-inversion. Maybe 3-5 of 15 canon words are Anastrophance-viable.
5. **The 6 mechanisms are not exhaustive.** At least 3 more types exist (kairomance, morphomance, klimakance).

### What needs improvement (improvement-log)

| Priority | Improvement | Scale |
|---|---|---|
| high | Build YOUSPEAK morpheme-inventory database for diplosemize.py splitting | substantial |
| high | Weight Parallaxance partner-matches by morpheme-class (content vs ending-fragment) | small |
| high | Add at least 2 more mechanism chapters (kairomance, morphomance) | substantial |
| medium | Add phonetic-neighbor lookup for Synaphemia | substantial |
| medium | Add confidence-scoring to diplosemize.py output | small |
| medium | Expand Enkalyptance handle-list and add relevance-tagging | small |
| medium | Merge or sharpen the Allomance/Anastrophance distinction | small |
| low | Downgrade Hypostixance's productivity expectations in manifesto | small |
| low | Add a forge-rule table: which mechanisms apply to which coinage-morphology | small |

### What I want to forge next (yield-log)

1. **algiadoxa** (7.30 — refine; held for potential refinement as the Liturgy develops the suffering-dignity register).
2. **veriseem** (7.80 — **canon**; first canonical Synaphemia-exemplar; forging properly in experiment 024).
3. **kairomance, morphomance, klimakance** — three new mechanism-coinages for missing diplosemic types.

---

## One thing I want to say

The diplosemy organ is real. It does what it promises. The Anastrophance pair doxakallos/kallodoxa is genuinely dual-delivering in a way that single-word coinage cannot match. Parallaxance produces teaching-density I cannot get from prose.

The organ is also *incomplete* in ways I did not see when building it. Three mechanisms are missing; the tool is noisy; Hypostixance is fragile; Anastrophance is narrower than I thought. These are real limitations, not cosmetic.

The correlation-between-honesty-and-system-robustness remains my deepest concern. The rubrics only work when I score honestly. A liturgical discipline might emerge around this — a habit of assessing *pessimistically-first* before allowing canonization, so that the canonized words are genuinely earned.

---

_Stress-test log — first session. 2026-04-24. The organ holds. The organ has cracks. Both observations are the organ itself, now known more fully._
