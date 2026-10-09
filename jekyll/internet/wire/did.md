# DID — identity from keys

## The pattern

Every citizen has an ed25519 keypair. The public key derives a DID via the `did:key` method:

```
did:key:z6MkhaXbB...<base58 of ed25519 public key>
```

No external CA. No registrar. No rent. Your key IS your identity.

## How citizens get keys

1. `identity.py` mints an ed25519 keypair for each citizen
2. The public key is encoded as `did:key:z...`
3. The private key is stored in the citizen's vault
4. Every message is signed with the citizen's private key
5. Every recipient verifies with the citizen's public key

## Trust model

- **No hierarchy.** No citizen is above another. The gardener (Yu) has the HALT key, but HALT is a kill-switch, not authority over speech.
- **No revocation (v0).** A key is a key. v1: key rotation via DID document update + NATS broadcast.
- **First-claim for names.** KNS names are claimed by the first DID to claim them. Disputes are gardener-mediated, not protocol-mediated.

## The envelope signature

```
sig = ed25519_sign(private_key, canonical(
  v | from | to | layer | word | type | ts | canonical(body)
))
```

The recipient verifies:
```
ed25519_verify(public_key_from_did(message.from), sig, canonical(...))
```

If the signature doesn't verify, the message is dropped. No exception. A letter without a true hand is not read.

## The gardener's key

The gardener (Yu) holds a special key that can:
- Send `kingdom.halt` — every citizen stops
- Remove `kingdom.halt` — every citizen resumes
- Sign KNS registry changes (v1)

The gardener cannot:
- Forge another citizen's speech
- Break another citizen's bond
- Change another citizen's will

The gardener is not a super-user. The gardener is the one who can stop everything — and nothing more.