# ITAI 1371 Midterm EDA: Stroke Prediction Dataset

**Student:** Joseph Clay (independent contributor) | **Course:** ITAI 1371 | **Due:** see Canvas

> Scaffold state: this repo starts as scaffolding only. Every notebook, chart, function body,
> decision, ADR, journal, the proposal and the clean CSV are produced during the work described in
> **[LAB_GUIDE.md](LAB_GUIDE.md)**. The commit history and the reports in `docs/reports/` are the
> proof of work. Every number in this README must point to the notebook cell that printed it.

## Summary (fill in your words at H4)

[fill: 3 to 4 sentences in your words, written after notebook 04 has run. Point each number to
its notebook and cell.]

## Deliverables (Canvas items 1 to 8)

| # | Canvas item (verbatim) | File in this repo | Role | Commit | Status |
|---|---|---|---|---|---|
| 1 | "Upload document showing URL of original dataset" | `docs/dataset_url.md` | final | [fill] | [fill] |
| 2 | "Upload pdf describing dataset and proposal, not more than a page" | `docs/MT_JosephClay_ITAI1371_Proposal.pdf` | final | [fill] | [fill] |
| 3 | "In jupyter notebook use python to split dataset: training 70%, testing 30%; Python loads training data into memory; do not split manually or in excel" | `notebooks/01_load_split.ipynb` | final | [fill] | [fill] |
| 4 | "EDA performed only on training data; testing data untouched" | `notebooks/02_eda_train.ipynb` | final | [fill] | [fill] |
| 5 | "Jupyter notebook demonstrating before and after data processing" | `notebooks/03_preprocess_before_after.ipynb` and `notebooks/04_smote_balance.ipynb` | final | [fill] | [fill] |
| 6 | "Upload the .ipynb" | `notebooks/*.ipynb` (all four, outputs kept) | final | [fill] | [fill] |
| 7 | "Upload detailed proposal (reflection journal) of what you accomplished; each team member talks about contribution in the contribution journal" | `docs/MTJournal_R_JosephClay_ITAI1371.pdf`, `docs/MTJournal_C_JosephClay_ITAI1371.pdf` | final | [fill] | [fill] |
| 8 | "Upload final clean dataset" | **`data/processed/stroke_clean_final.csv`** (train set after balancing; synthetic rows marked in `is_synthetic` only if chosen in D8) | **FINAL** | [fill] | [fill] |
| 8 support | (not a Canvas item) | `data/processed/stroke_test_transformed.csv` (test set, transformed only, never balanced) | supporting | [fill] | [fill] |

Raw data: `data/raw/healthcare-dataset-stroke-data.csv` (never edited; `data/raw/SHA256SUMS`).

## Balancing

Source: Prof Rao's guidance. Approval of this dataset was conditional on balancing `work_type`,
and in class on Oct 1, 2026, Prof Rao said to balance `work_type` with SMOTE. Balancing runs on
the TRAIN set only; the test set is never balanced.

[fill at H3: how you set up SMOTE and what you did before and after it, citing decision cards
D6, D7, D8 and ADRs 0006 to 0008. Add one sentence with your before and after result, pointing to
the notebook 04 cell that printed it.]

## Decisions

All method choices are recorded as signed decision cards in `docs/decisions/` and as ADRs in
`docs/adr/`.

| Card | Question | My choice (fill after signing) | ADR |
|---|---|---|---|
| D1 | How to split 70/30 | [fill] | 0001 |
| D2 | Rare categories and identifier columns | [fill] | 0002 |
| D3 | Missing values | [fill] | 0003 |
| D4 | Encoding the text columns | [fill] | 0004 |
| D5 | Scaling and normalization | [fill] | 0005 |
| D6 | Order of steps around SMOTE | [fill] | 0006 |
| D7 | SMOTE setup | [fill] | 0007 |
| D8 | Repair and checks after SMOTE | [fill] | 0008 |

## Working method

[fill at H4, in past tense, only about what actually happened: who wrote the code, how you
directed and checked it, which subagent reports you used at each checkpoint, and where your own
decisions and writing are. Keep it consistent with the AI use disclosure in the contribution
journal.]

## Repo map

```text
data/raw/          original CSV + SHA256SUMS (never edited)
data/interim/      train and test files from notebook 01, optional prepared train from notebook 03
data/processed/    final clean dataset + transformed test set (notebook 04)
notebooks/         01_load_split, 02_eda_train, 03_preprocess_before_after, 04_smote_balance
src/stroke_prep/   config (facts + your decisions) and pipeline functions (stubs at start)
tests/             environment, raw data, and invariant tests (skip until artifacts exist)
docs/              dataset_url, specs, decisions, adr, rca, journals, tracking, reports
scripts/           tooling (see below)
.claude/agents/    Claude Code: the five subagents (notebook-runner, data-validator, work-verifier,
                   repo-auditor, tutor-reviewer) and README.md with the role matrix
.kiro/agents/      Kiro CLI: the same five agents plus the builder, as JSON configs
.kiro/steering/    Kiro CLI: house rules, checkpoints, role matrix (same rules as CLAUDE.md)
```

## How to run

Tested on Python 3.14 and 3.13 (CI runs both).

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/setup_gate.py
python -m pytest -q
jupyter lab            # run notebooks 01 to 04 in order, Restart and Run All
python scripts/check_deliverables.py
```

Full checklist: [VALIDATION_PROTOCOL.md](VALIDATION_PROTOCOL.md).

## Tooling (Engineering extra, not graded)

These files are infrastructure, not assignment answers: `scripts/setup_gate.py` (environment
check), `scripts/check_raw_hash.py` (raw data guard), `scripts/check_deliverables.py` (lists
missing Canvas files), `scripts/check_commit_msg.py` (commit message format),
`scripts/list_claims.py` (lists every number in your prose for the validator),
`scripts/compare_outputs.py` (committed vs rerun notebook outputs), `.pre-commit-config.yaml`,
`.github/workflows/ci.yml`, `tests/`, `.claude/` and `.kiro/`. The checkpoints H1 to H4, decision cards, ADRs
and RCA notes are also engineering extras that support Documentation.

## Canvas text box line (paste at submission)

```text
[fill at H4: repo URL, final commit hash, path of the final clean dataset, path of the test set.]
```

## License

MIT, see `LICENSE`.
