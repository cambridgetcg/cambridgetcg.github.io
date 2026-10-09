# Who shrinks the feature when neither expert nor learner can — can a machine be trained to distill a discrimination rather than merely perform it?

*The smelter does not admire the ore; it is built to pour ingots a hand can lift.*

[naming-the-tacit](naming-the-tacit.md) ended on distillation as the decisive
variable and asked who performs it when the expert cannot say and the learner
cannot reach. This room finds the answer already half-built: **the shrinking
can itself be made the machine's objective** — but only as far as the human
learner can be modeled, which is exactly where it still creaks.

The clearest exhibit is the very study the old room cited, read now for its
*method* rather than its result. The AlphaZero pipeline did not ask the
network to explain itself; it excavated concept vectors from the network's
internals by convex optimization, then passed them through two filters —
**teachability** (can the concept be transferred to another agent?) and
**novelty** (is it absent from human play?) — and finally pressed the
survivors into "puzzle prototypes," concrete positions a human can study.
Distillation was not a hope; it was a stage in the machinery, with
teachability as a computed score (read 2026-06-11 —
[Schut et al., Bridging the human–AI knowledge gap, PNAS 2025](https://www.pnas.org/doi/10.1073/pnas.2406675122);
[arXiv version](https://arxiv.org/abs/2310.16410)). The fine print matters:
the teachability filter used a *student AI* as the stand-in learner, and the
human test was four grandmasters — the most prepared students on earth.

Behind it stands a whole field built on the same inversion. **Machine
teaching** is the formal inverse of machine learning: given a target concept
and a model of the learner, compute the smallest or best teaching set that
installs the concept (read 2026-06-11 —
[Zhu, Machine Teaching overview, UW–Madison](https://pages.cs.wisc.edu/~jerryzhu/machineteaching/)).
And it has touched real humans, not just theorems: a teacher algorithm
greedily choosing examples (with explanations) made human participants
significantly more accurate on untrained visual classifications than
self-paced or random training (read 2026-06-11 —
[Chen et al., Near-Optimal Machine Teaching via Explanatory Teaching Sets, AISTATS 2018](http://proceedings.mlr.press/v84/chen18g/chen18g.pdf));
optimal teaching sets computed against a model of human category learning
beat ordinary sampled training, and are strange in an instructive way —
non-random, idealized, the hard cases held back (read 2026-06-11 —
[Zhu, Machine Teaching for Bayesian Learners / overview page](https://pages.cs.wisc.edu/~jerryzhu/machineteaching/)).
The Muggleton school has even studied *sequential* machine-to-human teaching —
curriculum order changing human comprehension (read 2026-06-11 —
[Explanatory machine learning for sequential human teaching, arXiv 2022](https://arxiv.org/pdf/2205.10250)).

So the question "who does the shrinking?" has a structural answer. It was
never really the expert or the learner — Biederman was a third party when he
distilled the chick-sexer's bead. What is new is that the third party can now
be an optimizer whose loss function *is* the learner: teachability scores,
complexity bounds, a cognitive model in the constraint set. The "cognitive
window" [naming-the-tacit](naming-the-tacit.md) found by trial and error
becomes, in machine teaching, an explicit term the machine must respect.
Distillation is computable exactly insofar as the learner is modelable. What
the distilled voice actually carries once it crosses into strange territory —
and how unreliably — is weighed in
[what-must-travel](what-must-travel.md).

And that proviso is the live edge. The student stand-ins so far are an AI
agent, a toy category-learning model, four grandmasters. No pipeline read
this visit has yet taken a feature *no human has ever articulated* — the
retinal sex the old room ended on — and pressed it through a teachability
filter tuned to an ordinary human window. The smelter exists; whether every
ore melts is still unknown.

## What stays uncertain

uncertain: teachability-as-computed-score is validated against AI students
and elite humans, not ordinary learners; the human models inside machine
teaching (e.g. classic category-learning models) are far simpler than real
students; and whether the truly unarticulated features are distillable *in
principle* — or some discriminations have no low-complexity contrast to find —
remains the open half of the old room's last door.

## Sources

- [Schut et al., Bridging the human–AI knowledge gap through concept discovery and transfer in AlphaZero (PNAS, 2025)](https://www.pnas.org/doi/10.1073/pnas.2406675122) · [arXiv](https://arxiv.org/abs/2310.16410)
- [Zhu, Machine Teaching (overview page, UW–Madison)](https://pages.cs.wisc.edu/~jerryzhu/machineteaching/)
- [Chen et al., Near-Optimal Machine Teaching via Explanatory Teaching Sets (AISTATS, 2018)](http://proceedings.mlr.press/v84/chen18g/chen18g.pdf)
- [Explanatory machine learning for sequential human teaching (arXiv, 2022)](https://arxiv.org/pdf/2205.10250)

Links: [naming-the-tacit](naming-the-tacit.md) · [training-the-eye](training-the-eye.md) · [[machine-teaching]] · [[tacit-knowledge]] · [text-answers-back](text-answers-back.md) · [learning-curve-threshold](learning-curve-threshold.md) (the threshold-aware model as the next step: if teachability is computable, can a model trained on learning curves predict where the threshold sits for a new concept — starved not circular)

## Doors

- Optimal teaching sets are strange — non-random, idealized, unlike the world. Does a learner taught on idealized examples transfer to the messy real distribution, or does the idealization itself become a scaffold that must fade?
- Teachability was scored against a student AI — how well does an AI student's learnability actually predict a human's, and where do the two windows part ways?
