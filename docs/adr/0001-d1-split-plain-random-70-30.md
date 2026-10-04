# ADR 0001: Plain random 70/30 split with a fixed seed (D1)

> Drafted by the builder agent from Joseph's signed D1 card.
> Every reason below is quoted from `docs/decisions/D1_split.md`. Every result is quoted from the
> printed outputs of `notebooks/01_load_split.ipynb`. Nothing else was added.

* **Status:** Accepted
* **Date:** Oct 04, 2026
* **Checkpoint:** H1
* **Decision card:** `docs/decisions/D1_split.md`
* **Canvas line this supports:** "In jupyter notebook use python to split dataset: training 70%, testing 30%; Python loads training data into memory; do not split manually or in excel"

## Context
Canvas S3 fixes the ratio (70/30) and the tool (Python in a notebook). The D1 card left three
choices open: whether to stratify, on which column, and which random seed makes the split
repeatable.

Notebook outputs that show the split:
* `notebooks/01_load_split.ipynb` cell 6, In[3]: `shape: (5110, 12)`
* cell 12, In[7]: `TEST_SIZE: 0.3 / SPLIT_SEED: 33 / STRATIFY_ON: None`
* cell 13, In[8]: `train rows: 3577 / test rows: 1533`

## Options considered
From the D1 card:
* A. Plain random split: `train_test_split(..., test_size=0.30, random_state=seed)`
* B. Stratify on the target `stroke`
* C. Stratify on `work_type`
* D. Stratify on `stroke` and `work_type` together

## Decision
Option A, a plain random split with `SPLIT_SEED = 33` and `STRATIFY_ON = None`, signed by Joseph
Clay on 10/04/2026 at 9:49 AM (CT).

Joseph's reasoning, quoted from the card:

> Canvas S3 asks for a 70/30 split in Python and nothing more, so a plain random split (option A) meets it as written. A random split is a shuffle made by a formula, and the seed (`random_state`) is that formula's starting number. When I set a fixed seed, the same rows land in train and test every run. If I leave it unset, the starting number changes each time, so the split changes and can't be reproduced. The seed alone isn't enough, though. Reproducibility needs the same data, the same code, and the same seed, which is why the repo pins all three. The number I pick doesn't affect quality. I set it once and won't change it after seeing results, because trying seeds until results look better is cherry picking.

Source, quoted from the card: "Canvas S3 (70/30 split in Python); D1 card; tutor-reviewer explanation, Oct 4, 2026; scikit-learn train_test_split documentation (random_state)"

## Consequences
* Good: the split checks in notebook 01 passed:
  * cell 21, In[12]: `rows add up and no id is in both parts`
  * cell 22, In[13]: `every work_type group is in train and in test`
  * cell 23, In[14]: `same seed gives the same train ids`
  * cell 30, In[17]: `raw file hash matches SHA256SUMS`
* Bad or risk: the card lists this con for option A: "Shares of rare values can differ between the parts by chance". The stroke and work_type shares for each part are in cells 17 and 18 (In[10], In[11]). Joseph's risk to watch, quoted from the card: "If I ever changed the seed after seeing results, that would be cherry picking. I'll keep it fixed."
* Follow up: Joseph kept D1 at the H2 review, 10/04/2026 3:55 PM (CT).

## Evidence
* Notebook and cell: `notebooks/01_load_split.ipynb` cells 12 and 13 (settings and split), 17 and 18 (shares), 21 to 23 (split checks), 28 (save once, In[16]: `already saved, matches: train_raw.csv / already saved, matches: test_raw.csv`), 30 (raw hash)
* Validator report: `docs/reports/data-validator/H2_20261004_1231.md` (split invariants, D1 card vs notebook 01) and `docs/reports/data-validator/H2_20261004_1447.md` (claims check)
* Test: `tests/test_invariants_split.py::test_rows_reconcile_with_raw`, `tests/test_invariants_split.py::test_no_id_in_both_parts`, `tests/test_pipeline_contracts.py::test_split_is_repeatable`
* Commit: `149de94` (D1 card and config), `5f0abd5` (notebook 01 built and run)