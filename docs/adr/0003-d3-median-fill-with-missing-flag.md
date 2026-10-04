# ADR 0003: Fill bmi with the train median and add a bmi_missing flag (D3)

> Drafted by the builder agent from Joseph's signed card.
> Every reason below is quoted from `docs/decisions/D3_missing_values.md`. Every result is quoted from the
> printed outputs of `notebooks/03_preprocess_before_after.ipynb` and `notebooks/04_smote_balance.ipynb`. Nothing else was added.

* **Status:** Accepted
* **Date:** Oct 04, 2026
* **Checkpoint:** H2
* **Decision card:** `docs/decisions/D3_missing_values.md`
* **Canvas line this supports:** "Filling NaN and Null with appropriate values"

## Context
The card asks how to fill blanks and whether to keep a record of which values were blank.

Notebook outputs that show it:
* `notebooks/03_preprocess_before_after.ipynb` cell 18, In[10]: `bmi 138`, every other column `0`
* cell 14, In[8]: `columns filled: ['bmi']`, `fill values learned: {'bmi': np.float64(28.1)}`

## Options considered
From the D3 card, fill:
* A. Train median
* B. Train mean
* C. Median within groups learned on train
* D. Model based (`KNNImputer` or `IterativeImputer`, fit on train)
* E. Drop rows with missing values

From the D3 card, flag:
* A. Add a 0/1 column such as `bmi_missing`, created before filling
* B. No flag

## Decision
Fill option A and flag option A (`IMPUTE_STRATEGY = "median"`, `ADD_MISSING_FLAG = True`), signed by Joseph Clay on 10/04/2026 at 3:26 PM (CT).

Joseph's reasoning, quoted from the card:

> bmi is the only column with blanks: 138 in train (3.9%). bmi has an extreme high value (max 97.6) that pulls the mean, so the median (28.1) is a safer middle value. The median is learned from train only and applied to test unchanged. I add `bmi_missing` before filling so the fact that a value was blank isn't lost, which also counts as feature engineering (Canvas P7). smoking_status "Unknown" (1,082 rows, 30%) is not a blank in the file. It's a real answer, so I keep it as its own category and encode it in D4 instead of filling it.

Source, quoted from the card: "Canvas P1 and P7; D3 card; train EDA in notebooks/02_eda_train.ipynb (missing values cell, bmi histogram); scikit-learn SimpleImputer documentation"

## Consequences
* Good: cell 21, In[13]: `missing values left: 0`. Cell 22, In[14]: `{'bmi_missing': 138}`. `notebooks/04_smote_balance.ipynb` cell 40, In[27]: `test blanks hold the train learned fill values`.
* Bad or risk, quoted from the card: "All 138 filled rows get the same value, which narrows bmi's spread a little. `bmi_missing` has to stay 0/1 after SMOTE (the D8 repair handles that). No blanks can remain after this step." The spread before and after is printed in cell 24, In[16].
* Follow up: the card's "Review at H3" block is still for Joseph to complete.

## Evidence
* Notebook and cell: `notebooks/03_preprocess_before_after.ipynb` cells 14 (fit), 18 to 22 (counts and flag), 23 to 25 (before and after charts and table); `notebooks/04_smote_balance.ipynb` cell 40 (test fill check)
* Validator report: `docs/reports/data-validator/H3_20261004_1618.md` §2 (D3 steps) and §3 (leakage)
* Test: `tests/test_pipeline_contracts.py::test_transformed_train_has_no_missing_values`, `tests/test_invariants_final.py::test_final_has_no_missing_values`, `tests/test_invariants_final.py::test_test_set_has_no_missing_values`
* Commit: `ccc2dc4` (card), `a7ddbbc` (notebooks 03 and 04)
