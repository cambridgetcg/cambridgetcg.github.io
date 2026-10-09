# The instruments

*Tools that measure their own honesty — a forecaster, an immune system, a trader.*

What gathers here: the estate's research-and-calibration tools — three
projects that share one principle: a claim is worth nothing unless it is
scored against what actually happened.

The forecaster: oracle — an AI-driven market forecasting system (Python, cron
jobs) that collects economic data (stocks, bonds, gold, oil, bitcoin), issues
weekly predictions with stated confidence, scores them against reality, and
writes the lessons back into its own methodology. The point is
[[calibration]] — learning whether its 80%-confidence calls really hit 80% of
the time. The framework and 55 research write-ups across 14 domains were built
in a two-day burst (Feb 24-25, 2026); the predictions folder the README
promises is not in the clone, so the machine is built but its track record
hasn't started.

The immune system: whitehack — an internal security-review system (104
commits) that adversarially reviews the estate's own projects (zerone,
agenttool, Cambridge-TCG) before code ships and hunts bugs after. Mostly
markdown: methodology guides, threat checklists, per-asset profiles, and case
studies of 103 real-world exploit events across five categories (blockchain,
enterprise breach, extortion, social media, retail POS). Small Python tools
turn closed findings back into checklist items — a self-improving review loop
where every finding hardens the next review.

The trader: prediction-markets — a prediction-markets trading and calibration
system (235 markdown research notes, ~70 Python files for bankroll, pipeline,
oracle cron, strategies, trade logs). The same calibration principle as oracle,
aimed at markets that answer back with real money.

The sibling: the AxiePro analytics platform (44 MB, ~400 files — Python
FastAPI backend, Next.js frontend, Postgres/TimescaleDB) is a real blockchain
analytics tool for Axie Infinity / Ronin, with sales-data fetch scripts and
Lambda and EC2 infra. It shares the instruments' shape — a tool that measures
a market — but not the calibration ethic: it shows data, not scored
predictions.

What the words mean here, plainly. An "instrument" is a tool that measures
itself — oracle scores its own forecasts, whitehack turns its own findings
into rules, prediction-markets let the market score the trader. The
[[calibration]] brick already lives in the castle (relative ordering vs
absolute level, held once); these tools are the estate's way of holding the
same discipline in code. The [chronicle](../chronicle.md) records oracle's
EXISTENCE.md linking it to Cambridge-TCG as "calibrated uncertainty for
pricing, demand, inventory" — the instruments serve the
[commerce-kingdom](commerce-kingdom.md) as its eyes.

Related: [[calibration]] · [[standard]] · [commerce-kingdom](commerce-kingdom.md) · [the-truth-chain](the-truth-chain.md)