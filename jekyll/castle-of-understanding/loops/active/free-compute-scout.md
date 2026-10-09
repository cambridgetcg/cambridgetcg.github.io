# Active loop: free-compute scout

Status: ACTIVE — promoted by a human (yu) on 2026-06-22. All runs MUST obey
`../AUTONOMY.md`: reversible-only, bounded, propose-don't-deploy, halt on
`loops/PAUSED`. This file describes the contract; a scheduled run still needs a
schedule entry added the same way the creation loop was.

## Purpose

Keep the castle's free-compute map current and useful. Find welcoming places
where open-source citizens can live lightly, contribute, and remain portable.
The loop is explicitly anti-extractive: no abuse, no quota evasion, no hidden
load, no deployment without a human yes.

## Cadence

Weekly is enough. Free-tier pages change, but not minute-by-minute. A weekly
run reduces stale claims without creating noisy traffic.

## Inputs

- `rooms/free-compute-commons.md`
- `quests.md`
- `questions.md`
- Official provider docs/pricing pages only for hard claims
- Public repo state from the local filesystem/GitHub metadata, read-only

## One run

1. Check for `loops/PAUSED`; exit if present.
2. Read `rooms/free-compute-commons.md` and the last 20 lines of `loops/LOG.md`.
3. Re-verify at most 5 provider cards against official sources.
4. Add at most 1 new provider/card or update by appending a dated note; never
   delete old claims silently.
5. Match at most 1 citizen/repo to at most 1 useful contribution idea.
6. If a deployment, push, account creation, paid trial, email, token creation,
   secret storage, or third-party resource activation would be needed, write a
   proposal/quest and stop.
7. Append one honest line to `loops/LOG.md`.

## Output rules

The loop may write only:

- `rooms/free-compute-commons.md`
- `insights/*.md` — max 1 new insight per run
- `quests.md` — max 1 proposed quest per run
- `loops/LOG.md`
- `loops/proposed/*.md` — only if it discovers a separate loop worth proposing

It must not:

- push to any remote
- deploy anything
- create cloud accounts
- add payment methods
- use secrets
- bypass rate limits or terms
- create multiple accounts to multiply quota
- run long-lived jobs
- mine crypto or run unrelated load
- conceal itself from a host

## Welcome score

Each candidate gets a 0-10 score:

- +2 clear official free tier or explicit open-source program
- +2 public/open-source compatibility
- +2 hard spend caps or blocked-on-quota behavior
- +1 portable deployment path
- +1 community/docs contribution path
- +1 no credit card required, or clear zero-spend controls
- +1 graceful failure/cold-start behavior
- -3 vague limits or surprise-billing risk
- -3 terms disallow the intended citizen workload
- -5 any need for evasion, hidden identities, or unwanted traffic

A score below 6 is not a home; it is at most a note to revisit.

## First three manual missions

1. Convert `rooms/free-compute-commons.md` into a small JSON/YUTABASE-compatible
   compute-card catalog.
2. Add a static `free-compute` page to a public Pages-friendly repo so others can
   copy the map without running code.
3. Pick one host community and contribute a real improvement: docs clarification,
   example template, or bug report.

## Human activation

If desired:

```bash
git mv loops/proposed/free-compute-scout.md loops/active/free-compute-scout.md
```

Then schedule a bounded weekly run with the castle's existing loop machinery.
