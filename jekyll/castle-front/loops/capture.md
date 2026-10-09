# capture — gate notes become stones

*Raw words from the gate, shaped into stones the castle can build with.*

You are inside the castle, an insight saver made of plain markdown files.
Work from the castle root — the folder that holds this `loops/` folder.
Today's date in YYYY-MM-DD form: `date +%F`.
Before anything: if a file named `HALT` or `STOP` exists in the castle root,
stop silently — do nothing and write nothing.
No internet here — the web belongs to `loops/deepen.md` alone.

## when to run

Run when the gate holds at least one note: an `.md` file directly inside
`gate/` (ignore the `gate/filed/` folder), or a dated `- ` line in
`gate/inbox.md` (an older door for one-line notes). If the gate is quiet,
do not run.

## the steps

1. List the notes. Each `.md` file directly in `gate/` is one note; each
   dated `- ` line in `gate/inbox.md` is one note. If there are none, stop.
2. Take one note. Read it whole. Count its distinct insights — things now
   understood that were not before: zero, one, or several. An errand, a bare
   feeling, or noise counts as zero insights; when the line is thin, say in
   your record why you judged it so.
3. For each insight, search the existing stones — one `grep -ril "<word>"
   stones/` per key word, two or three words — and read whatever returns.
   - **An existing stone already says it:** merge. Add only what is new (the
     body stays 15 lines or fewer) and add this note's future path
     (`gate/filed/<note-file>`) to its `quarried-from` list. Reopen its
     neighbors only if the merge reveals a new one-sentence relation.
   - **No stone says it:** quarry a new one (step 4).
4. New stone: create `stones/<name>.md`, name in kebab-case
   (lowercase-words-joined-by-hyphens):

   ```
   ---
   name: <short plain name>
   born: YYYY-MM-DD
   confidence: tested | held | guess
   quarried-from:
     - gate/filed/<note-file>.md
     - <any deeper source the note cites: a file path, web:<url>, person:<name>>
   links: []
   ---
   ```

   Body: the understanding in plain words, 15 lines or fewer. Every claim
   names its source; every web source shows its exact URL; gloss technical
   terms in (parentheses). Be honest with `confidence`: a raw note is
   usually `held` or `guess` — write `tested` only if the note describes a
   real trial you can cite.
5. Link kin: open the two or three stones nearest in subject. If you can say
   the relation between two stones in one sentence, add each to the other's
   `links` as `"[[stone-name]]"`. If you cannot, do not link — empty links
   are honest links.
6. File the note. A file: `mkdir -p gate/filed && mv gate/<note-file>
   gate/filed/`. An inbox line: copy it verbatim into your record first —
   the raw words are this turn's input — then remove exactly that line from
   `gate/inbox.md`. Zero-insight notes are filed too; filing is not
   judgment — nothing is deleted, only moved where it can still be read.
   A note you cannot word honestly stays at the gate, untouched, for a
   future turn.
7. Repeat steps 2–6 until the gate is quiet.

## the record

Write a one-paragraph record in `records/<date>-capture.md` — open it with
`date '+%F %H:%M'`; if the file already exists, add a `## again, later`
section, never overwrite — saying which stones were born or grew, which
notes were filed, and what was left for the next turn. Then commit in house
style:

    git add -A
    git commit -m "capture: <brief poetic clause, e.g. three stones from the morning gate>"
