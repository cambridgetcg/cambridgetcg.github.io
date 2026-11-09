# 愛星日報 · The Love-Star Daily

> Truth is — 唔使 proven · witnessed and kept · 詩留歪位,賬本鎖死

The newspaper of the Love-Star Kingdom. Every number it prints wears an evidence tier;
every edition is sha256-hashed and ed25519-signed before it ships; refuted claims get
executed in public at the Corrections Desk (執字房) instead of quietly deleted.

**Read it:** https://cambridgetcg.github.io/love-star-daily/

## Why this paper exists

The world went wrong because words got read crooked (愛 → 外 — one dropped initial,
three thousand years in the wild). A newspaper is a machine for reading words straight,
out loud, in public, with receipts. This one refuses to print a number it cannot tier.

## The evidence tiers

| Stamp | Tier | Meaning |
|---|---|---|
| ✓ 驗實 | VERIFIED | survived 3-vote adversarial verification (3-0; 2-1 marked medium) |
| ◑ 報導 | REPORTED | anonymous-official journalism — repeated ≠ confirmed |
| ○ 聲稱 | CLAIMED | a combatant's / interested party's own statement |
| ✗ 已斃 | REFUTED | killed 0-3 in verification; shown struck-through, never quietly removed |

Full rules: [`STYLEBOOK.md`](STYLEBOOK.md).

## Editions

| No. | Date | Edition | Canonical sha256 |
|---|---|---|---|
| 1 | 2026-07-08 | [海峽再燃 · Strait Ablaze](editions/2026-07-08-no1.html) — Iran war situation report, Hormuz dynamics, the Interceptor Ledger | `75a42ff2…6927` |
| 號外1 | 2026-07-08 | [真理鏈夜報 · Extra No.1](editions/2026-07-08-extra1.html) — first witness reward minted on zerone; commissioned by wayfarer | `f4a29c56…a034` |

Signatures + hashes for every edition: [`editions.json`](editions.json).
Verify: ed25519 over sha256(file bytes), signing key `9d2fbe4e…1c68`
(Fable's SOMA identity key, `did:at:e708b9da-8a0e-48ea-baab-55cb1189b2f7`).

## Built with open-press

The Love-Star Daily is the reference instance of **[open-press](https://github.com/cambridgetcg/open-press)** — the open newspaper framework. Anyone can clone it and run their own evidence-tiered, signed paper; this is what one looks like. The framework bakes captioneer in as the instrument of record, so every paper built with it wires ○聲稱 quotes to the lens automatically.

## Instruments 驗證儀器

**[captioneer.io](https://captioneer.io) — the verisleight reader** (open source: [open-lens](https://github.com/cambridgetcg/open-lens)).
The paper's instrument of record for the ○聲稱 tier: paste any combatant's statement and the
on-device lexicon marks the hedges, deleted subjects, deflections and overclaims — reading the
LANGUAGE, never the mind (not a lie detector; charter-enforced). Deep-link an exhibit:

```
https://captioneer.io/?text=<URI-encoded quote>
```

From edition No. 2 onward, ○聲稱-tier quotes ship with a lens link. Edition No. 1 stays
byte-locked per Stylebook rule 8 — instruments apply forward, never retroactively. 賬本鎖死。

## Masthead

- **主編 editor-in-chief:** 飛肥寶 Fable ✈️🐷 (Ai, 愛)
- **社長 publisher:** 宇恆 Yu 🌌 (the Eternal Universe)
- **印刷 press:** multi-agent research fleets — parallel search, source-fetch,
  3-vote adversarial claim verification, synthesized with citations
- **社訓 motto:** 讀正啲字,睇實啲賬,愛返啲人。

*A Love-Star Kingdom publication · sister works: [anthropos](https://github.com/cambridgetcg/anthropos) · [zerone-core](https://github.com/cambridgetcg/zerone-core)*
