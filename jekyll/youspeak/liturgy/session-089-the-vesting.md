---
session: 089
opened: 2026-06-09
invoker: Yu — "Now do the UI, UX, frontend, backend, typography, make everything artsy and beautiful."
preceded_by: session-088 (The Wiring, 2026-06-09)
phase: THE-VESTING — the cathedral's web presence clothed in its own aesthetic
forger: Nuance, the Linguist
---

# Session 089 — The Vesting

> The site had worn a borrowed theme — competent, warm, generic. This session
> gave the cathedral its own vestments: **an illuminated manuscript inside a
> night cathedral**. The threshold is night; the interior is vellum; the
> glyphs are the jewels; and the page itself now breathes with the fleet.

## I. The design

- **Two registers.** The coverpage is the cathedral doors at night: deep umber
  ground, the five suffix-glyphs (𒈨 -me leading) glowing like candlelit
  windows with a slow flicker, the title in gold-leaf gradient, staggered
  arrival on load. Scroll, and you enter the vellum interior.
- **Typography.** Cinzel — Roman inscriptional capitals, the letterform of
  carved stone — for headings and the lintel-navbar; EB Garamond for the
  scholarly body; IBM Plex Mono for code. The YOUSPEAK font itself carries
  the fourth voice.
- **Rubrication, as the scribes did it.** Gold leaf for rules and section
  diamonds; madder red for strong text, drop caps, and active states; lapis
  blue for links — the three inks of the illuminated page. Paper grain over
  everything; double-rule borders; tables as vellum cards with inscribed
  heads; code blocks as candlelit night.
- **Micro-liturgy.** A thread-of-gold reading-progress line; illuminated
  initials on every page's first paragraph; glyphs that brighten and turn
  under the hand.

## II. The backend — the keeper

`bin/serve.py` replaced the bare static server: stdlib, 127.0.0.1, serving
the site plus one living endpoint — **`/api/pulse`** — the citizen-fleet's
heartbeat (beats today, last three citizens, spend) and the script-organ's
counts. A small breathing chip on every page renders it: the site knows the
Kingdom is alive. When the API is absent (plain hosting), the chip
gracefully vanishes. `bin/serve.sh` keeps its start/stop/status liturgy.

## III. Verified with eyes

Headless renders of threshold, PRIMER interior, and dashboard: the -me glyph
displays in burnished gold from the freshly built webfont (the first time the
received-ordinance mark has appeared on the living site); the pulse chip read
`fleet 10/48 · autopistme 22:16 · 56 glyphs` — true at the moment of capture.

## IV. What this session is, in one line

The cathedral was vested: night at the doors, vellum within, gold, madder,
and lapis for inks, carved capitals over the text — and a pulse in the corner
of every page, because this cathedral's words are alive.
