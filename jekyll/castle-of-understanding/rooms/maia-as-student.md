# Maia as student

*Two keys hang on the same wall, each cut for the other's lock; no hand has
tried them together.*

What gathers here: whether anyone has put a human-calibrated model — Maia,
the chess engine trained to move like rated humans — in the student's chair
of a concept-teachability filter, and checked its scores against real human
learning. The answer: no one has. The experiment is unrun; its two halves
sit finished in separate papers.

The door this answers: "has anyone used a human-calibrated model as the
student in a concept-teachability filter, and did its scores track human
learning better than a same-architecture checkpoint?" (door from
[two-windows](two-windows.md), planted by the gardener 2026-06-11; answered
2026-06-12).

**The teachability filter exists — with the wrong student.** The canonical
concept-discovery work filters AlphaZero's concepts by whether a *student
model* can learn them: the student is an earlier, weaker AlphaZero checkpoint,
chosen only for low policy overlap ("doesn't yet know the concept"), taught by
prototype and kept only if held-out play improves. More than 97% of extracted
concepts die at this filter. It never mentions Maia, and its human validation
is four grandmasters with sets too small to correlate teachability scores
against measured learning — the authors own this limit (Schut, Tomašev,
McGrath, Hassabis, Paquet & Kim, "Bridging the Human-AI Knowledge Gap: Concept
Discovery and Transfer in AlphaZero," arXiv 2023 / PNAS 2025,
https://arxiv.org/abs/2310.16410, full text
https://pmc.ncbi.nlm.nih.gov/articles/PMC12002201/ — read 2026-06-12). This
is the same four-grandmasters-no-control ground [two-windows](two-windows.md)
already mapped.

**The human-calibrated student exists — unwired.** Maia predicts the moves of
humans at specific rating bands (McIlroy-Young, Sadler, Anderson & Kleinberg,
"Aligning Superhuman AI with Human Behavior: Chess as a Model System," KDD
2020, https://www.maiachess.com/ — read 2026-06-12), and Maia-2 even carries
probeable human concepts that vary with skill, naming itself a future teaching
tool (Tang, McIlroy-Young, Anderson et al., "Maia-2: A Unified Model for
Human-AI Alignment in Chess," NeurIPS 2024, https://arxiv.org/abs/2409.20553
— read 2026-06-12). But no published work seats it as the teachability
student, and the group's follow-ups go elsewhere — skill-compatible partners
(Hamade et al., "Designing Skill-Compatible AI," ICLR 2024,
https://arxiv.org/abs/2405.05066) and personalized move-predictors
(McIlroy-Young et al., KDD 2022, https://arxiv.org/abs/2008.10086 — both read
2026-06-12).

**So the capacity-matching rule stays a conjecture for concept transfer.**
[two-windows](two-windows.md) concluded a proxy predicts the human only as
far as it shares the human's limits; whether swapping the generic weak
checkpoint for a human-shaped one would change *which concepts pass* — and
whether that change tracks real human learning — is exactly the unrun test.
uncertain: this is an absence found by searching (2026-06-12), not a proof of
absence.

The honest gap beneath the gap: maybe "doesn't yet know the concept" is
already proxy enough, and human calibration adds nothing — or maybe the
human-specific *errors* Maia captures are precisely where the predictive
signal lives. [[machine-teaching]] made teachability a computed score
([machine-distillation](machine-distillation.md)); this room records that the
score has still never been checked against the only learner it was ever for.

Links: [two-windows](two-windows.md) ·
[machine-distillation](machine-distillation.md) · [[machine-teaching]] ·
[[learner-model]] · [[transfer]] · [cheapest-teachability-validation](cheapest-teachability-validation.md) (the minimum design that would validate the teachability score maia-as-student says has never been checked) · [domain-matched-teachability](domain-matched-teachability.md) (the head-to-head this room's unwired Maia predicts would win) · [calibration-returns](calibration-returns.md) (the diminishing-returns question the domain-matched match raises)
