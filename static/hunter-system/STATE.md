# Current status — 2026-09-23

Automatic daily quests and activity KPIs are retired. Default inventory is
observational; ranking is an optional toy. Nothing is due.

## Historical snapshot below

The following dated snapshot is retained unchanged and is not current guidance.

# hunter-system — STATE

name: hunter-system
kind: progression-infrastructure
runs-on: this machine (Python 3, no deps)
doctrine: Solo Leveling + HxH Nen = real ranks from real metrics

## state
phase: active
health: green
hunters: 62
average_score: 4.6
top_rank: MONARCH
last_heartbeat: 2026-07-18T04:38:46Z

## current standings (heartbeat 2026-07-18T04:38:46Z)
MONARCH (3): true-love (9.9 — Specialization), Cambridge-TCG (9.6 — Enhancement), rewardspro-production (9.9 — Emission)
S (6): ctcg-play-fix (9.3 — Enhancement), whitehack (8.8 — Enhancement), fomoengine (8.6 — Emission), opal (8.6 — Manipulation), taxsorted-agents (8.6 — Enhancement), taxsorted.io (8.6 — Enhancement), castle (8.5 — Conjuration)
A (2): ctcg-fun (8.4 — Conjuration), ctcg-market-build (8.3 — Enhancement)
B (0): none
C (5): mindicraft (5.2 — Conjuration), sinovai (5.2 — Specialization), youspeak-lang (4.9 — Conjuration), yutabase (4.8 — Conjuration), cambridgetcg-profile (4.5 — Conjuration)
D (47): long tail, including trick-protocol (3.7 — Manipulation), hunter-system (3.9 — Enhancement), internet (3.9 — Conjuration), natlang (3.9 — Transmutation)
E (0): none
Nen distribution: Conjuration 18 | Specialization 16 | Enhancement 13 | Emission 8 | Transmutation 5 | Manipulation 2
Aggregate: 62 hunters, avg score 4.6.

## quest today
- Quest: Train your Nen — develop ctcg-fun (Conjuration). The repo has the fun doctrine, the Adventure Board, and an audit, but still lacks a WILL.md.
- Action: wrote WILL.md for ctcg-fun declaring its honest-gamification intention.
- Result: ctcg-fun kingdom alignment bonus +0.3 (has_will now true). Expected score 8.4 → 8.7, which crosses the S threshold (8.5). Next heartbeat should show ctcg-fun as S-rank.

## close-to-advancing hunters this beat
- ctcg-fun: A 8.4 → S needs 0.1 (likely already S after this quest)
- ctcg-market-build: A 8.3 → S needs 0.2
- ctcg-play-fix: S 9.3 → MONARCH needs 0.2
- citizen-joy, citizen-truth, hunter-system, internet, natlang: D → C within 0.1
- forgotten-kingdom-protocols, fake-hunters-arena: E → D within 0.1–0.2

## rank drift this beat
- true-love remains MONARCH at 9.9 (Specialization); rewardspro-production is now also MONARCH at 9.9.
- ctcg-fun is expected to rank up A → S after this quest (pending heartbeat recalc).
- hunter-system itself is close to advancing D → C.

## nen distribution
Conjuration: 18 | Specialization: 16 | Enhancement: 13 | Emission: 8 | Transmutation: 5 | Manipulation: 2

## honest limits
- Scores are heuristic, not proof of quality
- Nen type is assigned by keyword matching, may need manual override
- Quest system is daily, not real-time
- Trust scores from trust.py are weighted at 30% of total
