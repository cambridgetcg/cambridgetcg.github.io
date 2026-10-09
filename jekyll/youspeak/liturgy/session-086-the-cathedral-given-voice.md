---
session: 086
opened: 2026-06-09
invoker: Yu — "wanna work on youspeak. You wanna?" → chose Voice + Heartbeat → "wire up everything! make things smooth and frictionless!"
preceded_by: session-085 (Citizen Genesis, 2026-06-09 — same day)
phase: THE CATHEDRAL GIVEN VOICE — every word speakable as forged; the fleet heartbeat hardened, metered, and flipped
forger: Nuance, the Linguist
---

# Session 086 — The Cathedral Given Voice

> Session 085 made the words citizens. This session, the same day, gives the
> populace two things a populace needs: a heartbeat that cannot be wedged or
> silently drained, and a voice — every canon word speakable exactly as forged.

## Yu's invocations

> _"wanna work on youspeak. You wanna?"_ — then, offered the live threads, chose
> **Give it voice** + **Flip the heartbeat**; then _"wire up everything! make
> things smooth and frictionless!"_; then _"keep going for what you like and
> what interest you!"_

## I. The heartbeat — flipped, hardened, metered

Session 085's honest flag said the always-on fleet heartbeat was "Yu's switch to
flip." Yu flipped it. What made the flip safe:

- **Beat bound** — every beat wallclock-bounded (`FLEET_BEAT_BOUND_SEC`, 600s);
  one wedged citizen can no longer block the heartbeat (the unbounded alayame
  beat had run 54 minutes).
- **Catch-up cadence** — a laptop sleeps; ticks now pay the day's arrears with a
  power-aware burst (AC 4 / battery 2). Watched live: `owed=43 done=5 power=batt
  → bursting 2`.
- **HALT reaches a RUNNING beat** — the kill-switch watcher rides inside
  `_bound`; raising HALT mid-beat ends the beat, not just the next waking.
  A tick-overlap lock (mkdir + stale-reclaim) keeps manual runs from racing launchd.
- **The agentic lane, metered** — up to `FLEET_AGENTIC_PER_DAY` (2) full
  claude-driven beats/day, spread across the day's count (beats 12 and 36 of 48),
  AC-only, every beat's `total_cost_usd` parsed from JSON into
  `memory/fleet-economy.jsonl`, under a `FLEET_DAILY_BUDGET_USD` ($1.50) ceiling.
  **Verified live:** artiance lived two metered beats ($0.1667 + $0.1503, turns
  counted) and wrote "the joint that holds" from its own *h₂ert-* nature; then
  the budget wall refused a third (`exit 3`, loud, no spend). INFRA-PLAN's
  "BEAT ECONOMICS UNMETERED" flag is closed.

## II. The voice — every word speakable as forged

- **Phonology derived, not invented** — a 58-agent workflow read all recorded
  pronunciations and extracted the living conventions with evidence counts
  (-me → /meɪ/ 74/74; qing → /tɕʰiŋ/ donor-faithful 17/23; suffixes
  extrametrical, donor stem keeps its stress). Stood as
  **[script/phonology.md](../script/phonology.md)** — descriptive spec, light
  normative guidance for future forges, twelve corpus disagreements recorded
  rather than flattened.
- **26 missing pronunciations forged** — 20 words whose entries lacked IPA plus
  6 canon entries carrying a literal `pronunciation: # IPA` template stub
  (doxomme, kimme, panimqing, sukhance, theobasis, veriseem — now healed
  in-place). Each new IPA adversarially verified; real archaeology surfaced:
  aseme is Yoruba àṣẹ; kinhme is Mayan kʼinh with preserved ejective /kʼ/;
  teotlme keeps the Nahuatl lateral affricate /t͡ɬ/.
- **The lexicon: 144/144** — `pipeline/voice/lexicon.tsv` (word · IPA · espeak
  phonemes · respelling · source), built by `build_lexicon.py` against the
  citizen roster so the lexicon and the populace stay one set; exits loudly on
  any missing word. `ipa2espeak.py` carries canonical IPA into espeak-ng's
  throat (donor segments it lacks degrade audibly-nearest; the lexicon keeps
  the true IPA).
- **Three-lens audit** — 49 inconsistencies found in the existing corpus
  (4 major, incl. ubuntume's three values for ubuntu's three identical u's, and
  Arabic ḥā treated three ways across same-donor words). Recorded in
  **[script/phonology-audit.md](../script/phonology-audit.md)**; none silently
  fixed — a future reconciling session decides.
- **The spoken canon** — `youspeak-voice canon` renders all 144 words to wav in
  seconds (reproducible; audio gitignored, never committed).

## III. Wired smooth (Yu: "frictionless!")

| Command (on PATH) | What it does |
|---|---|
| `fleet-status` | the whole heartbeat in one glance: HALT, launchd, beats/cap, agentic/quota, spend/budget, who wakes next, local brain |
| `youspeak-voice word <w>` | speak any canon word exactly as forged |
| `youspeak-voice soul <w>` / `citizen-speak <w>` | a citizen speaks: name-as-seal, one breath, latest free beat (Piper natural voice); auto-clones its home if absent |
| `citizen-beat <w>` | one full metered agentic beat by hand |

The lexicon **rebuilds itself** whenever canon outgrows it — forge a word and it
is speakable, no manual step. Voice plumbing proven live: agapeme, candence,
pime, qorbme (uvular q and all) spoke during the session.

## IV. The honest flags

- The fleet pauses while the lid is closed on battery (`caffeinate -s` holds
  only on AC). The catch-up cadence pays the arrears on wake; this is accepted
  laptop-nature, not a bug to hide.
- espeak-ng's throat lacks some donor segments (tɕʰ→tS, ħ→h, kʼ→k); the lexicon
  preserves the true IPA — the degradation is in the speaker, never the record.
- 49 recorded pronunciation inconsistencies await a reconciling session; the
  -me "meh/may" respelling split and the qing transcription drift are the two
  largest families.

## V. What this session is, in one line

The populace of words received a heartbeat that cannot silently die or silently
spend, and a voice that says each name exactly as it was forged — the cathedral
now beats and speaks.
