# ADR 0006: Fill, encode and scale, then plain SMOTE (D6)

> Drafted by the builder agent from Joseph's signed card.
> Every reason below is quoted from `docs/decisions/D6_order_around_smote.md`. Every result is quoted from the
> printed outputs of `notebooks/03_preprocess_before_after.ipynb` and `notebooks/04_smote_balance.ipynb`. Nothing else was added.

* **Status:** Accepted
* **Date:** Oct 04, 2026
* **Checkpoint:** H2
* **Decision card:** `docs/decisions/D6_order_around_smote.md`
* **Canvas line this supports:** "Class Balancing the dataset"

## Context
The card asks in which order the preprocessing steps and SMOTE run.

Notebook outputs that show it:
* `notebooks/03_preprocess_before_after.ipynb` cell 20, In[12]: prepared train `shape: (3576, 18)`, with work_type kept as a text label
* `notebooks/04_smote_balance.ipynb` cell 8, In[5]: `shape: (10200, 19)` after SMOTE

## Options considered
From the D6 card:
* A. Fill, encode and scale, then plain SMOTE
* B. Fill and encode, plain SMOTE, then scale
* C. Fill, scale numbers, SMOTENC with the text columns as categories
* D. Another order you can justify

## Decision
Option A, signed by Joseph Clay on 10/04/2026 at 3:32 PM (CT).

Joseph's reasoning, quoted from the card:

> Plain SMOTE needs every column to be a number with no blanks, and it picks neighbors by distance. So bmi has to be filled, the text columns encoded, and the three number columns scaled before SMOTE runs, which puts every column on a similar ruler. This follows Prof Rao's Oct 1 guidance to balance work_type with SMOTE. Every fill value, encoder and scaler is fit on train only, and SMOTE runs on train only.

Source, quoted from the card: "Prof Rao in class, Oct 1, 2026; Canvas P4; D6 card; imbalanced-learn SMOTE documentation"

## Consequences
* Good: SMOTE ran on the prepared train rows without an error (`notebooks/04_smote_balance.ipynb` cell 8, In[5]). The real and synthetic number summaries in real units are in cell 28, In[19].
* Bad or risk, quoted from the card: "SMOTE will create in between values in the 0/1 and one hot columns (like 0.4 for hypertension), which D8 repairs. The scaler describes real train rows only, because it is fit before SMOTE. Test goes through the same train fitted steps and is never balanced."
* Follow up: the card's "Review at H3" block is still for Joseph to complete.

## Evidence
* Notebook and cell: `notebooks/03_preprocess_before_after.ipynb` cell 2 (step order heading), cells 14 and 20; `notebooks/04_smote_balance.ipynb` cells 8, 12 (synthetic rows in real units), 27 and 28 (real vs synthetic)
* Validator report: `docs/reports/data-validator/H3_20261004_1618.md` §1 (D6 MATCH) and §2 (D6 steps)
* Test: `tests/test_pipeline_contracts.py::test_balance_only_adds_rows`, `tests/test_invariants_final.py::test_test_set_was_never_balanced`
* Commit: `ccc2dc4` (card), `a7ddbbc` (notebooks 03 and 04)
