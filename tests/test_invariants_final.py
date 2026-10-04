"""Final dataset invariants (checkpoint H3). They hold for ANY defensible set of decisions.

Nothing here knows the "right" numbers. Each test compares your files with each other, with
the raw file, or with a rule (0/1 stays 0/1, one hot groups stay valid, test never balanced).
"""
import pandas as pd
import pytest
from conftest import binary_columns, need_file, need_synthetic_flag, onehot_groups

from stroke_prep import config

FLAG = config.SYNTHETIC_FLAG


def _final():
    return pd.read_csv(need_file(config.FINAL, "H3"))


def _test_out():
    return pd.read_csv(need_file(config.TEST_TRANSFORMED, "H3"))


def _real(df):
    # Telling real rows from SMOTE rows needs the flag column, which is a D8 choice.
    need_synthetic_flag()
    return df[df[FLAG] == 0]


# ---- final clean dataset ---------------------------------------------------------------

def test_final_has_no_missing_values():
    df = _final()
    assert int(df.isna().sum().sum()) == 0


def test_final_is_all_numeric():
    df = _final()
    text = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])
            and not pd.api.types.is_bool_dtype(df[c])]
    assert text == [], f"text columns left: {text}"


def test_final_keeps_target():
    df = _final()
    assert config.TARGET in df.columns


def test_final_has_synthetic_flag_when_chosen():
    flag = need_synthetic_flag()
    assert flag in _final().columns, "D8 chose a synthetic row flag, but the column is missing"


def test_ids_in_final_trace_back_to_train_only():
    # Keeping or dropping id is decision D2. If you keep it, real rows must carry train ids
    # only (no test id leaked into the final file).
    df = _final()
    if "id" not in df.columns:
        pytest.skip("id not kept in the final file (decision D2)")
    train = pd.read_csv(need_file(config.TRAIN_RAW, "H2"))
    test = pd.read_csv(need_file(config.TEST_RAW, "H2"))
    real_ids = set(_real(df)["id"])
    assert real_ids <= set(train["id"])
    assert real_ids.isdisjoint(set(test["id"]))


def test_binary_columns_hold_only_0_and_1():
    df = _final()
    bad = {c: sorted(set(df[c].unique()) - {0, 1}) for c in binary_columns(df.columns)}
    bad = {c: v[:5] for c, v in bad.items() if v}
    assert bad == {}, f"values other than 0/1: {bad}"


def test_each_onehot_group_is_valid():
    df = _final()
    groups = onehot_groups(df.columns)
    if not groups:
        pytest.skip("no one hot columns found (named <column>_<category>)")
    if config.ONEHOT_DROP_FIRST is None:
        pytest.skip("set ONEHOT_DROP_FIRST in src/stroke_prep/config.py after decision D4")
    for name, cols in groups.items():
        sums = df[cols].sum(axis=1)
        if config.ONEHOT_DROP_FIRST:
            assert sums.isin([0, 1]).all(), f"{name}: a row has more than one 1"
        else:
            assert (sums == 1).all(), f"{name}: a row does not have exactly one 1"


def test_synthetic_flag_reconciles():
    need_synthetic_flag()
    df = _final()
    assert set(df[FLAG].unique()) <= {0, 1}
    assert int(df[FLAG].sum()) == len(df) - len(_real(df))


def test_real_rows_reconcile_with_train():
    # Real rows can only come from train: never more than train, and equal to the prepared
    # train file when you saved one (rows you removed on purpose are explained in D2).
    df = _final()
    train = pd.read_csv(need_file(config.TRAIN_RAW, "H2"))
    assert len(_real(df)) <= len(train)
    if config.TRAIN_PREPARED.exists():
        assert len(_real(df)) == len(pd.read_csv(config.TRAIN_PREPARED))


def test_balancing_only_adds_rows():
    df = _final()
    wt = onehot_groups(df.columns).get(config.BALANCE_COL)
    if not wt:
        pytest.skip("work_type one hot columns not found in the final file")
    real_counts = _real(df)[wt].sum()
    all_counts = df[wt].sum()
    assert (all_counts >= real_counts).all()


# ---- test set: transformed only, never balanced -------------------------------------------

def test_test_set_has_same_columns_as_final():
    final, test = _final(), _test_out()
    assert [c for c in final.columns if c != FLAG] == [c for c in test.columns if c != FLAG]


def test_test_set_has_no_missing_values():
    assert int(_test_out().isna().sum().sum()) == 0


def test_test_set_was_never_balanced():
    test = _test_out()
    raw_test = pd.read_csv(need_file(config.TEST_RAW, "H2"))
    if config.FLAG_SYNTHETIC is True and FLAG in test.columns:
        assert int(test[FLAG].sum()) == 0, "the test set must contain no synthetic rows"
    assert len(test) <= len(raw_test), "the test set gained rows, so something was added"
    wt = onehot_groups(test.columns).get(config.BALANCE_COL)
    if wt and len(test) == len(raw_test):
        after = {c.split(config.BALANCE_COL + "_", 1)[1]: int(test[c].sum()) for c in wt}
        before = raw_test[config.BALANCE_COL].value_counts().to_dict()
        assert {k: before.get(k, 0) for k in after} == after


def test_test_set_binary_columns_hold_only_0_and_1():
    df = _test_out()
    bad = [c for c in binary_columns(df.columns) if not set(df[c].unique()) <= {0, 1}]
    assert bad == []
