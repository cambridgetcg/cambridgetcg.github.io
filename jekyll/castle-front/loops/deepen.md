# deepen — one friction, one expedition, stones carried home

*An open question goes out the gate; understanding comes home with receipts.*

You are inside the castle, an insight saver made of plain markdown files.
Work from the castle root — the folder that holds this `loops/` folder.
Today's date in YYYY-MM-DD form: `date +%F`.
Before anything: if a file named `HALT` or `STOP` exists in the castle root,
stop silently — do nothing and write nothing.
**This is the only loop allowed to touch the internet.**

## when to run

Run when at least one file in `frictions/` has `status: open` in its
frontmatter (the labeled block between `---` lines). If none, do not run.

## the friction shape

Every friction is one file, `frictions/<kebab-name>.md`, in exactly this
shape — every loop or hand that names a friction writes it this way:

```
---
name: <short plain name>
born: YYYY-MM-DD
room: <the room the gap belongs to; "castle" when the gap is in the castle itself>
status: open
---

What rubs: <the gap or question, one or two plain sentences>

What was tried: <"nothing yet", or one line per attempt>
```

## the steps

1. Read every `frictions/*.md` whose `status:` is `open`. If there are
   none, stop.
2. Pick exactly ONE — the oldest (earliest `born:`), unless a younger one
   would clearly unblock far more stones or a whole room; if you take the
   younger, say why in your record.
3. **Before going anywhere**, create `expeditions/<date>-<friction-name>.md`
   (`mkdir -p expeditions` if the folder does not yet exist) and write its
   header:

   ```
   # expedition: <friction-name>
   - friction served: frictions/<friction-name>.md
   - date: YYYY-MM-DD
   - question carried: <one plain sentence>
   ```

4. Search home first, in this order — the answer may already be a link away:
   - **the castle:** `stones/`, `rooms/`, `keep/`;
   - **the device:** the sibling repos beside the castle root and anything
     else this machine already holds;
   - **the internet, last**, only where home runs dry. Read three to five
     sources. For each, append under `## sources visited`: the link, and one
     or two lines of what it actually said — not what you hoped it would
     say. If sources disagree, record both sides.
5. Bring it home. For each thing learned, quarry a new stone or grow an
   existing one — the stone shape is in `loops/capture.md` step 4 — with
   `quarried-from` citing this expedition file and the exact source links.
   Label honestly: what you verified is `tested` (cite how), what a credible
   source asserts is `held`, what you merely suspect is `guess`.
6. Judge the friction honestly, and edit its file:
   - **Answered** → set `status: closed`; add a line
     `Closed: <date> — <what closed it>`.
   - **Partly answered** → keep `status: open`; rewrite `What rubs:` sharper
     than before; add what you did to `What was tried:` — so the next turn
     starts ahead of where you did.
   - **The question itself was wrong** → close it with a line saying so, and
     write the truer question as a new friction file.
7. Tend the friction's room: in `rooms/<room>/ROOM.md`, fix the
   `## open frictions` list and add any new stones under
   `## what this room knows`.
8. Finish the expedition file with `## what came home`: stones born or grown
   (named), and whether the friction closed or sharpened, and why.

## the record

Write a one-paragraph record in `records/<date>-deepen.md` — open it with
`date '+%F %H:%M'`; if the file already exists, add a `## again, later`
section, never overwrite — saying which friction was served, where the
expedition went, and what came home. Then commit in house style:

    git add -A
    git commit -m "deepen: <brief poetic clause, e.g. one question carried over the hills>"
