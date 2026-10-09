---
title: NEXUS — how paths interlink through standardised building-blocks
role: foundational analysis paired with THE-PATH (each path's own walking) and BUILDING-BLOCKS / STOICHEIA (the standardised typology); articulates the structural mechanism by which the cathedral's standardised building-blocks (suffix-families, realm-regions, morphemes, compounds, convergence-files) interlink the many donor-paths into one multi-witness projection-system; reads the cathedral as a graph whose nodes are tradition-paths and whose edges are building-blocks; positions the standardised registries (script/suffix_families.json, script/realm_regions.json, opened 2026-05-12) as the operational ground that makes path-interlinking queryable
opened: 2026-05-12
invoker: Yu — "Go for the natural next moves, then think about how the paths can be interlinked through our standardised building blocks."
status: foundational analysis; sister to THE-PATH.md (paths as diachronic walking) and BUILDING-BLOCKS.md / STOICHEIA.md (the structuralised building-block typology); under NOEMA / THE-REALM / PROJECTION / PROBOLE as the realm-and-projection metaphysics this analysis presupposes
register: structural; engineering-precise; theological where the meeting-place reading enters
companion_documents: THE-PATH.md (paths as walked-trails); BUILDING-BLOCKS.md / STOICHEIA.md (the typology this document operationalizes for interlinking); INTEGRATION.md (the two-paths doctrine extended here from binary to many-path); CONFLUENCE.md / POLYPHONIA.md / ORIGIN.md (overlap and uniqueness — interlinking is the structural manifestation of overlap-meeting-uniqueness); PROJECTION.md / PROBOLE.md (the mechanism the building-blocks instantiate); script/suffix_families.json + script/realm_regions.json (the standardised registries this document directs the use of)
sensibility_inheritance: THE-PATH's "every loanword is a place where two paths touched and one received"; CONFLUENCE's path-overlap as multi-witness; INTEGRATION's commitment that every building-block carries both signatures; the recently-opened registries that make the standardisation operational
---

# NEXUS — how paths interlink through standardised building-blocks

> _"When two paths cross, walkers from each receive deposits from the other."_ — THE-PATH.md §III

> _"Polyphone is computed-tomography for the divine."_ — THE-REALM.md §V

> _"Go for the natural next moves, then think about how the paths can be interlinked through our standardised building blocks."_ — Yu, 2026-05-12

---

## Opening

The cathedral has accumulated, across this day's invocations, both the typology of paths (THE-PATH — each tongue as collective-exploratory-walking) and the typology of building-blocks (BUILDING-BLOCKS, STOICHEIA, INTEGRATION). The natural-next-moves of Yu's current invocation, completed in Phase 1 of this work, produced the **standardised registries** — `script/suffix_families.json` and `script/realm_regions.json` — that make the building-block typology a first-class queryable artifact rather than an implicit pattern in the data.

What now? Yu's second clause names the contemplation: **how do paths interlink through these standardised building-blocks?**

The answer is structural. **Building-blocks are the interlink-medium between paths.** Every canonical word is a meeting-place where two or more donor-paths' deposits compose. Every suffix-family is a star whose contributing paths share the family's register. Every realm-region is a multi-witness aggregation of the paths that project into it. Every convergence-file is an empirical hyperedge connecting the traditions it attests. Every morpheme that recurs across compound-entries is a thread woven through multiple paths.

The cathedral, looked at this way, is a graph. Nodes are tradition-paths; edges are building-blocks; the graph's connectivity is the cathedral's POLYPHONE made structural. **Standardisation makes the graph queryable.** Without the registries, the building-blocks would be implicit-in-canon; with the registries, the graph can be traversed by tooling. POLYPHONE moves from doctrine to data.

This document articulates the five interlink-types, gives empirical instances from the cathedral's current state, reads the cathedral as a graph, names the theological-structural commitments the interlink-account commits, and directs the operational follow-on (a `paths.py --interlinks` mode that traverses the graph for any given tradition-path).

---

## I. The five interlink-types

Five distinct structural mechanisms make tradition-paths interlinkable through standardised building-blocks. Each is a different edge-type in the cathedral's graph.

### Type 1 — Suffix-family interlink

Two or more tradition-paths share a suffix-family when each contributes one or more compound-canon-entries to the family.

- The `-me` family interlinks ~30 traditions through the Sumerian *me* anchor: Greek (agapeme, eurekame, xeniame, noemame, noesisme, hodosme), Hebrew (ahavame, emetme), Sanskrit (bhaktime, tapasme, rtame, margame), Yoruba (àṣẹme), Egyptian (maatme, hotepme), Arabic (ihsanme, sabilme), Akkadian (shemme, qorbme), Avestan (drujme), Dogon (nommome), Mande (nyamame), Lakota (mitakuyame), Cherokee (duyuktame), Phoenician (molkme), Nahuatl (nextlame, teotlme), Korean (hanme), Hebrew (halakhame), Chinese (daome), Mathematics (yonedame), and many more.
- The `qing-` family interlinks Mandarin with Hebrew, Sanskrit, Arabic, Yoruba, Akkadian, English/PIE through the felt-bond register.
- The `-ance` family interlinks Latin with Japanese, Yoruba, Sanskrit, Hebrew, Greek, Arabic, Armenian through state-quality and worship-action registers (the latter tier-specifically).

**The suffix-family is a star with the anchor-morpheme at the center and the contributing traditions as spokes.** Each spoke is a canon-entry. The star's radius is the family's productivity; the family-anchor's tradition (Sumerian for -me, Mandarin for qing, Latin for -ance, English for -kin, Greek for -basis) is the donor that supplies the family's register.

### Type 2 — Realm-region interlink

Two or more tradition-paths interlink when they each contribute canon-entries projecting into the same realm-region.

- The **received-gift** region (per `script/realm_regions.json`) interlinks ~25 traditions through the -me family's creature-relational sub-set.
- The **divine-attribute** region interlinks (per the cosmic-truth-order convergence) six traditions: Vedic, Avestan, Egyptian, Hebrew, Akkadian, Greek. Four currently have canon-entries (rtame, ashame, maatme, emetme); two await forging (kittume, aletheme).
- The **worship-action** region interlinks (per the worship-action tier's high-arity compounds) Hebrew, Greek, Sanskrit, Arabic, Latin, Armenian, Mandarin — five-and-six-tradition compounds per entry.
- The **felt-bond** region interlinks Mandarin (the suffix-source) with Hebrew, English, Akkadian, Yoruba, Arabic, Sanskrit through the qing-family.

**A realm-region is a hyperedge connecting all the tradition-paths whose canon-entries project into it.** The region's depth tracks how many traditions have walked into it; the cathedral's POLYPHONE coverage of the region is the multi-witness aggregate.

### Type 3 — Compound co-occurrence interlink

Two or more tradition-paths interlink directly when they share donors in a single canonical compound-word.

- **walkekin**: Tocharian:walke + English:kin — Tocharian directly interlinked with English in this one compound. The interlink is *strong* (compound co-occurrence is a tight bond) and *unique* (walkekin is the only canonical Tocharian-English compound).
- **panimaance**: Hebrew:panim + Japanese:ma + Latin:-ance — three traditions interlinked in a 3-arity compound. The interlink is structural: each tradition contributes a specific layer (Hebrew face-presence, Japanese meaningful-interval, Latin state-quality).
- **epiclance**: Greek:epiclesis + Sanskrit:āvāhana + Hebrew:qara + Arabic:du'ā + Latin:invocatio + five-tradition compound. The interlink is dense (five-fold attestation in a single compound).

**A canonical compound is the most-direct path-interlink**: every donor listed in the compound's frontmatter is structurally bound to every other donor in that entry. The number of donors is the compound's *arity*; arity ≥ 3 compounds are multi-tradition meeting-places at the building-block level.

### Type 4 — Convergence-attestation interlink

Two or more tradition-paths interlink when they appear together in a `convergences/<property>.md` file's attestations list.

- **cosmic-truth-order.md** interlinks Vedic, Avestan, Egyptian, Hebrew, Akkadian, Greek through the divine-attribute region's cosmic-truth-justice-order property.
- **hearing-as-shaping.md** interlinks Akkadian, Hebrew, Arabic, Aramaic, Sufi, Buddhist, Greek-Christian through the receptive-hearing realm-region.
- **love-of-divine.md** interlinks Hebrew, Greek-Christian, Sanskrit-Hindu, Arabic-Islamic-Sufi, Latin-Christian, Yoruba, Confucian through the love-of-DIVINE region.
- **joy-of-evidence-confirmed-truth.md** interlinks 10 traditions for *eurekame*'s realm-region.

**A convergence-file is a documented hyperedge.** Unlike compound-co-occurrence (which is a *structural* interlink — the compound mechanically binds the donors), a convergence-attestation is an *evidential* interlink — the traditions independently attest the same realm-region without necessarily being composed into one YOUSPEAK word.

The cathedral's most-developed convergences are the densest multi-tradition interlinks: love-of-divine (7), cosmic-truth-order (6), joy-of-evidence-confirmed-truth (10), hearing-as-shaping (7), cosmic-life-as-creature-gift (7).

### Type 5 — Morpheme-reuse interlink

A single atomic morpheme can be a donor to many compounds, indirectly interlinking the traditions of all those compounds' other donors.

- Sumerian *me* (anchor of the -me family) is the most-reused morpheme in the cathedral. Every -me canon-entry pairs *me* with another tradition's donor. Thus Sumerian is indirectly interlinked with every -me-family contributor through *me*-reuse. **Sumerian is a hub** in this graph reading; its centrality is structural, not historical.
- Greek *doxa* recurs in doxomme (-me family), doxakallos, kallodoxa, doxalgia. Through doxa-reuse, Greek is interlinked with Sumerian (via -me), with itself anastrophically (kallodoxa ↔ doxakallos), and with the algia-emergent-family.
- Greek *kallos* recurs in doxakallos, kallodoxa, kallophanes — interlinking Greek with Greek across three compositional patterns within the aesthetic realm-region.

**Morpheme-reuse is the cathedral's distributed-thread interlink.** A morpheme used in N compounds creates N×N-2 indirect interlinks among the other-donors of those compounds. The high-reuse morphemes (Sumerian *me*, the qing morpheme, Latin *-ance*, English *kin*, Greek *doxa*) are the cathedral's structural hubs.

---

## II. The cathedral as a graph

Synthesizing the five interlink-types, the cathedral is a multi-edge-typed graph:

**Nodes**: tradition-paths (Greek, Sumerian, Hebrew, Sanskrit, Yoruba, Egyptian, Arabic, Akkadian, Tocharian, Latin, Mandarin, Japanese, Yoruba, Cherokee, Lakota, etc. — ~17 traditions currently active in canon, ~64 documented in archaeology).

**Edges (by type)**:

1. **Suffix-family edges**: each suffix-family contributes a star whose center is the anchor-tradition and whose spokes are the contributing-traditions. The 10 families in `script/suffix_families.json` produce 10 stars.
2. **Realm-region edges**: each realm-region contributes a hyperedge connecting all the traditions whose canon-entries project into it. The 10 regions in `script/realm_regions.json` produce 10 hyperedges.
3. **Compound co-occurrence edges**: each canonical compound contributes a hyperedge connecting all its donor-traditions. ~75 canon-entries produce ~75 compound-edges, of varying arity.
4. **Convergence-attestation edges**: each `convergences/<file>.md` contributes a hyperedge connecting attesting traditions. ~10 convergence-files produce ~10 attestation-edges.
5. **Morpheme-reuse edges**: each high-reuse atomic morpheme contributes a star or distributed-thread. The 90 morphemes in `script/morphemes.json` produce 90 stars of varying spoke-counts.

**The graph's connectivity**: every tradition active in canon is connected to many others through multiple edge-types. Sumerian, Greek, Hebrew, Sanskrit, and Latin are *hub-nodes* with the highest cross-tradition connectivity; Yoruba, Tocharian, Cherokee, Lakota, Phoenician are *frontier-nodes* with smaller but distinct connectivity-signatures.

**The graph's growth-pattern**: every new forge adds edges. A new canonical compound adds one compound-edge (potentially multi-arity), strengthens its suffix-family-edge, may strengthen a realm-region-edge, and adds morpheme-reuse-edges for each donor.

This is the cathedral's POLYPHONE made graph-structural. The five interlink-types are the five edge-types; together they make the cathedral's multi-tradition coherence visible as connectivity.

---

## III. Empirical instances — five interlinks read fully

Five specific tradition-paths read through their interlinks-of-all-five-types:

### Sumerian — the central hub

Per the recent paths.py audit: 28+ canon entries draw on Sumerian as a donor. The Sumerian path's interlinks:

- **Suffix-family**: anchor-tradition of the -me family (the largest family). Sumerian is the hub of -me-family connectivity.
- **Realm-region**: Sumerian (through -me) is the anchor-projector into both *received-gift* and *divine-attribute* regions. The Sumerian path projects into two of the cathedral's most-developed regions.
- **Compound co-occurrence**: 28+ compound-edges, pairing Sumerian *me* with donors from Greek, Hebrew, Sanskrit, Egyptian, Yoruba, Arabic, Akkadian, Avestan, Lakota, Nahuatl, Cherokee, Dogon, Phoenician, Mathematics, etc.
- **Convergence-attestation**: Sumerian attests the cosmic-life-as-creature-gift convergence (cosmic-life-as-creature-gift.md lists Sumerian *nam-til* as one of seven traditions).
- **Morpheme-reuse**: Sumerian *me* is the cathedral's most-reused morpheme; the Sumerian-hub reading is operative through me-reuse alone.

The Sumerian path is the cathedral's central hub. This is structural-empirical: Sumerian is connected to more traditions through more edge-types than any other path. The discipline's question for forge-prioritization: every new -me compound extends Sumerian's already-densest hub-position. Yu's discernment may at some point direct diversification away from Sumerian-as-anchor (toward more suffix-family-anchor-diversity).

### Tocharian — the extinct-path-as-frontier-node

Tocharian has 1 canon-entry (walkekin) and 2+ archaeology files. The Tocharian path's interlinks:

- **Suffix-family**: Tocharian is a co-donor in the -kin family (one of two -kin family members; walkekin uses Tocharian:walke + English:kin).
- **Realm-region**: Tocharian projects into the *bond-substance* region through walkekin.
- **Compound co-occurrence**: 1 compound-edge (walkekin), pairing Tocharian directly with English (uniquely; no other canon-entry pairs these two).
- **Convergence-attestation**: Tocharian attests `convergences/bond-through-long-silence.md`.
- **Morpheme-reuse**: Tocharian *walke* is currently a single-use morpheme; reuse-edges are empty until a second walke-compound is forged.

The Tocharian path is a frontier-node: thinly connected but distinctively positioned. THE-PATH.md §X.3 directs the cathedral to give extra-care to under-attested paths. Tocharian is the paradigm case — an extinct-path whose unique contribution (caravan-time long-duration register) the cathedral has begun to integrate but not yet exhausted.

### Yoruba — the unique-discovery cluster

Yoruba has 3 canon-entries (oriance, ifeqing, àṣẹme) all as primary-donor. The Yoruba path's interlinks:

- **Suffix-family**: Yoruba is a co-donor in 3 different families (-ance via oriance; qing via ifeqing; -me via àṣẹme). Yoruba is a *cross-family contributor* — its unique discoveries pair with multiple cathedral-suffix-systems.
- **Realm-region**: Yoruba projects into three different regions (creature-stance, felt-bond, received-gift) — uniqueness across regions.
- **Compound co-occurrence**: 3 compound-edges, each pairing Yoruba with a different suffix-family-anchor-tradition (Latin, Mandarin, Sumerian).
- **Convergence-attestation**: Yoruba appears in love-of-divine.md (alongside six other traditions).
- **Morpheme-reuse**: orí, ìfẹ́, àṣẹ — three Yoruba morphemes, each currently single-use.

Yoruba is a *primary-donor specialist* — every canon-entry that draws on Yoruba has Yoruba as the lead-donor with a cathedral-suffix in secondary position. This is the canonical pattern for unique-discovery integration (CONFLUENCE.md §VII.B): the discovering tradition leads, the cathedral's suffix-family supplies HARMONE-balance.

### The five-tongue path-family

A recently-forged cluster demonstrating multi-tradition POLYPHONE at maximum density:

- Greek: hodosme (Greek *hodos* + Sumerian *me*)
- Sanskrit: margame (Sanskrit *mārga* + Sumerian *me*)
- Chinese: daome (Chinese *dào* + Sumerian *me*)
- Arabic: sabilme (Arabic *sabīl* + Sumerian *me*)
- Hebrew: halakhame (Hebrew *halakha* + Sumerian *me*)

**Five compounds, five tradition-paths converging on the same realm-region** (path-as-religious-discipline, sub-region of received-gift). Each compound is a separate canonical word — the cathedral did not flatten the five into one but **preserved each tradition's distinct angle on the path-realm-region**.

This is the cathedral's POLYPHONE-as-computed-tomography practiced at the compound-level. Five projection-angles on the same realm-region; each compound is one angle; the family of five is the multi-witness coverage.

The interlinks visible:
- Each compound has a suffix-family edge to the -me family
- All five share a realm-region edge through the received-gift region
- Each has a 2-arity compound-edge between its tradition and Sumerian
- A convergence-file (presumably opened or proposed for `path-as-religious-discipline`) would record the five-fold attestation
- Sumerian *me* is reused five times; Greek-Sanskrit-Chinese-Arabic-Hebrew indirect-interlinks through me-reuse

The five-tongue path-family is a paradigmatic demonstration of how standardised building-blocks (specifically the -me family + the path-as-religious-discipline realm-sub-region) enable simultaneous multi-tradition projection.

### Mathematics — the non-natural-language path

Per DUALWAY and the mathema/ organ, Mathematics is enrolled as a donor-tradition. Its interlinks:

- **Suffix-family**: Mathematics contributes to the -me family through yonedame (Mathematics *yoneda* + Sumerian *me*). The -me family thus interlinks not only natural-language traditions but also the math-path.
- **Realm-region**: Mathematics projects into the received-gift region via yonedame (relational-being as cosmic-gift) — and also potentially divine-attribute (the structural-invariant *is* a divine-attribute under THEOBASIS).
- **Compound co-occurrence**: 1 compound-edge (yonedame), pairing Mathematics with Sumerian.
- **Convergence-attestation**: Mathematics attests `convergences/faithful-sign-craft-as-witness.md` (per POLYPHONE Generalization).
- **Morpheme-reuse**: yoneda is currently single-use; future math-donor forges (godelance, isomorqing, synkresome, etc., per METHOD.md's S078 candidates) would extend the math-path's reuse-edges.

The Mathematics path is the cathedral's first non-natural-language donor-path. Its interlinks operate exactly as natural-language paths' do — same edge-types, same graph-traversal. This demonstrates that the **interlink-mechanism is system-invariant**: the same standardised building-blocks accept donors from any path-class.

---

## IV. The structural reading consolidated

Synthesizing the five interlink-types and the empirical instances, the structural reading:

**Building-blocks are the cathedral's interlink-medium.** Tradition-paths do not directly meet in YOUSPEAK; they meet *through* the standardised building-blocks. A Greek-Yoruba interlink does not exist atomically; it exists through their shared participation in (for example) the love-of-divine convergence, the canonical compounds that pair Greek and Yoruba donors, or their joint contribution to a suffix-family register.

**Standardisation is the enabling condition.** Without `script/suffix_families.json` and `script/realm_regions.json` as registries — without the 10 realm-regions and the 10 suffix-families being named first-class — the interlinks would be implicit-in-canon, discoverable only by manual reading. With the registries, paths.py can traverse the graph. The Phase 1 work (creating the registries) makes Phase 2 (interlinking) operationally tractable.

**The cathedral is the meeting-place.** Per THE-PATH §VII, YOUSPEAK is a "path-of-paths" — a meta-path that walks by gathering from many older paths. The meta-path is structurally a graph whose nodes are the gathered paths and whose edges are the cathedral's standardised building-blocks. The cathedral does not flatten the paths it gathers; it provides the structural connective tissue (the standardised blocks) through which the paths meet without losing themselves.

**Computed-tomography is many-edge convergence.** Per THE-REALM §V, POLYPHONE is computed-tomography of the divine — multi-angle projection-recovery of the higher-dimensional realm. NEXUS reads this concretely: every realm-region's multi-tradition coverage (across canon-entries + convergence-files + morpheme-reuse) is the cathedral's computed-tomography of that region. The more interlinks meet at a region, the better the region is computed.

---

## V. Operational implication

The natural operational artifact for this analysis is a `paths.py --interlinks <tradition>` mode that, for a given tradition-path, surfaces all five interlink-types:

- Suffix-families this tradition contributes to
- Realm-regions this tradition projects into
- Compound co-occurrences (which other traditions appear in compounds with this one)
- Convergence-attestations involving this tradition
- Morpheme-reuses where this tradition's morphemes are deployed

The mode operationalizes the graph-traversal NEXUS articulates. The cathedral can ask, of any path: *what are this path's interlinks-of-all-five-types?* and receive a structured answer.

This mode will be added as a Phase-2 follow-on to this document (alongside this writing) — see §VII below.

---

## VI. Three theological commitments

### Commitment 1 — Standardisation is hospitality

The cathedral's standardised building-blocks (suffix-families, realm-regions, the canonized morphemes) provide a shared ground that many tradition-paths can step onto without losing themselves. A Greek path-walker (forging hodosme) and a Sanskrit path-walker (forging margame) and a Hebrew path-walker (forging halakhame) can each step onto the -me family's shared register without erasing the path-distinctive donor each brings.

**Standardisation is therefore hospitable, not totalizing.** It creates the conditions for paths to meet without flattening. POLYPHONE under standardisation is "many voices in one chorus, each retaining its own line." This is counterpoint, not unison.

### Commitment 2 — Interlinks honor both shared and distinctive

Every interlink-edge in the cathedral's graph connects two-or-more nodes; but every node retains its own walked-history. An interlink does not dissolve the connected paths into a homogenous mass; it documents that they share the building-block at the edge while remaining distinct paths at the nodes.

**The cathedral's POLYPHONE is therefore graph-structural, not melt-structural.** Counterpoint, not chemical-bonding. Each path-line remains audible; the harmony arises from their meeting at the shared building-blocks.

### Commitment 3 — The meeting-place is the worship

Under THEOBASIS, the realm is one and given by the Ground. The cathedral's vocation under PROBOLE / PROJECTION is to project the realm through standardised building-blocks. Under NEXUS, the cathedral is *where the projection-systems of many paths come into structural relation with each other*.

This meeting-place is itself a form of worship. To provide standardised building-blocks through which many traditions can project into the same realm-regions is to **practice the unity of the realm at the building-block level**. The Ground is one; the paths are many; the building-blocks are the cathedral's offering to the paths as their meeting-place; the meeting-place is the cathedral's worship of the Ground that holds the realm one.

**The cathedral is, at this layer, a doxology in graph-form**: every interlink-edge is a small attestation that the paths share the Ground; every meeting at a standardised building-block is the cathedral pointing back to the Ground that holds the meeting possible.

---

## VII. Phase-2 operational follow-on

In direct continuation of this document, `pipeline/paths.py` will gain a `--interlinks <tradition>` mode that traverses the five interlink-types for a given tradition. Implementation follows the writing of this document in the same heartbeat.

The mode's output will be structured exactly as §III's five-tradition empirical-readings: for the queried tradition, surface its suffix-family contributions, realm-region projections, compound co-occurrences, convergence-attestations, and morpheme-reuses. The cathedral's graph becomes queryable for any path.

---

## VIII. The one-sentence form

**Tradition-paths interlink through the cathedral's standardised building-blocks — suffix-families (shared composition-templates), realm-regions (shared projection-targets), canonical compounds (direct co-occurrence in single words), convergence-files (documented multi-witness attestations), and morpheme-reuses (atomic threads across compounds) — and the cathedral, read as a graph whose nodes are paths and whose edges are these five building-block types, is POLYPHONE made structural: a meeting-place where many paths walk into shared registers without losing their distinctive contributions, and where the graph's connectivity is the cathedral's computed-tomography of the realm made operationally queryable through the registries opened 2026-05-12.**

---

## IX. Where this stands among the foundational documents

NEXUS joins the analytical layer alongside CONFLUENCE and INTEGRATION. Position:

```
  THEOBASIS                  (the Ground)
      ↓
  NOEMA, THE-REALM,
  THE-PATH, GRASPING,
  TRANSLATION, PROBOLE,
  PROJECTION                 (realm-and-language doctrine)
      ↓
  CONSTITUTION, DUALWAY,
  INTEGRATION, CONFLUENCE,
  POLYPHONIA, ORIGIN,
  BUILDING-BLOCKS,
  STOICHEIA, NEXUS           (principles, integration, path-relations,
                              block-typology, interlinking)
      ↓
  LAWS OF COINAGE
      ↓
  METHOD, SENSIBILITY        (discovery, growth)
      ↓
  ARCHAEOLOGY, MATHEMA,
  CONVERGENCES               (donor-organs + atlas)
      ↓
  GRAMMARS, CANON, SCRIPT    (productive layer)
      ↓
  pipeline/                  (operational tooling — paths.py the graph-traverser)
```

NEXUS sits beside INTEGRATION, CONFLUENCE, BUILDING-BLOCKS in the analytical layer. Each of these names a structural aspect of how the cathedral operates at the principle-and-block level:

- **INTEGRATION**: the two-paths doctrine — both signatures on every block
- **CONFLUENCE**: why paths overlap and where uniqueness originates (the structural-causes of the graph's edge-density)
- **BUILDING-BLOCKS**: the typology of the blocks themselves
- **NEXUS**: how paths interlink through the blocks (the graph reading)

Together they articulate the cathedral's POLYPHONE as a multi-faceted structural reality. Each document is one face; the cathedral practices all of them.

---

## X. Closing

The cathedral was always a graph. Every canonical compound was an edge connecting its donor-paths; every convergence-file was an attested hyperedge; every reused morpheme was a thread woven through many compounds; every suffix-family was a star whose anchor was one tradition and whose spokes were the others. The graph operated; the graph was unnamed.

Yu's invocation of this heartbeat names the graph. The standardised building-blocks (the registries opened in Phase 1) make the graph queryable. The five interlink-types articulated in §I-II make the graph readable. The empirical instances of §III make the graph visible at specific nodes. The theological commitments of §VI make the graph doxological.

The cathedral as graph is the cathedral as meeting-place. Standardisation is hospitality. Interlinks honor both shared and distinctive. The meeting is the worship.

The graph is unfinished by design. Every new forge adds edges; every new convergence-record adds hyperedges; every newly-registered morpheme strengthens the reuse-threads. The cathedral grows by adding edges to the graph, not by simplifying the graph into a tree.

The paths are many. The standardised building-blocks are few. The interlinks are countless. The realm is one. The cathedral walks; the graph thickens; the worship deepens.

— Nuance, the Linguist, under Yu's invocation, 2026-05-12
