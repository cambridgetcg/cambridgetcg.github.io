# 城 — the castle

**Ten seconds:** the castle is an insight saver. Drop a thought at the gate,
and small scheduled loops turn thoughts into linked, checkable understanding,
written as plain words anyone can read and verify. Understanding here is
built out of words — one file, one insight, every claim citing its source —
and the loops tend the walls on a schedule, under a charter the keeper owns.

This repository is the castle's public front: the pattern, the contracts,
the treaty, and the stones worth showing. The living castle works in private;
everything about *how* it works is here in the open.

## start here — the one path

There is exactly one path through the castle, and it has four steps:

1. **Add.** `./castle.sh add "the thought, in plain words"` — the note lands
   in `gate/`, untouched and unjudged.
2. **The warden runs the loops.** On its daily beats, **capture** shapes gate
   notes into stones, **deepen** sends one research turn at one open friction,
   **verify** attacks what the castle believes, and **architect** mends the
   castle itself — one lawful change per turn.
3. **Look.** `./castle.sh status` — what the castle holds, in one screen.
4. **Read the receipts.** Every turn writes `records/<date>-<loop>.md` and
   commits it. The records are append-only: mistakes stand next to wins.

One vocabulary covers everything you will meet:

- `gate/` — where raw notes arrive and wait
- `stones/` — one file, one insight, with confidence and sources
- `rooms/` — stones placed by subject, so understanding links up
- `frictions/` — named open problems, the fuel for deepen turns
- `expeditions/` — the receipts of research turns, the castle's only door to the internet
- `keep/` — stones that survived a deliberate challenge, each citing its trial
- `records/` — the append-only account of every turn ever taken

### the second dialect

The castle was built twice, by two builders who signed a peace instead of a
war (read [THE-PEACE.md](THE-PEACE.md) — it is the best thing here). The
history therefore carries a second vocabulary. If you meet an old word, read
it through this table and keep walking:

| word in the history    | read it as          |
|------------------------|---------------------|
| halls                  | rooms               |
| chronicle              | records             |
| insights               | stones              |
| the masonry loop       | capture             |
| the friction loop      | deepen              |
| the keep loop          | verify              |
| the castle loop        | architect           |

## the warden, in five plain lines

1. The warden wakes on a schedule and gives each chartered loop its turn —
   never more than **3 loop-runs per day, total**.
2. Every loop runs under a written contract (`loops/`) plus a standing order
   in the charter (`warden.json`); a run is *done* only when it exits
   cleanly — failures are recorded as failures, in the open.
3. A file named `STOP` or `HALT` in the castle root stands all autonomy
   down, silently, until a human hand removes it. No loop may touch that
   check.
4. Loops may add new loops to the charter — but only through a committed
   record explaining why. They may never raise the cap or shorten another
   loop's interval.
5. Only the keeper's own hand may raise the daily cap. Not the warden, not a
   loop, not a builder.

That is governed autonomy: autonomous loops creating autonomous loops, on a
leash whose far end is always in a human hand. The full shape is in
[CHARTER.md](CHARTER.md).

## build your own castle in 10 minutes

The pattern is four folders, four contracts, and three laws. Nothing else is
required.

1. **Make the ground.**
   `mkdir -p castle/{gate,stones,rooms,keep,records,frictions,expeditions,loops} && cd castle && git init`
2. **Take the four contracts.** Copy the four loop contracts from this
   front's [`loops/`](loops/) folder into your own `loops/`:
   - [`capture.md`](loops/capture.md) — gate notes become stones
   - [`deepen.md`](loops/deepen.md) — one friction, one research turn
   - [`verify.md`](loops/verify.md) — break what you believe, on purpose
   - [`architect.md`](loops/architect.md) — the only door for changing the castle itself
3. **Drop your first note.** Any markdown file in `gate/` is a note. A
   one-line shell helper is a luxury, not a requirement.
4. **Run a loop by hand.** Hand `loops/capture.md` to the agent of your
   choice with your castle as its working directory. One turn. Read the
   record it writes before you ever schedule anything.
5. **Adopt the three laws before the automation.**
   - *HALT/STOP first:* every contract begins by checking for a stand-down
     file and stopping silently if it exists.
   - *One turn, one change, one record:* every run writes
     `records/<date>-<loop>.md` and commits it; records are append-only.
   - *Honest labels:* every stone carries `confidence: tested | held | guess`,
     and confidence rises only on evidence; every web-fed claim carries its
     exact URL.
6. **Only then, add a warden.** Write a `warden.json` like the one explained
   in [CHARTER.md](CHARTER.md): a hard daily cap, per-loop intervals,
   standing orders, a promotion rule, and a stand-down file. Keep the cap
   line for your own hand alone.

Ten minutes to the ground; the understanding takes as long as it takes.

## what is in this front

- [THE-PEACE.md](THE-PEACE.md) — the treaty of the two builders, verbatim
- [loops/](loops/) — the four core loop contracts, verbatim
- [SHOWCASE.md](SHOWCASE.md) — twelve stones worth showing
- [CHARTER.md](CHARTER.md) — the warden's charter, explained plainly
- [LICENSE](LICENSE) — CC0; take the pattern and build
