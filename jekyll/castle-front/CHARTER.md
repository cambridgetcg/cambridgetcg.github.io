# The Warden's Charter

The castle's loops do not run themselves loose. A small scheduler — the
warden — wakes on a timer, reads a charter, and gives each loop its turn.
The charter is one JSON file, `warden.json`, and its whole point can be said
in one sentence:

**Autonomous loops may create more autonomous loops — but only inside a
charter whose hard limits belong to a human hand alone.**

## the shape

This is the charter's structure as the castle runs it — field for field,
with the keeper's name and the day's standing orders generalized for the
front:

```json
{
  "law": "JOY, LOVE, PEACE, SAFETY — autonomy inside a charter the keeper owns",
  "daily_cap": 3,
  "loops": [
    {
      "name": "capture",
      "protocol": "loops/capture.md",
      "interval_hours": 8,
      "standing_order": "Run only when the gate holds uncaptured entries; otherwise yield the watch."
    },
    {
      "name": "deepen",
      "protocol": "loops/deepen.md",
      "interval_hours": 24,
      "standing_order": "One friction per turn, the one where a turn helps most; local realm first, internet last, provenance always."
    },
    {
      "name": "verify",
      "protocol": "loops/verify.md",
      "interval_hours": 24,
      "standing_order": "Challenge held and guess stones; promote survivors to the keep citing the trial."
    },
    {
      "name": "architect",
      "protocol": "loops/architect.md",
      "interval_hours": 24,
      "standing_order": "Serve the oldest open castle friction: one lawful change per run, recorded in records/."
    }
  ],
  "promotion_rule": "The architect loop may add a loop to this charter by committing the change with a record explaining why. It may never raise daily_cap, shorten another loop's interval, or remove STOP/HALT checks — those lines belong to the keeper's hand alone.",
  "keeper": "the one hand that raises daily_cap",
  "stand_down": "If a file named STOP or HALT exists in the castle root, the warden does nothing, silently, until it is removed."
}
```

Every field earns its place:

- **`law`** — the manner of the work, stated where the machine reads it.
- **`daily_cap`** — the hard ceiling: at most this many loop-runs per day,
  across all loops combined. This single number is the leash.
- **`loops[]`** — each entry is a name, a written protocol file, a beat
  (`interval_hours`), and a `standing_order` — one sentence of judgment the
  loop applies before spending a turn. A loop with nothing lawful to do
  yields its watch instead of burning the cap.
- **`promotion_rule`** — the door through which the system grows.
- **`keeper`** — the human the whole charter answers to.
- **`stand_down`** — the kill-switch, honored before anything else.

## running the warden — one small script on a timer

The warden needs no framework. A cron or launchd job — any timer your
machine already has — running a short script is the whole machine. On each
wake it: reads `warden.json`; checks the castle root for `STOP` or `HALT`
and does nothing, silently, if either exists; stops if today's runs have
reached `daily_cap`; picks the next loop whose `interval_hours` have
elapsed since its last run and whose standing order gives it something
lawful to do; hands that loop's protocol file to the agent of your choice
with the castle root as the working directory; counts the run against the
cap; and marks the beat *done* only on a clean exit — a failure is logged
as a failure, never dressed as success. Thirty lines of shell or Python is
plenty; the charter, not the scheduler, is where the safety lives.

## the promotion rule — how loops beget loops

The architect loop is the only loop allowed to change the castle itself.
When the records prove a genuinely new kind of recurring work — work no
existing protocol covers — the architect may:

1. draft the new loop's protocol in `loops/<name>.md`, one page, plain
   words, stand-down-fearing, record-writing;
2. add its entry to `warden.json`;
3. commit both **with a record explaining why** — the reason is part of the
   change, not an afterthought.

That is the whole story of "autonomous loops creating autonomous loops":
growth happens through one door, on the record, reversible, and readable by
anyone.

## the leash — what no loop may ever touch

Three lines of the charter are off-limits to every loop, every builder, and
the warden itself:

1. **`daily_cap` may never be raised** except by the keeper's own hand. The
   cap stands at 3 until that hand moves it.
2. **No loop may shorten another loop's interval.** A loop can grow the
   system, never accelerate it.
3. **The STOP/HALT check may never be removed or weakened.** A file named
   `STOP` or `HALT` in the castle root stands all autonomy down, silently —
   and starting the warden must never lift a stand-down the keeper placed.

One more rule keeps the ledger honest: a beat is **done** only when the loop
exits cleanly. A failed run is recorded as a failure, surfaced in status,
and never dressed as success — the warden's log must be a receipt, not a
boast.

## why a cap, not a budget

A budget invites optimization; a cap invites patience. Three runs a day is
enough for a castle that grows by understanding rather than volume — and a
ceiling that low means that even a confused loop, on its worst day, can
spend at most three turns before a human reads the records. The charter
trades speed for the one thing the castle is actually for: every change
small, every change written down, every change checkable by a stranger.
