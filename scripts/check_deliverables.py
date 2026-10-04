#!/usr/bin/env python3
"""Tooling (not graded): fail if any Canvas deliverable file is missing.

Expected to FAIL until H4. Paths match the README Deliverables table.
"""
import sys
from pathlib import Path

REQUIRED = {
    "1 dataset URL document": "docs/dataset_url.md",
    "2 one page proposal PDF": "docs/MT_JosephClay_ITAI1371_Proposal.pdf",
    "3 split notebook (70/30)": "notebooks/01_load_split.ipynb",
    "4 EDA on train only": "notebooks/02_eda_train.ipynb",
    "5a before and after cleanup, encoding, scaling": "notebooks/03_preprocess_before_after.ipynb",
    "5b before and after SMOTE balancing": "notebooks/04_smote_balance.ipynb",
    "7a reflection journal": "docs/MTJournal_R_JosephClay_ITAI1371.pdf",
    "7b contribution journal": "docs/MTJournal_C_JosephClay_ITAI1371.pdf",
    "8 FINAL clean dataset (train, SMOTE balanced)": "data/processed/stroke_clean_final.csv",
    "8 support: test set (never balanced)": "data/processed/stroke_test_transformed.csv",
    "raw data (untouched)": "data/raw/healthcare-dataset-stroke-data.csv",
}
# Item 6 (upload the .ipynb) is covered by the four notebooks above.


def main() -> int:
    missing = [f"{k}: {v}" for k, v in REQUIRED.items() if not Path(v).exists()]
    for line in missing:
        print("MISSING", line)
    if missing:
        return 1
    print(f"OK all {len(REQUIRED)} deliverable files present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
