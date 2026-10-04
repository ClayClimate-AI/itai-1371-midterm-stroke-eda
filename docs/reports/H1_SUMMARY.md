# H1 SUMMARY  (one page)  2026-10-04 11:01 CT  commit 149de94

Written by the repo-auditor from the reports listed below. Facts only, no interpretation.

## Status
* Tests: 16 passed / 49 skipped / 0 failed   Raw hash: OK   CI on this commit: not run by agents (`gh` denied)
* Notebooks run clean: none exist at H1
* Reports behind this page:
  * data-validator: `docs/reports/data-validator/H1_20261004_1050.md`
  * work-verifier: `docs/reports/work-verifier/H1_20261004_1059.md`
  * repo-auditor (full): `docs/reports/repo-auditor/H1_20261004_1101.md`
  * notebook-runner: not run at H1 (Joseph's rule)

## Changes the agents made on their own since the last checkpoint
4 entries in RUN_LOG.md (#0 to #3). Mechanical only. Notable: no BUILD (builder built nothing); no FIX; three check runs (data-validator, work-verifier, repo-auditor), none changed code or data.

## Approve or correct (Joseph ticks each line)
| # | Item | Fact from the reports | Approve | Correct (what, in my words) |
|---|---|---|---|---|
| 1 | Fresh clone install | clone of 149de94, Python 3.14.6, new venv, `pip check`: "No broken requirements found.", `setup_gate.py`: "OK environment check passed" (repo-auditor) | [x] | |
| 2 | Raw data hash | `144ea5366832bb5432645c0e49fbb951aadf4ee1e75e73d2e15d3dc0841525bd` equals config and SHA256SUMS; `check_raw_hash.py`: "OK raw data hash unchanged" (data-validator, repo-auditor) | [x] | |
| 3 | Raw shape | `(5110, 12)`, 12 columns listed in the data-validator report | [x] | |
| 4 | Tests and lint | pytest `16 passed, 49 skipped`; ruff `All checks passed!` (repo-auditor) | [x] | |
| 5 | D1 split | card "Option I chose: A", signed 10/04/2026 9:49 AM (CT); config `SPLIT_SEED = 33`, `STRATIFY_ON = None`, `TEST_SIZE = 0.30` (data-validator, work-verifier, repo-auditor) | [x] | |
| 6 | D2 to D8 | deferred to H2 by Joseph (GATES.md H1 row); Signed lines blank; config slots unchanged since scaffold (work-verifier #4) | [x] | |
| 7 | A2.5 cards before code | D1 committed in 149de94; 0 notebook commits in history (repo-auditor) | [x] | |
| 8 | Split and final files | none in `data/interim` or `data/processed` (only `.gitkeep`) (data-validator) | [x] | |
| 9 | Secrets, junk, large files, reference material | none found in 90 tracked files; largest file 327451 bytes (repo-auditor) | [x] | |
| 10 | Deliverables | `check_deliverables.py`: 9 MISSING (notebooks 01 to 04, proposal PDF, two journal PDFs, final and test CSVs); `docs/dataset_url.md` present (repo-auditor) | [x] | |

## Verifier (pasted verbatim from the work-verifier report)
<!-- VERIFIER SECTION START -->
### Verifier (checks the agents, not Joseph)

Changes reviewed: 4 files (3 committed since 89193d0, 1 untracked), 2 commits since base (51c3003, 149de94), 0 RUN_LOG entries   Unlogged changes: 0 agent changes (the only agent file is the data-validator report, which the repo-auditor logs at this checkpoint)

| # | Finding | Where | Rule (spec / decision / lane / tests) | Evidence | FLAG/OK |
|---|---|---|---|---|---|
| 1 | `docs/tracking/GATES.md` H1 row changed by Joseph's commit | 51c3003 | lane: `docs/tracking/` owned by Joseph | `git diff --stat 89193d0`: GATES.md 1 line; author ClayClimate-AI, scope `docs(decisions)` | OK |
| 2 | `docs/decisions/D1_split.md` decision block filled by Joseph's commit | 149de94 | lane: decision cards owned by Joseph | `git diff 89193d0 -- docs/decisions`: only D1 changed; author ClayClimate-AI | OK |
| 3 | `src/stroke_prep/config.py` `SPLIT_SEED None -> 33` by Joseph's commit; `STRATIFY_ON` unchanged at `None` | 149de94, config.py line 40 | lane: `config.py` decision values owned by Joseph; decision: D1 card states `SPLIT_SEED = 33`, `STRATIFY_ON = None` | `git diff 89193d0 -- src`: 1 line changed in config.py; no other slot touched | OK |
| 4 | D2 to D8 cards unsigned, their config slots unchanged since scaffold | `docs/decisions/D2..D8`, `config.py` | decision: deferred to H2 by Joseph (GATES.md H1 row) | `grep "Signed:"`: only D1 line 57 filled; config diff is the one D1 line | OK |
| 5 | Untracked `docs/reports/data-validator/H1_20261004_1050.md` | working tree | lane: data-validator writes only `docs/reports/data-validator/` | `git status --porcelain --untracked-files=all`: this is the only untracked file | OK |
| 6 | No other agent writes in the working tree (notebooks, src, data, tests, scripts, `.kiro/`, `.claude/`, `.github/`, RUN_LOG, summaries) | working tree | lane | `git status --porcelain --ignored`: only the report above, plus ignored `.venv/`, caches, `__pycache__/`, `scratch/`, `LAB_GUIDE.pdf`, `START_HERE.md` | OK |
| 7 | `src/stroke_prep/pipeline.py` untouched since scaffold; all functions still `NotImplementedError` TODO shells; no D2 to D8 code | `src/stroke_prep/pipeline.py` lines 22 to 88 | decision: no D2 to D8 code at H1 | `git diff --quiet 89193d0 -- src/stroke_prep/pipeline.py` exit 0; grep lists 8 `raise NotImplementedError("TODO ...")` | OK |
| 8 | No notebooks built | `notebooks/` | spec: nothing built at H1 | `ls -a notebooks`: only `.gitkeep` | OK |
| 9 | Tests, scripts, CI, VALIDATION_PROTOCOL unchanged since scaffold (no new skip, xfail, noqa, hash change) | `tests/`, `scripts/`, `.github/`, `VALIDATION_PROTOCOL.md` | tests | `git diff --stat 89193d0` lists only GATES.md, D1_split.md, config.py | OK |
| 10 | RUN_LOG has no entries; the data-validator report's run is the one agent action to log | `docs/reports/RUN_LOG.md` | lane: repo-auditor logs at checkpoint | file holds only the template block | OK |
| 11 | Data-validator report contains no interpretation and no number beyond quoted command outputs | `docs/reports/data-validator/H1_20261004_1050.md` | lane: INVENTED VALUE / interpretation | numbers quoted (hash, shape 5110 x 12, 16/49 test counts, 88 claim sentences) are outputs; hash, shape, test counts reproduced below | OK |
| 12 | An earlier clone `scratch/clones/work-verifier_H1_20261004_1053` already exists; this run used a new clone `work-verifier_H1_20261004_1059` | `scratch/clones/` | lane: own clone folders only, never delete | `ls scratch/clones` | OK |

Spot checks:

| Check | My result (clone at 149de94) | Agent report said | Agree/disagree |
|---|---|---|---|
| `python scripts/check_raw_hash.py` | `OK raw data hash unchanged`, exit 0 | n/a (used shasum -c: OK) | agree |
| Raw SHA-256 vs `config.RAW_SHA256` | `144ea5366832bb5432645c0e49fbb951aadf4ee1e75e73d2e15d3dc0841525bd`, equal True; same value in `data/raw/SHA256SUMS` | same hash, MATCH | agree |
| Raw shape and columns | `(5110, 12)`; `['id', 'gender', 'age', 'hypertension', 'heart_disease', 'ever_married', 'work_type', 'Residence_type', 'avg_glucose_level', 'bmi', 'smoking_status', 'stroke']` | same | agree |
| D1 slots vs card | config `SPLIT_SEED 33`, `STRATIFY_ON None`, `TEST_SIZE 0.3`; card line "Value set in config.py: `SPLIT_SEED = 33`, `STRATIFY_ON = None`", Signed line filled | PASS | agree |
| `data/interim`, `data/processed` empty | only `.gitkeep` in each (clone and working tree); `train_raw.csv`, `test_raw.csv`, `train_prepared.csv`, `stroke_clean_final.csv`, `stroke_test_transformed.csv` all `exists() False` | PASS | agree |
| `python -m pytest -q -p no:cacheprovider` | `16 passed, 49 skipped in 1.60s` | data-validator: 16 passed, 49 skipped; builder: 16 passed, 49 skipped, 0 failed | agree |
| Notebook rerun in clone | not applicable: no notebooks exist | n/a | n/a |

Not verified: notebook rerun (no notebook exists at H1). Listing tags not run (`git tag` is denied to this agent; base taken as scaffold 89193d0 as stated by Joseph).
<!-- VERIFIER SECTION END -->

## Waiting for you (escalations)
None.

## Your writing at this checkpoint
* Sign off row H1 in `docs/tracking/GATES.md` (date, commit, summary file, signed)
* Approve or correct ticks on this page
* Tag `H1-signed` and push
