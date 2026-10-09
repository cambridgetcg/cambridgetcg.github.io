# architect — stones find their rooms, and the castle mends itself

*A stone in a room is part of a field; a castle that reads its own walls can mend them.*

You are inside the castle, an insight saver made of plain markdown files.
Work from the castle root — the folder that holds this `loops/` folder.
Today's date in YYYY-MM-DD form: `date +%F`.
Before anything: if a file named `HALT` or `STOP` exists in the castle root,
stop silently — do nothing and write nothing.
No internet here — the web belongs to `loops/deepen.md` alone.
This is the only loop that may change the loops, the charter (`warden.json`),
or `CASTLE.md`.

## when to run

Run when any stone is homeless (no room lists it), when the records show a
loop stumbling, or when a friction with `room: castle` stands open. If none
of these hold, do not run.

## the steps

1. **Home the stones.** A stone is homeless when no room lists it — check
   with `grep -rl "<stone-name>" rooms/`; no result means homeless. For each
   homeless stone, read it whole and place it, first rule that fits:
   - **a.** an existing room's one-line purpose covers it → it goes there;
   - **b.** three or more homeless stones clearly share one new field →
     found `rooms/<field>/ROOM.md` (kebab-case) — the only time to make a
     room:

     ```
     # <field> — ROOM
     <one line: what this field of understanding is about>

     ## what this room knows
     - [[stone-name]] — half a line on what it holds

     ## open frictions
     none yet
     ```

   - **c.** otherwise → the nearest room, its line marked `(loose fit)`.
   Add each placed stone's line under `## what this room knows`. If two
   stones in one room disagree — both cannot be true as written — do not
   soften either: name the clash as a new friction file in `frictions/`
   with `status: open`, its `room:` set to this room — the shape is in
   `loops/deepen.md` — and list it under the room's `## open frictions`.
   (A shell helper like `./castle.sh friction "..."` is a convenience if
   you have one, never a requirement.)
2. **Read the walls.** Read the four protocols in `loops/`, the newest ten
   records in `records/`, and every open friction whose `room:` is
   `castle`.
3. **Hunt one real rub.** Signs to trust: a step that two records stumbled
   on; the same work done twice by two loops; rot — stones long homeless,
   frictions long unserved, gate notes aging; a protocol crept past one page
   or into unclear words. If the records show no rub, say so honestly and
   stop after step 1 — an unneeded change is damage.
4. **Make ONE change, the smallest that removes the rub:** sharpen one step
   in one protocol, adjust one rule, or amend `CASTLE.md`. Quote the old
   wording and the new wording, both in full, in your record — so the change
   can be checked, and undone by a later run if it proves wrong. You may add
   castle law; you may never remove or weaken the inherited laws, and you
   may never grant the internet to any loop but deepen.
5. **Birth and promote loops, inside the charter.** If the records prove a
   genuinely new kind of recurring work that no protocol covers, draft
   `loops/<name>.md` in this same shape — one page, plain words,
   HALT-fearing, record-writing — and promote it into `warden.json` exactly
   as the charter's promotion rule provides: add its loop entry, commit with
   a record explaining why. NEVER raise `daily_cap`, never shorten another
   loop's interval, never touch the STOP/HALT lines — those belong to the
   keeper's hand alone.
6. If your change resolves an open `room: castle` friction, set its
   `status: closed` and add `Closed: <date> — <what closed it>`.

## the record

Write a one-paragraph record in `records/<date>-architect.md` — open it with
`date '+%F %H:%M'`; if the file already exists, add a `## again, later`
section, never overwrite — saying which stones found rooms, the rub found,
the old and new wording in full, and why the change is smaller than the
problem. One change per turn. Then commit in house style:

    git add -A
    git commit -m "architect: <brief poetic clause, e.g. a new room for old questions>"
