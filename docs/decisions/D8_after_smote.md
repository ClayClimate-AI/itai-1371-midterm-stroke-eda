# D8: How do I repair and check synthetic rows, and what goes in the final file?

**Decided at:** checkpoint H1, with all other cards in one sitting. **Reviewed at:** H3. **Feeds:** ADR 0008.
**Canvas S8:** "Upload final clean dataset"
**Canvas GL9:** "Finals will implement models on this prepared dataset"

## The question

A synthetic row is made by blending numbers. A blended 0/1 column or one hot group can hold a
value that no real patient has. How do you make every synthetic row valid, how do you check the
blended numeric values are realistic, and what exactly goes into the final file?

## Why it matters (plain words)

A patient cannot be "a little bit" hypertensive, and a tick box row needs exactly one tick. If a
blended row breaks those rules, the Final would learn from rows that cannot exist.

## Options for repairing 0/1 and one hot columns

| Option | Pros | Cons |
|---|---|---|
| A. Round 0/1 columns at 0.5; set the largest value in each one hot group to 1 and the rest to 0 (argmax) | Every row becomes valid; easy to count what changed | Changes generated values; the change itself must be reported |
| B. Use a SMOTE variant that never creates in between category values (see D6) | No repair needed for categories | Only if the variant fits Prof Rao's guidance |
| C. Drop synthetic rows that break a rule | Keeps only clean generated rows | Groups may no longer be balanced; you must count how many were dropped |

Whatever you choose, COUNT what changed (values rounded, rows fixed or dropped) and print it.

## Options for checking numeric values

| Option | Pros | Cons |
|---|---|---|
| A. Range check in real units: each synthetic value lies inside the min and max of the real train rows of its own work_type | Simple, explainable | Does not check combinations of values |
| B. Compare distributions of real and synthetic rows (histograms per column) | Shows shape, not only limits | A judgment, not a pass or fail |
| C. Both | Most complete | More output to explain |

## What goes in the final file (decide each line)

* Numeric columns scaled, or converted back to real units?
* `work_type` as one hot columns (needed so the file is all numeric)?
* A 0/1 column that marks SMOTE rows (`FLAG_SYNTHETIC` in config; column name `is_synthetic`)?
  See the options below.
* Any row key (see D2)?
* The test set: transformed with the train fitted objects only, never balanced, same columns as
  the final file. This part is a rule, not a choice.

## Options for marking synthetic rows

| Option | Pros | Cons |
|---|---|---|
| A. Add a 0/1 column (1 for every row SMOTE made, 0 for every real row) | The Final can train or evaluate with or without synthetic rows; checks can count real rows exactly | One more column that is not a patient measurement; it must be dropped or handled before modeling |
| B. No marking column | The file holds only patient columns | Real and synthetic rows can no longer be told apart in the file; row checks must rely on counts saved elsewhere |

Set `FLAG_SYNTHETIC` in `src/stroke_prep/config.py` to True (A) or False (B). Tests that need
the flag skip unless it is True.

## How to test the choice on your own data

1. Before repair: count values that are not 0 or 1 in each 0/1 column, and rows whose one hot
   group does not sum to the rule in each group. Print the counts.
2. After repair: the same counts must be zero (the invariant tests check this).
3. Run your numeric check and print its result.
4. Run `python -m pytest -q` and ask the data-validator for a report.

## My decision (Joseph fills this in at H1, in his own words)

* **Option I chose:** Repair: A, round 0/1 columns at 0.5 and use argmax for each one hot group, then count the changes. Numeric check: C, both the range check and the distribution comparison. Final file: numbers stay scaled, work_type is one hot, no row key (id dropped in D2), and an `is_synthetic` column marks SMOTE rows (option A).

* **Why, in my words:**
  SMOTE blends numbers, so a synthetic row can come out "0.4 hypertensive" or with two half ticks in one group. No real patient looks like that. Rounding and argmax make every row valid, and I print how many values changed so the repair isn't hidden. For the numbers, the range check gives a clear pass or fail (each value inside its work_type's real min and max), and the histograms show whether the shape looks real, so I do both. I keep the numbers scaled so the file is ready for the models in the Final (Canvas GL9), and the train fitted scaler can convert them back anytime. `is_synthetic` lets the Final train or evaluate with or without the synthetic rows. Test is transformed with train fitted objects only, never balanced, and has the same columns.

* **Source:** Canvas S8 and GL9; D8 card; D7 SMOTE setup

* **Evidence** (added at H3: notebook name and cell number, chart, report file):
  `notebooks/04_smote_balance.ipynb` cells 18 to 21 (repair counts and chart), 23 (0/1 shares),
  26 to 28 (numeric check), 31 to 36 (final file), 38 to 42 (test file); validator report
  `docs/reports/data-validator/H3_20261004_1618.md` §2, §4, §5

* **What I will watch for:** Repair changes generated values, so the change counts must be printed. The range check needs real units, so values are converted with `inverse_transform` first. `is_synthetic` isn't a patient measurement, so it has to be dropped or handled before modeling.

* **Value set in `src/stroke_prep/config.py`:** `REPAIR_RULE = "A"`, `NUMERIC_CHECK = "C"`, `FINAL_NUMERIC_UNITS = "scaled"`, `FLAG_SYNTHETIC = True`

* **ADR:** `docs/adr/0008-d8-repair-check-and-final-file.md`

* **Signed:** Joseph Clay, 10/04/2026 3:34 PM (CT)
## Review at H3 (Joseph)

* [x] Keep as decided   [ ] Amend (new option, and why, in my words):
* **What in the H3 evidence I looked at:** nb04 cells 19, 26, 34: 0/1 fixes 334, 223, 194, 181; 0 out of range; final 10200 x 23.
* **Signed:** Joseph Clay, 10/04/2026 6:40PM (CT)
