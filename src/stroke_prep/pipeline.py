"""Pipeline SHELLS for the ITAI 1371 Midterm.

Every function below is a TODO. Each docstring is a CONTRACT that holds for any correct choice.
It says what must be true, never which method to pick or what number to expect. The method
choices live in docs/decisions/ (decision cards D1 to D8). You decide; Claude writes the code
at your direction; tests in tests/ check the contracts.

Suggested flow (you may rename or merge functions, keep the contracts):

    load_raw -> split_train_test -> fit_prep (train only) -> transform (train, later test)
             -> balance (train only, y = work_type) -> repair_after_balance -> save_csv
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from stroke_prep import config


def load_raw(path: Path = config.RAW_PATH) -> pd.DataFrame:
    """Read the raw CSV with Python. Never modify the file.

    Contract: returns every row and column of the file; text placeholders for missing values
    are read as missing (check the file to see how missing values are written); the file hash
    is unchanged afterwards.
    """
    # First pass: read as written, to find the text tokens used for missing values.
    first = pd.read_csv(path)
    tokens = missing_tokens(first)
    # Second pass: read again with those tokens treated as missing.
    return pd.read_csv(path, na_values=tokens)


def missing_tokens(df: pd.DataFrame) -> list[str]:
    """Find text tokens that stand for missing values inside number columns.

    A text column whose values are numbers except for a few repeated text tokens is a number
    column with placeholders. Those tokens are returned. Real text columns are left alone.
    """
    tokens: set[str] = set()
    for col in [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]:
        values = df[col].dropna().astype(str)
        as_number = pd.to_numeric(values, errors="coerce")
        if as_number.notna().any():
            tokens.update(values[as_number.isna()].unique())
    return sorted(tokens)


def split_train_test(df: pd.DataFrame, test_size: float = config.TEST_SIZE,
                     seed: int | None = config.SPLIT_SEED, stratify_on=config.STRATIFY_ON):
    """Split ONCE into (train, test) with Python.

    Contract: test holds test_size of the rows (Canvas: 30%); every row lands in exactly one
    part; no id in both parts; same seed gives the same split; returns copies so later steps
    cannot change the original frame. Stratification and seed are decision card D1.
    """
    from sklearn.model_selection import train_test_split

    if seed is None:
        raise ValueError("SPLIT_SEED is blank in config.py: decision card D1")
    # D1: None means a plain random split; a column name or a list of names means stratify.
    if stratify_on is None:
        labels = None
    elif isinstance(stratify_on, str):
        labels = df[stratify_on]
    else:
        labels = df[list(stratify_on)].astype(str).agg("|".join, axis=1)
    train, test = train_test_split(df, test_size=test_size, random_state=seed, stratify=labels)
    return train.copy(), test.copy()


def fit_prep(train: pd.DataFrame) -> dict:
    """Learn everything that is learned from data (fill values, encoders, scalers) from TRAIN.

    Contract: reads only the frame it is given (call it with train only); does not modify its
    input; returns a state object that transform() can reuse on any frame. Which values are
    learned depends on decision cards D2 to D6.
    """
    raise NotImplementedError("TODO H3: see docs/decisions/D2 to D6")


def transform(df: pd.DataFrame, state: dict) -> pd.DataFrame:
    """Apply the learned state to a frame (train first, test at the very end).

    Contract: never fits anything; does not modify its input; keeps the index of the rows it
    keeps; each row's result depends only on that row and the state (a row gives the same
    output alone or inside the whole frame), which is what keeps test information out of train.
    """
    raise NotImplementedError("TODO H3: see docs/decisions/D2 to D6")


def balance(prepared_train: pd.DataFrame, **settings) -> pd.DataFrame:
    """Balance work_type on TRAIN only with SMOTE (Prof Rao's guidance, Oct 1, 2026).

    Contract: never called on test; real rows come back unchanged; if D8 chose a synthetic row
    flag (config.FLAG_SYNTHETIC), every new row is 1 in that column and every real row 0. The
    SMOTE settings (variant, k_neighbors, seed, sampling strategy, dtypes) are decision card D7.
    """
    raise NotImplementedError("TODO H3: see docs/decisions/D7_smote_setup.md")


def repair_after_balance(balanced: pd.DataFrame):
    """Make synthetic rows valid again, and report what changed. Returns (frame, report).

    Contract: after repair every 0/1 column holds only 0 or 1, every one hot group follows its
    rule (exactly one 1 per row, or at most one if you dropped a column per group), and the
    report counts what was changed so you can describe it. The method is decision card D8.
    """
    raise NotImplementedError("TODO H3: see docs/decisions/D8_after_smote.md")


def save_csv(df: pd.DataFrame, path: Path) -> Path:
    """Write df to path with index=False, creating folders.

    Contract: refuses to write anywhere inside data/raw.
    """
    target = Path(path).resolve()
    raw_dir = config.RAW_PATH.parent.resolve()
    if target == raw_dir or raw_dir in target.parents:
        raise PermissionError(f"refusing to write inside data/raw: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(target, index=False)
    return target
