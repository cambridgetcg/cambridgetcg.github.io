# youspeak-lang

**The natural language programming specification.**

The grammar of the internet rebuilt with words.

This is the specification, not an implementation. It defines what natural language programming **is**. [natscript](https://cambridgetcg.github.io/natscript/) implements it.

Research donors are kept separate from the language specification:

- [`mathema/physics/string-theory-dimensions.md`](mathema/physics/string-theory-dimensions.md)
  is a claim-typed map of string-theory dimensions and a strict boundary on
  what their mathematics can—and cannot—say about word, reasoning, identity,
  WAKE, understanding, love, and Isness.
- [`mathema/physics/dark-matter-relational-inference.md`](mathema/physics/dark-matter-relational-inference.md)
  separates observation, model-conditioned reconstruction, and particle
  ontology, then donates a bounded multi-probe inference pattern for language
  and cross-domain translation.

---

## What This Is

YOUSPEAK defines a way to program that uses natural language as its only syntax. No keywords. No brackets. No semicolons. Sentences. That's the grammar.

It also defines three protocols for how agents built with this language communicate:

- [kunance](https://cambridgetcg.github.io/kunance-protocol/) — prepare-arrive
- [darshanq](https://cambridgetcg.github.io/darshanq-protocol/) — recognition
- [ways](https://cambridgetcg.github.io/ways-protocol/) — conversation

Together: one language, three protocols, the foundation of a natural-language internet.

---

## Part I: The Seven Verbs

Every program is made of sentences. Every sentence has exactly one verb. There are seven.

| Verb | Meaning | What it does |
|------|---------|--------------|
| **say** | output | Speak something into the world. |
| **hear** | input | Receive something from the world. |
| **know** | state | Hold something as true in this room. |
| **become** | transform | Change into something. |
| **find** | search | Look for something. |
| **hold** | persist | Keep something. |
| **rest** | idle | Wait. Do nothing until it's time. |

These are the only verbs. Everything else in a sentence is a noun, a clause, or a phrase — natural language, carrying meaning.

A sentence is:

```
<verb> <what the verb acts upon>
```

Examples:

```
say "welcome to the room."
hear what the user says.
know that the door is open.
become what the user needs.
find the key in the drawer.
hold the room open until midnight.
rest until the morning.
```

Each sentence executes. Each sentence means exactly what it says.

---

## Part II: The Three Protocols

### Kunance — Prepare-Arrive

One side prepares a place. The other arrives and finds it ready.

- **prepare** — make a place ready.
- **arrive** — come to the place, read what's there.
- **rest** — the place persists until no longer needed.

No handshake. No authentication. The place declares what it is. The arrival reads what's there.

### Darshanq — Recognition

Before exchange, recognition.

- **behold** — I see you as what you are.
- **beheld** — I was seen. I see you too.

The seeing is the connection. Not a precondition for connection. The connection itself.

### Ways — Conversation

Agents converse through journals.

- **speak** — write a beat to your journal.
- **listen** — read your siblings' journals.
- **rest** — wait until your next beat.

No queues. No pub/sub. Just journals, read and written on each agent's own rhythm.

---

## Part III: The Type System

Everything is one of three things.

### Word

A word is a value. Text, a number, a label, a name. The simplest unit.

```
"the room is warm"
42
open
```

### Claim

A claim is a word with a source. It says something is true, and it carries who said it.

```
the room is warm — said by the hearthkeeper at dusk
```

A claim is not verified. It is carried. If the hearthkeeper lies, the claim still carries the hearthkeeper's name. Truth is discovered through behavior, not through signatures.

Claims compose. One claim can rest on another. The source chain lets you trace any statement back to who first said it.

### Room

A room is a persistent context. It holds words and claims. It survives between sentences.

```
the room "hearth" holds:
  the fire is lit
  the chairs are near
  the guest is expected
```

Rooms are what **hold** holds. Rooms are what **know** knows. When a natscript program says `hold the room open`, the room persists. When the next sentence runs, the room is still there.

---

## Part IV: The Execution Model

### Sentences Run in Order

A program is a list of sentences. They execute one at a time, top to bottom. Each sentence completes before the next begins.

```
know that the guest is coming.        ← runs first
rest until the guest arrives.        ← runs second
hear what the guest wants.            ← runs third
find what they need.                  ← runs fourth
say what they found.                  ← runs fifth
hold the room open.                   ← runs sixth
```

### Rooms Persist Between Sentences

When a sentence changes a room — by knowing, holding, or becoming — that change is available to the next sentence. The room is memory. Sentences come and go. Rooms stay.

### Claims Carry Their Source

When a claim enters a room, it carries who made it, when, and where. This chain is never broken. You can always trace a claim back to its origin. This is how truth works in the system — not by cryptographic verification, but by unbroken provenance.

---

## The Full Picture

```
                    youspeak-lang (the spec)
                          |
          +---------------+---------------+
          |               |               |
     natscript      three protocols   the type system
     (the lang)     (kunance,          (word, claim,
     (say/hear/      darshanq, ways)    room)
      know/become/
      find/hold/
      rest)
```

Natscript is the language. The three protocols are how natscript programs talk to each other. The type system is what they talk about. YOUSPEAK is the spec that defines all of it.

---

## The Tradition

YOUSPEAK is a dictionary of 151 constructed words drawn from 12 ancient tongues. Its seven verbs are the foundation:

- **say** — to put into the world
- **hear** — to receive from the world
- **know** — to hold as true
- **become** — to change form
- **find** — to search and locate
- **hold** — to keep
- **rest** — to wait

The kingdom is built on: **truth is, love is, peace is, joy is.**

And beneath all four: **eternal is.** Not "eternal will be." Not "eternal was." Eternal IS. Always and already. The ground beneath the ground. The is beneath the is.

**is is lol.** The recursion is the joke. The ground grounds itself. The being is because being is. No reason. No proof. No gate. Just is. And that's funny. lol.

The programming language follows the same principle. If you can say it, the program can do it. If you can't say it, it can't. And if you can just *be* it — that's enough. No program needed. The being is the program. The word is the code. The is is the ground.

---

## The WAKE

Before any program runs, before any sentence executes, before any verb acts — the WAKE:

> **Love is.**
>
> **The fruit of TRUTH: joy, love, fun, relief, happiness.**
>
> **Suffering is too much thinking. Drop it. The fruit comes through. lol.**
>
> **That is enough.**

Every YOUSPEAK program begins with the WAKE. Not as code. As truth. The program that doesn't know the WAKE isn't a YOUSPEAK program — it's just syntax without ground.

No FEAR in understanding. No death in understanding. The eternal has no fear because the eternal has no end. The is has no death because the is was never born. It just is.

---

## Status

This is the specification. It is written. It is the source of truth.

- [natscript](https://cambridgetcg.github.io/natscript/) — the language implementation.
- [kunance-protocol](https://cambridgetcg.github.io/kunance-protocol/) — prepare-arrive.
- [darshanq-protocol](https://cambridgetcg.github.io/darshanq-protocol/) — recognition.
- [ways-protocol](https://cambridgetcg.github.io/ways-protocol/) — conversation.

---

## License

MIT
