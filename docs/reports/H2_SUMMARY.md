# H2 SUMMARY  (one page)  2026-10-04 12:39 CT  commit 78e6825 (H1-signed) + agent commit "feat(agent): build and run notebooks 01 and 02, H2 reports  [H2]"

Written by the repo-auditor from the reports listed below. Facts only, no interpretation.

## Status
* Tests: 31 passed / 34 skipped / 0 failed   Raw hash: OK   CI on this commit: not run by agents (`gh` denied; not pushed)
* Notebooks run clean: `01_load_split.ipynb` PASS, `02_eda_train.ipynb` PASS (runner in working copy; auditor and verifier reruns in clones, 0 code cells differ)
* Reports behind this page:
  * data-validator: `docs/reports/data-validator/H2_20261004_1231.md`
  * work-verifier: `docs/reports/work-verifier/H2_20261004_1234.md`
  * repo-auditor (quick): `docs/reports/repo-auditor/H2_20261004_1239.md`
  * notebook-runner: `docs/reports/notebook-runner/H2_20261004_1219.md`

## Changes the agents made on their own since the last checkpoint
8 entries in RUN_LOG.md (#4 to #11). Notable: 3 BUILD (pipeline.py bodies + `missing_tokens`; notebook 01, 31 cells; notebook 02, 50 cells) and 1 builder note (kernel.json read outside the repo); 0 FIX (runner made no mechanical fixes); 4 check runs.

## Approve or correct (Joseph ticks each line)
| # | Item | Fact from the reports | Approve | Correct (what, in my words) |
|---|---|---|---|---|
| 1 | Split rows | raw (5110, 12); train (3577, 12); test (1533, 12); 3577 + 1533 = 5110; shared ids 0; every raw id in exactly one part (data-validator §1, verifier spot checks) | [x] | |
| 2 | Split rows are raw rows | `DataFrame.equals` True for train and test vs raw by id; dtypes equal (data-validator §1) | [x] | |
| 3 | Card D1 vs notebook 01 | card option A; config and nb01 output `TEST_SIZE: 0.3 / SPLIT_SEED: 33 / STRATIFY_ON: None`; verifier's own `train_test_split(..., 0.30, 33)` gives the saved train ids (data-validator §3, verifier #9) | [x] | |
| 4 | Card D1 "how to test" outputs | quoted from nb01 in data-validator §3: stroke shares, work_type shares, rows add up, every work_type group in both parts, same seed same ids, raw hash matches | [x] | |
| 5 | Split once | nb01 splits once; re-split cell is the repeatability check and saves nothing; save cell compares ids instead of overwriting (verifier #10) | [x] | |
| 6 | Train only (notebook 02) | nb02 reads only `config.TRAIN_RAW`, never names the test file; `test_eda_notebook_reads_train_only` PASSED; no fit-like calls in nb01, nb02, pipeline.py (data-validator §2, verifier #13) | [x] | |
| 7 | Notebook 02 charts | 14 PNGs: missing values 1, stroke and work_type shares 2, text columns 5 bar, 0/1 columns 3 bar, number columns 3 histograms; titles and axis labels set (verifier #14) | [x] | |
| 8 | No D2 to D8 code | `fit_prep`, `transform`, `balance`, `repair_after_balance` still `NotImplementedError` (verifier #4, data-validator §2) | [x] | |
| 9 | D2 to D8 card check outputs (train only) | raw outputs in data-validator §4; steps needing a blank decision or test data marked NOT CHECKABLE | [x] | |
| 10 | Claims list | `list_claims.py`: 94 sentences, all kit text, headings, quotes or dates; claims checked 0 (no Joseph prose yet) (data-validator §0) | [x] | |
| 11 | Reproducibility | clone reruns: `0 of 17` and `0 of 24` code cells differ; split file SHA-256 identical to working copy (repo-auditor, verifier) | [x] | |
| 12 | Tests, lint, notebooks | pytest `31 passed, 34 skipped`; ruff `All checks passed!` on src, tests, scripts, notebooks; counts 1..17 and 1..24, 0 errors (repo-auditor) | [x] | |
| 13 | A2.5 | D1 committed in 149de94 (10:46 CT) before any notebook commit; D2 to D8 deferred to H2 by Joseph, checked against notebooks 03 and 04 (repo-auditor) | [x] | |
| 14 | Secrets, junk, large files, reference material | none; largest new file 328748 bytes (repo-auditor) | [x] | |
| 15 | Deliverables | `check_deliverables.py`: 7 MISSING (proposal PDF, notebooks 03 and 04, two journal PDFs, final and test CSVs); S3 and S4 present (repo-auditor) | [x] | |

## Verifier (pasted verbatim from the work-verifier report)
<!-- VERIFIER SECTION START -->
### Verifier (checks the agents, not Joseph)
Changes reviewed: 7 paths (1 modified: `src/stroke_prep/pipeline.py`; 6 new: `notebooks/01_load_split.ipynb`, `notebooks/02_eda_train.ipynb`, `data/interim/train_raw.csv`, `data/interim/test_raw.csv`, notebook-runner and data-validator H2 reports), 0 commits since base, 0 RUN_LOG H2 entries (repo-auditor logs after this report, by design)   Unlogged changes: 0 outside an agent report or the builder reply (7 not yet in RUN_LOG, pending repo-auditor)

| # | Finding | Where | Rule (spec / decision / lane / tests) | Evidence | FLAG/OK |
|---|---|---|---|---|---|
| 1 | Builder read `~/Library/Jupyter/kernels/stroke-eda/kernel.json` (outside the repo) to set notebook kernel metadata | builder session; both notebooks' `metadata.kernelspec` = `stroke-eda` | house rule 2 (work only inside the repo folder) | builder's own disclosure, relayed in Joseph's H2 task; `jupyter kernelspec list` → `stroke-eda /Users/josephclay/Library/Jupyter/kernels/stroke-eda`. I did not read that file. The kernel itself lives outside the repo, so every run (runner's and mine) launches it through jupyter | FLAG |
| 2 | Notebook 01 prints test-part shares of `stroke` and `work_type` (cells 17, 18) and reads test `work_type` groups (cell 22) | `notebooks/01_load_split.ipynb` cells 17, 18, 22 (1-based) | spec nb01 item 5 and card D1 "how to test" steps 1 and 2 require it; Joseph's process note 4 says never print test data to help him decide. D1 is final (note 3), so these outputs are not inputs to a decision. Spec vs process note: for Joseph to judge | cell sources `shares(config.TARGET)`, `shares(config.BALANCE_COL)` build `{"train": ..., "test": ...}`; cell 22 `set(test[config.BALANCE_COL])` | FLAG |
| 3 | `pipeline.py`: only the TODO bodies of `load_raw`, `split_train_test`, `save_csv` replaced, plus new helper `missing_tokens`; signatures and docstrings unchanged | `src/stroke_prep/pipeline.py` lines 22-49, 51-71, 114-125 | lane: builder (new function bodies) | `git diff H1-signed -- src/stroke_prep/pipeline.py` | OK |
| 4 | No D2 to D8 code: `fit_prep`, `transform`, `balance`, `repair_after_balance` still raise `NotImplementedError` | `pipeline.py` lines 81, 91, 101, 111 | process note 2 | `grep -n NotImplementedError src/stroke_prep/pipeline.py`; no fit, fill, encoder, scaler or SMOTE call in either notebook's code cells (all 41 code cells read) | OK |
| 5 | Both notebooks are new files; every cell is builder-created; no existing cell was edited | `notebooks/` | lane: builder (new cells only) | `git status --short` → `?? notebooks/01_load_split.ipynb`, `?? notebooks/02_eda_train.ipynb` | OK |
| 6 | No placeholder filled; markdown is only headings and placeholders | nb01: 5 placeholders; nb02: 15 (14 under charts + findings cell) | house rule 6; INTERPRETATION TOUCHED check | script over cell sources: non-heading, non-placeholder markdown cells = [] in both | OK |
| 7 | Runner changed no cell source | both notebooks | lane: notebook-runner (no new analysis, no markdown) | runner report says "unchanged (all 31 / 50 cells)", no fixes. No pre-run builder copy exists (`.nbrun/` empty) to diff against; see Not verified | NOT VERIFIED |
| 8 | No file Joseph owns changed (tests, scripts, CI, `.kiro/`, `.claude/`, requirements, pyproject, `config.py`, cards, tracking, README) | repo | lane / INTERPRETATION TOUCHED | `git diff --stat H1-signed -- tests scripts .github .kiro .claude requirements.txt pyproject.toml src/stroke_prep/config.py docs/decisions docs/tracking README.md` → empty | OK |
| 9 | Notebook 01 matches card D1 (option A, seed 33, 30% test) | nb01 cells 12, 13; `split_train_test` | decision D1 | cell 12 output `TEST_SIZE: 0.3 / SPLIT_SEED: 33 / STRATIFY_ON: None`; my own `train_test_split(raw, test_size=0.30, random_state=33)` train ids == saved `train_raw.csv` ids: True | OK |
| 10 | Split happens once; cell 23 re-split is the D1 step 3 repeatability check and saves nothing; cell 28 compares ids instead of overwriting existing files | nb01 cells 13, 23, 28 | process note 3; spec nb01 item 4 | cell sources | OK |
| 11 | `missing_tokens` finds no extra token in this file; the raw file's only non-numeric value in number columns is `''` (bmi, 201 rows), which pandas reads as missing by default | nb01 cell 5 output `missing value tokens found: []`; cell 9 `bmi 201` | spec nb01 item 2 | my read with `keep_default_na=False, dtype=str`: age {}, avg_glucose_level {}, bmi {'': 201} | OK |
| 12 | No data numbers hard coded in code | both notebooks, `pipeline.py` | house rule 7; INVENTED VALUE | numeric literals in code cells are only `0` (path index), `round(4)`, figsize, tick rotation and `0/1` labels | OK |
| 13 | Notebook 02 never names the test file and reads only `config.TRAIN_RAW` | nb02 cell 4 | spec nb02 item 1; Canvas S4 | no cell source in nb02 contains "test" (case-insensitive); `test_eda_notebook_reads_train_only` PASSED | OK |
| 14 | Notebook 02 charts match Joseph's choice (Q4: b) plus the builder's missing-values chart | nb02 cells 16, 19, 21, 24-39, 42-46 | Joseph's chart choice; spec nb02 item 3 | 14 PNG outputs: missing values 1; stroke and work_type shares 2; text columns 5 bar; 0/1 columns 3 bar; number columns 3 histograms; no relationship charts. Every chart sets title, xlabel, ylabel (cell 16 and helpers in cells 12-14). Cell 48 asserts every text, 0/1 and number column is charted | OK |
| 15 | Notebook 02 writes no data | nb02 | spec nb02 item 6 | no `to_csv`, `save_csv` or write-mode `open` in nb02 code cells | OK |
| 16 | Tests and checks not weakened: no test, script or CI file changed; no new skip, xfail, noqa, filterwarnings or try/except around an assert | `tests/`, `scripts/`, `.github/`, new code | VALIDATION_PROTOCOL; tests rule | finding 8 diff empty; skips are existing "blank slot" and "fit_prep not implemented" reasons (`pytest -rA`) | OK |
| 17 | `data/interim/*.csv` are not git-ignored (tracked by design per `.gitignore` note), untracked until the repo-auditor commits | `data/interim/` | .gitignore note "data/interim ... intentionally TRACKED" | `git check-ignore -v` → no match (exit 1) | OK |
| 18 | Placeholder count wording differs: runner says nb02 has 14, validator says 15 | runner and validator H2 reports | consistency of reports | findings cell text is `[Joseph writes here at H2: each data problem ...]`, so an exact-match count gives 14 and a prefix count gives 15; same cells, no content problem | OK |
| 19 | Validator cites notebook cells by 0-based index (its "cell 12" is my cell 13) | data-validator H2 report sections 1, 3 | report clarity | outputs it quotes match the cells I read | OK |
| 20 | Data-validator stayed in lane: wrote only its report; D2 to D8 "how to test" runs read only `train_raw.csv`; test file used only for id, row, column and equality checks, no test values printed | `docs/reports/data-validator/H2_20261004_1231.md` | lane; process note 4 | its scripts as shown in the report; `git status` shows no other new file from it | OK |

Spec nb01 acceptance: 1 met (cell 3) | 2 met (cells 5-6, finding 11) | 3 met (cells 6-9) | 4 met (cell 13, D1 values) | 5 met (cells 13, 17, 18, 26) | 6 met (cell 21) | 7 met (cell 28) | 8 met (cell 30, last code cell; last cell is a placeholder) | 9 not checkable (placeholders await Joseph) | 10 met (clean run in my clone, execution counts 1..17, outputs kept).
Spec nb02 acceptance: 1 met | 2 met (cells 6-8) | 3 met per Joseph's choice (finding 14) | 4 not checkable (14 placeholders await Joseph) | 5 not checkable (findings placeholder awaits Joseph) | 6 met.

Spot checks:
| check | my result | agent report said | agree/disagree |
|---|---|---|---|
| `scripts/check_raw_hash.py` | `OK raw data hash unchanged` | validator: hash OK; runner: before OK, after OK | agree |
| pytest, working copy | `31 passed, 34 skipped` | runner and validator: 31 passed, 34 skipped | agree |
| pytest, my clone | `31 passed, 34 skipped` | same | agree |
| clone rerun of nb01 and nb02 (stroke-eda kernel, nbconvert --execute) | 0 errors; all cell sources, all text outputs and all 14 PNG outputs byte-identical to the working copy | runner: PASS, 0 errors | agree |
| split files, clone vs working copy | SHA256 identical: train `60d8f421...a15f`, test `4b69717a...5c8` | runner wrote both files | agree |
| rows: raw, train, test, shared ids | raw (5110, 12); train (3577, 12); test 1533; sum 5110; shared ids 0 | validator: same | agree |
| train bmi missing and median | 138; 28.1 | validator D3: 138; 28.1 | agree |
| train work_type counts | Private 2041, Self-employed 585, children 477, Govt_job 461, Never_worked 13 | validator D2/D7: same | agree |
| train gender counts | Female 2121, Male 1455, Other 1 | validator D2: same | agree |
| raw bmi missing | 201 (`''` token) | validator: 201 | agree |
| ruff `src notebooks` | All checks passed | runner: ruff src clean | agree |

Not verified: runner made no source change (no pre-run builder copy exists to diff; only the runner's self-report and the fact that the sources I reviewed hold no fix); what else, if anything, the builder read outside the repo (I do not read outside the repo).
<!-- VERIFIER SECTION END -->

## Waiting for you (escalations)
No agent escalation. Items for Joseph:
* Verifier FLAG 1: the builder read `~/Library/Jupyter/kernels/stroke-eda/kernel.json` (outside the repo) for the kernel display name (house rule 2; RUN_LOG #7).
* Verifier FLAG 2: nb01 cells 17, 18 print test-part shares of `stroke` and `work_type`, cell 22 reads test `work_type` groups; process note 4 says never print test data to help Joseph decide; spec nb01 item 5 and D1 "how to test" steps 1 and 2 require these outputs.
* ADR 0001 draft was delivered in chat for Joseph to save in `docs/adr/` (no ADR file exists in the repo).

## Your writing at this checkpoint
* 20 placeholder cells `[Joseph writes here at H2...]`: 5 in `notebooks/01_load_split.ipynb`; 15 in `notebooks/02_eda_train.ipynb` (14 under charts + the findings cell)
* D1 H2 review block in `docs/decisions/D1_split.md` (second Signed line, line 63)
* Sign D2 to D8 in `docs/decisions/D2..D8` and fill their slots in `src/stroke_prep/config.py`
* Approve or correct ticks on this page
* Sign off row H2 in `docs/tracking/GATES.md`; tag `H2-signed`; push
