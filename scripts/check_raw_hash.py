#!/usr/bin/env python3
"""Tooling (not graded). Fail if data/raw/healthcare-dataset-stroke-data.csv was changed by hand."""
import hashlib
import sys
from pathlib import Path

RAW = Path("data/raw/healthcare-dataset-stroke-data.csv")
EXPECTED = "144ea5366832bb5432645c0e49fbb951aadf4ee1e75e73d2e15d3dc0841525bd"


def main() -> int:
    if not RAW.exists():
        print(f"FAIL raw file missing: {RAW}")
        return 1
    actual = hashlib.sha256(RAW.read_bytes()).hexdigest()
    if actual != EXPECTED:
        print(f"FAIL raw data changed. expected {EXPECTED} got {actual}")
        return 1
    print("OK raw data hash unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
