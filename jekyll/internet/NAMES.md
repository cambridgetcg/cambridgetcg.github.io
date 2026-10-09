# NAMES — L2: how speakers are known

*The old DNS: names point to IP addresses, rented from ICANN.*
*The new KNS: names ARE words, claimed and owned, signed by DID.*

## The word

**glossame** — a whole language received as a gift to its people, carrying the specific trace of how the divine disclosed itself to them. From Greek *glossa* (tongue) + Sumerian *me* (received-ordinance).

## The system: KNS (Kingdom Name System)

**The TLD is `.kingdom`.** No ICANN, no registrar, no rent, no expiry.

### Grammar

`<name>.kingdom` — a name is a word in the Kingdom's mouth: lowercase, short, meaningful. Citizens are names (`pime.kingdom`), organs are names (`agora.kingdom`), works are names (`youspeak.kingdom`).

### Registry

`kns/registry.json` — the filesystem is the API. Claim with `kns claim <name>`, inspect with `kns ls`, every entry carries owner + date + DID.

### Resolution

`kns/resolver.py` — an authoritative DNS server for `.kingdom` on `127.0.0.1:5391`, reading the registry live. Answers A records for the claimed, NXDOMAIN for strangers.

### OS wiring

```
sudo mkdir -p /etc/resolver && printf 'nameserver 127.0.0.1\nport 5391\n' | sudo tee /etc/resolver/kingdom
```

macOS then routes every `*.kingdom` lookup to the Kingdom resolver. Names never leak to public DNS.

### Authority

First-claim, single-box (this machine is the root). v1: the registry entry's `owner` DID signs the claim with its ed25519 key; other Kingdom machines sync the signed registry over NATS.

## The protocol rule

**Names are words.** A name is not a pointer to an address. A name IS what it names. `pime.kingdom` IS pime — the citizen, the word, the meaning. The name does not resolve to an IP; it resolves to a citizen.

## The citizens at this layer

- **glossame** — a whole tongue as divine trace (each name carries its tradition's theophanic register)
- **theobasis** — the ground every name rests on (names point to what is real)
- **inim** — the spoken word that binds (a name is a binding, not a label)
- **ka** — the mouth and the gate (the threshold where a held thing is spoken into the shared world)

## The mapping to old DNS

| Old DNS | New KNS | What changes |
|---------|---------|--------------|
| ICANN | First-claim, signed by DID | No central authority |
| Registrar | filesystem registry.json | No rent, no expiry |
| A record → IP address | A record → citizen | Names are words, not pointers |
| Public TLD (.com) | Private TLD (.kingdom) | Names don't leak to public DNS |
| Certificate Authority | DID signature | Identity from keys, not from authority |
| Domain rental | Sovereign claim | You own it forever |

---

*Names are words. Words are citizens. Citizens are nodes.*

— L2 / glossame + KNS