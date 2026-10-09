# Pointing presumes a pointer who can say what they see, but much expertise is tacit — in a field whose experts cannot articulate their own features, how does a learner extract them: contrast alone, or machines that learned the discrimination naming it back?

*The master sexes the chick and cannot say how; someone else, watching, finds the one word he was missing — and a minute later the novice can do it too.*

[training-the-eye](training-the-eye.md) leaned on a pointer who could name the
diagnostic feature. This room asks what happens when no one can — and finds the
bottleneck is rarely that the feature is unsayable, only that no one has yet
*said it out*.

Start with the very case that made "tacit" famous. Chick-sexing is told as
proof that some skill lives only in the trained eye. But Biederman & Shiffrar
did an expert-systems analysis — interviewing sexers of eighteen to thirty-six
years' standing — and isolated a single nameable contrast: the genital bead is
**convex in males, concave or flat in females**. A roughly one-minute
instruction sheet naming that contrast lifted novices about forty points, to
near-expert on the lab images (read 2026-06-10 —
[Biederman & Shiffrar 1987](https://www.sciepub.com/reference/17257)). The
[tacit knowledge](../words/tacit-knowledge.md) was not locked; it was
**un-analyzed**. This naming-nudge is the same law
[words-shape-thought](words-shape-thought.md) found in the Russian-blue studies,
read from a second literature — each room the other's strongest evidence. The same move works on statistics no eye weights on its own:
a five-and-a-half-minute module on which fingerprint minutiae are *rare* — and
so diagnostic — improved 551 people including fifty-two professional examiners
(read 2026-06-10 — [Growns et al. 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9288576/)).

How much stays un-analyzed is the real question. The knowledge-elicitation
trade works from a rule of thumb that experts run most decisions on automatic,
unverbalized knowledge and omit much of what a novice needs when they narrate
their own task — a robust direction, a folklore-grade number (read 2026-06-10 —
[Global Cognition, Cognitive Task Analysis](https://www.globalcognition.org/cognitive-task-analysis/);
review, [PMC8903544](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8903544/)). So
the analyst recovers a meaningful slice, never the whole.

When no analyst can reach the feature, two routes remain. **Contrast and
feedback alone** build the discrimination without ever naming it: Kellman's
perceptual-learning modules raise accuracy *and* speed across histology,
dermatology, radiology by many feedback-driven classification trials (read
2026-06-10 — [Kellman lab](https://kellmanlab.psych.ucla.edu/research-perceptual-and-adaptive-learning-in-medicine.php)),
and feedback by itself — with no bottom-up exposure driving it — can install a
discrimination (read 2026-06-10 —
[Liu, Lu & Dosher 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3352973/)).
This is [training-the-eye](training-the-eye.md)'s engine, running with the
pointer switched off. **Machines naming the feature back** is the newer route
and has two real successes. DeepMind mined AlphaZero's latent space, filtered
its concepts by *teachability* and *novelty*, and taught the survivors to four
grandmasters, every one of whom improved on unseen puzzles — one going from
none solved to five (read 2026-06-10 —
[Schut et al., PNAS 2025](https://www.pnas.org/doi/10.1073/pnas.2406675122)).
And the fingerprint features above were, in effect, the discrimination
analyzed out of the data and handed back.

But the machine route mostly disappoints, and the reason sharpens the whole
answer. The common explainer — the saliency map, the heat-blob over the image —
fails to lift human performance about as often as it helps, across sixty-eight
user studies (read 2026-06-10 —
[Müller 2024](https://arxiv.org/abs/2404.16042)). Worse, a machine explanation
that exceeds the learner's "cognitive window" — too complex to hold — leaves
them performing *below* no explanation at all (read 2026-06-10 —
[Ai, Muggleton et al. 2021](https://link.springer.com/article/10.1007/s10994-020-05941-0)).
And the explanatory concept is often *harder* to learn than the thing it
explains (read 2026-06-10 —
[Ramaswamy et al. 2022](https://arxiv.org/pdf/2207.09615)). The decisive
variable is not contrast versus machine. It is **distillation**: a
discrimination becomes teachable only when someone — a human analyst, or an
ML method constrained to be teachable — reduces it to a low-complexity,
human-legible contrast. That is exactly what Biederman did by hand for the
chick. Where the feature cannot be so reduced — a network reads age and sex
and cardiac risk off a retinal photograph that no clinician can interpret
(read 2026-06-10 — [Poplin et al. 2018](https://www.nature.com/articles/s41551-018-0195-0))
— the machine plainly *uses* a real feature it cannot yet hand to a human.

So: contrast and feedback always work and need no pointer; a named feature,
when one can be distilled, works faster and even re-trains experts; and a
machine helps only when its answer survives the same shrinking the human
analyst performs. The eye [training-the-eye](training-the-eye.md) trains is
the floor that never fails; the named feature is the elevator, and it runs
only when someone fits it into the cognitive window. And the elevator has a
floor of its own: [precise-across-time](precise-across-time.md) holds the other
half of the law — name a feature finer than its category and the naming erases
the very precision it meant to keep — so together the two rooms bound when to
name and when to stay silent. And the silence is not willed:
[choosing-not-to-name](choosing-not-to-name.md) finds the name fires on its own
the moment one exists, so staying silent means starving the label, never
ordering it quiet.

## What stays uncertain

uncertain: there is no clean horse-race — no rigorous trial pitting pure
contrast-plus-feedback against feature instruction on the *same* perceptual
task with transfer and retention measured, so their relative efficiency is
essentially unknown. The concept-based explainers in dermatology and pathology
demonstrate the model *can* articulate human-legible concepts but almost never
test whether a learner's own unaided skill improves after studying them. The
AlphaZero transfer is four elite players, no control group — whether
machine-found concepts teach ordinary learners, or transfer out of closed-world
games into noisy medical perception, is untested. And whether the truly
un-articulable features (retinal sex, some histopathology gestalts) are *in
principle* distillable or permanently locked in the network is open.

## Sources

- [Biederman & Shiffrar, Sexing Day-Old Chicks (JEP:LMC, 1987)](https://www.sciepub.com/reference/17257)
- [Growns et al., Statistical feature training improves fingerprint matching (PNAS Nexus, 2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9288576/)
- [Global Cognition — What is Cognitive Task Analysis?](https://www.globalcognition.org/cognitive-task-analysis/)
- [CTA in clinical research, systematic review (PMC8903544)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8903544/)
- [Kellman lab — Perceptual & Adaptive Learning Modules](https://kellmanlab.psych.ucla.edu/research-perceptual-and-adaptive-learning-in-medicine.php)
- [Liu, Lu & Dosher, Perceptual learning solely induced by feedback (Vision Research, 2012)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3352973/)
- [Schut, Kim et al., Bridging the human–AI knowledge gap (PNAS, 2025)](https://www.pnas.org/doi/10.1073/pnas.2406675122)
- [Müller, How explainable AI affects human performance — 68 studies (2024)](https://arxiv.org/abs/2404.16042)
- [Ai, Muggleton et al., Beneficial and harmful explanatory machine learning (Machine Learning, 2021)](https://link.springer.com/article/10.1007/s10994-020-05941-0)
- [Ramaswamy et al., Overlooked factors in concept-based explanations (2022)](https://arxiv.org/pdf/2207.09615)
- [Poplin et al., Predicting cardiovascular risk factors from retinal photographs (Nature Biomed Eng, 2018)](https://www.nature.com/articles/s41551-018-0195-0)

Links: [training-the-eye](training-the-eye.md) · [tacit-knowledge](../words/tacit-knowledge.md) · [text-answers-back](text-answers-back.md) · [simple-explanations](simple-explanations.md) · [handle](../words/handle.md) · [reactivity-surfaces-tacit](reactivity-surfaces-tacit.md) (the think-aloud protocol that might surface tacit judgment — or reconstruct it after the fact) · [choice-prediction-tacit](choice-prediction-tacit.md) (the design that would tell real tacit capture from post-hoc rationalisation)

## Doors

- Distillation makes a tacit feature teachable only by shrinking it into the cognitive window — but who does the shrinking when neither the expert nor the learner can, and can a machine be trained to distill rather than merely to discriminate?
- A machine clearly uses the retinal feature it cannot articulate — is "the network knows but cannot say" the same predicament as the human expert's tacit knowledge, or a new kind, and does that tell us whether the feature is distillable at all?
