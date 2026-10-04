# Midterm acceptance criteria (source of truth)

Quoted exactly as supplied from Canvas. IDs are for cross reference only. Nothing in the
annotation section is a Canvas requirement.

## Guidelines

* **GL1:** "choose Kaggle dataset >=2000 rows"
* **GL2:** "perform cleanup using Modules 4 and 5 guidelines"
* **GL3:** "Preprocessing exercises (P1 to P7)"
* **GL4:** "NEVER EVER change the dataset manually. If you do this you have failed the exam. All changes to be done via Python code in Jupyter lab."
* **GL5:** "Use Matplotlib to plot data distributions and show before and after preprocessing (example: balancing)"
* **GL6:** "Print sample data as it gets processed"
* **GL7:** "Build a Jupyter notebook to show dataset before and after cleanup"
* **GL8:** "Discuss how you would use this dataset to solve an ML problem"
* **GL9:** "Finals will implement models on this prepared dataset"

## Preprocessing exercises

* **P1:** "Filling NaN and Null with appropriate values"
* **P2:** "Scaling"
* **P3:** "Normalization"
* **P4:** "Class Balancing the dataset"
* **P5:** "One hot encoding"
* **P6:** "Encoding categorical to numbers"
* **P7:** "Feature engineering"

## Oct 3 submission items

(extended to Sun Oct 4, 11:59 PM CT)

* **S0:** "Sep 20 dataset for approval"
* **S1:** "Upload document showing URL of original dataset"
* **S2:** "Upload pdf describing dataset and proposal, not more than a page"
* **S3:** "In jupyter notebook use python to split dataset: training 70%, testing 30%; Python loads training data into memory; do not split manually or in excel"
* **S4:** "EDA performed only on training data; testing data untouched"
* **S5:** "Jupyter notebook demonstrating before and after data processing"
* **S6:** "Upload the .ipynb"
* **S7:** "Upload detailed proposal (reflection journal) of what you accomplished; each team member talks about contribution in the contribution journal"
* **S8:** "Upload final clean dataset"
* **S9:** "Create GitHub repo, upload all, give URL in Canvas"
* **S10:** "DO NOT change original dataset manually"

## Rubric

* **R1:** "Project 70: Working Program 60"
* **R2:** "Project 70: Documentation 10"
* **R3:** "Reflection 10"
* **R4:** "Individual contribution: no entry minus 20, no participation minus 100"

## Annotation (not Canvas text)

* **Instructor guidance (Prof Rao):** the dataset was approved on the condition that `work_type`
  is balanced. In class on Oct 1, 2026, Prof Rao said to balance `work_type` with SMOTE.
  Cite it as "Prof Rao, in class, Oct 1, 2026".
* **Every other method choice is Joseph's** and is recorded on a decision card in
  `docs/decisions/` (D1 to D8) and in an ADR.
* Deliverable file names used by the README and `scripts/check_deliverables.py` are a naming
  convention, not a requirement from Canvas.
* Checkpoints H1 to H4, the subagent reports, tests, hooks, CI, ADRs and RCA notes are
  **[Engineering extra, not graded]**. They support Documentation (R2).
