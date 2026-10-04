# D2: Which rows or columns do I remove or recode?

**Decided at:** checkpoint H1, with all other cards in one sitting. **Reviewed at:** H3. **Feeds:** ADR 0002.
**Canvas GL2:** "perform cleanup using Modules 4 and 5 guidelines"
**Canvas GL4:** "NEVER EVER change the dataset manually. If you do this you have failed the exam. All changes to be done via Python code in Jupyter lab."

## The question

Two separate questions, answered from your EDA on train:

1. **Rare category values.** The dataset documentation lists the gender values as "Male",
   "Female" or "Other". If your train EDA shows a category value with very few rows (gender or any
   other column), what do you do with it?
2. **The `id` column.** The documentation calls it a unique identifier. Does it stay, and if so,
   where?

## Why it matters (plain words)

A category with only a handful of cards gives a model almost nothing to learn from, and it
creates columns that are almost always 0. An id is a label printed on the card, not a fact about
the patient, but it can be useful for tracing a row back to the raw file.

## Options for a rare category value

| Option | Pros | Cons |
|---|---|---|
| A. Remove those rows from train | Simple; no near empty columns | Loses real rows; the test set may still contain the value, so the transform must handle it |
| B. Keep it as its own category | Keeps every row; honest to the data | Adds a column that is almost always 0; methods that measure distance treat it like any other column |
| C. Merge it into another group or an "unknown" group | Keeps rows; fewer columns | The merged group now mixes different things; you must justify the mapping |
| D. Treat it as missing and fill it (see D3) | Keeps rows | Invents a value for a real answer |

Whatever you choose, decide it from train only, and make sure the test transform cannot crash on
a value it did not see in train (for example `OneHotEncoder(handle_unknown="ignore")`).

## Options for `id`

| Option | Pros | Cons |
|---|---|---|
| A. Drop it before any modeling step | No risk of a label being used as a number | Rows can no longer be traced back to the raw file after processing |
| B. Keep it as a row key outside the feature columns (not passed to SMOTE or scalers) | Traceability for real rows | Synthetic rows have no real id; you must decide what they get |
| C. Keep it as a feature | Nothing removed | Distance based methods and models read it as a meaningful number |

## How to test the choice on your own data

1. In train only, count the rows for every category value of every text column. Write the
   counts you see in your notebook (from the cell output).
2. For each option you consider, count how many train rows it removes or changes.
3. Fit your encoder on train, then transform a tiny made up frame that contains an unseen value
   and confirm the transform does what you intend (no crash, no silent wrong row).
4. If you keep `id`, check that the processed files never contain a test id among the train rows
   (the test `test_ids_in_final_trace_back_to_train_only` does this).

## My decision (Joseph fills this in at H1, in his own words)

* **Option I chose:**
* **Why, in my words:**
* **Source** (module or lecture, documentation page, or Prof Rao with date):
* **Evidence** (added at H3: notebook name and cell number, chart, report file):
* **What I will watch for** (a risk this choice brings):
* **Value set in `src/stroke_prep/config.py`** (if any):
* **ADR:** `docs/adr/____-________.md`
* **Signed:** Joseph Clay, date and time (CT):

## Review at H3 (Joseph)

* [ ] Keep as decided   [ ] Amend (new option, and why, in my words):
* **What in the H3 evidence I looked at:**
* **Signed:** Joseph Clay, date and time (CT):
