# Spec: `notebooks/04_smote_balance.ipynb` (checkpoint H3)

Requirements only. Settings come from decision cards D6, D7 and D8. No expected results.

## Canvas lines this notebook satisfies

* **P4:** "Class Balancing the dataset"
* **P5:** "One hot encoding"
* **P6:** "Encoding categorical to numbers"
* **GL5:** "Use Matplotlib to plot data distributions and show before and after preprocessing (example: balancing)"
* **GL6:** "Print sample data as it gets processed"
* **GL8:** "Discuss how you would use this dataset to solve an ML problem"
* **GL9:** "Finals will implement models on this prepared dataset"
* **S5:** "Jupyter notebook demonstrating before and after data processing"
* **S8:** "Upload final clean dataset"

## Acceptance criteria

1. Loads the prepared train file from notebook 03 (train only).
2. Runs SMOTE with y = `work_type` (Prof Rao, in class, Oct 1, 2026) on train only, with the
   settings from D7. If D8 chose a marking column (`FLAG_SYNTHETIC`), adds `is_synthetic`
   (1 for every new row, 0 for every real row).
3. Repairs and checks synthetic rows as chosen in D8, and prints the counts of what changed.
4. Before and after charts chosen by Joseph that show the balancing column and its effect on the
   other columns, plus a before and after table produced by code.
5. Saves `data/processed/stroke_clean_final.csv`: no missing values, all numeric, target and
   `is_synthetic` present if D8 chose it.
6. Transforms the test set with the train fitted objects only (no fitting, no SMOTE) and saves
   `data/processed/stroke_test_transformed.csv` with the same columns.
7. Final markdown cell, in Joseph's words: how this dataset could be used to solve an ML problem.

## Checks (Engineering extra, not graded)

* `tests/test_invariants_final.py`, `tests/test_pipeline_contracts.py` (balance and repair part),
  data-validator and repo-auditor reports for H3.
