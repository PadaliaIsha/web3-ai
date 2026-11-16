#!/usr/bin/env python3
"""Print tools listed in the Awesome Web3 AI README.

Usage:
    python examples/list_tools.py
    python examples/list_tools.py --section "DeFi AI Tools"
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

HEADING = re.compile(r"^##\s+(.+)$")
ROW = re.compile(r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|")


def parse_catalog(text: str) -> dict[str, list[tuple[str, str]]]:
    """Return section title -> list of (name, url) from markdown tables."""
    catalog: dict[str, list[tuple[str, str]]] = {}
    section: str | None = None

    for line in text.splitlines():
        heading = HEADING.match(line)
        if heading:
            title = heading.group(1).strip()
            if title.lower().startswith("how to choose"):
                section = None
                continue
            section = title
            catalog.setdefault(section, [])
            continue

        if section is None:
            continue

        row = ROW.match(line)
        if row:
            catalog[section].append((row.group(1).strip(), row.group(2).strip()))

    return {title: tools for title, tools in catalog.items() if tools}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--section",
        help="Only print tools whose section title contains this text (case-insensitive).",
    )
    args = parser.parse_args()

    catalog = parse_catalog(README.read_text(encoding="utf-8"))
    needle = (args.section or "").casefold()

    shown = 0
    for title, tools in catalog.items():
        if needle and needle not in title.casefold():
            continue
        print(title)
        for name, url in tools:
            print(f"  - {name}: {url}")
        print()
        shown += len(tools)

    if shown == 0:
        raise SystemExit("No matching tools found.")


if __name__ == "__main__":
    main()
