# RCA 0001: SMOTE returned whole numbers, hiding values to repair

> Engineering extra, not graded. Write one when a cell, test or validator check fails for a
> reason you did not expect. Your words.

* **Date:** Oct 04, 2026
* **Checkpoint:** H3
* **Notebook / cell, test or report:** nb04 cell 18; work-verifier H3_20261004_1622 #10
* **Symptom:** the first run printed the count of 0/1 values not 0 or 1 as 0, 0, 0, 0, which can't
  be right after SMOTE blends rows.
* **Cause:** the columns went into SMOTE as integers, so SMOTE returned int64. Every blended value
  was cut down (trunc), for example 0.76 became 0 (runner H3_1614, validator H3_1704, all 10200
  rows).
* **Fix:** cast the columns to float before SMOTE. Card line in 0b94ef8, code X.astype(float) in
  a7ddbbc.
* **Why this fix:** float keeps SMOTE's blended values, so the D8 repair rounds them at 0.5 and
  prints how many it changed. Cutting values silently would hide the repair and bias every 0/1
  column toward 0.
* **How it is prevented next time:** nb04 cell 18 prints the D8 step 1 counts. A count of 0 right
  after SMOTE is now treated as a warning sign. No test was added.
