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

# D2 (signed card): id is a row label, dropped before any modeling step.
DROP_COLUMNS = ["id"]

# Fitted objects from notebook 03, loaded by notebook 04 (a file name, not a result).
STATE_PATH = config.ROOT / "data" / "interim" / "prep_state.joblib"


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
    from sklearn import preprocessing
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder

    df = train.drop(columns=[c for c in DROP_COLUMNS if c in train.columns])
    # D3: columns with blanks in train get a 0/1 flag (if chosen) and a fill value learned here.
    fill_cols = [c for c in df.columns if df[c].isna().any()]
    imputer = None
    if fill_cols:
        imputer = SimpleImputer(strategy=config.IMPUTE_STRATEGY).fit(df[fill_cols])
    # D4: one hot for every text column except work_type, which stays the SMOTE label (y).
    drop = "first" if config.ONEHOT_DROP_FIRST else None
    text_cols = [c for c in config.RAW_CATEGORICAL if c != config.BALANCE_COL]
    encoder = OneHotEncoder(handle_unknown="ignore", drop=drop, sparse_output=False)
    encoder.fit(df[text_cols])
    # D4: work_type is one hot encoded after SMOTE, with an encoder learned from real train rows.
    balance_encoder = OneHotEncoder(handle_unknown="ignore", drop=drop, sparse_output=False)
    balance_encoder.fit(df[[config.BALANCE_COL]])
    # D5: scaler learned on the filled train values of the chosen columns.
    filled = df[config.SCALE_COLUMNS].copy()
    if imputer is not None:
        filled[fill_cols] = imputer.transform(df[fill_cols])
    scaler = getattr(preprocessing, config.SCALER)().fit(filled[config.SCALE_COLUMNS])
    return {"fill_cols": fill_cols, "imputer": imputer, "text_cols": text_cols,
            "encoder": encoder, "balance_encoder": balance_encoder, "scaler": scaler}


def transform(df: pd.DataFrame, state: dict) -> pd.DataFrame:
    """Apply the learned state to a frame (train first, test at the very end).

    Contract: never fits anything; does not modify its input; keeps the index of the rows it
    keeps; each row's result depends only on that row and the state (a row gives the same
    output alone or inside the whole frame), which is what keeps test information out of train.

    Order (card D6, option A): drop columns (D2), flag and fill (D3), encode (D4), scale (D5).
    work_type stays a text label here; encode_balance_col() encodes it after SMOTE (D4).
    """
    out = df.drop(columns=[c for c in DROP_COLUMNS if c in df.columns]).copy()
    # D3: add the 0/1 missing flags before filling, then fill with the train learned values.
    if state["fill_cols"]:
        if config.ADD_MISSING_FLAG:
            for c in state["fill_cols"]:
                out[c + "_missing"] = out[c].isna().astype(int)
        out[state["fill_cols"]] = state["imputer"].transform(out[state["fill_cols"]])
    # D4: replace each text column with its one hot columns.
    onehot = pd.DataFrame(state["encoder"].transform(out[state["text_cols"]]).astype(int),
                          columns=state["encoder"].get_feature_names_out(), index=out.index)
    label = out[config.BALANCE_COL]
    out = out.drop(columns=state["text_cols"] + [config.BALANCE_COL])
    # D5: scale the chosen number columns with the train fitted scaler.
    out[config.SCALE_COLUMNS] = state["scaler"].transform(out[config.SCALE_COLUMNS])
    return pd.concat([out, onehot, label], axis=1)


def drop_rare_rows(train: pd.DataFrame, rare: dict[str, list]) -> pd.DataFrame:
    """D2: remove train rows whose value is listed as rare on the signed card. Train only."""
    keep = pd.Series(True, index=train.index)
    for col, values in rare.items():
        keep &= ~train[col].isin(values)
    return train[keep].copy()


def encode_balance_col(df: pd.DataFrame, state: dict) -> pd.DataFrame:
    """D4: replace the work_type label with its one hot columns (after SMOTE). Never fits."""
    enc = state["balance_encoder"]
    onehot = pd.DataFrame(enc.transform(df[[config.BALANCE_COL]]).astype(int),
                          columns=enc.get_feature_names_out(), index=df.index)
    out = df.drop(columns=[config.BALANCE_COL])
    flag = [config.SYNTHETIC_FLAG] if config.SYNTHETIC_FLAG in out.columns else []
    rest = [c for c in out.columns if c not in flag]
    return pd.concat([out[rest], onehot, out[flag]], axis=1)


def to_real_units(df: pd.DataFrame, state: dict) -> pd.DataFrame:
    """D5 and D8: convert the scaled columns back to real units with the train fitted scaler."""
    out = df.copy()
    out[config.SCALE_COLUMNS] = state["scaler"].inverse_transform(out[config.SCALE_COLUMNS])
    return out


def binary_cols(columns) -> list[str]:
    """0/1 columns: raw 0/1 columns and the D3 missing flags (SMOTE blends both)."""
    return [c for c in columns if c in config.RAW_BINARY or str(c).endswith("_missing")]


def onehot_cols(columns) -> dict[str, list[str]]:
    """One hot columns grouped by the text column they came from (name prefix)."""
    groups = {}
    for cat in config.RAW_CATEGORICAL:
        members = [c for c in columns if str(c).startswith(cat + "_")]
        if members:
            groups[cat] = members
    return groups


def validity_counts(df: pd.DataFrame) -> dict:
    """D8 steps 1 and 2: non 0/1 values per 0/1 column, rows breaking each one hot rule."""
    binary = {c: int((~df[c].isin([0, 1])).sum()) for c in binary_cols(df.columns)}
    groups = {}
    for name, cols in onehot_cols(df.columns).items():
        sums = df[cols].sum(axis=1)
        ok = sums.isin([0, 1]) if config.ONEHOT_DROP_FIRST else sums.eq(1)
        groups[name] = int((~ok | ~df[cols].isin([0, 1]).all(axis=1)).sum())
    return {"binary": binary, "onehot": groups}


def balance(prepared_train: pd.DataFrame, **settings) -> pd.DataFrame:
    """Balance work_type on TRAIN only with SMOTE (Prof Rao's guidance, Oct 1, 2026).

    Contract: never called on test; real rows come back unchanged; if D8 chose a synthetic row
    flag (config.FLAG_SYNTHETIC), every new row is 1 in that column and every real row 0. The
    SMOTE settings (variant, k_neighbors, seed, sampling strategy, dtypes) are decision card D7.
    """
    import imblearn.over_sampling as over

    params = {"k_neighbors": config.SMOTE_K_NEIGHBORS,
              "sampling_strategy": config.SMOTE_SAMPLING_STRATEGY,
              "random_state": config.SMOTE_RANDOM_STATE}
    params.update(settings)
    X = prepared_train.drop(columns=[config.BALANCE_COL])
    y = prepared_train[config.BALANCE_COL]
    # Work in float so SMOTE's blended values reach the D8 repair as they are; the library
    # would otherwise cast them back to the integer type of the 0/1 and one hot columns.
    X_res, y_res = getattr(over, config.SMOTE_VARIANT)(**params).fit_resample(X.astype(float), y)
    out = pd.DataFrame(X_res, columns=X.columns).reset_index(drop=True)
    out[config.BALANCE_COL] = pd.Series(y_res).reset_index(drop=True)
    out = out[list(prepared_train.columns)]
    if config.FLAG_SYNTHETIC:
        # imbalanced-learn returns the real rows first, in order, then the new rows.
        out[config.SYNTHETIC_FLAG] = (out.index >= len(prepared_train)).astype(int)
    return out


def repair_after_balance(balanced: pd.DataFrame):
    """Make synthetic rows valid again, and report what changed. Returns (frame, report).

    Contract: after repair every 0/1 column holds only 0 or 1, every one hot group follows its
    rule (exactly one 1 per row, or at most one if you dropped a column per group), and the
    report counts what was changed so you can describe it. The method is decision card D8.

    REPAIR_RULE "A" (signed card): round each 0/1 column at 0.5 (0.5 and above becomes 1) and
    set the largest column of each one hot group to 1 and the rest to 0 (argmax).
    """
    import numpy as np

    if config.REPAIR_RULE != "A":
        raise ValueError(f"REPAIR_RULE {config.REPAIR_RULE!r} has no code yet: card D8")
    out = balanced.copy()
    report = {"binary_values_changed": {}, "onehot_rows_changed": {}}
    for c in binary_cols(out.columns):
        fixed = (out[c] >= 0.5).astype(int)
        report["binary_values_changed"][c] = int((fixed != out[c]).sum())
        out[c] = fixed
    for name, cols in onehot_cols(out.columns).items():
        values = out[cols].to_numpy()
        fixed = np.zeros_like(values, dtype=int)
        fixed[np.arange(len(values)), values.argmax(axis=1)] = 1
        report["onehot_rows_changed"][name] = int((fixed != values).any(axis=1).sum())
        out[cols] = fixed
    return out, report


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
