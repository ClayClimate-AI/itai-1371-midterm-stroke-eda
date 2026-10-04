# Validation protocol

Two levels. Local checks prove each notebook and each claim. Repository checks prove a stranger
can clone the repo and get the same outputs. None of these checks knows an "expected" number:
they compare your text with your data, and your data with rules that hold for any correct choice.

Run commands from the repo root with the venv active (`source .venv/bin/activate`).

**Who runs what.** Between checkpoints the agents run sections A and B themselves, in a loop, and
fix mechanical failures on their own, each in its own lane (role matrix in
`.claude/agents/README.md`; each fix is logged in `docs/reports/RUN_LOG.md`). Section D checks
the agents themselves. You do
not run these by hand unless you want to. At each checkpoint you read ONE page,
`docs/reports/H#_SUMMARY.md`, which reports every check below as PASS, FAIL or SKIPPED with a link
to the full report. The commands are here so you can rerun any check yourself.

## A. Local level

### A1. Per notebook (every time a notebook changes)

| # | Check | How to run | Pass when |
|---|---|---|---|
| A1.1 | Runs top to bottom in a clean kernel | Jupyter: Kernel > Restart and Run All. Or ask: "Use the notebook-runner subagent on notebooks/0N_....ipynb" | no error cell; execution counts run 1, 2, 3 ... with no gaps |
| A1.2 | Committed outputs match a rerun | notebook-runner report, or `python scripts/compare_outputs.py notebooks/0N.ipynb .nbrun/0N.ipynb` | no differing cell, or each difference explained |
| A1.3 | Raw file untouched | `python scripts/check_raw_hash.py` | OK |
| A1.4 | EDA reads train only | `python -m pytest -q tests/test_invariants_notebooks.py` | pass |
| A1.5 | Charts readable | look at each chart | title, labeled axes, legend where needed |
| A1.6 | Sample data printed as it is processed | look for `head()` before and after each step | present (Canvas GL6) |
| A1.7 | Lint | `ruff check src tests scripts` | no errors |

### A2. Per claim (every number in your prose)

Prose means: notebook markdown cells, README, `docs/*.md`, journals, ADRs, decision cards.

| # | Check | How to run | Pass when |
|---|---|---|---|
| A2.1 | List every number you wrote | `python scripts/list_claims.py` | you recognize every line |
| A2.2 | Each number points to a cell | read the list; each claim names a notebook and cell | no claim without a source cell |
| A2.3 | Each number is recomputed independently | "Use the data-validator subagent on <files> for H#" | every claim is MATCH; NOT CHECKABLE ones explained |
| A2.4 | Words match the numbers | reread each sentence next to its output | the sentence says no more than the output shows |
| A2.5 | Decision cards are signed before code | `git log --follow docs/decisions/D*.md` vs the notebook commit | card commit comes first |

### A3. Data integrity (H2, H3)

| # | Check | How to run | Pass when |
|---|---|---|---|
| A3.1 | Split reconciles | `python -m pytest -q tests/test_invariants_split.py` | pass (skips before notebook 01) |
| A3.2 | Pipeline contracts | `python -m pytest -q tests/test_pipeline_contracts.py` | pass (skips until functions exist and D1 is set) |
| A3.3 | Final and test files | `python -m pytest -q tests/test_invariants_final.py` | pass (skips before notebook 04) |
| A3.4 | No leakage | data-validator report, section "Leakage" | every item PASS: all fitting on train only, test never balanced, EDA on train only |
| A3.5 | Rows and columns reconcile raw to final | data-validator report, section "Reconciliation" | every row and column change is explained by a signed card |
| A3.6 | After SMOTE | data-validator report, section "Integrity" | no NaN; binaries 0/1; each one hot group valid; if D8 chose a marking column, `is_synthetic` present and its count equals rows added |

## B. Repository level

### B1. Fresh clone reproducibility (H1 and H4, full mode)

Clones live in `scratch/clones/` inside the repo folder, so no agent needs to read or write
outside the project. `scratch/` is ignored by git, pytest, ruff and the pre-commit hooks.
Delete old clones yourself when you like (`rm -rf scratch/clones`).

Ask: "Use the repo-auditor subagent in full mode for H4." It does the following; you can also
run it by hand:

```bash
# Run from the repo root. The clone goes in scratch/clones/ (git ignored, inside the repo).
C="scratch/clones/manual_$(date +%Y%m%d_%H%M)"
mkdir -p scratch/clones && git clone . "$C"
cd "$C"
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/setup_gate.py
(cd data/raw && shasum -a 256 -c SHA256SUMS)     # Linux: sha256sum -c SHA256SUMS
python -m pytest -q
ruff check src tests scripts
mkdir -p .nbrun
for nb in notebooks/0*.ipynb; do
  (cd notebooks && jupyter nbconvert --to notebook --execute \
     --ExecutePreprocessor.timeout=600 --output-dir ../.nbrun "$(basename "$nb")")
  python scripts/compare_outputs.py "$nb" ".nbrun/$(basename "$nb")"
done
python scripts/check_deliverables.py
```

| # | Check | Pass when |
|---|---|---|
| B1.1 | Clean install from `requirements.txt` | no errors |
| B1.2 | Environment check | `OK environment check passed` |
| B1.3 | Raw hash | `OK` |
| B1.4 | Tests | 0 failed (at H4, the invariant tests must run, not skip) |
| B1.5 | Every notebook reruns | no error; outputs match the committed ones or the difference is explained |
| B1.6 | Deliverables | `check_deliverables.py` prints OK |
| B1.7 | Canvas uploads | every item in `docs/specs/midterm_acceptance.md` has a file in the README table |
| B1.8 | README pointers | every "cell [n]" in README points to a real cell with that output |
| B1.9 | No secrets or junk | no keys, tokens, `.env`, venv, caches, zip files, or files over 20 MB committed |

### B2. CI (every push)

| # | Check | How to run | Pass when |
|---|---|---|---|
| B2.1 | CI workflow ran | GitHub > Actions, or `git push` then open the run | job `gates` green |
| B2.2 | Deliverables job | same run, job `deliverables` | allowed red before H4; at H4 remove `continue-on-error` and it must be green |
| B2.3 | CI used the pushed commit | the run's commit hash equals `git rev-parse HEAD` | equal |

## C. Checkpoint rule

| Checkpoint | Sections the summary must cover | Mode |
|---|---|---|
| H1 Kickoff | A1.3, A1.7, B1 (on the scaffold), B2, every card signed with a source | auditor full |
| H2 After EDA | A1 for notebooks 01 and 02, A2 (claims list), A3.1, A3.2, A3.4 (train only), card D1 checks | auditor quick |
| H3 After prep and SMOTE | A1 for notebooks 03 and 04, A2 (your H2 text rechecked), A3 all, cards D2 to D8 checks | auditor quick |
| H4 Final | A2 on all prose, B1 full, B2, definition of done | auditor full |

A checkpoint is signed in `docs/tracking/GATES.md` only when: its summary exists and links a
data-validator report, a work-verifier report and a repo-auditor report for that checkpoint, the
verifier section is present and every FLAG in it is approved or corrected by you, every approve or correct
line is ticked or corrected by you, no escalation is open, and you have read it. Green tests alone
never count as done.

## D. Checking the agents (work-verifier, every checkpoint)

Ask: "Use the work-verifier subagent for H<n>." It does not trust the other reports.

| # | Check | How it runs | Pass when |
|---|---|---|---|
| D1 | Every change is logged | `git diff H<n-1>-signed` vs RUN_LOG entries | no unlogged change |
| D2 | Changes meet the specs | each changed notebook or function vs `midterm_acceptance.md` and nb01 to nb04 specs | no FLAG |
| D3 | Data handling matches your decisions | each data handling change vs signed cards and ADRs | no `UNDECIDED DATA HANDLING`, no `DIFFERS FROM CARD` |
| D4 | Every agent stayed in its lane | each change vs the role matrix | no `OUT OF LANE`, `INTERPRETATION TOUCHED`, `INVENTED VALUE` |
| D5 | Checks were not weakened | diff of `tests/`, `scripts/`, CI, hash, skips, try/except, noqa, warnings filters | none, or each approved by you |
| D6 | Its own spot checks agree | raw hash, pytest, two recomputations, one notebook rerun in its clone in `scratch/clones/` | agree with the other agents' reports |
