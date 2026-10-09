# canon · the standing words

Each canonical entry has crossed the 5-axis assessment threshold (≥ 7.5 weighted) and bears its full genealogy: donor-morphemes, tradition labels, the gap it names, the example sentence.

## Tiers

- **[core/](core/)** — Core canon (currently 37 entries). The cathedral's spine.
- **[worship-action/](worship-action/)** — Worship-action verbs (currently 9 entries). Forged 2026-04-30 to fill the verb-register gap.
- Specialised entries — live as `canon/<word>.md` at this level (~16 entries). Below the Core threshold but defended.

## Master list

The single living index of all standing words sits at the cathedral's root, not here:

→ [../canon.md](../canon.md)

## How a word reaches canon

The pipeline:

```
labs/logos/experiments/NNN-<word>.md  →  pipeline/assess.py
                                       ↓
                                weighted_total ≥ 7.5
                                       ↓
                            canon/{core,worship-action}/<word>.md
```

See [../METHOD.md](../METHOD.md) for the Six Patterns of discovery and [../pipeline/](../pipeline/) for the CLI tools.
