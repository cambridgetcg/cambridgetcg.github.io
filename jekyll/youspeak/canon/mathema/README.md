# canon · mathema · the worship-vocabulary forged from mathematical donors

_The cathedral's fifth canon-domain. Opened 2026-05-12, Session 078, under the POLYPHONE Generalization (METHOD.md §S078)._

---

## What this domain is for

`canon/mathema/` houses worship-vocabulary forged from mathematical donor-traditions. Sister-domain to `canon/core/` (universal everyday-worship vocabulary), `canon/worship-action/` (verbs of worship-act), and the Liturgy/Zerone/Grammar specialized domains.

The domain's scope is **worship-vocabulary specific to the mathematical-experience-as-worship-form** — words that name the inner liturgy of mathematics, the felt-quality of mathematical work, and the worship-grade experiences mathematicians live but English does not name.

The Greek *mathēma* (μάθημα), before it narrowed to mean "mathematics," meant simply *"that which is learned"* — any received instruction. The domain's name preserves the wider sense: this is the cathedral's vocabulary for received-truth-by-discipline, of which mathematics is the paradigm but not the limit.

---

## What lives here vs. what lives in core

Some words forged from mathematical donors have **universal scope** (the experience they name is not restricted to mathematicians). Those live in `canon/core/`. The first such forge:

- `canon/core/yonedame.md` — being-fully-known-through-relation, received as cosmic-gift (Yoneda lemma + Sumerian me). Universal worship-experience; happens to be donated by mathematics. Lives in core.

Other words forged from mathematical donors have **mathematics-specific scope** (the experience is paradigmatic in mathematical work and rare or absent elsewhere). Those live in `canon/mathema/`. Proposed first inhabitants:

- `mathemame` (proposed; the strategic keystone) — *that-which-is-learned, received-as-cosmic-gift*; the theorem received as gift rather than achievement; from Greek *mathēma* + Sumerian *me*. Names every theorem, every proof-result, every insight that lands with the structure-of-receiving-rather-than-inventing.

- `gödelance` (proposed) — *the discipline of remaining within a system while honoring its horizon*; from Gödel's incompleteness theorems + Latin *-ance*. Names the worship-stance of working faithfully inside a discourse while knowing the discourse cannot speak about everything it must serve.

- `isomorqing` (proposed) — *the felt-bond of recognizing same-structure-different-substance*; from Greek *isomorph-* (same form) + Mandarin *qing*. Names the "ah, this is THAT again" recognition that is a core mathematical experience and that English flattens to "analogy."

- `synkresome` (proposed) — *the gift of compression: when many become one without loss*; from Greek *synkresis* (compression) + Sumerian *me*. Names the Euler-identity-class experience: nine glyphs holding the bond between geometry, algebra, analysis, negation, and the foundation of arithmetic.

- (future) Curry-Howard-donor words for the doing-and-knowing-as-one-act experience.

The boundary between core and mathema is **scope of the experience named**, not the source of the donor. A math-donor word whose scope is universal goes to core; a math-donor word whose scope is the mathematician's working life goes to mathema.

---

## Doctrinal grounding

This domain rests on:

- **METHOD.md §POLYPHONE Generalization (S078)** — the principle that licenses mathematics as donor tradition
- **`archaeology/mathematics/README.md`** — the donor-tradition declaration
- **`convergences/faithful-sign-craft-as-witness.md`** — the structural argument for why mathematics qualifies
- **THEOBASIS** — the metaphysical ground that makes the qualification structurally necessary, not discretionary

The domain is **doctrinally subordinate** to all four. Forges in `canon/mathema/` must meet the standard 6-axis rubric and must include religious-tradition convergence alongside the mathematical donor — POLYPHONE-balance is preserved, not relaxed.

---

## What is NOT in this domain

The discipline is exact about its reach.

- **Mathematical concepts as such** — this domain does not contain mathematical theorems, definitions, or proofs. Those live in mathematical literature, where they belong. The cathedral receives mathematical concepts as donors; it does not republish them.

- **Theology of mathematics** — this domain does not advance metaphysical claims about mathematics. THEOBASIS does the metaphysics; the mathema domain does the vocabulary.

- **Specialized worship-words for mathematicians-only** — this domain serves any worshipper who wants to name experiences mathematicians have named. Many of the words here will be useful to non-mathematicians who do similarly-disciplined work (composers, programmers, theologians-as-formal-thinkers, philosophers, certain craftspeople). The mathematical specificity is in the donor, not in the audience.

- **Hagiography of mathematicians** — Yoneda, Gödel, Euler, and the rest are donors of structural concepts. The cathedral does not canonize them as theological figures.

---

## How forges enter this domain

Same pipeline as all other domains:

```
archaeology/mathematics/<concept>.md   →  labs/logos/experiments/<NNN>-<word>.md
                                                        ↓
                                            pipeline/assess.py (6-axis rubric)
                                                        ↓
                                            weighted_total ≥ 7.5
                                                        ↓
                              canon/{core,mathema,worship-action}/<word>.md
                              (scope-determined: core for universal,
                              mathema for math-specific)
```

Each entry includes the standard frontmatter plus:

- `donor_discipline:` field naming the mathematical source
- `principle:` field referencing METHOD.md §S078
- `religious_convergence:` field documenting the cross-tradition witnesses (still required for POLYPHONE-balance)

---

## See also

- METHOD.md §POLYPHONE Generalization (S078)
- `archaeology/mathematics/README.md`
- `convergences/faithful-sign-craft-as-witness.md`
- `canon/core/yonedame.md` — the first forge under the generalization (lives in core, not mathema, due to universal scope)
- `grammars/mathema/` — future grammar-domain for proof-as-liturgy register

---

_Domain opened 2026-05-12. The first entry awaits the next heartbeat._
