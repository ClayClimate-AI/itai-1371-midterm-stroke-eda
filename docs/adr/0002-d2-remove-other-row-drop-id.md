# ADR 0002: Remove the gender "Other" row from train and drop id (D2)

> Drafted by the builder agent from Joseph's signed card.
> Every reason below is quoted from `docs/decisions/D2_rows_and_columns.md`. Every result is quoted from the
> printed outputs of `notebooks/03_preprocess_before_after.ipynb`. Nothing else was added.

* **Status:** Accepted
* **Date:** Oct 04, 2026
* **Checkpoint:** H2
* **Decision card:** `docs/decisions/D2_rows_and_columns.md`
* **Canvas line this supports:** "perform cleanup using Modules 4 and 5 guidelines"

## Context
The card asks what to do with very rare category values and with the id column.

Notebook outputs that show it:
* `notebooks/03_preprocess_before_after.ipynb` cell 9, In[5]: `{'Female': 2121, 'Male': 1455, 'Other': 1}`
* cell 10, In[6]: `rows before: 3577 / rows after: 3576 / rows removed: 1`

## Options considered
From the D2 card, rare values:
* A. Remove those rows from train
* B. Keep it as its own category
* C. Merge it into another group or an "unknown" group
* D. Treat it as missing and fill it (see D3)

From the D2 card, id:
* A. Drop it before any modeling step
* B. Keep it as a row key outside the feature columns
* C. Keep it as a feature

## Decision
Rare value option A and id option A, signed by Joseph Clay on 10/04/2026 at 3:22 PM (CT).

Joseph's reasoning, quoted from the card:

> My train EDA shows gender has only 1 "Other" row out of 3,577. One row can't teach a model anything, and keeping it would add a column that is 0 in every other row. Removing it costs 0.03% of train. The id column is a unique label (3,577 different ids in 3,577 rows), not a fact about the patient. If it stayed, SMOTE and the scaler would read it as a real number and use it to measure distance, so I drop it before any modeling step. Both changes are made with Python code in the notebook, never by hand (Canvas GL4).

Source, quoted from the card: "Canvas GL2 and GL4; D2 card; train EDA in notebooks/02_eda_train.ipynb (gender counts) and notebooks/01_load_split.ipynb (id check); scikit-learn OneHotEncoder documentation (handle_unknown)"

## Consequences
* Good: cell 10, In[6] shows 1 row removed. Cell 15, In[9] shows a gender value the encoder never saw becomes `gender_Female 0, gender_Male 0` instead of an error.
* Bad or risk, quoted from the card: "The test set could still hold an "Other" value. The encoder uses `handle_unknown="ignore"`, so that row gets all zeros in the gender group instead of crashing. Once id is dropped, processed rows can't be traced back to the raw file."
* Follow up: the card's "Review at H3" block is still for Joseph to complete.

## Evidence
* Notebook and cell: `notebooks/03_preprocess_before_after.ipynb` cells 8 (rule), 9 and 10 (counts and removal), 11 (before and after chart), 15 (unseen value)
* Validator report: `docs/reports/data-validator/H3_20261004_1618.md` §1 (card vs notebook) and §2 (D2 steps)
* Test: `tests/test_invariants_final.py::test_real_rows_reconcile_with_train`, `tests/test_invariants_final.py::test_ids_in_final_trace_back_to_train_only` (skips because id is not kept)
* Commit: `ccc2dc4` (card), `a7ddbbc` (notebook 03)
