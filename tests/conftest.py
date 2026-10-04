"""Shared test setup.

The tests in this repo check PROPERTIES that hold for any correct set of decisions (no leakage,
rows reconcile, 0/1 columns stay 0/1, and so on). None of them contains an expected result.
Tests that need a file or a function that does not exist yet SKIP with a message saying which
checkpoint creates it.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from stroke_prep import config

ROOT = config.ROOT
RAW = config.RAW_PATH


@pytest.fixture(scope="session")
def raw_path() -> Path:
    return RAW


@pytest.fixture(scope="session")
def raw_df() -> pd.DataFrame:
    # Read the raw file the plain way, independent of Joseph's load_raw().
    return pd.read_csv(RAW, na_values=["N/A"])


def need_file(path: Path, checkpoint: str) -> Path:
    """Skip the calling test until the artifact exists."""
    if not path.exists():
        pytest.skip(f"{path.relative_to(ROOT)} does not exist yet (created at {checkpoint})")
    return path


def call_or_skip(fn, *args, **kwargs):
    """Call a pipeline function; skip while it is still a TODO shell."""
    try:
        return fn(*args, **kwargs)
    except NotImplementedError as exc:
        pytest.skip(f"{fn.__name__} not implemented yet: {exc}")


def onehot_groups(columns) -> dict[str, list[str]]:
    """Group one hot columns by the raw categorical column they came from (name prefix)."""
    groups = {}
    for cat in config.RAW_CATEGORICAL:
        members = [c for c in columns if str(c).startswith(cat + "_")]
        if members:
            groups[cat] = members
    return groups


def need_synthetic_flag() -> str:
    """Skip unless decision D8 chose a 0/1 column that marks SMOTE rows (FLAG_SYNTHETIC)."""
    if config.FLAG_SYNTHETIC is not True:
        state = "blank" if config.FLAG_SYNTHETIC is None else "False"
        pytest.skip(f"FLAG_SYNTHETIC is {state} in src/stroke_prep/config.py (card D8, set at "
                    "H1); checks that rely on a synthetic row flag skip")
    return config.SYNTHETIC_FLAG


def binary_columns(columns) -> list[str]:
    """Columns that must hold only 0 or 1: raw 0/1 columns, flags, one hot columns."""
    cols = [c for c in config.RAW_BINARY if c in columns]
    cols += [c for c in columns if str(c).endswith(("_missing", "_flag"))]
    if config.FLAG_SYNTHETIC is True and config.SYNTHETIC_FLAG in columns:
        cols.append(config.SYNTHETIC_FLAG)
    for members in onehot_groups(columns).values():
        cols += members
    return sorted(set(cols))
