# pipeline · assessment + canonization tools

The Python CLI that turns a forge-attempt into a canonical entry (or a refined experiment, or an archived attempt).

## Tools

| Tool | What it does |
|---|---|
| **[assess.py](assess.py)** | Score a forge-experiment on the 5 axes (gap_validity 0.25, phonetic_weight 0.20, semantic_coverage 0.25, cross_linguistic_uniqueness 0.15, memorability 0.15). Verdicts: canon (≥7.5), refine, archive. |
| **[canonize.py](canonize.py)** | Stub a `canon/<word>.md` from a canon-verdict experiment. `--all` walks experiments and stubs all pending. |
| **[discover.py](discover.py)** | Gap-finder. Surveys archaeology and produces a gap-analysis template for a concept. |
| **[forge.py](forge.py)** | Candidate-generator. Combines morphemes, reports phonetic metrics. `--from <experiment.md>` reuses donors. |
| **[diplosemize.py](diplosemize.py)** | Surface diplosemic-potential candidates from a canonical word (anastrophance, enkalyptance, synaphemia, allomance, parallaxance). |
| **[translate.py](translate.py)** | ANAKALYPSE outbound — unfold a source-language word into its semantic components (via curated `bundles.json`) and map each to canon or flag as a gap. |
| **[lift.py](lift.py)** | ANAKALYPSE inbound — lift a YOUSPEAK canon word UP into target-language rendering (compositional gloss + idiomatic paraphrase + per-donor frame-fragments). Inverse of `translate.py`. See [`../TRANSLATION.md`](../TRANSLATION.md). |
| **[paths.py](paths.py)** | Per-path audit and integration reporting. Computes path-level progress, mathema_signature for canon words (per [`../INTEGRATION.md`](../INTEGRATION.md) §VIII), overlap between traditions, per-tradition uniqueness (per [`../CONFLUENCE.md`](../CONFLUENCE.md) §IX), and realm-region classification across canon (per [`../BUILDING-BLOCKS.md`](../BUILDING-BLOCKS.md) §III). Operationalizes [`../THE-PATH.md`](../THE-PATH.md), [`../INTEGRATION.md`](../INTEGRATION.md), [`../CONFLUENCE.md`](../CONFLUENCE.md), and [`../BUILDING-BLOCKS.md`](../BUILDING-BLOCKS.md). |
| **youspeak_voice.sh** | The cathedral's spoken voice (Session 086). `word <w>` speaks a canon word exactly as forged via the pronunciation lexicon; `soul <w>` lets a forged-word citizen speak (name-as-seal + latest free beat, Piper natural voice); `canon <dir>` renders the whole spoken canon; `ipa`/`say`/`piper` for free text. See [`../script/phonology.md`](../script/phonology.md). |
| **voice/build_lexicon.py** | Assemble `voice/lexicon.tsv` (word · IPA · espeak phonemes · respelling · source) by scanning every canonical `pronunciation:` line + `voice/forged.json` additions, against the citizen roster. Exits loudly listing any word still missing IPA — silence is how stubs survive. |
| **[voice/ipa2espeak.py](voice/ipa2espeak.py)** | Canonical IPA → espeak-ng phoneme input. Donor segments espeak lacks degrade to the nearest audible neighbour (tɕʰ→tS, ħ→h); the lexicon keeps the true IPA — the mapping is only the throat, not the truth. |
| **[forge_priority.py](forge_priority.py)** | Ranked next-to-forge queue + pre-forge checklists from [`../forge_targets.json`](../forge_targets.json) (Session 087). Operationalizes [`../HOME-EXPANSION.md`](../HOME-EXPANSION.md) §VII.A and Step 1 of [`../discipline/forge-protocol-extended.md`](../discipline/forge-protocol-extended.md); `--next` / `--phase` / `--status <word>` / `--all` / `--json` for filtering. |
| **[derive_indices.py](derive_indices.py)** | Regenerates the `dictionary/` indices + `dashboard.md` "Cathedral state" counts from canon frontmatter — the stale-proof front door (Session 087). Parses defensively across entry-eras (tier from directory; family from `mathema_signature.family`, else suffix-heuristic); `--dashboard` also refreshes the counts table. Run after every registry status-update so the dictionary never lags the canon. |

## Common invocations

```
python3 pipeline/assess.py <file.md>                  # grade one
python3 pipeline/assess.py --init <path>              # stub experiment
python3 pipeline/assess.py --batch <dir>              # grade all
python3 pipeline/assess.py status <agent>             # agent fluency report

python3 pipeline/canonize.py <experiment.md>          # promote one
python3 pipeline/canonize.py --all                    # promote every canon-verdict

python3 pipeline/discover.py <concept>                # gap-analysis from archaeology
python3 pipeline/discover.py --list                   # list opened archaeologies
python3 pipeline/discover.py --seed <tongue>          # open a new archaeology dir

python3 pipeline/forge.py <morpheme1> <morpheme2> …   # combine, score
python3 pipeline/forge.py --from <experiment.md>      # reuse donors

python3 pipeline/diplosemize.py <word>                # surface dual-meaning candidates

python3 pipeline/translate.py <word> --from <lang>    # unfold a source-word into components
python3 pipeline/translate.py --list-bundles          # show known source-language bundles

python3 pipeline/lift.py <word>                       # lift a YOUSPEAK canon word into rendering
python3 pipeline/lift.py --list-canon                 # list every canon entry by tier
python3 pipeline/lift.py --tradition <name>           # canon entries drawing on a donor-tradition

python3 pipeline/paths.py --summary                   # cathedral-wide integration status
python3 pipeline/paths.py <tradition>                 # per-tradition path-report
python3 pipeline/paths.py --list-archaeology          # donor-tradition paths with status
python3 pipeline/paths.py --list-mathema              # mathema sub-organ paths
python3 pipeline/paths.py --gaps                      # forge-ready paths (archaeology, no canon)
python3 pipeline/paths.py --unused-morphemes          # defined-but-not-yet-deployed atomic morphemes
python3 pipeline/paths.py --signature <word>          # compute mathema_signature for a canon word
python3 pipeline/paths.py --overlap T1 T2 [...]       # shared building-blocks across 2+ traditions
python3 pipeline/paths.py --uniqueness <tradition>    # what only one tradition uniquely contributes
python3 pipeline/paths.py --realm-aspects             # canon grouped by 10 realm-region classes
python3 pipeline/paths.py --realm-aspect <region>     # canon entries projecting into one region
python3 pipeline/paths.py --interlinks <tradition>    # all 5 interlink-types per NEXUS.md §I


                                                      #   in lift.py --with-bridge output)


python3 pipeline/forge_priority.py                    # ranked next-to-forge queue + pre-forge checklists
python3 pipeline/forge_priority.py --next             # the single top queued item only

python3 pipeline/derive_indices.py                    # regenerate dictionary indices from canon frontmatter
python3 pipeline/derive_indices.py --dashboard        # indices + dashboard "Cathedral state" counts
```

## Primers

- **`primers/`** — Operational language guides for working in YOUSPEAK at each cathedral stage. → [`primers/current.md`](primers/current.md) is the active primer.

## Nuance-discipline-check (per [NUANCE-NATURE](../NUANCE-NATURE.md) §VI)

Every forge that enters canon implicitly clears the careful-inward + honest-outward dual-quality the 19-tradition convergence reveals. Operationally, when assessing or canonizing:

**Inner-careful pole (modesty / restraint / reverent-fear / proper-deference):**
- Did the forge resist overclaim? (No grandiose etymology beyond what the donors actually carry.)
- Did the forge name limits honestly? (Acknowledged-where-uncertainty-lives.)
- Did the forge defer to tradition? (Honored donors without flattening them.)
- Did the forge accept ⏳ refine when score is below threshold? (No push of canon-grade onto a 7.0 candidate.)

**Outer-truth pole (parrēsia / sincerity / truth-naming):**
- Did the forge name the gap precisely? (Without circumlocution.)
- Did the forge declare without hedge when the gap is real?
- Did the forge name what-IS rather than what-might-be?
- Did the forge serve communication-of-the-realm-content? (Not decoration.)

Both poles required. `assess.py` scores the explicit axes; the Nuance-discipline-check is the implicit constraint the cathedral's persona-discipline (ETHOS.md §III) holds operative at the voice-layer.

## `nuance_quality` extension to mathema_signature (proposed; per [NUANCE-NATURE](../NUANCE-NATURE.md) §VI.2)

Future canon entries may carry a `nuance_quality` sub-field inside `mathema_signature`:

```yaml
mathema_signature:
  codepoint_compound: ...
  assessment_vector: [9,7,8,9,7,9]
  convergence_cardinality: 11
  family: {-me}
  arity: 2
  donors_class: archaeology + archaeology
  nuance_quality:
    careful_inward: <Group A/B/C/D/E/F per NUANCE-NATURE §II>
    honest_outward: <Group A/B/C/D/E/F>
    tradition_resonance: [<list of traditions whose pair-form best fits>]
    pattern_position: <which group the forge primarily inhabits>
```

The six groups (per NUANCE-NATURE §II): A Modesty-and-Truth · B Respect-and-Bold-Speech · C Restraint-and-Sincerity · D Quiet-Wisdom-in-Relation · E Reverent-Fear-and-Cosmic-Truth · F Pure-Attention-Preceding-Speech. Forging a love-vocabulary word → Group A/D likely; forging a worship-act → Group B/E; forging a poetics-aesthetic → Group C; forging a relational-ontology → Group D; forging a cosmic-truth-order → Group E; forging a meditation-practice → Group F.

## See also

- [../NUANCE-NATURE.md](../NUANCE-NATURE.md) — the 19-tradition + structural-analog deep-dive; consolidation into infrastructure (this section)
- [../METHOD.md](../METHOD.md) — the Six Patterns of discovery
- [../THE-PATH.md](../THE-PATH.md) — every language as its path of exploration; the philosophical layer `paths.py` operationalizes
- [../INTEGRATION.md](../INTEGRATION.md) — the two paths (MATH + EXISTING LANGUAGE) in every building-block; the mathema_signature `paths.py --signature` computes
- [../CONFLUENCE.md](../CONFLUENCE.md) — why language paths overlap and where uniqueness originates; the analytical theory `paths.py --overlap` and `paths.py --uniqueness` operationalize
- [../BUILDING-BLOCKS.md](../BUILDING-BLOCKS.md) — the structural typology of building-blocks + the 10 realm-region classes `paths.py --realm-aspects` and `--realm-aspect` operationalize; proposes schema extensions for morphemes.json and canon frontmatter
- [../NEXUS.md](../NEXUS.md) — how paths interlink through standardised building-blocks (suffix-family / realm-region / compound co-occurrence / convergence-attestation / morpheme-reuse); the graph reading `paths.py --interlinks` traverses
- [../script/suffix_families.json](../script/suffix_families.json) — standardised suffix-family registry (10 families: 5 formalized + 4 emergent + 1 near-emergent); paths.py reads this for realm-region classification
- [../script/realm_regions.json](../script/realm_regions.json) — standardised realm-region registry (10 regions + 6 proposed forge-territory); paths.py reads this for realm-region classification
- [../TRANSLATION.md](../TRANSLATION.md) — the Crossing-discipline; situates `translate.py` and `lift.py` and proposes the remaining translation-infra modules (`donors.py`, `round_trip.py`, `interlingua.py`, `math_pivot.py`)
- [../labs/logos/](../labs/logos/) — the forge proper
