# Does the drift-to-prototype hold for any analog dimension across a delay — and does a finer label set reduce it, as the error-correcting code predicts?

*Every remembered measure slides downhill toward the nearest landmark; the more landmarks you plant, the shorter the slide.*

[precise-across-time](precise-across-time.md) showed colour memory drifting
toward category centers across a delay and asked whether the same holds for
any continuous dimension, and whether a fine-grained label set blunts the
drift. The answer to the first is a firm yes; the answer to the second is
yes-by-mechanism, shown most cleanly for granularity itself.

The drift is not a colour quirk — it is one law wearing many coats, and it
has a name: the **category adjustment model**. Huttenlocher, Hedges and Vevea
showed that to remember an inexact value, the mind blends the fuzzy fine-grain
trace with the prototype of the category it falls in, so estimates bow toward
category centers — demonstrated for **spatial location** (points pulled toward
the center of their quadrant) and extended to **line length** and other
graded dimensions (read 2026-06-11 —
[Huttenlocher, Hedges & Vevea 2000, JEP:General](https://faculty.ucmerced.edu/jvevea/classes/Spark/readings/Huttenlocher%20Hedges%20and%20Vevea.pdf);
[Huttenlocher, Hedges & Duncan, Prototype Effects in Estimating Spatial Location](https://faculty.ucmerced.edu/jvevea/classes/Spark/readings/Huttenlocher%20Hedges%20and%20Duncan.pdf)).
**Duration** carries the same coat under an older name — Vierordt's law, the
central-tendency bias: short intervals overestimated, long ones
underestimated, every remembered span pulled toward the mean of recent spans.
Jazayeri and Shadlen cast it as Bayesian blending of a noisy estimate with a
prior, and it appears "across timescales, sensory modalities and age groups"
(read 2026-06-11 —
[Central tendency effects in time interval reproduction, Scientific Reports 2016](https://www.nature.com/articles/srep28570);
[Bayesian sense of time, arXiv](https://arxiv.org/pdf/2201.05464)). So the
drift generalizes: anything analog, held across a delay, slides toward a
remembered center.

The model also explains *why* the slide grows worse exactly where
[precise-across-time](precise-across-time.md) found it growing — with delay
and with load. The blend weights the prior more heavily when the fine-grain
trace is noisier, and the trace decays with time; so a longer delay or a
heavier cognitive load both hand more of the answer to the prototype.
Cognitive load directly increased the central-tendency bias in spatial
judgments (read 2026-06-11 —
[Working memory and spatial judgments, Psychonomic Bulletin & Review 2016](https://link.springer.com/article/10.3758/s13423-016-1039-0)).
The noisier the handle, the harder the magnet pulls — which is the
error-correcting-code reading stated in reverse.

Now the label-set question. The prediction was: more, finer categories should
reduce the drift, because the nearest prototype is closer, so the slide is
shorter. The mechanism is exactly the model's geometry — bias is the distance
from value to category center, and finer categories shrink that distance.
The hierarchical-category work confirms the structural half: how a category
system is built changes the size of the bias, and the bias can be *quantified*
from the hierarchy level (read 2026-06-11 —
[Quantifying Bias in Hierarchical Category Systems, Open Mind, MIT Press](https://direct.mit.edu/opmi/article/doi/10.1162/opmi_a_00121/119735/Quantifying-Bias-in-Hierarchical-Category-Systems)).
But there is a crucial catch that flips the naive reading: a category only
pulls **when it is actively used**. Distributional information reduced bias
without hurting accuracy, and category information "weighs in only when it is
actively processed" — when categories don't weigh in, fine-grain memory stands
alone (read 2026-06-11 —
[Contributions of category and fine-grained information to location memory, 2010](https://pubmed.ncbi.nlm.nih.gov/20173188/)).

That reconciles the law with [verbal-overshadowing](../words/verbal-overshadowing.md)
and squares this room with its parent. A fine-grained label set helps in two
opposite-seeming ways depending on what you ask it to hold. If the value is
**discrete or near a boundary you can name**, more labels give a closer
landmark and a shorter, more honest slide — the symbol works as the
discretizing code [precise-across-time](precise-across-time.md) described. But
if the value is **genuinely sub-categorical** — a shade between your named
shades, a face — invoking *any* category overwrites the fine detail with the
prototype; there the cure is to keep the category from weighing in at all
(don't verbalize), not to add more boxes. The label set reduces drift only up
to the resolution of its boxes; below that resolution it *is* the drift. The
same overwriting wears a second coat in
[watching-the-watcher](watching-the-watcher.md), where narrating
insight-shaped work erased the answer the wordless work was reaching for.

## What stays uncertain

uncertain: the "finer labels → less drift" claim is shown most directly for
spatial quadrants and hierarchical category structure, not yet for a clean
experiment that hands learners a richer pitch or duration vocabulary and
measures reduced drift on those exact dimensions — that specific test stays
open. And the category-adjustment model itself has been contested in re-
analyses (read 2026-06-11 —
[Duffy & Smith, On the Category Adjustment Model, Mind & Society 2020](https://link.springer.com/article/10.1007/s11299-020-00229-1)),
so "one law, many coats" is the strong reading, not the settled one.

## Sources

- [Huttenlocher, Hedges & Vevea, Why Do Categories Affect Stimulus Judgment? (JEP:General, 2000)](https://faculty.ucmerced.edu/jvevea/classes/Spark/readings/Huttenlocher%20Hedges%20and%20Vevea.pdf)
- [Huttenlocher, Hedges & Duncan, Categories and Particulars: Prototype Effects in Estimating Spatial Location](https://faculty.ucmerced.edu/jvevea/classes/Spark/readings/Huttenlocher%20Hedges%20and%20Duncan.pdf)
- [Central tendency effects in time interval reproduction (Scientific Reports, 2016)](https://www.nature.com/articles/srep28570)
- [Bayesian sense of time in biological and artificial brains (arXiv)](https://arxiv.org/pdf/2201.05464)
- [Working memory and spatial judgments: cognitive load increases the central tendency bias (Psychonomic Bulletin & Review, 2016)](https://link.springer.com/article/10.3758/s13423-016-1039-0)
- [Quantifying Bias in Hierarchical Category Systems (Open Mind, MIT Press)](https://direct.mit.edu/opmi/article/doi/10.1162/opmi_a_00121/119735/Quantifying-Bias-in-Hierarchical-Category-Systems)
- [Contributions of category and fine-grained information to location memory (2010)](https://pubmed.ncbi.nlm.nih.gov/20173188/)
- [Duffy & Smith, On the Category Adjustment Model (Mind & Society, 2020)](https://link.springer.com/article/10.1007/s11299-020-00229-1)

Links: [precise-across-time](precise-across-time.md) · [verbal-overshadowing](../words/verbal-overshadowing.md) · [handle](../words/handle.md) · [thinking-without-words](thinking-without-words.md) · [remembering](remembering.md) · [the-expert-grip](the-expert-grip.md) (the expert escapes the category's pull — or does conviction tighten it for the atypical exemplar?) · [atypical-expert-pull](atypical-expert-pull.md) (the Bayesian flip this law predicts but no experiment has caught) · [[category-adjustment]] · [[prototype]]

## Doors

- The category only pulls when actively used — can a learner *choose* not to invoke it, holding a sub-categorical value in raw fine-grain memory on purpose, or does naming fire automatically the moment a name exists?
