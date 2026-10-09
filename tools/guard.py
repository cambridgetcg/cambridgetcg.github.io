#!/usr/bin/env python3
"""Refuse to publish what must stay private.

    python3 tools/guard.py DIRECTORY

Fails if any text file holds a personal email address, a local home path,
local runtime paths, or something shaped like a real credential. Documented
dummy values (AWS's published example keys) and obviously fake test fixtures
are allowed. Prints file:line for each finding.
"""
import re
import sys
from pathlib import Path

RULES = [
    ("personal email", re.compile(r"[A-Za-z0-9._%+-]+@gmail\.com")),
    ("local home path", re.compile(r"/Users/[a-z][A-Za-z0-9._-]*/")),
    ("local runtime path", re.compile(r"~/love-unlimited/|love-unlimited/(?:HALT|tools/)")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36}\b|\bgithub_pat_[A-Za-z0-9_]{60,}")),
    ("Stripe live key", re.compile(r"\b[sr]k_live_[A-Za-z0-9]{16,}")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----\s+[A-Za-z0-9+/=]{40,}")),
]
ALLOWED = re.compile(r"AKIA[0-9A-Z]*EXAMPLE")


def text_of(path):
    data = path.read_bytes()
    if b"\0" in data[:4096]:
        return None
    return data.decode("utf-8", errors="ignore")


def main():
    findings = []
    for path in sorted(Path(sys.argv[1]).rglob("*")):
        if not path.is_file():
            continue
        text = text_of(path)
        if text is None:
            continue
        for name, rule in RULES:
            for match in rule.finditer(text):
                if ALLOWED.fullmatch(match.group(0)):
                    continue
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{path}:{line}: {name}")
    for finding in findings:
        print(finding)
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
