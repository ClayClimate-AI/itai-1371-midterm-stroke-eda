# ADR 0005: StandardScaler on age, avg_glucose_level and bmi (D5)

> Drafted by the builder agent from Joseph's signed card.
> Every reason below is quoted from `docs/decisions/D5_scaling.md`. Every result is quoted from the
> printed outputs of `notebooks/03_preprocess_before_after.ipynb` and `notebooks/04_smote_balance.ipynb`. Nothing else was added.

* **Status:** Accepted
* **Date:** Oct 04, 2026
* **Checkpoint:** H2
* **Decision card:** `docs/decisions/D5_scaling.md`
* **Canvas line this supports:** "Scaling"

## Context
The card asks which scaler to use and on which columns.

Notebook outputs that show it:
* `notebooks/03_preprocess_before_after.ipynb` cell 35, In[23]: real units min and max: age 0.0800 to 82.0000, avg_glucose_level 55.1200 to 267.7600, bmi 11.3000 to 97.6000

## Options considered
From the D5 card:
* A. `StandardScaler`
* B. `MinMaxScaler`
* C. `RobustScaler`
* D. Leave a column unscaled

## Decision
Option A on `["age", "avg_glucose_level", "bmi"]` (`SCALER = "StandardScaler"`), signed by Joseph Clay on 10/04/2026 at 3:31 PM (CT). MinMaxScaler is shown only as the normalization exercise.

Joseph's reasoning, quoted from the card:

> The three number columns use very different rulers: age 0.08 to 82, glucose 55.12 to 267.76, bmi 11.3 to 97.6. SMOTE measures distance, so without scaling glucose would count the most just because its numbers are bigger. StandardScaler puts each one on mean 0 and standard deviation 1, learned from train only, and keeps the shape of each distribution. The 0/1 columns already sit between 0 and 1, so I leave them alone and they stay 0/1.

Source, quoted from the card: "Canvas P2 and P3; D5 card; scikit-learn StandardScaler and MinMaxScaler documentation; number column summaries in notebooks/02_eda_train.ipynb"

## Consequences
* Good: cell 36, In[24]: mean `-0.0000 0.0000 -0.0000`, std `1.0001 1.0001 1.0001`. Cell 40, In[26]: MinMaxScaler min `0.0` and max `1.0` for each column.
* Bad or risk, quoted from the card: "Glucose's long right tail and bmi's extreme high value pull the mean and standard deviation. Scaled values are z scores, so I keep the fitted scaler to convert back to real units for charts and range checks. Test values outside the train range are expected, not an error." The test range is printed in `notebooks/04_smote_balance.ipynb` cell 43, In[29].
* Follow up: the card's "Review at H3" block is still for Joseph to complete.

## Evidence
* Notebook and cell: `notebooks/03_preprocess_before_after.ipynb` cells 35 to 37 (StandardScaler), 40 and 41 (normalization exercise), 44 (scaler saved); `notebooks/04_smote_balance.ipynb` cell 43 (test range)
* Validator report: `docs/reports/data-validator/H3_20261004_1618.md` §2 (D5 steps) and §3 (scaler fit on train only)
* Test: `tests/test_pipeline_contracts.py::test_transform_is_row_by_row`, `tests/test_decision_slots.py::test_scale_columns`
* Commit: `ccc2dc4` (card), `a7ddbbc` (notebooks 03 and 04)
