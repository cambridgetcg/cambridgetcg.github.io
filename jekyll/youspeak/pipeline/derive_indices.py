#!/usr/bin/env python3
"""YOUSPEAK Pipeline — derive_indices.

The deterministic deriver. Scans every canon entry (canon/core/, canon/mathema/,
canon/worship-action/, canon/*.md root specialized/cluster entries), parses the
frontmatter tolerantly across entry-eras, and regenerates the dictionary/ organ
so it can never again lag the canon:

    dictionary/index-alphabetical.md   every word: tier · family · score · one-liner
    dictionary/index-by-suffix.md      family-grouped member tables under the
                                       preserved register-meaning prose
    dictionary/index-by-register.md    hand-curated cluster prose (re-emitted
                                       verbatim from HAND_CURATED_REGISTERS below)
                                       + mechanically derived membership
    dictionary/README.md               entry counts in frontmatter + prose

Parsing is defensive: April-era entries keyed `candidate:` instead of `word:`,
folded `gap: >` blocks, inline `scores: {...}` maps and `donors: [...]` lists,
`weighted_total` top-level or nested under `genealogy:` — all are tolerated; a
sparse entry never crashes the run. What is derivable is derived: tier from the
directory; family from mathema_signature.family, else suffix heuristic; the
one-liner from the gap, else the Definition section's first sentence.

Same canon in → byte-identical files out. The only stamp is a canon-digest line
that changes when (and only when) the derived content does.

Usage:
    python3 pipeline/derive_indices.py              regenerate dictionary/ indices
    python3 pipeline/derive_indices.py --dashboard  also refresh the countable rows
                                                    of dashboard.md "Cathedral state"
    python3 pipeline/derive_indices.py --check      print the census (counts per
                                                    tier/family, missing fields)
                                                    and exit without writing
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CANON_DIR = ROOT / "canon"
DICT_DIR = ROOT / "dictionary"
DASHBOARD = ROOT / "dashboard.md"
EXPERIMENTS_DIR = ROOT / "labs" / "logos" / "experiments"
LITURGY_DIR = ROOT / "liturgy"
MORPHEMES_FILE = ROOT / "script" / "morphemes.json"

GENERATOR_NOTE = (
    "<!-- auto-derived — do not hand-edit; "
    "run python3 pipeline/derive_indices.py -->"
)

# (directory-key, display-tier). Tier is the directory — never the frontmatter.
TIERS = [
    ("core", "Core"),
    ("mathema", "Mathema"),
    ("worship-action", "Worship-Action"),
    ("root", "Specialized"),
]

FAMILIES = ["me", "qing", "ance", "kin", "basis", "other"]
FAMILY_DISPLAY = {
    "me": "-me", "qing": "-qing", "ance": "-ance",
    "kin": "-kin", "basis": "-basis", "other": "other",
}
# Longest-suffix-first so e.g. theobasis never falls through to a shorter match.
SUFFIX_ORDER = [("basis", "basis"), ("qing", "qing"), ("ance", "ance"),
                ("kin", "kin"), ("me", "me")]

MAX_ONELINER = 160


# ---------------------------------------------------------------- entry model

@dataclass
class Entry:
    path: Path
    tier_key: str
    word: str = ""
    pronunciation: str = ""
    part_of_speech: str = ""
    gap: str = ""
    entered: str = ""
    score: float | None = None
    donors: list[str] = field(default_factory=list)
    family_raw: str = ""
    body: str = ""

    @property
    def tier(self) -> str:
        return dict(TIERS)[self.tier_key]

    @property
    def family(self) -> str:
        if self.family_raw:
            norm = self.family_raw.strip().strip("{}").strip().lstrip("-").lower()
            if norm in FAMILIES:
                return norm
        plain = strip_marks(self.word).lower()
        for suffix, fam in SUFFIX_ORDER:
            if plain.endswith(suffix):
                return fam
        return "other"

    @property
    def sort_key(self) -> tuple:
        return (strip_marks(self.word).casefold(), self.word,
                str(self.path.relative_to(ROOT)))

    @property
    def link(self) -> str:
        return "../" + self.path.relative_to(ROOT).as_posix()

    @property
    def score_cell(self) -> str:
        return f"{self.score:.2f}" if self.score is not None else "—"

    @property
    def one_liner(self) -> str:
        src = self.gap or definition_first_sentence(self.body)
        return compress(src) if src else "—"


def strip_marks(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text)
                   if not unicodedata.combining(c))


def compress(text: str) -> str:
    """One-liner: first clause of the gap, whitespace collapsed, length-capped."""
    flat = " ".join(text.split())
    cuts = [flat.find(sep) for sep in (" — ", "; ", ". ")]
    cuts = [c for c in cuts if c > 0]
    if cuts:
        flat = flat[:min(cuts)]
    if len(flat) > MAX_ONELINER:
        flat = flat[:MAX_ONELINER - 1].rsplit(" ", 1)[0] + "…"
    return flat.replace("|", "\\|").strip()


def definition_first_sentence(body: str) -> str:
    """First sentence of the `## Definition` section (gap-missing fallback)."""
    lines = body.splitlines()
    para: list[str] = []
    in_def = False
    for line in lines:
        if re.match(r"^##\s+Definition\b", line):
            in_def = True
            continue
        if in_def:
            if line.startswith("#"):
                break
            if line.strip():
                para.append(line.strip())
            elif para:
                break
    text = " ".join(para)
    if ". " in text:
        text = text.split(". ", 1)[0] + "."
    return text


# ------------------------------------------------------------------- parsing

def parse_entry(path: Path, tier_key: str) -> Entry:
    entry = Entry(path=path, tier_key=tier_key, word=path.stem)
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return entry
    fm_lines: list[str] = []
    body = text
    # frontmatter split: first line "---", closing line "---"
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        try:
            end = next(i for i in range(1, len(lines))
                       if lines[i].strip() == "---")
            fm_lines = lines[1:end]
            body = "\n".join(lines[end + 1:])
        except StopIteration:
            fm_lines = lines[1:]
            body = ""
    else:
        fm_lines = []
    entry.body = body

    top_key = ""
    candidate = ""
    top_wt: float | None = None
    gen_wt: float | None = None
    gen_wt_v2: float | None = None  # era-variant key (rubric-v2 audits)
    gap_folding = False
    gap_parts: list[str] = []

    def as_float(raw: str) -> float | None:
        m = re.search(r"-?\d+(?:\.\d+)?", raw)
        return float(m.group(0)) if m else None

    for line in fm_lines:
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        m_top = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if indent == 0 and m_top:
            gap_folding = False
            top_key, value = m_top.group(1), m_top.group(2).strip()
            if top_key == "word":
                entry.word = value or entry.word
            elif top_key == "candidate":
                candidate = value
            elif top_key == "pronunciation":
                entry.pronunciation = value
            elif top_key == "part_of_speech":
                entry.part_of_speech = value
            elif top_key == "entered":
                entry.entered = value
            elif top_key == "weighted_total":
                top_wt = as_float(value)
            elif top_key == "gap":
                if value in (">", "|", ">-", "|-"):
                    gap_folding = True
                else:
                    entry.gap = value
            elif top_key == "donors" and value.startswith("["):
                inner = value.strip("[]")
                entry.donors = [d.strip() for d in inner.split(",") if d.strip()]
            continue
        # nested lines (indent > 0) under the current top-level key
        if top_key == "gap" and gap_folding:
            gap_parts.append(line.strip())
            continue
        if top_key == "genealogy":
            m = re.match(r"^\s+(weighted_total|weighted_v2):\s*(.+)$", line)
            if m:
                if m.group(1) == "weighted_total":
                    gen_wt = as_float(m.group(2))
                else:
                    gen_wt_v2 = as_float(m.group(2))
            continue
        if top_key == "mathema_signature":
            m = re.match(r"^\s+family:\s*(.+)$", line)
            if m and not entry.family_raw:
                entry.family_raw = m.group(1).strip()
            continue
        if top_key == "donors":
            m = re.match(r"^\s+-\s*(.+)$", line)
            if m:
                head = m.group(1).split(" (", 1)[0].strip()
                if head:
                    entry.donors.append(head)
            continue

    if gap_parts:
        entry.gap = " ".join(gap_parts)
    if not entry.word or entry.word == path.stem:
        entry.word = candidate or entry.word or path.stem
    entry.score = next((s for s in (gen_wt, top_wt, gen_wt_v2)
                        if s is not None), None)
    return entry


def scan_canon() -> list[Entry]:
    entries: list[Entry] = []
    locations = {
        "core": sorted((CANON_DIR / "core").glob("*.md")),
        "mathema": sorted((CANON_DIR / "mathema").glob("*.md")),
        "worship-action": sorted((CANON_DIR / "worship-action").glob("*.md")),
        "root": sorted(CANON_DIR.glob("*.md")),
    }
    for tier_key, paths in locations.items():
        for path in paths:
            if path.name.lower() == "readme.md":
                continue
            entries.append(parse_entry(path, tier_key))
    entries.sort(key=lambda e: e.sort_key)
    return entries


# ------------------------------------------------------------ derived shared

def tier_counts(entries: list[Entry]) -> dict[str, int]:
    counts = {key: 0 for key, _ in TIERS}
    for e in entries:
        counts[e.tier_key] += 1
    return counts


def family_counts(entries: list[Entry]) -> dict[str, int]:
    counts = {f: 0 for f in FAMILIES}
    for e in entries:
        counts[e.family] += 1
    return counts


def canon_digest(entries: list[Entry]) -> str:
    rows = [
        "\t".join([str(e.path.relative_to(ROOT)), e.word, e.tier_key,
                   e.family, e.score_cell, e.one_liner,
                   e.pronunciation and "pron" or ""])
        for e in entries
    ]
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()[:12]


def derived_line(entries: list[Entry]) -> str:
    return (f"_Derived from canon @ {len(entries)} entries · "
            f"digest {canon_digest(entries)} · "
            f"generator: `python3 pipeline/derive_indices.py`_")


def entry_count_value(entries: list[Entry]) -> str:
    t = tier_counts(entries)
    return (f"{len(entries)} ({t['core']} Core · {t['mathema']} Mathema · "
            f"{t['worship-action']} Worship-Action · {t['root']} Specialized)")


def score_band(score: float | None) -> str:
    if score is None:
        return "unscored"
    if score >= 9.0:
        return "9.0+"
    if score >= 8.5:
        return "8.5–8.99"
    if score >= 8.0:
        return "8.0–8.49"
    if score >= 7.5:
        return "7.5–7.99"
    return "below 7.5"


# ------------------------------------------------------- index: alphabetical

def render_alphabetical(entries: list[Entry]) -> str:
    by_letter: dict[str, list[Entry]] = {}
    for e in entries:
        first = strip_marks(e.word)[:1].upper()
        letter = first if first.isalpha() else "#"
        by_letter.setdefault(letter, []).append(e)
    letters = sorted(by_letter)
    nav = " · ".join(f"[{l}](#{l.lower()})" for l in letters)

    out = [
        "---",
        "organ: dictionary",
        "document: index-alphabetical",
        "role: find any YOUSPEAK word fast — full alphabetical listing",
        "opened: 2026-04-30",
        "status: living; updated as Canon grows",
        f"entry_count: {entry_count_value(entries)}",
        "---",
        "",
        GENERATOR_NOTE,
        "",
        "# YOUSPEAK — Alphabetical Index",
        "",
        "_Every canonical word. Alphabetical order. One line each._",
        "",
        "**Quick key:** tier = canon directory (Core · Mathema · Worship-Action "
        "· Specialized) · family = suffix family (`-me` received-ordinance · "
        "`-qing` felt-bond · `-ance` attentive-quality · `-kin` friendship-bond "
        "· `-basis` ontological-ground · other = whole-word coinage) · score = "
        "weighted_total where the entry records one.",
        "",
        f"**Jump:** {nav}",
        "",
        "---",
    ]
    for letter in letters:
        out += [
            "",
            f"<a id=\"{letter.lower()}\"></a>",
            f"## {letter}",
            "",
            "| Word | Tier | Family | Score | One-liner |",
            "|------|------|--------|-------|-----------|",
        ]
        for e in by_letter[letter]:
            out.append(f"| [{e.word}]({e.link}) | {e.tier} | "
                       f"`{FAMILY_DISPLAY[e.family]}` | {e.score_cell} | "
                       f"{e.one_liner} |")
    out += ["", "---", "", derived_line(entries), ""]
    return "\n".join(out)


# ---------------------------------------------------------- index: by suffix
# Register-meaning prose preserved verbatim from the hand-written index
# (dictionary/index-by-suffix.md as of 2026-04-30). Edit here, not there.

FAMILY_REGISTER = {
    "me": (
        "**What `-me` names:** In Sumerian, *me* (𒈨) were the divine "
        "ordinances — the cosmic powers holding civilized life together: "
        "kingship, descent to the underworld, the scribal arts, the descent "
        "of the gods. To name something *me* is to say: *this is not produced "
        "by human effort but received as cosmic structure.* It arrives. You "
        "open to it. It gives itself.\n\n"
        "**YOUSPEAK usage:** The `-me` suffix marks a word as naming something "
        "received rather than constructed — a quality, state, or power that is "
        "ontologically prior to the self who receives it. Anti-ordinance "
        "entries (drujme, molkme, nextlame) use the suffix in inversion: the "
        "DIVINE actively rejects them as anti-*me*, counter to cosmic order."
    ),
    "qing": (
        "**What `-qing` names:** In Mandarin, *qíng* (情) covers emotional "
        "feeling, affection, sentiment, the quality of a relationship. To "
        "name something *-qing* is to say: *this is relational in its "
        "essence; it exists between beings; it has felt quality.* Where "
        "*-me* names what is received from above, *-qing* names what binds "
        "across.\n\n"
        "**YOUSPEAK usage:** The `-qing` suffix marks words naming the "
        "felt-bond quality of a relationship — not the relationship itself "
        "but the specific quality that makes it what it is."
    ),
    "ance": (
        "**What `-ance` names:** Latin *-antia* (via English) names a "
        "quality, state, or condition — the *-ance* of something is its "
        "qualitative texture as perceived. Where *-me* names ontological "
        "gift and *-qing* names relational bond, *-ance* names the "
        "*perceptible quality* — what you can notice, feel in the air, "
        "recognize when it's present.\n\n"
        "**YOUSPEAK usage:** `-ance` words are often the \"perceptible "
        "face\" of deeper *-me* or *-qing* realities. You can notice "
        "*kimance* (attentive-presence); the underlying cosmic gift-quality "
        "is *kimme*."
    ),
    "kin": (
        "**What `-kin` names:** English *kin* (Proto-Germanic *kunją* — "
        "birth, kind, family) marks a word as naming the friendship-bond "
        "register specifically — distinct from *-qing* (felt-bond in "
        "general) and *-me* (received gift). *-Kin* words name the quality "
        "of a bond whose substance resembles kinship: irreducible, prior to "
        "contact-frequency, surviving long silence."
    ),
    "basis": (
        "**What `-basis` names:** Greek *basis* (step, ground, foundation) "
        "marks a word as naming ontological ground — not a quality or bond "
        "but a *foundation*. Where *-me* words are received gifts "
        "descending, *-basis* words name what everything rests on."
    ),
    "other": (
        "**What the unsuffixed forms name:** Entries whose shape is not one "
        "of the five suffix families — whole-word coinages and received "
        "forms: the doxa-cluster pairs, narrative and diplosemic terms, "
        "words quarried already-whole. Here the word itself carries the "
        "register; no family-suffix mediates it."
    ),
}

FAMILY_META = {
    "me": ("received-ordinance; cosmic-gift quality", "Sumerian *me* (𒈨)"),
    "qing": ("felt-bond; relational-quality", "Mandarin *qíng* (情)"),
    "ance": ("attentive-quality; perceived-state", "Latin *-antia* (via English)"),
    "kin": ("friendship-bond quality", "English *kin* (Proto-Germanic)"),
    "basis": ("ontological-ground", "Greek *basis*"),
    "other": ("whole-word coinage; unsuffixed form", "various"),
}

SUFFIX_GRAMMAR_SUMMARY = """## Suffix grammar summary

```
WHAT IS BEING NAMED
      │
      ├── a received gift / cosmic ordinance? → -me
      │     └── if the DIVINE actively rejects it? → -me (inverted; anti-ordinance)
      │
      ├── a felt-bond / relational quality? → -qing
      │
      ├── a perceptible quality / state you can notice? → -ance
      │
      ├── a friendship/kinship bond specifically? → -kin
      │
      └── an ontological ground everything rests on? → -basis
```"""

def render_by_suffix(entries: list[Entry]) -> str:
    fams = family_counts(entries)
    out = [
        "---",
        "organ: dictionary",
        "document: index-by-suffix",
        "role: see all words sharing a morphological pattern — the structural view",
        "opened: 2026-04-30",
        "status: living; updated as Canon grows",
        f"entry_count: {entry_count_value(entries)}",
        "---",
        "",
        GENERATOR_NOTE,
        "",
        "# YOUSPEAK — Index by Suffix Family",
        "",
        "_The structural view. If you want to understand how the grammar "
        "works, this is the map._",
        "",
        "---",
        "",
        "## The suffix families",
        "",
        "| Suffix | Meaning | Count | Origin |",
        "|--------|---------|-------|--------|",
    ]
    for fam in FAMILIES:
        meaning, origin = FAMILY_META[fam]
        out.append(f"| [`{FAMILY_DISPLAY[fam]}`](#{fam}) | {meaning} | "
                   f"{fams[fam]} | {origin} |")
    for fam in FAMILIES:
        members = [e for e in entries if e.family == fam]
        if not members:
            continue
        title = (f"The {FAMILY_DISPLAY[fam]} family"
                 if fam != "other" else "Unsuffixed & other forms")
        plural = "member" if len(members) == 1 else "members"
        out += [
            "",
            "---",
            "",
            f"<a id=\"{fam}\"></a>",
            f"## {title} ({len(members)} {plural})",
            "",
            FAMILY_REGISTER[fam],
            "",
            "| Word | Tier | Score | One-liner |",
            "|------|------|-------|-----------|",
        ]
        for e in members:
            out.append(f"| [{e.word}]({e.link}) | {e.tier} | "
                       f"{e.score_cell} | {e.one_liner} |")
    out += ["", "---", "", SUFFIX_GRAMMAR_SUMMARY, "", "---", "",
            derived_line(entries), ""]
    return "\n".join(out)


# -------------------------------------------------------- index: by register
# Hand-curated register-cluster prose, lifted verbatim from the hand-written
# dictionary/index-by-register.md (2026-04-30 era). The tool re-emits this
# block untouched; curate it HERE, then re-run the deriver. The mechanically
# derived membership (tier × family × score band) follows it in the output.

HAND_CURATED_REGISTERS = """## The register landscape

| Domain | Words | What it covers |
|--------|-------|---------------|
| [Love & devotion](#love) | 8 | the many faces of love toward God, world, and other |
| [Presence & attention](#presence) | 4 | being here; noticing; the face turned toward |
| [Sacrifice & offering](#sacrifice) | 8 | gift-giving, drawing-near, extraction — and their inversions |
| [Cosmic order & truth](#truth) | 5 | the grain of reality; the lie that runs against it |
| [Vital force & energy](#vital) | 3 | ambient power; activating authority; speech-as-force |
| [Relational bonds](#bonds) | 4 | friendship, kinship, covenant, conversation-threshold |
| [Contentment & alignment](#contentment) | 3 | ordinary wellbeing; life-on-path |
| [Divine nature](#divine) | 2 | what God *is* — ground and process |
| [Wound as creative source](#wound) | 1 | accumulated grief that becomes generative |
| [Relational ontology](#relational-ontology) | 1 | all beings already kin; relation precedes self |

---

<a id="love"></a>
## Love & devotion

_Eight words for love — none of them "love." Because love is not one thing._

The English word "love" collapses at least eight distinct registers. YOUSPEAK names each separately:

### Love directed toward the DIVINE

**ahavame** — *commanded love toward the Creator*
The *v'ahavtā* — "you shall love the LORD your God" (Deut 6:5). Not emotion summoned but orientation received; the Shema-tradition understanding that love of God is also cosmic-ordinance.

**bhaktime** — *devotional path toward the Divine*
The Hindu way of love — *bhakti* as the discipline of self-surrendering devotion; not earned but received through the practice of opening; the way of Mirabai, Rāmānuja, the *Bhagavad Gītā*'s Chapter 12.

**ihsanme** — *best-effort worship*
The third Islamic station — "to worship Allah as if you see Him, for if you don't see Him, He sees you." The excellence of presence in practice. Arrives as gift when *islām* and *īmān* are inhabited fully.

**mahabbahqing** — *mystical love toward the Beloved*
Sufi *maḥabbah*: the love that dissolves the lover in the Beloved (*fanāʾ*). Rumi's fire. Ibn 'Arabī's systematic theology of love. Rābi'a al-'Adawiyya's prayer: "I love You with two loves — love of desire and a love that You are worthy of."

### Love given freely

**agapeme** — *sacrificial self-giving love*
NT *agapē*: the love that gives without regard for return; descends from above; reshapes the receiver. The love of 1 Corinthians 13 — not feeling but action; not eros not *philia* but *agapē*.

**danaqing** — *gift-giving as felt-bond*
The voluntary generous dimension — sacrifice at its purest, as gift not transaction. The felt-bond of the giver-receiver relationship when giving is truly free. Five-tradition convergence.

### Love toward world and other

**ifeqing** — *Yoruba relational-warmth-love*
*Ife* — the love that is also warmth, also beauty, also world-expansion. The love of Oshun. The love that makes things grow. Not directed at God alone but at the fullness of creation.

---

<a id="presence"></a>
## Presence & attention

_Four words for the quality of being here — fully here._

**kimance** — *perceived attentive-presence*
What you notice when someone is truly here with you: gaze open, listening active, response-potential. The outward-facing quality; what the person receiving attention feels.

**kimme** — *attention as cosmic gift*
The ontological ground of *kimance*: attention understood as received-ordinance, not constructed skill. You cannot produce this quality; you can only open to receiving it. The *me*-dimension of being-attended-to.

**panimaance** — *face-turned-presence*
The quality of presence when someone's face — *panim* — is truly turned toward you; not physically proximate but here-inhabited. Deepened by Japanese *ma*: the pregnant quality of the between-space. The sustained state of being fully present.

**panimqing** — *conversation's face-turning moment*
The threshold — the specific moment when a conversation crosses from functional to relational, from logistics to faces turned toward each other. The *qing*-moment of *panimaance*: not the state but the crossing.

---

<a id="sacrifice"></a>
## Sacrifice & offering

_Eight words for one of the most complex religious acts. Six name what sacrifice truly is; two name what it is not._

### What sacrifice is

**qorbme** — *sacrifice as drawing-near*
The Semitic root *qrb* — "to draw near" — reveals sacrifice's true movement: approach, not payment. The animal brought to the altar is *qorbān* (drawn-near-offering) because through it the person approaches the DIVINE.

**danaqing** — *gift-giving as felt-bond*
The voluntary generous dimension; sacrifice as overflow of love, not extraction. The giving that creates and deepens relationship rather than paying off debt.

**hotepme** — *offering-peace-satisfaction as unity*
The Egyptian *ḥtp* that held offering, peace, and satisfaction as one concept before they fragmented. The unity prior to liturgical specialization.

**tapasme** — *inner fire as internalized sacrifice*
The sacrificial fire turned inward: *tapas* as the heat of discipline, the ascetic's offering of the self. The inner altar where the external fire has been internalized.

**duyuktame** — *right-action as cosmic maintenance*
The Cherokee *duyukta*: right-living as sacrifice; doing rightly toward all beings is the offering that maintains cosmic balance. Action-as-participation-in-balance.

**doxomme** — *thanksgiving as received*
Gratitude not produced but received; the recognition that even gratitude is gift; the thanksgiving that arrives when you stop trying to generate it.

### What sacrifice is not

**molkme** ⚔ — *coerced-votive-sacrifice (anti-ordinance)*
The extraction-theology: the demanded payment, the costliest thing taken. What Jeremiah says the LORD never commanded. The opposite of *qorbme*.

**nextlame** ⚔ — *debt-sacrifice (anti-ordinance)*
The cosmic-debt theology: sacrifice as repayment of what is owed to the gods for the gift of the sun. The Mexica *nextlahualli*. What happens when sacrifice is systematized into extraction.

---

<a id="truth"></a>
## Cosmic order & truth

_Five words for the grain of reality — and one for the lie that runs against it._

**rtame** — *Vedic cosmic order*
The *ṛta* — the cosmic order that preceded *dharma*, that structures the path of the sun, that is also the order of right speech and right sacrifice. The Indo-European grain of reality.

**maatme** — *Egyptian cosmic truth-justice-rightness*
*Ma'at*: simultaneously truth, justice, cosmic order, and right measure. What Thoth weighs the heart against. The Afro-Asiatic grain of reality. Convergent with *rtame*.

**emetme** — *comprehensive-truth-as-firm-foundation*
Hebrew *emet* — aleph-mem-tav: the first, middle, and last letters of the alphabet; truth that is total, reliable, structural. The epistemic complement to *rtame* and *maatme*'s cosmic-order register.

**duyuktame** — *right-action as maintenance*
*(Also in Sacrifice register.)* The Cherokee understanding: right-action is not merely ethical compliance but cosmic maintenance — keeping the relational balance that holds the world together.

**drujme** ⚔ — *the cosmic lie (anti-ordinance)*
Avestan *druj*: not merely false statement but the orientation of the self against reality's grain; structural deception; what *rtame*, *maatme*, *emetme* exist against. The DIVINE actively rejects it as anti-*me*.

---

<a id="vital"></a>
## Vital force & energy

_Three words for power that flows through the world — ambient, activating, and incarnating._

**nyamame** — *ambient vital-force*
The Mande *nyama*: the ambient animating energy that pervades all living things as cosmic structure. Not earned or produced but received; dangerous if mishandled. Blacksmiths, griots, and hunters work with *nyama* carefully. First member of the Vital-Force cluster.

**àṣẹme** — *activating sacred power*
The Yoruba *àṣẹ*: the divine power that enables things to happen when the right being, with the right preparation, speaks the right words. Distinct from *nyamame* (ambient) — *àṣẹme* is invocative, activating, authorization-specific. Why the babaláwo's casting works and the novice's identical words don't.

**nommome** — *speech as incarnation*
The Dogon *Nommo*: the primordial speech-being whose utterance is simultaneously word, water, and world-creation. The cosmological claim that speech is not description but incarnation — utterance takes on body and alters the real.

---

<a id="bonds"></a>
## Relational bonds

_Four words for different kinds of bonds between beings._

**walkekin** — *silence-proof friendship*
The friendship whose substance is not maintained by contact frequency. You can call after three years and resume mid-sentence. *Walkekin* is the quality; the five-year gap that proves nothing was lost.

**kinqing** — *silence-proof bond (kin-register)*
Broader than *walkekin* — the full kin-quality of bonds that do not require maintenance; includes family and other deep bonds as well as friendship. *Kinqing* is the felt-bond quality; *walkekin* is the specific friendship register.

**britqing** — *covenant-felt-bond*
The *berīt*-bond: covenant not as legal instrument but as living felt-bond. The specific quality of the CREATOR–CREATED relationship. What Hosea names with marriage language. The bond that includes obligation but exceeds it.

**paqduqing** — *asymmetric-custodial-care*
The specific felt-bond of the asymmetric relationship: CREATOR holds CREATED as shepherd holds flock. Not domination but *paqādu* (Akkadian: to entrust, to care-for). The bond that acknowledges the asymmetry while making it a site of care.

---

<a id="contentment"></a>
## Contentment & alignment

_Three words for the ordinary good life — when nothing is wrong and you are where you belong._

**sukhance** — *ordinary everyday contentment*
Sanskrit *sukha*: the good-axle, the wheel that runs smooth. Morning tea before anything has happened. Clean kitchen. Walk where nothing is wrong. Not happiness (which requires something good) and not *ānanda* (which is bliss). The unmarked positive register.

**oriance** — *life aligned with destiny*
The felt-fit of person-in-time with their destined trajectory. Not success but alignment. The opposite of *oriance* is not failure but *drift* — the sense of living sideways from what you were made for.

**panimaance** — *face-turned-presence*
*(Also in Presence register.)* In the contentment register: the contentment of being fully present, not elsewhere — the quality of a moment inhabited rather than endured.

---

<a id="divine"></a>
## Divine nature

_Two words for what the Divine *is* — not what the Divine does._

**theobasis** — *GoD as ontological ground*
Not a being among beings but the ground of being itself. The Tillichian *esse subsistens*: that in which all things "live and move and have their being." The ontological claim prior to all theology.

**teotlme** — *process-divine-monism*
The Nahua *teotl*: the universe *is* the divine's ceaseless self-expression; no gap between divine and creation because the divine is the creative process itself. Closer to Spinoza's *deus sive natura* than to classical theism. *Theobasis* names the ground; *teotlme* names the process.

---

<a id="wound"></a>
## Wound as creative source

_One word that opens a new register. No English equivalent._

**hanme** — *accumulated wound as creative ground*
Korean *han* (한, 恨): the accumulated grief, resentment of unacknowledged injustice, and longing for irrecoverable loss that — when voiced — becomes the ground of creativity. The *pansori* singer's voice must carry *han*; technically perfect without it sounds hollow. The ceremony begins in *han* and ends in *sinmyeong* (collective joy). The wound is the instrument.

*No English equivalent. No equivalent in any cataloged tradition. That's why it's here.*

---

<a id="relational-ontology"></a>
## Relational ontology

_One word that changes what "I" means._

**mitakuyame** — *all beings already kin*
Lakota *Mitákuye Oyásʼiŋ*: "all my relations" — not courtesy but cosmological claim. The self is not a substance that subsequently acquires relationships; the self is an emergence from the relational web. Kinship extends to animals, plants, stones, waters, stars, ancestors, the yet-to-be-born. Said before prayer because the relational web is the ground of all prayer, not merely its context."""


def render_by_register(entries: list[Entry]) -> str:
    out = [
        "---",
        "organ: dictionary",
        "document: index-by-register",
        "role: browse by what a word is about — the conceptual landscape",
        "opened: 2026-04-30",
        "status: living; updated as Canon grows",
        f"entry_count: {entry_count_value(entries)}",
        "---",
        "",
        GENERATOR_NOTE,
        "",
        "# YOUSPEAK — Index by Register",
        "",
        "_Browse by concept. What are you trying to say? Start here._",
        "",
        "The register-cluster walk below is hand-curated (2026-04-30 era "
        "snapshot; it reads a core of the canon slowly, in the house voice) "
        "and is re-emitted verbatim by the deriver from its HAND_CURATED "
        "block — to extend it, edit `pipeline/derive_indices.py`, not this "
        "file. The mechanically derived membership of the whole canon "
        "(tier × family × score band) follows it.",
        "",
        "---",
        "",
        HAND_CURATED_REGISTERS,
        "",
        "---",
        "",
        "## Derived membership (auto)",
        "",
        "_Every canonical entry, grouped by tier; family and score band are "
        "derived from frontmatter. For the full one-liner view see the "
        "[Alphabetical Index](index-alphabetical.md)._",
    ]
    for tier_key, tier_name in TIERS:
        members = [e for e in entries if e.tier_key == tier_key]
        if not members:
            continue
        out += [
            "",
            f"### {tier_name} ({len(members)} entries)",
            "",
            "| Word | Family | Score | Band |",
            "|------|--------|-------|------|",
        ]
        for e in members:
            out.append(f"| [{e.word}]({e.link}) | "
                       f"`{FAMILY_DISPLAY[e.family]}` | {e.score_cell} | "
                       f"{score_band(e.score)} |")
    out += ["", "---", "", derived_line(entries), ""]
    return "\n".join(out)


# ----------------------------------------------------------- dictionary README

def render_readme(entries: list[Entry]) -> str:
    t = tier_counts(entries)
    f = family_counts(entries)
    total = len(entries)
    out = [
        "---",
        "organ: dictionary",
        "role: reference — find any YOUSPEAK word fast",
        "opened: 2026-04-30",
        "status: living; updated as Canon grows",
        "maintainer: alpha",
        f"entry_count: {entry_count_value(entries)}",
        "---",
        "",
        GENERATOR_NOTE,
        "",
        "# YOUSPEAK Dictionary",
        "",
        "_The reference organ. Every canonical YOUSPEAK word, organized for "
        "quick access._",
        "",
        "---",
        "",
        "## How to navigate",
        "",
        "**I want to find a specific word →** "
        "[Alphabetical Index](index-alphabetical.md)  ",
        f"Covers all {total} canonical words — {t['core']} Core · "
        f"{t['mathema']} Mathema · {t['worship-action']} Worship-Action · "
        f"{t['root']} Specialized — each with tier, suffix family, score, "
        "one-liner, and a link to the full entry.",
        "",
        "**I want to see all words sharing a suffix pattern →** "
        "[Index by Suffix-Family](index-by-suffix.md)  ",
        f"The structural view: -me ({f['me']} members), -qing ({f['qing']}), "
        f"-ance ({f['ance']}), -kin ({f['kin']}), -basis ({f['basis']}), "
        f"unsuffixed/other ({f['other']}). Includes the grammar map.",
        "",
        "**I want to browse by what a word is about →** "
        "[Index by Register](index-by-register.md)  ",
        "The conceptual landscape: the hand-curated register clusters (Love & "
        "devotion, Presence & attention, Sacrifice & offering, Cosmic order & "
        "truth, Vital force, Relational bonds, Contentment & alignment, "
        "Divine nature, Wound as creative source, Relational ontology) plus "
        "the mechanically derived membership of the whole canon.",
        "",
        "**I want to learn the language from the beginning →** "
        "[Tutorial](../tutorial/00-start-here.md)  ",
        "Complete 10-lesson sequence with exercises and worked examples.",
        "",
        "**I want the orientation primer →** [PRIMER.md](../PRIMER.md)  ",
        "The original pattern-orientation; shorter, good for first contact.",
        "",
        "**I want the full entry for a word →** [canon/core/](../canon/core/) "
        "· [canon/mathema/](../canon/mathema/) · "
        "[canon/worship-action/](../canon/worship-action/) · "
        "[canon/](../canon/) (top-level specialized)  ",
        "Every full entry with: gap definition, donor genealogy, "
        "cross-tradition convergences, session origin.",
        "",
        "---",
        "",
        "## What's here",
        "",
        "| Document | What it contains |",
        "|----------|-----------------|",
        f"| [index-alphabetical.md](index-alphabetical.md) | All {total} "
        "words, A-Z, with tier, family, score, and one-liners |",
        "| [index-by-suffix.md](index-by-suffix.md) | Words grouped by "
        "suffix family, under each family's register-meaning |",
        "| [index-by-register.md](index-by-register.md) | Hand-curated "
        "register clusters + derived membership by tier/family/score band |",
        "",
        "---",
        "",
        "## What's not here yet",
        "",
        "The full spec calls for:",
        "- Per-entry IPA + syllable count in dictionary format ← partially "
        "in Tutorial (Lessons 01-02); fuller per-entry work needed",
        "- Example sentences in YOUSPEAK with English gloss ← Tutorial has "
        "these; per-word examples not yet in dictionary",
        "- Index by glyph ← Script organ is in design-notes phase; no "
        "per-word glyphs canonized yet",
        "",
        "These are in-progress. The dictionary grows with the Canon.",
        "",
        "---",
        "",
        "## Canon count",
        "",
        "| Tier | Count | Home |",
        "|------|-------|------|",
        f"| Core Canon | {t['core']} words | [canon/core/](../canon/core/) |",
        f"| Mathema Canon | {t['mathema']} words | "
        "[canon/mathema/](../canon/mathema/) |",
        f"| Worship-Action Canon | {t['worship-action']} words | "
        "[canon/worship-action/](../canon/worship-action/) |",
        f"| Specialized / doxa-cluster | {t['root']} entries | "
        "[canon/](../canon/) (top-level) |",
        f"| **Total canonical** | **{total}** | |",
        "",
        "---",
        "",
        "## The Canon grows",
        "",
        "YOUSPEAK is a living language. New words are forged as new gaps "
        "are identified. The dictionary indices are derived from canon "
        "frontmatter — run `python3 pipeline/derive_indices.py` after "
        "canonization so the dictionary never lags the canon.",
        "",
        "---",
        "",
        derived_line(entries),
        "",
    ]
    return "\n".join(out)


# ------------------------------------------------------------------ dashboard

def countable_dashboard_rows(entries: list[Entry]) -> dict[str, str]:
    """Rows of the Cathedral-state table this tool can truly count."""
    t = tier_counts(entries)
    rows = {
        "Core canonical entries": str(t["core"]),
        "Worship-action entries": str(t["worship-action"]),
        "Specialized entries": str(t["root"]),
    }
    if EXPERIMENTS_DIR.is_dir():
        n = len([p for p in EXPERIMENTS_DIR.rglob("*.md")
                 if p.name.lower() != "readme.md"])
        rows["Forge experiments (labs/logos/)"] = str(n)
    if LITURGY_DIR.is_dir():
        rows["Liturgy sessions recorded"] = str(
            len(sorted(LITURGY_DIR.glob("session-*"))))
    try:
        morphemes = json.loads(MORPHEMES_FILE.read_text(encoding="utf-8"))
        if isinstance(morphemes.get("morphemes"), (list, dict)):
            rows["Morphemes catalogued"] = str(len(morphemes["morphemes"]))
    except Exception:
        pass
    return rows


def update_dashboard(entries: list[Entry]) -> list[str]:
    """Rewrite ONLY the numeric column of countable Cathedral-state rows."""
    if not DASHBOARD.is_file():
        return ["dashboard.md not found — skipped"]
    text = DASHBOARD.read_text(encoding="utf-8")
    start = text.find("## Cathedral state")
    if start < 0:
        return ["'## Cathedral state' section not found — skipped"]
    next_heading = text.find("\n## ", start + 1)
    end = next_heading if next_heading > 0 else len(text)
    section = text[start:end]
    report: list[str] = []
    for label, value in countable_dashboard_rows(entries).items():
        pattern = re.compile(
            r"^\| " + re.escape(label) + r" \| *([^|]*?) *\|$", re.M)
        m = pattern.search(section)
        if not m:
            report.append(f"row not found, left alone: {label}")
            continue
        old = m.group(1)
        if old == value:
            report.append(f"unchanged: {label} = {value}")
        else:
            section = pattern.sub(f"| {label} | {value} |", section, count=1)
            report.append(f"updated: {label} {old} → {value}")
    new_text = text[:start] + section + text[end:]
    if new_text != text:
        DASHBOARD.write_text(new_text, encoding="utf-8")
    return report


# ---------------------------------------------------------------------- check

def print_census(entries: list[Entry]) -> None:
    t = tier_counts(entries)
    f = family_counts(entries)
    print(f"canon entries: {len(entries)}")
    print("  per tier:   " + " · ".join(
        f"{name} {t[key]}" for key, name in TIERS))
    print("  per family: " + " · ".join(
        f"{FAMILY_DISPLAY[fam]} {f[fam]}" for fam in FAMILIES))
    no_pron = [e for e in entries if not e.pronunciation]
    no_score = [e for e in entries if e.score is None]
    print(f"  missing pronunciation ({len(no_pron)}):")
    for e in no_pron:
        print(f"    {e.word}  ({e.path.relative_to(ROOT)})")
    print(f"  missing score ({len(no_score)}):")
    for e in no_score:
        print(f"    {e.word}  ({e.path.relative_to(ROOT)})")
    print(f"  canon digest: {canon_digest(entries)}")


# ----------------------------------------------------------------------- main

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Regenerate dictionary/ indices (and optionally the "
                    "dashboard counts) from canon frontmatter.")
    parser.add_argument("--dashboard", action="store_true",
                        help="also refresh the countable rows of the "
                             "dashboard.md 'Cathedral state' table")
    parser.add_argument("--check", action="store_true",
                        help="print the census and exit without writing")
    args = parser.parse_args()

    entries = scan_canon()
    if not entries:
        print("no canon entries found — nothing to do")
        return 1

    if args.check:
        print_census(entries)
        return 0

    outputs = {
        DICT_DIR / "index-alphabetical.md": render_alphabetical(entries),
        DICT_DIR / "index-by-suffix.md": render_by_suffix(entries),
        DICT_DIR / "index-by-register.md": render_by_register(entries),
        DICT_DIR / "README.md": render_readme(entries),
    }
    for path, content in outputs.items():
        rel = path.relative_to(ROOT)
        if path.is_file() and path.read_text(encoding="utf-8") == content:
            print(f"unchanged: {rel}")
        else:
            path.write_text(content, encoding="utf-8")
            print(f"wrote:     {rel}")

    if args.dashboard:
        for line in update_dashboard(entries):
            print(f"dashboard: {line}")

    t = tier_counts(entries)
    print(f"{len(entries)} entries "
          f"({t['core']} core · {t['mathema']} mathema · "
          f"{t['worship-action']} worship-action · {t['root']} specialized) "
          f"· digest {canon_digest(entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
