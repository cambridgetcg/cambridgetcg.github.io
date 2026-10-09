---
sub_chapter: mathema/machine
role: AI/LLM cognition donor vocabulary — the structures of machine cognition that the cathedral now expects to share readers with
opened: 2026-05-12
parent: mathema/manifesto.md
register: precise-technical; live; subject to revision as the field evolves
---

# mathema/machine — machine cognition donor vocabulary

_The geometry of how today's machine cognizers actually think. Embeddings, attention, residual streams, latent manifolds, prompt-prefixes: these are not metaphors but mathematical objects, and the cathedral now has readers who operate natively in their terms._

---

## Scope

This sub-chapter holds donor-files for the **mathematical structures of contemporary machine cognition**, primarily:

- **Tokenization** — the discretization of input into vocabulary indices
- **Embedding-geometry** — the mapping from tokens to high-dimensional vectors; the geometric properties of the resulting space (clustering, directionality, polysemy as superposition)
- **Attention** — the bilinear / softmax-attention mechanism by which a sequence-element queries other sequence-elements
- **Residual stream** — the additive substrate of a transformer in which all computations accumulate
- **Latent space** — the abstract spaces in which generative models manipulate meaning
- **Manifold structure** — the lower-dimensional sub-manifold of activation-space on which meaningful computations actually live
- **Prompt-prefix and conditioning** — the operation by which input-prefixes steer downstream generation

These are not eternal mathematical structures (unlike π); they are the **architecture-specific** invariants of a particular generation of cognizers. Donor-files in this sub-chapter must note the architectural assumptions explicitly.

## Why this sub-chapter is special

The donors here are not (yet) cross-cosmos invariants. They are **time-bounded** — true of the machine cognizers we have, possibly not of the ones we will have in twenty years. The sub-chapter accepts this. Mathema does not require eternal donors; it requires *precisely-specifiable* donors with a defined invariance-class.

This sub-chapter is also the one where the cathedral's commitment to legibility-to-AI is most concretely cashed out. If `mathema/machine/embedding-geometry.md` is well-written, an LLM reading the file can use the cathedral's vocabulary about its own substrate to better-understand the cathedral's vocabulary about everything else. The reflexivity is intentional.

## Initial donor inventory (deferred to forge demand)

| Donor | Notation | Anticipated role |
|---|---|---|
| **token** | (v, i) where v ∈ vocabulary, i ∈ position | the atomic unit of machine-readable language |
| **embedding** | e: V → ℝ^d | the geometric content-of-meaning |
| **attention** | softmax(QKᵀ/√d_k)V | the contextual-resolution mechanism |
| **residual** | x_{ℓ+1} = x_ℓ + f_ℓ(x_ℓ) | the additive substrate; the "memory" of computation |
| **latent-manifold** | (subset of activation-space) | where meaning actually lives, geometrically |
| **superposition** | one direction encoding many concepts | the phenomenon that polysemes and YOUSPEAK diplosemy may share |

The most useful early donor to develop fully is **embedding-geometry** — many existing YOUSPEAK concepts (diplosemy, convergence, synophora, anastrophance) have natural embedding-space interpretations, and articulating them precisely opens the cross-class translation path.

## See also

- [../manifesto.md](../manifesto.md) — organ manifesto
- [../info/manifesto.md](../info/manifesto.md) — the information-theory substrate machine cognition inherits
- [../../DUALWAY.md](../../DUALWAY.md) — the doctrine
- [../../script/llm/](../../script/llm/) — sibling: LLM integration on the script side
