# ITAI 1371 Midterm EDA: Stroke Prediction Dataset

**Student:** Joseph Clay (independent contributor) | **Course:** ITAI 1371 | **Due:** see Canvas

> Scaffold state: this repo starts as scaffolding only. Every notebook, chart, function body,
> decision, ADR, journal, the proposal and the clean CSV are produced during the work described in
> **[LAB_GUIDE.md](LAB_GUIDE.md)**. The commit history and the reports in `docs/reports/` are the
> proof of work. Every number in this README must point to the notebook cell that printed it.

## Summary (fill in your words at H4)

This repo takes the Kaggle stroke dataset (5110 rows) through EDA, preprocessing and SMOTE
balancing on work_type. Train was split 70/30 with seed 33 (3577 train, 1533 test, nb01). After
cleaning, encoding and scaling, SMOTE grew every work_type group to 2040 rows, giving a final train
file of 10200 rows by 23 columns (nb04 cells 9, 33). The test file was never balanced and has the
same 23 columns.

## Deliverables (Canvas items 1 to 8)

| # | Canvas item (verbatim) | File in this repo | Role | Commit | Status |
|---|---|---|---|---|---|
| 1 | "Upload document showing URL of original dataset" | `docs/dataset_url.md` | final | 89193d0 | Done |
| 2 | "Upload pdf describing dataset and proposal, not more than a page" | `docs/MT_JosephClay_ITAI1371_Proposal.pdf` | final | [fill] | Done |
| 3 | "In jupyter notebook use python to split dataset: training 70%, testing 30%; Python loads training data into memory; do not split manually or in excel" | `notebooks/01_load_split.ipynb` | final | 5f0abd5 | Done |
| 4 | "EDA performed only on training data; testing data untouched" | `notebooks/02_eda_train.ipynb` | final | a24f16f, c17a968 | Done |
| 5 | "Jupyter notebook demonstrating before and after data processing" | `notebooks/03_preprocess_before_after.ipynb` and `notebooks/04_smote_balance.ipynb` | final | a7ddbbc, 1f4ae1e, c3594f5 | Done |
| 6 | "Upload the .ipynb" | `notebooks/*.ipynb` (all four, outputs kept) | final | 5f0abd5, a7ddbbc, c3594f5 | Done |
| 7 | "Upload detailed proposal (reflection journal) of what you accomplished; each team member talks about contribution in the contribution journal" | `docs/MTJournal_R_JosephClay_ITAI1371.pdf`, `docs/MTJournal_C_JosephClay_ITAI1371.pdf` | final | [fill] | Done |
| 8 | "Upload final clean dataset" | **`data/processed/stroke_clean_final.csv`** (train set after balancing; synthetic rows marked in `is_synthetic` only if chosen in D8) | **FINAL** | a7ddbbc | Done |
| 8 support | (not a Canvas item) | `data/processed/stroke_test_transformed.csv` (test set, transformed only, never balanced) | supporting | a7ddbbc | Done |

Raw data: `data/raw/healthcare-dataset-stroke-data.csv` (never edited; `data/raw/SHA256SUMS`).

## Balancing

Source: Prof Rao's guidance. Approval of this dataset was conditional on balancing `work_type`,
and in class on Oct 1, 2026, Prof Rao said to balance `work_type` with SMOTE. Balancing runs on
the TRAIN set only; the test set is never balanced.

I filled, encoded and scaled first, then ran plain SMOTE on work_type with k 5, sampling "auto" and
seed 33, after casting to float (D6, D7; ADRs 0006, 0007). Every group reached 2040 rows (nb04 cell
9). Blended 0/1 and one hot values were repaired, range checked and flagged with is_synthetic (D8;
ADR 0008).

## Decisions

All method choices are recorded as signed decision cards in `docs/decisions/` and as ADRs in
`docs/adr/`.

| Card | Question | My choice (fill after signing) | ADR |
|---|---|---|---|
| D1 | How to split 70/30 | plain random 70/30 split, seed 33, no stratify | 0001 |
| D2 | Rare categories and identifier columns | drop the gender Other row and id | 0002 |
| D3 | Missing values | median fill for bmi plus a bmi_missing flag | 0003 |
| D4 | Encoding the text columns | full one hot encoding, handle_unknown ignore | 0004 |
| D5 | Scaling and normalization | StandardScaler on age, avg_glucose_level, bmi | 0005 |
| D6 | Order of steps around SMOTE | fill, encode, scale, then SMOTE, train only | 0006 |
| D7 | SMOTE setup | plain SMOTE on work_type, k 5, auto, seed 33, float first | 0007 |
| D8 | Repair and checks after SMOTE | repair A, check C, scaled units, is_synthetic flag | 0008 |

## Working method

**Tools used:** Kiro CLI with a builder agent and the five project subagents (notebook-runner,
data-validator, work-verifier, repo-auditor, tutor-reviewer). I also used an AI assistant (Grok
Bot) to explain concepts and options.

**What AI did:**
* The Kiro builder agent wrote the Python code (notebook cells and functions) from the decisions I
  signed on the decision cards, and drafted the ADRs from those cards for me to review and save.
* Between my checkpoints, the notebook-runner, data-validator, work-verifier and repo-auditor ran
  the notebooks, checked them and each other, and wrote a one page summary for each checkpoint. At
  H2 they flagged two items for me: the builder read one file outside the project folder (a kernel
  settings file), and notebook 01 prints test shares. I kept the test shares because the D1 card's
  checks require them.
* At H3 the builder stopped and escalated because it had chosen a SMOTE input setting (cast to
  float first) that my D7 card left open. I reviewed both options and signed float first, so
  blended 0/1 values get rounded at 0.5 instead of being cut off.
* The tutor-reviewer explained concepts, like how a random seed works, and asked me questions.
* The AI assistant explained each data chart, recommended an option for D2 to D8 with pros and
  cons, and drafted the wording of my EDA observations and decision card text from the numbers in
  my notebooks.

**What I did:** I chose and signed every decision card, approved or corrected each checkpoint
summary, reviewed and edited every observation and card before saving it, set the decision values
in config.py, saved the ADRs, wrote both journals and the proposal, and made my own commits, pushes
and checkpoint tags.

**How I checked AI output:**
* The data-validator rechecked 84 claims in my EDA notes. It found 0 wrong but 3 that needed
  fixing: a vague bullet about id, a reference to "box 6" that didn't match any label, and a
  notebook title hidden by an HTML comment. I fixed all three (c17a968).
* When I filled in config.py, the ruff check stopped my commit because two lines were too long. I
  shortened them, and the decision slot tests passed 15 of 15 (ccc2dc4).

**Learning and preparation note:**
* Before building, I used a reference website as an all inclusive guide to understand the new
  concepts, mapped against the assignment criteria and made to fit my learning style. With that
  understanding, I built my own repo, made and signed every decision, and ran every notebook
  individually, so every number, decision and conclusion here comes from my own run. This project
  was also my chance to apply multi agent orchestration, which I learned from that reference, and I
  count it as part of my learning process and individual contribution.

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
