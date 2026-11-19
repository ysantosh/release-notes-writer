#!/usr/bin/env python3
"""Extract and group git commits between two refs for release notes drafting.

Usage:
    python3 scripts/extract_commits.py v2.3.0 v2.4.0
"""

import re
import subprocess
import sys
from collections import defaultdict

CATEGORY_MAP = {
    "breaking": "Breaking Changes",
    "feat": "New Features",
    "perf": "Improvements",
    "fix": "Bug Fixes",
    "security": "Security & Deprecations",
}

NOISE_PREFIXES = ("chore", "ci", "style", "test", "build")


def get_commits(from_ref: str, to_ref: str) -> list[str]:
    cmd = ["git", "log", f"{from_ref}..{to_ref}", "--pretty=format:%h %s", "--no-merges"]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return [line for line in result.stdout.splitlines() if line.strip()]


def categorize(commits: list[str]) -> dict[str, list[str]]:
    grouped: dict[str, list[str]] = defaultdict(list)
    pattern = re.compile(r"^([a-f0-9]+)\s+([a-z]+)(\([^)]+\))?(!)?:\s*(.+)$")

    for line in commits:
        match = pattern.match(line)
        if not match:
            grouped["Uncategorized"].append(line)
            continue

        _, prefix, _, bang, _ = match.groups()
        if bang:
            grouped[CATEGORY_MAP["breaking"]].append(line)
        elif prefix in NOISE_PREFIXES:
            continue
        elif prefix in CATEGORY_MAP:
            grouped[CATEGORY_MAP[prefix]].append(line)
        else:
            grouped["Uncategorized"].append(line)

    return grouped


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python3 scripts/extract_commits.py <from_tag> <to_tag>", file=sys.stderr)
        sys.exit(1)

    commits = get_commits(sys.argv[1], sys.argv[2])
    grouped = categorize(commits)

    for section, items in grouped.items():
        print(f"## {section}")
        for item in items:
            print(f"- {item}")
        print()


if __name__ == "__main__":
    main()
