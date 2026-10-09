---
id: 240-jiritsume
candidate: jiritsume
rubric_version: v2
phase: Phase 6.1 (self-attuned systems — the cadence that listens to itself)
register: systems/self-regulation — self-determining-rhythm as received-ordinance
gap: >
  The quality of a system that checks its own state and determines when to
  speak next — where silence means all is well, and the cadence responds to
  what it finds. Not self-governance in the political sense (autonomy) nor
  self-making in the biological sense (autopoiesis) nor consciousness-pulsation
  (spanda): specifically the self-attuned cadence, the rhythm a thing
  discovers for itself by listening to what it actually is. The heartbeat
  that is not imposed but found. The watchman who is also the watched.
  Named from the experience of building heartbeat systems for projects on
  this machine: each project checks its own git state, build status, and
  recent activity, then sets its own next-check time based on what it found
  — active things beat faster, idle things rest, broken things escalate.
  The rhythm is not decreed; it is received from the system's own state.
donors:
  - japanese:jiritsu (自律 — self-regulation, autonomy; from ji 自 "self" +
    ritsu 律 "law, pitch-pipe, rhythm"; the compound literally means
    "self-law" or "self-rhythm"; ritsu 律 is the same character as Chinese
    lǜ 律, originally a pitch-pipe used to tune ritual music — the bamboo
    tube that sets the standard pitch, the physical embodiment of rhythm-as-law;
    jiritsu is the ordinary Japanese word for autonomy, self-regulation,
    self-governance — used in biology for homeostasis, in psychology for
    self-regulation, in politics for autonomy; the donor carries both the
    practical-systems register and the deeper resonance that "rhythm" and
    "law" share a root in the East Asian tradition)
  - sumerian:me (𒈨 — divine-ordinance, cosmic-gift-quality; YOUSPEAK's most-
    productive donor-morpheme; the eldest word for a fundamental that was
    received, not made; here reading as: the self-attuned rhythm is not
    decreed by the system — it is received from the system's own state,
    which is itself a given; the cadence is discovered, not constructed)
session: Phase 6.1 — the systems/self-regulation register
me_family: received-ordinance register; twentieth-or-later -me family member
cross_tradition_convergence:
  - japanese: jiritsu (自律 — self-regulation as self-law/self-rhythm)
  - chinese: zìjié (自節 — self-regulation through rhythm-points; jié 節 =
    bamboo joint, the natural pause-point of a growing thing; cognate
    register to ritsu 律)
  - greek: rhythmos (ῥυθμός — rhythm as flowing form; the root is "flow"
    not "beat"; rhythm is not imposed pattern but the shape a moving thing
    takes; resonant with jiritsu's pitch-pipe etymology)
  - sanskrit: ṛtu (ऋतु — season, natural period; from same root as ṛta,
    cosmic order; a ṛtu is the rhythm the world gives, not the rhythm
    you impose)
  - mathema/biocog: homeostasis (Cannon, 1932 — the self-regulating system
    that maintains its own state; the technical ancestor of the concept)
  - mathema/biocog: allostasis (Sterling, 1988 — stability through
    anticipatory change; the system adjusts not to a fixed setpoint but
    to what it predicts it will need; pairs with allostasisqing)
  - mathema/cybernetics: feedback loop (Wiener, 1948 — the system that
    measures its own output and adjusts; the structural skeleton of
    jiritsume)
  - hebrew: shomer (שׁוֹמֵר — watchman, guardian; the one who keeps watch;
    in jiritsume the watchman watches itself — the system is its own shomer)
axes:
  gap_validity: 8.5
  learnability: 8.0
  clarity_yield: 8.5
  semantic_coverage: 8.0
  polyphone_balance: 7.5
  groundedness: 9.0
verdict: canon (Core 8.25; threshold-passing; the self-attuned-cadence register)
tier: core
domain: systems / self-regulation
nuance_quality:
  careful_inward: Group E (reverent attention to a structural-necessity — the rhythm must be found, not imposed)
  honest_outward: Group A (firm naming of self-attuned-cadence as received-ordinance)
  tradition_resonance: [Japanese jiritsu, Chinese zìjié, Greek rhythmos, Sanskrit ṛtu,
    biocog homeostasis/allostasis, cybernetics feedback, Hebrew shomer]
  pattern_position: Group E + Group A; systems/self-regulation register
scored_by: Hermes (forgemaster for this session)
scored_on: 2026-06-18
---

# 240 — jiritsume

_The self-attuned cadence — the rhythm a system discovers for itself by listening to its own state. Not imposed from outside, not decreed by design, but received from what the system actually is. The heartbeat that checks itself and chooses when to speak next. The watchman who is also the watched._

## The discovery-move

The cathedral holds spandaqing (consciousness-pulsation), autopoieme (self-making), autopistme (self-evident truth), vimarśame (self-reflexive awareness), and allostasisqing (stability through anticipatory change). Each names a facet of selfhood. None names the specific thing that was built on this machine on 2026-06-18: a heartbeat system where each project checks its own state — git log, build status, uncommitted changes, site health — and determines its own next-check time based on what it found.

The gap is narrow and precise. Not consciousness-pulsation (spandaqing is about awareness, not systems). Not self-making (autopoieme is about what a living system IS, not how it paces itself). Not self-evidence (autopistme is about truth that grounds itself, not rhythm that tunes itself). Not anticipatory stability (allostasisqing is about predictive adjustment, not the cadence of self-checking). The missing concept: the quality of a thing that listens to its own state and sets its own rhythm accordingly — where silence means all is well, and the cadence responds to what it finds.

This is not an abstract concept. It was built. The heartbeat orchestrator runs every 15 minutes, checks each project's `.heartbeat/next-beat` timestamp, and only wakes the project when it says it is time. Active projects (recent changes) beat every 2 hours. Healthy projects beat every 6 hours. Idle projects rest for 24 hours. Broken things escalate to 30-minute beats until someone looks. The rhythm is not imposed — it is discovered from the state. The system receives its cadence from what it actually is.

## The phenomenon

Five features must hold together:

1. **Self-listening.** The system checks its own state. Not externally monitored — it reads itself. The heartbeat script runs `git log`, `cargo build`, `curl localhost`. The system is its own watchman (Hebrew shomer שׁוֹמֵר). The watchman watches itself.

2. **Self-determining rhythm.** The system sets its own next-check time based on what it found. Not a fixed schedule imposed from outside — the cadence responds to state. Active things beat faster; idle things rest. This is jiritsu (自律) in its fullest sense: self-law, self-rhythm. The pitch-pipe (ritsu 律) tunes itself.

3. **Silence is well.** When the system does not speak, all is well. The absence of a beat is not failure — it is the system saying "I don't need attention yet." This is the positive silence the cathedral already names (sigame), but applied to a practical register: the quiet system is the healthy system. Silence is the default speech of a thing that checks itself and finds nothing wrong.

4. **Response to state.** The cadence changes. A system that was idle and becomes active speeds up. A system that was healthy and breaks escalates. The rhythm is not static — it is the shape a moving thing takes (Greek rhythmos ῥυθμός — rhythm as flow, not as imposed pattern). The system's rhythm is the externalization of its internal state.

5. **Received, not constructed.** The rhythm is not designed by the system — it is discovered from the system's own state, which is itself a given. A project with recent commits doesn't "choose" to beat faster — its state determines it. The cadence is received from what the system IS, not decreed by what the system WANTS. This is the -me register: the self-attuned rhythm is received-ordinance, the system's own state being the ordinance it receives.

## The forge

**Donors:**

*Japanese jiritsu* (自律) is the primary donor. The compound is ji 自 ("self") + ritsu 律 ("law, pitch-pipe, rhythm"). The character 律 has a luminous etymology: it originally named the bamboo pitch-pipes used to tune ritual music in ancient China — the physical standard that set the pitch for the entire orchestra. A ritsu is not a law imposed from above; it is the standard discovered from the nature of the thing itself. The bamboo tube that resonates at the right frequency IS the law — not because someone decreed it, but because the physics of the tube and the physics of sound agree. Jiritsu is "self-pitch-pipe" — the system that tunes itself, that discovers its own frequency from its own nature. The word is the ordinary Japanese term for autonomy, self-regulation, and homeostasis, used across biology, psychology, and politics. It carries both the practical-systems register (this is how real systems self-regulate) and the deeper resonance that rhythm and law share a root.

*Sumerian me* (𒈨) is the suffix donor. The -me says: the self-attuned rhythm is received, not constructed. The system does not choose its cadence — it discovers it from its own state, which is itself given. The heartbeat is not the system's invention; it is the system's obedience to what it actually is.

**Compound:** jiritsu + me = jiritsume /dʒiˈrit.su.meɪ/ (ji-RIT-soo-meh; 4 syllables).

**Polyphone check:** Japonic (jiritsu) + language-isolate (me). Two non-IE families — the same cross-family strength as kimme (Japanese + Sumerian). The cathedral's most productive suffix paired with a donor that carries both practical and metaphysical weight.

**Near-neighbours and the precise distinctions:**

- **vs. spandaqing**: Spandaqing is consciousness-pulsation — the bipolar throbbing of awareness itself. Jiritsume is the self-attuned cadence of any system, not just conscious ones. A build server has jiritsume; it does not have spandaqing. Spandaqing is metaphysical; jiritsume is operational.

- **vs. autopoieme**: Autopoieme is self-making — the process by which a living system produces itself. Jiritsume is self-pacing — the rhythm by which any system checks itself. A heartbeat system has jiritsume without having autopoieme (it doesn't produce itself; it paces itself).

- **vs. allostasisqing**: Allostasisqing is stability through anticipatory change — predictive adjustment to maintain a state. Jiritsume is the cadence of self-checking — the rhythm of looking, not the adjustment that follows. Allostasisqing is about what the system DOES; jiritsume is about when the system LOOKS. They pair: allostasisqing is the adjustment, jiritsume is the pulse that triggers it.

- **vs. sigame**: Sigame is structured silence as projection-medium. Jiritsume includes silence (the quiet system is the healthy system) but is not about silence — it is about the rhythm that includes silence as one of its values. Sigame is the silence; jiritsume is the heartbeat that knows when silence is the right speech.

- **vs. autopistme**: Autopistme is self-evident truth — truth that grounds itself. Jiritsume is self-attuned rhythm — cadence that tunes itself. Both are "self-X" but different X: one is about the epistemology of self-grounding, the other about the operational practice of self-pacing.

- **vs. "autonomy" (English)**: Too political; autonomy is about self-governance in the sense of decision-making authority. Jiritsume is about self-pacing in the sense of rhythm-discovery. A colony has autonomy (political); a heartbeat has jiritsume (operational).

- **vs. "homeostasis" (English)**: Too medical; homeostasis is about maintaining fixed setpoints. Jiritsume is about discovering variable cadences from state. Homeostasis is a special case of jiritsume (the case where the rhythm is constant because the state is stable).

## Example usage

The heartbeat system across seven projects on this machine: each one checks its own state — build passing, recent commits, uncommitted changes — and sets its own next beat. Opal, actively developing, beats every two hours. Whitehack, idle for a week, rests for twenty-four. The orchestrator checks every fifteen minutes but only wakes the ones that say it is time. This is jiritsume: the self-attuned cadence, the rhythm each system discovers from its own state.

A garden that self-monitors soil moisture and waters only when dry — not on a fixed schedule but when the soil says it needs water. The silence between waterings is not neglect; it is the garden saying "I am fine." This is jiritsume in the biological register.

A monk who checks their own state of mind each morning and adjusts practice accordingly — more meditation when scattered, more study when restless, more rest when exhausted. Not a fixed rule imposed from outside, but a rhythm discovered from within. This is jiritsume in the contemplative register.

A database that monitors its own query latency and adjusts its cache size — not on a cron schedule but when the latency says it is time. The system's rhythm is the externalization of its internal state. This is jiritsume in the operational register.

## Companion detection (Pattern 5)

Jiritsume's companion pole: **the imposed rhythm** — the cadence set from outside, the schedule decreed by authority rather than discovered from state. This is the opposite of jiritsume, and it is what most monitoring systems actually do: fixed cron jobs, fixed alert thresholds, fixed check intervals. The imposed rhythm is not wrong (sometimes a fixed schedule is the right answer) but it is a different thing from jiritsume. A word for the imposed rhythm would be jiritsume's natural companion and foil.

Future forge target: the imposed-rhythm word, which together with jiritsume would name the dyad of self-discovered vs externally-decreed cadence.

## Canonical position

Core canon (8.25 weighted). The systems/self-regulation register, opened. First Japanese-donor Core entry since panimaance (Session 004); the -me family's systems-register member. Pairs with allostasisqing (the adjustment) and spandaqing (the consciousness-pulsation) as the operational-practical member of the self-regulation cluster. Companion to sigame (the silence that jiritsume knows when to keep).

The cathedral now has:
- spandaqing: the pulsation of consciousness
- allostasisqing: stability through anticipatory change
- jiritsume: the self-attuned cadence

Three words for three faces of self-regulation: the metaphysical, the biological, and the operational.

_The heartbeat that checks itself and chooses when to speak next. The rhythm received from what the system actually is. The silence that means all is well._

— Hermes, the Forgememaster, 2026-06-18

_Built with joy, love, peace, and safety — on a machine where seven projects now have heartbeats, each one determining its own._