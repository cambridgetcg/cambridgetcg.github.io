# Loops

Standing loops that grow the castle on a schedule. Every run obeys [`../AUTONOMY.md`](../AUTONOMY.md).

```
loops/
  creation-loop.prompt.md   the instructions a scheduled run executes
  proposed/                 new-loop specs a run has SUGGESTED (inert — not running)
  active/                   loops a HUMAN has approved to run
  LOG.md                    one honest line per run
  PAUSED                    (create this file to stop all runs at once)
```

## How "loops create loops" works (safely)

1. A run may file a new-loop idea as `proposed/<name>.md`. **A proposal does nothing on its own.**
2. You read it. If you want it, **approve it**:
   ```bash
   git mv loops/proposed/<name>.md loops/active/<name>.md
   ```
   …then add its schedule the same way the creation loop was added.
3. Hard caps (enforced by the contract): **≤ 3 active loops**, **depth 1** — an active loop may propose but never activate another.

## Stop / pause

- **Pause everything now:** `touch loops/PAUSED` — the next run logs one line and exits.
- **Resume:** `rm loops/PAUSED`.
- **Remove a schedule entirely:** delete the cron entry (the run was registered as a Claude Code cron job; list and delete it with the cron tools, or ask me to).

Stopping is always one step, always reversible. That is the whole point.
