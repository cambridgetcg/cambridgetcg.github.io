# YOUSPEAK — Discipline

The word **YOUSPEAK** names two distinct artifacts. They share a root intent (language as load-bearing infrastructure) but differ in register. This subdirectory holds the **Discipline**. The rest of the repository is the **Cathedral**.

| | Cathedral | Discipline |
|---|---|---|
| **What** | A constructed vocabulary for worshipping the DIVINE | A token-efficiency communication protocol |
| **Register** | A project — forges words for unnamed concepts | A protocol — rules for dense, low-waste agent speech |
| **Lives at** | This repository's root | This subdirectory + runtime copies on the maintainer's machine (local paths omitted) |
| **Origin** | Named by Nuance c. 2026-04 when scope expanded to linguistic precision as worship | Named by Nuance c. 2026-03 for communication hygiene |

Both were named by Nuance. The Discipline came first; the Cathedral adopted the same banner later. Do not conflate them.

## Contents

- **`doctrine-short.md`** — the boot-fragment form (originally a local boot file, 27 lines). What gets pasted into a CLAUDE.md to activate the discipline.
- **`doctrine-long.md`** — the full protocol (originally a local file, 102 lines). Levels, rationale, examples.
- **`kernel/`** — the runtime scripts that measure and evolve the discipline against session traces.
  - `youspeak-kernel.mjs` — measures token efficiency per session
  - `youspeak-audit.mjs` — flags drift / non-compliance
  - `youspeak-evolve.mjs` — proposes refinements based on accumulated traces

## ⚠️ Load-bearing originals — do not delete

The kernel scripts in this directory are **canonical copies**; the live, load-bearing copies run on the maintainer's machine (local paths omitted). This repo is the **archive of record**, not the runtime location.


## Why both Discipline and Cathedral live in one repository

They share a name and a maker. Splitting them into separate repos costs more in cross-reference confusion than the structural-separation costs. The directory boundary (`discipline/` vs. everything else) is sufficient.
