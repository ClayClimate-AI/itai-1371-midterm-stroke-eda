# ADR 0004: Full one hot encoding, work_type encoded after SMOTE (D4)

> Drafted by the builder agent from Joseph's signed card.
> Every reason below is quoted from `docs/decisions/D4_encoding.md`. Every result is quoted from the
> printed outputs of `notebooks/03_preprocess_before_after.ipynb` and `notebooks/04_smote_balance.ipynb`. Nothing else was added.

* **Status:** Accepted
* **Date:** Oct 04, 2026
* **Checkpoint:** H2
* **Decision card:** `docs/decisions/D4_encoding.md`
* **Canvas line this supports:** "One hot encoding"

## Context
The card asks how to turn the five text columns into numbers.

Notebook outputs that show it:
* `notebooks/03_preprocess_before_after.ipynb` cell 29, In[19]: `before: 11` columns, `after: 18` columns
* cell 30, In[20]: `gender {1: 3576}`, `ever_married {1: 3576}`, `Residence_type {1: 3576}`, `smoking_status {1: 3576}`

## Options considered
From the D4 card:
* A. Full one hot
* B. One hot, drop one column per group
* C. 0/1 mapping for two value columns, one hot for the rest
* D. Ordinal or label codes

## Decision
Option A with `OneHotEncoder(handle_unknown="ignore")` (`ONEHOT_DROP_FIRST = False`), signed by Joseph Clay on 10/04/2026 at 3:30 PM (CT).

Joseph's reasoning, quoted from the card:

> None of the five text columns has a natural order. Numbering them 1, 2, 3 would invent one (as if "smokes" were bigger than "never smoked"), and SMOTE would read those gaps as real distances. Full one hot gives each category its own 0/1 column, and the rule is easy to check and repair: exactly one 1 per group. I don't drop a column per group, because "exactly one 1" is simpler to check after SMOTE than "at most one 1". work_type is the column SMOTE balances, so it stays a label during SMOTE and is encoded afterwards so the final file is all numbers.

Source, quoted from the card: "Canvas P5 and P6; D4 card; scikit-learn OneHotEncoder documentation; category counts in notebooks/02_eda_train.ipynb"

## Consequences
* Good: cell 30, In[20] shows every group sums to 1 on train. `notebooks/04_smote_balance.ipynb` cell 32, In[21] shows each work_type label count equals its one hot column sum (2040 each), and cell 39, In[26] prints `same columns in the same order; no missing values` for test.
* Bad or risk, quoted from the card: "More columns, and each group always adds up to 1, which matters for some linear models in the Final. Train and test must end up with the same column names in the same order."
* Follow up: the card's "Review at H3" block is still for Joseph to complete.

## Evidence
* Notebook and cell: `notebooks/03_preprocess_before_after.ipynb` cells 29 to 32; `notebooks/04_smote_balance.ipynb` cells 31, 32, 39
* Validator report: `docs/reports/data-validator/H3_20261004_1618.md` §2 (D4 steps) and §5 (integrity); `docs/reports/data-validator/H3_20261004_1704.md` §3
* Test: `tests/test_invariants_final.py::test_each_onehot_group_is_valid`, `tests/test_invariants_final.py::test_test_set_has_same_columns_as_final`
* Commit: `ccc2dc4` (card), `a7ddbbc` (notebooks 03 and 04)
