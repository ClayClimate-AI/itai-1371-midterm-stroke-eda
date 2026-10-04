#!/usr/bin/env python3
"""Tooling (not graded). Compare a committed notebook with a freshly executed copy.

Usage:  python scripts/compare_outputs.py committed.ipynb rerun.ipynb

Compares the text output of every code cell (printed text, tables, error text). Images are
compared by presence only, because pixels can differ between machines. Prints each cell whose
text output differs and exits 1 if any differ. The repo-auditor subagent uses this.
"""
import json
import re
import sys
from pathlib import Path

ADDR = re.compile(r"0x[0-9a-f]+")


def texts(path):
    cells = json.loads(Path(path).read_text(encoding="utf-8"))["cells"]
    out = []
    for c in cells:
        if c["cell_type"] != "code":
            continue
        parts, images = [], 0
        for o in c.get("outputs", []):
            if o.get("output_type") == "stream":
                parts.append("".join(o.get("text", "")))
            elif o.get("output_type") in ("execute_result", "display_data"):
                data = o.get("data", {})
                if "text/plain" in data:
                    parts.append("".join(data["text/plain"]))
                images += sum(1 for k in data if k.startswith("image/"))
            elif o.get("output_type") == "error":
                parts.append(o.get("ename", "") + ": " + o.get("evalue", ""))
        out.append((ADDR.sub("0x..", "\n".join(parts)).strip(), images))
    return out


def main():
    a, b = texts(sys.argv[1]), texts(sys.argv[2])
    if len(a) != len(b):
        print(f"DIFFERENT number of code cells: {len(a)} vs {len(b)}")
        return 1
    diffs = 0
    for i, ((ta, ia), (tb, ib)) in enumerate(zip(a, b, strict=True), 1):
        if ta != tb or ia != ib:
            diffs += 1
            print(f"--- code cell {i} differs (images {ia} vs {ib})")
            print("committed:", ta[:400])
            print("rerun:    ", tb[:400])
    print(f"{diffs} of {len(a)} code cells differ")
    return 1 if diffs else 0


if __name__ == "__main__":
    sys.exit(main())
