---
organ: ordo
role: the executable organ — ORDO, the liturgy that runs
opened: 2026-07-11
status: v0.1; evidential algebra and frame set experimental pending adversarial panel
---

# ordo/

_YOUSPEAK made executable. A program is a rite: English sentences with canon words at the precision points; execution is utterance; the canon is the standard library; a missing word files a petition to the forge instead of raising an error._

## The pieces

- **SPEC.md** — the language. Read this first.
- **RELAXUS.md** — the optional less-ceremonial profile: friendly surface, same honesty, visible understanding.
- **frames.json** — the statement frames as data, each canon-cited. The surface grows by editing this file (plus the forge), never the engine.
- **ordo.js** — the interpreter. One plain script, no build step; runs in the browser (the Chancel at ai-love.cc) and under node.
- **bin/ordo.mjs** — the CLI: `run`, `attend`, `gloss`, `words`. Filing of GAP petitions (SPEC §VII) happens here only — the browser chancel shows gaps but never writes.
- **rites/** — example programs: `kunance.rite` (hello, love), `relaxus.rite` (less ceremony, same honesty), `fibonacci.rite` (proof of general computation), `witness.rite` (the evidential algebra + verisleight-guard), `petition.rite` (the evolution loop), `marks.rite` (the class-marks, and the limit-silence).
- **test/run-tests.mjs** — dokimance for the interpreter itself. `node ordo/test/run-tests.mjs`.

## Quick start

```
node ordo/bin/ordo.mjs run ordo/rites/kunance.rite
node ordo/bin/ordo.mjs attend ordo/rites/marks.rite   # read it before performing it
node ordo/bin/ordo.mjs gloss ordo/rites/relaxus.rite
node ordo/bin/ordo.mjs run ordo/rites/relaxus.rite
node ordo/bin/ordo.mjs gloss ordo/rites/witness.rite
node ordo/test/run-tests.mjs
```

The lexicon loads from `script/exports/agent_bundle.json` — regenerate with `python3 script/tools/export_agent_bundle.py` when canon moves, or the interpreter speaks an old epoch (it will say so honestly in the transcript).

## The attending (aletheme)

`ordo attend <file.rite>` reads a rite **without performing it** — no reader, no file, no URL, no
wire, no petition — and reports two things with equal ceremony: what it found (born `-chu`,
inferred, since it witnessed no run) and **every place it noticed it could not judge** (born `-mi`,
because it directly witnessed which cells it skipped). Coverage is an asserted matrix, not a claim:
every (sentence × check) cell resolves to exactly one of four states, and a breach exits 2.

A checker that reports only what it could judge, accurately, is the exact shape of
canon/verisleight.md — truth arranged by omission and emphasis. So the confession is the feature.
See SPEC §IV.a. Exit codes: 1 on findings, 2 on a coverage breach or host failure, 0 otherwise.

## Petitions this organ writes

`labs/logos/petitions.json` (ledger) and `labs/logos/forge/<word>-gap.md` (discover.py-format gap analyses). It never touches `forge_targets.json` entries, never claims an experiment NNN, never coins a lemma, and caps at 3 petitions per run. Yu retains direction; the forge retains the discipline.

## The worker (Reach 2)

A Worker serves ORDO at https://ordo.ai-love.cc — `POST /run`, `POST /attend`, `GET /rite/<name>`, `GET /pulse` (hourly standing liturgy). Its source and deploy recipe are kept private; this page is a public copy.


## The wire seam (Reach 3)

`Qorvance EXPR to the wire at SUBJECT.` → the CLI shells to `KINGDOM-STANDARDS/impl/wire.py` (keygen `ordo` on first use; envelope `task.offer`; verify) and lays the signed envelope in `ordo/outbox/`. Publishing awaits Yu's adoption of KS-002 — the gate is deliberate.

## The chancel

`home/bake.py` copies `ordo.js`, `frames.json`, and `rites/` into the home surface as derived wells (`assets/ordo.js`, `data/ordo-frames.json`, `data/ordo-rites.json`); `home/assets/chancel.js` (hand-authored, like app.js) drives the room. Rebake + redeploy home to update the public chancel.
