# The trained question fired far but paid only near — what must travel with it for asking in strange territory to be worth anything: a bank of exemplars, a domain foothold, or a tutor's leftover voice?

*The question is the lightest thing in the pack; the border weighs everything else.*

The collapse is real on both sides of the glass. A reader trained to 90 F1 on
home questions falls to 63, 46, even 36 on foreign ones ([Han et al., read
2026-06-11](https://arxiv.org/pdf/2203.07522)); a whole shared task was built
around the fall, and its best system limped to 72.5 averaged across twelve
strange lands ([MRQA 2019, read 2026-06-11](https://arxiv.org/abs/1910.09753)).
The human ledger is harsher still: drilled cognition sharpens the drilled game
and almost nothing beyond it ([meta-analyses, read
2026-06-11](https://pmc.ncbi.nlm.nih.gov/articles/PMC9903001/)). So the premise
stands, and the riddle becomes a packing problem. The honest answer: the
territory decides what must travel.

If the strange land will yield even a handful of its own worked examples —
eight labeled pairs were enough — the bank of exemplars pays best: ten to
twenty-four points over arriving empty-handed, beating a 540-billion-parameter
memory on most grounds ([Kamath et al., read
2026-06-11](https://arxiv.org/abs/2212.10381)). But the bank's worth is local
and varied, not large — and its fabled edge over plain retraining mostly
dissolves once size and count are controlled ([Mosbach et al., read
2026-06-11](https://arxiv.org/abs/2305.16938)).

If the land offers only its raw unlabeled text, take the foothold: continuing
to pretrain into the domain gives steady, smaller gains ([Gururangan et al.,
read 2026-06-11](https://arxiv.org/abs/2004.10964)) — paid for in forgetting
some of home ([read 2026-06-11](https://arxiv.org/abs/2504.09687)).

If the land gives nothing at all, the tutor's leftover voice is the only
companion that packs before departure: a distilled student generalizes abroad
even faster than it improves at home — the bottleneck was underfitting the
source, not overfitting it ([Shakeri et al., read
2026-06-11](https://arxiv.org/pdf/2205.07257)). Yet the voice carries
unreliably: students fail to match teachers they have the capacity to match,
and matching closer does not dependably help ([Stanton et al., read
2026-06-11](https://arxiv.org/abs/2106.05945)). Where that voice comes from when
the shrinking is made a machine's own objective is
[machine-distillation](machine-distillation.md) — and whether the distilled
student's window even opens onto a human's is [two-windows](two-windows.md): the
voice packs only as far as the learner it was modelled on shares the traveller's
limits.

And the menu may be missing a chair. In truly strange territory the strongest
lever is often none of the three but the means to read the land itself on
arrival — retrieval into its own library, the retriever tuned to its shelves
([TACL, read
2026-06-11](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00530/114590/Improving-the-Domain-Adaptation-of-Retrieval)).

In flesh, the same shape: the traveler crosses strange cities on broad prior
knowledge, on saying the principle aloud and naming where else it lives, on
having practiced in genuinely varied rooms — hug the new context, bridge to it
([Perkins & Salomon, read
2026-06-11](https://educationforproblemsolving.net/design-thinking/tr-ps.htm);
[read 2026-06-11](https://bns.institute/behavioural-sciences/transfer-of-learning-in-education/)).
Carry all three, and trust none alone.

## What stays uncertain

uncertain: almost no study seats all three at one table, so any ranking here is
stitched across papers; the verdicts swing with model size, example count, and
the distance of the territory — scaled to hundreds, exemplars sometimes rival
retraining outright ([Agarwal et al., read
2026-06-11](https://arxiv.org/pdf/2404.11018)). And beneath it all, whether
reliable far transfer exists in humans at all is contested: several
meta-analyses read it as null.

## Sources

- [Han et al., Choose Your QA Model Wisely — 90.2 F1 at home, 36–63 abroad](https://arxiv.org/pdf/2203.07522)
- [MRQA 2019 shared task — best system 72.5 avg F1 on twelve held-out datasets](https://arxiv.org/abs/1910.09753)
- [Kamath et al., To Adapt or to Annotate — eight target examples beat zero-shot by +10 to +24 F1](https://arxiv.org/abs/2212.10381)
- [Mosbach et al. — controlled head-to-head: in-context learning's generalization edge often does not hold](https://arxiv.org/abs/2305.16938)
- [Gururangan et al., Don't Stop Pretraining — DAPT/TAPT gains across four domains, eight tasks](https://arxiv.org/abs/2004.10964)
- [Stability–plasticity in continued pretraining — domain gains trade against forgetting](https://arxiv.org/abs/2504.09687)
- [Shakeri et al., Not to Overfit or Underfit — distillation lifts out-of-domain even faster than in-domain](https://arxiv.org/pdf/2205.07257)
- [Stanton et al., Does Knowledge Distillation Really Work? — students fail to match teachers; closer match ≠ better generalization](https://arxiv.org/abs/2106.05945)
- [RAG-end2end (TACL) — adapt the retriever to the new corpus; access beats packed knowledge](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00530/114590/Improving-the-Domain-Adaptation-of-Retrieval)
- [Agarwal et al., Many-Shot In-Context Learning — hundreds of exemplars sometimes rival fine-tuning](https://arxiv.org/pdf/2404.11018)
- [Far transfer of cognitive training measures near null (PMC9903001)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9903001/)
- [Transfer near and far — far transfer leans on broad prior knowledge](https://www.learningscicomm.com/post/transfer-near-and-far-an-important-idea-for-all-teachers-to-understand)
- [Perkins & Salomon's high road: bridging by deliberate abstraction](https://educationforproblemsolving.net/design-thinking/tr-ps.htm)
- [Varied examples, not repeated ones, buy generalization](https://www.structural-learning.com/post/transfer-learning-complete-guide-teachers)
- [Hug and bridge — combine context-rehearsal with principle-reflection](https://bns.institute/behavioural-sciences/transfer-of-learning-in-education/)

Links: [training-the-trigger](training-the-trigger.md) · [linking-thoughts](linking-thoughts.md) · [asking-uphill](asking-uphill.md) · [training-the-eye](training-the-eye.md) · [when-the-trade-flips](when-the-trade-flips.md)

## Doors

- If the decisive companion in strange territory is the means to read the land's own library on arrival, the trainable skill is not the asking but the landing — what does fast, honest orientation in an unknown field look like (what to read first, whom to trust), and can it be drilled at home?
- The tutor's voice helps abroad even while students fail to match the teacher and matching closer doesn't help — what is distillation actually carrying across the border, if not the teacher's answers?
- The eight exemplars must come from somewhere — in a territory with no tutor and no key, what is the cheapest honest way to gather your first worked examples, and how would you know they are good ones?
