#!/usr/bin/env python3
"""Tooling (not graded). commit-msg hook: Conventional Commits plus optional checkpoint tag.

Style follows Module 3 ADR 0004.

Example: feat(split): add 70/30 split  [H2, verified [4]]
"""
import re
import sys
from pathlib import Path

PATTERN = re.compile(
    r"^(feat|fix|docs|test|chore|ci|build|refactor|perf|style|data)"
    r"(\([a-z0-9_\-]+\))?!?: .{3,72}(\s+\[H[1-4][^\]]*\](\])?)?$"
)


def main() -> int:
    first = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()[0].strip()
    if first.startswith(("Merge ", "Revert ")) or PATTERN.match(first):
        return 0
    print("FAIL commit message must look like: type(scope): subject  [H#]")
    print("got:", first)
    return 1


if __name__ == "__main__":
    sys.exit(main())
