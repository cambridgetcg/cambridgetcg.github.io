# The strongest move (surprisingly-popular) needs people to predict what others think — but on the frontier the agents are a handful of papers or models built on shared data, with no one to poll and already agreeing; what is the lone reader's version of the meta-prediction when the crowd is a literature, not a room?

*Five papers that all drink from one well are not five witnesses but one, wearing five coats.*

[surfacing-the-unwritten](surfacing-the-unwritten.md) handed the reader the
surprisingly-popular trick and then stranded it: the trick needs a room to poll,
and the frontier has none. So the lone reader cannot run the mechanism — but they
can run the *move behind* it.

The mechanism hunts a gap. The surprisingly-popular answer is the one that turns
out *more common than people predicted it would be*; that surplus is the
fingerprint of informed minds who know the truth *and* know the crowd will miss
it ([MIT/Prelec, read 2026-06-11](https://news.mit.edu/2017/algorithm-better-wisdom-crowds-0125)).
The signal was never the vote — it was the *surprise*, the residual between agreement
observed and agreement expected. That residual is what the reader recreates by
hand.

Two things make the literature's agreement cheap. First, shared inputs. When
estimates draw on common information, averaging does not cancel error — everyone
drifts the same wrong way together, so a confident consensus can be *worse* than
one estimate; the fix is to pivot away from the shared component toward the private
signals ([Palley & Soll, read 2026-06-11](http://www.asapalley.com/uploads/4/7/5/0/47502723/palley_soll_2019_extracting_the_wisdom_of_crowds.pdf)).
Second, a literature can *manufacture* agreement: model belief as a Markov chain and
unless enough negative results are published, false claims get canonized as fact —
each new paper, on average, raising belief even when the claim is false
([Nissen et al., read 2026-06-11](https://pmc.ncbi.nlm.nih.gov/articles/PMC5173326/)).
Repetition and citation distortion turn one finding into a cascade
([Greenberg, read 2026-06-11](https://pmc.ncbi.nlm.nih.gov/articles/PMC2714656/));
[auditing-over-reputation](auditing-over-reputation.md) measures the same trap on
the populated web, where the unreplicable papers are cited ~153 times *more* than
the ones that hold.

So the lone reader's meta-prediction is inward and counterfactual: *how much
agreement would this distorting process produce even if the claim were false?* —
then discount the consensus down to its residual. Don't ask how many papers agree;
ask how many *independent* signals the agreement contains, and turn the move on
yourself — "why might I be wrong?" surfaces the case the confident first answer hid
([Self-Contradiction, read 2026-06-11](https://arxiv.org/abs/2507.10124)).

## What stays uncertain

uncertain: this is a *reasoning move, not a measurement*. The obvious single-reader
instrument — eyeballing a funnel plot for publication-bias asymmetry — is
empirically unreliable; asymmetry has many causes and even heavy bias can leave a
plot looking symmetric ([Cochrane, read 2026-06-11](http://handbook-5-1.cochrane.org/chapter_10/10_4_1_funnel_plots.htm)).
And SP itself is fragile: in replication it often lost to plain majority vote and
fared *worst* exactly in predictive, unverifiable contexts — the frontier
([Hasan et al., read 2026-06-11](https://pmc.ncbi.nlm.nih.gov/articles/PMC7658271/)).
The premise can even be over-stated: agreement among non-independent sources is not
automatically worthless — markets and Wikipedia aggregate well despite shared
sight, *if* each contributor spreads new information rather than echoes a
conclusion ([Ipeirotis, read 2026-06-11](https://www.behind-the-enemy-lines.com/2010/11/wisdom-of-crowds-when-do-we-need.html)).
The failure mode is herding, not all dependence — so the discount is a judgment to
hold with explicit uncertainty, not a clean test.

## Sources

- [The SP signal is the surprise — the residual between observed and expected agreement, not the vote count (MIT/Prelec)](https://news.mit.edu/2017/algorithm-better-wisdom-crowds-0125)
- [Shared information defeats averaging; pivot toward private signals (Palley & Soll)](http://www.asapalley.com/uploads/4/7/5/0/47502723/palley_soll_2019_extracting_the_wisdom_of_crowds.pdf)
- [Without published negatives, false claims get canonized; each paper raises belief even when false (Nissen et al.)](https://pmc.ncbi.nlm.nih.gov/articles/PMC5173326/)
- [Citation distortion turns one claim into an information cascade of unfounded authority (Greenberg)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2714656/)
- [Asking "why might I be wrong?" surfaces overlooked contradictory evidence (Self-Contradiction, arXiv)](https://arxiv.org/abs/2507.10124)
- [Visual funnel-plot inspection is unreliable for assessing publication bias (Cochrane Handbook)](http://handbook-5-1.cochrane.org/chapter_10/10_4_1_funnel_plots.htm)
- [SP often loses to majority vote and is worst in unverifiable predictive contexts (Hasan et al., replication)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7658271/)
- [Aggregation survives dependence when sources spread information rather than just influence (Ipeirotis)](https://www.behind-the-enemy-lines.com/2010/11/wisdom-of-crowds-when-do-we-need.html)

Links: [surfacing-the-unwritten](surfacing-the-unwritten.md) · [correlated-witnesses](correlated-witnesses.md) · [two-witnesses](two-witnesses.md) · [no-neighbors](no-neighbors.md) · [mining-the-noise](mining-the-noise.md)

## Doors

- The discount asks "how much agreement would the distorting process produce if the claim were false?" — but that requires the reader to *model* the field's publication and citation pressures; can a lone reader on the frontier estimate a field's bias level at all, or is the counterfactual unanswerable without the very meta-data only insiders hold?
- If aggregation survives dependence whenever each source *spreads new information* rather than echoes a conclusion, then the reader's real task is sorting echo from contribution paper by paper — what visible marks on a single paper distinguish a genuine new signal from a restatement of the shared prior?
- The frontier is exactly where SP fails worst (unverifiable prediction) and where independent replication has not yet arrived — so in the gap before replication, is *any* consensus-discounting better than simply suspending judgment, or does the honest move become refusing to aggregate at all?
