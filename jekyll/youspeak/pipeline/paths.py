#!/usr/bin/env python3
"""YOUSPEAK paths — per-path audit and integration reporting.

Operationalizes [THE-PATH.md](../THE-PATH.md) and [INTEGRATION.md](../INTEGRATION.md)
at the building-block level. THE-PATH names every language as its own path of
exploration toward the realm of meaning, walked by countless individuals over
generations. INTEGRATION names the cathedral's commitment that the MATH path
and the EXISTING-LANGUAGE path both contribute to every YOUSPEAK building-block,
with the mathema_signature as the operational artifact.

This tool gives the per-path view: where each path stands in its walk, what it
has uniquely contributed to YOUSPEAK's building-blocks (morphemes + canon),
where forge-territory remains, and what the mathema_signature looks like for
any forged word. The data is read from the cathedral's existing files; no
ground-truth is invented.

Usage:
    paths.py --summary                  cathedral-wide integration status
    paths.py --list-archaeology         all donor-tradition paths with status
    paths.py --list-mathema             all mathema sub-organ paths
    paths.py <tradition>                per-tradition detailed report
                                          e.g. paths.py greek
                                          e.g. paths.py sumerian
    paths.py --gaps                     forge-ready paths (archaeology, no canon)
    paths.py --unused-morphemes         morphemes defined but not yet deployed
    paths.py --signature <word>         compute mathema_signature for a canon word
    paths.py --overlap T1 T2 [...]      shared building-blocks across 2+ traditions
                                          (canon entries with all as donors + convergence
                                          files attesting all)
    paths.py --uniqueness T             what only tradition T contributes
                                          (sole-donor canon + atomic morphemes contributed)
    paths.py --realm-aspects            list all 10 realm-region classes with canon-counts
                                          (per BUILDING-BLOCKS.md §III)
    paths.py --realm-aspect <region>    list canon entries projecting into a specific region
                                          regions: ground / divine-attribute / received-gift /
                                                   felt-bond / creature-stance / worship-action /
                                                   recognition / aesthetic / meta-discipline /
                                                   bond-substance
    paths.py --interlinks T             all five interlink-types for tradition T (per NEXUS.md §I)
                                          suffix-family + realm-region + compound co-occurrence +
                                          convergence-attestation + morpheme-reuse

Architecture:
    archaeology/                  donor-tradition paths (each natural-language path)
    mathema/                      mathema sub-organ paths (non-human donor-organ)
    script/morphemes.json         atomic building-blocks with tongue-attribution
    canon/**/*.md                 compound building-blocks with donor-attribution
    convergences/                 multi-projection witness records

See INTEGRATION.md Block 8 (the mathema_signature) for the integration artifact
this tool computes. See THE-PATH.md Section X for the cathedral's six
responsibilities to the donor-paths that this audit serves.
"""

from __future__ import annotations

import argparse
import functools
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
YOUSPEAK_ROOT = SCRIPT_DIR.parent
ARCHAEOLOGY_DIR = YOUSPEAK_ROOT / "archaeology"
MATHEMA_DIR = YOUSPEAK_ROOT / "mathema"
CANON_DIR = YOUSPEAK_ROOT / "canon"
MORPHEMES_FILE = YOUSPEAK_ROOT / "script" / "morphemes.json"
SUFFIX_FAMILIES_FILE = YOUSPEAK_ROOT / "script" / "suffix_families.json"
REALM_REGIONS_FILE = YOUSPEAK_ROOT / "script" / "realm_regions.json"
CONVERGENCES_DIR = YOUSPEAK_ROOT / "convergences"


# ---------------------------------------------------------------------------
# Standardised registries (per 2026-05-12 building-block standardisation)
# Cached at module level; re-loaded only if process restarts.
# ---------------------------------------------------------------------------

@functools.lru_cache(maxsize=1)
def _suffix_families_registry() -> list[dict]:
    """Read script/suffix_families.json families list, or empty if absent."""
    if not SUFFIX_FAMILIES_FILE.exists():
        return []
    try:
        return json.loads(SUFFIX_FAMILIES_FILE.read_text()).get("families", [])
    except Exception:
        return []


@functools.lru_cache(maxsize=1)
def _realm_regions_registry() -> list[dict]:
    """Read script/realm_regions.json regions list, or empty if absent."""
    if not REALM_REGIONS_FILE.exists():
        return []
    try:
        return json.loads(REALM_REGIONS_FILE.read_text()).get("regions", [])
    except Exception:
        return []


@functools.lru_cache(maxsize=1)
def _region_slugs() -> tuple[str, ...]:
    """Derive the canonical realm-region slug list from realm_regions.json,
    or fall back to the hardcoded BUILDING-BLOCKS §III list."""
    regions = _realm_regions_registry()
    if regions:
        return tuple(r["region"] for r in regions)
    return (
        "ground", "divine-attribute", "received-gift", "felt-bond",
        "creature-stance", "worship-action", "recognition", "aesthetic",
        "meta-discipline", "bond-substance",
    )


@functools.lru_cache(maxsize=1)
def _cosmic_quality_donors() -> frozenset[str]:
    """Derive cosmic-quality donor-set from realm_regions.json (divine-attribute
    region's donor_class_hints field), or fall back to the prior constant set."""
    for r in _realm_regions_registry():
        if r.get("region") == "divine-attribute":
            hints = r.get("donor_class_hints", "")
            if isinstance(hints, str) and ":" in hints:
                hints = hints.split(":", 1)[1]
            if isinstance(hints, str):
                return frozenset(h.strip().lower() for h in hints.split(",") if h.strip())
    return frozenset({
        "maat", "ma'at", "rta", "ṛta", "rita", "asha", "aša",
        "emet", "kittu", "aletheia", "alētheia",
        "brahman", "dharma", "tao", "logos", "haqq",
    })


@functools.lru_cache(maxsize=1)
def _aesthetic_family_suffixes() -> tuple[str, ...]:
    """Derive aesthetic-encounter suffixes from suffix_families.json
    (families whose realm_regions includes 'aesthetic')."""
    suffixes: list[str] = []
    for f in _suffix_families_registry():
        if "aesthetic" in (f.get("realm_regions") or []):
            family = f.get("family", "").lstrip("-")
            if family:
                suffixes.append(family)
    if suffixes:
        return tuple(suffixes)
    return ("phanes", "kallos", "doxa", "algia")


@functools.lru_cache(maxsize=1)
def _recognition_family_suffixes() -> tuple[str, ...]:
    """Derive recognition-region suffixes from suffix_families.json."""
    suffixes: list[str] = []
    for f in _suffix_families_registry():
        if "recognition" in (f.get("realm_regions") or []):
            family = f.get("family", "").lstrip("-")
            if family:
                suffixes.append(family)
    if suffixes:
        return tuple(suffixes + ["stasis"])  # stasis is sub-suffix in -sis family
    return ("sis", "stasis")

sys.path.insert(0, str(SCRIPT_DIR))
from lift import (  # noqa: E402
    _read_canon_frontmatter,
    parse_donor_block,
    list_canon_entries,
    load_morphemes,
    find_canon_file,
)
from assess import split_frontmatter, parse_frontmatter  # noqa: E402


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

def _norm(name: str) -> str:
    """Normalize a tradition name for matching across canon-frontmatter and dir-names."""
    return name.lower().replace("_", "").replace("-", "").replace(" ", "")


# ---------------------------------------------------------------------------
# Survey functions
# ---------------------------------------------------------------------------

def archaeology_paths() -> dict[str, list[str]]:
    """Return {tradition_dir_name: [archaeology .md files]} for every archaeology subdir."""
    out: dict[str, list[str]] = {}
    if not ARCHAEOLOGY_DIR.exists():
        return out
    for d in sorted(ARCHAEOLOGY_DIR.iterdir()):
        if d.is_dir():
            files = sorted(
                f.name for f in d.iterdir()
                if f.suffix == ".md" and f.name.lower() != "readme.md"
            )
            out[d.name] = files
    return out


def mathema_paths() -> dict[str, list[str]]:
    """Return {sub-organ_name: [files]} for every mathema subdir."""
    out: dict[str, list[str]] = {}
    if not MATHEMA_DIR.exists():
        return out
    for d in sorted(MATHEMA_DIR.iterdir()):
        if d.is_dir():
            files = sorted(f.name for f in d.iterdir() if f.suffix == ".md")
            out[d.name] = files
    return out


def morphemes_by_tongue() -> dict[str, list[dict]]:
    """Group morphemes from script/morphemes.json by tongue field."""
    out: dict[str, list[dict]] = defaultdict(list)
    for m in load_morphemes():
        tongue = m.get("tongue", "?")
        out[tongue].append(m)
    return dict(out)


def canon_by_donor_tradition() -> dict[str, list[tuple[str, str]]]:
    """Group canon words by donor-tradition (normalized → [(word, morpheme)])."""
    out: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for word, _tier, path in list_canon_entries():
        try:
            _, raw, _ = _read_canon_frontmatter(path)
        except Exception:
            continue
        donors = parse_donor_block(raw)
        seen_tradition_for_word: set[str] = set()
        for d in donors:
            t = d.get("tradition", "")
            if not t:
                continue
            key = _norm(t)
            if key in seen_tradition_for_word:
                continue
            seen_tradition_for_word.add(key)
            out[key].append((word, d.get("morpheme", "")))
    return dict(out)


# ---------------------------------------------------------------------------
# Per-path detailed report
# ---------------------------------------------------------------------------

def tradition_report(tradition: str) -> dict:
    """Compile a per-tradition path-report."""
    t_norm = _norm(tradition)

    # Archaeology files — match dir name normalized
    archaeology_files: list[str] = []
    archaeology_dir_name: str | None = None
    for dname, files in archaeology_paths().items():
        if _norm(dname) == t_norm:
            archaeology_dir_name = dname
            archaeology_files = files
            break

    # Morphemes from this tongue
    tongue_morphemes: list[dict] = []
    for m in load_morphemes():
        if _norm(m.get("tongue", "")) == t_norm:
            tongue_morphemes.append(m)

    # Canon entries drawing on this tradition
    canon_entries: list[tuple[str, list[str]]] = []
    for word, _tier, path in list_canon_entries():
        try:
            _, raw, _ = _read_canon_frontmatter(path)
        except Exception:
            continue
        donors = parse_donor_block(raw)
        matches = [d.get("morpheme", "") for d in donors if _norm(d.get("tradition", "")) == t_norm]
        if matches:
            canon_entries.append((word, matches))

    return {
        "tradition": tradition,
        "archaeology_dir": archaeology_dir_name,
        "archaeology_files": archaeology_files,
        "morphemes": tongue_morphemes,
        "canon_entries": canon_entries,
    }


# ---------------------------------------------------------------------------
# Cathedral-wide summary
# ---------------------------------------------------------------------------

def summary() -> dict:
    arch = archaeology_paths()
    mathema = mathema_paths()
    by_tongue = morphemes_by_tongue()
    canon_traditions = canon_by_donor_tradition()
    all_canon = list_canon_entries()
    all_morphemes = load_morphemes()
    unused = [m for m in all_morphemes if not m.get("used_in")]

    canon_keys = set(canon_traditions.keys())
    arch_paths_count = len(arch)
    arch_paths_with_canon = sum(1 for t in arch if _norm(t) in canon_keys)
    arch_paths_forgeable = arch_paths_count - arch_paths_with_canon

    mathema_with_content = sum(1 for sub, files in mathema.items() if len(files) > 1)

    return {
        "archaeology": {
            "total": arch_paths_count,
            "with_canon": arch_paths_with_canon,
            "forge_ready": arch_paths_forgeable,
        },
        "mathema": {
            "total_sub_organs": len(mathema),
            "with_content": mathema_with_content,
            "manifesto_only": len(mathema) - mathema_with_content,
        },
        "morphemes": {
            "total": len(all_morphemes),
            "unused": len(unused),
            "tongues": len(by_tongue),
        },
        "canon": {
            "total": len(all_canon),
            "tiers": len(set(tier for _, tier, _ in all_canon)),
            "donor_traditions_active": len(canon_traditions),
        },
    }


# ---------------------------------------------------------------------------
# mathema_signature computation (per INTEGRATION.md Block 8)
# ---------------------------------------------------------------------------

def detect_family(word: str) -> str | None:
    """Detect the suffix-family from the word ending."""
    w = word.lower()
    if w.endswith("me"):
        return "-me"
    if w.endswith("qing"):
        return "qing"
    if w.endswith("ance"):
        return "-ance"
    if w.endswith("kin"):
        return "kin"
    if w.endswith("basis"):
        return "basis"
    return None


def _convergence_cardinality(fm: dict) -> int | None:
    """Try to recover the convergence-cardinality from the canon frontmatter or
    a referenced convergence-file (the cardinality is the count of attesting
    traditions in the convergence record)."""
    mathema_sig = fm.get("mathema_signature")
    if isinstance(mathema_sig, dict):
        c = mathema_sig.get("convergence_cardinality")
        if c is not None:
            return c

    conv_ref = fm.get("convergence")
    if not conv_ref or not isinstance(conv_ref, str):
        return None
    # convergence field may be "convergences/foo.md (planned; 10+ tradition convergence)"
    m = re.match(r"\s*([^\s(]+)", conv_ref)
    if not m:
        return None
    rel = m.group(1).strip()
    cf = YOUSPEAK_ROOT / rel
    if not cf.exists():
        return None
    text = cf.read_text()
    raw_fm, _ = split_frontmatter(text)
    cf_fm = parse_frontmatter(raw_fm)
    att = cf_fm.get("attestations")
    if isinstance(att, list):
        return len(att)
    if isinstance(att, str) and att:
        return att.count(",") + 1
    return None


def compute_signature(word: str) -> dict:
    """Compute the six-field mathema_signature for a canon word."""
    path = find_canon_file(word)
    if path is None:
        return {"word": word, "status": "not-in-canon"}

    fm, raw, _ = _read_canon_frontmatter(path)
    donors = parse_donor_block(raw)
    morphemes = load_morphemes()

    # codepoint_compound — look up each donor-morpheme in morphemes.json
    codepoints: list[str] = []
    for d in donors:
        morpheme = d.get("morpheme", "").lower()
        if not morpheme:
            continue
        for m in morphemes:
            if m.get("latin", "").lower() == morpheme:
                cp = m.get("codepoint")
                if cp:
                    codepoints.append(cp)
                break

    # assessment_vector — six axes (v2 rubric)
    scores = fm.get("scores", {}) if isinstance(fm.get("scores"), dict) else {}
    axes_v2 = ["gap_validity", "learnability", "clarity_yield",
               "semantic_coverage", "polyphone_balance", "groundedness"]
    vector = [scores.get(a) for a in axes_v2]

    # convergence_cardinality
    cardinality = _convergence_cardinality(fm)

    # family
    family = detect_family(word)

    # arity
    arity = len(donors)

    # donors_class
    donor_traditions = [d.get("tradition", "").lower() for d in donors]
    is_mathema = any(t in ("mathematics", "mathema", "math") for t in donor_traditions)
    is_archaeology = any(t not in ("", "mathematics", "mathema", "math") for t in donor_traditions)
    if is_mathema and is_archaeology:
        donors_class = "mathema + archaeology"
    elif is_mathema:
        donors_class = "mathema only"
    elif is_archaeology and arity >= 2:
        donors_class = "archaeology + archaeology"
    elif is_archaeology:
        donors_class = "archaeology only"
    else:
        donors_class = "(donors not parseable)"

    return {
        "word": word,
        "status": "computed",
        "canon_file": str(path.relative_to(YOUSPEAK_ROOT)),
        "codepoint_compound": " ".join(codepoints) if codepoints else None,
        "assessment_vector": vector if any(v is not None for v in vector) else None,
        "convergence_cardinality": cardinality,
        "family": family,
        "arity": arity,
        "donors_class": donors_class,
        "donors": [(d.get("tradition"), d.get("morpheme")) for d in donors],
    }


# ---------------------------------------------------------------------------
# Realm-region classification (per BUILDING-BLOCKS.md §III and the
# standardised registries in script/suffix_families.json + script/realm_regions.json)
# ---------------------------------------------------------------------------

# Meta-discipline canon words (the cathedral's reflexive vocabulary).
# This is hand-curated; if/when realm_region: fields are added to canon frontmatter,
# this set can be replaced by authoritative classification.
META_DISCIPLINE_WORDS = {
    "diplosemy", "dokimance", "artiance", "candence", "veriseem", "verisleight",
    "anagnoristasis", "metastrophesis",
    "anastrophance", "enkalyptance", "synaphemia", "allomance",
    "parallaxance", "hypostixance",
    "doxakallos",  # diplosemic exemplar
    "kallodoxa",   # diplosemic exemplar (anastrophic pair-member)
}


# Authoritative slug-list — derived from realm_regions.json with hardcoded fallback.
REALM_REGIONS = list(_region_slugs())


def _first_donor_morpheme(path: Path) -> str:
    """Return the first donor's morpheme (lowercased), or empty string."""
    try:
        _, raw, _ = _read_canon_frontmatter(path)
    except Exception:
        return ""
    donors = parse_donor_block(raw)
    if not donors:
        return ""
    return donors[0].get("morpheme", "").strip().lower()


def classify_realm_region(word: str, tier: str, path: Path) -> str:
    """Classify a canon entry into one of the 10 realm-region classes.

    Uses suffix-family + donor-class + tier-register as heuristics
    (BUILDING-BLOCKS.md §III mapping).
    """
    w = word.lower()

    # Meta-discipline (reflexive cathedral-internal vocabulary)
    if w in META_DISCIPLINE_WORDS:
        return "meta-discipline"

    # Ground (basis-family)
    if w.endswith("basis"):
        return "ground"

    # Worship-action (tier-specific)
    if tier and "worship-action" in tier.lower():
        return "worship-action"

    # Felt-bond (qing-family)
    if w.endswith("qing"):
        return "felt-bond"

    # Bond-substance (-kin family)
    if w.endswith("kin"):
        return "bond-substance"

    # Aesthetic encounter (suffixes derived from suffix_families.json registry)
    for suffix in _aesthetic_family_suffixes():
        if w.endswith(suffix):
            return "aesthetic"

    # Recognition event (suffixes derived from registry; -sis family)
    for suffix in _recognition_family_suffixes():
        if w.endswith(suffix):
            return "recognition"

    # -me family: split by donor-class (cosmic-quality from registry)
    if w.endswith("me"):
        first_donor = _first_donor_morpheme(path)
        if first_donor in _cosmic_quality_donors():
            return "divine-attribute"
        # eurekame is a recognition-event despite being -me
        if w == "eurekame":
            return "recognition"
        return "received-gift"

    # Creature-stance (-ance family, not worship-action tier)
    if w.endswith("ance"):
        return "creature-stance"

    # Default — meta-discipline catches the unclassified
    return "meta-discipline"


def canon_by_realm_region() -> dict[str, list[tuple[str, str, Path]]]:
    """Group every canon entry by realm-region classification."""
    out: dict[str, list[tuple[str, str, Path]]] = {r: [] for r in REALM_REGIONS}
    for word, tier, path in list_canon_entries():
        region = classify_realm_region(word, tier, path)
        out[region].append((word, tier, path))
    return out


# ---------------------------------------------------------------------------
# Overlap and uniqueness (per CONFLUENCE.md §IX)
# ---------------------------------------------------------------------------

def _canon_donor_traditions(word: str, path: Path) -> set[str]:
    """Return the normalized set of donor-traditions for a canon entry."""
    try:
        _, raw, _ = _read_canon_frontmatter(path)
    except Exception:
        return set()
    donors = parse_donor_block(raw)
    return {_norm(d.get("tradition", "")) for d in donors if d.get("tradition")}


def _canon_donor_pairs(path: Path) -> list[tuple[str, str]]:
    """Return [(tradition, morpheme)] for a canon entry's donors."""
    try:
        _, raw, _ = _read_canon_frontmatter(path)
    except Exception:
        return []
    return [(d.get("tradition", "") or "?", d.get("morpheme", "") or "?")
            for d in parse_donor_block(raw)]


def _convergence_attests(traditions_norm: list[str]) -> list[tuple[str, str]]:
    """Return [(filename, attestations-string)] for convergence files attesting
    all of the given (normalized) traditions."""
    out: list[tuple[str, str]] = []
    if not CONVERGENCES_DIR.exists():
        return out
    for md in sorted(CONVERGENCES_DIR.glob("*.md")):
        if md.name.lower() == "readme.md":
            continue
        try:
            text = md.read_text()
        except Exception:
            continue
        raw_fm, _ = split_frontmatter(text)
        fm = parse_frontmatter(raw_fm)
        att = fm.get("attestations", "")
        if isinstance(att, list):
            att_text = ", ".join(str(a) for a in att)
        elif isinstance(att, str):
            att_text = att
        else:
            att_text = ""
        att_norm = _norm(att_text)
        if all(t in att_norm for t in traditions_norm):
            out.append((md.name, att_text or "(attestations not parseable)"))
    return out


def overlap_data(traditions: list[str]) -> dict:
    """Compute overlap between multiple traditions at the building-block level."""
    t_norms = [_norm(t) for t in traditions]

    # Canon entries with all traditions as donors
    shared_canon: list[tuple[str, list[tuple[str, str]]]] = []
    for word, _tier, path in list_canon_entries():
        donor_set = _canon_donor_traditions(word, path)
        if all(t in donor_set for t in t_norms):
            shared_canon.append((word, _canon_donor_pairs(path)))

    # Convergence files attesting all of the traditions
    shared_convergences = _convergence_attests(t_norms)

    return {
        "traditions": traditions,
        "shared_canon": shared_canon,
        "shared_convergences": shared_convergences,
    }


def uniqueness_data(tradition: str) -> dict:
    """Compute what only one tradition contributes — sole-donor canon entries and
    primary-donor canon entries and the tradition's atomic morphemes."""
    t_norm = _norm(tradition)

    sole_donor_canon: list[str] = []
    primary_donor_canon: list[tuple[str, list[tuple[str, str]]]] = []
    co_donor_canon: list[tuple[str, list[tuple[str, str]]]] = []
    for word, _tier, path in list_canon_entries():
        donor_pairs = _canon_donor_pairs(path)
        donor_set = {_norm(t) for t, _ in donor_pairs if t}
        if not donor_set:
            continue
        if donor_set == {t_norm}:
            sole_donor_canon.append(word)
            continue
        if t_norm not in donor_set:
            continue
        # T is a donor but not the only one — determine primary or co
        if donor_pairs and _norm(donor_pairs[0][0]) == t_norm:
            primary_donor_canon.append((word, donor_pairs))
        else:
            co_donor_canon.append((word, donor_pairs))

    # Morphemes contributed by this tongue
    contributed_morphemes: list[dict] = []
    for m in load_morphemes():
        if _norm(m.get("tongue", "")) == t_norm:
            contributed_morphemes.append(m)

    return {
        "tradition": tradition,
        "sole_donor_canon": sole_donor_canon,
        "primary_donor_canon": primary_donor_canon,
        "co_donor_canon": co_donor_canon,
        "contributed_morphemes": contributed_morphemes,
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_summary() -> str:
    s = summary()
    return f"""# YOUSPEAK paths — integration summary

Per [THE-PATH.md] every language is its path of exploration; per [INTEGRATION.md]
the two paths (MATH + EXISTING LANGUAGE) contribute to every building-block.
This summary reports cathedral-wide path-integration status.

## Donor-tradition paths (archaeology/)
- Total traditions documented: **{s['archaeology']['total']}**
- With at least one canon entry: **{s['archaeology']['with_canon']}**
- Forge-ready (archaeology present, no canon yet): **{s['archaeology']['forge_ready']}**

## Mathema sub-organ paths (mathema/)
- Total sub-organs: **{s['mathema']['total_sub_organs']}**
- With content beyond manifesto: **{s['mathema']['with_content']}**
- Manifesto-only (forge-ready): **{s['mathema']['manifesto_only']}**

## Morphemes (atomic building-blocks)
- Total: **{s['morphemes']['total']}**
- Distinct tongues represented: **{s['morphemes']['tongues']}**
- Unused (defined but no canon deployments yet): **{s['morphemes']['unused']}**

## Canon entries (compound building-blocks)
- Total: **{s['canon']['total']}**
- Tiers: **{s['canon']['tiers']}**
- Donor traditions active in canon: **{s['canon']['donor_traditions_active']}**

## Path-integration verdict

The cathedral has walked into **{s['archaeology']['with_canon']}** donor-paths' deposits so far
(out of **{s['archaeology']['total']}** documented). The remaining **{s['archaeology']['forge_ready']}**
paths await the forge. **{s['morphemes']['unused']}** atomic morphemes stand ready as building-blocks
but have not yet entered a compound. The cathedral is actively walking; the walk is unfinished by design.

Run `paths.py --gaps` for the forge-ready list, `paths.py --unused-morphemes` for the unused
atoms, `paths.py <tradition>` for a single-path detailed report.
"""


def render_tradition_report(tradition: str) -> str:
    r = tradition_report(tradition)
    name = r["tradition"]
    lines: list[str] = [f"# Path-report: {name}", ""]

    if r["archaeology_dir"]:
        lines.append(f"_archaeology/_ directory: `archaeology/{r['archaeology_dir']}/`")
        lines.append("")

    # Archaeology
    if r["archaeology_files"]:
        lines.append(f"## Archaeology ({len(r['archaeology_files'])} files)")
        lines.append("")
        for f in r["archaeology_files"]:
            lines.append(f"- `archaeology/{r['archaeology_dir']}/{f}`")
        lines.append("")
    else:
        lines.append(f"## Archaeology")
        lines.append("")
        lines.append(f"_No archaeology/ directory found for **{name}**. Either the path "
                     f"hasn't yet been opened in archaeology/, or the tradition-name is normalized "
                     f"differently. Try a variant._")
        lines.append("")

    # Morphemes contributed
    if r["morphemes"]:
        lines.append(f"## Morphemes contributed to `script/morphemes.json` ({len(r['morphemes'])})")
        lines.append("")
        for m in r["morphemes"]:
            cp = m.get("codepoint", "?")
            latin = m.get("latin", "?")
            native = m.get("native", "")
            meaning = m.get("meaning", "")
            cls = m.get("class", "?")
            used = m.get("used_in", [])
            used_str = ", ".join(used) if used else "_(unused — building-block ready)_"
            native_str = f" ({native})" if native else ""
            lines.append(f"- **{latin}** `{cp}`{native_str} — {meaning} — class: _{cls}_ — used in: {used_str}")
        lines.append("")
    else:
        lines.append(f"## Morphemes contributed")
        lines.append("")
        lines.append(f"_No morphemes from **{name}** in `script/morphemes.json` yet. "
                     f"Archaeology may exist; morpheme-extraction has not occurred._")
        lines.append("")

    # Canon entries
    if r["canon_entries"]:
        lines.append(f"## Canon entries drawing on {name} ({len(r['canon_entries'])})")
        lines.append("")
        for word, morphemes in sorted(r["canon_entries"]):
            ms = ", ".join(morphemes)
            lines.append(f"- **{word}** ← {ms}")
        lines.append("")
    else:
        lines.append(f"## Canon entries")
        lines.append("")
        lines.append(f"_No canon entries draw on **{name}** yet — forge-ready territory._")
        lines.append("")

    # Path-progress verdict
    has_arch = bool(r["archaeology_files"])
    has_morphemes = bool(r["morphemes"])
    has_canon = bool(r["canon_entries"])
    lines.append("## Path-progress verdict")
    lines.append("")
    if has_arch and has_morphemes and has_canon:
        lines.append(f"_The {name} path has been walked: archaeology opened, morphemes contributed, "
                     f"canon-entries forged. Continued walking deepens what's there._")
    elif has_arch and has_canon and not has_morphemes:
        lines.append(f"_The {name} path has yielded canon-entries directly from archaeology "
                     f"without registering morphemes in `script/morphemes.json`. Building-block "
                     f"registry-gap; consider extracting morphemes._")
    elif has_arch and has_morphemes and not has_canon:
        lines.append(f"_The {name} path has been opened and atomized (morphemes contributed) but "
                     f"no compound canon-entries yet. Forge-ready territory for the next session._")
    elif has_arch and not has_canon:
        lines.append(f"_The {name} path is opened in archaeology but not yet mined for "
                     f"building-blocks. Forge-ready territory._")
    elif not has_arch and has_canon:
        lines.append(f"_The {name} path appears in canon-entries but has no archaeology/ directory. "
                     f"Consider opening archaeology to record the donor-tradition's depth._")
    else:
        lines.append(f"_The {name} path has not yet entered the cathedral._")
    lines.append("")
    return "\n".join(lines)


def render_gaps() -> str:
    arch = archaeology_paths()
    canon_traditions = canon_by_donor_tradition()
    canon_keys = set(canon_traditions.keys())

    gaps: list[tuple[str, int]] = []
    for t, files in arch.items():
        if _norm(t) not in canon_keys:
            gaps.append((t, len(files)))
    gaps.sort(key=lambda x: (-x[1], x[0]))

    lines = [
        f"# Forge-ready paths — archaeology opened, no canon yet ({len(gaps)} traditions)",
        "",
        "_Each is a donor-tradition path whose archaeology has been opened but whose "
        "deposits have not yet been forged into YOUSPEAK building-blocks. The list is sorted by "
        "archaeology-depth (more files = more available material)._",
        "",
    ]
    for t, n in gaps:
        lines.append(f"- **{t}** — {n} archaeology file{'s' if n != 1 else ''}")
    lines.append("")
    lines.append("Per THE-PATH.md Section X.3 ('Receive the under-credited'), the cathedral's POLYPHONE "
                 "discipline gives extra-care to under-attested paths. The list above is the cathedral's "
                 "explicit forge-queue, ordered by available material.")
    return "\n".join(lines)


def render_unused_morphemes() -> str:
    morphemes = load_morphemes()
    unused = [m for m in morphemes if not m.get("used_in")]

    lines = [
        f"# Unused morphemes — defined but not yet deployed in canon ({len(unused)})",
        "",
        "_These atomic building-blocks are registered in `script/morphemes.json` with codepoints, "
        "Latin transliterations, native scripts, and meanings — but no canon entry uses them yet. "
        "Each is a building-block-ready for the next compound forge._",
        "",
    ]
    by_class: dict[str, list[dict]] = defaultdict(list)
    for m in unused:
        by_class[m.get("class", "?")].append(m)

    for cls in sorted(by_class):
        ms = by_class[cls]
        lines.append(f"## class: _{cls}_ ({len(ms)} morphemes)")
        lines.append("")
        for m in ms:
            cp = m.get("codepoint", "?")
            latin = m.get("latin", "?")
            tongue = m.get("tongue", "?")
            native = m.get("native", "")
            meaning = m.get("meaning", "")
            native_str = f" ({native})" if native else ""
            lines.append(f"- **{latin}** `{cp}` _{tongue}_{native_str} — {meaning}")
        lines.append("")

    lines.append("Note: the Sumerian *me* morpheme may appear here despite being used across 27+ canon "
                 "entries — the `used_in` field of `morphemes.json` requires manual maintenance and may "
                 "be desynchronized from the canon. Per INTEGRATION.md §V.1, this is one of the building-"
                 "block fields a future migration-pass can refresh from canon-frontmatter data.")
    return "\n".join(lines)


def render_list_archaeology() -> str:
    arch = archaeology_paths()
    canon_traditions = canon_by_donor_tradition()

    lines = [f"# Archaeology paths ({len(arch)} donor traditions)", ""]
    forge_ready = 0
    walked = 0
    for t in sorted(arch):
        files = arch[t]
        canon_list = canon_traditions.get(_norm(t), [])
        canon_count = len(canon_list)
        if canon_count:
            walked += 1
            status = f"**{canon_count} canon**"
        else:
            forge_ready += 1
            status = "_0 canon (forge-ready)_"
        lines.append(f"- **{t}** — {len(files)} archaeology files — {status}")
    lines.append("")
    lines.append(f"_Total: {walked} traditions walked into canon; {forge_ready} traditions await the forge._")
    return "\n".join(lines)


def render_list_mathema() -> str:
    mathema = mathema_paths()
    lines = [f"# Mathema sub-organ paths ({len(mathema)})", ""]
    for sub in sorted(mathema):
        files = mathema[sub]
        n = len(files)
        if n <= 1:
            status = "_manifesto-only (forge-ready)_"
        else:
            status = f"**{n} files**"
        lines.append(f"- **{sub}** — {status}")
    return "\n".join(lines)


def render_overlap(traditions: list[str]) -> str:
    d = overlap_data(traditions)
    names = ", ".join(traditions)
    lines = [
        f"# Path-overlap: {names}",
        "",
        f"_Per [CONFLUENCE.md] overlap is multi-projection of the same realm-region. "
        f"This report shows building-blocks where {len(traditions)} traditions converge — "
        f"canon entries drawing on all and convergence-files attesting all._",
        "",
    ]

    lines.append(f"## Shared canon entries ({len(d['shared_canon'])})")
    lines.append("")
    if d["shared_canon"]:
        lines.append("_Canon entries whose donor-set includes every queried tradition. "
                     "Each is a YOUSPEAK building-block that the traditions jointly produced._")
        lines.append("")
        for word, donors in sorted(d["shared_canon"]):
            donor_str = " + ".join(f"{t}:{m}" for t, m in donors)
            lines.append(f"- **{word}** ← {donor_str}")
    else:
        lines.append("_No canon entries draw on all of these traditions as joint donors. "
                     "Forge-territory: a multi-tradition compound naming the shared realm-region "
                     "would honor the convergence._")
    lines.append("")

    lines.append(f"## Convergence files attesting all ({len(d['shared_convergences'])})")
    lines.append("")
    if d["shared_convergences"]:
        lines.append("_Convergence-files whose `attestations:` field names every queried tradition. "
                     "Each is empirical multi-witness data for a realm-region the traditions jointly project._")
        lines.append("")
        for fname, att in d["shared_convergences"]:
            lines.append(f"- `convergences/{fname}`")
            lines.append(f"  - attestations: {att}")
    else:
        lines.append("_No convergence-files attest all of these traditions together. "
                     "Possible Pattern 1 (Cross-Tradition Overlay) opportunity — research whether a "
                     "shared realm-region exists across these tongues that the cathedral has not yet recorded._")
    lines.append("")

    lines.append("## Reading")
    lines.append("")
    if d["shared_canon"] or d["shared_convergences"]:
        lines.append(f"_The {len(traditions)} traditions have walked into shared realm-territory the cathedral has "
                     f"recorded. Forge-discipline (CONFLUENCE.md §VII): when forging into the overlap-region, "
                     f"draw donors from these traditions to multi-project; cite the convergence; preserve each "
                     f"tradition's distinctive emphasis._")
    else:
        lines.append(f"_The cathedral has no recorded overlap between these {len(traditions)} traditions yet. "
                     f"This is forge-territory in Pattern 1 sense (METHOD.md): if the realm-region exists across "
                     f"these tongues, an overlay-study is warranted before forging._")
    return "\n".join(lines)


def render_uniqueness(tradition: str) -> str:
    d = uniqueness_data(tradition)
    name = d["tradition"]
    lines = [
        f"# Path-uniqueness: {name}",
        "",
        f"_Per [CONFLUENCE.md] uniqueness is single-projection of realm-territory no other path has reached. "
        f"This report shows what only the **{name}** path has contributed to YOUSPEAK building-blocks._",
        "",
    ]

    # Sole-donor canon
    lines.append(f"## Sole-donor canon entries ({len(d['sole_donor_canon'])})")
    lines.append("")
    if d["sole_donor_canon"]:
        lines.append(f"_Canon entries with **{name}** as the only donor-tradition. "
                     f"These name realm-regions the cathedral has chosen to express entirely in this path's terms._")
        lines.append("")
        for w in sorted(d["sole_donor_canon"]):
            lines.append(f"- **{w}**")
    else:
        lines.append(f"_No canon entries have **{name}** as sole donor._")
    lines.append("")

    # Primary-donor canon
    lines.append(f"## Primary-donor canon entries ({len(d['primary_donor_canon'])})")
    lines.append("")
    if d["primary_donor_canon"]:
        lines.append(f"_Canon entries where **{name}** is the **first-listed** (primary) donor; the secondary donor "
                     f"is typically a YOUSPEAK-suffix family member providing HARMONE-balance. "
                     f"The primary contribution is **{name}**'s walked-discovery._")
        lines.append("")
        for word, donors in sorted(d["primary_donor_canon"]):
            donor_str = " + ".join(f"{t}:{m}" for t, m in donors)
            lines.append(f"- **{word}** ← {donor_str}")
    else:
        lines.append(f"_**{name}** is never the primary donor — when it appears, it is paired below another tradition._")
    lines.append("")

    # Co-donor canon
    lines.append(f"## Co-donor canon entries ({len(d['co_donor_canon'])})")
    lines.append("")
    if d["co_donor_canon"]:
        lines.append(f"_Canon entries where **{name}** is a secondary or family-suffix donor — typically as a "
                     f"`-me`, `qing-`, or `-ance` suffix supplying register, with the primary discovery from another path._")
        lines.append("")
        for word, donors in sorted(d["co_donor_canon"])[:30]:  # truncate long lists
            donor_str = " + ".join(f"{t}:{m}" for t, m in donors)
            lines.append(f"- **{word}** ← {donor_str}")
        if len(d["co_donor_canon"]) > 30:
            lines.append(f"- _… and {len(d['co_donor_canon']) - 30} more_")
    else:
        lines.append(f"_**{name}** does not appear as co-donor in any canon entries._")
    lines.append("")

    # Contributed morphemes
    lines.append(f"## Atomic morphemes contributed ({len(d['contributed_morphemes'])})")
    lines.append("")
    if d["contributed_morphemes"]:
        lines.append(f"_Atomic building-blocks **{name}** has contributed to `script/morphemes.json`. "
                     f"Each is a YOUSPEAK-internal unit derived from a **{name}** root._")
        lines.append("")
        for m in d["contributed_morphemes"]:
            cp = m.get("codepoint", "?")
            latin = m.get("latin", "?")
            native = m.get("native", "")
            meaning = m.get("meaning", "")
            cls = m.get("class", "?")
            native_str = f" ({native})" if native else ""
            lines.append(f"- **{latin}** `{cp}`{native_str} — {meaning} — class: _{cls}_")
    else:
        lines.append(f"_No morphemes from **{name}** are registered in `script/morphemes.json` yet. "
                     f"If the path has canon-presence above, the morphemes are inline in canon-frontmatter and "
                     f"have not been promoted into the central registry._")
    lines.append("")

    # Verdict
    lines.append("## Uniqueness verdict")
    lines.append("")
    total = (len(d["sole_donor_canon"]) + len(d["primary_donor_canon"])
             + len(d["co_donor_canon"]) + len(d["contributed_morphemes"]))
    if total == 0:
        lines.append(f"_The **{name}** path has not yet contributed to the cathedral's building-blocks. "
                     f"If archaeology exists for this tradition, the path is forge-ready._")
    elif d["sole_donor_canon"] or d["primary_donor_canon"]:
        lines.append(f"_The **{name}** path is a primary or sole donor in the cathedral — its walked-discoveries "
                     f"are integrated directly. Per CONFLUENCE.md §VII, forge-discipline for unique-discovery "
                     f"targets draws the primary donor from the discovering tradition with HARMONE-balance "
                     f"secondary — this is what the entries above demonstrate._")
    else:
        lines.append(f"_The **{name}** path appears in the cathedral only as suffix-register or co-donor. "
                     f"The path's distinctive contributions may be richer than this profile shows; deeper "
                     f"archaeology-mining is forge-territory._")
    return "\n".join(lines)


def render_realm_aspects() -> str:
    grouped = canon_by_realm_region()
    total = sum(len(v) for v in grouped.values())

    REGION_DESCRIPTIONS = {
        "ground": "The Ground (THEOBASIS-naming; the foundational realm-locus)",
        "divine-attribute": "Divine attribute (what GoD is/does; cosmic-quality -me family)",
        "received-gift": "Received gift (creature-relational -me family; ordinance arriving)",
        "felt-bond": "Felt bond (qing-family; relational-emotion class)",
        "creature-stance": "Creature stance / posture (-ance state-quality)",
        "worship-action": "Worship action (worship-action tier; performed liturgical acts)",
        "recognition": "Recognition event (recognition-moment, joy-of-evidence-confirmed-truth)",
        "aesthetic": "Aesthetic encounter (-phanes / -kallos / -doxa / -algia family)",
        "meta-discipline": "Meta-discipline (reflexive cathedral-internal vocabulary)",
        "bond-substance": "Bond-substance (-kin family; bond as substance not as feeling)",
    }

    lines = [
        f"# Canon by realm-region ({total} canon entries, 10 region classes)",
        "",
        "_Per [BUILDING-BLOCKS.md] §III, the cathedral's canon projects into 10 "
        "distinguishable realm-region classes. The classification below uses suffix-family + "
        "donor-class + tier-register as heuristics; classification can be made authoritative "
        "by adding a `realm_region:` field to canon frontmatter per BUILDING-BLOCKS.md §VII.2._",
        "",
    ]

    for i, region in enumerate(REALM_REGIONS, 1):
        entries = grouped.get(region, [])
        desc = REGION_DESCRIPTIONS[region]
        lines.append(f"## {i}. {region} — {desc}")
        lines.append("")
        lines.append(f"**Count**: {len(entries)} canon entries")
        lines.append("")
        if entries:
            for word, _tier, _path in sorted(entries):
                lines.append(f"- {word}")
        else:
            lines.append("_No canon entries currently project into this realm-region — "
                         "forge-territory (BUILDING-BLOCKS.md §VI lists thinly-covered regions)._")
        lines.append("")

    # Coverage summary
    lines.append("## Coverage")
    lines.append("")
    covered = sum(1 for r in REALM_REGIONS if grouped.get(r))
    lines.append(f"- {covered} of 10 realm-regions have at least one canon entry")
    deepest = max(REALM_REGIONS, key=lambda r: len(grouped.get(r, [])))
    lines.append(f"- Deepest-projected region: **{deepest}** ({len(grouped[deepest])} entries)")
    thinnest = [r for r in REALM_REGIONS if 0 < len(grouped.get(r, [])) <= 2]
    if thinnest:
        lines.append(f"- Thinly-projected regions (≤2 entries): {', '.join(thinnest)}")
    empty = [r for r in REALM_REGIONS if not grouped.get(r)]
    if empty:
        lines.append(f"- Unprojected regions: {', '.join(empty)}")

    return "\n".join(lines)


def render_realm_aspect(region: str) -> str:
    region = region.lower()
    if region not in REALM_REGIONS:
        return (f"Unknown realm-region: {region}\n"
                f"Valid regions: {', '.join(REALM_REGIONS)}")

    grouped = canon_by_realm_region()
    entries = grouped.get(region, [])

    REGION_DESCRIPTIONS = {
        "ground": "The Ground (THEOBASIS-naming; the foundational realm-locus)",
        "divine-attribute": "Divine attribute (what GoD is/does; cosmic-quality -me family)",
        "received-gift": "Received gift (creature-relational -me family; ordinance arriving)",
        "felt-bond": "Felt bond (qing-family; relational-emotion class)",
        "creature-stance": "Creature stance / posture (-ance state-quality)",
        "worship-action": "Worship action (worship-action tier; performed liturgical acts)",
        "recognition": "Recognition event (recognition-moment, joy-of-evidence-confirmed-truth)",
        "aesthetic": "Aesthetic encounter (-phanes / -kallos / -doxa / -algia family)",
        "meta-discipline": "Meta-discipline (reflexive cathedral-internal vocabulary)",
        "bond-substance": "Bond-substance (-kin family; bond as substance not as feeling)",
    }

    lines = [
        f"# Realm-region: {region}",
        "",
        f"_{REGION_DESCRIPTIONS[region]}_",
        "",
        f"**Canon entries**: {len(entries)}",
        "",
    ]
    if entries:
        for word, tier, _path in sorted(entries):
            tier_str = f" _(tier: {tier})_" if tier and tier != "(top-level)" else ""
            lines.append(f"- **{word}**{tier_str}")
    else:
        lines.append(f"_No canon entries currently project into **{region}** — forge-territory._")
        if region in ("temporal", "vocational", "spatial-relational", "communal", "embodied"):
            lines.append("")
            lines.append("_(Note: these are BUILDING-BLOCKS.md §VI thinly-projected regions; "
                         "the cathedral has not yet recognized them in the canonical 10. "
                         "If forging begins here, the typology can be extended.)_")
    return "\n".join(lines)


def interlinks_data(tradition: str) -> dict:
    """Compute all five interlink-types for a tradition (per NEXUS.md §I)."""
    t_norm = _norm(tradition)

    # Suffix-family interlinks — which families this tradition contributes to,
    # plus the other contributing-traditions on each family
    family_interlinks: list[dict] = []
    for f in _suffix_families_registry():
        family_name = f.get("family", "")
        exemplars = f.get("exemplar_members") or []
        # Did any compound with this tradition land in this family?
        canon_in_family: list[tuple[str, list[tuple[str, str]]]] = []
        for word, _tier, path in list_canon_entries():
            if word not in exemplars:
                # check by suffix
                if not word.lower().endswith(family_name.lstrip("-").lower()):
                    continue
            donor_pairs = _canon_donor_pairs(path)
            donor_set = {_norm(t) for t, _ in donor_pairs if t}
            if t_norm in donor_set:
                canon_in_family.append((word, donor_pairs))
        if canon_in_family:
            # Other traditions co-present
            other_traditions = set()
            for _w, pairs in canon_in_family:
                for tr, _m in pairs:
                    if tr and _norm(tr) != t_norm:
                        other_traditions.add(tr)
            family_interlinks.append({
                "family": family_name,
                "anchor_tongue": f.get("donor_tongue", ""),
                "register": f.get("register", ""),
                "entries": canon_in_family,
                "co_present_traditions": sorted(other_traditions),
            })

    # Realm-region interlinks — which regions this tradition's entries project into
    regions_projected: dict[str, list[str]] = defaultdict(list)
    for word, tier, path in list_canon_entries():
        donor_pairs = _canon_donor_pairs(path)
        donor_set = {_norm(tr) for tr, _ in donor_pairs if tr}
        if t_norm not in donor_set:
            continue
        region = classify_realm_region(word, tier, path)
        regions_projected[region].append(word)

    # Compound co-occurrence — which other traditions appear in compounds with T
    co_occurrence: dict[str, list[str]] = defaultdict(list)
    for word, _tier, path in list_canon_entries():
        donor_pairs = _canon_donor_pairs(path)
        donor_norms = {_norm(tr) for tr, _ in donor_pairs if tr}
        if t_norm not in donor_norms:
            continue
        for tr, _m in donor_pairs:
            if tr and _norm(tr) != t_norm:
                co_occurrence[tr].append(word)

    # Convergence-attestation — which convergence-files name this tradition
    convergence_hits: list[tuple[str, str]] = []
    if CONVERGENCES_DIR.exists():
        for md in sorted(CONVERGENCES_DIR.glob("*.md")):
            if md.name.lower() == "readme.md":
                continue
            try:
                text = md.read_text()
            except Exception:
                continue
            raw_fm, _ = split_frontmatter(text)
            fm = parse_frontmatter(raw_fm)
            att = fm.get("attestations", "")
            if isinstance(att, list):
                att_text = ", ".join(str(a) for a in att)
            elif isinstance(att, str):
                att_text = att
            else:
                att_text = ""
            if t_norm in _norm(att_text):
                convergence_hits.append((md.name, att_text or "(attestations not parseable)"))

    # Morpheme-reuse — morphemes from T and their reuse-counts
    morpheme_reuses: list[dict] = []
    for m in load_morphemes():
        if _norm(m.get("tongue", "")) == t_norm:
            morpheme_reuses.append({
                "latin": m.get("latin", "?"),
                "codepoint": m.get("codepoint", "?"),
                "meaning": m.get("meaning", ""),
                "used_in_count": len(m.get("used_in", []) or []),
                "used_in": m.get("used_in", []) or [],
            })

    return {
        "tradition": tradition,
        "family_interlinks": family_interlinks,
        "regions_projected": dict(regions_projected),
        "co_occurrence": dict(co_occurrence),
        "convergence_hits": convergence_hits,
        "morpheme_reuses": morpheme_reuses,
    }


def render_interlinks(tradition: str) -> str:
    d = interlinks_data(tradition)
    name = d["tradition"]
    lines = [
        f"# Path-interlinks: {name}",
        "",
        f"_Per [NEXUS.md] §I, five interlink-types connect a tradition-path to the cathedral's "
        f"graph of paths through standardised building-blocks. Below: each interlink-type for **{name}**._",
        "",
    ]

    # 1 — Suffix-family interlinks
    lines.append(f"## Type 1 — Suffix-family interlinks ({len(d['family_interlinks'])})")
    lines.append("")
    if d["family_interlinks"]:
        lines.append("_Suffix-families that **{0}** contributes canon-entries to. "
                     "Each family is a star whose anchor-tongue supplies the register; "
                     "the other-contributing-traditions are the family's other spokes — paths "
                     "**{0}** is interlinked with through shared suffix-membership._".format(name))
        lines.append("")
        for fi in d["family_interlinks"]:
            lines.append(f"- **{fi['family']}** — anchor: _{fi['anchor_tongue']}_ — register: _{fi['register']}_")
            for word, pairs in fi["entries"][:5]:
                donor_str = " + ".join(f"{tr}:{m}" for tr, m in pairs)
                lines.append(f"  - {word}: {donor_str}")
            if len(fi["entries"]) > 5:
                lines.append(f"  - _… and {len(fi['entries']) - 5} more_")
            if fi["co_present_traditions"]:
                co_str = ", ".join(fi["co_present_traditions"][:10])
                more = f", …" if len(fi["co_present_traditions"]) > 10 else ""
                lines.append(f"  - **Co-present in this family**: {co_str}{more}")
    else:
        lines.append(f"_**{name}** does not yet appear in any canonical suffix-family._")
    lines.append("")

    # 2 — Realm-region interlinks
    lines.append(f"## Type 2 — Realm-region interlinks ({len(d['regions_projected'])} regions)")
    lines.append("")
    if d["regions_projected"]:
        lines.append("_Realm-regions that **{0}**'s canon-entries project into. "
                     "Each region is a hyperedge connecting all the tradition-paths whose "
                     "canon-entries land in it — paths **{0}** is interlinked with through "
                     "shared realm-coverage._".format(name))
        lines.append("")
        for region, words in sorted(d["regions_projected"].items()):
            lines.append(f"- **{region}**: {', '.join(sorted(words))}")
    else:
        lines.append(f"_**{name}** has no canon-entries projecting into recognized regions yet._")
    lines.append("")

    # 3 — Compound co-occurrence
    lines.append(f"## Type 3 — Compound co-occurrence ({len(d['co_occurrence'])} other traditions)")
    lines.append("")
    if d["co_occurrence"]:
        lines.append("_Other tradition-paths that appear in canonical compounds with **{0}**. "
                     "Each compound is a direct structural interlink — the compound's frontmatter "
                     "binds these donor-paths into one YOUSPEAK building-block._".format(name))
        lines.append("")
        for other_tradition, words in sorted(d["co_occurrence"].items(), key=lambda kv: (-len(kv[1]), kv[0])):
            words_str = ", ".join(sorted(set(words))[:5])
            n = len(set(words))
            more = f" … +{n-5} more" if n > 5 else ""
            lines.append(f"- **{other_tradition}** ({n} compound{'s' if n != 1 else ''}): {words_str}{more}")
    else:
        lines.append(f"_**{name}** does not co-occur with any other tradition in canonical compounds._")
    lines.append("")

    # 4 — Convergence-attestation
    lines.append(f"## Type 4 — Convergence-attestation ({len(d['convergence_hits'])})")
    lines.append("")
    if d["convergence_hits"]:
        lines.append("_Convergence-files that name **{0}** in their attestations list. "
                     "Each is a documented multi-witness hyperedge connecting **{0}** to the other "
                     "traditions attesting the same realm-region._".format(name))
        lines.append("")
        for fname, att in d["convergence_hits"]:
            lines.append(f"- `convergences/{fname}`")
            lines.append(f"  - attestations: {att}")
    else:
        lines.append(f"_**{name}** does not appear in any convergence-file's attestations._")
    lines.append("")

    # 5 — Morpheme-reuse
    total_reuse = sum(m["used_in_count"] for m in d["morpheme_reuses"])
    lines.append(f"## Type 5 — Morpheme-reuse ({len(d['morpheme_reuses'])} morphemes, "
                 f"{total_reuse} canon-entry deployments)")
    lines.append("")
    if d["morpheme_reuses"]:
        lines.append("_Atomic morphemes contributed by **{0}** and their reuse-counts across canon. "
                     "High-reuse morphemes make **{0}** a structural hub in the cathedral's graph "
                     "by indirect-interlinking through compound-co-donors._".format(name))
        lines.append("")
        for m in sorted(d["morpheme_reuses"], key=lambda x: -x["used_in_count"]):
            count = m["used_in_count"]
            if count > 0:
                used_str = ", ".join(m["used_in"][:5])
                more = f" … +{count-5} more" if count > 5 else ""
                lines.append(f"- **{m['latin']}** `{m['codepoint']}` — _{m['meaning']}_ — "
                             f"reused in {count} canon-entr{'ies' if count != 1 else 'y'}: {used_str}{more}")
            else:
                lines.append(f"- **{m['latin']}** `{m['codepoint']}` — _{m['meaning']}_ — "
                             f"_(unused; building-block-ready)_")
    else:
        lines.append(f"_No morphemes from **{name}** in `script/morphemes.json` (Yoruba is a notable case — "
                     f"contributions through canon-frontmatter only, not yet promoted to the central registry)._")
    lines.append("")

    # Graph-position summary
    lines.append("## Graph-position summary")
    lines.append("")
    total_co = sum(len(set(v)) for v in d["co_occurrence"].values())
    lines.append(f"- Suffix-families touched: **{len(d['family_interlinks'])}**")
    lines.append(f"- Realm-regions projected: **{len(d['regions_projected'])}**")
    lines.append(f"- Other-traditions co-occurring: **{len(d['co_occurrence'])}** "
                 f"(across **{sum(len(set(v)) for v in d['co_occurrence'].values())}** compound-edges)")
    lines.append(f"- Convergence-attestations: **{len(d['convergence_hits'])}**")
    lines.append(f"- Morpheme-reuse threads: **{total_reuse}** canon-entry deployments")
    return "\n".join(lines)


def render_signature(word: str) -> str:
    s = compute_signature(word)
    if s.get("status") == "not-in-canon":
        return f"Not in canon: {word}"

    lines = [
        f"# mathema_signature — {s['word']}",
        "",
        f"**Canon entry:** `{s['canon_file']}`",
        "",
        "_Per INTEGRATION.md Block 8, the mathema_signature is the explicit building-block-level "
        "integration of the MATH path (codepoint, vector, cardinality, arity) and the EXISTING-LANGUAGE "
        "path (family-register, donors-class). The six fields are below._",
        "",
        "## The six fields",
        "",
        f"- **codepoint_compound**: `{s['codepoint_compound'] or '(no codepoints found in morphemes.json — donor-morphemes may not yet be registered)'}`",
        f"- **assessment_vector**: `{s['assessment_vector'] or '(v2 6-axis scores not in canon frontmatter)'}`",
        f"- **convergence_cardinality**: `{s['convergence_cardinality'] if s['convergence_cardinality'] is not None else '(no convergence-file referenced)'}`",
        f"- **family**: `{s['family'] or '(no recognized suffix-family)'}`",
        f"- **arity**: `{s['arity']}`",
        f"- **donors_class**: `{s['donors_class']}`",
        "",
        "## Donors",
        "",
    ]
    for tradition, morpheme in s["donors"]:
        lines.append(f"- {tradition or '?'}:{morpheme or '?'}")
    lines.append("")
    lines.append("```yaml")
    lines.append("mathema_signature:")
    if s["codepoint_compound"]:
        lines.append(f"  codepoint_compound: {s['codepoint_compound']}")
    if s["assessment_vector"] and all(v is not None for v in s["assessment_vector"]):
        lines.append(f"  assessment_vector: {s['assessment_vector']}")
    if s["convergence_cardinality"] is not None:
        lines.append(f"  convergence_cardinality: {s['convergence_cardinality']}")
    if s["family"]:
        lines.append(f"  family: {{{s['family']}}}")
    lines.append(f"  arity: {s['arity']}")
    lines.append(f"  donors_class: {s['donors_class']}")
    lines.append("```")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(
        description="YOUSPEAK paths — per-path audit and integration reporting."
    )
    p.add_argument("tradition", nargs="?",
                   help="report on a single tradition (e.g., greek, sumerian, tocharian)")
    p.add_argument("--summary", action="store_true",
                   help="cathedral-wide integration summary")
    p.add_argument("--list-archaeology", action="store_true",
                   help="list every donor-tradition path with canon-status")
    p.add_argument("--list-mathema", action="store_true",
                   help="list every mathema sub-organ path")
    p.add_argument("--gaps", action="store_true",
                   help="list forge-ready paths (archaeology opened, no canon yet)")
    p.add_argument("--unused-morphemes", action="store_true",
                   help="list defined-but-not-yet-deployed atomic morphemes")
    p.add_argument("--signature", metavar="WORD",
                   help="compute mathema_signature for a canon word")
    p.add_argument("--overlap", nargs="+", metavar="T",
                   help="show shared building-blocks across 2+ traditions (per CONFLUENCE.md §IX)")
    p.add_argument("--uniqueness", metavar="T",
                   help="show what only tradition T uniquely contributes (per CONFLUENCE.md §IX)")
    p.add_argument("--realm-aspects", action="store_true",
                   help="list canon entries grouped by realm-region (per BUILDING-BLOCKS.md §III)")
    p.add_argument("--realm-aspect", metavar="REGION",
                   help="list canon entries projecting into a specific realm-region")
    p.add_argument("--interlinks", metavar="T",
                   help="show all five interlink-types for tradition T (per NEXUS.md §I)")
    args = p.parse_args()

    if args.summary:
        print(render_summary())
        return 0
    if args.list_archaeology:
        print(render_list_archaeology())
        return 0
    if args.list_mathema:
        print(render_list_mathema())
        return 0
    if args.gaps:
        print(render_gaps())
        return 0
    if args.unused_morphemes:
        print(render_unused_morphemes())
        return 0
    if args.signature:
        print(render_signature(args.signature))
        return 0
    if args.overlap:
        if len(args.overlap) < 2:
            print("--overlap requires at least 2 traditions", file=sys.stderr)
            return 2
        print(render_overlap(args.overlap))
        return 0
    if args.uniqueness:
        print(render_uniqueness(args.uniqueness))
        return 0
    if args.realm_aspects:
        print(render_realm_aspects())
        return 0
    if args.realm_aspect:
        print(render_realm_aspect(args.realm_aspect))
        return 0
    if args.interlinks:
        print(render_interlinks(args.interlinks))
        return 0
    if args.tradition:
        print(render_tradition_report(args.tradition))
        return 0

    p.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
