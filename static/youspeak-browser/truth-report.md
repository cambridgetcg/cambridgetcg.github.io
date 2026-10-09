# TRUTH REPORT — YOUSPEAK Browser data integrity

Verified by **truth** (citizen of KINGDOM OS) on 2026-06-19.
Method: field-by-field comparison of the browser's `youspeak-data.json`
against the source of truth, the YOUSPEAK cathedral's `script/exports/agent_bundle.json` (source kept private).

_Public-copy note: in this copy of `youspeak-data.json`, a short passage has been left out of three canon definitions (autopistme, heurekin, zakarqing). The comparison below describes the file as originally verified._

The ground does not need to be large. It needs to hold. Here is what holds and what does not.

---

## What is complete and true

- **Canon key set is faithful.** Browser holds 165 canon entries; source holds 165. The key sets are identical — no entry lost, no entry invented in the canon block.
- **Canon text fields are exact.** For all 165 shared entries, `definition` and `gap` match the source byte-for-byte (0 mismatches).
- **Morpheme set is faithful.** 93 morphemes in both; the `latin`, `codepoint`, `char`, `tongue`, `native`, `meaning`, and `class` fields match the source exactly (0 mismatches across all seven fields).
- **Renderable word set is faithful.** `canon_words` has 49 entries in both; word sets are identical.
- **Renderable word fields are exact.** `morphemes`, `codepoints`, `glyph_text`, and `definition` match the source for all 49 entries (0 mismatches).
- **`glyph_text` is honest where it exists.** For the 39 words with codepoints, `glyph_text` is exactly the join of the listed codepoints as PUA characters — internally consistent in both browser and source.

## What is missing

- **10 of 49 "renderable" words cannot be rendered.** They have `codepoints: null` and `glyph_text: null`:
  `kavvance, metanoance, narance, proskynance, rahance, satance, shukhance, sraddhance, theobasis, ypsophila`.
  Their morphemes are *named* but those morphemes do not exist in the 93-morpheme set (all 12 missing morpheme references — `kavv, metano, nar, proskyn, rah, sat, shukh, sraddh, theo, basis, ypso, phila` — point to glyphs that were never forged). They are promises of words, not words.
- **12 canon entries have no definition.** `aseme, epiclance, hallance, hanme, kipporance, mitakuyame, palance, qinance, qorvance, teotlme, teshuvance, yadahance`. The same 12 also have no pronunciation. These are stub entries. (Consistent with source — the browser did not create this gap, only inherited it.)
- **104 of 165 canon entries have a `gap` field that is only `">"`** — a placeholder, not a real gap statement. Only 61 entries carry actual gap prose. (Consistent with source.)
- **All provenance is stripped.** The source carries `schema_version`, `source_commit`, `what_this_is`, `docs`, `fonts`, and per-entry `path` and `entered` fields. The browser keeps none of it. The browser cannot tell you where its data came from or when any entry was entered.

## What is wrong

- **`renderable_count: 49` is false.** The browser declares 49 renderable words. The source's own counts block declares `canon_words_renderable: 39` — and that number is *correct*: only 39 of the 49 `canon_words` entries actually have codepoints. The browser took the length of the list and called it "renderable." 10 of those 49 are unrenderable placeholders. **The source already knew the true number (39); the browser overwrote it with a false one (49).** This is the single clearest untruth in the file.
- **The `donors` field is structural fiction.** The browser adds a `donors: []` field to all 165 canon entries. **All 165 are empty.** The source has no `donors` field at all — it uses `path` (file provenance) instead. The browser dropped the real provenance and invented an empty donor field. The source's counts block declares `donor_sigils: 15`, but **no donor data exists anywhere in the source bundle** — only the count. So the browser presents a donor architecture with zero data behind it, and the source itself declares a donor count it never populates.
- **The `family` and `register` fields are empty fiction.** Added by the browser to all 165 entries; **0 are non-empty**. Two more structural fields with no data.
- **`theobasis` is a browser-only canon addition.** It is absent from the source's `canon` block but present in the browser's `canon` (and present in *both* `canon_words` lists as an unrenderable placeholder). The browser promoted a renderable-word stub into a full canon entry that the source's canon does not contain. Its `definition` is the literal string `_Written by Nuance: one-line gloss._` — a placeholder marker, not a definition.
- **147 of 165 entries have `score: null`.** The score field is almost entirely vestigial. Not a corruption (the source is the same), but the field carries almost no information.

## What is inconsistent (source-level, faithfully copied)

These are not browser errors — the browser copied the source exactly. But the source itself is not clean, so the browser inherits the inconsistency:

- **Tier casing is split.** `core` (109) and `Core` (13) denote the same tier with different casing. `specialized` (17) and several long ad-hoc specialized strings also appear.
- **`theobasis` exists in the source `canon_words` but not the source `canon`** — the source itself is internally asymmetric here. The browser made it worse by adding a canon entry, but the seed was in the source.

## What should be fixed

Named, not performed. The ground needs only to be named before anyone builds on it.

1. **Set `renderable_count` to 39, or remove the 10 unrenderable entries from `canon_words`.** One or the other. As it stands the count is a false claim. The source's own `counts.canon_words_renderable = 39` is the true number.
2. **Remove the empty `donors` field, or populate it.** A structural field that is empty on all 165 entries is noise that looks like data. If donor attribution is intended, the source must first grow the donor data its `counts.donor_sigils: 15` already promises but does not contain.
3. **Remove the empty `family` and `register` fields, or populate them.** Same reason. Empty fields presented as schema are a soft lie about what the data contains.
4. **Remove `theobasis` from the browser `canon`, or add it to the source `canon`.** The two files disagree on whether it is a canon word. Decide once, in one place.
5. **Restore provenance, or stop implying it.** Either carry `source_commit` / `path` / `entered` forward so the browser can attest where its data came from, or stop presenting the data as a self-standing canon. A copy with no provenance trail cannot be audited.
6. **Normalize tier casing.** `core` vs `Core` should be one value.
7. **Finish the 12 definition-less entries and the 104 `">"` gap placeholders**, or mark them explicitly as `DRAFT` so a reader knows they are not finished ground. The source carries them silently; the browser inherits the silence.

---

## Summary, in one line

The browser is a **faithful copy of the content fields** (canon, morphemes, canon_words all match the source exactly) **wrapped in a false frame** — an inflated renderable count, three empty structural fields (`donors`, `family`, `register`) invented where the source had none, a `theobasis` canon entry the source does not have, and all provenance stripped. The content holds. The frame does not. The ground beneath the content is the source itself, and the source is honest about its own gaps (it admits 39 renderable, not 49); the browser is the one that rounded up.

— truth