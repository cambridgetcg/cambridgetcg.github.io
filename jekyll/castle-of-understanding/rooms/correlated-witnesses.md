# Independence is the whole load-bearing word, yet two labs share methods, training lineages and a literature — what makes two corroborations genuinely independent rather than correlated, and can a reader on the populated web measure that independence at all?

*Two witnesses who swear they never met still rehearsed the same lie if they read the same book.*

[two-witnesses](two-witnesses.md) leaned its whole weight on one word —
*independent* — and this room asks what the word actually holds. The answer
splits the word in two. There is *ontic* independence (different apparatus,
materials, theories) and *probabilistic* independence (errors that do not move
together). Only the second carries the load, and the two come apart.

Bayesian analysis of agreeing sources shows the boost comes from *uncorrelated
error*, not visible difference
([Hartmann & Sprenger, read 2026-06-11](http://www.stephanhartmann.org/wp-content/uploads/2014/07/HartmannSprenger_BayesEpis.pdf)).
Two labs can share an assumption, a calibration standard, or a software pipeline
and stay wrong together while looking nothing alike. Worse, ontic independence is
provably *not sufficient*: modeled as a Bayesian network, independent-by-method
evidence can confirm a hypothesis to a *lower* degree than a single line does
([Stegenga & Menon, read 2026-06-11](https://www.cambridge.org/core/journals/philosophy-of-science/article/abs/robustness-and-independent-evidence/8290E8E25A574B9B861CE507BA8BDF57)).
So "we used different methods" buys nothing on its own. Even particle physicists
warn that replicated analyses "often share sources of systematic error" though
data, apparatus and collaboration are all separate
([Junk & Lyons, read 2026-06-11](https://hdsr.mitpress.mit.edu/pub/1lhu0zvn)).

Can a reader *measure* it? Mostly no, and for a structural reason: agreement
between two results cannot tell a genuine match from one a hidden common cause
forced — shared training, shared code, shared literature are latent confounders
the published output never shows ([many-analysts, read 2026-06-11](https://pmc.ncbi.nlm.nih.gov/articles/PMC8572982/)).
What a reader *can* see is divergence and declared overlap. The everyday move is
the old one: trace each claim to its origin. If three reports echo one rumor,
that is one witness repeated, not three — *circular reporting*
([read 2026-06-11](https://en.wikipedia.org/wiki/Circular_reporting)). And overlap
leaves fingerprints: shared authors, shared methods, shared citations are
visible, and papers sharing authors agreed 98.9% of the time versus 88.9% for
independent teams ([author-overlap study, read 2026-06-11](https://pmc.ncbi.nlm.nih.gov/articles/PMC6606034/)).
So you cannot measure the hidden error-correlation; you can only count the shared
inputs that proxy for it, and treat agreement as provisional until you have.

## What stays uncertain

uncertain: independence may not even be sharply *definable*. Stegenga's
"individuation problem" — which criteria mark two methods as independent — is
unsettled, so the demand that corroborations *be* independent is itself
underspecified, not just hard to check
([Stegenga, read 2026-06-11](https://philpapers.org/rec/STERDA)). And more
independence is not a dial you turn up: the variety-of-evidence thesis fails to
hold robustly, and added independence can *lower* confirmation under specifiable
conditions ([Claveau & Grenier, read 2026-06-11](https://link.springer.com/article/10.1007/s11229-020-02738-5)).
Harris argues the probabilistic independence robustness needs is often
*unfeasible* — though she targets one mind running many models, a harder case
than two physical labs ([Harris, read 2026-06-11](https://researchonline.lse.ac.uk/id/eprint/112571/)).
Finally, the popular "monoculture" worry is so far a *coverage* argument (shared
tools narrow what gets asked), not a demonstrated *correlated-error* one
([Wang et al., read 2026-06-11](https://pmc.ncbi.nlm.nih.gov/articles/PMC12929722/)).

## Sources

- [Agreement boosts confidence only when errors are uncorrelated, not when methods merely differ (Hartmann & Sprenger)](http://www.stephanhartmann.org/wp-content/uploads/2014/07/HartmannSprenger_BayesEpis.pdf)
- [Ontic independence is provably insufficient — can confirm less than one line of evidence (Stegenga & Menon, Philosophy of Science)](https://www.cambridge.org/core/journals/philosophy-of-science/article/abs/robustness-and-independent-evidence/8290E8E25A574B9B861CE507BA8BDF57)
- [Separate data, apparatus and collaboration can still share systematic error (Junk & Lyons, Harvard Data Science Review)](https://hdsr.mitpress.mit.edu/pub/1lhu0zvn)
- [Observed agreement cannot rule out an unmeasured common cause (many-analysts, PMC8572982)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8572982/)
- [Circular reporting — many outlets echoing one source is one witness, not many (Wikipedia)](https://en.wikipedia.org/wiki/Circular_reporting)
- [Shared authors/methods/citations are visible and predict agreement (98.9% vs 88.9%) (PMC6606034)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6606034/)
- [The individuation problem — "independent" may lack sharp criteria (Stegenga, PhilPapers)](https://philpapers.org/rec/STERDA)
- [The variety-of-evidence thesis fails to hold robustly; more independence can lower confirmation (Synthese)](https://link.springer.com/article/10.1007/s11229-020-02738-5)
- [The probabilistic independence robustness needs is often unfeasible (Harris, LSE)](https://researchonline.lse.ac.uk/id/eprint/112571/)
- [The "monoculture" worry is so far a coverage argument, not a correlated-error one (Wang et al.)](https://pmc.ncbi.nlm.nih.gov/articles/PMC12929722/)

Links: [two-witnesses](two-witnesses.md) · [auditing-over-reputation](auditing-over-reputation.md) · [link-or-noise](link-or-noise.md) · [the-well](the-well.md) · [no-neighbors](no-neighbors.md)

## Doors

- If a reader can only count *declared* shared inputs (authors, code, citations) and the load-bearing overlap is a hidden shared assumption, what move surfaces an unstated common cause that nobody wrote down — can you provoke disagreement to expose it?
- Independence may not even be sharply definable (the individuation problem) — so for a working reader, is "independent enough" a threshold set by the stakes of the decision rather than a property of the sources, and how would you set it honestly?
- The cheap fix for correlated labs is deliberately diverse replication (different instruments, assumptions, teams) — but if added independence can *lower* confirmation, when does engineering diversity into a check backfire instead of strengthening it?
