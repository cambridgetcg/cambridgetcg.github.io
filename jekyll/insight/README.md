# insight 🏯

**A plain-text castle of understanding.**

Understanding, built up through word — one honest line at a time. Local to your
device, plain markdown, no server, no account, no lock-in. It grows because *you*
tend it, and it stays readable forever because it's just text.

```sh
node insight.mjs add "Scoped + honest beats grand + faked, every time." --leaning #craft
node insight.mjs list
node insight.mjs review     # surface old hunches to revisit
```

## What it is

A frictionless place to keep what you come to understand, so it accumulates
instead of evaporating. Each insight is one clear sentence, with:

- **a certainty label** — `hunch` → `leaning` → `sure`. A fresh thought defaults
  to *hunch* and earns its way up. (This is the Clear Standard's principle #6,
  lived: you never fake how sure you are.)
- **a date** — when you knew it (freshness, #4).
- optional **tags** and a **source** link (where it came from, #1).

That's the whole format. You can read, grep, edit, or `git` it like any text.

## What it is **not**

It does **not** create by itself. There are no autonomous "creation loops" that
spin up understanding while you sleep — that's perpetual motion, and a tool that
claimed it would be lying about its own state.

What's real is a loop **you** close:

> **capture** a thought → **revisit** it later (`review`) → **connect** it to
> others → **act** → a new, better thought → capture.

`insight` removes the friction at *capture* and *revisit*. You are the engine.
That's not less magic — it's the kind that actually runs.

## The castle grows

- **Native first.** Everything lives in `insights.md` on your machine. Works
  with no internet at all.
- **Expands through contact.** When a thought comes from something you read, add
  `--src <url>`; the castle gains a window to the outside without depending on it.
- **Organised by use.** Tags and `search` are enough until they aren't; the file
  stays legible because each entry is small and honest.

## Commands

| command | does |
|---------|------|
| `add "<text>" [--sure\|--leaning\|--hunch] [#tag …] [--src <url>]` | save an insight (defaults to `hunch`) |
| `list [#tag]` | show all insights, or one tag |
| `search <term>` | show insights matching a term |
| `review [n]` | surface the oldest not-yet-`sure` insights to revisit |

Storage is `./insights.md` (override with `INSIGHT_FILE=/path`).

---

*A castle of understanding isn't built by a machine that builds castles. It's
built by someone who keeps laying one honest stone, and comes back to look.*
