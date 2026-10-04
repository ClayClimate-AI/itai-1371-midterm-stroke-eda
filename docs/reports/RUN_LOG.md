# Run log

Only the repo-auditor writes this file. It appends one entry per change or escalation found in
the other agents' reports (and its own). Newest at the bottom. Joseph skims this at each
checkpoint. Earlier entries are never deleted or rewritten.

```text
#<n>  <date time CT>  <agent>  since <checkpoint>
Type:    BUILD (builder) | FIX (mechanical, notebook-runner) | RERUN | ESCALATION
What:    <one line>
Why:     <error text or check that failed>
Files:   <paths>
Change:  <before -> after, or "none, waiting for Joseph">
Rule:    <for ESCALATION: decision not recorded | unexplained mismatch | data handling change | interpretation text>
Commit:  <hash or "uncommitted">
```

(entries start below)

```text
#0  2026-10-04 11:01 CT  builder  since scaffold (89193d0)
Type:    BUILD
What:    none: builder built nothing at H1 (no notebooks, pipeline.py unchanged); ran pytest only (16 passed, 49 skipped, 0 failed)
Why:     H1 has no build step; D2 to D8 deferred to H2 by Joseph
Files:   none
Change:  none
Rule:    n/a
Commit:  n/a
```

```text
#1  2026-10-04 10:50 CT  data-validator  since scaffold (89193d0)
Type:    RERUN (check run, no code or data changed)
What:    H1 checks: raw hash vs config and SHA256SUMS, raw shape and columns, D1 slots vs D1 card, no split or final files; all PASS
Why:     H1 data-validator report
Files:   docs/reports/data-validator/H1_20261004_1050.md
Change:  none
Rule:    n/a (no escalations)
Commit:  committed with the H1 reports (hash in H1_SUMMARY.md reply and git log)
```

```text
#2  2026-10-04 10:59 CT  work-verifier  since scaffold (89193d0)
Type:    RERUN (check run in clone scratch/clones/work-verifier_H1_20261004_1059)
What:    checked 4 changed files and 2 commits since 89193d0 against lanes, decisions and tests; 12 OK, 0 FLAG
Why:     H1 work-verifier report
Files:   docs/reports/work-verifier/H1_20261004_1059.md
Change:  none
Rule:    n/a (no flags)
Commit:  committed with the H1 reports
```

```text
#3  2026-10-04 11:01 CT  repo-auditor  since scaffold (89193d0)
Type:    RERUN (FULL audit in clone scratch/clones/repo-auditor_H1_20261004_1101)
What:    new venv install OK, setup_gate OK, raw hash OK, pytest 16 passed 49 skipped, ruff clean, no secrets or junk, A2.5 D1 before notebook 01 holds; check_deliverables 9 MISSING (not yet built)
Why:     H1 full reproducibility audit
Files:   docs/reports/repo-auditor/H1_20261004_1101.md, docs/reports/RUN_LOG.md, docs/reports/H1_SUMMARY.md
Change:  none to code or data; .gitignore unchanged
Rule:    n/a (no escalations)
Commit:  docs(agent): H1 reports, run log and summary  [H1]
```

```text
#4  2026-10-04 12:39 CT  builder  since H1 (78e6825, tag H1-signed)
Type:    BUILD
What:    src/stroke_prep/pipeline.py: new bodies for load_raw, split_train_test, save_csv; new helper missing_tokens; fit_prep, transform, balance, repair_after_balance still TODO shells
Why:     card D1 (option A), spec nb01
Files:   src/stroke_prep/pipeline.py
Change:  TODO NotImplementedError bodies -> implementations (git diff: 40 insertions, 3 deletions); signatures and docstrings unchanged (work-verifier #3, #4)
Rule:    n/a
Commit:  feat(agent): build and run notebooks 01 and 02, H2 reports  [H2]
```

```text
#5  2026-10-04 12:39 CT  builder  since H1 (78e6825)
Type:    BUILD
What:    notebooks/01_load_split.ipynb created, 31 cells (17 code, 14 markdown, 5 placeholders [Joseph writes here at H2])
Why:     card D1, spec nb01
Files:   notebooks/01_load_split.ipynb
Change:  new file
Rule:    n/a
Commit:  feat(agent): build and run notebooks 01 and 02, H2 reports  [H2]
```

```text
#6  2026-10-04 12:39 CT  builder  since H1 (78e6825)
Type:    BUILD
What:    notebooks/02_eda_train.ipynb created, 50 cells (24 code, 26 markdown, 14 chart placeholders + findings cell); reads train only; 14 charts
Why:     spec nb02; Joseph's chart choice Q4 b (bar charts for text and 0/1 columns, histograms for number columns, stroke and work_type share bars); missing-values bar per spec nb02 item 3
Files:   notebooks/02_eda_train.ipynb
Change:  new file
Rule:    n/a
Commit:  feat(agent): build and run notebooks 01 and 02, H2 reports  [H2]
```

```text
#7  2026-10-04 12:39 CT  builder  since H1 (78e6825)
Type:    BUILD (note)
What:    builder read ~/Library/Jupyter/kernels/stroke-eda/kernel.json (outside the repo) for the kernel display name; both notebooks' metadata.kernelspec = stroke-eda
Why:     builder's own disclosure; work-verifier FLAG 1 (house rule 2)
Files:   none in the repo beyond the kernelspec metadata in both notebooks
Change:  none, waiting for Joseph (listed under "Waiting for you" in H2_SUMMARY.md)
Rule:    n/a (verifier FLAG, not an agent escalation)
Commit:  n/a
```

```text
#8  2026-10-04 12:19 CT  notebook-runner  since H1 (78e6825)
Type:    RERUN
What:    executed notebooks 01 and 02 in the working copy with the stroke-eda kernel; both PASS, 0 errors, counts 1..17 and 1..24; no mechanical fixes; notebook 01 wrote data/interim/train_raw.csv (229343 bytes) and test_raw.csv (98231 bytes)
Why:     H2 notebook-runner report
Files:   docs/reports/notebook-runner/H2_20261004_1219.md, notebooks/01_load_split.ipynb, notebooks/02_eda_train.ipynb, data/interim/train_raw.csv, data/interim/test_raw.csv (tracked by design per .gitignore note)
Change:  none to cell sources or pipeline.py; outputs saved; two split files written
Rule:    n/a (no escalations)
Commit:  feat(agent): build and run notebooks 01 and 02, H2 reports  [H2]
```

```text
#9  2026-10-04 12:31 CT  data-validator  since H1 (78e6825)
Type:    RERUN (check run, no code or data changed)
What:    split invariants, train-only check of notebook 02, card D1 vs notebook 01, raw outputs of D2 to D8 "how to test" steps on TRAIN only; all PASS; claims checked 0 (no Joseph prose yet)
Why:     H2 data-validator report
Files:   docs/reports/data-validator/H2_20261004_1231.md
Change:  none
Rule:    n/a (no escalations)
Commit:  feat(agent): build and run notebooks 01 and 02, H2 reports  [H2]
```

```text
#10  2026-10-04 12:34 CT  work-verifier  since H1 (78e6825)
Type:    RERUN (check run in clone scratch/clones/work-verifier_H2_20261004_1234)
What:    checked 7 changed paths against specs, card D1, lanes and tests; 20 findings: 17 OK, 2 FLAG (#1 kernel.json read outside the repo; #2 nb01 prints test-part shares vs process note 4), 1 NOT VERIFIED (#7 runner changed no cell source)
Why:     H2 work-verifier report
Files:   docs/reports/work-verifier/H2_20261004_1234.md
Change:  none
Rule:    n/a (FLAGs go to Joseph by design)
Commit:  feat(agent): build and run notebooks 01 and 02, H2 reports  [H2]
```

```text
#11  2026-10-04 12:39 CT  repo-auditor  since H1 (78e6825)
Type:    RERUN (QUICK audit; notebook rerun in clone scratch/clones/repo-auditor_H2_20261004_1239)
What:    raw hash OK; pytest 31 passed 34 skipped; ruff clean (src tests scripts; src notebooks); counts 1..17 and 1..24, 0 errors; clone rerun compare_outputs 0 of 17 and 0 of 24 differ; split file hashes identical; check_deliverables 7 MISSING (not yet built or written); no secrets or junk; A2.5 D1 before notebook 01 holds
Why:     H2 quick reproducibility audit
Files:   docs/reports/repo-auditor/H2_20261004_1239.md, docs/reports/RUN_LOG.md, docs/reports/H2_SUMMARY.md
Change:  none to code or data; .gitignore unchanged
Rule:    n/a (no escalations)
Commit:  feat(agent): build and run notebooks 01 and 02, H2 reports  [H2]
```

```text
#12  2026-10-04 14:40 CT  notebook-runner  since H1 (78e6825), logged at H3 on Joseph's request (verifier 1622 #2)
Type:    FIX (mechanical)
What:    notebook 01 execution count restored by a full rerun; no cell source change
Why:     H2 notebook-runner report
Files:   docs/reports/notebook-runner/H2_20261004_1440.md, notebooks/01_load_split.ipynb
Change:  execution counts restored by rerun; sources unchanged
Rule:    n/a (no escalations)
Commit:  1aed277 (committed by Joseph)
```

```text
#13  2026-10-04 14:47 CT  data-validator  since H1 (78e6825), logged at H3 on Joseph's request (verifier 1622 #2)
Type:    RERUN (check run, no code or data changed)
What:    claims check on Joseph's H2 prose: 84 claims, 71 MATCH, 0 MISMATCH
Why:     H2 data-validator report
Files:   docs/reports/data-validator/H2_20261004_1447.md
Change:  none
Rule:    n/a (no escalations)
Commit:  1aed277 (committed by Joseph)
```

```text
#14  2026-10-04 16:09 CT  builder  since H2 (ea395d1, tag H2-signed)
Type:    BUILD
What:    src/stroke_prep/pipeline.py: bodies for fit_prep, transform, balance, repair_after_balance; new helpers drop_rare_rows, encode_balance_col, to_real_units, binary_cols, onehot_cols, validity_counts; new constants DROP_COLUMNS, STATE_PATH
Why:     cards D2 to D8 (signed in ccc2dc4); constants' location in pipeline.py accepted by Joseph (verifier 1622 #8, #9; 1711 #9)
Files:   src/stroke_prep/pipeline.py
Change:  TODO NotImplementedError bodies -> implementations (git diff: 139 insertions, 4 deletions)
Rule:    n/a
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#15  2026-10-04 16:09 CT  builder  since H2 (ea395d1)
Type:    BUILD
What:    notebooks/03_preprocess_before_after.ipynb created, 44 cells (28 code, 6 placeholders [Joseph writes here at H3])
Why:     cards D2 to D6, spec nb03
Files:   notebooks/03_preprocess_before_after.ipynb
Change:  new file
Rule:    n/a
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#16  2026-10-04 16:10 CT  builder  since H2 (ea395d1)
Type:    BUILD
What:    notebooks/04_smote_balance.ipynb created, 42 cells at first (28 code, 4 placeholders)
Why:     cards D6 to D8, spec nb04
Files:   notebooks/04_smote_balance.ipynb
Change:  new file
Rule:    n/a
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#17  2026-10-04 16:13 CT  builder  since H2 (ea395d1)
Type:    BUILD (change to its own uncommitted balance())
What:    SMOTE runs on X.astype(float) instead of the columns as loaded, after the first run (runner 1610)
Why:     builder change; no escalation at the time
Files:   src/stroke_prep/pipeline.py (balance, l.210)
Change:  fit_resample(X, y) -> fit_resample(X.astype(float), y); nb04 rerun by runner 1614
Rule:    see #18
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#18  2026-10-04 16:22 CT  builder / work-verifier  since H2 (ea395d1)
Type:    ESCALATION E3 (resolved)
What:    float cast in balance() not on the signed D7 card ("Column types going in" was a setting to decide); raised by the work-verifier (1622 #10) and the builder
Why:     D7 option line did not name the column types going in
Files:   src/stroke_prep/pipeline.py; docs/decisions/D7_smote_setup.md
Change:  none by agents; Joseph answered "D7 dtype b" and recorded "Column types going in: cast to float first" on the D7 card (0b94ef8); code matches (verifier 1711 #10, validator 1704 §2)
Rule:    decision not recorded / data handling change
Commit:  card: 0b94ef8 (Joseph); code: feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#19  2026-10-04 16:48 CT  builder  since H2 (ea395d1)
Type:    BUILD (on Joseph's instruction)
What:    nb04 new code cell (work_type label counts vs one hot sums, table + Matplotlib chart) plus empty placeholder (verifier 1622 #20); nb04 markdown sentence turned into heading "### D7 how to test step 5: one k value on the signed card" (verifier 1622 #6, edit to the builder's own uncommitted cell)
Why:     process note 8; house rule 6
Files:   notebooks/04_smote_balance.ipynb (cells 15, 31, 32); now 44 cells
Change:  42 -> 44 cells; cell 15 sentence -> heading
Rule:    n/a
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#20  2026-10-04 16:10 CT  notebook-runner  since H2 (ea395d1)
Type:    RERUN
What:    executed nb03 and nb04 in the working copy (stroke-eda); both PASS, counts 1..28 and 1..28; no mechanical fixes; wrote the 4 data files
Why:     H3 notebook-runner report
Files:   docs/reports/notebook-runner/H3_20261004_1610.md, notebooks/03_preprocess_before_after.ipynb, notebooks/04_smote_balance.ipynb, data/interim/train_prepared.csv, data/interim/prep_state.joblib, data/processed/stroke_clean_final.csv, data/processed/stroke_test_transformed.csv
Change:  none to cell sources or pipeline.py; outputs saved
Rule:    n/a (no escalations)
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#21  2026-10-04 16:14 CT  notebook-runner  since H2 (ea395d1)
Type:    RERUN
What:    nb04 rerun after #17; PASS, counts 1..28; 6 of 28 code cells differ from the 16:10 copy; stroke_clean_final.csv changed, other 3 data files unchanged
Why:     H3 notebook-runner report
Files:   docs/reports/notebook-runner/H3_20261004_1614.md, notebooks/04_smote_balance.ipynb, data/processed/stroke_clean_final.csv, data/processed/stroke_test_transformed.csv
Change:  none to cell sources or pipeline.py
Rule:    n/a (no escalations)
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#22  2026-10-04 16:48 CT  notebook-runner  since H2 (ea395d1)
Type:    RERUN
What:    nb04 rerun after #19; PASS, 44 cells, counts 1..29; only the new cell differs from the backup; 4 data files unchanged (SHA-256 equal to 16:14)
Why:     H3 notebook-runner report
Files:   docs/reports/notebook-runner/H3_20261004_1648.md, notebooks/04_smote_balance.ipynb
Change:  none to cell sources or pipeline.py
Rule:    n/a (no escalations)
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#23  2026-10-04 16:18 CT  data-validator  since H2 (ea395d1)
Type:    RERUN (check run, no code or data changed)
What:    full H3: card vs notebook D2..D8 7 MATCH; how to test 30 steps (27 MATCH, 2 NOT RUN, 1 N/A); leakage and integrity 24 PASS; claims 20 (17 MATCH, 0 MISMATCH, 3 NOT CHECKABLE)
Why:     H3 data-validator report
Files:   docs/reports/data-validator/H3_20261004_1618.md
Change:  none
Rule:    n/a (no escalations)
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#24  2026-10-04 17:04 CT  data-validator  since H2 (ea395d1)
Type:    RERUN (delta check)
What:    4 data file hashes unchanged vs 16:18; D7 "Column types going in" vs code MATCH; new nb04 cell recomputed MATCH; 1 claim MATCH
Why:     H3 data-validator report
Files:   docs/reports/data-validator/H3_20261004_1704.md
Change:  none
Rule:    n/a (no escalations)
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#25  2026-10-04 16:22 CT  work-verifier  since H2 (ea395d1)
Type:    RERUN (check run in its clone)
What:    first H3 review: 7 FLAG (#2, #3, #6, #8, #9, #10, #20)
Why:     H3 work-verifier report
Files:   docs/reports/work-verifier/H3_20261004_1622.md
Change:  none
Rule:    n/a (FLAGs go to Joseph by design; #10 became E3, #18)
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#26  2026-10-04 17:11 CT  work-verifier  since H2 (ea395d1)
Type:    RERUN (check run in clone scratch/clones/work-verifier_H3_20261004_1711)
What:    final H3 review: 17 findings, 16 OK, 1 open FLAG (#2: RUN_LOG missing entries; closed by #12 to #27)
Why:     H3 work-verifier report
Files:   docs/reports/work-verifier/H3_20261004_1711.md
Change:  none
Rule:    n/a
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```

```text
#27  2026-10-04 17:16 CT  repo-auditor  since H2 (ea395d1)
Type:    RERUN (QUICK audit; nb03 and nb04 rerun in clone scratch/clones/repo-auditor_H3_20261004_1716)
What:    raw hash OK; pytest 64 passed 1 skipped; ruff clean (src notebooks; src tests scripts); counts gap free in all 4 notebooks, 0 errors; clone rerun nb03 1 of 28 differ (stdout chunking only, text identical), nb04 0 of 29; 4 data file hashes identical; check_deliverables 3 MISSING (H4 PDFs); no secrets or junk; A2.5 D2 to D8 before notebooks 03 and 04 holds
Why:     H3 quick reproducibility audit
Files:   docs/reports/repo-auditor/H3_20261004_1716.md, docs/reports/RUN_LOG.md, docs/reports/H3_SUMMARY.md
Change:  none to code or data; .gitignore unchanged
Rule:    n/a (no escalations)
Commit:  feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]
```
