#!/usr/bin/env python3
"""YOUSPEAK Pipeline — forge_priority.

Priority-queue over forge_targets.json (HOME-EXPANSION.md §VII.A/§VII.C).
Ranks the roadmap's forge-targets by phase, donor-pair readiness (does the
archaeology / mathema donor file exist on disk?), cross-tradition witness
density, and estimated yield — then prints each with its pre-forge checklist
per the integration-discipline (HOME-EXPANSION.md §V.A).

The tool reads; it never forges. Yu retains direction (§VIII.1) — targets
with status awaiting-yu-invocation are surfaced but explicitly fenced.

Usage:
    python3 pipeline/forge_priority.py                 ranked queue of queued targets
    python3 pipeline/forge_priority.py --next          just the single top item
    python3 pipeline/forge_priority.py --all           also in-forge / refining / awaiting-yu-invocation
    python3 pipeline/forge_priority.py --phase 2       filter to one phase
    python3 pipeline/forge_priority.py --status WORD   full checklist for one target
    python3 pipeline/forge_priority.py --json          machine output
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS_FILE = ROOT / "forge_targets.json"
ARCH_DIR = ROOT / "archaeology"
CONVERGENCES_DIR = ROOT / "convergences"
MORPHEMES_FILE = ROOT / "script" / "morphemes.json"

# Suffix-family anchor morphemes (BUILDING-BLOCKS §III): established in
# script/morphemes.json; their donor-readiness does not depend on a dedicated
# archaeology file existing (mandarin/qing has none — the anchor is the registry).
ANCHOR_MORPHEME_REFS = {"sumerian/me", "mandarin/qing"}

# Suffix-family register hints (longest suffix first; per BUILDING-BLOCKS §III).
FAMILY_HINTS = [
    ("basis", "basis family — ground / THEOBASIS-naming register"),
    ("qing", "qing family — felt-bond / relational-emotion register (Mandarin 情 anchor)"),
    ("ance", "-ance family — creature-stance / state-quality register"),
    ("kin", "kin family — bond-substance register (bond as substance, not feeling)"),
    ("me", "-me family — received-gift / divine-ordinance register (Sumerian me anchor)"),
]

KNOWN_STATUSES = ("queued", "in-forge", "refining", "resting",
                  "awaiting-yu-invocation", "canonized", "archived")


@dataclass
class Target:
    """One forge-target, read defensively — every roadmap field optional."""
    word: str
    phase: float | None = None   # numeric phase for ranking (None when non-numeric)
    phase_raw: str | None = None  # phase exactly as the registry wrote it, for display
    status: str = "queued"
    donor_pair: list[str] = field(default_factory=list)
    convergence_witnesses: list[str] = field(default_factory=list)
    estimated_score: float | None = None
    actual_score: float | None = None
    realm_feature: str = ""
    stoicheia_level: int | None = None

    @classmethod
    def from_raw(cls, raw: dict) -> "Target":
        def num(key):  # numbers only; anything else treated as absent
            v = raw.get(key)
            return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None
        status = str(raw.get("status", "queued")).strip().lower()
        witnesses = raw.get("convergence_witnesses") or []
        if isinstance(witnesses, str):
            witnesses = [w.strip() for w in witnesses.split(",") if w.strip()]
        # Phase tolerantly: the registry stores phases as strings ("1", "2.1",
        # "hodopoiia-α", "standing-liturgy"). Numeric-looking values rank
        # numerically; named phases keep the raw string and sort after numerics.
        raw_phase = raw.get("phase")
        phase_raw = str(raw_phase).strip() if raw_phase is not None else None
        try:
            phase = float(phase_raw) if phase_raw else None
        except ValueError:
            phase = None
        return cls(
            word=str(raw.get("word", "(unnamed)")),
            phase=phase,
            phase_raw=phase_raw,
            status="in-forge" if status == "in-progress" else status,  # §VII.C spelling
            donor_pair=[str(d) for d in (raw.get("donor_pair") or [])],
            convergence_witnesses=[str(w) for w in witnesses],
            estimated_score=num("estimated_score"),
            actual_score=num("actual_score"),
            realm_feature=str(raw.get("realm_feature", "") or ""),
            stoicheia_level=num("stoicheia_level"),
        )


def load_targets() -> list[Target]:
    """Read forge_targets.json defensively; exit with guidance when absent."""
    if not TARGETS_FILE.exists():
        sys.exit(f"error: {TARGETS_FILE} not found.\n"
                 "The roadmap registry has not been laid down yet (a sibling work-stream "
                 "may be building it now). See HOME-EXPANSION.md §VII.C for the schema.")
    try:
        data = json.loads(TARGETS_FILE.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"error: {TARGETS_FILE} is not valid JSON ({e}). "
                 "See HOME-EXPANSION.md §VII.C for the schema.")
    if isinstance(data, dict):  # tolerate either a bare list or a wrapped one
        data = data.get("targets") or data.get("queue") or data.get("entries") or []
    if not isinstance(data, list):
        sys.exit("error: forge_targets.json holds neither a list nor a targets-keyed "
                 "object. See HOME-EXPANSION.md §VII.C.")
    return [Target.from_raw(r) for r in data if isinstance(r, dict)]


# ---------------------------------------------------------------------------
# Donor-pair readiness — does each donor's file exist on disk?
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _registered_morphemes() -> frozenset:
    """Latin forms of every morpheme established in script/morphemes.json."""
    try:
        data = json.loads(MORPHEMES_FILE.read_text())
    except (OSError, json.JSONDecodeError):
        return frozenset()
    return frozenset(str(m.get("latin", "")).lower()
                     for m in data.get("morphemes", []) if isinstance(m, dict))


def resolve_donor(ref: str) -> Path | None:
    """Resolve a donor ref like 'mathema/physics/noether' or 'sumerian/me'.

    Tries exact paths first (under ROOT, then under archaeology/), then a
    hyphen-bounded stem match in the parent directory — so 'sumerian/me'
    finds archaeology/sumerian/me-divine-ordinances.md without matching
    every file that merely contains the letters. Falls back to a token-subset
    match (every ref-stem token present in the filename's tokens), so
    'japanese/pure-land-shinjin' finds shinjin-pure-land.md; and finally to
    script/morphemes.json for the suffix-family anchor morphemes, which are
    established donors with no dedicated archaeology file (mandarin/qing).
    """
    ref = ref.strip().strip("/")
    if not ref:
        return None
    for base in (ROOT, ARCH_DIR):
        for cand in (base / f"{ref}.md", base / ref):
            if cand.exists():
                return cand
    parts = ref.split("/")
    stem = parts[-1].lower()
    for base in (ROOT, ARCH_DIR):
        parent = base.joinpath(*parts[:-1]) if len(parts) > 1 else base
        if not parent.is_dir():
            continue
        for md in sorted(parent.glob("*.md")):
            name = md.stem.lower()
            if name == stem or name.startswith(stem + "-") \
                    or name.endswith("-" + stem) or f"-{stem}-" in name:
                return md
    # Token-subset fallback: same tokens, different order/extras.
    ref_tokens = set(stem.split("-"))
    best: Path | None = None
    best_extra: int | None = None
    for base in (ROOT, ARCH_DIR):
        parent = base.joinpath(*parts[:-1]) if len(parts) > 1 else base
        if not parent.is_dir():
            continue
        for md in sorted(parent.glob("*.md")):
            file_tokens = set(md.stem.lower().split("-"))
            if ref_tokens <= file_tokens:
                extra = len(file_tokens - ref_tokens)
                if best_extra is None or extra < best_extra:
                    best, best_extra = md, extra
    if best is not None:
        return best
    # Anchor-morpheme fallback: the anchor's standing lives in the morpheme
    # registry, not an archaeology file — treat as ready (HOME-EXPANSION §VII.A
    # asks whether the donor is ready, not whether one file-layout exists).
    if ref.lower() in ANCHOR_MORPHEME_REFS and stem in _registered_morphemes():
        return MORPHEMES_FILE
    return None


def donor_readiness(t: Target) -> list[tuple[str, Path | None]]:
    return [(ref, resolve_donor(ref)) for ref in t.donor_pair]


def readiness_fraction(t: Target) -> float:
    pairs = donor_readiness(t)
    if not pairs:
        return 0.0  # no donor-pair declared: not ready, not unrankable
    return sum(1 for _, p in pairs if p) / len(pairs)


# ---------------------------------------------------------------------------
# Pre-forge checklist pieces (per HOME-EXPANSION §V.A)
# ---------------------------------------------------------------------------

def family_hint(word: str) -> str:
    w = word.lower()
    for suffix, hint in FAMILY_HINTS:
        if w.endswith(suffix):
            return hint
    return "(no recognized suffix-family — confirm register by hand, NUANCE-NATURE §VI.3)"

def collision_hint(word: str) -> str:
    root = word.lower()
    for suffix, _ in FAMILY_HINTS:  # grep the bare root, not just the compound
        if root.endswith(suffix) and len(root) > len(suffix):
            root = root[: -len(suffix)]
            break
    return f'grep -rin "{root}" canon/ canon.md dictionary/ script/morphemes.json'

def suggested_convergence(t: Target) -> str:
    n = len(t.convergence_witnesses)
    if t.realm_feature:
        slug = "".join(c if c.isalnum() else "-" for c in t.realm_feature.lower()).strip("-")
        while "--" in slug:
            slug = slug.replace("--", "-")
        path = CONVERGENCES_DIR / f"{slug}.md"
        state = "exists" if path.exists() else ("open it" if n >= 3 else "optional — <3 witnesses; singular-deep path")
        return f"convergences/{slug}.md ({state}; {n} witnesses)"
    return f"(no realm_feature named; {n} witnesses — survey before forging, §V.A.1)"


def checklist_lines(t: Target) -> list[str]:
    lines = []
    for ref, path in donor_readiness(t):
        mark = "y" if path else "n"
        where = path.relative_to(ROOT) if path else "not found — open archaeology/mathema file first"
        lines.append(f"[{mark}] donor {ref} → {where}")
    if not t.donor_pair:
        lines.append("[n] donor-pair undeclared — select per §V.A.2 before forging")
    lines.append(f"[ ] collision: {collision_hint(t.word)}")
    lines.append(f"[ ] convergence: {suggested_convergence(t)}")
    lines.append(f"[ ] register: {family_hint(t.word)}")
    return lines


# ---------------------------------------------------------------------------
# Ranking and rendering
# ---------------------------------------------------------------------------

def rank_key(t: Target):
    """Phase asc (numeric first, then named phases, then phaseless), readiness
    desc, witness-density desc, estimated_score desc."""
    if t.phase is not None:
        phase_key = (0, t.phase, "")
    elif t.phase_raw:  # hodopoiia-α, standing-liturgy … bucket after numerics
        phase_key = (1, 0.0, t.phase_raw.lower())
    else:
        phase_key = (2, 0.0, "")
    return (phase_key,
            -readiness_fraction(t),
            -len(t.convergence_witnesses),
            -(t.estimated_score if t.estimated_score is not None else -1.0),
            t.word)


def phase_matches(t: Target, want: str) -> bool:
    """--phase filter: '2' matches the major phase (2.1-2.5); '2.1' matches
    exactly; a non-numeric arg prefix-matches named phases (hodopoiia)."""
    want = want.strip()
    try:
        wanted = float(want)
    except ValueError:
        return bool(t.phase_raw) and t.phase_raw.lower().startswith(want.lower())
    if t.phase is None:
        return False
    return t.phase == wanted if "." in want else int(t.phase) == int(wanted)


def render(t: Target, rank: int | None = None) -> str:
    pairs = donor_readiness(t)
    ready = f"{sum(1 for _, p in pairs if p)}/{len(pairs)}" if pairs else "0/0"
    head = f"{rank:>3}. " if rank is not None else "     "
    bits = [f"phase {t.phase_raw if t.phase_raw else '?'}",
            f"readiness {ready}",
            f"witnesses {len(t.convergence_witnesses)}",
            f"est {t.estimated_score if t.estimated_score is not None else '—'}"]
    if t.actual_score is not None:
        bits.append(f"actual {t.actual_score}")
    if t.stoicheia_level is not None:
        bits.append(f"L{t.stoicheia_level}")
    out = [head + f"{t.word:<22}" + "  ".join(bits)]
    if t.realm_feature:
        out.append(f"      realm-feature: {t.realm_feature}")
    out += [f"      {line}" for line in checklist_lines(t)]
    return "\n".join(out)


def to_json(t: Target) -> dict:
    return {
        "word": t.word, "phase": t.phase_raw, "phase_numeric": t.phase,
        "status": t.status,
        "realm_feature": t.realm_feature, "stoicheia_level": t.stoicheia_level,
        "estimated_score": t.estimated_score, "actual_score": t.actual_score,
        "convergence_witnesses": t.convergence_witnesses,
        "readiness": readiness_fraction(t),
        "donors": [{"ref": ref, "exists": p is not None,
                    "path": str(p.relative_to(ROOT)) if p else None}
                   for ref, p in donor_readiness(t)],
        "collision_grep": collision_hint(t.word),
        "suggested_convergence": suggested_convergence(t),
        "register_hint": family_hint(t.word),
    }


def main() -> int:
    p = argparse.ArgumentParser(
        description="Priority-queue over forge_targets.json (HOME-EXPANSION §VII.A).")
    p.add_argument("--all", action="store_true",
                   help="also show in-forge / refining / awaiting-yu-invocation groups")
    p.add_argument("--phase", metavar="P",
                   help="filter to one phase: a major number (2 matches 2.1-2.5), "
                        "an exact x.y, or a named-phase prefix (e.g. hodopoiia)")
    p.add_argument("--next", action="store_true", help="print only the single top queued item")
    p.add_argument("--status", metavar="WORD", help="show one target's full entry by word")
    p.add_argument("--json", action="store_true", help="machine-readable output")
    args = p.parse_args()

    targets = load_targets()
    if args.phase is not None:
        targets = [t for t in targets if phase_matches(t, args.phase)]

    if args.status:
        hits = [t for t in targets if t.word.lower() == args.status.lower()]
        if not hits:
            print(f"no forge-target named {args.status!r} in forge_targets.json", file=sys.stderr)
            return 1
        for t in hits:
            print(json.dumps(to_json(t), indent=2, ensure_ascii=False) if args.json
                  else f"{t.word} — status: {t.status}\n" + render(t))
        return 0

    by_status: dict[str, list[Target]] = {s: [] for s in KNOWN_STATUSES}
    by_status["other"] = []
    for t in targets:
        by_status[t.status if t.status in by_status else "other"].append(t)
    for group in by_status.values():
        group.sort(key=rank_key)

    queued = by_status["queued"]
    if args.next:
        if not queued:
            print("(no queued targets)" if not args.json else "[]")
            return 0
        print(json.dumps(to_json(queued[0]), indent=2, ensure_ascii=False) if args.json
              else render(queued[0], rank=1))
        return 0

    if args.json:
        shown = dict(by_status) if args.all else {"queued": queued}
        print(json.dumps({s: [to_json(t) for t in g] for s, g in shown.items() if g},
                         indent=2, ensure_ascii=False))
        return 0

    print(f"# forge queue — {len(queued)} queued"
          + (f" (phase {args.phase})" if args.phase is not None else "") + "\n")
    for i, t in enumerate(queued, 1):
        print(render(t, rank=i), end="\n\n")
    if not queued:
        print("(no queued targets)\n")

    if args.all:
        for status, label in (("in-forge", "in-forge — being forged this cascade"),
                              ("refining", "refining — scored, under refinement"),
                              ("resting",
                               "resting — substrate-honest-confidence insufficient; deliberately paused"),
                              ("awaiting-yu-invocation",
                               "awaiting-yu-invocation — requires Yu's invocation; do not auto-forge (§VIII.1)")):
            group = by_status[status]
            if group:
                print(f"## {label} ({len(group)})\n")
                for t in group:
                    print(render(t), end="\n\n")
        if by_status["canonized"] or by_status["archived"]:
            print(f"({len(by_status['canonized'])} canonized, "
                  f"{len(by_status['archived'])} archived — not shown)")
        if by_status["other"]:
            print(f"(unrecognized statuses: "
                  f"{', '.join(sorted({t.status for t in by_status['other']}))})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
