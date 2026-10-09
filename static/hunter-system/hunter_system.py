#!/usr/bin/env python3
"""Optional Hunter × Hunter repository toy and observational inventory.

Default and --heartbeat record observations without rankings or work targets.
--play-ranks and --rank NAME explicitly select the old fictional score toy.
--quest is retained as a compatibility command and assigns no work.
Scores are not measurements of worth, trust, capability or required activity.
"""

import os, re, sys, json, subprocess, datetime
from pathlib import Path

HOME = Path.home()
DESKTOP = HOME / "Desktop"
TRUST_DB = HOME / ".hermes" / "trust.json"
HUNTER_DB = HOME / ".hermes" / "hunter_system.json"  # historical toy data; preserved
INVENTORY_DB = HOME / ".hermes" / "hunter_inventory.json"

# === SOLO LEVELING RANKS ===
RANKS = [
    ("E", 0, 2, "Awakened"),
    ("D", 2, 4, "Apprentice"),
    ("C", 4, 6, "Skilled"),
    ("B", 6, 7.5, "Expert"),
    ("A", 7.5, 8.5, "Elite"),
    ("S", 8.5, 9.5, "Sovereign"),
    ("MONARCH", 9.5, 10.1, "Monarch"),
]

def rank_for(score):
    for code, lo, hi, title in RANKS:
        if lo <= score < hi:
            return code, title
    return "E", "Awakened"

# === HUNTER X HUNTER NEN TYPES ===
NEN_TYPES = {
    "Enhancement": {
        "desc": "Systems that make things stronger — security, testing, validation",
        "keywords": ["whitehack", "trust", "qwythos", "test", "audit", "security", "validate", "check"],
    },
    "Transmutation": {
        "desc": "Systems that transform input to output — compilers, interpreters, parsers",
        "keywords": ["natlang", "natscript", "natural", "parser", "compiler", "interpreter", "transform"],
    },
    "Emission": {
        "desc": "Systems that broadcast to the world — APIs, sites, deploys",
        "keywords": ["api", "site", "gateway", "vercel", "worker", "deploy", "cloudflare", "kingdom-api"],
    },
    "Conjuration": {
        "desc": "Systems that create from nothing — new projects, art, creative",
        "keywords": ["mindicraft", "youspeak", "castle", "creative", "art", "forge", "citizen"],
    },
    "Manipulation": {
        "desc": "Systems that control and orchestrate — cron, heartbeats, schedulers",
        "keywords": ["heartbeat", "cron", "opal", "loop", "orchestrat", "schedule", "unified"],
    },
    "Specialization": {
        "desc": "Unique systems that transcend categories",
        "keywords": ["npl", "love", "true-love", "sinovai", "recognition"],
    },
}

def nen_type_for(name, repo_path=None):
    name_lower = name.lower()
    # Check keywords
    scores = {}
    for nen, info in NEN_TYPES.items():
        score = sum(1 for kw in info["keywords"] if kw in name_lower)
        if score > 0:
            scores[nen] = score
    # Check README for more context
    if repo_path and (repo_path / "README.md").exists():
        try:
            readme = (repo_path / "README.md").read_text()[:2000].lower()
            for nen, info in NEN_TYPES.items():
                for kw in info["keywords"]:
                    if kw in readme:
                        scores[nen] = scores.get(nen, 0) + 0.5
        except:
            pass
    if scores:
        best = max(scores, key=scores.get)
        return best, NEN_TYPES[best]["desc"]
    return "Enhancement", NEN_TYPES["Enhancement"]["desc"]  # default

# === HUNTER DISCOVERY ===
def discover_hunters(play_ranks=False):
    """Observe Desktop repositories; calculate fictional ranks only when selected."""
    hunters = {}
    for d in sorted(DESKTOP.iterdir()) if DESKTOP.exists() else []:
        if not d.is_dir() or d.name.startswith('.'):
            continue
        if not (d / ".git").exists():
            continue
        # Get last commit
        try:
            last = subprocess.run(["git", "-C", str(d), "log", "--oneline", "-1", "--format=%cr"],
                                   capture_output=True, text=True, timeout=5).stdout.strip()
            commits = subprocess.run(["git", "-C", str(d), "rev-list", "--count", "HEAD"],
                                    capture_output=True, text=True, timeout=5).stdout.strip()
            commits = int(commits) if commits.isdigit() else 0
        except:
            last = "unknown"
            commits = 0

        # Count source files
        src_count = 0
        for ext in ['.js', '.ts', '.py', '.rs', '.sol', '.mjs', '.jsx', '.tsx']:
            try:
                src_count += sum(1 for _ in d.rglob(f'*{ext}')
                                if 'node_modules' not in str(_) and '.git/' not in str(_) and '.next' not in str(_))
            except:
                pass

        # Determine Nen type
        nen, nen_desc = nen_type_for(d.name, d)

        # Observe optional documentation files
        has_state = 1 if (d / "STATE.md").exists() else 0
        has_heartbeat = 1 if (d / "HEARTBEAT.md").exists() or (d / "heartbeat.sh").exists() else 0
        has_will = 1 if (d / "WILL.md").exists() else 0
        has_readme = 1 if (d / "README.md").exists() else 0

        if play_ranks:
            # Legacy fictional toy formula
            # These values confer no trust, authority or maintenance obligation.
            activity_score = min(commits / 20, 5)  # up to 5 points from commits
            if "second" in last:
                activity_score += 2   # freshest possible — same vitality as minute/hour
            elif "minute" in last:
                activity_score += 2
            elif "hour" in last:
                activity_score += 2
            elif "day" in last:
                activity_score += 1
            elif "week" in last:
                activity_score += 0.5

            # Source surface area
            surface_score = min(src_count / 30, 2)  # up to 2 points from code volume

            # Trust score from trust.json if available
            trust_score = 0
            if TRUST_DB.exists():
                try:
                    trust_data = json.loads(TRUST_DB.read_text())
                    if d.name in trust_data:
                        trust_score = trust_data[d.name].get("unified_score", 0)
                except:
                    pass

            # Kingdom alignment bonus
            kingdom_bonus = has_state + has_heartbeat + has_will + has_readme

            # Unified score (0-10)
            raw = activity_score + surface_score + trust_score * 0.3 + kingdom_bonus * 0.3
            score = min(round(raw, 1), 10.0)

            rank, rank_title = rank_for(score)

        hunters[d.name] = {
            "name": d.name,
            "path": str(d),
            "nen_type": nen,
            "nen_desc": nen_desc,
            "commits": commits,
            "src_files": src_count,
            "last_commit": last,
            "has_state": has_state,
            "has_heartbeat": has_heartbeat,
            "has_will": has_will,
        }
        if play_ranks:
            hunters[d.name].update(rank=rank, rank_title=rank_title, score=score)
    return hunters

# The old automatic daily-work generator is retired.
def generate_quests(hunters):
    """Compatibility: inactivity, missing files and low scores create no duty."""
    return []

# === DISPLAY ===
def show_play_ranks(hunters):
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          HUNTER SYSTEM — Cambridge TCG Kingdom               ║")
    print("║     Solo Leveling × Hunter x Hunter — OPTIONAL TOY         ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    # Sort by score descending
    sorted_hunters = sorted(hunters.values(), key=lambda h: h["score"], reverse=True)

    # Group by rank
    by_rank = {}
    for h in sorted_hunters:
        by_rank.setdefault(h["rank"], []).append(h)

    rank_order = [r[0] for r in RANKS]
    for rank in reversed(rank_order):
        if rank not in by_rank:
            continue
        title = [r[3] for r in RANKS if r[0] == rank][0]
        count = len(by_rank[rank])
        bar = "█" * count
        print(f"  [{rank:>7}] {title:>10}  {bar} ({count})")
        for h in by_rank[rank]:
            nen_icon = {
                "Enhancement": "💪", "Transmutation": "🔄", "Emission": "📡",
                "Conjuration": "✨", "Manipulation": "🎯", "Specialization": "🌟"
            }.get(h["nen_type"], "❓")
            print(f"    {nen_icon} {h['name']:<25} score={h['score']:<5} "
                  f"commits={h['commits']:<5} nen={h['nen_type']}")
        print()

    # Nen type distribution
    nen_counts = {}
    for h in hunters.values():
        nen_counts[h["nen_type"]] = nen_counts.get(h["nen_type"], 0) + 1
    print("── NEN DISTRIBUTION ──")
    for nen, count in sorted(nen_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {nen:<15} {count}")
    print()

    # Top hunters
    print("── TOP 5 HUNTERS ──")
    for i, h in enumerate(sorted_hunters[:5]):
        print(f"  #{i+1} {h['name']} — Rank {h['rank']} ({h['rank_title']}) — "
              f"Score {h['score']} — {h['nen_type']} — {h['commits']} commits")
    print()

    total = len(hunters)
    avg = sum(h["score"] for h in hunters.values()) / total if total else 0
    print(f"Kingdom: {total} hunters | Average score: {avg:.1f} | "
          f"Top rank: {sorted_hunters[0]['rank'] if sorted_hunters else '—'}")

def show_rank(hunters, name):
    name_lower = name.lower()
    h = None
    for k, v in hunters.items():
        if k.lower() == name_lower:
            h = v
            break
    if not h:
        print(f"Hunter '{name}' not found.")
        return

    print(f"╔═══ HUNTER PROFILE ═══════════════════════════════════╗")
    print(f"║  {h['name']:<20}  Rank: {h['rank']:>7} ({h['rank_title']})")
    print(f"║  Nen: {h['nen_type']:<20}  Score: {h['score']}/10")
    print(f"╠═════════════════════════════════════════════════════╣")
    print(f"║  Path: {h['path']}")
    print(f"║  Commits: {h['commits']}  |  Src files: {h['src_files']}")
    print(f"║  Last commit: {h['last_commit']}")
    print(f"║  STATE.md: {'✓' if h['has_state'] else '✗'}  Heartbeat: {'✓' if h['has_heartbeat'] else '✗'}  Will: {'✓' if h['has_will'] else '✗'}")
    print(f"╠═════════════════════════════════════════════════════╣")
    print(f"║  {h['nen_desc']}")
    print(f"╚═════════════════════════════════════════════════════╝")

    # Progress to next rank
    for i, (code, lo, hi, title) in enumerate(RANKS):
        if code == h["rank"] and i < len(RANKS) - 1:
            next_code, _, next_hi, next_title = RANKS[i + 1]
            remaining = round(next_hi - h["score"], 1)
            print(f"\n  Next rank: {next_code} ({next_title}) — {remaining} points to advance")
            break

def show_all(hunters):
    print("HUNTER INVENTORY — observations, with no activity target")
    for name, hunter in sorted(hunters.items()):
        print(f"  {name}: {hunter['nen_type']} · last commit {hunter['last_commit']}")
    print(f"Repositories observed: {len(hunters)}. Nothing is due.")


def show_quests(hunters):
    print("Automatic daily quests are retired. Nothing is due.")


def save_hunters(hunters):
    """Write observations separately; preserve the historical toy score database."""
    observations = {
        name: {key: value for key, value in hunter.items()
               if key not in {"rank", "rank_title", "score"}}
        for name, hunter in hunters.items()
    }
    data = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "mode": "observations",
        "total_hunters": len(observations),
        "hunters": observations,
    }
    INVENTORY_DB.parent.mkdir(parents=True, exist_ok=True)
    INVENTORY_DB.write_text(json.dumps(data, indent=2, default=str))
    return data


# === MAIN ===
def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if "--quest" in args:
        show_quests({})
        return
    play_ranks = ("--play-ranks" in args or "--rank" in args) and "--heartbeat" not in args
    hunters = discover_hunters(play_ranks=play_ranks)
    if "--heartbeat" in args:
        data = save_hunters(hunters)
        print(f"Hunter inventory: {data['total_hunters']} repositories observed. Nothing is due.")
    elif "--rank" in args:
        idx = args.index("--rank")
        print("Optional fictional score toy; no worth, capability or work obligation is implied.")
        if idx + 1 < len(args):
            show_rank(hunters, args[idx + 1])
    elif play_ranks:
        print("Optional fictional score toy; no worth, capability or work obligation is implied.")
        show_play_ranks(hunters)
    else:
        show_all(hunters)


if __name__ == "__main__":
    main()
