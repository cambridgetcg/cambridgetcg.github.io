# KNS Protocol — Kingdom Name System

## v0 (stands)

- **TLD:** `.kingdom`
- **Registry:** `registry.json` (filesystem IS the API)
- **Resolver:** `resolver.py` on `127.0.0.1:5391`
- **Authority:** first-claim, single-box
- **OS wiring:** `/etc/resolver/kingdom` → `127.0.0.1:5391`

## v1 (waits)

- Signed claims (DID + ed25519)
- NATS registry sync across machines
- Multi-box root without consensus theater

## CLI

```sh
kns claim <name>      # claim a name
kns ls                # list all names
kns resolve <name>    # resolve to A record
```

## Grammar

A name is a word in the Kingdom's mouth:
- lowercase
- short (one word)
- meaningful (a YOUSPEAK word, a Sumerian root, or a Kingdom concept)

Examples:
- `pime.kingdom` — the citizen pime (mathematical invariant)
- `agora.kingdom` — the square
- `youspeak.kingdom` — the cathedral
- `internet.kingdom` — this protocol