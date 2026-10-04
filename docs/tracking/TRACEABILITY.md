# Traceability matrix

The Canvas column is quoted verbatim from `docs/specs/midterm_acceptance.md`. Checkpoint, file and check
columns are the plan. **The evidence columns are blank: Joseph fills them** with the cell number,
commit hash and status, only after the cell has run.

| ID | Canvas (verbatim) | Checkpoint | Where (file) | Test or check | Evidence: cell or output | Evidence: commit | Status |
|---|---|---|---|---|---|---|---|
| GL1 | "choose Kaggle dataset >=2000 rows" | H1 | `docs/dataset_url.md`, raw CSV | test_raw_meets_canvas_row_minimum | | | |
| GL2 | "perform cleanup using Modules 4 and 5 guidelines" | H2 to H3 | notebooks 02 and 03, decision cards D2 to D6 | validator reports | | | |
| GL3 | "Preprocessing exercises (P1 to P7)" | H3 | see P rows | see P rows | | | |
| GL4 | "NEVER EVER change the dataset manually. If you do this you have failed the exam. All changes to be done via Python code in Jupyter lab." | every checkpoint | `scripts/check_raw_hash.py`, `data/raw/SHA256SUMS` | test_raw_file_hash_unchanged, test_no_notebook_writes_into_data_raw | | | |
| GL5 | "Use Matplotlib to plot data distributions and show before and after preprocessing (example: balancing)" | H2 to H3 | notebooks 02, 03, 04 (chart outputs) | notebook-runner report | | | |
| GL6 | "Print sample data as it gets processed" | H2 to H3 | `head()` outputs in notebooks 01 to 04 | validator report | | | |
| GL7 | "Build a Jupyter notebook to show dataset before and after cleanup" | H3 | `notebooks/03_preprocess_before_after.ipynb` | notebook-runner report | | | |
| GL8 | "Discuss how you would use this dataset to solve an ML problem" | H3, H4 | notebook 04 last cell, proposal | tutor-reviewer review | | | |
| GL9 | "Finals will implement models on this prepared dataset" | H3 | `data/processed/` | test_invariants_final.py | | | |
| P1 | "Filling NaN and Null with appropriate values" | H3 | notebook 03, card D3 | test_final_has_no_missing_values | | | |
| P2 | "Scaling" | H3 | notebook 03, card D5 | test_transform_is_row_by_row | | | |
| P3 | "Normalization" | H3 | notebook 03, card D5 | validator report | | | |
| P4 | "Class Balancing the dataset" | H3 | notebook 04, cards D6 to D8 | test_balance_keeps_real_rows_unchanged, test_synthetic_flag_reconciles | | | |
| P5 | "One hot encoding" | H3 | notebooks 03 and 04, card D4 | test_each_onehot_group_is_valid | | | |
| P6 | "Encoding categorical to numbers" | H3 | notebooks 03 and 04, card D4 | test_final_is_all_numeric | | | |
| P7 | "Feature engineering" | H3 | notebook 03, card D3 | validator report | | | |
| S0 | "Sep 20 dataset for approval" | done | Canvas (submitted Sep 17, 2026) | n/a | | | |
| S1 | "Upload document showing URL of original dataset" | H1 | `docs/dataset_url.md` | check_deliverables | | | |
| S2 | "Upload pdf describing dataset and proposal, not more than a page" | H4 | `docs/MT_JosephClay_ITAI1371_Proposal.pdf` | check_deliverables, one page | | | |
| S3 | "In jupyter notebook use python to split dataset: training 70%, testing 30%; Python loads training data into memory; do not split manually or in excel" | H2 | `notebooks/01_load_split.ipynb`, card D1 | test_invariants_split.py | | | |
| S4 | "EDA performed only on training data; testing data untouched" | H2 | `notebooks/02_eda_train.ipynb` | test_eda_notebook_reads_train_only | | | |
| S5 | "Jupyter notebook demonstrating before and after data processing" | H3 | notebooks 03 and 04 | notebook-runner report | | | |
| S6 | "Upload the .ipynb" | H4 | `notebooks/*.ipynb` (outputs kept) | check_deliverables, test_committed_notebooks_were_run_top_to_bottom | | | |
| S7 | "Upload detailed proposal (reflection journal) of what you accomplished; each team member talks about contribution in the contribution journal" | H4 | `docs/MTJournal_R_JosephClay_ITAI1371.pdf`, `docs/MTJournal_C_JosephClay_ITAI1371.pdf` | check_deliverables | | | |
| S8 | "Upload final clean dataset" | H3 | `data/processed/stroke_clean_final.csv` | test_invariants_final.py | | | |
| S9 | "Create GitHub repo, upload all, give URL in Canvas" | H1, H4 | GitHub repo | repo-auditor full report, CI | | | |
| S10 | "DO NOT change original dataset manually" | every checkpoint | same as GL4 | test_raw_file_hash_unchanged | | | |
| R1 | "Project 70: Working Program 60" | H2 to H3 | notebooks and processed files | repo-auditor full report | | | |
| R2 | "Project 70: Documentation 10" | H4 | README, markdown cells, decision cards, ADRs | tutor-reviewer review | | | |
| R3 | "Reflection 10" | H4 | `docs/MTJournal_R_JosephClay_ITAI1371.pdf` | check_deliverables | | | |
| R4 | "Individual contribution: no entry minus 20, no participation minus 100" | H4 | `docs/MTJournal_C_JosephClay_ITAI1371.pdf` | check_deliverables | | | |
