# Spec: `notebooks/02_eda_train.ipynb` (checkpoint H2)

Requirements only. No expected results, no expected conclusions.

## Canvas lines this notebook satisfies

* **S4:** "EDA performed only on training data; testing data untouched"
* **GL5:** "Use Matplotlib to plot data distributions and show before and after preprocessing (example: balancing)"
* **GL6:** "Print sample data as it gets processed"
* **GL2:** "perform cleanup using Modules 4 and 5 guidelines"

## Acceptance criteria

1. Loads `data/interim/train_raw.csv` ONLY. The test file is never named in this notebook.
2. Prints `info()`, `describe()`, `head()`.
3. Matplotlib charts, each with a title and labeled axes, chosen by Joseph to cover: missing
   values, the target, the balancing column `work_type`, every text column, every numeric
   column's distribution, and relationships Joseph wants to check. The LAB_GUIDE has a menu of
   chart types; picking which ones is part of the analysis.
4. Under each chart, a markdown cell in Joseph's words says what the chart shows, citing the
   numbers printed by a cell above it.
5. A findings cell lists the data problems Joseph found and, for each, the decision card that
   will handle it (D2 to D8). No fix is chosen in this notebook.
6. No data is changed or saved (analysis only). A temporary helper column for analysis is allowed.

## Checks (Engineering extra, not graded)

* `test_eda_notebook_reads_train_only`, data-validator report for H2 (every number in the
  markdown cells is recomputed).
