# Stroke Prediction Dataset: EDA, Preprocessing and SMOTE Balancing

![Course](https://img.shields.io/badge/course-ITAI%201371%20Midterm-1f6feb)
![Checkpoints](https://img.shields.io/badge/checkpoints-H1%20to%20H4%20signed-2ea44f)
![Python](https://img.shields.io/badge/python-3.13%20%7C%203.14-3776ab?logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/notebooks-4-f37626?logo=jupyter&logoColor=white)
![Balancing](https://img.shields.io/badge/balancing-SMOTE%20on%20work__type-8250df)
![Tests](https://img.shields.io/badge/tests-64%20passed%2C%201%20skipped-2ea44f)
![Built with](https://img.shields.io/badge/built%20with-multi%20agent%20orchestration-ff6f00)
![Agents](https://img.shields.io/badge/Kiro%20CLI-builder%20%2B%205%20subagents-6e40c9)
[![CI](https://github.com/ClayClimate-AI/itai-1371-midterm-stroke-eda/actions/workflows/ci.yml/badge.svg)](https://github.com/ClayClimate-AI/itai-1371-midterm-stroke-eda/actions/workflows/ci.yml)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

A reproducible pipeline that takes the Kaggle stroke dataset from raw CSV to a balanced, model
ready train file and an untouched test file, built with multi agent orchestration.

**Student:** Joseph Clay (independent contributor) | **Course:** ITAI 1371 | **Due:** see Canvas

## Contents

[About](#about) · [Results](#results-at-a-glance) · [Quick start](#quick-start) ·
[Pipeline](#pipeline) · [Deliverables](#deliverables) · [Decisions](#decisions) ·
[Balancing](#balancing) · [How this was built](#how-this-was-built) ·
[Structure](#project-structure) · [Quality checks](#quality-checks) ·
[Submission](#submission)

## About

This repo takes the Kaggle stroke dataset (5110 rows) through EDA, preprocessing and SMOTE
balancing on work_type. Train was split 70/30 with seed 33 (3577 train, 1533 test, nb01). After
cleaning, encoding and scaling, SMOTE grew every work_type group to 2040 rows, giving a final train
file of 10200 rows by 23 columns (nb04 cells 9, 33). The test file was never balanced and has the
same 23 columns.

> Every decision was structured around remaining in control and in the loop at the appropriate entry pointa. A Kiro CLI builder
> agent wrote the code from my signed decision cards, and five subagents ran, checked and audited
> the work between four checkpoints that only I could sign. See
> [How this was built](#how-this-was-built).

> **Proof of work.** The commit history and the reports in `docs/reports/` record every step. Every
> number in this README points to the notebook cell that printed it. Steps are in
> [LAB_GUIDE.md](LAB_GUIDE.md).

## Results at a glance

| Measure | Value | Printed by |
|---|---|---|
| Raw dataset | 5110 rows × 12 columns | nb01 cell 6 |
| Train / test split | 3577 / 1533 (70/30, seed 33) | nb01 cell 13 |
| Missing values (train) | bmi only, 138 rows | nb02 cell 16 |
| Stroke share (train) | 4.7% | nb02 cell 19 |
| work_type after SMOTE | 2040 rows in every group | nb04 cell 9 |
| Synthetic rows added | 6624, marked in `is_synthetic` | nb04 cell 9 |
| Synthetic values outside real range | 0 (age, glucose, bmi) | nb04 cell 28 |
| Final train file | 10200 rows × 23 columns | nb04 cell 33 |
| Test file | 1533 rows × 23 columns, never balanced | nb04 cells 40, 41 |

## Quick start

Tested on Python 3.14 and 3.13 (CI runs both).

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/setup_gate.py           # environment check
python -m pytest -q                    # tests
jupyter lab                            # run notebooks 01 to 04 in order, Restart and Run All
python scripts/check_deliverables.py   # every Canvas file present
```

Full checklist: [VALIDATION_PROTOCOL.md](VALIDATION_PROTOCOL.md).

## Pipeline

Every value that is learned from data is learned from train only. The test set is transformed with
those train fitted objects, never fit and never balanced.

```text
raw CSV  5110 x 12
   │  nb01  split 70/30, seed 33 (D1)
   ├──▶ test  1533 x 12 ─────────────────────────────────────┐
   ▼                                                         │  transform only:
train  3577 x 12                                             │  never fit,
   │  nb02  EDA on train only                                │  never balanced
   │  nb03  drop Other row and id (D2), fill bmi + flag (D3),│
   │        one hot (D4), StandardScaler (D5), fit on train  │
   ▼                                                         │
prepared train  3576 x 18                                    │
   │  nb04  SMOTE on work_type (D6, D7), repair + checks (D8)│
   ▼                                                         ▼
final train  10200 x 23                      test transformed  1533 x 23
stroke_clean_final.csv                       stroke_test_transformed.csv
```

| Notebook | What it does |
|---|---|
| [`01_load_split`](notebooks/01_load_split.ipynb) | loads the raw CSV, splits 70/30 once, saves train and test |
| [`02_eda_train`](notebooks/02_eda_train.ipynb) | EDA on train only: 14 charts and my findings |
| [`03_preprocess_before_after`](notebooks/03_preprocess_before_after.ipynb) | D2 to D5 with before and after charts |
| [`04_smote_balance`](notebooks/04_smote_balance.ipynb) | SMOTE, repair, checks, final and test files |

## Deliverables

| # | Item | File | Commit | Status |
|---|---|---|---|---|
| 1 | Dataset URL | [`docs/dataset_url.md`](docs/dataset_url.md) | 89193d0 | Done |
| 2 | One page proposal | [Proposal PDF](docs/MT_JosephClay_ITAI1371_Proposal.pdf) | 2d6c658 | Done |
| 3 | 70/30 split in Python | [`01_load_split.ipynb`](notebooks/01_load_split.ipynb) | 5f0abd5 | Done |
| 4 | EDA on train only | [`02_eda_train.ipynb`](notebooks/02_eda_train.ipynb) | a24f16f<br>c17a968 | Done |
| 5 | Before and after | [`03_preprocess_before_after.ipynb`](notebooks/03_preprocess_before_after.ipynb)<br>[`04_smote_balance.ipynb`](notebooks/04_smote_balance.ipynb) | a7ddbbc<br>1f4ae1e<br>c3594f5 | Done |
| 6 | The .ipynb files | [`notebooks/`](notebooks/) (all four, outputs kept) | 5f0abd5<br>a7ddbbc<br>c3594f5 | Done |
| 7 | Journals | [Reflection journal PDF](docs/MTJournal_R_JosephClay_ITAI1371.pdf)<br>[Contribution journal PDF](docs/MTJournal_C_JosephClay_ITAI1371.pdf) | 2d6c658 | Done |
| 8 | **Final clean dataset** | [**`stroke_clean_final.csv`**](data/processed/stroke_clean_final.csv) | a7ddbbc | Done |
| 8+ | Test set (support) | [`stroke_test_transformed.csv`](data/processed/stroke_test_transformed.csv) | a7ddbbc | Done |

* Item 8 is the train set after balancing; synthetic rows are marked in `is_synthetic` (D8).
* Item 8+ is not a Canvas item: the test set, transformed only, never balanced.
* Raw data: `data/raw/healthcare-dataset-stroke-data.csv` (never edited; `data/raw/SHA256SUMS`).

<details>
<summary>Canvas item text (verbatim)</summary>

1. "Upload document showing URL of original dataset"
2. "Upload pdf describing dataset and proposal, not more than a page"
3. "In jupyter notebook use python to split dataset: training 70%, testing 30%; Python loads
   training data into memory; do not split manually or in excel"
4. "EDA performed only on training data; testing data untouched"
5. "Jupyter notebook demonstrating before and after data processing"
6. "Upload the .ipynb"
7. "Upload detailed proposal (reflection journal) of what you accomplished; each team member
   talks about contribution in the contribution journal"
8. "Upload final clean dataset"

</details>

## Decisions

Every method choice is a signed decision card in [`docs/decisions/`](docs/decisions/) with an ADR
in [`docs/adr/`](docs/adr/).

```text
D1  split ............ plain random 70/30 split, seed 33, no stratify ............ ADR 0001
D2  rows, columns .... drop the gender Other row and id ........................... ADR 0002
D3  missing values ... median fill for bmi plus a bmi_missing flag ................ ADR 0003
D4  encoding ......... full one hot encoding, handle_unknown ignore ............... ADR 0004
D5  scaling .......... StandardScaler on age, avg_glucose_level, bmi .............. ADR 0005
D6  order ............ fill, encode, scale, then SMOTE, train only ................ ADR 0006
D7  SMOTE setup ...... plain SMOTE on work_type, k 5, auto, seed 33, float first .. ADR 0007
D8  after SMOTE ...... repair A, check C, scaled units, is_synthetic flag ......... ADR 0008
```

One root cause note: [`docs/rca/0001-smote-int-truncation.md`](docs/rca/0001-smote-int-truncation.md).

## Balancing

Source: Prof Rao's guidance. Approval of this dataset was conditional on balancing `work_type`,
and in class on Oct 1, 2026, Prof Rao said to balance `work_type` with SMOTE. Balancing runs on
the TRAIN set only; the test set is never balanced.

I filled, encoded and scaled first, then ran plain SMOTE on work_type with k 5, sampling "auto" and
seed 33, after casting to float (D6, D7; ADRs 0006, 0007). Every group reached 2040 rows (nb04 cell
9). Blended 0/1 and one hot values were repaired, range checked and flagged with is_synthetic (D8;
ADR 0008).

## How this was built

This project was built with **multi agent orchestration**: one builder agent and five subagents
in Kiro CLI, each with one lane, working between four checkpoints that only I could sign.

```text
Joseph               decides, writes, signs, tags, pushes
│
├── builder          writes notebook cells and pipeline functions from signed cards
├── notebook-runner  runs notebooks in a fresh kernel; mechanical fixes only
├── data-validator   recomputes every number I wrote; leakage and integrity checks
├── work-verifier    checks the other agents against my cards and the role matrix
├── repo-auditor     fresh clone audits, run log, agent commits, checkpoint summary
└── tutor-reviewer   explains concepts and asks me questions; writes nothing
```

One checkpoint cycle, repeated for H1 to H4:

```text
Joseph    builder    runner    validator    verifier    auditor
  │ sign     │          │          │            │           │
  ├─────────▶│ build    │          │            │           │
  │          ├─────────▶│ run, fix │            │           │
  │          │          ├─────────▶│ check      │           │
  │          │          │          ├───────────▶│ check     │
  │          │          │          │            ├──────────▶│ audit, commit
  │◀─────────┴──────────┴──────────┴────────────┴───────────┤ H#_SUMMARY.md
  │ approve or correct, write, sign GATES.md, tag, push     │
```

Roles and rules: [`.kiro/steering/`](.kiro/steering/), [`.kiro/agents/`](.kiro/agents/),
[`.claude/agents/`](.claude/agents/). Run log: [`docs/reports/RUN_LOG.md`](docs/reports/RUN_LOG.md).
Checkpoint sign offs: [`docs/tracking/GATES.md`](docs/tracking/GATES.md).

### Working method

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
* At H3 the builder made the float change, and the work-verifier then raised it as escalation E3
  for my review because it had chosen a SMOTE input setting (cast to float first) that my D7 card
  left open. I reviewed both options and signed float first, so blended 0/1 values get rounded at
  0.5 instead of being cut off.
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

## Project structure

```text
.
├── data/
│   ├── raw/            original CSV + SHA256SUMS (never edited)
│   ├── interim/        train and test (nb01); prepared train and fitted objects (nb03)
│   └── processed/      final clean dataset + transformed test set (nb04)
├── notebooks/          01_load_split, 02_eda_train, 03_preprocess_before_after,
│                       04_smote_balance
├── src/stroke_prep/    config (facts + my decisions) and pipeline functions
├── tests/              environment, raw data and invariant tests
├── docs/
│   ├── decisions/      signed decision cards D1 to D8
│   ├── adr/            ADRs 0001 to 0008
│   ├── rca/            root cause notes
│   ├── journals/       reflection and contribution journals, proposal outline
│   ├── reports/        agent reports, RUN_LOG, checkpoint summaries H1 to H4
│   ├── tracking/       checkpoint sign offs (GATES.md)
│   └── specs/          Canvas requirements and notebook specs
├── scripts/            tooling (see Quality checks)
├── .kiro/              Kiro CLI agents and steering (house rules, checkpoints, role matrix)
└── .claude/            Claude Code agents and the role matrix
```

## Quality checks

Engineering extras, not graded; they support Documentation.

```text
python -m pytest -q             raw data, split, pipeline contract and final file invariants
scripts/check_raw_hash.py       raw CSV unchanged (SHA-256)
scripts/check_deliverables.py   every Canvas file present
scripts/compare_outputs.py      committed vs rerun notebook outputs
scripts/list_claims.py          every number in my prose, for the data-validator
scripts/check_commit_msg.py     commit message format
scripts/setup_gate.py           environment check
.pre-commit-config.yaml         nbstripout, ruff, raw hash, fast tests, commit message
.github/workflows/ci.yml        CI on Python 3.13 and 3.14, deliverables gate
```

At H4 a fresh clone with a new environment reran all four notebooks with matching outputs, and
`check_deliverables.py` reported all 11 files present (`docs/reports/H4_SUMMARY.md`). One test
skips by design: `id` was dropped at D2, so the id trace check has nothing to trace.

## Submission

Canvas text box line:

```text
https://github.com/ClayClimate-AI/itai-1371-midterm-stroke-eda
tag H4-signed (final commit is the latest on main)
final:  data/processed/stroke_clean_final.csv
test:   data/processed/stroke_test_transformed.csv
```

## Author

Joseph Clay, ITAI 1371. Individual project.

## License

MIT, see [`LICENSE`](LICENSE).
