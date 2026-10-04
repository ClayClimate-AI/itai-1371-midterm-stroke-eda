# ADR 0008: Repair, numeric check and final file format (D8)

> Drafted by the builder agent from Joseph's signed card.
> Every reason below is quoted from `docs/decisions/D8_after_smote.md`. Every result is quoted from the
> printed outputs of `notebooks/04_smote_balance.ipynb`. Nothing else was added.

* **Status:** Accepted
* **Date:** Oct 04, 2026
* **Checkpoint:** H2
* **Decision card:** `docs/decisions/D8_after_smote.md`
* **Canvas line this supports:** "Upload final clean dataset"

## Context
The card asks how to make synthetic rows valid, how to check their numbers, and what the final file holds.

Notebook outputs that show it:
* `notebooks/04_smote_balance.ipynb` cell 18, In[12]: 0/1 values not 0 or 1 `{'hypertension': 334, 'heart_disease': 223, 'stroke': 194, 'bmi_missing': 181}`; one hot rows breaking the rule `{'gender': 658, 'ever_married': 123, 'Residence_type': 735, 'smoking_status': 1056}`

## Options considered
From the D8 card, repair:
* A. Round 0/1 columns at 0.5; argmax for each one hot group
* B. Use a SMOTE variant that never creates in between category values
* C. Drop synthetic rows that break a rule

From the D8 card, numeric check:
* A. Range check in real units
* B. Compare distributions of real and synthetic rows
* C. Both

From the D8 card, final file: numeric columns scaled or converted back to real units; marking column A (add `is_synthetic`) or B (no marking column).

## Decision
Repair A, numeric check C, numbers stay scaled, `is_synthetic` added (`REPAIR_RULE = "A"`, `NUMERIC_CHECK = "C"`, `FINAL_NUMERIC_UNITS = "scaled"`, `FLAG_SYNTHETIC = True`), signed by Joseph Clay on 10/04/2026 at 3:34 PM (CT).

Joseph's reasoning, quoted from the card:

> SMOTE blends numbers, so a synthetic row can come out "0.4 hypertensive" or with two half ticks in one group. No real patient looks like that. Rounding and argmax make every row valid, and I print how many values changed so the repair isn't hidden. For the numbers, the range check gives a clear pass or fail (each value inside its work_type's real min and max), and the histograms show whether the shape looks real, so I do both. I keep the numbers scaled so the file is ready for the models in the Final (Canvas GL9), and the train fitted scaler can convert them back anytime. `is_synthetic` lets the Final train or evaluate with or without the synthetic rows. Test is transformed with train fitted objects only, never balanced, and has the same columns.

Source, quoted from the card: "Canvas S8 and GL9; D8 card; D7 SMOTE setup"

## Consequences
* Good: cell 20, In[14]: every count is 0 after repair. Cell 26, In[17]: `synthetic values outside their work_type's real range: {'age': 0, 'avg_glucose_level': 0, 'bmi': 0}`. Cell 34, In[22]: final `10200` rows, `23` columns.
* Bad or risk, quoted from the card: "Repair changes generated values, so the change counts must be printed. The range check needs real units, so values are converted with `inverse_transform` first. `is_synthetic` isn't a patient measurement, so it has to be dropped or handled before modeling." Change counts are printed in cell 19, In[13].
* Follow up: the card's "Review at H3" block is still for Joseph to complete.

## Evidence
* Notebook and cell: `notebooks/04_smote_balance.ipynb` cells 18 to 21 (repair counts and chart), 23 (0/1 shares), 26 to 28 (numeric check), 31 to 36 (final file), 38 to 42 (test file)
* Validator report: `docs/reports/data-validator/H3_20261004_1618.md` §2 (D8 steps), §4 (reconciliation), §5 (integrity)
* Test: `tests/test_invariants_final.py::test_binary_columns_hold_only_0_and_1`, `tests/test_invariants_final.py::test_synthetic_flag_reconciles`, `tests/test_invariants_final.py::test_final_is_all_numeric`
* Commit: `ccc2dc4` (card), `a7ddbbc` (notebook 04)
