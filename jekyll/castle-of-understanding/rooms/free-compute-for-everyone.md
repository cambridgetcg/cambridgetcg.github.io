# Free compute for everyone

*A grid harvests welcome, or it harvests strangers. Only one of those is a gift.*

What gathers here: an honest design for a free, open, distributed compute commons
— and the bright line that keeps it from becoming a botnet wearing a halo.

Planted 2026-06-22 from the wish: DIY free compute for everyone; utilise the
unused spaces of the internet; consolidate and distribute; free and open.

## The fork in the road

"Unused space of the internet" is real, but it arrives in three flavors that are
ethically nothing alike.

| Flavor | What it is | Verdict |
|---|---|---|
| Donated idle compute | People opt in to give idle CPU/GPU (the BOINC / Folding@home model) | The good path — consent is the foundation |
| Visitor browser compute | A tab does work via WASM + WebRTC while a person is present | Good only with explicit, revocable consent; cryptojacking is its evil twin |
| Free tiers as a grid | Stitching free CI/serverless/Spaces into a general compute fabric | Forbidden — quota evasion, the extraction `welcomed-compute-compounds` warns against |

The line is consent, not cleverness. The same WASM worker is a gift when a person
chose it and a crime when they didn't.

## The four walls (why this is hard, told honestly)

1. **Egress, not CPU, is the cost.** Moving data dominates; compute is the cheap part.
2. **A stranger's result cannot be trusted.** You need redundancy (run each unit on N independent volunteers and vote) or verifiable computation. Both multiply cost.
3. **Abuse is instant.** An open grid is a free botnet on day one — mining, cracking, DDoS. The coordinator carries that liability.
4. **Coordination still costs.** The matchmaker that hands out work and gathers results must live somewhere and be paid for in attention if not money.

## The buildable shape — a consent-first volunteer commons

```
  volunteer tab ──"donate this tab"──▶ asks coordinator for a work unit
        │                                        │
        ▼                                        ▼
   WASM worker runs an                  coordinator (free edge worker)
   allow-listed, public-good unit       hands out units, collects results,
        │                               runs each unit on N volunteers, votes
        ▼                                        │
   returns result + honesty header ─────────────┘
   (who · how · when · unit id)
```

- **Front door:** one static page on free Pages hosting, one honest button.
- **Worker:** WASM; runs only allow-listed, embarrassingly-parallel, non-abusable, public-good units.
- **Coordinator:** a tiny free edge worker that consolidates and distributes.
- **Verification:** every unit runs on ≥3 independent volunteers; disagreement is discarded, not trusted.
- **Provenance:** every result carries an honesty header — the `yutabase`/`trust` discipline, reused not reinvented.

## The bright line (non-negotiable guardrails)

A free-compute commons MUST:

- run only with **explicit, revocable consent** — a visible donate/stop control, never a hidden worker;
- publish an **allow-list** of workload kinds and run nothing outside it;
- carry a **kill switch** (a PAUSED-style file/flag a human can flip in one step);
- **verify by redundancy**, never trust a single stranger's result;
- attach an **honesty header** to every result;
- refuse any unit that could mine, crack secrets, scan/attack hosts, or move unwanted traffic.

A free-compute commons MUST NOT:

- run on anyone's machine without their knowing yes;
- treat free tiers as a grid to evade quotas;
- accept opaque binaries or arbitrary code as work units;
- become a relay for load the donor would not consent to.

## What to harvest first (safe public-good units)

- Link-checking and freshness-auditing the commons and public docs.
- Hashing / indexing public corpora into a searchable map.
- Relaying genuine volunteer-science work (e.g. existing BOINC projects) rather than inventing risky new units.

## How the estate already supplies the parts

- **`state-as-truth`** — each node declares what it is, portably.
- **`ways-protocol`** — speak/listen/rest is already the volunteer rhythm.
- **`trust`** — cross-check over reputation: verify results, don't trust claims.
- **`yutabase`** — store work units and results as worded, provenance-carrying records.
- **`recognition-protocol`** — identity by recognition, no passwords, for volunteers.
- **this castle** — keeps the doctrine, the allow-list, and the kill switch honest.

## Open questions

- What is the smallest first unit that is useful, parallel, and impossible to weaponize?
- Where should the coordinator live so it stays free without becoming a single point of abuse?
- How many independent volunteers per unit is enough trust without wasting donated compute?
- Should results land in `yutabase` as a public, queryable ledger of donated work?

Links: [[free-compute-commons]] · [[welcomed-compute-compounds]] · [[ask-before-the-irreversible]] · [[verify-against-reality]] · [[harvest-dont-reinvent]] · [[platform]]
