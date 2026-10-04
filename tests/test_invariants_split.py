"""Split invariants (checkpoint H2). Checked on the files notebook 01 saves. No expected numbers:
every comparison is between the raw file and your own split files."""
import pandas as pd
from conftest import need_file

from stroke_prep import config


def _load():
    train = pd.read_csv(need_file(config.TRAIN_RAW, "H2"), na_values=["N/A"])
    test = pd.read_csv(need_file(config.TEST_RAW, "H2"), na_values=["N/A"])
    return train, test


def test_rows_reconcile_with_raw(raw_df):
    train, test = _load()
    assert len(train) + len(test) == len(raw_df)


def test_no_id_in_both_parts():
    train, test = _load()
    assert set(train["id"]).isdisjoint(set(test["id"]))


def test_every_raw_row_lands_somewhere(raw_df):
    train, test = _load()
    assert set(train["id"]) | set(test["id"]) == set(raw_df["id"])


def test_split_ratio_matches_canvas(raw_df):
    # Canvas S3: training 70%, testing 30%. Allow one row of rounding.
    _, test = _load()
    assert abs(len(test) - config.TEST_SIZE * len(raw_df)) <= 1


def test_split_files_have_raw_columns(raw_df):
    train, test = _load()
    assert list(train.columns) == list(raw_df.columns) == list(test.columns)


def test_split_rows_are_unedited_copies_of_raw(raw_df):
    # The split files must hold the raw rows exactly as they are (no cleaning yet).
    train, test = _load()
    raw = raw_df.set_index("id").sort_index()
    both = pd.concat([train, test]).set_index("id").sort_index()
    pd.testing.assert_frame_equal(both, raw, check_dtype=False)
