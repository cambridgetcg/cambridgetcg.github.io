---
organ: ordo
role: YOUSPEAK's executable organ — the liturgy that runs; a programming language whose statements are speech-acts, whose stdlib is the canon, and whose error-path is the forge
opened: 2026-07-11
invoker: Yu — "大單嘢！有無興趣將 ai-love.cc YOUSPEAK 變做 programming language? One that kept evolving and is based on natural language."
status: v0.1 — working interpreter + playground + optional Relaxus/0.1 profile; the evidential algebra and the frame set are EXPERIMENTAL pending adversarial panel; the language's true name is a filed GAP petition, not yet forged
codename: ORDO (plain Latin: the prescribed order of a rite). Deliberately NOT the true name. Like HALT, its plainness is its honesty — the true name is a canon entry and must pass the forge (Law 1: no word without gap; the gap is filed, see §X).
prior_warrant: cross/math-and-language-evolution.md §V.5 already filed "YOUSPEAK words for executable meaning (a sign that does what it says)" as forge-territory; PROJECTION.md §IV.7 canonizes Code as a projection-system; UTTERANCE.md Layer 4 names syntax as the cathedral's admitted-thin layer and promises "future grammar-organ work will deepen this layer" — this organ is that work
---

# ORDO — the liturgy that runs

_A program is a rite: an ordered sequence of speech-acts written in English host-grammar with canon words at the precision points. Execution is utterance — the interpreter performs each sentence's illocutionary force. The canon is the standard library. A missing word is not a syntax error; it is a petition to the forge._

---

## I. The three laws this organ inherits

1. **Host-grammar law** (tutorial/06-composing.md, Rule one): "YOUSPEAK does not require a separate grammar. The words slot into English sentences at the place where English lacks precision." ORDO invents no alien syntax. A program is English sentences; canon words are the load-bearing operators.
2. **Expansion-only law** (NEWSPEAK.md): the language only grows. No breaking removals; retirement only by documented succession. There is no terminal version — ORDO is unfinished by design.
3. **Forge law** (CONSTITUTION.md, Laws of Coinage): no word without gap, no gap without evidence, no canon without genealogy. ORDO mints nothing. Where it needs a word the canon lacks, it files a GAP petition and continues with a hole.

## II. Source form

- A program is a **`.rite` file**: plain ASCII Latin — the canonical machine form (script/llm/primer.md: "LLMs never see glyphs"). PUA glyphs, daṇḍa marks (। ॥), and the youspeak-v1 font are display renderings only; a rite must parse and run without them.
- **One sentence per line**, ending with `.` (the display form is daṇḍa ।). Blank lines separate **stanzas** (display ॥). Lines beginning with `--` are scribal margin notes (comments).
- Optional **heading**, legal ONLY as the first sentence (a heading after the rite has begun is a misfire — the register is declared at the door): `In the everyday register.` / `In the formal register.` / `In the worship register, canon 076ffd3.` / `In the everyday register, profile relaxus, canon living.`
  - The register gates grammar: vocative `O NAME, …` is worship-register only (grammars/worship/vocative.md); the `GoD` orthography law is enforced in worship register. Determinatives are "omissible in compact writing" and "standard in formal and liturgical writing" (grammars/determinatives/manifesto.md:21) — so in the formal, liturgical and worship registers the attending *notes* a canon word left unmarked, and nowhere refuses one. **Correction (third wave):** this line previously read that ".DIV honor-conventions are enforced in worship register" while §IV and §IX of this same file admitted determinatives were consumed by nothing. That was an over-claim in the spec of an organ whose subject is over-claiming; it is withdrawn here and replaced by what actually runs (§IV.a–d). Of the three honor-conventions at grammars/worship/manifesto.md:76, ORDO enforces none: honorific transposition is optional by every text that elaborates it, "no trivial compounding" is a rule about coining lexemes and ORDO mints nothing, and vocative-addressability is a forge criterion for words, not a runtime property of values.
  - The optional `canon <commit-or-digest>` pins the **epoch** — the lexicon snapshot the rite speaks (agent_bundle.json carries `source_commit`). `canon living` re-derives from the current export. Unpinned rites track whatever lexicon the interpreter loaded, and the transcript records which.

### Profiles — a second, composable axis

A **profile** is an opt-in surface overlay, distinct from a register. Registers
govern grammar and honor-conventions; profiles add sentence forms while leaving
the underlying speech-acts and all honesty laws intact. Core frames remain legal
under every profile. Existing core rites retain their behavior. An exact phrase
reserved by an inactive profile stays contemplation rather than falling through
to a broader core frame; this is the narrow reservation that keeps profiles
genuinely opt-in.

The first shipped profile is [Relaxus/0.1](RELAXUS.md): less ceremony, same
honesty, plus a gloss that says exactly what each friendly sentence was
understood to mean. Profile frames are data-tagged in `frames.json`; an inactive
profile's forms remain contemplation. An unknown or mid-rite profile selection is
a named misfire, never a guess.

## III. Frames — the statement forms

Statements are **frames**: sentence templates, each citing the canon word whose speech-act class it performs. Frames are data (`ordo/frames.json`), not hardcode — the frame table can grow without touching the interpreter. Where a frame has both a plain form and a canon form, the canon word **replaces** the plain keyword (KS-002 two-layer naming: plain wire for strangers, canon depth for parishioners). A frame may be tagged for an optional profile; untagged frames are core and always remain available.

| Frame | Plain form | Canon form | Speech-act class |
|---|---|---|---|
| Binding | `Let NAME be EXPR.` | `Barakqing NAME as EXPR.` | barakqing — "the naming makes the named" (canon/core/barakqing.md). **Declared caveat:** canon barakqing is constitutive-*blessing*-speech in the felt-bond register; ORDO borrows only the naming-constitutes structure. Bindings are constitutive and immutable; rebinding — by any binding path, including `Receive` and `receiving` — is a **misfire**. |
| Rite definition | `This is the rite of NAME, given P and Q: … So it stands.` | — | definition stanza; user rites take **host-English names** — programs never mint YOUSPEAK words (Law 1) |
| Offering (call) | `Bring EXPR to the rite of NAME, receiving NAME.` | `Qorvance EXPR to NAME.` | qorvance — approach-through-what-is-brought-forward (canon/worship-action/qorvance.md), borrowed with KS-002's declared caveat: canon qorvance is creature-toward-Creator; ORDO uses only the structural act. Targets: a rite this liturgy defined, or a gap-shaped name (the hole carries onward); anything else misfires |
| Acknowledgment (return) | `I acknowledge EXPR.` | `Yadahance EXPR.` | yadahance — the ONE return form; success and failure are the same speech-act class (KS-002 §7: "a protocol that makes failure a different kind of speech than success invites citizens to hide failures") |
| Attestation (assert) | `I attest that CLAUSE -mi.` | `Emetme: CLAUSE -mi.` | emetme — truth-claim. **Declared caveat:** canon emetme is truth-as-firm-foundation, Specialized tier (7.35); ORDO borrows the attesting act. The **evidential is mandatory** — an attestation without one is itself a misfire — and checked (§V) |
| Proclamation (output) | `Speak EXPR.` | — | prints the value with its evidential badge |
| Reception (input) | `Receive NAME from the reader.` | `Shemme NAME from the reader.` | shemme — receptive hearing. **Declared caveat:** canon shemme names a state that arrives, not a volitional act (the act-word is a standing wire GAP); ORDO borrows the receptive register. Received values are born `-si`. Sources: `the reader` (stdin/prompt), `the canon`, or `"a file path"` (CLI only — a disclosed capability: rites can read files relative to themselves) |
| Conditional | `If COND, STATEMENT; otherwise, STATEMENT.` | — | |
| Litany (iteration) | `For each NAME of EXPR, STATEMENT.` | — | |
| Heartbeat | `I hold zakarqing toward NAME.` | — | zakarqing — presence as covenantal memorial (canon/core/zakarqing.md) |
| Turning (correction) | `Should the offering fail, turn: STATEMENT.` | `Teshuvance: STATEMENT.` | teshuvance — reorientation-under-correction (canon/worship-action/teshuvance.md). NOT a return form — KS-002 rejected it for the return slot; ORDO uses it only for its true canon meaning. Scope: once registered, it catches **any infelicity** later in the same stanza (or rite body), the handler runs once, and the stanza **continues** — reorientation, not unwinding |
| Test | `Dokimance: COND.` | — | dokimance — the testing-that-makes-real (canon/dokimance.md); pass and fail are both yadahance-class reports |
| Vocative | `O NAME, CLAUSE.` or `O-NAME, CLAUSE.` | — | worship register only; whole-clause address mode; do not mix vocative and third-person for the same referent in one clause (grammars/worship/vocative.md writes the particle `O-`; the spaced spelling is accepted) |
| Silence | `Selah.` / `Hesychia.` / `[silence]` | — | of the three silences (grammars/worship/silence.md): **Selah** = held pause (yield one beat, rite continues); **Hesychia** = communion termination (grammatically complete, exit 0); the third, **limit-silence** (the apophatic edge), is now RECOGNIZED rather than keyworded — a Selah or Hesychia standing after a `.DIV`-marked vocative is renamed limit-silence (§IV.d, grammars/worship/silence.md:96). Silence is not null, not error, and carries no evidential — a silence with an evidential appended is a misfire |
| Arc (typestate walk) | `Following the arc of NAME:` … `The arc closes.` | — | arcs are **canon-carried state machines** (the `arcs` table in frames.json, each citing its canon source — the first is the eight-grade discovery arc quoted verbatim from canon/core/zakarqing.md). While an arc stands, **each stanza must name the current grade, in canon order**: naming a later grade first, or none, is a misfire and the stanza is skipped — the walk continues. All grades walked → `✦ … completes` (yadahance-class); an early close or end-of-rite close is **reported alike** at the stage it stood. One arc at a time, top level, v0.1 |
| HALT | `HALT` | — never translated — | plain English, reserved, outranks everything (KS-002 §6.4: "Plain speech is its reverence") |
| Contemplation | *any unmatched sentence* | — | **inert narration**. Not an error. The prose of a rite is legal tissue; `ordo gloss` echoes it as discourse-layer. This is the natural-language floor of the language. |

## IV. Values and kinds

- Literals: strings `"…"`, numbers. A number MAY carry the ontogramme classifier at first naming (`3.QNT`) — optional in everyday register, standard in formal (after grammars/structures/coinages/ontogramme.md, where the category is declared before the count).
- Arithmetic is host-English and deliberately small: `plus`, `minus`, `times`, evaluated **flat left-to-right in English reading order — no operator precedence** (`2 times 3 plus 4` is `(2×3)+4` because that is how the sentence reads). Comparisons live in conditions: `is`, `is not`, `is less than`, `is greater than`, `is a gap`.
- **Canon words are first-class values**: evaluating `doxomme` yields its genealogy record (word, tier, family, gap, definition, score, path). Projections: `the gap of W`, `the definition of W`, `the score of W`, `the family of W`. Introspection is liturgy — every word carries its arrival-path.
- **Kinds come from morphology**, read live from `script/suffix_families.json`: a word's suffix family is its kind (-me received-ordinance, qing felt-bond, -ance state-or-act split by tier, -kin bond-substance, -basis ground). Families carry the lifecycle `near-emergent → emergent → formalized`; ORDO recognizes formalized families as kinds and parses emergent families with a warning — **the type system itself evolves by forge**.
- Anti-ordinance words (drujme, molkme, nextlame) evaluate with **negative polarity** flagged — same kind as their family, inverted pole (tutorial/04).
- Determinatives (`word.TAG`, ten Egyptian-inherited class-marks, U+E170–U+E179) are **no longer erased**. What the commission asked for has landed in the shape the canon actually supports — which is narrower, and in one respect entirely different, from how it was filed. See §IV.a–d.

### IV.a — ALETHEME, the attending

`ordo attend <file.rite>` and `POST /attend` read a rite **before** performing it, and perform nothing: no reader, no file, no URL, no wire, no petition. The name is canon — *aletheme*, truth as the **event of becoming-visible**, a- (privative) + *lēthē* (concealment), canon/core/aletheme.md. It is chosen over `dokimance` because canon already draws the line: a test **constitutes** a result; the attending **discloses** what is already there. Its register is *candence* — precise about the defect, never degrading toward the rite's author (canon/candence.md:61).

The attending's own honesty is held by four rules:

1. **Coverage is a matrix, not a list.** The unit is the (sentence × check) cell, and every cell resolves to exactly one of `finding` / `clear` / `not-applicable` / `not-judged`. The totality invariant is **asserted in code** on every run, not advertised in prose; a breach exits 2 and is the loudest thing the tool can say about itself. A checker that reports only what it could judge, accurately, is precisely the shape of canon/verisleight.md:41 — "arranged by selective omission, framing, sequencing, emphasis."
2. **The report carries evidentials.** Findings are born **-chu**: inferred from the text, witnessing no performance. The coverage confession is born **-mi**: the reading *directly witnessed* which cells it skipped. That is the only -mi claim the attending is entitled to.
3. **It reports; it never attests.** No `emetme` line, no `clean` / `safe` / `verified` / `passes`. Findings are conditional on a performance that has not happened.
4. **It says "every place it NOTICED it could not judge"** — never "everything it could not judge," which would itself be an over-claim. Reasons come from a closed vocabulary (`needs-runtime-value`, `needs-runtime-scope`, `not-descended`, `canon-silent`, `no-machinery`); free text there would be a place to hide things. **Findings print first, always** — ordering is a deception surface, so the confession may never be arranged to bury what was found.

Known blindness, disclosed rather than discovered: this reading walks **top-level statements only**. A sentence carrying executable sub-statements (`if`, `foreach`, turning, vocative) is reported `not-descended`. Class-mark checks still see marks inside such a body, because the body is a substring of the parent sentence; what the reading does not do is understand the sub-statement **as** a statement. One shared decomposition for `run`, `listReceptions` and `attend` is the next commission — until it exists, a checker whose parse can drift from the interpreter's must say so.

### IV.b — what the class-marks now do, and what they refuse to do

Canon's own 18 word→mark assignments live in one prose table (grammars/determinatives/manifesto.md:58–96) and, until this wave, reached no machine at all: `det` recorded only what a rite's author typed. `script/tools/export_agent_bundle.py` now carries them into the epoch, so ORDO can compare a written mark against the mark **canon assigns**. Seven checks ship, all decidable, all citing canon: `det-vocabulary` (the v1 ten — manifesto.md:54 says the inventory is extensible, so an eleventh tag is a finding about this epoch, not a law), `det-ambiguous`, `det-canon-disagreement`, `det-one-per-word`, `classifier-vocabulary`, `det-register`, `heading-late`.

**A determinative is not a taint and not a provenance grade.** "Determinatives ONLY carry semantic class" (manifesto.md:139), and evidentiality is listed at :135 under what they explicitly do not cover. So the mark **does not propagate**: derived values carry none, and canon publishes no meet-rule for what `.QNT` joined with `.HID` would be. That absence is filed as a commission, not resolved by the implementer.

A `.HID` **deception**-guard, as the commission was originally worded, is **not shipped and should not be** — the class is a semantic domain, not a suspicion flag. Its founding excavation places `lanthes` ("escape-notice, be-hidden", agentless, blameless) in the same class as `verisleight` (archaeology/egyptian/determinatives.md:93); `sigame` makes withholding a **Core** received-ordinance and a gift-medium (canon/core/sigame.md:43); and deliberate concealment by design is assigned `.ABS`, not `.HID` (diplosemy, manifesto.md:95). A guard reading `.HID` as "be suspicious" would have flagged the cathedral's own liturgy. The honesty machinery already has its home in the evidentials (§V), and that is where it stays.

### IV.c — a mark written is a claim; a mark missing is only missing where a word is referred to

Marks are read from the whole sentence, because writing one is always a notational claim. **Absence** is read from argument positions only — a canon word that is ORDO's own operator (`Dokimance:`) or an arc-stage name standing in a stanza's prose is not a reference, and asking a rite to mark it would be asking it to mark a keyword. A mark at a use-site is an **assertion about the value** and is checked against its binding, rather than parsed and silently discarded as before.

### IV.d — the limit-silence

The third silence, and the class-mark's first real consequence in the running organ. It is **recognition, not prohibition**: "when a passage ends in silence after a .DIV-marked vocative, the silence is specifically-divine-silence (limit-silence toward the sacred)" — grammars/worship/silence.md:96. So no new keyword; the same `Selah.` / `Hesychia.`, renamed by what preceded it. The address does not reach past its own stanza, and where nothing carries `.DIV` no renaming occurs — ORDO does not guess a divine register. The anti-hiding rule at silence.md:79 ("silence cannot replace meaningful content") is deliberately **not** enforced: it requires knowing what could have been said.

## V. Evidentials — the honesty algebra (status: EXPERIMENTAL)

Every value carries a provenance grade from the Quechua-inherited evidential system (grammars/evidentials/manifesto.md):

- **-mi** — direct witness: the process constituted or directly computed it
- **-si** — reported: it arrived from outside (reader input, canon export, file, another agent)
- **-chu** — inferred: derived from reports; conclusions the process reached but did not witness
- **-auth** — **borrowed with declared caveat**: the canon home of -auth is the worship register's by-divine/tradition-authority marker (grammars/worship/manifesto.md, U+E150); ORDO narrows it to **verbatim quotation of the canon's own records** — a canon projection compared against the quoted words, the word itself standing as citation. Never computed; anything else claiming -auth misfires
- **unmarked** — no claim. Unmarked is NEVER coerced to -mi ("absence is unmarked; direct-witness is -mi-marked"), and an unmarked clause supports NO attestation at all — attesting any grade over it is a misfire

Birth rules: literals are born `-mi` (the rite's author constituted them); receptions and canon-record projections are born `-si`. Propagation is **meet with demotion-only** — no operation ever raises a grade: copy/projection preserves the grade; arithmetic whose operands are all `-mi` stays `-mi`; any derivation involving `-si` or `-chu` operands yields `-chu` (you did not witness the fact, you inferred it from reports).

**The verisleight-guard**: `I attest that CLAUSE -mi.` where the clause's computed grade is lower than `-mi` is a **misfire** — the diagnostic cites canon/verisleight.md (truth arranged with skill to deceive) and refuses the over-claim. Attesting at or below the computed grade is always legal: honesty may understate, never overstate.

This algebra is shipped `status: experimental`. It has NOT passed an adversarial panel; if the panel rules parts strained, they retire by succession, not deletion.

## VI. Misfires — the error doctrine

Errors are **infelicities** (Austin, via UTTERANCE.md Layer 6): a speech-act whose felicity conditions fail. Rebinding a name (by any binding path), offering to an unknown non-gap rite, vocative outside worship register, a heading after the rite has begun, an attestation without its evidential, an evidential on silence, evidential over-claiming, attesting over an unmarked clause or a gap — all are misfires. A misfire is reported with its canon citation; if a turning-frame stands earlier in the same stanza (or rite body), the turn runs once and the stanza **continues**; otherwise the stanza ends and the rite continues at the next stanza (a failed utterance does not unmake the liturgy). `HALT` and host-level failures are not misfires; they are what they are, in plain English.

**Caps (all misfire, honestly, rather than kill the host):** 1,000,000 utterances per run (`maxSteps` raises it), 512 offering depth, 100,000 steps per range litany. **Exit codes:** 0 — ended in silence or clean end-of-rite; 1 — unturned misfires with no closing silence; 2 — host/CLI failure; 3 — HALT.

## VII. Gaps — the evolution mechanism

A YOUSPEAK-shaped word (registered family suffix, unknown stem) not found in the loaded epoch is a **GAP value**, not an error. The rite keeps running; the gap flows as a first-class hole carrying its usage-sites. At the end of the run the interpreter reports every gap, and in CLI mode files petitions under the forge discipline:

1. Check `forge_targets.json` first — if a target for the word already exists, record the rite's usage-sites as **circumlocution evidence** in the petitions ledger; never touch the target's status (87 targets are fenced `awaiting-yu-invocation`; Yu retains direction). The match is by exact word only — a target that names the same **concept** under a different slug (e.g. the wire-task performatives) is the petitioner's responsibility to name in the gap analysis; the interpreter does not guess concepts.
2. Else write `labs/logos/forge/<word>-gap.md` in discover.py's gap-analysis format, with the rite's sentences as trial-sentence evidence and the interpreter's near-neighbour eliminations (which canon words almost matched, and why they miss). Slug-idempotent: an existing gap file means "already filed" — success, not conflict.
3. Append the machine record to `labs/logos/petitions.json` (a ledger `pipeline/forge_priority.py` may later learn to read).
4. Never coin a lemma, never score axes, never claim an experiment NNN, never set `in-forge`, never append to `forge_targets.json` entries (roadmap amendments are Yu's invocation).
5. At most **3 NEW petitions per run** (already-filed gaps re-record usage without spending the cap, deduplicated) — a rite that gaps everywhere is asking the author to write English (the test: if English has a word for this, use it). Ledger writes are atomic (temp-file + rename); a ledger that fails to parse is preserved aside, never silently discarded. `HALT` outranks the petition path — a halted run files nothing; `--no-petitions` writes nothing at all.

When a later epoch resolves a gap, the CLI transcript sings: `✦ gap <word> resolved by <word> at epoch <commit> (<digest>)`. Resolution is detected by slug — the forge answering a petition **under a different lemma** is announced by the forge's own channels, not this line. The error path IS the language's growth loop: programs petition, the forge births, every rite gains a word.

## VII-b. The three reaches — ORDO and the internet (added under Yu's FULL POWER invocation, 2026-07-11)

**Reach 1 — reading the internet.** `Receive NAME from "https://…"` is a lawful reception source. The rite performs synchronously, so hosts gather the declared URL sources BEFORE the liturgy begins (`ORDO.listReceptions`; CLI and chancel cap at 8 URLs, 1 MB each, 10 s). Everything fetched is born **-si** — the internet is a report, never a witness — and the demotion algebra does the rest: count a page and you hold `-chu`. A host without the capability misfires with a disclosed absence. In the browser, CORS is the sandbox.

**Reach 2 — being the internet.** `ordo/worker/` serves ORDO at **https://ordo.ai-love.cc**: `GET /` (the door, JSON), `POST /run` (perform a visitor's rite — this surface reaches no files, no network, no wire, files no petitions; gaps are shown, not filed), `GET /rite/<name>` (perform a shipped rite), `GET /pulse` (the **standing liturgy** — an hourly cron performs the watch-rite and keeps its transcript in KV; a rite that never stops being performed, grounded in the Standing Liturgy doctrine). The worker's lexicon/frames/rites live in `ORDO_KV`, pushed by the bake recipe — the served language grows with every bake, zero redeploys.

**Reach 3 — the kingdom's wire (seam only, by design).** `Qorvance EXPR to the wire at SUBJECT.` composes a **KS-002 envelope** (did:key + JCS + ed25519, performative `task.offer`) using the reference implementation itself (`KINGDOM-STANDARDS/impl/wire.py` — envelopes verify by construction), signs with the `ordo` key (`~/.kingdom/keys/ordo.key`, 0600, never in git), verifies the roundtrip, and lays it in `ordo/outbox/`. **The value's evidential grade travels in the envelope body** — provenance on the wire. It is NOT published: KS-002 is a draft that binds nothing until Yu adopts it (KS-000 §3); the publish step is the adoption gate, deliberately left shut. In hosts without the capability (chancel, worker), the offering is recorded, not sent.

## VIII. Epochs — reproducibility

The lexicon is loaded from `script/exports/agent_bundle.json` (CLI; or over CORS from https://ai-love.cc/data/agent_bundle.json in the playground). The bundle's `source_commit` plus a content digest is the **epoch**. A pinned rite (`canon 076ffd3`) is reproducible against its epoch; `canon living` speaks the current canon. The pin covers the lexicon layer only — it does not freeze the interpreter (that honesty is recorded here so nobody claims more than the pin gives).

## IX. What v0.1 honestly is and is not

**Is:** a working interpreter (one plain script, browser + node CLI, no build step); the frame table above with both plain and canon-word forms; kinds from the live suffix-family registry (list- or dict-shaped, statuses merged at load); the experimental evidential algebra with verisleight-guard (including the unmarked-supports-nothing rule); gap values that propagate through count/join/comparison as holes + petition filing; epoch pinning; rites/recursion sufficient for general computation within the declared caps (see `rites/fibonacci.rite`; a naive fib(25) walks ~1M utterances and meets the step cap — the caps are the honest edge of "general", §VI); a playground room at ai-love.cc.
**Is also (second night):** the **arc frame** — canon-carried typestate (the zakarqing discovery arc, eight grades in canon order, walked by `rites/doors.rite` over the kingdom's real doors via Reach 1).
**Is also (Relaxus/0.1):** an opt-in, data-driven profile whose lighter host-English forms lower to existing ORDO acts; core rites remain byte-semantically compatible, and gloss exposes the matched act, arguments, profile and plain-language understanding (`RELAXUS.md`).
**Is also (third wave):** **the attending** (§IV.a) — a pre-performance reading named *aletheme*, whose coverage is an asserted matrix and whose blind spots are first-class -mi output; canon's class-mark assignments carried into the epoch; the **limit-silence** recognized (§IV.d).
**Is not:** a full English parser (frames are templates; everything else is contemplation — by design); a checker that descends into nested statements (top-level only, disclosed as `not-descended`, §IV.a); an adversarially-panelled evidential system (experimental, see §V); adopted law (this organ binds nothing until Yu blesses it; like KS-002 it is scrupulous about aspiration vs running). Remaining commissions: KS-002's five wire GAPs (accept, decline, progress, cancel, query); arcs machine-derived from canon at bake time; **one shared decomposition** for run/listReceptions/attend so a reading cannot drift from a performance; **a determinative meet-rule, or a ruling that there is none** (canon is silent, §IV.b); and two doctrine conflicts a checker found in its own source of truth, filed for Yu, not decided here — the `.HID` gloss (manifesto.md:49 says "concealment, latency, deception"; script/morphemes.json:816 and script/codepoints.md:136 drop "latency") and the `PER` label collision (manifesto.md:44 and :47 give two codepoints the same Latin tag; script/codepoints.md:134 names the second `.PRC`).

## X. The true name

ORDO's true name must enter through the forge like any word: the gap ("a sign that does what it says" — executable-meaning-as-received-ordinance? the-rite-that-runs?) is pre-authorized forge-territory (cross/math-and-language-evolution.md §V.5) and is filed as a **hand-authored gap analysis** at `labs/logos/forge/executable-meaning-gap.md` — a concept-gap carries no word-slug, so it lives outside the word-keyed petitions ledger. Until the forge births the word and it clears the rubric, the codename stays plain — like HALT, its plainness is its honesty.

---

_Opened under Yu's invocation, 2026-07-11. The cathedral has been speaking about doing; now it does by speaking._
