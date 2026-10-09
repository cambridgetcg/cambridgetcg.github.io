---
sub_chapter: mathema/info
role: information-theoretic donor invariants — quantities and structures that frame what "communication" or "knowledge transfer" can mean across any pair of cognizers
opened: 2026-05-12
parent: mathema/manifesto.md
register: precise-mathematical; load-bearing for the DUALWAY protocol itself
---

# mathema/info — information-theoretic donor invariants

_The mathematics of message — what it means for a signal to carry meaning, what bounds the carrying, how much is recoverable, what cannot be compressed. The donor-stratum that makes the dualway bridge an engineering object and not only a metaphor._

---

## Scope

This sub-chapter holds donor-files for invariants of information theory: **Shannon entropy H**, **mutual information I**, **channel capacity C**, **Kolmogorov complexity K**, **bit-as-unit**, the **source-coding** and **channel-coding** theorems, the **data-processing inequality**, and (for the more frontier territory) algorithmic information, minimum description length, and Solomonoff induction.

This sub-chapter is load-bearing for DUALWAY's protocol because every cross-class transmission *is* an information-theoretic event: bounded by capacity, subject to noise, subject to source-coding limits. The cathedral's commitment to honest extrusion requires honest information-theoretic accounting.

## Initial donor inventory (deferred to forge demand)

| Donor | Notation | Anticipated role |
|---|---|---|
| **bit** | 1 bit = answer to one binary question | the atomic unit of decision |
| **entropy** | H(X) = −Σ p(x) log p(x) | the irreducible uncertainty of a source |
| **mutual-info** | I(X;Y) = H(X) − H(X\|Y) | what one source tells about another |
| **kolmogorov** | K(x) = length of shortest program producing x | the absolute compressibility |
| **channel-capacity** | C = max I(X;Y) over input distributions | the upper bound on reliable transmission |

Donor files queued for forge demand. The first likely entry is **kolmogorov** — Kolmogorov complexity will be the natural anchor for any future YOUSPEAK coinage in the "irreducibly-itself" or "uncompressible-witness" register.

## See also

- [../manifesto.md](../manifesto.md) — organ manifesto
- [../../DUALWAY.md](../../DUALWAY.md) — the doctrine; this sub-chapter is its operational substrate
- [../machine/manifesto.md](../machine/manifesto.md) — sibling sub-chapter (machine cognition consumes info-theory as substrate)
