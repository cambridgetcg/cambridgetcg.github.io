---
chapter: determinatives
organ: grammars
role: conflicts inside this chapter's own inventory, found by the first tool ever built to consume it
opened: 2026-07-24
opened_by: ORDO's attending (aletheme) — ordo/SPEC.md §IV
status: FILED — awaiting Yu's invocation. Nothing here is decided; a checker may not settle a doctrine question by choosing a branch quietly.
---

# Open conflicts in the determinatives inventory

_The determinatives chapter was written in 2026-04-24 and, until 2026-07-24, was read by no machine. `ordo/` is the first organ to consume it. Two conflicts surfaced immediately — not by argument, but because a program had to pick a branch and could not. They are recorded here rather than resolved, because a tool that quietly picks a branch of its own source of truth has replaced doctrine with implementation detail, which is exactly the failure this chapter's `.HID` class is about._

---

## Conflict 1 — the `PER` label names two codepoints

`manifesto.md:44` and `manifesto.md:47` both label their marker **PER**:

| Code | label in this chapter | marks |
|---|---|---|
| U+E171 | **PER** — person | human-agent words, beholder-words |
| U+E174 | **PER** — perception | seeing, knowing, attending |

But the registry disambiguates them:

- `script/codepoints.md:131` — `| U+E171 | .PER | Egyptian | 𓀀 | determinative: person / agent |`
- `script/codepoints.md:134` — `| U+E174 | .PRC | Egyptian | 𓁹 | determinative: perception / seeing / attending |`

`script/morphemes.json` agrees with the registry (`.PER`, `.PRC`).

**Why it matters.** The Latin notation this chapter itself prescribes is `word.TAG` (`kimance.PER`, manifesto.md:114) — and the tag is exactly what a parser reads. So this chapter's own worked example, `kimance.PER`, is undecidable between person and perception on the evidence of this chapter alone. The applied-to-canon table has two PER rows (`kimance`, `doxalgia`); both rationales read *perception*, so the intent is almost certainly U+E174 — but "almost certainly" is not a thing a checker may act on.

**What ORDO does meanwhile.** `.PER` is reported as **ambiguous**, citing both lines, and no class is guessed. The tag table's own disagreement is the first finding the attending ever produced.

**The shapes a ruling could take** (not a recommendation — the choice is Yu's):
1. Amend this chapter to `.PRC` for U+E174, matching the registry. Under expansion-only discipline (NEWSPEAK.md) a silent rename is not available; this would be a documented succession of a label.
2. Rule the registry wrong and rename U+E174 in `script/codepoints.md` + `script/morphemes.json` instead.
3. Rule that both marks legitimately share one Latin tag and that the notation must carry the codepoint where it matters — which would mean `word.PER` is never sufficient notation.

---

## Conflict 2 — does `.HID` contain *latency*?

`manifesto.md:49` glosses the class three ways:

> `| U+E176 | **HID** — hidden | (YOUSPEAK original: dashed outline) | concealment, latency, deception |`

The two machine-readable inventories drop the middle term:

- `script/morphemes.json:816` — `"meaning": "determinative: hidden / concealed / deceptive"`
- `script/codepoints.md:136` — `determinative: hidden / concealed / deceptive`

**Why it matters.** ORDO's commission (`ordo/SPEC.md` §IV, as originally filed) named "a `.HID` deception-register guard." Whether such a guard is even coherent depends entirely on this line. The evidence is genuinely split:

- **For a wide class.** The founding excavation puts `lanthes` and `verisleight` in the *same* cell: `archaeology/egyptian/determinatives.md:93` — `| **hidden** | (YOUSPEAK: dashed outline) | lanthes, verisleight |`. `lanthes` is "escape-notice, be-hidden" (`script/morphemes.json:355`) — agentless, blameless. `DICTIONARY.md:606` says of that kind of hiddenness: "the blindness is the condition of possibility for the crossing, not a deficiency." And `canon/core/sigame.md:43` makes withholding a **Core** received-ordinance — a gift-medium, not a defect.
- **For a narrow class.** Both canon words actually assigned `.HID` are deception-class (`verisleight` :88, `veriseem` :96), and both machine inventories say so.

Note also that concealment-by-design does **not** earn `.HID`: `diplosemy` conceals depth-meaning from the uninitiated and is assigned `.ABS` (manifesto.md:95). Whatever `.HID` marks, it is not "this thing hides something."

**What ORDO does meanwhile.** No `.HID` guard ships, and the tag receives no special treatment of any kind. `manifesto.md:139` — "Determinatives ONLY carry semantic class" — and `:135` lists evidentiality under what determinatives explicitly do not cover; ORDO's honesty machinery therefore stays in the evidentials (`ordo/SPEC.md` §V), where canon put it.

---

## Conflict 3 (lesser) — the chapter promised a file it never wrote

`archaeology/egyptian/determinatives.md:104` proposes the file when it proposes the chapter: "`grammars/determinatives/classes.md` — the class-inventory with codepoints." It was never written, and the manifesto's own **Pending** list (`manifesto.md:153-158`) does not carry it forward — that list ends at Espanso triggers. `grammars/determinatives/` contains `manifesto.md` and, as of today, this file. There is no per-class doctrine for `.DIV`, `.HID`, or any other mark, so every question of the form "what exactly does this class cover" resolves to a single table cell.

---

## A fourth thing, not a conflict — a gap the tooling exposed

Until 2026-07-24 the 18 word→mark assignments existed **only** as prose in this chapter. `script/tools/export_agent_bundle.py` now carries them into the agent bundle, so the assignments are machine-readable for the first time. Two consequences worth naming:

- The prose table is now load-bearing for a running program. Editing a row changes what a checker says. It should probably gain the same care as `canon.md`.
- 18 of 255 canon entries carry a mark. Nothing since 2026-04-24 has been assigned one — including the divine-pole words (`theokimme`, `theoshemme`, `walkehesed`, `andemame`) that `.DIV` would most obviously cover. Whether the applied-to-canon table should be extended, or whether determinatives are deliberately a small annotated subset, is unstated.
