#!/usr/bin/env python3
"""Tooling (not graded). environment check (adapted from Lab 04/05 setup_gate.py)."""
import importlib
import sys

REQUIRED = [
    "pandas", "numpy", "sklearn", "imblearn",
    "matplotlib", "jupyterlab", "nbconvert", "pytest",
]


def main() -> int:
    missing = []
    for name in REQUIRED:
        try:
            importlib.import_module(name)
        except ImportError:
            missing.append(name)
    if missing:
        print("FAIL missing:", ", ".join(missing))
        print("Run: pip install -r requirements.txt")
        return 1
    print("OK environment check passed")
    print("Python", sys.version.split()[0])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
