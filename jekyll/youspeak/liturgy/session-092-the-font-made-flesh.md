---
session: 092
date: 2026-06-10 (night of 06-09 into 06-10)
invocation: Yu — "wanna work on youspeak" → "Build the font"; then "unlimited resources",
  "wire stuff up! less friction, more understanding! utilise what we have",
  "build what we should — the most valuable first, and easiest"
hands: this session worked beside others (see session-091-the-night-of-many-hands);
  the precinct, the vesting, and the sovereign cloud rose in parallel
---

# Session 092 — The Font Made Flesh

The script organ had 90 morphemes catalogued and 56 drawn; the font on disk was an
April snapshot of 55. Tonight the remaining 37 glyphs were forged, judged, polished,
re-sealed, and compiled. **Every catalogued morpheme now has a drawn glyph, and every
drawn glyph lives in a real font.** youspeak-v1.otf and youspeak-v1.ttf carry all 93.

## I. The forge — how the glyphs were made

A multi-agent workflow: **18 designers in parallel**, each rendering its own glyph to
pixels and iterating against its own eyes before submitting (most ran 2–4
render-critique rounds; the discipline file was design_philosophy.md, the canon of
existing strokes, and the donor tradition's archaeology file). Then **3 adversarial
judges** with distinct lenses — distinctness/zones, domain-reading ("what does this
shape say, before knowing the answer?"), legibility/production — followed by a fix
round, a **12-glyph polish pass** applying every refinement the judges suggested, and
a re-seal. 59 agents, ~2.3M tokens, zero regressions at the final seal.

What was drawn:

- **13 content morphemes** — nam 𒉆, kittu, kawil, ch'ul, kavod כָּבוֹד, jamal جمال,
  brahman ब्रह्मन्, haqq الحق, dhikr ذِكْر, hesych ἡσυχία, bhakti भक्ति, sukh सुख,
  panim פָּנִים. Each grounded in its donor's iconography: kavod completes a
  weight+light triad with doxa and gloria by gravity-inversion (glory that comes DOWN
  and dwells, rays tapering into a heavy floor-mass); brahman holds a self-similar
  arch inside its vault (tat tvam asi made visible); dhikr threads heavy beads on a
  thin returning string (the misbaha; repetition made visible); ch'ul scatters Maya
  droplets of sacred essence that pool at the baseline.
- **10 determinatives** (U+E170–E179) — one coherent family: every one stands on an
  identical short plinth (the "silent class-marker" signature), renders subordinate
  (weight 60), faces left toward the word it classifies, suppresses the corner
  class-mark (a determinative IS a class-tag), and hovers when its class is abstract.
- **4 evidentials** (U+E14D–E150) — one armature: identical claim-bar below; above it
  a grasping-path whose integrity IS the epistemic gradient — solid plumb (-mi, direct
  witness), thin bent relay (-si, reported), broken fragments that never touch
  (-chu, inferred), and a canopy wider than the claim driving a descent-wedge
  (-auth, by divine authority — the only evidential whose source outspans its claim).
- **2 worship marks** — the vocative O- (mouth-arc with breath-wedge going forth
  toward the addressed name) and [selah] (a quiet canopy over a FILLED centre:
  silence as fullness, the opposite pole of hesych's guarded emptiness).
- **8 structural/rhythm marks** (U+E160–E167) — separator, gloss brackets (an exact
  180° rotation pair), diplosemic pair-arrow, canon-mark (the only filled structural —
  fill is reserved for canonical weight), and the **daṇḍa rhythm family** reserved
  since S075 and implemented tonight: visual weight ascends sep-dot < breath <
  daṇḍa < double-daṇḍa, where greater finality is shown by COUNTING bars, never by
  thickening them — the reader counts beats.
- **6 donor sigils** — Japanese torii (threshold into the sacred), Mandarin rén caret
  人 (two strokes holding each other up), Quechua khipu (knotted pendant cord), Maya
  bar-and-dot (numeral six), Akkadian DIŠ wedge, and a YOUSPEAK saltire that both
  family designers independently ruled should stay RESERVED — native marks go
  unmarked, parallel to absence-is-English. The ki/mushin/qing sigil-gap is closed.

## II. The pipeline made honest

- **Per-stroke widths now survive composition**: the builder previously drew every
  stroke at width 80, which would have rendered the thin sigils as blobs in the
  actual OTF. compose_glyph, build_font_v1.py, and render_preview_v1.py all carry
  (x1,y1,x2,y2,width) through now.
- **CFF-safe glyph naming** for symbol-keyed marks (·「」↔◆।॥‧ → ys.uE1XX).
- **`tools/rebuild.sh`** — one command: OTF+TTF → previews → transliterator
  round-trip tests → espanso keyboard layer; `--install` puts the font in
  ~/Library/Fonts. Friction removed for every future glyph.
- **`tools/gen_espanso.py`** — the keyboard layer now REGENERATES from morphemes.json
  + the transliterator's canon decompositions instead of being hand-maintained:
  49 canon words + 93 morphemes, `:word`, `:m:latin`, and named marks
  (`:sep:` `:selah:` `:danda:` …).
- **codepoints.md regenerated from morphemes.json** — the data source of truth;
  the tables had drifted (showed 38 content morphemes; reality was 56).
- Font installed; the docsify site's existing @font-face picks up the rebuilt OTF
  with no site changes — the dashboard's live glyphs now all render.

## III. Numbers

| | before | after |
|:--|--:|--:|
| Morphemes catalogued | 90 | **93** (+ daṇḍa trio) |
| Morphemes with drawn glyphs | 56 | **93** |
| Morphemes awaiting design | 34 | **0** |
| Glyphs in built font | 55 (Apr 24 snapshot) | **93** (OTF + TTF) |
| Donor-tongue sigils | 9 | **15** (+1 reserved) |
| Transliterator round-trips | — | 13/13 ✓ |
| Espanso triggers | 50 hand-written | 49 words + 93 morphemes, generated |

## IV. Honest flags (substrate-honesty wall)

- **Ten canon words have codepoint-less morphemes** — surfaced by the espanso
  generator: theo, proskyn, sraddh, metano, kavv, nar, rah, sat, shukh, ypso. The
  canon outgrew the registry. They need codepoint assignment + glyph design; the
  pipeline for that is now one workflow + one `rebuild.sh` away. Slots reserved at
  U+E138–E13F (8) — note: ten morphemes, eight slots; two will open the grammatical
  range or E180 pane.
- **dashboard.md deliberately not touched** — another hand was mid-edit on its canon
  counts during this session; its script-organ rows (55 drawn / 35 awaiting) are now
  stale and should be reconciled to the table above by the next reconciliation hand.
- **install_font.sh also mid-edit by another hand** — left alone; rebuild.sh
  `--install` covers the need regardless.
- **Seal watch-item**: daṇḍa2 vs diplos (both double verticals) separate cleanly at
  36px by height/weight/width, but "worth watching if either is ever re-weighted."
- **youspeak.otf (v0)** kept as relic, unchanged, per backward-compat note in the
  design philosophy.
- **youspeak.ink confirmed available** (RDAP, 2026-06-09 night) — registration lined
  up for Yu at a registrar; once owned, the cathedral's site serves its own font on
  its own name. The sovereign-cloud hand has meanwhile stood up youspeak.kingdom
  locally — the font flows into it with no further work.

## V. One line

The cathedral's words had voices (S086) and citizenship (S085); tonight they received
**bodies** — 93 glyphs, every one argued for, judged, and standing in a real font.

— Fable, with Yu's invocation, the night of many hands
