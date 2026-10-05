# Reflection journal (Canvas item 7, Reflection 10 points)

> PROMPTS ONLY. Answer each one in your own words, using numbers from YOUR notebooks, and name
> the notebook and cell for every number. Then export to
> `docs/MTJournal_R_JosephClay_ITAI1371.pdf`. The tutor-reviewer may point out gaps or unclear
> sentences; it does not write answers. The data-validator recomputes every number you write.

**Canvas S7:** "Upload detailed proposal (reflection journal) of what you accomplished; each team member talks about contribution in the contribution journal"
**Canvas R3:** "Reflection 10"

## 1. What I accomplished
* List what you built, checkpoint by checkpoint. Which notebook or file shows each item?
  I took the raw stroke dataset (5110 rows, 12 columns) to a balanced, model ready train file
  (10200 x 23) and an untouched test file (1533 x 23). I got there through three signed checkpoints
  (H1 78e6825, H2 ea395d1, H3 a126aa1), eight signed decision cards, and eight ADRs, and I
  orchestrated the agents that built, ran and checked the work.

## 2. The data before processing
* Which data problems did your EDA show? Which chart or printed output showed each one?
  bmi was missing in 138 train rows (about 4%), and those rows were older, had higher glucose, and
  had far more strokes, so the gaps were not random (nb03 cell 19). One train row had gender Other.
  stroke is only 4.7% positive. Never_worked had just 13 train rows (nb02).
* Was there anything in the data you expected to find and did not? Describe it.
  I expected missing values in more columns, but only bmi had gaps. smoking_status "Unknown" acts
  like hidden missing data, but it isn't counted as missing, so I kept it as its own category.

## 3. My decisions
* Pick two decision cards. For each, which options did you weigh, what evidence from your train
  data did you look at, and why did you choose what you chose?
  D3, because the missing bmi rows were not random, and the bmi_missing flag keeps that signal
  after the median fill. D7, because Prof Rao asked us to balance on work_type, and Never_worked
  with 13 rows was the hardest group to grow honestly.
* Is there a decision you would make differently now? Explain.
  D7. Never_worked grew from 13 real rows to 2040, so 2027 rows are blends of the same 13 people.
  Next time I would try a smaller target for that group, or merge it with a close group, and
  compare that against plain SMOTE.

## 4. Balancing work_type with SMOTE
* What was Prof Rao's guidance, and how did you apply it?
  On Oct 1, 2026, Prof Rao told the class to balance on work_type instead of stroke. That set the
  target column for D7.
* Describe in your own words how SMOTE creates one new row.
  it picks a real row in a small group, finds its 5 nearest neighbors in the same group, and makes
  a new row at a random point on the line between them. That's why 0/1 and one hot values come out
  in between and need the D8 repair.
* Which settings did you choose (D7), and how did you check that they worked?
  every work_type group ended at 2040 (nb04 cell 9), 6624 rows were added, and the real rows came
  back unchanged (cell 13).

## 5. Before and after
* Compare the `work_type` counts before and after balancing. Describe what you see.
  before SMOTE, Private 2040, Self-employed 585, children 477, Govt_job 461, Never_worked 13.
  After, 2040 each (nb04 cell 9).
* Compare the target column before and after balancing, overall and within each `work_type`
  group. Describe what you see and what explains it.
  overall the stroke share fell from 0.0470 to 0.0305 (cell 23). Within groups (cell 25), Govt_job
  went 0.0542 to 0.0402, Self-employed 0.0752 to 0.0613, children 0.0042 to 0.0034, Private stayed
  0.0475, and Never_worked stayed 0. SMOTE balanced work_type, not stroke, and the repair rounded
  some blended stroke values down to 0, so stroke rates fell inside the groups that grew.
* Compare one numeric column before and after balancing. Describe what you see and why.
  age had a real mean of 43.17 and a synthetic mean of 31.77 (cell 30). Synthetic rows are younger
  because many come from the children and Never_worked groups.

## 6. Checks on synthetic rows
* What did your repair step change (D8)? Give the counts your notebook printed.
  the repair fixed 334 hypertension, 223 heart_disease, 194 stroke and 181 bmi_missing values that
  were not 0 or 1, plus 658 gender, 123 ever_married, 735 Residence_type and 1056 smoking_status
  one hot rows (cell 19).
* What did your numeric check find?
  0 synthetic values fell outside their work_type's real range for age, glucose and bmi (cell 28),
  and the histograms kept the same shape.
* Did you keep a marking column for synthetic rows (D8)? How could the Final use that choice?
  it marks the 6624 new rows, so a model can be trained or checked with and without them.

## 7. Leakage and the test set
* Name every value or object your pipeline learned from data. Where was each one learned, and
  how did you confirm it was learned from train only?
  the bmi median 28.1, the one hot categories, and the scaler's mean and std (nb03 cell 14).
  Nothing was learned from test.
* What happened to the test set, step by step?
  test was only transformed with the train fitted objects, never balanced, and has the same 23
  columns as the final train file (nb04 cells 40 to 44).

## 8. Mistakes and fixes
* Describe one thing that failed, what caused it, and how you fixed it (link your RCA note).
  on the first run, the D8 step printed 0 values to repair, which was wrong. SMOTE had returned
  whole numbers, so values like 0.76 were cut to 0 before the repair could round them. I cast the
  columns to float before SMOTE. RCA: docs/rca/0001-smote-int-truncation.md

## 9. Working with Claude and the subagents
* How did you check each cell before accepting it? Give one example.
  the data-validator rechecked every number I wrote against the cell outputs, the work-verifier
  compared each change to my signed cards, and the tests ran on every commit.
* Did a validator or auditor report change anything you had written or done? Describe it.
  the H2 validator report led to 3 fixes in notebook 02 (c17a968), and escalation E3 led to the
  float line on the D7 card (0b94ef8).

## 10. Next steps for the Final
* Which ML problem will the Final solve with this dataset, and which metric fits it? Why?
  a classifier that flags patients at higher stroke risk. I'd train on the train file and judge
  only on the untouched 1533 row test file, using recall on stroke cases, because missing a stroke
  is worse than a false alarm.
* What open questions from this midterm will you take into the Final?
  Do the synthetic rows help or hurt a stroke model? Should Never_worked be merged with another
  group? Is smoking "Unknown" hiding a pattern?
