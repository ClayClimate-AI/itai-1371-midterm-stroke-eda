# D3: How do I fill missing values, and do I add a missing flag?

**Decided at:** checkpoint H1, with all other cards in one sitting. **Reviewed at:** H3. **Feeds:** ADR 0003.
**Canvas P1:** "Filling NaN and Null with appropriate values"
**Canvas P7:** "Feature engineering"

## The question

Your load step and EDA show which columns have missing values and how many (use your own cell
output). How do you fill them, using only train to learn the fill values? Do you also keep a
record of which rows were originally missing?

## Why it matters (plain words)

A blank on a card stops many tools from working at all (SMOTE and most scalers refuse blanks).
Filling a blank means writing in a best guess. A missing flag is a small sticker that says "this
was blank before", so the guess never hides the fact that the value was missing.

## Options for the fill value

| Option | Pros | Cons |
|---|---|---|
| A. Train median | Not pulled by extreme values; simple; easy to reuse on test | Every filled row gets the same value, which narrows the spread |
| B. Train mean | Simple; keeps the column mean unchanged | Pulled by extreme values; same narrowing as A |
| C. Median within groups learned on train (for example by age band or another column) | Uses related information; filled values vary | More choices to justify; small groups give unstable values |
| D. Model based (`KNNImputer` or `IterativeImputer`, fit on train) | Uses several columns; filled values vary | More complex; depends on scaling and encoding; harder to explain |
| E. Drop rows with missing values | No guessed values | Canvas P1 asks for filling; loses real rows; may remove a pattern |

## Options for a missing flag (feature engineering)

| Option | Pros | Cons |
|---|---|---|
| A. Add a 0/1 column such as `bmi_missing`, created BEFORE filling | Keeps the information that a value was missing; counts as feature engineering | One more column; it must stay 0/1 after SMOTE |
| B. No flag | Fewer columns | The fact that a value was missing is lost once it is filled |

## How to test the choice on your own data (train only)

You decide at H1 from the options, your course material and the dataset documentation. After
the split, the agents run these checks on train and put the raw outputs (no interpretation) in
your H3 summary. At H3 you keep or amend the decision.

1. Count missing values per column in train (cell output) and write the count you see.
2. Compare the column's distribution before and after each fill option you consider (histogram
   and `describe()`), and note how the spread changes.
3. Compare the rows with and without a missing value on a few other columns, including the
   target. Describe what you see in your own words. Whatever you find is evidence for or against
   keeping a flag; it is not a required result.
4. Check the fill value is learned from train only, then applied to test unchanged.
5. Confirm zero missing values remain after the step (`isna().sum()`).

## My decision (Joseph fills this in at H1, in his own words)

* **Option I chose:** Fill: A, train median. Flag: A, add a 0/1 `bmi_missing` column before filling.

* **Why, in my words:**
  bmi is the only column with blanks: 138 in train (3.9%). bmi has an extreme high value (max 97.6) that pulls the mean, so the median (28.1) is a safer middle value. The median is learned from train only and applied to test unchanged. I add `bmi_missing` before filling so the fact that a value was blank isn't lost, which also counts as feature engineering (Canvas P7). smoking_status "Unknown" (1,082 rows, 30%) is not a blank in the file. It's a real answer, so I keep it as its own category and encode it in D4 instead of filling it.

* **Source:** Canvas P1 and P7; D3 card; train EDA in notebooks/02_eda_train.ipynb (missing values cell, bmi histogram); scikit-learn SimpleImputer documentation

* **Evidence** (added at H3: notebook name and cell number, chart, report file):

* **What I will watch for:** All 138 filled rows get the same value, which narrows bmi's spread a little. `bmi_missing` has to stay 0/1 after SMOTE (the D8 repair handles that). No blanks can remain after this step.

* **Value set in `src/stroke_prep/config.py`:** `IMPUTE_STRATEGY = "median"`, `ADD_MISSING_FLAG = True`

* **ADR:** `docs/adr/____-________.md`

* **Signed:** Joseph Clay, 10/04/2026 3:26PM (CT)

## Review at H3 (Joseph)

* [ ] Keep as decided   [ ] Amend (new option, and why, in my words):
* **What in the H3 evidence I looked at:**
* **Signed:** Joseph Clay, date and time (CT):
