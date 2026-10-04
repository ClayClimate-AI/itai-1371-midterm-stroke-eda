# Spec: `notebooks/01_load_split.ipynb` (checkpoint H2)

Requirements only. They say WHAT must be true, not HOW to code it, and contain no expected
results. Method choices come from decision card D1.

## Canvas lines this notebook satisfies

* **GL1:** "choose Kaggle dataset >=2000 rows"
* **GL4:** "NEVER EVER change the dataset manually. If you do this you have failed the exam. All changes to be done via Python code in Jupyter lab."
* **GL6:** "Print sample data as it gets processed"
* **S3:** "In jupyter notebook use python to split dataset: training 70%, testing 30%; Python loads training data into memory; do not split manually or in excel"
* **S10:** "DO NOT change original dataset manually"

## Acceptance criteria

1. First cell makes `src/` importable (`sys.path.insert(0, str(Path.cwd().parent / "src"))`) and
   imports `stroke_prep.config` for every path.
2. Loads the raw CSV with Python from `data/raw/` (no manual edits, no Excel), reading the file's
   missing value placeholders as missing.
3. Prints shape, dtypes, `head()` and missing counts before any change.
4. Splits ONCE with Python into 70% train and 30% test, using the stratification and seed from D1.
5. Prints the size of each part, the shares you chose to check in D1, and `train.head()` (the
   training data is in memory).
6. Asserts: the parts add up to the raw row count; no id in both parts.
7. Saves `data/interim/train_raw.csv` and `data/interim/test_raw.csv` by code.
8. Last cell asserts the raw file SHA256 still matches `data/raw/SHA256SUMS`.
9. Markdown cells explain each step in Joseph's words, written only after the cell above them ran.
10. Runs clean with Restart and Run All; outputs kept.

## Checks (Engineering extra, not graded)

* `tests/test_invariants_split.py`, `tests/test_raw_data.py`, `tests/test_pipeline_contracts.py`
  (split part), data-validator report for H2.
