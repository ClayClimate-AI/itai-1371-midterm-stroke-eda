# Spec: `notebooks/03_preprocess_before_after.ipynb` (checkpoint H3)

Requirements only. Every method in this notebook comes from a signed decision card.

## Canvas lines this notebook satisfies

* **P1:** "Filling NaN and Null with appropriate values"
* **P2:** "Scaling"
* **P3:** "Normalization"
* **P5:** "One hot encoding"
* **P6:** "Encoding categorical to numbers"
* **P7:** "Feature engineering"
* **GL5:** "Use Matplotlib to plot data distributions and show before and after preprocessing (example: balancing)"
* **GL6:** "Print sample data as it gets processed"
* **GL7:** "Build a Jupyter notebook to show dataset before and after cleanup"
* **S5:** "Jupyter notebook demonstrating before and after data processing"

## Acceptance criteria

1. Loads `data/interim/train_raw.csv`. Never loads the test file.
2. Applies D2 (rows and columns) and D3 (missing values), learning every value from train only.
   Shows a before and after chart and prints `head()`. Asserts no missing values remain.
3. Applies D4 (encoding) with an encoder fit on train only. Shows the columns before and after
   and prints `head()`.
4. Applies D5 (scaling) with a scaler fit on train only, and also demonstrates normalization
   (Canvas P3). Shows numeric columns before and after.
5. Follows the step order chosen in D6, and says so in a markdown cell.
6. Saves what notebook 04 needs (for example `data/interim/train_prepared.csv`) by code.
7. Every markdown interpretation is in Joseph's words and cites the cell that produced each
   number.

## Checks (Engineering extra, not graded)

* `tests/test_pipeline_contracts.py` (fit and transform part), data-validator reports for H3.
