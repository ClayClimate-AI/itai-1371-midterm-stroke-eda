# H3 SUMMARY  (one page)  2026-10-04 17:16 CT  commit 0b94ef8 + agent commit "feat(agent): build and run notebooks 03 and 04, H3 reports  [H3]"

Written by the repo-auditor from the reports listed below. Facts only, no interpretation.

## Status
* Tests: 64 passed / 1 skipped (`tests/test_invariants_final.py:58`, id not kept, D2) / 0 failed   Raw hash: OK   CI on this commit: not run by agents (`gh` denied; not pushed)
* Notebooks run clean: `03_preprocess_before_after.ipynb` PASS, `04_smote_balance.ipynb` PASS (runner in working copy; auditor and verifier reruns in clones); 01 and 02 unchanged since H2
* Reports behind this page:
  * data-validator: `docs/reports/data-validator/H3_20261004_1618.md` (full), `docs/reports/data-validator/H3_20261004_1704.md` (delta)
  * work-verifier: `docs/reports/work-verifier/H3_20261004_1711.md` (final; first review `H3_20261004_1622.md`)
  * repo-auditor (quick): `docs/reports/repo-auditor/H3_20261004_1716.md`
  * notebook-runner: `docs/reports/notebook-runner/H3_20261004_1610.md`, `H3_20261004_1614.md`, `H3_20261004_1648.md`

## Changes the agents made on their own since the last checkpoint
16 entries in RUN_LOG.md (#12 to #27). Notable: #12, #13 log the 2 H2 reports Joseph committed in 1aed277; 6 builder BUILD entries (#14 to #17, #19) and E3 (#18, resolved); 0 runner FIX at H3 (runner made no mechanical fixes).

## Approve or correct (Joseph ticks each line)
| # | Item | Fact from the reports | Approve | Correct (what, in my words) |
|---|---|---|---|---|
| 1 | Card vs notebook D2 to D8 | 7 MATCH, 0 DIFFERS; D7 "Column types going in: cast to float first" vs `fit_resample(X.astype(float), y)` MATCH (validator 1618 §1, 1704 §2) | [x] | |
| 2 | Card "how to test" steps | 30 steps: 27 MATCH, 0 MISMATCH, 2 NOT RUN (D6.1 other orders; D7.5 second k), 1 N/A (D2.4, id not kept) (validator 1618 §2) | [x] | |
| 3 | Leakage | every §3 row PASS (report header: leakage and integrity 24 PASS, 0 FAIL): every fit inside `fit_prep` on train only; MinMaxScaler exercise on train; `fit_resample` once on prepared train; test path transform only; state holds train only statistics; test never balanced, not filtered by D2 (validator 1618 §3, verifier 1711 #13) | [x] | |
| 4 | Reconciliation table rows | raw 5110; train 3577; test raw 1533; train after D2 3576 (−1); prepared train 3576; after SMOTE 10200 (+6624); after repair 10200; final 10200; test transformed 1533 (validator 1618 §4) | [x] | |
| 5 | Reconciliation table columns | raw 12; prepared train 18 (−1 id, +1 bmi_missing, −4 text, +10 one hot); after SMOTE 19 (+is_synthetic); final 23 (work_type −1 +5 one hot); test transformed 23, same columns in order (validator 1618 §4) | [x] | |
| 6 | Integrity after SMOTE | every §5 row PASS, final and test: no NaN, all numeric, 0/1 columns only 0/1, each one hot group sums to 1, is_synthetic 6624 = rows added, real rows = prepared train, work_type 2040 × 5; label count = one hot sum for all 5 (validator 1618 §5, 1704 §3) | [x] | |
| 7 | D8 repair change counts | 0/1: hypertension 334, heart_disease 223, stroke 194, bmi_missing 181; one hot rows: gender 658, ever_married 123, Residence_type 735, smoking_status 1056; 0 invalid after repair (nb04, validator 1618 §2 D8.1, D8.2) | [x] | |
| 8 | D8 range check | synthetic rows outside work_type real min/max: age 0, avg_glucose_level 0, bmi 0 (nb04, validator 1618 §2 D8.3) | [x] | |
| 9 | Independent rebuilds | prepared train, final file and test file each equal the validator's own rebuild (atol 1e-9) (validator 1618 §1, §5) | [x] | |
| 10 | Claims in changed prose | 1618: 20 rows, 17 MATCH, 0 MISMATCH, 3 NOT CHECKABLE; 1704: 1 MATCH (D7 "0.76 would become 0 as loaded") | [x] | |
| 11 | Tests, lint, notebooks | pytest `64 passed, 1 skipped`; ruff `All checks passed!` on src, tests, scripts, notebooks; counts 1..28 (nb03), 1..29 (nb04), 0 errors (repo-auditor) | [x] | |
| 12 | Reproducibility | clone reruns: nb04 `0 of 29` differ; nb03 `1 of 28` differ in the auditor clone (code cell 23, stdout split into 2 vs 1 stream chunks, joined text identical; verifier clone `0 of 28`); 4 data file SHA-256 identical in auditor clone, verifier clone and working copy (repo-auditor, verifier 1711) | [x] | |
| 13 | A2.5 | D2 to D8 committed in ccc2dc4, D7 dtype line in 0b94ef8; notebooks 03 and 04 first committed by this audit, after both (repo-auditor) | [x] | |
| 14 | Secrets, junk, large files, reference material | none; largest new file 1010047 bytes; `prep_state.joblib` 3529 bytes, written by nb03, byte identical in clone rerun (repo-auditor) | [x] | |
| 15 | Deliverables | `check_deliverables.py`: 3 MISSING (proposal PDF, two journal PDFs, H4); S5a, S5b, S8 present (repo-auditor) | [x] | |

## Verifier (pasted verbatim from the work-verifier report)
<!-- VERIFIER SECTION START -->
### Verifier (checks the agents, not Joseph)
Changes reviewed: 1 commit since base (0b94ef8, Joseph: docs/decisions/D7_smote_setup.md +2 lines, docs/journals/contribution_journal.md); uncommitted agent work: src/stroke_prep/pipeline.py, nb03, nb04, 4 data files, 6 agent reports (data-validator 1618, 1704; notebook-runner 1610, 1614, 1648; work-verifier 1622); RUN_LOG entries since base: 0 (last entry #11, 12:39 CT)   Unlogged changes: all H3 agent work + the 2 H2 reports in 1aed277 (pending the repo-auditor, which runs after this report)

| # | Finding | Where | Rule (spec / decision / lane / tests) | Evidence | FLAG/OK |
|---|---|---|---|---|---|
| 1 | 0b94ef8 is Joseph's (author ClayClimate-AI), touches only D7 card (adds the "Column types going in" line; original Signed line 3:33PM unchanged) and his contribution journal. Content not judged. | 0b94ef8 | lane (Joseph owns cards, journals) | `git show --stat 0b94ef8`; `git diff --stat ea395d1 HEAD`: 2 files | OK |
| 2 | 1622 #2: the 2 H2 reports committed in 1aed277 still have no RUN_LOG entry. Joseph's answer: repo-auditor logs them. | docs/reports/RUN_LOG.md (ends at #11) | unlogged | `grep` RUN_LOG: last entry #11 | FLAG (open, pending repo-auditor) |
| 3 | 1622 #3 (H2 sign off after H3 build started): Joseph's answer "noted, no change". Recorded. | ea395d1 | steering 02 order | Joseph's answer | OK (closed by Joseph) |
| 4 | 1622 #6 resolved: nb04 cell[15] is now the heading `### D7 how to test step 5: one k value on the signed card`; no other non heading, non placeholder builder prose. This is a builder edit to its own existing uncommitted cell, made on Joseph's explicit instruction; needs a BUILD entry in RUN_LOG. | nb04 cell[15] | house rule 6 / lane (builder: new cells; edit Joseph directed) | cell diff vs my 1622 clone copy: only cell[15] replaced | OK (Joseph directed; log pending) |
| 5 | 1622 #20 resolved: new nb04 code cell[31] (work_type label counts vs one hot sums, table + 2 panel Matplotlib bar chart) and new placeholder cell[32] `[Joseph writes here at H3]`. Cell uses config.BALANCE_COL, no hard coded data number. Table pairs sorted labels with encoder column order by position; my row wise argmax check confirms label and one hot agree. | nb04 cells[31],[32] | process note 8 / lane (builder new cell) / house rules 6, 7 | cell diff: `insert 31..33`; my recompute below | OK |
| 6 | No other nb04 cell changed since 1622; nb03 unchanged (0 of 44 cells); pipeline.py byte identical to the copy reviewed at 1622 (sha256 c86059d1...). pipeline.py file birth time is 17:07:52, 3 s after Joseph's commit (consistent with the pre-commit hook stash and restore of unstaged files); content unchanged. | nb03, nb04, pipeline.py | lane | cell compare script; `shasum -a 256` both copies equal; `stat` | OK |
| 7 | Placeholders: nb03 6, nb04 6 (cells 10, 21, 23, 28, 32, 43), all empty. | nb03, nb04 | house rule 6 | markdown scan | OK |
| 8 | Runner 1648 changed no cell source: .nbrun/04.before_H3rerun_1648.ipynb vs nb04 0 of 44 differ; runner did not touch nb03, pipeline.py, D7 card. | nb04 | lane (runner mechanical only) | source compare (caveat: backup made by the runner) | OK |
| 9 | 1622 #8, #9 (STATE_PATH and DROP_COLUMNS in pipeline.py): Joseph's answer "accept where they are". Recorded. | pipeline.py l.22, l.24 | house rule 7 | Joseph's answer | OK (closed by Joseph) |
| 10 | 1622 #10 resolved: D7 card now says "Column types going in: cast to float first" (added 4:46 PM per card, committed 17:07:49 in 0b94ef8); code `fit_resample(X.astype(float), y)` matches. No config slot for it; decision lives on the card and in code. | pipeline.py l.210; D7 card | decision D7 | `git show 0b94ef8`; `grep -n fit_resample` | OK |
| 11 | A2.5 for the new D7 line: card line committed (0b94ef8); nb03, nb04 and pipeline.py have no git history yet, so when the repo-auditor commits them after 0b94ef8 the card precedes the notebooks in git. Fact (already in 1622 #10): the float cast in code (16:13) was written before the card line (4:46 PM). | git history | A2.5 (process note 5) | `git log --all -- notebooks/03* notebooks/04*`: empty | OK |
| 12 | 1622 #11 to #19 (D2 to D8 vs cards, spec nb03 and nb04) unchanged: no code or cell change except #4, #5. nb04 cell indexes after 30 shifted by 2 (test cells now 37 to 41). Spec nb03 #7, nb04 #7 still wait for Joseph's text. | nb03, nb04 | decisions / specs | cell diff | OK |
| 13 | Leakage: `.fit` only in fit_prep (pipeline l.96, 101, 104, 109; called once, nb03 cell[13] on train_clean) and MinMaxScaler on train (nb03 cell[39]); `fit_resample` only in balance (l.210; nb04 cell[7], prepared train); test path nb04 cell[37] uses transform + encode_balance_col only, is_synthetic 0; test never balanced. New cell[31] reads train objects only. | pipeline.py; nb03; nb04 | leakage rule / house rule 5 / process note 7 | grep scan of fit, fit_resample, test in code cells | OK |
| 14 | Process note 4: I read and printed no test values (test file compared by hash only). | this review | process note 4 | commands list | OK |
| 15 | Tests and checks: no change to tests/, scripts/, .github/, .kiro/, .claude/, requirements.txt, pyproject.toml, .pre-commit-config.yaml, config.py, docs/decisions, docs/adr, docs/tracking, journals, README in the working tree; 0b94ef8 touched none of the protected test or CI paths. Still 1 skip (existing D2 id skip). | repo | tests / VALIDATION_PROTOCOL / process note 11 | `git diff --stat HEAD -- <paths>`: empty; `git status` | OK |
| 16 | Agent reports 1648 and 1704 quote only executed outputs or their own recomputations; headers state commit ea395d1 and "D7 card uncommitted", correct at 16:48 and 17:04 (before 0b94ef8 at 17:07:49). | runner H3_1648, validator H3_1704 | INVENTED VALUE | file times; my recompute | OK |
| 17 | Kernel stroke-eda in nb03 and nb04 metadata; clone reruns used it. | notebooks | process note 11 | metadata read | OK |

Spot checks:
| check | my result | agent report said | agree/disagree |
|---|---|---|---|
| raw hash (working copy and clone) | `OK raw data hash unchanged` | runner 1648, validator 1704: OK | agree |
| pytest (working copy and clone) | `64 passed, 1 skipped`; skip `tests/test_invariants_final.py:58` (D2 id) | runner 1648, validator 1704: 64 passed, 1 skipped | agree |
| ruff check src notebooks | `All checks passed!` | runner 1648: same | agree |
| clone of 0b94ef8 + uncommitted pipeline.py, nb03, nb04; rerun nb03 then nb04 (stroke-eda) | both exit 0; compare_outputs vs working copy: nb03 `0 of 28 code cells differ`, nb04 `0 of 29 code cells differ` | runner 1648: nb04 PASS | agree |
| SHA-256 of 4 data files, clone vs working copy | train_prepared f7a906de..., prep_state 13369514..., final a88d968b..., test_transformed c6c4ed58...: all identical; working copy files not rewritten by my run (mtimes 16:11 / 16:48) | runner 1648, validator 1704: same 4 hashes | agree |
| 1704 §3 label count vs one hot sum | 2040 for each of the 5 work_type values in both; row wise argmax == label `True` | validator: 2040 x 5, `True` | agree |
| 1704 §4 as loaded vs float | 14 int columns, 10200 rows; cells in [0.5, 1) as float 3040, as loaded 0 for 3040 | validator: 3040 / 3040 | agree |
| 1704 §4 example | first stroke in (0.5, 1) is row 3576: float 0.759024, as loaded 0 | validator: row 3576, 0.759024, 0 | agree |
| D8 rule A on float output | final hypertension and stroke == (float SMOTE >= 0.5) `True`; is_synthetic 6624, final (10200, 23) | validator 1618/1704: same | agree |

Not verified:
| item | reason |
|---|---|
| which agent wrote the nb04 cells[15],[31],[32] edits | uncommitted, no git authorship; based on Joseph's note, runner 1648 report and the .nbrun backup timing (16:48:42) |
| runner changed no cell source | only evidence is the .nbrun backup, which the runner made |
| that pipeline.py rebirth at 17:07:52 came from the pre-commit stash and restore | inferred from timing and the hook config; content hash proves no change |
| spec nb03 #7, nb04 #7; D7 "Review at H3" | Joseph's text and review not written yet (his lane, not judged) |
<!-- VERIFIER SECTION END -->

## Waiting for you (escalations)
No open agent escalation. Items for Joseph:
* E3 resolved: float cast in `balance()` not on the signed D7 card (decision not recorded / data handling change; verifier 1622 #10, RUN_LOG #17, #18). Your answer: "D7 dtype b"; recorded on the D7 card in 0b94ef8 ("Column types going in: cast to float first").
* 12 empty placeholders: nb03 cells 11, 15, 26, 32, 37, 41; nb04 cells 10, 21, 23, 28, 32, 43 (43 = ML use cell) (0-based).
* D2 to D8 "Review at H3" blocks: second Signed line blank in each card.
* ADRs 0002 to 0008: drafted by the builder in chat for you to save in `docs/adr/` (only 0001 exists in the repo).
* `docs/tracking/GATES.md` H3 row (line 45) blank.
* Push, and tag `H3-signed` (not pushed: push is Joseph's, denied to agents; no tag made).

## Your writing at this checkpoint
* 12 placeholder cells `[Joseph writes here at H3...]` in `notebooks/03_preprocess_before_after.ipynb` and `notebooks/04_smote_balance.ipynb` (before and after notes, ML use cell)
* "Review at H3" blocks in `docs/decisions/D2_rows_and_columns.md` to `D8_after_smote.md`
* ADRs 0002 to 0008 in `docs/adr/`
* Approve or correct ticks on this page
* Sign off row H3 in `docs/tracking/GATES.md`; tag `H3-signed`; push
