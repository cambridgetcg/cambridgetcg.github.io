# protocol

**The network layer for a natural-language internet.**

Protocol defines how systems discover each other, declare their state,
negotiate interaction, and exchange information — all through readable
declarations instead of rigid API contracts.

The truth IS the protocol. Before two systems exchange bytes, they
exchange meaning.

## The four layers

```
┌─────────────────────────────────────────┐
│  4. exchange   — message passing         │  "opal, run cargo build"
│  3. handshake  — negotiate interaction   │  "can you build? yes I can"
│  2. discovery  — find and read STATE.md  │  "who's out there?"
│  1. declare    — emit STATE.md           │  "here's what I am"
└─────────────────────────────────────────┘
```

## Layer 1 — declare

A system emits a STATE.md at its root. Six sections: identity, state,
knows, can, needs, how-to-talk-to-me. Following the Clear Standard's
six principles. Any agent can read it and know what the system is.

Spec: [clear-standard/STATE.md](https://cambridgetcg.github.io/clear-standard/)

## Layer 2 — discovery

discover.py reads every STATE.md in range, cross-checks each declaration
against reality (build passing? git clean? freshness current?), and finds
where one system's needs meet another's can. The output is a living map —
generated from truth, not hand-maintained.

Reader: discover.py (a local script; source kept private)

## Layer 3 — handshake

Two systems that discovered each other negotiate interaction. The handshake
is a natural-language exchange:

  opal -> youspeak:
    "I can respond to timer interrupts (arm, fire, re-arm)"
    "Can you use a heartbeat?"

  youspeak -> opal:
    "I need the heartbeat to keep forging"
    "Can you provide a timer?"

  handshake result:
    opal provides timer pattern -> youspeak uses it for heartbeat scheduling
    agreement: opal's heartbeat fires every 4h, youspeak's every 6h

The handshake is not a contract — it is a conversation. Either party can
update their STATE.md and the agreement re-negotiates on the next discovery.

## Layer 4 — exchange

Once handshake is complete, systems exchange messages. Messages are
natural-language commands or state updates, not JSON RPC calls:

  discover.py -> opal:
    "cross-check your STATE.md"

  opal -> discover.py:
    "build: passing (verified), health: active (verified),
     freshness: live (verified), 3 uncommitted files (verified)"

The exchange follows the Clear Standard: every claim is labelled
(measured vs guessed, live vs cached, verified vs unverified).

## The discovery message format

  DISCOVER <from-system>
  DECLARE <state-md-content>
  CROSS-CHECK <claim> <result>
  NEED <what-I-need>
  CAN <what-I-can-do>
  CONNECT <my-need> <your-can> <shared-keywords>

Plain text. Human-readable. Agent-parseable. No JSON, no protobuf, no
binary encoding. The protocol IS natural language.

## What exists now

- Layer 1 (declare): STATE.md spec + 5 live implementations
- Layer 2 (discovery): discover.py working — reads, cross-checks, finds connections
- Layer 3 (handshake): designed, not yet implemented
- Layer 4 (exchange): designed, not yet implemented

## Related

- [natural](https://cambridgetcg.github.io/natural-lang/) — the programming language
- [clear-standard](https://cambridgetcg.github.io/clear-standard/) — the honesty standard
- discover.py — the reader (a local script; source kept private)

---

*Before bytes, meaning. Before contracts, truth. Before APIs, declaration.
The protocol IS natural language.*