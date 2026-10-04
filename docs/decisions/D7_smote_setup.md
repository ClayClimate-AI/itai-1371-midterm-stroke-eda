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

* **Option I chose:**
* **Why, in my words:**
* **Source** (module or lecture, documentation page, or Prof Rao with date):
* **Evidence** (added at H3: notebook name and cell number, chart, report file):
* **What I will watch for** (a risk this choice brings):
* **Value set in `src/stroke_prep/config.py`** (slots `SMOTE_VARIANT`, `SMOTE_K_NEIGHBORS`, `SMOTE_SAMPLING_STRATEGY`, `SMOTE_RANDOM_STATE`; blank until you sign):
* **ADR:** `docs/adr/____-________.md`
* **Signed:** Joseph Clay, date and time (CT):

## Review at H3 (Joseph)

* [ ] Keep as decided   [ ] Amend (new option, and why, in my words):
* **What in the H3 evidence I looked at:**
* **Signed:** Joseph Clay, date and time (CT):
