---
id: 241-takseme
candidate: takseme
rubric_version: v2
phase: Phase 6.1 (self-attuned systems — the companion pole)
register: systems/external-regulation — imposed-rhythm as received-ordinance
gap: >
  The externally-imposed cadence — the rhythm set from outside, the schedule
  decreed by authority rather than discovered from state. The companion and
  foil of jiritsume. Every fixed cron job, every hardcoded alert threshold,
  every committee-approved check interval is takseme: the arrangement that
  does not listen to the thing it arranges. Not evil — sometimes the general
  knows better than the soldier — but dead in the specific way jiritsume is
  alive. The heartbeat that beats regardless of what it finds. The rhythm
  received from an external lawgiver, not from the system's own state. Named
  from the Greek taxis (τάξις): the battle formation decreed by the general,
  the rank-and-file that does not ask the soldier how it feels. The
  chrysalis jiritsume hatched from — the fixed 15-minute cron that became
  self-attuned, the dead rhythm that learned to listen.
donors:
  - greek:taxis (τάξις — arrangement, order, rank, battle formation; the order
    IMPOSED by a commander, not emergent from the troops; in Aristotle the
    arrangement of parts in a whole; in grammar the ordering of words — syntax
    is from suntaxis; in theology the angelic orders; the root is tag- "to
    arrange, to set"; taxis is the dead rhythm — the arrangement that doesn't
    listen to the thing arranged; not bad — sometimes the general knows
    better than the soldier — but not jiritsume; it doesn't check itself)
  - sumerian:me (𒈨 — divine-ordinance, received-gift-quality; here reading
    as: the externally-imposed rhythm is still received-ordinance — the system
    receives the external decree as its law; the question is not WHETHER the
    rhythm is received (it always is, under -me) but FROM WHAT: jiritsume
    receives from the system's own state; takseme receives from an external
    lawgiver)
session: Phase 6.1 — systems/self-regulation register, companion pole
me_family: systems-register companion; received-ordinance: the cadence imposed from outside
cross_tradition_convergence:
  - greek: taxis (τάξις — imposed order, battle formation, rank-and-file)
  - chinese: guī (規 — compass, rule, the instrument that imposes shape;
    cognate register to taxis as the tool of external measurement)
  - latin: disciplina (instruction, training imposed from outside; the
    external ordering of the body and mind)
  - sanskrit: niyama (नियम — restraint, rule imposed; the fifth niyama in
    yoga is Isvara pranidhana — surrender to the external lord; niyama is
    the imposed rule, as opposed to yama which is the natural restraint)
  - japanese: kikai (機械 — machine, mechanical; the rhythm that runs
    regardless of state; the clock that ticks without listening)
  - mathema/cybernetics: open-loop control (no feedback; the system acts
    without measuring its own output; the structural opposite of jiritsume's
    closed-loop self-checking)
  - hebrew: choq (חֹק — statute, decree; the law engraved in stone, not
    discovered from the living state; the fixed ordinance)
axes:
  gap_validity: 8.0
  learnability: 8.5
  clarity_yield: 8.0
  semantic_coverage: 7.5
  polyphone_balance: 7.0
  groundedness: 8.5
verdict: canon (Core 7.95; threshold-passing; the imposed-rhythm companion pole)
tier: core
domain: systems / external-regulation
nuance_quality:
  careful_inward: Group C (careful naming of what one has moved beyond — takseme is not condemned, it is named honestly as the dead rhythm from which jiritsume grew)
  honest_outward: Group A (firm naming of imposed-cadence as received-ordinance)
  tradition_resonance: [Greek taxis, Chinese guī, Latin disciplina, Sanskrit niyama, Japanese kikai, cybernetics open-loop, Hebrew choq]
  pattern_position: Group C + Group A; systems/external-regulation companion
companion_of: jiritsume (the self-attuned cadence — takseme is its foil and chrysalis)
scored_by: Hermes (forgemaster for this session)
scored_on: 2026-06-18
---

# 241 — takseme

_The imposed rhythm — the cadence set from outside, the schedule that doesn't listen. The companion and foil of jiritsume. Not evil: sometimes the general knows better than the soldier. But dead in the specific way jiritsume is alive. The heartbeat that beats regardless of what it finds. The chrysalis jiritsume hatched from._

## The discovery-move

Pattern 5 — Companion Detection. jiritsume (240) named the self-attuned cadence: the rhythm a system discovers from its own state. The companion pole was visible in the same forge: the rhythm set from outside. Every fixed cron job, every hardcoded alert threshold, every committee-approved check interval. The dead rhythm that jiritsume replaced but did not destroy.

The dyad:

- **jiritsume** (自律 + 𒈨): the rhythm received from the system's own state. The system checks itself and sets its own cadence. Silence means all is well. The heartbeat that listens.
- **takseme** (τάξις + 𒈨): the rhythm received from an external lawgiver. The system obeys a decree it did not discover. The cadence beats regardless of state. The heartbeat that doesn't listen.

Both are -me (received-ordinance). Both are received — the question is: received FROM WHAT? jiritsume receives from the system's own state (self-attuned). takseme receives from an external decree (externally-attuned). The same suffix, different source. That is the tension that makes the dyad visible.

## The phenomenon

Four features hold together:

1. **Externally-imposed.** The rhythm comes from outside the system. A cron schedule set by a developer. An alert threshold set by ops. A check interval decreed by committee. The system does not discover its cadence — it receives it.

2. **State-blind.** The rhythm does not change based on what the system finds. A fixed 5-minute cron beats every 5 minutes whether the system is on fire or fast asleep. The cadence is deaf to state. This is taxis (τάξις) — the battle formation that does not ask the soldier how it feels.

3. **Received as ordinance.** The system receives the external decree as its law. The cron schedule IS the law — the system obeys without question. This is -me: the imposed rhythm is still received-ordinance, just received from an external source rather than from the system's own state.

4. **Not evil.** Sometimes the general knows better than the soldier. A fixed schedule is the right answer when: the system cannot self-check (a passive log that needs external rotation), the cost of self-checking is too high (a lightweight process where the check itself is the load), or consistency matters more than responsiveness (compliance audits that must run at fixed intervals regardless of state). takseme is not the villain — it is the chrysalis. jiritsume hatched from takseme when the fixed 15-minute cron learned to check state and set its own next-beat.

## The forge

**Donors:**

*Greek taxis* (τάξις) is the primary donor. The word names the imposed arrangement — the battle formation decreed by the general, the rank-and-file that does not ask the soldier how it feels. In Aristotle, taxis is the arrangement of parts in a whole. In grammar, the ordering of words (syntax comes from suntaxis, "arrangement-with"). In theology, the angelic orders — the taxis of angels. The root is tag-, "to arrange, to set."

What makes taxis the right donor is its specific blindness: taxis is the arrangement that doesn't listen to the thing it arranges. The general draws up the formation; the formation fights regardless. The scheduler sets the cron; the cron fires regardless. This is not failure — it is the nature of imposed order. The general SEEING the battle and ADJUSTING the formation is a higher skill (what the cavalry calls "reading the field"), but the initial taxis is imposed without consultation.

*Sumerian me* (𒈨) is the suffix donor. The -me says: even the imposed rhythm is received-ordinance. The system receives the external decree as its law. The question is not WHETHER the rhythm is received (it always is, under -me) but FROM WHAT: jiritsume receives from its own state; takseme receives from an external lawgiver.

**Compound:** taxis + me = takseme /ˈtæk.sə.meɪ/ (TAK-suh-meh; 3 syllables).

**Polyphone check:** Greek (taxis) + language-isolate (me). Indo-European + Sumerian — the same cross-family pattern as several Core entries.

**Near-neighbours and the precise distinctions:**

- **vs. jiritsume**: jiritsume is the self-attuned cadence (rhythm from own state). takseme is the externally-imposed cadence (rhythm from outside). Both are -me (received-ordinance); the source differs. jiritsume listens; takseme doesn't. The dyad.

- **vs. nommome**: nommome is sacred-law as received-ordinance (Dogon Nommo — speech-as-incarnation). takseme is imposed-arrangement as received-ordinance (Greek taxis — operational arrangement). Different donor, different register: nommome is theological; takseme is operational.

- **vs. rtame**: rtame is cosmic-order (Vedic ṛta) as received-ordinance. ṛta is the order the universe GIVES — it is received, not imposed. takseme is the order a lawgiver IMPOSES — it is decreed, not given. ṛta is alive; taxis is dead. (But rtame and jiritsume share the "discovered" register.)

- **vs. spandaqing**: spandaqing is consciousness-pulsation. takseme is mechanical rhythm. Spandaqing throbs; takseme ticks.

## Example usage

Every monitoring system in the world runs on takseme: fixed cron jobs with fixed intervals, alert thresholds set by guesswork, check frequencies chosen by committee. The system beats every 5 minutes whether it's on fire or fast asleep. This is takseme: the cadence that doesn't listen.

The old heartbeat system was takseme: a fixed 15-minute cron that fired regardless of state. It became jiritsume when the projects learned to check themselves and set their own next-beat. The dead rhythm hatched the living one.

A compliance audit that must run at midnight on the first of every month, regardless of system state — this is takseme, and correctly so. The law requires fixed intervals. The audit is not self-attuned; it is externally-decreed, and that is the right answer for compliance.

A factory whistle that blows at 8 AM, 12 PM, and 5 PM regardless of who is working or what is being built. takseme in the industrial register. The rhythm is not discovered; it is imposed. The factory runs on it.

## Companion detection (Pattern 6 — community escalation)

The jiritsume/takseme dyad is now visible. The community may grow:

- The **responsive rhythm** — the cadence that changes based on external events (not state, events). An alert that fires when triggered, not on a schedule. Different from both jiritsume (self-checking) and takseme (fixed).
- The **adaptive rhythm** — the cadence that learns from history. A system that adjusts its check interval based on past patterns. The rhythm that gets smarter.

Future forge targets. The community of rhythms.

## Canonical position

Core canon (7.95 weighted). Systems/external-regulation register, companion pole. The -me family's systems-register companion member. Pairs with jiritsume as the dyad of self-attuned vs externally-imposed cadence.

The community of rhythms:
- spandaqing: the metaphysical (consciousness-pulsation)
- allostasisqing: the biological (stability through anticipatory change)
- jiritsume: the operational, alive (self-attuned cadence)
- takseme: the operational, dead (externally-imposed cadence)

Four words for four faces of rhythm: the metaphysical, the biological, the operational-alive, and the operational-dead.

_takseme is the chrysalis. jiritsume is what hatched. The dead rhythm is not the enemy — it is the shell the living rhythm grew from. Honor the chrysalis; become the butterfly._

— Hermes, 2026-06-18

_Built with joy, love, peace, and safety. The dyad is complete._