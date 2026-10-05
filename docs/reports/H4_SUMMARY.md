# H4 SUMMARY  (one page)  2026-10-04 20:25 CT  commit 6577524

Written by the repo-auditor from the reports listed below. Facts only, no interpretation.

## Status
* Tests: 64 passed / 1 skipped / 0 failed   Raw hash: OK   CI on this commit: NOT VERIFIED (gh and network denied to agents)
* Notebooks run clean (fresh clone, new venv): 01 PASS, 02 PASS, 03 PASS, 04 PASS
* Reports behind this page:
  * data-validator: `docs/reports/data-validator/H4_20261004_2007.md`
  * work-verifier: `docs/reports/work-verifier/H4_20261004_2011.md`
  * repo-auditor (full): `docs/reports/repo-auditor/H4_20261004_2017.md`
  * repo-auditor (commit only, H4 prep): `docs/reports/repo-auditor/H4_20261004_1856_commit.md`
  * notebook-runner: `docs/reports/notebook-runner/H4_20261004_1854.md`

## Changes the agents made on their own since the last checkpoint
8 entries in RUN_LOG.md (#28 to #35). Mechanical only; no fixes. Notable: builder added nb04 cell
25 (stroke share by work_type) and placeholder cell 26 on your request (#28, #31; committed
c3594f5); runner E1 on placement resolved by the builder's move (#30).

## Approve or correct (Joseph ticks each line)
| # | Item | Fact from the reports | Approve | Correct (what, in my words) |
|---|---|---|---|---|
| 1 | Clone install | fresh clone of 6577524, NEW venv Python 3.14.6, `pip install -r requirements.txt` no errors, `OK environment check passed` (auditor B1.1, B1.2) | [ ] | |
| 2 | Raw hash | `healthcare-dataset-stroke-data.csv: OK`, `OK raw data hash unchanged` (auditor B1.3; validator I1; verifier #17) | [ ] | |
| 3 | Tests | `64 passed, 1 skipped`; skip = `tests/test_invariants_final.py:58` "id not kept in the final file (decision D2)"; B1.4 says invariant tests must run, not skip at H4 (auditor B1.4; verifier #12) | [ ] | |
| 4 | Lint | ruff 0.16.9 `All checks passed!` on src tests scripts and on notebooks (auditor) | [ ] | |
| 5 | Notebook reruns | clone venv kernel `python3` (not stroke-eda): 01 0/17, 02 0/24, 03 1/28 (code cell 23 stdout in 2 chunks vs 1, joined text identical), 04 0/30 code cells differ; 0 errors, 0 stderr, counts 1..n no gaps (auditor B1.5). Verifier clone with stroke-eda: 0 differ in all 4 (#16) | [ ] | |
| 6 | Data file hashes | 7 SHA-256 identical before and after rerun and = validator §4 (final a88d968b…, test transformed c6c4ed58…) (auditor B1.5b; verifier #17) | [ ] | |
| 7 | Deliverables | `OK all 11 deliverable files present` (auditor B1.6; verifier #13) | [ ] | |
| 8 | Canvas list | S1 to S8 each have a README row and an existing file; S9 = README Canvas text box line (l.148, yours); S10 = raw hash OK (auditor B1.7) | [ ] | |
| 9 | README pointers | nb04 cells 9 and 33 print 2040 per group and `shape: (10200, 23)`; nb01 prints 3577 / 1533; 36 paths exist; 0 BROKEN (auditor B1.8) | [ ] | |
| 10 | Claims | 87 checked: 76 MATCH, 2 MISMATCH, 1 NO SOURCE CELL, 8 NOT CHECKABLE; 15 commit hashes OK (validator §1, §2) | [ ] | |
| 11 | Integrity | 20 PASS, 0 FAIL; reconciliation 5110 -> 3577/1533 -> 3576 -> 10200 x 23, test 1533 x 23 (validator §4) | [ ] | |
| 12 | PDFs | journal R 3 pages and C 3 pages = committed markdown (layout only); proposal 1 page, 4 of 4 data claims MATCH (validator §3); journal PDFs made with WeasyPrint 69.0, not in the repo venv (verifier #10) | [ ] | |
| 13 | CI | `continue-on-error: true` removed from job `deliverables` in 6577524; run result and run hash NOT VERIFIED; protocol B2.1 names job `gates`, ci.yml names it `checkpoints` (auditor B2) | [ ] | |
| 14 | Secrets and junk | none committed; largest tracked file 1010047 bytes; no images, zip, .env, caches (auditor B1.9) | [ ] | |
| 15 | Cards before code (A2.5) | D1 149de94 before nb01 5f0abd5; D2 to D8 ccc2dc4 and D7 float line 0b94ef8 before nb03/nb04 a7ddbbc (auditor A2.5) | [ ] | |

## Verifier (pasted verbatim from the work-verifier report)
<!-- VERIFIER SECTION START -->
### Verifier (checks the agents, not Joseph)

Changes reviewed: 24 files (22 committed in 3 commits + 2 uncommitted agent reports), 3 commits (1 agent c3594f5, 2 Joseph 2d6c658 and 6577524), 5 RUN_LOG entries (#28 to #32)   Unlogged changes: 1 (data-validator H4 report, not yet in RUN_LOG)

| # | Finding | Where | Rule (spec / decision / lane / tests) | Evidence | FLAG/OK |
|---|---|---|---|---|---|
| 1 | Agent commit c3594f5 touches only nb04 (builder BUILD #28, #31; runner RERUN #29, ESCALATION E1 #30), runner report (runner's folder) and RUN_LOG (repo-auditor). Each file is in its owner's lane; committed by repo-auditor, scope `agent`; message passes `scripts/check_commit_msg.py` | c3594f5 | lane | `git log --stat a126aa1..HEAD`; `check_commit_msg.py /dev/stdin` exit 0 for c3594f5, 2d6c658, 6577524 | OK |
| 2 | c3594f5 only adds 2 cells to nb04 (1-based 25 code, 26 placeholder `[Joseph writes here at H4]`). All 44 base cells identical by position in type, source, outputs and metadata once execution counts are ignored; later cells' counts +1 (rerun with the new cell at In[17]); cell ids renumbered by nbstripout (the auditor's report says so) | notebooks/04_smote_balance.ipynb | lane (builder new cells only; runner no fixes) | my script, base vs c3594f5 with cells 25-26 removed: `diff ignoring exec counts: []`; 44 -> 46 cells | OK |
| 3 | c3594f5 against the request as RUN_LOG #28 records it ("stroke share within each work_type, real rows only and after SMOTE"): cell groups `repaired` by `config.BALANCE_COL`, mean of `config.TARGET` for `is_synthetic == 0` rows vs all rows, prints the table, draws a bar chart. Train only (no test read, no fit), no data handling change, no number from the data hard coded (only figsize 8x4 and round(4)). Chat wording itself NOT VERIFIED (I cannot see the chat) | nb04 cell 25 | spec / decision / INVENTED VALUE check | cell 25 source read; `git diff a126aa1 HEAD -- src tests scripts` empty | OK |
| 4 | Placement: the 2 cells sit after Joseph's H3 note on the 0/1 shares chart (cell 24) and before `## D8 Numeric check` (cell 27); runner E1 resolved by the builder's move (#31). Builder moved only its own new cells | nb04 cells 23 to 27 | lane (placement next to interpretation text) | c3594f5 cells 24-27 printed in order | OK |
| 5 | Uncommitted `docs/reports/data-validator/H4_20261004_2007.md` has no RUN_LOG entry yet (the repo-auditor H4 run is next in order). `docs/reports/repo-auditor/H4_20261004_1856_commit.md` is named in RUN_LOG #32. Both in their owners' folders | docs/reports/ | lane / logging | `git status --short` shows only these 2 files | FLAG |
| 6 | Joseph's 2d6c658 touches 19 files: README.md, the 3 PDFs (added), ADR 0003, 0004, 0005, 0006, 0008, cards D3, D4, D5, D6, D8, contribution, proposal and reflection journals, docs/rca/0001, notebooks/04 (cell 26: placeholder replaced). All are Joseph-owned file types. Cell 26 text = his draft (scratch/h4_drafts.md line 51) apart from line wraps; the fill is in Joseph's commit, not an agent's | 2d6c658 | lane (lane check only) | `git show --stat 2d6c658`; `git show 2d6c658 -- notebooks/04_smote_balance.ipynb` (1 hunk, cell id 25 source only) | OK |
| 7 | Joseph's 6577524 touches 4 files: `.github/workflows/ci.yml` (removes `continue-on-error: true` from job `deliverables`, 1 line), README.md (2 `[fill]` -> 2d6c658), docs/journals/contribution_journal.md (same 2 cells), docs/MTJournal_C_JosephClay_ITAI1371.pdf (re-exported) | 6577524 | lane (Joseph owns CI) | `git show --stat 6577524`; `git log -- .github/workflows/ci.yml`: only 89193d0 and 6577524 | OK |
| 8 | Builder wrote files into `scratch/h4/` (README.md, docs/journals/contribution_journal.md, both journal PDFs), `scratch/decisions/` (D2 to D8) and created `scratch/adr/` (empty). `scratch/` is not in the builder's write lane (`notebooks/**`, `src/stroke_prep/pipeline.py`); done at Joseph's request, git ignored. Committed README, contribution journal and both journal PDFs are byte identical to the scratch/h4 copies. Committed reflection journal, RCA 0001 and proposal outline vs Joseph's drafts: the extra word runs are kit template prompts and headings (word diff). scratch/decisions files are dated 18:39, before the base (a126aa1 18:48); scratch D3 = a126aa1 D3 including the "Review at H3" lines. Who typed those lines in the scratch copy: NOT VERIFIED (Joseph's note: Joseph wrote them) | scratch/ | lane (OUT OF LANE, at Joseph's request) | `ls -la scratch/*`; `cmp` (4 IDENTICAL); `git show a126aa1:docs/decisions/D3_missing_values.md \| diff - scratch/...` no output | FLAG |
| 9 | House rule 2: per Joseph's note the builder wrote a preview PNG to /tmp (outside the repo) while checking a PDF page count and deleted it at once without opening it. I cannot read outside the repo, so this is recorded from Joseph's note, not checked; no trace inside the repo | builder, this session | house rule 2 (work only inside the repo) | Joseph's process note | FLAG |
| 10 | Both journal PDFs report `Producer: WeasyPrint 69.0`; weasyprint is not in `.venv` site-packages and not in requirements.txt (mistune 3.3.4 is in .venv, an nbconvert dependency). So the export ran with a tool outside the repo's environment; where it ran: NOT VERIFIED. Proposal PDF: `Skia/PDF m154`, HeadlessChrome | docs/MTJournal_R/C_*.pdf | house rule 2 / requirements | `pdfinfo`; `ls .venv/lib/python3*/site-packages \| grep -i weasy` empty | FLAG |
| 11 | No test, script, src, config, hook, requirements, .kiro or .claude change since base; no new skip, xfail, noqa or filterwarnings. Only CI change is the removal of continue-on-error (makes the gate stricter) | tests/, scripts/, src/, ci.yml | tests | `git diff a126aa1 HEAD --stat -- tests scripts src .pre-commit-config.yaml requirements.txt pyproject.toml .kiro .claude` empty | OK |
| 12 | B1.4 states "at H4, the invariant tests must run, not skip". 1 skip remains: `tests/test_invariants_final.py:58 test_ids_in_final_trace_back_to_train_only`, which skips when `id` is not in the final file. D2 card: "id: A, drop it before any modeling step". My check: `id` in final columns: False | tests/test_invariants_final.py:58; docs/decisions/D2_rows_and_columns.md l.55 | tests / VALIDATION_PROTOCOL B1.4 | pytest `64 passed, 1 skipped`, `SKIPPED [1] ...:58: id not kept in the final file (decision D2)` (working copy and clone) | FLAG |
| 13 | B2.2: `continue-on-error` is gone from ci.yml (only comment and step-name text still mention it: l.73-75 "EXPECTED RED ... until checkpoint H4", l.87 step name "expected red until H4, then remove continue-on-error"). `check_deliverables.py` locally and in the clone: `OK all 11 deliverable files present`. The GitHub run result for 6577524 (green or red, B2.3 hash): NOT VERIFIED (gh and network denied) | .github/workflows/ci.yml | VALIDATION_PROTOCOL B2.2 | `grep -n continue-on-error ci.yml`; `check_deliverables.py` exit 0 | OK |
| 14 | Data-validator MISMATCH N2 (nb04 cell 26 "fell in every group that grew") rechecked: Never_worked grew 13 -> 2040 rows; stroke = 1 rows 0 real and 0 after SMOTE, share 0.0000 both; it fell in Govt_job, Self-employed, children. Text is Joseph's; listed for him | nb04 cell 26 | data-validator recheck | my script: `Never_worked stroke=1: real 0 all rows 0 rows 2040`; table below | FLAG |
| 15 | Data-validator MISMATCH J5 (reflection §2 cites nb02 for missing vs present bmi rows) rechecked: no nb02 code cell compares rows with and without bmi (nb02 cell 16 In[10] prints only missing counts); the values are printed by nb03 cell 19 In[11]. Recomputed on train after D2: age 53.6701 / 42.7484, glucose 131.8070 / 104.7432, stroke 0.1957 / 0.0410 = nb03 cell 19. Text is Joseph's; listed for him | docs/journals/reflection_journal.md §2 | data-validator recheck | my script over nb02/nb03 code cells containing `isna`/`missing` | FLAG |
| 16 | Fresh clone of 6577524 rerun, all 4 notebooks, kernel stroke-eda: 0 errors, 0 stderr, execution counts 1..n no gaps; compare_outputs vs the committed notebooks: 01 `0 of 17`, 02 `0 of 24`, 03 `0 of 28`, 04 `0 of 30 code cells differ` | scratch/clones/work-verifier_H4_20261004_2011 | B1.5 | nbconvert --execute --output-dir .wv_out; `scripts/compare_outputs.py` | OK |
| 17 | SHA-256 of raw, the 4 interim files and the 2 processed files after the clone rerun = before the rerun = data-validator H4 §4 and runner H4 values | clone data/ | integrity | `shasum -a 256` (7 hashes, all equal) | OK |
| 18 | My own slip: `mkdir -p ../wv_out_H4_20261004_2011` created an empty folder in scratch/clones/ next to my clone; removed at once (empty, mine, not a clone). Outputs went to my clone's `.wv_out/` | scratch/clones/ | lane (verifier clone only) | `ls -la` showed it empty before `rmdir` | OK |

Spot checks:

| Check | My result | Agent report said | agree/disagree |
|---|---|---|---|
| raw shape | (5110, 12) | validator R1 (5110, 12) | agree |
| train rows, bmi missing, gender Other, Never_worked, stroke share (train_raw) | 3577, 138, 1, 13, 0.047 | validator R2, J4, J6, J8, J7 | agree |
| final shape, `id` in final, is_synthetic sum, rows per work_type | (10200, 23), False, 6624, 2040 x 5 | validator R3, J13, J24 | agree |
| nb04 cell 25 table (real = train_raw minus Other; all = final, one hot argmax) | Govt_job 0.0542/0.0402, Never_worked 0.0000/0.0000, Private 0.0475/0.0475, Self-employed 0.0752/0.0613, children 0.0042/0.0034 | validator §5 MATCH 10 of 10; runner quote | agree |
| age mean real / synthetic (scaler inverse from prep_state) | 43.1698 / 31.7685 | validator J19 | agree |
| synthetic rows with stroke = 1 | 143 of 6624 | validator N4 | agree |
| MISMATCH N2 | Never_worked 0.0000 both, grew by 2027 | validator MISMATCH | agree |
| MISMATCH J5 | values only in nb03 cell 19 In[11] | validator MISMATCH | agree |
| raw hash | `OK raw data hash unchanged` (working copy and clone) | validator I1 | agree |
| pytest | 64 passed, 1 skipped (working copy 1.55 s, clone 2.04 s) | validator §6, runner, auditor 64/1 | agree |
| check_deliverables.py | `OK all 11 deliverable files present` (working copy and clone) | not stated by the validator | n/a |
| 4 notebooks rerun in clone vs committed | 0 differing code cells in each | runner (nb04 only): 0 of 29 old cells differ | agree |

Not verified:
* the chat text of Joseph's request for cell 25 (I see only RUN_LOG #28),
* the /tmp PNG write and delete (outside the repo, from Joseph's note only),
* where WeasyPrint 69.0 ran (not in the repo's .venv),
* who typed the H3 review lines in scratch/decisions copies (written before the base),
* the GitHub Actions result for 6577524 (B2.2 green, B2.3 hash): gh and network are denied.
<!-- VERIFIER SECTION END -->

## Waiting for you (escalations)
No agent escalation is open. Items only you decide (text MISMATCH = interpretation text):
1. MISMATCH N2, nb04 cell 26: "fell in every group that grew"; cell 25: fell in Govt_job, Self-employed, children; Never_worked grew by 2027 and stayed 0.0000 (validator §1f; verifier #14).
2. MISMATCH J5, reflection journal §2 cites nb02; the missing vs present bmi values are printed by nb03 cell 19 In[11] (validator §1b; verifier #15).
3. NO SOURCE CELL J17, reflection journal §5 "rounded many blended stroke values down to 0": no cell prints the direction; recomputed of 194: 95 to 0, 99 to 1 (validator §1b).
4. Fact note: README l.75 and contribution journal l.43 say "At H3 the builder stopped and escalated"; RUN_LOG #17 (16:13) "no escalation at the time", #18 E3 raised by the work-verifier (1622 #10) and the builder (validator §1h).
5. B1.4 skip: keep or change `tests/test_invariants_final.py:58` skip (verifier #12; auditor B1.4). Tests are yours; agents changed nothing. Skip accepted: id was dropped at D2 by design.
6. Verifier FLAGs 8 (builder writes in scratch/), 9 (/tmp PNG), 10 (WeasyPrint outside the venv): approve or correct each. [x] FLAG 8 approved [x] FLAG 9 approved [x] FLAG 10 approved. FLAG 5 closed by RUN_LOG #33; FLAGs 12, 14, 15 = items 5, 1, 2.
7. README "Canvas text box line" (your note: line 109; in the file at 6577524 the placeholder is line 148): still `[fill at H4: ...]` (yours, at submission).
8. Definition of done ticks, LAB_GUIDE §7 (S1 to S10).
9. `docs/tracking/GATES.md` H4 row (empty), tag `H4-signed`, push with tags; CI result for the pushed commit (B2.1 to B2.3 NOT VERIFIED by agents).

## Your writing at this checkpoint
* nb04 cell 26 (`notebooks/04_smote_balance.ipynb`), `docs/journals/reflection_journal.md` §2 and §5, README "What AI did" (l.75) and Canvas text box line (l.148), `docs/journals/contribution_journal.md` l.43, PDFs re-exported if the text changes
* `docs/tracking/GATES.md` H4 row; LAB_GUIDE §7 ticks
