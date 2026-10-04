#!/usr/bin/env python3
"""Tooling (not graded). List every number written in prose, so each one can be checked.

Scans markdown cells of notebooks/*.ipynb plus README.md, docs/journals/*.md, docs/adr/*.md,
docs/decisions/*.md and docs/*.md. Prints one line per sentence that contains a number:

    file | location | number(s) | sentence

The data-validator subagent uses this list and recomputes every number from the data.
It does not judge anything itself. Usage:  python scripts/list_claims.py [--json]
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NUM = re.compile(r"(?<![\w.])[-+]?\d[\d,]*(?:\.\d+)?%?")
TEMPLATE_MARK = "[fill"
LIST_MARK = re.compile(r"^\s*(?:\d+\.|[-*])\s+")


def scan_text(path, location, text, out):
    in_code = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or TEMPLATE_MARK in line:
            continue
        line = LIST_MARK.sub("", line)
        for s in re.split(r"(?<=[.!?])\s+", line):
            nums = NUM.findall(s)
            if nums:
                out.append({"file": str(path.relative_to(ROOT)), "where": location,
                            "numbers": nums, "text": s.strip()[:300]})


def main():
    out = []
    for nb in sorted((ROOT / "notebooks").glob("*.ipynb")):
        cells = json.loads(nb.read_text(encoding="utf-8"))["cells"]
        for i, c in enumerate(cells, 1):
            if c["cell_type"] == "markdown":
                scan_text(nb, f"cell {i}", "".join(c["source"]), out)
    files = [ROOT / "README.md"] + sorted((ROOT / "docs").glob("*.md"))
    for sub in ["journals", "adr", "decisions"]:
        files += sorted((ROOT / "docs" / sub).glob("*.md"))
    for f in files:
        if f.exists() and f.name not in {"TEMPLATE.md"}:
            scan_text(f, "text", f.read_text(encoding="utf-8"), out)
    if "--json" in sys.argv:
        print(json.dumps(out, indent=1))
    else:
        for c in out:
            print(f"{c['file']} | {c['where']} | {', '.join(c['numbers'])} | {c['text']}")
        print(f"\n{len(out)} sentences with numbers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
