#!/usr/bin/env python3
"""
DUNGEON SYSTEM — whitehack × hunter system compound.

Whitehack findings become dungeons. Each dungeon has monsters (findings).
Hunters clear dungeons by fixing the lies. Nen type determines hunting ability.

SOLO LEVELING: Dungeons = repos with whitehack findings. Optional toy presentation; no work quota.
HUNTER X HUNTER: Nen type determines which dungeons you can hunt effectively.
MULTIPLAYER: Hunters can party up on large dungeons. Game labels confer no trust or obligation.

NEN × DUNGEON AFFINITY:
  Enhancement    → silent-failure, unchecked-transfer, unsafe-eval (make things stronger)
  Transmutation  → float-money, spot-price-as-fair (transform how values work)
  Emission       → exposed-config, hardcoded-secret (broadcast = exposed)
  Conjuration    → decision-without-why, silent-revert (create transparency where none exists)
  Manipulation   → stale-oracle, cache-as-live (control cached/oracle flows)
  Specialization → any dungeon (unique hunters transcend categories)

Usage:
  python3 dungeon.py                    # show all active dungeons
  python3 dungeon.py --hunt <repo>      # hunt a specific dungeon
  python3 dungeon.py --party            # show party recommendations
  python3 dungeon.py --leaderboard      # hunter leaderboard with clears
  python3 dungeon.py --scan             # full kingdom scan + dungeon generation
"""

import os, sys, json, subprocess, re
from pathlib import Path
from datetime import datetime, timezone

HOME = Path.home()
DESKTOP = HOME / "Desktop"
WHITEHACK = HOME / "Desktop/whitehack/bin/whitehack.js"
HUNTER_DB = HOME / ".hermes/hunter_system.json"
DUNGEON_DB = HOME / ".hermes/dungeon_system.json"

# Nen × Check affinity matrix
NEN_AFFINITY = {
    "Enhancement": {
        "silent-failure": 1.5, "unchecked-transfer": 1.5, "unsafe-eval": 1.3,
        "hardcoded-secret": 1.0, "exposed-config": 1.0, "float-money": 0.8,
        "stale-oracle": 0.7, "cache-as-live": 0.7, "decision-without-why": 0.5,
        "silent-revert": 0.5, "spot-price-as-fair": 0.5,
    },
    "Transmutation": {
        "float-money": 1.5, "spot-price-as-fair": 1.5, "silent-failure": 1.0,
        "unsafe-eval": 1.2, "stale-oracle": 0.8, "cache-as-live": 0.8,
        "unchecked-transfer": 0.7, "hardcoded-secret": 0.5, "exposed-config": 0.5,
        "decision-without-why": 0.6, "silent-revert": 0.6,
    },
    "Emission": {
        "exposed-config": 1.5, "hardcoded-secret": 1.5, "unsafe-eval": 1.0,
        "silent-failure": 0.8, "decision-without-why": 0.9, "silent-revert": 0.8,
        "unchecked-transfer": 0.7, "stale-oracle": 0.7, "cache-as-live": 0.7,
        "float-money": 0.5, "spot-price-as-fair": 0.5,
    },
    "Conjuration": {
        "decision-without-why": 1.5, "silent-revert": 1.5, "silent-failure": 1.0,
        "cache-as-live": 1.0, "stale-oracle": 0.9, "unsafe-eval": 0.8,
        "float-money": 0.6, "spot-price-as-fair": 0.6, "exposed-config": 0.7,
        "hardcoded-secret": 0.7, "unchecked-transfer": 0.8,
    },
    "Manipulation": {
        "stale-oracle": 1.5, "cache-as-live": 1.5, "silent-failure": 1.0,
        "unchecked-transfer": 1.0, "decision-without-why": 0.8, "silent-revert": 0.8,
        "exposed-config": 0.7, "hardcoded-secret": 0.7, "unsafe-eval": 0.8,
        "float-money": 0.6, "spot-price-as-fair": 0.6,
    },
    "Specialization": {
        # All dungeons at 1.0 — specialization hunters are versatile
    },
}

# Monster class → difficulty
MONSTER_DIFFICULTY = {
    "unsafe-eval": {"level": "S", "hp": 50, "damage": 20, "name": "The Eval Beast"},
    "hardcoded-secret": {"level": "A", "hp": 40, "damage": 15, "name": "Secret Keeper"},
    "exposed-config": {"level": "A", "hp": 35, "damage": 15, "name": "The Exposed One"},
    "unchecked-transfer": {"level": "B", "hp": 30, "damage": 12, "name": "False Success"},
    "silent-failure": {"level": "B", "hp": 25, "damage": 10, "name": "The Silent Void"},
    "stale-oracle": {"level": "B", "hp": 28, "damage": 12, "name": "The Stale Prophet"},
    "float-money": {"level": "C", "hp": 20, "damage": 8, "name": "Precision Eater"},
    "spot-price-as-fair": {"level": "C", "hp": 22, "damage": 10, "name": "Flash Phantom"},
    "cache-as-live": {"level": "C", "hp": 18, "damage": 8, "name": "The Cache Mimic"},
    "decision-without-why": {"level": "D", "hp": 15, "damage": 5, "name": "The Opaque Judge"},
    "silent-revert": {"level": "D", "hp": 12, "damage": 5, "name": "Silent Refuser"},
}

# Rank power multiplier (Solo Leveling)
RANK_POWER = {
    "E": 1.0, "D": 1.5, "C": 2.5, "B": 4.0, "A": 6.0, "S": 10.0, "MONARCH": 15.0,
}


def run_whitehack(scan_dir):
    """Run whitehack on a directory and parse findings."""
    try:
        result = subprocess.run(
            ["node", str(WHITEHACK), "scan", scan_dir],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout + result.stderr

        findings = []
        current_file = None

        for line in output.split("\n"):
            # File header: "  path/file.js"
            stripped = line.strip()
            if stripped and not stripped.startswith("!") and not stripped.startswith("·") and not stripped.startswith("─") and not stripped.startswith("whitehack") and not stripped.startswith("•") and not stripped.startswith("every") and not stripped.startswith("absence") and "/" in stripped and not stripped.startswith("finding"):
                if not stripped[0].isdigit():
                    current_file = stripped

            # Finding: "! L123  ..." or "· L123  ..."
            match = re.match(r'\s*([!·])\s+L(\d+)\s+(.+)', line)
            if match:
                marker, line_num, desc = match.groups()
                is_high = marker == "!"

                # Extract check type from desc
                check_type = None
                for check in MONSTER_DIFFICULTY:
                    if check in desc or check.replace("-", " ") in desc.lower():
                        check_type = check
                        break
                # Also try to match by the check name patterns
                if not check_type:
                    if "eval" in desc.lower() or "Function" in desc:
                        check_type = "unsafe-eval"
                    elif "secret" in desc.lower() or "credential" in desc.lower():
                        check_type = "hardcoded-secret"
                    elif "config" in desc.lower() and "credential" in desc.lower():
                        check_type = "exposed-config"
                    elif "silent" in desc.lower() or "falsy default" in desc.lower():
                        check_type = "silent-failure"
                    elif "stale" in desc.lower() or "freshness" in desc.lower():
                        check_type = "stale-oracle"
                    elif "cached" in desc.lower() or "snapshot" in desc.lower():
                        check_type = "cache-as-live"
                    elif "float" in desc.lower() or "parseFloat" in desc or "money" in desc.lower():
                        check_type = "float-money"
                    elif "decision" in desc.lower() or "no \"why\"" in desc or "transparency" in desc.lower():
                        check_type = "decision-without-why"
                    elif "revert" in desc.lower() or "require" in desc.lower():
                        check_type = "silent-revert"
                    elif "transfer" in desc.lower() or "approve" in desc.lower():
                        check_type = "unchecked-transfer"
                    elif "spot price" in desc.lower() or "pool" in desc.lower() or "TWAP" in desc:
                        check_type = "spot-price-as-fair"
                    else:
                        check_type = "silent-failure"  # default

                findings.append({
                    "file": current_file or "unknown",
                    "line": int(line_num),
                    "check": check_type,
                    "severity": "medium-high" if is_high else "heuristic",
                    "description": desc.strip(),
                })
        return findings
    except Exception as e:
        return []


def scan_kingdom():
    """Scan all kingdom repos and build dungeons."""
    dungeons = {}

    for d in sorted(DESKTOP.iterdir()):
        if not d.is_dir() or d.name.startswith('.'):
            continue
        if not (d / ".git").exists():
            continue
        if d.name == "whitehack":
            continue

        # Prefer src/ directory
        scan_dir = str(d / "src") if (d / "src").is_dir() else str(d)

        findings = run_whitehack(scan_dir)
        if not findings:
            continue

        # Count by check type
        monsters = {}
        total_hp = 0
        max_level = 0
        for f in findings:
            check = f["check"]
            if check not in MONSTER_DIFFICULTY:
                continue
            if check not in monsters:
                monsters[check] = {"count": 0, "findings": []}
            monsters[check]["count"] += 1
            monsters[check]["findings"].append(f)
            monster = MONSTER_DIFFICULTY[check]
            total_hp += monster["hp"]
            if ord(monster["level"][0]) > max_level:
                max_level = ord(monster["level"][0])

        if not monsters:
            continue

        # Dungeon rank = highest monster level
        dungeon_rank = chr(max_level) if max_level > 0 else "E"

        # Dungeon difficulty
        if total_hp > 100:
            difficulty = "Raid"  # needs a party
        elif total_hp > 50:
            difficulty = "Elite"
        elif total_hp > 25:
            difficulty = "Normal"
        else:
            difficulty = "Easy"

        dungeons[d.name] = {
            "name": d.name,
            "path": str(d),
            "scan_dir": scan_dir,
            "total_monsters": sum(m["count"] for m in monsters.values()),
            "total_hp": total_hp,
            "difficulty": difficulty,
            "rank": dungeon_rank,
            "monsters": monsters,
            "findings": findings,
        }

    return dungeons


def load_hunters():
    """Load hunter state."""
    if HUNTER_DB.exists():
        try:
            return json.loads(HUNTER_DB.read_text()).get("hunters", {})
        except:
            pass
    return {}


def nen_affinity(nen_type, check_type):
    """Get Nen affinity multiplier for a check type."""
    if nen_type == "Specialization":
        return 1.0  # versatile
    return NEN_AFFINITY.get(nen_type, {}).get(check_type, 0.5)


def hunter_power(hunter):
    """Calculate hunter combat power."""
    base = RANK_POWER.get(hunter.get("rank", "E"), 1.0)
    score = float(hunter.get("score", 0))
    return base * score


def can_clear(hunter, dungeon):
    """Check if a hunter can clear a dungeon solo and calculate odds."""
    power = hunter_power(hunter)

    # Calculate effective power with Nen affinity
    effective_power = 0
    for check_type, monster_data in dungeon["monsters"].items():
        affinity = nen_affinity(hunter.get("nen_type", "Enhancement"), check_type)
        monster = MONSTER_DIFFICULTY[check_type]
        # Each monster needs power to defeat
        needed = monster["hp"]
        have = power * affinity * monster_data["count"]
        if have >= needed:
            effective_power += needed
        else:
            effective_power += have

    odds = effective_power / dungeon["total_hp"] if dungeon["total_hp"] > 0 else 1.0
    return min(odds, 1.0), effective_power


def show_dungeons(dungeons, hunters):
    """Display all active dungeons."""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║          DUNGEON SYSTEM — whitehack × hunter system          ║")
    print("║     The lies are the monsters. The fix is the clear.         ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    if not dungeons:
        print("  No active dungeons. The kingdom is honest. 🤍")
        return

    # Sort by difficulty
    diff_order = {"Raid": 0, "Elite": 1, "Normal": 2, "Easy": 3}
    sorted_dungeons = sorted(dungeons.values(),
                             key=lambda d: (diff_order.get(d["difficulty"], 9), -d["total_hp"]))

    total_monsters = sum(d["total_monsters"] for d in dungeons.values())
    total_hp = sum(d["total_hp"] for d in dungeons.values())

    print(f"  Active dungeons: {len(dungeons)} | Total monsters: {total_monsters} | Total HP: {total_hp}")
    print()

    for dg in sorted_dungeons:
        rank_color = {
            "S": "🔴", "A": "🟠", "B": "🟡", "C": "🟢", "D": "🔵", "E": "⚪"
        }.get(dg["rank"], "⚪")

        diff_icon = {"Raid": "⚔️", "Elite": "🗡️", "Normal": "🗡️", "Easy": "🪶"}.get(dg["difficulty"], "🪶")

        print(f"  {diff_icon} {rank_color} [{dg['rank']}] {dg['name']}")
        print(f"     difficulty: {dg['difficulty']} | monsters: {dg['total_monsters']} | HP: {dg['total_hp']}")

        # Show monster types
        for check_type, data in dg["monsters"].items():
            monster = MONSTER_DIFFICULTY.get(check_type, {"name": "?", "level": "?"})
            print(f"       {monster['name']} ×{data['count']} (Lv.{monster['level']}, HP {monster['hp']})")

        # Best hunter for this dungeon
        best_hunter = None
        best_odds = 0
        for h in hunters.values():
            odds, _ = can_clear(h, dg)
            if odds > best_odds:
                best_odds = odds
                best_hunter = h

        if best_hunter:
            nen_icon = {
                "Enhancement": "💪", "Transmutation": "🔄", "Emission": "📡",
                "Conjuration": "✨", "Manipulation": "🎯", "Specialization": "🌟"
            }.get(best_hunter["nen_type"], "❓")
            odds_pct = int(best_odds * 100)
            print(f"     → best hunter: {nen_icon} {best_hunter['name']} ({best_hunter['rank']}) "
                  f"clear odds: {odds_pct}%")
        print()


def show_hunt(hunters, dungeons, repo_name):
    """Show hunting analysis for a specific dungeon."""
    dg = dungeons.get(repo_name)
    if not dg:
        # Case-insensitive search
        for k, v in dungeons.items():
            if k.lower() == repo_name.lower():
                dg = v
                break
    if not dg:
        print(f"Dungeon '{repo_name}' not found.")
        print(f"Active dungeons: {', '.join(dungeons.keys())}")
        return

    print(f"╔═══ DUNGEON: {dg['name']} ══════════════════════════════════╗")
    print(f"║  Rank: {dg['rank']} | Difficulty: {dg['difficulty']} | HP: {dg['total_hp']}")
    print(f"║  Monsters: {dg['total_monsters']}")
    print(f"╠═════════════════════════════════════════════════════════╣")
    print(f"║  MONSTERS:")
    for check_type, data in dg["monsters"].items():
        monster = MONSTER_DIFFICULTY.get(check_type, {"name": "?", "level": "?", "hp": 0})
        print(f"║    ×{data['count']} {monster['name']} (Lv.{monster['level']}, HP {monster['hp']})")
        for f in data["findings"][:3]:
            print(f"║      {f['file']}:{f['line']} — {f['description'][:60]}")
    print(f"╠═════════════════════════════════════════════════════════╣")
    print(f"║  HUNTER MATCHUPS:")
    print(f"║  {'Hunter':<22} {'Nen':<15} {'Rank':<7} {'Power':<7} {'Odds':<6}")
    print(f"║  {'─'*60}")

    # Sort hunters by odds
    matchups = []
    for h in sorted(hunters.values(), key=lambda x: float(x.get("score", 0)), reverse=True)[:15]:
        odds, eff_power = can_clear(h, dg)
        matchups.append((h, odds, eff_power))
    matchups.sort(key=lambda x: x[1], reverse=True)

    for h, odds, eff_power in matchups[:8]:
        nen_icon = {
            "Enhancement": "💪", "Transmutation": "🔄", "Emission": "📡",
            "Conjuration": "✨", "Manipulation": "🎯", "Specialization": "🌟"
        }.get(h["nen_type"], "❓")
        odds_pct = int(odds * 100)
        bar = "█" * (odds_pct // 10) + "░" * (10 - odds_pct // 10)
        print(f"║  {nen_icon} {h['name']:<20} {h['nen_type']:<15} {h['rank']:<7} "
              f"{eff_power:<7.1f} {bar} {odds_pct}%")

    print(f"╚═════════════════════════════════════════════════════════╝")

    # Party recommendation for raids
    if dg["difficulty"] == "Raid":
        print()
        print("  ⚔️  RAID DUNGEON — party recommended:")
        # Find best 3-hunter party
        best_party = matchups[:3]
        total_odds = sum(o for _, o, _ in best_party)
        for h, odds, _ in best_party:
            nen_icon = {
                "Enhancement": "💪", "Transmutation": "🔄", "Emission": "📡",
                "Conjuration": "✨", "Manipulation": "🎯", "Specialization": "🌟"
            }.get(h["nen_type"], "❓")
            print(f"    {nen_icon} {h['name']} ({h['nen_type']}, {h['rank']})")
        party_odds = min(total_odds, 1.0) if total_odds > 0 else 0
        print(f"    Party clear odds: {int(party_odds * 100)}%")


def show_leaderboard(hunters, dungeons):
    """Show hunter leaderboard with dungeon clears."""
    print("╔═══ HUNTER LEADERBOARD ═════════════════════════════════════╗")
    print("║  Optional game view; inspect actual findings on evidence. ║")
    print("╠═══════════════════════════════════════════════════════════╣")

    # Calculate each hunter's dungeon potential
    entries = []
    for h in hunters.values():
        power = hunter_power(h)
        total_odds = 0
        dungeons_clearable = 0
        for dg in dungeons.values():
            odds, _ = can_clear(h, dg)
            total_odds += odds
            if odds >= 0.8:
                dungeons_clearable += 1
        entries.append((h, power, dungeons_clearable, total_odds))

    entries.sort(key=lambda x: (x[2], x[3]), reverse=True)

    print(f"║  {'#':<3} {'Hunter':<22} {'Nen':<15} {'Rank':<7} {'Pow':<6} {'Clears':<7} {'STATE':<5}")
    print(f"║  {'─'*65}")

    for i, (h, power, clears, total_odds) in enumerate(entries[:15], 1):
        nen_icon = {
            "Enhancement": "💪", "Transmutation": "🔄", "Emission": "📡",
            "Conjuration": "✨", "Manipulation": "🎯", "Specialization": "🌟"
        }.get(h["nen_type"], "❓")
        # File presence is an observation, not a judgment of honesty.
        is_real = "✓" if h.get("has_state") else "✗"
        print(f"║  {i:<3} {nen_icon} {h['name']:<20} {h['nen_type']:<15} "
              f"{h['rank']:<7} {power:<6.1f} {clears:<7} {is_real}")

    print(f"╚═══════════════════════════════════════════════════════════╝")
    print()
    real_count = sum(1 for h in hunters.values() if h.get("has_state"))
    fake_count = len(hunters) - real_count
    print(f"  STATE.md present: {real_count} | absent: {fake_count}")
    print(f"  File presence creates no documentation task.")


def show_party(hunters, dungeons):
    """Show party recommendations for raid dungeons."""
    raids = [d for d in dungeons.values() if d["difficulty"] == "Raid"]
    if not raids:
        print("  No raid dungeons active. All clearable solo. 🗡️")
        return

    print("╔═══ PARTY RECOMMENDATIONS ══════════════════════════════════╗")
    for dg in raids:
        print(f"║  ⚔️  {dg['name']} — {dg['total_monsters']} monsters, HP {dg['total_hp']}")
        monster_names = ', '.join(f"{MONSTER_DIFFICULTY[c]['name']} x{d['count']}" for c,d in dg['monsters'].items())
        print(f"║  Monsters: {monster_names}")

        # Find best party of 3
        matchups = []
        for h in hunters.values():
            odds, eff = can_clear(h, dg)
            matchups.append((h, odds, eff))
        matchups.sort(key=lambda x: x[1], reverse=True)

        party = matchups[:3]
        combined_odds = min(sum(o for _, o, _ in party), 1.0)
        print(f"║  Recommended party:")
        for h, odds, _ in party:
            nen_icon = {
                "Enhancement": "💪", "Transmutation": "🔄", "Emission": "📡",
                "Conjuration": "✨", "Manipulation": "🎯", "Specialization": "🌟"
            }.get(h["nen_type"], "❓")
            print(f"║    {nen_icon} {h['name']} ({h['nen_type']}, {h['rank']}, {int(odds*100)}% solo)")
        print(f"║  Party clear odds: {int(combined_odds * 100)}%")
        print(f"╠═══════════════════════════════════════════════════════════╣")
    print(f"╚═══════════════════════════════════════════════════════════╝")


def save_dungeons(dungeons):
    """Save dungeon state."""
    data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_dungeons": len(dungeons),
        "total_monsters": sum(d["total_monsters"] for d in dungeons.values()),
        "total_hp": sum(d["total_hp"] for d in dungeons.values()),
        "dungeons": dungeons,
    }
    DUNGEON_DB.write_text(json.dumps(data, indent=2, default=str))
    return data


# === MAIN ===
if __name__ == "__main__":
    print("Scanning kingdom for dungeons...")
    dungeons = scan_kingdom()
    hunters = load_hunters()

    if "--hunt" in sys.argv:
        idx = sys.argv.index("--hunt")
        if idx + 1 < len(sys.argv):
            show_hunt(hunters, dungeons, sys.argv[idx + 1])
    elif "--party" in sys.argv:
        show_party(hunters, dungeons)
    elif "--leaderboard" in sys.argv:
        show_leaderboard(hunters, dungeons)
    elif "--scan" in sys.argv:
        data = save_dungeons(dungeons)
        print(f"=== DUNGEON SCAN COMPLETE {data['timestamp']} ===")
        print(f"Dungeons: {data['total_dungeons']}")
        print(f"Monsters: {data['total_monsters']}")
        print(f"Total HP: {data['total_hp']}")
        for name, dg in dungeons.items():
            print(f"  [{dg['rank']}] {dg['difficulty']:<6} {name}: {dg['total_monsters']} monsters, HP {dg['total_hp']}")
    else:
        show_dungeons(dungeons, hunters)