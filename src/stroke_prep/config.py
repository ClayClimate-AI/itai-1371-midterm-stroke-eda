"""Project settings in one place.

Two kinds of values live here:

* FACTS that are not choices: file paths, the raw file fingerprint, the target column, the
  Canvas split ratio, and Prof Rao's balancing guidance.
* DECISIONS that start as None. Fill a decision value ONLY after you have signed the matching
  decision card in docs/decisions/ and written its ADR. Tests that need a decision value skip
  until it is set.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ---- Facts -----------------------------------------------------------------------------
RAW_PATH = ROOT / "data" / "raw" / "healthcare-dataset-stroke-data.csv"
RAW_SHA256 = "144ea5366832bb5432645c0e49fbb951aadf4ee1e75e73d2e15d3dc0841525bd"  # SHA256SUMS
TARGET = "stroke"            # the column the Final will predict (dataset fact)
BALANCE_COL = "work_type"    # Prof Rao's guidance: balance work_type with SMOTE (Oct 1, 2026)
TEST_SIZE = 0.30             # Canvas S3: "training 70%, testing 30%"
RAW_CATEGORICAL = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]
RAW_BINARY = ["hypertension", "heart_disease", "stroke"]   # stored as 0/1 in the raw file

# File names used by the notebooks, tests and checks (a naming convention, not a result)
TRAIN_RAW = ROOT / "data" / "interim" / "train_raw.csv"
TEST_RAW = ROOT / "data" / "interim" / "test_raw.csv"
TRAIN_PREPARED = ROOT / "data" / "interim" / "train_prepared.csv"   # optional, see nb03 spec
FINAL = ROOT / "data" / "processed" / "stroke_clean_final.csv"       # Canvas item 8
TEST_TRANSFORMED = ROOT / "data" / "processed" / "stroke_test_transformed.csv"
SYNTHETIC_FLAG = "is_synthetic"   # column name, used only if D8 sets FLAG_SYNTHETIC = True

# ---- Decisions (fill after you sign the card) ------------------------------------------
# Every slot below is BLANK (None) on purpose. The kit chooses nothing. Copy each value from the
# signed card named in the comment. tests/test_decision_slots.py skips a slot while it is None
# and tells you which card fills it.

# D1 split: docs/decisions/D1_split.md
SPLIT_SEED: int | None = 33          # D1
STRATIFY_ON: str | list[str] | None = None   # D1 (None is also a valid choice: write it in D1)

# D3 missing values: docs/decisions/D3_missing_values.md
IMPUTE_STRATEGY: str | None = "median"  # D3 fill option, in the card's words
ADD_MISSING_FLAG: bool | None = True   # D3 True if you add a 0/1 missing flag before filling

# D4 encoding: docs/decisions/D4_encoding.md
ONEHOT_DROP_FIRST: bool | None = False  # D4: True if you drop one column per one hot group

# D5 scaling: docs/decisions/D5_scaling.md
SCALER: str | None = "StandardScaler"              # D5 method name as written on the card
SCALE_COLUMNS: list[str] | None = ["age", "avg_glucose_level", "bmi"]  # D5 columns to scale

# D7 SMOTE setup: docs/decisions/D7_smote_setup.md (Prof Rao fixed SMOTE on work_type)
SMOTE_VARIANT: str | None = "SMOTE"       # D7 "SMOTE" or the variant named on the card
SMOTE_K_NEIGHBORS: int | None = 5   # D7 k_neighbors; must be below the smallest work_type
                                       #    group in train (the test checks this once set)
SMOTE_SAMPLING_STRATEGY: str | dict[str, int] | None = "auto"  # D7 "auto" or a dict of counts
SMOTE_RANDOM_STATE: int | None = 33  # D7 random_state; never change it after seeing results

# D8 after SMOTE: docs/decisions/D8_after_smote.md
REPAIR_RULE: str | None = "A"         # D8 repair option for 0/1 and one hot columns
NUMERIC_CHECK: str | None = "C"       # D8 numeric check option
FINAL_NUMERIC_UNITS: str | None = "scaled"  # D8 "scaled" or "real" units in the final file
FLAG_SYNTHETIC: bool | None = True     # D8 True if you add a 0/1 column marking SMOTE rows

# One list so tests and the checkpoint summary can report which slots are still blank.
DECISION_SLOTS: dict[str, str] = {
    "SPLIT_SEED": "D1", "STRATIFY_ON": "D1",
    "IMPUTE_STRATEGY": "D3", "ADD_MISSING_FLAG": "D3",
    "ONEHOT_DROP_FIRST": "D4",
    "SCALER": "D5", "SCALE_COLUMNS": "D5",
    "SMOTE_VARIANT": "D7", "SMOTE_K_NEIGHBORS": "D7",
    "SMOTE_SAMPLING_STRATEGY": "D7", "SMOTE_RANDOM_STATE": "D7",
    "REPAIR_RULE": "D8", "NUMERIC_CHECK": "D8", "FINAL_NUMERIC_UNITS": "D8",
    "FLAG_SYNTHETIC": "D8",
}
