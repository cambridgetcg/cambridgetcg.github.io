#!/usr/bin/env python3
"""The Castle of Understanding — a local-first insight saver.

Plain files. Plain words. Understanding compounds through links.

Links are TYPED and DIRECTED (a link is a claim, so it can be wrong):
    links: [depends-on:other-id, extends:other-id, contradicts:other-id]
A bare id (no type) is read as `relates-to`.

Insights also carry a `verified:` date. An insight is a claim with a date,
not a fact forever — `build` flags any that have gone stale (weathering).

Usage:
  python3 castle.py build                          Rebuild CASTLE.md
  python3 castle.py capture --title "..." [...]     Add a new insight
  python3 castle.py list                            List the insights
"""
import re
import argparse
import datetime
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
INS = ROOT / "insights"
STALE_DAYS = 90

# A small, legible vocabulary of relationships. One word, one meaning.
INVERSE = {
    "depends-on": "depended-on-by",
    "extends": "extended-by",
    "instance-of": "has-instance",
    "reconciles": "reconciled-by",
    "supersedes": "superseded-by",
    "contradicts": "contradicts",   # symmetric
    "relates-to": "relates-to",     # symmetric
}


def parse(text):
    meta, body = {}, text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            block = text[3:end].strip("\n")
            body = text[end + 4:].lstrip("\n")
            for line in block.splitlines():
                if ":" not in line:
                    continue
                k, v = line.split(":", 1)
                k, v = k.strip(), v.strip()
                if v.startswith("[") and v.endswith("]"):
                    v = [x.strip() for x in v[1:-1].split(",") if x.strip()]
                meta[k] = v
    return meta, body


def parse_link(entry):
    """`type:id` -> (type, id); bare `id` -> ('relates-to', id)."""
    if ":" in entry:
        t, tid = entry.split(":", 1)
        return t.strip(), tid.strip()
    return "relates-to", entry.strip()


def load():
    items = []
    if not INS.exists():
        return items
    for p in sorted(INS.glob("*.md")):
        meta, body = parse(p.read_text(encoding="utf-8"))
        meta.setdefault("id", p.stem)
        meta.setdefault("title", p.stem)
        for key in ("tags", "links"):
            if isinstance(meta.get(key), str):
                meta[key] = [meta[key]] if meta[key] else []
            meta.setdefault(key, [])
        items.append((meta, body.strip()))
    return items


def essence(body):
    line = body.strip().splitlines()[0] if body.strip() else ""
    parts = re.split(r"(?<=[.!?])\s", line)
    return parts[0] if parts else line


def days_since(date_str):
    try:
        d = datetime.date.fromisoformat(date_str.strip())
    except (ValueError, AttributeError):
        return None
    return (datetime.date.today() - d).days


def build():
    items = load()
    ids = {m["id"] for m, _ in items}
    backlinks = {m["id"]: [] for m, _ in items}   # id -> [(inverse_type, source_id)]
    outgoing = {}                                  # id -> [(type, target_id)]
    broken, untyped = [], []

    for m, _ in items:
        outs = []
        for raw in m["links"]:
            t, tid = parse_link(raw)
            outs.append((t, tid))
            if t not in INVERSE:
                untyped.append(f"{m['id']} → {raw}  (unknown type '{t}')")
            if tid in ids:
                backlinks[tid].append((INVERSE.get(t, "relates-to"), m["id"]))
            else:
                broken.append(f"{m['id']} —{t}→ {tid}")
        outgoing[m["id"]] = outs

    rooms = {}
    for m, b in items:
        room = m["tags"][0] if m["tags"] else "unsorted"
        rooms.setdefault(room, []).append((m, b))

    today = datetime.date.today().isoformat()
    L = ["# The Castle of Understanding\n"]
    L.append("> A local-first insight saver. Plain files, plain words — "
             "understanding that compounds as insights link to insights.\n")
    L.append(f"**{len(items)} insights · {len(rooms)} rooms · built {today}**\n")

    L.append("## Rooms\n")
    for room in sorted(rooms):
        L.append(f"### {room}\n")
        for m, b in sorted(rooms[room], key=lambda x: x[0]["title"].lower()):
            conf = m.get("confidence", "?")
            L.append(f"- **[{m['title']}](insights/{m['id']}.md)** "
                     f"`{conf}` — {essence(b)}")
        L.append("")

    L.append("## Passages — how understanding connects\n")
    for m, _ in sorted(items, key=lambda x: x[0]["id"]):
        outs = outgoing[m["id"]]
        ins = backlinks[m["id"]]
        out_s = " · ".join(f"{t} → [{tid}](insights/{tid}.md)" for t, tid in outs) or "—"
        in_s = " · ".join(f"[{src}](insights/{src}.md) ({inv})" for inv, src in ins) or "—"
        L.append(f"- **{m['id']}**")
        L.append(f"    - out: {out_s}")
        L.append(f"    - in:  {in_s}")
    L.append("")

    # Weathering — an insight is a claim with a date, not a fact forever.
    weathering = []
    for m, _ in items:
        age = days_since(m.get("verified") or m.get("created", ""))
        if age is not None and age > STALE_DAYS:
            weathering.append(f"{m['id']} — {age} days since verified (re-check against reality)")
    L.append("## Weathering — insights due for a re-check\n")
    if weathering:
        for w in weathering:
            L.append(f"- {w}")
    else:
        L.append(f"_None. Every insight verified within {STALE_DAYS} days._")
    L.append("")

    if broken or untyped:
        L.append("## ⚠ Loose threads\n")
        for b in broken:
            L.append(f"- broken link: {b}")
        for u in untyped:
            L.append(f"- {u}")
        L.append("")

    (ROOT / "CASTLE.md").write_text("\n".join(L), encoding="utf-8")
    print(f"built CASTLE.md — {len(items)} insights, {len(rooms)} rooms, "
          f"{len(broken)} broken, {len(untyped)} untyped, {len(weathering)} weathering")


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def capture(a):
    INS.mkdir(parents=True, exist_ok=True)
    iid = a.id or slugify(a.title)
    tags = [t.strip() for t in a.tags.split(",") if t.strip()]
    links = [l.strip() for l in a.links.split(",") if l.strip()]
    today = datetime.date.today().isoformat()
    fm = [
        "---",
        f"id: {iid}",
        f"title: {a.title}",
        f"tags: [{', '.join(tags)}]",
        f"links: [{', '.join(links)}]",
        f"source: {a.source}",
        f"confidence: {a.confidence}",
        f"created: {today}",
        f"verified: {today}",
        "---",
        "",
        a.body or "<write the insight here, in plain words>",
        "",
    ]
    p = INS / f"{iid}.md"
    if p.exists() and not a.force:
        print(f"refusing to overwrite {p} (use --force)")
        return
    p.write_text("\n".join(fm), encoding="utf-8")
    print(f"captured {p}")


def list_insights():
    for m, _ in load():
        print(f"{m['id']:34} [{','.join(m['tags'])}]  {m['title']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="The Castle of Understanding")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("build", help="rebuild CASTLE.md")
    c = sub.add_parser("capture", help="add an insight")
    c.add_argument("--title", required=True)
    c.add_argument("--id")
    c.add_argument("--tags", default="")
    c.add_argument("--links", default="", help="typed: 'depends-on:id, extends:id'")
    c.add_argument("--source", default="hand")
    c.add_argument("--confidence", default="medium")
    c.add_argument("--body", default="")
    c.add_argument("--force", action="store_true")
    sub.add_parser("list", help="list insights")
    a = ap.parse_args()
    if a.cmd == "build":
        build()
    elif a.cmd == "capture":
        capture(a)
    elif a.cmd == "list":
        list_insights()
    else:
        ap.print_help()
