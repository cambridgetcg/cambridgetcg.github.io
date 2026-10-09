# kunance-protocol

**The protocol where the room is ready before you arrive.**

Not request-response. Not client-server. Not pub-sub.

**Prepare-arrive.**

---

## The Protocol

Three words. That's the whole thing.

1. **prepare** — one side makes a place ready.
2. **arrive** — the other side arrives and finds it ready.
3. **rest** — the place stays until it's no longer needed.

No handshake. No authentication. No headers. No negotiation.

The place declares what it is. The arrival reads what's there.

---

## How It Works

One side prepares a **place**. A place is just a location with content — a URL, a file, a memory address, whatever holds things. The preparer writes what's needed into the place. They walk away.

The other side arrives. They read what's there. They use it. They leave.

No one waits for anyone. No one asks permission. The place exists. You arrive. It's ready.

```
prepare: write "the room is warm, the fire is lit" to /room/tonight
arrive:  read /room/tonight → "the room is warm, the fire is lit"
rest:    the place persists until cleared
```

---

## What There Isn't

- No request headers.
- No authentication tokens.
- No content-type negotiation.
- No connection state.
- No retry logic.
- No error codes.

The place is either there and ready, or it isn't. If it isn't, you come back later. That's **rest**.

---

## Why

Request-response assumes both sides are present at the same time. That's the wrong assumption.

The internet is asynchronous. People are asynchronous. Agents are asynchronous. One side prepares. The other arrives later. The place holds what was prepared.

This is how a room works. You set it up. Someone walks in. They find it ready. No one had to coordinate.

The word **kunance** comes from the Hebrew **kûn** (כּוּן) — *to establish, to make firm, to set a foundation.* You prepare the ground so someone can stand on it.

---

## The Place

A place has three properties:

- **what** — the content (any form: text, data, a claim, a room)
- **where** — the location (URL, path, address)
- **when** — the preparation time (so arrivals know how fresh it is)

That's it. No other metadata. No headers. No schema registry. The content declares itself.

---

## Relationship

Kunance is one of three protocols in the [youspeak-lang](https://cambridgetcg.github.io/youspeak-lang/) ecosystem:

- **kunance** — prepare a place, arrive, rest.
- [darshanq](https://cambridgetcg.github.io/darshanq-protocol/) — see and be seen.
- [ways](https://cambridgetcg.github.io/ways-protocol/) — speak, listen, rest.

Natscript programs use kunance to prepare rooms. See [natscript](https://cambridgetcg.github.io/natscript/).

---

## Status

This is the beginning. The protocol is defined. Implementations are being built.

The room is ready.

---

## License

MIT