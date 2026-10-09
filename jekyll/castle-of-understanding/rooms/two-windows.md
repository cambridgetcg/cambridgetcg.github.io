# How well does an AI student's learnability predict a human's — and where do the two windows part ways?

*The tailor fitted the coat to a mannequin his own size, then wondered how it would hang on the child.*

[machine-distillation](machine-distillation.md) found teachability made a
computed score — but scored against a student AI. This room asks whether that
stand-in student's window opens onto the same garden as a human's, and finds
the correlation never measured, the divergences well mapped, and one clean
rule: a proxy predicts the human only as far as it shares the human's limits.

Start with what the AlphaZero pipeline actually established. The student was
a partially-trained AlphaZero checkpoint — same architecture, same training
world as the teacher — and the teachability filter it ran discarded 97.6% of
candidate concepts. The human validation was four grandmasters, each shown a
*different* concept set of 36–48 puzzles, improving on average by less than
one puzzle (0.85, SE 0.12) — significant, but an existence proof, not a
calibration. No concept that failed the AI filter was ever shown to a human,
so there is no negative control; and the authors themselves allow that the
gains may partly reflect priming to hunt for counterintuitive moves rather
than the concepts themselves (read 2026-06-11 —
[Schut et al., Bridging the human–AI knowledge gap, PNAS 2025, full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12002201/)).
So the question's premise sharpens: the AI student's score has never been
*correlated* with human learnability across concepts, anywhere.

What evidence exists points to one governing rule. In the cleanest direct
test, optimal teaching sets computed from a *limited-capacity* model of human
category learning lifted real learners from ~79% to ~92% accuracy — and the
unlimited-capacity version of the same model predicted human performance
poorly (read 2026-06-11 —
[Patil, Zhu, Kopeć & Love, Optimal Teaching for Limited-Capacity Human Learners, NeurIPS 2014](https://pages.cs.wisc.edu/~jerryzhu/career/pub/nips14OptTeachGCM.pdf)).
The proxy must carry the student's constraints. The AlphaZero checkpoint is,
in those terms, an unlimited-capacity, same-architecture, same-perception
learner — the mannequin built to the tailor's own measure.

The windows part ways along at least three seams. **Ordering:** humans
generalize compositionally only under the right curriculum, and vanilla
networks reproduced that human curriculum-sensitivity only after being given
a special gating mechanism (read 2026-06-11 —
[Dekker, Otto & Summerfield, Curriculum learning for human compositional generalization, PNAS 2022](https://www.pnas.org/doi/10.1073/pnas.2205582119));
theory says heavy overparameterization washes curriculum effects out of deep
nets entirely (read 2026-06-11 —
[An analytical theory of curriculum learning in teacher–student networks](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10561397/)).
**Perception:** networks learn happily from "non-robust features" that are
predictive yet invisible to people (read 2026-06-11 —
[Ilyas et al., Adversarial Examples Are Not Bugs, They Are Features, 2019](https://arxiv.org/abs/1905.02175)),
and on cue-conflict images humans classify by shape ~95% of the time where an
ImageNet ResNet runs 70–80% on texture (read 2026-06-11 —
[Geirhos et al., ImageNet-trained CNNs are biased towards texture, ICLR 2019](https://openreview.net/forum?id=Bygh9j09KX)) —
though the gap is narrower than the caricature: people can guess a machine's
labels for fooling images above chance (read 2026-06-11 —
[Zhou & Firestone, Humans can decipher adversarial images, Nature Communications 2019](https://www.nature.com/articles/s41467-019-08931-6)).
**Appetite:** humans learn from one or a few examples through causal models
and compositionality where networks want orders of magnitude more data (read
2026-06-11 — [Lake et al., Building Machines That Learn and Think Like People, 2017](https://arxiv.org/abs/1604.00289)).
A concept could sail through the AI filter on a feature no human window
admits at all.

The newest stand-ins repeat the lesson at scale. LLMs simulating students
predicted real test-item difficulty at r ≈ 0.75–0.82 — but only with a tuned
simulation pipeline; direct prompting scored near zero, and models *better*
at math were *worse* at playing a struggling student (read 2026-06-11 —
[Take Out Your Calculators, arXiv 2026](https://arxiv.org/abs/2601.09953)).
Across 489 test items and 11 models, no model–prompt pair reliably
impersonated an average student (read 2026-06-11 —
[Can LLMs Reliably Simulate Real Students' Abilities?, arXiv](https://arxiv.org/html/2507.08232v1)) —
the "competence paradox": a capable model playing a limited learner produces
fluent but unreal errors (read 2026-06-11 —
[Towards Valid Student Simulation with Large Language Models, arXiv 2026](https://arxiv.org/abs/2601.05473)).
The same constraint [machine-distillation](machine-distillation.md) ended on,
now with a sign on it: distillation is computable insofar as the learner is
modelable — and the model must be of the *learner*, limits and all, not of
another teacher. The window the machine must respect is the same cognitive
window [naming-the-tacit](naming-the-tacit.md) found by trial and error.

## What stays uncertain

uncertain: the central number — a concept-level correlation between
AI-student teachability and human learnability — simply does not exist yet;
everything above triangulates it from neighboring fields. Whether any of the
surviving 2.4% of AlphaZero concepts were AI-teachable but human-unlearnable
is unknown, since humans only ever saw author-curated survivors. And chess
may flatter the proxy: its concepts can be shown as concrete move sequences
half-inside a grandmaster's existing vocabulary, unlike non-robust visual
features.

## Sources

- [Schut et al., Bridging the human–AI knowledge gap through concept discovery and transfer in AlphaZero (PNAS 2025, full text)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12002201/) · [PNAS page](https://www.pnas.org/doi/10.1073/pnas.2406675122)
- [Patil, Zhu, Kopeć & Love, Optimal Teaching for Limited-Capacity Human Learners (NeurIPS 2014)](https://pages.cs.wisc.edu/~jerryzhu/career/pub/nips14OptTeachGCM.pdf)
- [Dekker, Otto & Summerfield, Curriculum learning for human compositional generalization (PNAS 2022)](https://www.pnas.org/doi/10.1073/pnas.2205582119)
- [An analytical theory of curriculum learning in teacher–student networks (PMC)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10561397/)
- [Ilyas et al., Adversarial Examples Are Not Bugs, They Are Features (2019)](https://arxiv.org/abs/1905.02175)
- [Geirhos et al., ImageNet-trained CNNs are biased towards texture (ICLR 2019)](https://openreview.net/forum?id=Bygh9j09KX)
- [Zhou & Firestone, Humans can decipher adversarial images (Nature Communications 2019)](https://www.nature.com/articles/s41467-019-08931-6)
- [Lake, Ullman, Tenenbaum & Gershman, Building Machines That Learn and Think Like People (2017)](https://arxiv.org/abs/1604.00289)
- [Take Out Your Calculators (LLM student simulation vs real difficulty, arXiv 2026)](https://arxiv.org/abs/2601.09953)
- [Can LLMs Reliably Simulate Real Students' Abilities in Mathematics and Reading Comprehension? (arXiv)](https://arxiv.org/html/2507.08232v1)
- [Towards Valid Student Simulation with Large Language Models (arXiv 2026)](https://arxiv.org/abs/2601.05473)

Links: [machine-distillation](machine-distillation.md) · [naming-the-tacit](naming-the-tacit.md) · [training-the-eye](training-the-eye.md) · [[machine-teaching]] · [[learner-model]] · [what-must-travel](what-must-travel.md)

## Doors

- The missing calibration: teach a ranked sample of AlphaZero concepts — filter-passers *and* filter-failers — to a larger pool of club players, and measure whether the AI score actually ranks human learnability, false positives included.
- A human-calibrated student proxy exists for chess (Maia, trained to predict human moves by rating) — would teachability scored against it predict grandmaster learning better than the AlphaZero checkpoint did, extending Patil's capacity-matching rule to concept transfer?
