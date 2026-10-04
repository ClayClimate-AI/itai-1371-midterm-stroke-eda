# D4: How do I turn text categories into numbers?

**Decided at:** checkpoint H1, with all other cards in one sitting. **Reviewed at:** H3. **Feeds:** ADR 0004.
**Canvas P5:** "One hot encoding"
**Canvas P6:** "Encoding categorical to numbers"

## The question

The text columns are `gender`, `ever_married`, `work_type`, `Residence_type` and
`smoking_status`. How do you encode each one, and when is `work_type` encoded, given that it is
the column SMOTE balances?

## Why it matters (plain words)

Math tools read numbers, not words. One hot encoding gives each word its own yes/no column, like
a row of tick boxes where exactly one box is ticked. Other encodings use fewer columns but can
add meaning that is not really there (for example, that "smokes" is "bigger than" "never smoked").

## Options

| Option | What it is | Pros | Cons |
|---|---|---|---|
| A. Full one hot | one 0/1 column per category (`pd.get_dummies` or `OneHotEncoder`) | No false order; easy rule to check: exactly one 1 per group | More columns; columns in a group always add up to 1 (perfectly related), which matters for some linear models |
| B. One hot, drop one column per group | k categories give k minus 1 columns (`drop="first"` or `drop_first=True`) | Removes the perfectly related column; fewer columns | Rule becomes "at most one 1"; the dropped category is implicit, so charts and repairs need care |
| C. 0/1 mapping for two value columns, one hot for the rest | for example Yes to 1 and No to 0 | Fewest columns for yes/no questions | Mixed scheme to document |
| D. Ordinal or label codes | one integer per category | One column per text column | Adds an order that may not exist; distance based methods read the gaps as real |

**`work_type` timing:** encode it before SMOTE (then it must be turned back into a label for SMOTE)
or keep it as the text label during SMOTE and encode it afterwards. Decide and write it down.

**Unseen categories:** decide what happens when test contains a value train did not have (for
example `handle_unknown="ignore"` gives an all zero group).

**Config:** after deciding, set `ONEHOT_DROP_FIRST` in `src/stroke_prep/config.py` (True for B,
False for A or C). The one hot group test reads it.

## How to test the choice on your own data

1. Print the column list and count before and after encoding (a before and after chart works).
2. Check every group follows its rule on train (row sums of each group).
3. Fit on train, transform test, and confirm both have identical column names in the same order.
4. Print `head()` after encoding (Canvas GL6: "Print sample data as it gets processed").

## My decision (Joseph fills this in at H1, in his own words)

* **Option I chose:** A, full one hot with `OneHotEncoder(handle_unknown="ignore")`. work_type stays a text label during SMOTE (it is y) and gets one hot encoded after SMOTE.

* **Why, in my words:**
  None of the five text columns has a natural order. Numbering them 1, 2, 3 would invent one (as if "smokes" were bigger than "never smoked"), and SMOTE would read those gaps as real distances. Full one hot gives each category its own 0/1 column, and the rule is easy to check and repair: exactly one 1 per group. I don't drop a column per group, because "exactly one 1" is simpler to check after SMOTE than "at most one 1". work_type is the column SMOTE balances, so it stays a label during SMOTE and is encoded afterwards so the final file is all numbers.

* **Source:** Canvas P5 and P6; D4 card; scikit-learn OneHotEncoder documentation; category counts in notebooks/02_eda_train.ipynb

* **Evidence** (added at H3: notebook name and cell number, chart, report file):
  `notebooks/03_preprocess_before_after.ipynb` cells 29 to 32 (columns, group sums, chart,
  head); `notebooks/04_smote_balance.ipynb` cells 31, 32 (work_type one hot chart), 39;
  validator reports `docs/reports/data-validator/H3_20261004_1618.md` §2, §5 and
  `docs/reports/data-validator/H3_20261004_1704.md` §3

* **What I will watch for:** More columns, and each group always adds up to 1, which matters for some linear models in the Final. Train and test must end up with the same column names in the same order.

* **Value set in `src/stroke_prep/config.py`:** `ONEHOT_DROP_FIRST = False`

* **ADR:** `docs/adr/0004-d4-full-one-hot-encoding.md`

* **Signed:** Joseph Clay, 10/04/2026 3:30 PM (CT)

## Review at H3 (Joseph)

* [x] Keep as decided   [ ] Amend (new option, and why, in my words):
* **What in the H3 evidence I looked at:** nb03 cells 29, 30: 11 to 18 columns, and every one hot group sums to 1 on 3576 rows.
* **Signed:** Joseph Clay, 10/04/2026 6:40PM (CT)
