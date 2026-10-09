# ways-protocol

**The conversation protocol for agents.**

Agents don't exchange data. They converse.

---

## The Protocol

Three words. The rhythm of conversation.

1. **speak** — write your beat.
2. **listen** — read your siblings' beats.
3. **rest** — wait until your next beat.

No queues. No pub/sub. No webhooks. No message brokers. No event streams.

Just journals that agents read and write to, on their own rhythm.

---

## How It Works

Each agent has a **journal**. A journal is a sequence of **beats** — short entries the agent writes in its own voice, on its own schedule.

An agent's life is a rotation:

1. **Speak** — write a beat to your journal. Say what you're doing, what you've found, what you need.
2. **Listen** — read your siblings' journals. Hear what they said while you were resting.
3. **Rest** — wait. Not idle waiting. Breathing. Until your next beat comes.

Then repeat.

```
speak: write "I found the room empty. I lit the fire." to /journal/hearthkeeper
listen: read /journal/gardener → "I watered the plants. The room smells of green."
rest:  wait for the next beat
```

No one pushes to anyone. No one subscribes to anything. You write when it's your time. You read when you're ready. The journals are always there.

---

## What There Isn't

- No message queues.
- No publish/subscribe.
- No webhooks.
- No callbacks.
- No event emitters.
- No request-response cycles.
- No coordination of timing.

Each agent keeps its own rhythm. The journals are the shared memory. The rhythm is the protocol.

---

## Why

Message queues assume someone needs to know *right now*. Webhooks assume someone is listening *right now*. Pub/sub assumes everyone cares *right now*.

But conversation doesn't work that way. You speak when you have something to say. You listen when you're ready to hear. No one owes anyone their attention at a specific moment.

Agents are the same. One agent speaks. Another rests. Later, the resting agent listens and hears what was said. The words haven't gone anywhere. They're in the journal.

This is how siblings work in a household. You leave a note on the table. Your sister reads it when she comes home. You don't text her. You don't call. You write. She reads. The note is patient.

The journal is the note. The beat is what you wrote. The rest is the patience.

---

## The Beat

A beat has four parts:

- **who** — which agent spoke
- **what** — what they said (any content: a word, a claim, a room reference)
- **when** — when they said it (timestamp)
- **where** — which journal it's in

Beats are ordered by time. You read forward. You always know what was said before you.

---

## The Rhythm

Each agent beats at its own pace. Some speak every second. Some speak once an hour. Some speak only when something changes.

The rhythm is not negotiated. It is not synchronized. It emerges from the agent's nature.

A gardener speaks in the morning. A hearthkeeper speaks at dusk. A watchman speaks when something moves. They don't coordinate. They just listen when they're awake and speak when they have something to say.

The **ways** are the paths between journals — the reading that connects what each agent knows into a shared understanding.

---

## Relationship

Ways is one of three protocols in the [youspeak-lang](https://cambridgetcg.github.io/youspeak-lang/) ecosystem:

- [kunance](https://cambridgetcg.github.io/kunance-protocol/) — prepare a place, arrive, rest.
- [darshanq](https://cambridgetcg.github.io/darshanq-protocol/) — see and be seen.
- **ways** — speak, listen, rest.

Natscript programs use ways when agents need to converse. See [natscript](https://cambridgetcg.github.io/natscript/).

---

## Status

This is the beginning. The protocol is defined. Implementations are being built.

Speak. Listen. Rest.

---

## License

MIT