# Human checkpoints H1 to H4
**[Engineering extra, not graded]**

Four checkpoints, batched. Between them the agents work on their own. At each checkpoint you read
ONE page (`docs/reports/H#_SUMMARY.md`; each agent's full report sits in its own folder
`docs/reports/<agent>/`), tick approve or correct, and do the writing that only you
can do. A checkpoint should take minutes for the review part; the writing takes as long as it takes.

**Green tests alone never count as done.** A checkpoint passes only when the summary page exists,
it links a data-validator, a work-verifier and a repo-auditor report for that checkpoint, every
item on it is ticked approve or has a correction you wrote, you signed below, and you tagged the
commit `H<n>-signed` (`git tag H1-signed`, then `git push --tags`).

| Checkpoint | When | What you do | What the agents bring you |
|---|---|---|---|
| **H1 Kickoff** | before any analysis | Approve the setup report. Read all decision cards D1 to D8 and record every method decision in one sitting, each with source and reasoning, and set the values in `config.py`. Push. | `docs/reports/H1_SUMMARY.md` linking: notebook-runner setup report (environment, tests, raw hash, first push and CI) in `docs/reports/notebook-runner/`; data-validator report (raw file hash, row and column counts) in `docs/reports/data-validator/`; work-verifier report (setup changes against specs, lanes and tests) in `docs/reports/work-verifier/`; repo-auditor FULL report in `docs/reports/repo-auditor/` |
| **H2 After EDA** | notebooks 01 and 02 have run | Review the batched report and the claims list. Write your EDA observations in your own words under each chart and in the findings cell. Keep or amend D1. | `docs/reports/H2_SUMMARY.md` linking: notebook-runner report in `docs/reports/notebook-runner/`; data-validator report (split invariants, train only check, raw outputs of the cards' "how to test" checks) in `docs/reports/data-validator/`; work-verifier report (every change since H1 against specs, cards, lanes and tests) in `docs/reports/work-verifier/`; repo-auditor quick report in `docs/reports/repo-auditor/` |
| **H3 After prep and SMOTE** | notebooks 03 and 04 have run, final files saved | Review the batched before and after and invariant report. Correct anything. Keep or amend D2 to D8. Write your before and after interpretation and the ML use cell. Write ADRs. | `docs/reports/H3_SUMMARY.md` linking: notebook-runner report in `docs/reports/notebook-runner/`; data-validator report (leakage, reconciliation, integrity after SMOTE, every number in your H2 text rechecked) in `docs/reports/data-validator/`; work-verifier report (every change since H2 against specs, cards, lanes and tests) in `docs/reports/work-verifier/`; repo-auditor quick report in `docs/reports/repo-auditor/` |
| **H4 Final** | your documents are written | Read the fresh clone audit, finish journals, proposal and README, tick the definition of done, submit. | `docs/reports/H4_SUMMARY.md` linking: repo-auditor FULL report (fresh clone in `scratch/clones/`, new venv, all notebooks rerun, `check_deliverables.py`, Canvas list) in `docs/reports/repo-auditor/`; data-validator report on every number in all your prose in `docs/reports/data-validator/`; work-verifier report (every change since H3, clean clone rerun) in `docs/reports/work-verifier/` |

## Between checkpoints: what agents may do on their own

They may fix MECHANICAL problems without asking: errors, wrong paths, imports, formatting, lint,
a cell that crashes, a failing test caused by code (not by a decision), rerunning notebooks.
Each agent stays in its lane (role matrix in `.claude/agents/README.md`) and records its changes
in its own report; the repo-auditor copies them into `docs/reports/RUN_LOG.md`. Before each
summary, the work-verifier checks every change against the specs, your decisions, the lanes and
the tests, and its findings appear verbatim in the summary.

They must STOP and escalate (it reaches you under "Waiting for you" in the summary) for:

1. a decision that is not already recorded on a signed card,
2. a validator mismatch they cannot explain,
3. any change to how data is handled (rows, columns, fill, encoding, scaling, order, SMOTE
   settings, repair rules, what goes in the final file), even if it would fix an error,
4. anything that touches interpretation text (your markdown, journals, ADRs, proposal, README
   prose, decision cards).

## Sign off log (you fill this in)

| Checkpoint | Date and time (CT) | Commit | Summary file | Corrections I asked for | Signed |
|---|---|---|---|---|---|
| H1 | 10/04/2026 11:33 AM | 07ba010 | docs/reports/H1_SUMMARY.md | D2 to D8 deferred to H2; decided from train EDA | Joseph Clay |
| H2 | | | | | |
| H3 | | | | | |
| H4 | | | | | |
