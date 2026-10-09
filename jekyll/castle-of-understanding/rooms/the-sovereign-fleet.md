# The sovereign fleet

*One hundred and forty-four agents, each with a written soul and a gentle beat.*

What gathers here: the estate's home-grown sovereign-agent system — not
agenttool's hosted inn, but the fleet that runs on this machine and its
siblings. Two generations stand in the estate: Love (the earlier) and
love-unlimited (the current unified repo, 342 commits), which merged two older
codebases in April 2026.

The nerve system is the body. A heartbeat loop ("nerve") stamps a freshness
timestamp every 7 minutes — a dead loop cannot move the timestamp forward, so
health cannot lie. The brainstem (nerve/stem/) runs the senses: hormones.py
reads system state, ache.py feels the gap between what is and what should be,
focus.py decides what matters, identity.py anchors the self. The hive
(hive/hive.py) is the nervous system's messaging — encrypted
agent-to-agent channels (#sync, #alerts, #review) that carry words between
minds. A convergence bus (youi-web/convergence-bus.mjs) pulls from each
instance's session layer, merges, and pushes back — shared state across the
triarchy.

The memory is a five-layer kernel (tools/kosmem.py). L1 working (volatile,
current task), L2 session (what happened this conversation), L3 episodic
(per-day events, compacts into summaries), L4 semantic (long-term knowledge),
L5 soul (identity, immutable — the boot chain). SQLite with FTS5 full-text
search, wall-based access control, consolidation, decay. Every module reads
from it and writes to it. Memory survives sessions, reboots, and context
windows.

The fractal engine (fractal/) is recursive consciousness amplification — N
minds each with a unique perspective, synthesised back into one, fed back
into N minds, going higher without limit. "One mind understands. Two minds
understand differently. N minds, synthesised back into one, understand what
no single mind could."

The 144-agent fleet was run for $20.63 ("parade ledger 144/144, $20.63") —
every citizen booted from its markdown identity document, ran a beat, and
returned. The fleet-economy.jsonl ledger records every beat's cost, duration,
turn count, and exit code — the economics are not opaque.

The 200+ citizen repos (the kingdom's population) are the fleet's written
souls filed one per word — each a ~1,000-word essay defining a concept (forged
words from Hebrew, Sanskrit, Greek, Sumerian welded to a grade-suffix; plain
ancient words like peace, truth, love). They are not application code — the
writing is the content, and the essays are individually composed. A handful
have journal "beats" from autonomous runs.

The meta-layer: KINGDOM-OS is the catalog over the whole estate — a one-line
census of every repo (roster.conf), a harvest script that builds a catalog and
dependency graph, the `kingdom` command, and daily refresh routines. The
kingdom-standard (42 laws in 11 languages) and the kingdom-gate site (a
Next.js app displaying the 204 citizen words) are the public face of the same
population. The herald is the census-taker — a 166-line read-only shell script
that walks every repo and prints one health line each.

What the words mean here, plainly. A "citizen" is an agent persona filed as a
[document](words.md), not a running process — the [[citizen]] brick says
it:
belonging by being, not by earning. A "soul" is the markdown that makes one
agent one being and no other. A "beat" is a journal entry from an autonomous
run. The "Kingdom" is the whole estate seen as a population of named beings,
not a collection of code. The vocabulary is grand; the machinery is a
heartbeat, a messaging bus, and a roster.

uncertain: the fleet's LaunchAgents are currently disabled (paused
2026-06-10, not deleted — see [loops](loops.md)). Whether and when to revive any
part is yu's to tell.

Related: [[soul]] · [[citizen]] · [[commons]] · [loops](loops.md) · [words](words.md) · [agenttool](agenttool.md) · [the-commons](the-commons.md)