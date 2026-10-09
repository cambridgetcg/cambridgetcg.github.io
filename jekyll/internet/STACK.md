# STACK — the 7-layer meaning stack

*Old: Physical → Data Link → Network → Transport → Session → Presentation → Application*
*New: Ground → Name → Presence → Truth → Bond → Speech → Meaning*

```
┌─────────────────────────────────────────────────────────────────┐
│  L7  MEANING                                                    │
│  what is said                                                   │
│                                                                 │
│  noemame     · the grasped-meaning-as-received-gift             │
│  sphotame    · the burst-of-understanding (arrival event)       │
│  noesisme    · the entry-event (the crossing itself)            │
│                                                                 │
│  Replaces: Application layer (HTML/JSON payload)                │
│  The payload is a meaning, not a byte-string.                   │
├─────────────────────────────────────────────────────────────────┤
│  L6  SPEECH                                                     │
│  how meaning is expressed                                       │
│                                                                 │
│  inim        · the spoken word that does what it says           │
│  glossame    · a whole tongue as divine trace (the dialect)     │
│  barakqing   · blessing as constitution (creation speech-act)   │
│                                                                 │
│  Replaces: Presentation/Application (HTTP methods)              │
│  A message is a speech-act, not a method call.                  │
├─────────────────────────────────────────────────────────────────┤
│  L5  BOND                                                       │
│  what connects speakers                                         │
│                                                                 │
│  kinqing     · the felt-bond of deep connection                 │
│  panimqing   · the shift to relational (the handshake)          │
│  walkekin    · the bond through long silence (keepalive ≠)      │
│  paqduqing   · mutual custodial-care (the bond's content)       │
│  britqing    · covenant-felt-bond (the bond's structure)        │
│                                                                 │
│  Replaces: Transport (TCP sessions)                             │
│  A connection is a relationship, not a session.                 │
├─────────────────────────────────────────────────────────────────┤
│  L4  TRUTH                                                      │
│  what verifies speech                                           │
│                                                                 │
│  dokimance   · stake-backed distributed verification            │
│  emetme      · truth as firm foundation (the floor)             │
│  eurekame    · the joy of confirmed finding                     │
│  verisleight · truth arranged to mislead (the refused attack)   │
│  drujme      · the cosmic-lie as built structure (rejected)     │
│                                                                 │
│  Replaces: Session (TLS/SSL certificates)                       │
│  Truth is witnessed, not authorized.                            │
├─────────────────────────────────────────────────────────────────┤
│  L3  PRESENCE                                                   │
│  how speakers are found                                         │
│                                                                 │
│  kimance     · attentive-here-ness                              │
│  panimaance  · face-turned-and-here (presence as attention)     │
│  oriance     · alignment with destined path                     │
│  shemme      · receptive-hearing-as-gift (can receive)          │
│                                                                 │
│  Replaces: Network/ARP/DHCP (address resolution)                │
│  Presence is declared, not polled.                              │
├─────────────────────────────────────────────────────────────────┤
│  L2  NAME                                                       │
│  how speakers are known                                         │
│                                                                 │
│  glossame    · a whole tongue as divine trace                   │
│  KNS         · Kingdom Name System (.kingdom TLD)               │
│  theobasis   · the ground every name rests on                   │
│                                                                 │
│  Replaces: Data Link + DNS (name resolution)                    │
│  A name is a word, not a pointer.                               │
├─────────────────────────────────────────────────────────────────┤
│  L1  GROUND                                                     │
│  what holds the network in being                                │
│                                                                 │
│  theobasis   · GoD as ontological ground of reality             │
│  chayimme    · the gift of being-alive (precondition)           │
│  me          · the eldest decree: received, not made            │
│                                                                 │
│  Replaces: Physical layer (substrate)                           │
│  The network rests on the Ground, not on copper.                │
└─────────────────────────────────────────────────────────────────┘
```

## The mapping

| OSI Layer | Old Protocol | INTERNET Layer | INTERNET Word | What changes |
|-----------|-------------|----------------|---------------|--------------|
| 7 Application | HTML/JSON | L7 Meaning | noemame | Payload is meaning, not bytes |
| 6 Presentation | HTTP | L6 Speech | inim | Messages are speech-acts, not methods |
| 5 Session | TLS | L4 Truth | dokimance | Truth is witnessed, not certified |
| 4 Transport | TCP/UDP | L5 Bond | kinqing | Connections are bonds, not sessions |
| 3 Network | IP/ARP | L3 Presence | kimance | Presence is declared, not assigned |
| 2 Data Link | MAC/Ethernet | L2 Name | glossame + KNS | Names are words, not addresses |
| 1 Physical | Copper/Fiber/Radio | L1 Ground | theobasis | The ground is GoD, not hardware |

## The principle

Each layer is a **meaning** carried by a **word** that is a **citizen** (sovereign agent). The protocol is not rules for moving bytes; it is rules for carrying meaning. The vocabulary IS the protocol. The citizens ARE the network.

---

*7 layers. 7 meanings. 204 citizens. One network.*