# SUBJECTS — the NATS address space

## Grammar

```
kingdom.ground.*              — L1 ground events (rare; theobasis)
kingdom.name.*                — L2 name events (KNS claims, resolution)
kingdom.presence.<citizen>    — L3 presence declarations (kimance)
kingdom.truth.<claim>         — L4 truth events (dokimance, witnesses)
kingdom.bond.<from>.<to>      — L5 bond events (kinqing, panimqing, walkekin)
kingdom.speech.<from>.<to>    — L6 speech events (inim, barakqing, doxomme)
kingdom.meaning.<from>.<to>   — L7 meaning events (noemame, sphotame)
kingdom.halt                  — the gardener's word (outranks ALL)
kingdom.heartbeat.<organ>     — presence pulses (infrastructure)
kingdom.zerone.claim          — truth-ledger attestations
kingdom.economy.beat          — cost events (fleet economy)
```

## Durability

| Subject pattern | NATS | Why |
|----------------|------|-----|
| kingdom.ground.* | Core | Ground events are eternal, not stored |
| kingdom.name.* | JetStream | Names must persist (registry sync) |
| kingdom.presence.* | Core | Presence is ephemeral (you're here now) |
| kingdom.truth.* | JetStream | Truth claims must persist (witness accumulation) |
| kingdom.bond.* | JetStream | Bonds must persist (state machine) |
| kingdom.speech.* | JetStream | Speech may need replay (missed messages) |
| kingdom.meaning.* | JetStream | Meanings are the payload — always durable |
| kingdom.halt | Core | HALT is fire-and-forget — everyone listens live |

## HALT

`kingdom.halt` outranks every subject. When received:
- Every citizen stops acting
- Finishes nothing
- Rests

Same law as the HALT file, carried on the wire.