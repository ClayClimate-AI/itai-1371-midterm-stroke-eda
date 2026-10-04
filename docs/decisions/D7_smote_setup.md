# D7: How do I set up SMOTE?

**Decided at:** checkpoint H1, with all other cards in one sitting. **Reviewed at:** H3. **Feeds:** ADR 0007.
**Canvas P4:** "Class Balancing the dataset"
**Prof Rao (in class, Oct 1, 2026):** balance work_type with SMOTE. Train only; the test set is
never balanced.

## The question

Prof Rao fixed the method family (SMOTE) and the column to balance (`work_type`). You decide the
settings, and you record each one.

## Settings to decide

| Setting | Options | Pros and cons |
|---|---|---|
| Variant | `SMOTE` (needs all numeric input) or a variant such as `SMOTENC` (see D6) | Plain SMOTE is the basic method; a variant handles categories directly but must fit Prof Rao's guidance |
| `y` | `work_type` (Prof Rao's guidance) | Fixed |
| The target `stroke` | (a) ride along in X like any other column, or (b) set aside and attach afterwards | (a) synthetic rows get a stroke value made the same way as every other column, which then needs repair (D8); (b) you must decide where a synthetic row's stroke value comes from |
| `k_neighbors` | the library default or another value | Must be smaller than the size of the smallest work_type group in train (read it from your own counts); a larger k draws new points from a wider neighborhood, a smaller k keeps them closer to existing rows |
| `sampling_strategy` | `"auto"` (every smaller group grows to the size of the largest) or a dictionary of target counts | "auto" is simplest to explain; a dictionary gives control but every number in it needs a reason |
| `random_state` | any fixed integer | Makes the run repeatable; record it and do not change it after seeing results |
| Column types going in | as loaded, or cast to float first | Check what dtype comes OUT for each column and whether the values make sense; print a few synthetic rows |

## How to test the choice on your own data (train only)

You decide at H1 from the options, your course material and the dataset documentation. After
the split, the agents run these checks on train and put the raw outputs (no interpretation) in
your H3 summary. At H3 you keep or amend the decision.

1. Print the work_type counts in train before SMOTE (cell output). The smallest count limits k.
2. Run SMOTE once with your settings. Print the counts after, the number of rows added, and a
   few synthetic rows.
3. Check the real rows came back unchanged, and, if you chose a marking column in D8, that the
   new rows are marked 1 in it.
4. Print the dtypes before and after for every column and compare a few values.
5. If you consider two values of k, compare the spread of synthetic rows against real rows for
   both, and describe what you see.

## My decision (Joseph fills this in at H1, in his own words)

* **Option I chose:** Plain `SMOTE`. y = work_type. stroke rides along in X (option a). `k_neighbors = 5` (library default). `sampling_strategy = "auto"`. `random_state = 33`.

* **Why, in my words:**
  Prof Rao fixed SMOTE and work_type, and plain SMOTE is the basic method, so there's no variant to justify. My smallest work_type group in train is Never_worked with 13 rows. k has to be below that, so the default of 5 works. "auto" grows every smaller group to the size of the largest group (Private), which is the simplest to explain. random_state 33 matches my split seed so the run repeats, and I won't change it after seeing results. stroke rides along in X like any other 0/1 column and gets repaired in D8.

* **Source:** Prof Rao in class, Oct 1, 2026; Canvas P4; D7 card; imbalanced-learn SMOTE documentation; work_type counts in notebooks/02_eda_train.ipynb

* **Evidence** (added at H3: notebook name and cell number, chart, report file):

* **What I will watch for:** Never_worked grows from 13 rows to about 2,040, so about 99% of that group will be synthetic, made from only 13 real rows. I'll compare its synthetic rows against the real ones. Synthetic stroke values come out blended and must be rounded back to 0/1. The real rows must come back unchanged.

* **Value set in `src/stroke_prep/config.py`:** `SMOTE_VARIANT = "SMOTE"`, `SMOTE_K_NEIGHBORS = 5`, `SMOTE_SAMPLING_STRATEGY = "auto"`, `SMOTE_RANDOM_STATE = 33`

* **ADR:** `docs/adr/____-________.md`

* **Signed:** Joseph Clay, 10/04/2026 3:33PM (CT)

## Review at H3 (Joseph)

* [ ] Keep as decided   [ ] Amend (new option, and why, in my words):
* **What in the H3 evidence I looked at:**
* **Signed:** Joseph Clay, date and time (CT):
