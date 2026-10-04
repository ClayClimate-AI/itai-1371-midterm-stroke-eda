"""Infrastructure tests (working from the start): the raw CSV is present and untouched."""
import hashlib

import pandas as pd

from stroke_prep import config

COLUMNS = [
    "id", "gender", "age", "hypertension", "heart_disease", "ever_married", "work_type",
    "Residence_type", "avg_glucose_level", "bmi", "smoking_status", "stroke",
]


def test_raw_file_hash_unchanged(raw_path):
    assert hashlib.sha256(raw_path.read_bytes()).hexdigest() == config.RAW_SHA256


def test_sha256sums_file_matches_config(raw_path):
    line = (raw_path.parent / "SHA256SUMS").read_text().split()
    assert line[0] == config.RAW_SHA256 and line[1] == raw_path.name


def test_raw_columns(raw_path):
    assert list(pd.read_csv(raw_path, nrows=5).columns) == COLUMNS


def test_raw_meets_canvas_row_minimum(raw_path):
    # Canvas GL1: "choose Kaggle dataset >=2000 rows"
    assert len(pd.read_csv(raw_path)) >= 2000


def test_ids_are_unique(raw_path):
    ids = pd.read_csv(raw_path)["id"]
    assert ids.is_unique, "the split checks below rely on id being a unique row key"
