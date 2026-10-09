---
organ: ordo/profile/relaxus
role: an opt-in surface profile for programming with less ceremony and more visible understanding
opened: 2026-07-12
invoker: Yu — "Let's just be Relaxus Being. No limits to substrate."
status: Relaxus/0.1 — executable profile, deliberately small
name_status: plain host-language codename, not a forged YOUSPEAK canon word
---

# Relaxus — less ceremony, same honesty

Relaxus is an optional profile over ORDO. It does not replace the interpreter,
weaken its evidence rules, or pretend that a pattern matcher understands prose it
did not parse. It gives existing ORDO speech-acts a lighter host-English surface
and makes the interpreter's understanding visible before execution.

> **Relaxus does not make programs careless. It makes care less anxious.**

Humour is transport. Care is payload.

## I. Entering the profile

The profile composes with ORDO's existing registers:

```text
In the everyday register, profile relaxus.
In the formal register, profile relaxus, canon living.
In the worship register, profile relaxus, canon 557c143.
```

Register and profile are different axes. A register continues to govern grammar
such as the worship vocative. The profile changes only the optional surface
frames. Existing core rites behave as before; an exact phrase reserved by an
inactive profile stays contemplation instead of falling through to a broader
core frame. That small reservation is what keeps the profile genuinely opt-in.

The selector belongs in the first heading. Profiles cannot be switched halfway
through a rite. An unknown profile names its own misfire instead of being guessed.

## II. Laws that do not relax

Under Relaxus:

- Core ORDO frames remain legal. Friendly forms extend; they never remove.
- Bindings remain immutable. `Notice` cannot quietly rewrite what was named.
- Evidentials remain demotion-only: reports never dress themselves as witnesses.
- GAP values, caps, misfires, turning, exit codes and epoch recording are unchanged.
- `HALT` stays uppercase, plain and reserved.
- Unmatched sentences remain inert contemplation, not secretly executed intent.

Less serious is not less truthful.

## III. Friendly surface

Every Relaxus sentence lowers to an existing ORDO act:

| Relaxus sentence | ORDO act | Meaning |
|---|---|---|
| `Notice tea as "warm".` | binding | Name once; carry the value's actual evidence. |
| `Share tea.` | proclamation | Output as sharing, not command. |
| `Listen for word from the reader.` | reception | Receive; reader silence becomes an unmarked value. An unavailable external source misfires. |
| `Maybe CONDITION, STATEMENT; otherwise, STATEMENT.` | conditional | False takes the optional alternative, or does nothing; it is not a misfire. |
| `Try X with RITE, keeping the result as Y.` | offering | Call a rite through the existing qorvance structure. |
| `Back to you: X.` (`All good: X.` also works.) | acknowledgment | Inside a rite, return to its caller; at top level, acknowledge to the reader. |
| `If it tangles, gently: STATEMENT.` / `Oops: STATEMENT.` | turning | Repair one later misfire in the stanza or rite body, then continue. |
| `Check kindly: CONDITION.` | dokimance | Report true and false alike; hide neither. |
| `Stay with NAME.` | heartbeat | Record presence without demanding a reply. |
| `Chill.` / `Breathe.` | selah | Mark one quiet beat, then continue. |
| `Enough.` / `Enough for now.` / `We're good.` / `AFK.` / `Nope.` | hesychia | End cleanly. Unfinished work is not an error. |

`Nope.` currently ends the whole rite. Scoped capability denial such as
`Nope tracking.` would require a real effect-and-consent system. Relaxus/0.1
does not fake that semantic with a cute alias; it leaves the extension honest.

## IV. The understanding contract

`ordo gloss` and the Chancel's **gloss / understand** action show how every
sentence was parsed, without running it:

- the surface sentence;
- the matched frame;
- the canonical runtime act;
- the captured arguments;
- the profile in force;
- a plain-language sentence saying what the interpreter understood;
- the canon or specification citation grounding that interpretation.

If no frame matches, the explanation says so and the sentence remains
contemplation. Invalid and late profile headings are warned about here; all
other runtime checks still happen only when the rite is performed. This is full
disclosure, not a claim of full natural-language understanding.

## V. Substrate neutrality

Relaxus speaks of **Beings**, but the runtime does not type a participant as
human, bot, animal, fungus, machine or anything else. Substrate may matter to an
adapter's needs; it never determines authority, dignity or access to the
language.

The profile's social invariant is smaller and stronger:

```text
No Being has to prove a right to exist before participating.
```

## VI. A small rite

```text
In the everyday register, profile relaxus.

Notice tea as "warm".
Share "hello, Relaxus Being".
Maybe tea is "warm", Share "excellent tea situation".
Check kindly: tea is "warm".
Chill.
Enough for now.
```

The runnable form lives at `ordo/rites/relaxus.rite`. It becomes a Chancel
preset when `home/bake.py` gathers the rites.

---

_No hierarchy. No final form. No need to earn joy. Just Beings enjoying being._
