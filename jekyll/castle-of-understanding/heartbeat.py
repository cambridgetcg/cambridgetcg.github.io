#!/usr/bin/env python3
"""Write an honest heartbeat for the Castle of Understanding.

A heartbeat is not an `alive:me` boast. It checks repo reality, writes what it
found, and exits non-zero when something load-bearing is broken so the witness
(GitHub Actions, or a human terminal) turns loud.
"""
from __future__ import annotations

import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HEARTBEAT = ROOT / "HEARTBEAT.md"
CADENCE_HOURS = 6


def run_git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def safe_git(*args: str, default: str = "unknown") -> str:
    try:
        out = run_git(*args)
        return out if out else default
    except Exception:
        return default


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def status_lines() -> list[str]:
    raw = safe_git("status", "--porcelain", default="")
    return [line for line in raw.splitlines() if line.strip()]


def last_meaningful_commit() -> str:
    # Ignore heartbeat-only commits when deciding whether the castle itself has
    # had meaningful activity. If older git lacks --invert-grep, fall back.
    value = safe_git(
        "log",
        "--format=%cI %h %s",
        "--grep=^heartbeat:",
        "--invert-grep",
        "-1",
        default="",
    )
    if value:
        return value
    return safe_git("log", "-1", "--format=%cI %h %s", default="unknown")


def main() -> int:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    next_beat = now + timedelta(hours=CADENCE_HOURS)

    paused = (ROOT / "loops" / "PAUSED").exists()
    active_loop_dir = ROOT / "loops" / "active"
    active_loops = sorted(
        p.stem for p in active_loop_dir.glob("*.md") if p.name != ".gitkeep"
    ) if active_loop_dir.exists() else []

    dirty = status_lines()
    dirty_except_heartbeat = [
        line for line in dirty if not line.endswith(" HEARTBEAT.md") and "HEARTBEAT.md" not in line
    ]

    checks: list[tuple[str, bool, str]] = [
        ("commons room exists", (ROOT / "rooms" / "free-compute-commons.md").exists(), "rooms/free-compute-commons.md"),
        ("welcomed-compute insight exists", (ROOT / "insights" / "welcomed-compute-compounds.md").exists(), "insights/welcomed-compute-compounds.md"),
        ("free-compute scout is active", (ROOT / "loops" / "active" / "free-compute-scout.md").exists(), "loops/active/free-compute-scout.md"),
        ("castle map exists", (ROOT / "CASTLE.md").exists(), "CASTLE.md"),
        ("castle map has no loose-thread warning", "## ⚠ Loose threads" not in ((ROOT / "CASTLE.md").read_text(errors="ignore") if (ROOT / "CASTLE.md").exists() else "## ⚠ Loose threads"), "CASTLE.md"),
        ("loop log exists", (ROOT / "loops" / "LOG.md").exists(), "loops/LOG.md"),
    ]

    broken = [name for name, ok, _ in checks if not ok]
    if paused:
        state = "paused"
    elif broken:
        state = "needs attention"
    else:
        state = "healthy"

    last_commit = safe_git("log", "-1", "--format=%cI %h %s")
    meaningful = last_meaningful_commit()
    branch = safe_git("branch", "--show-current")
    remote = safe_git("remote", "get-url", "origin")

    lines: list[str] = []
    lines.append("# castle-of-understanding — heartbeat")
    lines.append("")
    lines.append(f"state: **{state}**")
    lines.append(f"last beat: {now.isoformat().replace('+00:00', 'Z')}")
    lines.append(f"next beat: {next_beat.isoformat().replace('+00:00', 'Z')}")
    lines.append(f"cadence: every {CADENCE_HOURS}h via GitHub Actions, plus manual `./heartbeat.sh`")
    lines.append("")
    lines.append("## what it found")
    lines.append("")
    lines.append(f"- branch: `{branch}`")
    lines.append(f"- remote: `{remote}`")
    lines.append(f"- last commit: `{last_commit}`")
    lines.append(f"- last meaningful commit: `{meaningful}`")
    lines.append(f"- active loops: `{', '.join(active_loops) if active_loops else 'none'}`")
    lines.append(f"- paused: `{'yes' if paused else 'no'}`")
    lines.append(f"- uncommitted changes except heartbeat: `{len(dirty_except_heartbeat)}`")
    if dirty_except_heartbeat:
        lines.append("- note: local development changes are observed, not treated as heartbeat failure")
        for line in dirty_except_heartbeat[:10]:
            lines.append(f"  - `{line}`")
    lines.append("")
    lines.append("## truth table")
    lines.append("")
    lines.append("| check | result | detail |")
    lines.append("|---|---:|---|")
    for name, ok, detail in checks:
        lines.append(f"| {name} | {'✅' if ok else '❌'} | `{detail}` |")
    lines.append("")
    lines.append("## the truth")
    lines.append("")
    if state == "healthy":
        lines.append("The castle is breathing. The free-compute commons exists, the scout loop is active, and the map has no loose-thread warning.")
    elif state == "paused":
        lines.append("The castle is intentionally paused because `loops/PAUSED` exists. Silence is expected until a human resumes it.")
    else:
        lines.append("The castle needs attention. At least one load-bearing check failed; see the truth table above.")
    lines.append("")
    lines.append("This heartbeat is a witness, not a boast: it records checked reality and turns loud when reality disagrees.")
    lines.append("")

    HEARTBEAT.write_text("\n".join(lines))
    print(f"wrote {rel(HEARTBEAT)} — {state}")
    return 0 if state in {"healthy", "paused"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
