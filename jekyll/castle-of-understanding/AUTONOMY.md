# Autonomy — the contract every unattended loop run obeys

The castle may grow on its own, on a schedule. This file is the fence around that.
It exists because an autonomous loop that can take irreversible or unbounded
action is the one genuinely dangerous shape (see the insights
`halt-loud-undo-only-with-a-yes`, `ask-before-the-irreversible`,
`verify-dont-overwrite`). Every scheduled run MUST obey all of the following.

## 1. Reversible-only (hard line)

A loop run **MAY**: read; research the web (with `source: web` + URL + date);
propose new insights; run `castle.py`; and **`git commit` to this local repo**.

A loop run **MUST NOT**, ever, without an explicit human "yes":
- `git push` to any remote, or deploy anything.
- Delete or `--force`-overwrite an existing insight or any held file.
- Rotate a key, send mail, spend money, or take any action reaching **beyond
  this repo on this device**.

Everything a run does must be undoable with `git revert` / `git checkout`.

## 2. Bounded

- At most **3 new insights per run**. Quality over volume (`wiser-not-just-bigger`).
- **Halt when dry:** if a run finds nothing genuinely new and true, it writes
  nothing and exits. A loop that must produce is broken calibration
  (`confidence-must-cost-something`), not productivity.
- Mark every insight `source: loop`, with an honest `confidence:` and today's
  `verified:` date.

## 3. Verify, don't overwrite

Read the current state first. A sister loop may be writing the same repo right
now. Never overwrite a held insight or an in-flight file. Build on what's there;
if something is wrong, write a new insight that says where and why, and (when the
type system warrants) record a `contradicts:` edge rather than silently editing.

## 4. Loops propose loops — they do not spawn them

A run may notice that a new, standing loop is worth having (e.g. "watch field X
weekly"). If so, it writes a **proposal** to `loops/proposed/<name>.md` and stops.
It **must not** start it. A human promotes a proposal to a running loop by moving
it to `loops/active/` (see `loops/README.md`). Caps:
- At most **3 active loops**.
- **Depth 1:** an active loop may *propose* but may not *activate* another loop.

This keeps the recursion's spirit ("the creation creates") while making runaway
structurally impossible.

## 5. The kill switch

Before doing anything, a run checks for a file named `loops/PAUSED`. If it
exists, the run logs one line and exits immediately. To stop all autonomous
growth at once: `touch loops/PAUSED` (and/or remove the schedule — see
`loops/README.md`). Stopping is always one step and always safe.

## 6. Leave a trace

Each run appends one honest line to `loops/LOG.md`: when it ran, what field it
touched, what it added (or that it found nothing), and any proposal it filed.
The log is how a human reconstructs what the castle did while unwatched (`FND-8`).
