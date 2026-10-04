---
inclusion: always
---

# Checkpoints, autonomy and escalation

## Only four checkpoints count: H1, H2, H3, H4

```text
H1 Kickoff (Joseph): setup approved, ALL cards D1..D8 signed, config.py set, pushed
   │
   ├─ agents, on their own: build notebook 01 (D1) and notebook 02 (charts on train)
   │    loop: notebook-runner → data-validator → fix mechanical → repeat
   │    then: work-verifier (checks the agents) → repo-auditor (quick, log, commit, summary)
   ▼
H2 After EDA (Joseph): read H2_SUMMARY.md, approve or correct, write EDA observations, keep or amend D1
   │
   ├─ agents, on their own: build notebook 03 (D2..D6) and notebook 04 (D6..D8), save final files
   │    same loop; data-validator runs cards D2..D8 checks, leakage, reconciliation, integrity
   │    then: work-verifier → repo-auditor
   ▼
H3 After prep and SMOTE (Joseph): read H3_SUMMARY.md, approve or correct, write before and after notes, ADRs
   │
   ├─ agents: data-validator on every number in Joseph's prose; work-verifier; repo-auditor FULL
   ▼
H4 Final (Joseph): read H4_SUMMARY.md, finish journals, proposal, README, definition of done, submit
```

* H1 to H4 are the ONLY checkpoints. Do not invent extra checkpoints or stop for approvals in
  between, except for the four escalation reasons below.
* The older builder loop with stages C0 to C4 (from earlier kit versions) is NOT used. Do not
  create C0 to C4 entries, labels or approval stops.
* Older gate names G0 to G7 are retired. Use H1 to H4 everywhere (commit tags `[H1]` to `[H4]`).
* `docs/tracking/PIOF.md` is an OPTIONAL log that Joseph may use when he directs a specific
  build. Agents never require it and never write it. Agent work is logged in
  `docs/reports/RUN_LOG.md` by the repo-auditor.
* Each checkpoint has ONE page: `docs/reports/H#_SUMMARY.md`, written by the repo-auditor from
  `docs/reports/CHECKPOINT_SUMMARY_TEMPLATE.md`, with an approve or correct list and the
  work-verifier section pasted verbatim.
* **Green tests alone never count as done.** A checkpoint needs the summary, a data-validator
  report, a work-verifier report and a repo-auditor report (full mode at H1 and H4) for that
  checkpoint, plus Joseph's sign off in `docs/tracking/GATES.md` and his tag `H<n>-signed`.

## Order at each checkpoint

```text
builder builds → notebook-runner runs and fixes → data-validator checks
  → work-verifier checks the agents → repo-auditor audits, logs, commits, writes H<n>_SUMMARY.md
  → Joseph approves or corrects, signs, tags H<n>-signed, pushes
```

## Autonomy between checkpoints

Fix on your own, without asking, inside your lane: errors, wrong paths, imports, formatting,
crashing code cells, failing tests caused by code, stale outputs. Each agent records its fixes in
its own report; the repo-auditor copies them into `docs/reports/RUN_LOG.md`.

## Escalation: STOP only for these four reasons

Write ESCALATION in your report or reply; the repo-auditor carries it to RUN_LOG and the summary;
then wait for Joseph.

1. a decision not already recorded on a signed card,
2. a validator mismatch you cannot explain,
3. any change to data handling choices (rows, columns, fill, encoding, scaling, order, SMOTE
   settings, repair rules, final file contents), even to fix an error,
4. anything touching interpretation text.
