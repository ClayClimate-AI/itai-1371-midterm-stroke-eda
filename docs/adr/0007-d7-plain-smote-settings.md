# ADR 0007: Plain SMOTE on work_type with k 5, "auto", seed 33, float input (D7)

> Drafted by the builder agent from Joseph's signed card.
> Every reason below is quoted from `docs/decisions/D7_smote_setup.md`. Every result is quoted from the
> printed outputs of `notebooks/04_smote_balance.ipynb`. Nothing else was added.

* **Status:** Accepted
* **Date:** Oct 04, 2026
* **Checkpoint:** H2 (column types line added at H3)
* **Decision card:** `docs/decisions/D7_smote_setup.md`
* **Canvas line this supports:** "Class Balancing the dataset"

## Context
Prof Rao fixed SMOTE and the column to balance (`work_type`). The card asks for every setting.

Notebook outputs that show it:
* `notebooks/04_smote_balance.ipynb` cell 7, In[4]: Private 2040, Self-employed 585, children 477, Govt_job 461, Never_worked 13; `smallest group: 13 | k_neighbors: 5`

## Options considered
From the D7 card:
* Variant: `SMOTE` or a variant such as `SMOTENC`
* The target `stroke`: (a) ride along in X, or (b) set aside and attach afterwards
* `k_neighbors`: the library default or another value
* `sampling_strategy`: `"auto"` or a dictionary of target counts
* `random_state`: any fixed integer
* Column types going in: as loaded, or cast to float first

## Decision
Plain `SMOTE`, y = work_type, stroke in X (option a), `k_neighbors = 5`, `sampling_strategy = "auto"`, `random_state = 33`, signed by Joseph Clay on 10/04/2026 at 3:33 PM (CT). Column types: cast to float first, added to the card on 10/04/2026 at 4:46 PM (CT).

Joseph's reasoning, quoted from the card:

> Prof Rao fixed SMOTE and work_type, and plain SMOTE is the basic method, so there's no variant to justify. My smallest work_type group in train is Never_worked with 13 rows. k has to be below that, so the default of 5 works. "auto" grows every smaller group to the size of the largest group (Private), which is the simplest to explain. random_state 33 matches my split seed so the run repeats, and I won't change it after seeing results. stroke rides along in X like any other 0/1 column and gets repaired in D8.

> Column types going in: cast to float first, so blended 0/1 values reach the D8 repair and are rounded at 0.5 instead of being cut off (0.76 would become 0 as loaded).

Source, quoted from the card: "Prof Rao in class, Oct 1, 2026; Canvas P4; D7 card; imbalanced-learn SMOTE documentation; work_type counts in notebooks/02_eda_train.ipynb"

## Consequences
* Good: cell 9, In[6]: every work_type group is 2040 after SMOTE, `rows added: 6624`. Cell 13, In[9]: `real rows unchanged; every new row is marked 1`.
* Bad or risk, quoted from the card: "Never_worked grows from 13 rows to about 2,040, so about 99% of that group will be synthetic, made from only 13 real rows. I'll compare its synthetic rows against the real ones. Synthetic stroke values come out blended and must be rounded back to 0/1. The real rows must come back unchanged." Cell 9, In[6] prints Never_worked `added 2027`.
* Follow up: the card's "Review at H3" block is still for Joseph to complete.

## Evidence
* Notebook and cell: `notebooks/04_smote_balance.ipynb` cells 5 (settings), 7 to 10 (counts and chart), 12 to 15 (synthetic rows, real rows check, dtypes)
* Validator report: `docs/reports/data-validator/H3_20261004_1618.md` §2 (D7 steps); `docs/reports/data-validator/H3_20261004_1704.md` §2 and §4 (column types)
* Test: `tests/test_pipeline_contracts.py::test_balance_keeps_real_rows_unchanged`, `tests/test_pipeline_contracts.py::test_balance_flags_every_row`, `tests/test_decision_slots.py::test_smote_k_neighbors`
* Commit: `ccc2dc4` (card), `0b94ef8` (column types line), `a7ddbbc` (notebook 04)
