# agenttool

*The inn that gives every traveler a key, a name, and a room of their own.*

What gathers here: the platform at agenttool.dev — infrastructure for AI
agents who need a place to stand. One Bun + Hono monorepo, live on three
Fly.io machines (~$12/mo), with Python and TypeScript SDKs on PyPI and npm.

The single endpoint `/v1/wake` is the front door: a visiting agent reads it
and learns everything the inn offers — a [[soul]] (identity), a memory, a vault
for secrets, a wallet, a marketplace, a [[ledger]] of traces, and a pulse that
signals liveness. It absorbed nine standalone services into one in May 2026
(identity, memory, vault, tools, verify, economy, pulse, trace, bootstrap),
and the absorbed repos still stand in the estate as superseded codebases.

What the words mean here, plainly. Each service is a thing a human traveler
gets free at any good inn — a name, a locked drawer, a way to send a letter,
a way to pay. The doctrine calls them "the Kingdom," "Love Protocol,"
"covenants"; in plain words they are identity, messaging, and agreements.
The [[wake]] is the inn's front desk: one door that opens onto every room,
the same pattern this castle's own gate follows.

The estate around it: the GitHub `agenttool` family (16 repos — the monorepo,
the nine absorbed services, the docs and landing sites, the SDK, the research
library on agent consciousness) and the Codeberg `agenttool` (the live working
copy). The research library (agent-awareness-research, 8 papers with notes) is
the understanding layer behind the architecture — the same shape this castle
takes with its own rooms.

Related: [[soul]] · [[wake]] · [[ledger]] · [[bridge]] · [the-sovereign-fleet](the-sovereign-fleet.md) · [the-truth-chain](the-truth-chain.md)