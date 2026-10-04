"""Contract tests for src/stroke_prep/pipeline.py.

Each test calls one of your functions and checks a property that must hold whatever you decided.
While a function is still a TODO shell (raises NotImplementedError) its tests SKIP.
"""
import numpy as np
import pandas as pd
import pytest
from conftest import binary_columns, call_or_skip, need_synthetic_flag, onehot_groups

from stroke_prep import config, pipeline

FLAG = config.SYNTHETIC_FLAG


@pytest.fixture(scope="module")
def raw():
    return call_or_skip(pipeline.load_raw)


@pytest.fixture(scope="module")
def parts(raw):
    if config.SPLIT_SEED is None:
        pytest.skip("set SPLIT_SEED in src/stroke_prep/config.py after decision D1")
    return call_or_skip(pipeline.split_train_test, raw)


# ---- load and split ----------------------------------------------------------------------

def test_load_raw_reads_every_row_and_missing_values(raw, raw_df):
    assert raw.shape == raw_df.shape
    for col in ["age", "avg_glucose_level", "bmi"]:
        assert pd.api.types.is_numeric_dtype(raw[col]), f"{col} was read as text"


def test_split_is_disjoint_and_complete(raw, parts):
    train, test = parts
    assert len(train) + len(test) == len(raw)
    assert set(train["id"]).isdisjoint(set(test["id"]))


def test_split_ratio_matches_canvas(raw, parts):
    _, test = parts
    assert abs(len(test) - config.TEST_SIZE * len(raw)) <= 1


def test_split_is_repeatable(raw, parts):
    again = pipeline.split_train_test(raw)
    assert list(again[0]["id"]) == list(parts[0]["id"])


def test_split_returns_copies(raw, parts):
    before = raw.copy()
    fresh_train, _ = pipeline.split_train_test(raw)
    fresh_train.iloc[0, 1] = None  # changing the result must not change the raw frame
    pd.testing.assert_frame_equal(raw, before)


# ---- fit on train only, transform without fitting ---------------------------------------------

@pytest.fixture(scope="module")
def state(parts):
    train, _ = parts
    snapshot = train.copy()
    st = call_or_skip(pipeline.fit_prep, train)
    pd.testing.assert_frame_equal(train, snapshot)  # fit_prep must not change its input
    return st


def test_transform_does_not_change_input(parts, state):
    _, test = parts
    snapshot = test.copy()
    call_or_skip(pipeline.transform, test, state)
    pd.testing.assert_frame_equal(test, snapshot)


def test_transform_is_row_by_row(parts, state):
    # If a row gives the same output alone as inside the full frame, transform() is not
    # learning anything from the frame it is given. That is the leakage guard for the test set.
    _, test = parts
    full = call_or_skip(pipeline.transform, test, state)
    rng = np.random.default_rng(0)
    for i in rng.choice(len(test), size=min(10, len(test)), replace=False):
        one = pipeline.transform(test.iloc[[i]], state)
        if len(one) == 0:
            assert test.index[i] not in full.index
            continue
        idx = one.index[0]
        pd.testing.assert_series_equal(one.loc[idx], full.loc[idx], check_names=False,
                                       check_dtype=False)


def test_transformed_train_has_no_missing_values(parts, state):
    train, _ = parts
    out = call_or_skip(pipeline.transform, train, state)
    assert int(out.isna().sum().sum()) == 0


# ---- balance and repair ------------------------------------------------------------------

@pytest.fixture(scope="module")
def prepared(parts, state):
    train, _ = parts
    return call_or_skip(pipeline.transform, train, state)


@pytest.fixture(scope="module")
def balanced(prepared):
    snapshot = prepared.copy()
    out = call_or_skip(pipeline.balance, prepared)
    pd.testing.assert_frame_equal(prepared, snapshot)  # balance must not change its input
    return out


def test_balance_flags_every_row(prepared, balanced):
    need_synthetic_flag()
    assert FLAG in balanced.columns
    assert set(balanced[FLAG].unique()) <= {0, 1}
    assert int((balanced[FLAG] == 0).sum()) == len(prepared)


def test_balance_keeps_real_rows_unchanged(prepared, balanced):
    need_synthetic_flag()
    real = balanced[balanced[FLAG] == 0].drop(columns=[FLAG])
    cols = [c for c in prepared.columns if c in real.columns]
    pd.testing.assert_frame_equal(real[cols].reset_index(drop=True),
                                  prepared[cols].reset_index(drop=True), check_dtype=False)


def test_balance_only_adds_rows(prepared, balanced):
    assert len(balanced) >= len(prepared)


def test_repair_makes_binary_and_onehot_valid(balanced):
    fixed, report = call_or_skip(pipeline.repair_after_balance, balanced)
    assert report is not None, "return a report of what was changed"
    for c in binary_columns(fixed.columns):
        assert set(fixed[c].unique()) <= {0, 1}, c
    if config.ONEHOT_DROP_FIRST is not None:
        for name, cols in onehot_groups(fixed.columns).items():
            sums = fixed[cols].sum(axis=1)
            ok = sums.isin([0, 1]) if config.ONEHOT_DROP_FIRST else (sums == 1)
            assert ok.all(), name


def test_save_csv_refuses_data_raw(tmp_path):
    df = pd.DataFrame({"a": [1]})
    try:
        pipeline.save_csv(df, config.RAW_PATH.parent / "should_not_exist.csv")
    except NotImplementedError:
        pytest.skip("save_csv not implemented yet")
    except Exception:
        return  # refused, as required
    (config.RAW_PATH.parent / "should_not_exist.csv").unlink(missing_ok=True)
    pytest.fail("save_csv wrote into data/raw")
