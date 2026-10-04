"""Decision slots in config.py: present, blank until signed, sensible once set.

No expected values live here. A blank slot SKIPS with the card that fills it. Once Joseph sets
a value, the test checks only its type and basic rules from the library documentation.
Note: STRATIFY_ON may legitimately stay None; D1 records that choice.
"""
from __future__ import annotations

import pandas as pd
import pytest

from stroke_prep import config

CARD_FILES = {
    "D1": "D1_split.md", "D3": "D3_missing_values.md", "D4": "D4_encoding.md",
    "D5": "D5_scaling.md", "D7": "D7_smote_setup.md", "D8": "D8_after_smote.md",
}


def _value_or_skip(name: str):
    value = getattr(config, name)
    if value is None:
        card = config.DECISION_SLOTS[name]
        pytest.skip(f"{name} is blank: sign docs/decisions/{CARD_FILES[card]} ({card}), "
                    f"then set {name} in src/stroke_prep/config.py")
    return value


def test_every_slot_exists():
    for name, card in config.DECISION_SLOTS.items():
        assert hasattr(config, name), f"config.py is missing slot {name} for {card}"
        assert card in CARD_FILES
        assert (config.ROOT / "docs" / "decisions" / CARD_FILES[card]).exists()


@pytest.mark.parametrize("name", ["IMPUTE_STRATEGY", "SCALER", "SMOTE_VARIANT",
                                  "REPAIR_RULE", "NUMERIC_CHECK"])
def test_text_slots(name):
    value = _value_or_skip(name)
    assert isinstance(value, str) and value.strip(), f"{name} must be non empty text"


@pytest.mark.parametrize("name", ["ADD_MISSING_FLAG", "ONEHOT_DROP_FIRST", "FLAG_SYNTHETIC"])
def test_true_false_slots(name):
    assert isinstance(_value_or_skip(name), bool)


def test_scale_columns():
    cols = _value_or_skip("SCALE_COLUMNS")
    assert isinstance(cols, list) and all(isinstance(c, str) for c in cols)
    raw_cols = pd.read_csv(config.RAW_PATH, nrows=1).columns
    missing = [c for c in cols if c not in raw_cols]
    assert not missing, f"SCALE_COLUMNS names columns not in the raw file: {missing}"


def test_final_numeric_units():
    assert _value_or_skip("FINAL_NUMERIC_UNITS") in {"scaled", "real"}


@pytest.mark.parametrize("name", ["SPLIT_SEED", "SMOTE_RANDOM_STATE"])
def test_integer_seeds(name):
    value = _value_or_skip(name)
    assert isinstance(value, int) and not isinstance(value, bool) and value >= 0


def test_smote_k_neighbors():
    k = _value_or_skip("SMOTE_K_NEIGHBORS")
    assert isinstance(k, int) and not isinstance(k, bool) and k >= 1
    if not config.TRAIN_RAW.exists():
        pytest.skip("train file not made yet (H2); the group size check runs after the split")
    smallest = pd.read_csv(config.TRAIN_RAW)[config.BALANCE_COL].value_counts().min()
    assert k < smallest, "SMOTE needs k_neighbors below the smallest work_type group in train"


def test_smote_sampling_strategy():
    s = _value_or_skip("SMOTE_SAMPLING_STRATEGY")
    if isinstance(s, str):
        assert s in {"auto", "not majority", "not minority", "all", "minority"}
    else:
        assert isinstance(s, dict) and s
        assert all(isinstance(k, str) and isinstance(v, int) and v > 0 for k, v in s.items())
