# Contribution journal (Canvas item 7)

**Canvas S7:** "Upload detailed proposal (reflection journal) of what you accomplished; each team member talks about contribution in the contribution journal"
**Canvas R4:** "Individual contribution: no entry minus 20, no participation minus 100"

## 1. My role

* This project was conducted individually. I carried out each method decision, reviewed and signed each checkpoint, wrote my interpretation, and directed, collaborated and asked clarifying question(tutor-reviewer-agent) with AI agents that implemented., ran and checked the codebase.

## 2. What I did, with proof

| Deliverable | What I did | Proof (file and commit hash) |
|---|---|---|
| 1 dataset URL document | Recorded the Kaggle source and URL for the stroke dataset | `docs/dataset_url.md`, 89193d0 |
| 2 one page proposal | wrote the one page proposal from my signed decisions. | `docs/MT_JosephClay_ITAI1371_Proposal.pdf`, 2d6c658 |
| 3 split notebook | Chose and signed the 70/30 split (D1: plain random, seed 33), then reviewed the split checks | `notebooks/01_load_split.ipynb`, D1 card 149de94, notebook 5f0abd5 |
| 4 EDA on train only | Wrote the observation under every chart and the findings cell, then fixed 3 points the data validator raised | `notebooks/02_eda_train.ipynb`, a24f16f, fixes c17a968 |
| 5 before and after notebooks | signed D2 to D8, ran notebooks 03 and 04, wrote all H3 notes, and asked for the stroke by work_type cell. | `notebooks/03_preprocess_before_after.ipynb`, `notebooks/04_smote_balance.ipynb`, a7ddbbc, 1f4ae1e, c3594f5 |
| 6 .ipynb files | Reviewed each notebook at its checkpoint | `notebooks/`, H1 78e6825, H2 ea395d1 |
| 7 journals | Wrote both journals | `docs/MTJournal_C_JosephClay_ITAI1371.pdf`, `docs/MTJournal_R_JosephClay_ITAI1371.pdf`, 2d6c658 |
| 8 final clean dataset | reviewed the final files and signed the integrity checks at H3. | `data/processed/stroke_clean_final.csv`, a7ddbbc |

## 3. Decisions I made

| Card | My choice (short) | ADR |
|---|---|---|
| D1 split | A: plain random 70/30, seed 33, no stratify | `docs/adr/0001-d1-split-plain-random-70-30.md` |
| D2 rows and columns | Remove the 1 gender "Other" row from train; drop id before modeling | `docs/adr/0002-d2-remove-other-row-drop-id.md`, 550d8a9 |
| D3 missing values | Fill bmi with the train median (28.1); add a `bmi_missing` flag first; keep smoking "Unknown" as a category | `docs/adr/0003-d3-median-fill-with-missing-flag.md`, 550d8a9 |
| D4 encoding | Full one hot with handle_unknown ignore; work_type encoded after SMOTE | `docs/adr/0004-d4-full-one-hot-encoding.md`, 550d8a9 |
| D5 scaling and normalization | StandardScaler on age, glucose and bmi; MinMax shown as the normalization exercise | `docs/adr/0005-d5-standard-scaler-on-number-columns.md`, 550d8a9 |
| D6 order around SMOTE | Fill, encode, scale, then plain SMOTE | `docs/adr/0006-d6-fill-encode-scale-then-smote.md`, 550d8a9 |
| D7 SMOTE setup | Plain SMOTE on work_type, k 5, "auto", random_state 33, columns cast to float first | `docs/adr/0007-d7-plain-smote-settings.md`, 550d8a9 |
| D8 after SMOTE and final file | Round 0/1 and argmax repair, both numeric checks, scaled units, `is_synthetic` flag | `docs/adr/0008-d8-repair-check-and-final-file.md`, 550d8a9 |

## 4. AI use disclosure

**Tools used:** Kiro CLI with a builder agent and the five project subagents (notebook-runner, data-validator, work-verifier, repo-auditor, tutor-reviewer). I also used an AI assistant (Grok Bot) to explain concepts and options.

**What AI did:**
* The Kiro builder agent wrote the Python code (notebook cells and functions) from the decisions I signed on the decision cards, and drafted the ADRs from those cards for me to review and save.
* Between my checkpoints, the notebook-runner, data-validator, work-verifier and repo-auditor ran the notebooks, checked them and each other, and wrote a one page summary for each checkpoint. At H2 they flagged two items for me: the builder read one file outside the project folder (a kernel settings file), and notebook 01 prints test shares. I kept the test shares because the D1 card's checks require them.
* At H3 the builder made the float change, and the work-verifier then raised it as escalation E3 for my review because it had chosen a SMOTE input setting (cast to float first) that my D7 card left open. I reviewed both options and signed float first, so blended 0/1 values get rounded at 0.5 instead of being cut off.
* The tutor-reviewer explained concepts, like how a random seed works, and asked me questions.
* The AI assistant explained each data chart, recommended an option for D2 to D8 with pros and cons, and drafted the wording of my EDA observations and decision card text from the numbers in my notebooks.

**What I did:** I chose and signed every decision card, approved or corrected each checkpoint summary, reviewed and edited every observation and card before saving it, set the decision values in config.py, saved the ADRs, wrote both journals and the proposal, and made my own commits, pushes and checkpoint tags.

**How I checked AI output:**
* The data-validator rechecked 84 claims in my EDA notes. It found 0 wrong but 3 that needed fixing: a vague bullet about id, a reference to "box 6" that didn't match any label, and a notebook title hidden by an HTML comment. I fixed all three (c17a968).
* When I filled in config.py, the ruff check stopped my commit because two lines were too long. I shortened them, and the decision slot tests passed 15 of 15 (ccc2dc4).

**Learning and preparation note:**
* Before building, I used a reference website as an all inclusive guide to understand the new concepts, mapped against the assignment criteria and made to fit my learning style. With that understanding, I built my own repo, made and signed every decision, and ran every notebook individually, so every number, decision and conclusion here comes from my own run. This project was also my chance to apply multi agent orchestration, which I learned from that reference, and I count it as part of my learning process and individual contribution.

## 5. Time log (optional)

| Date | Checkpoint | Hours | What |
|---|---|---|---|
| Before Oct 4 | Prep | Several sessions over multiple days | Learning the concepts with the midterm explainer, mapped to the assignment criteria |
| Before Oct 4 | H1 | Several sessions | Setting up the repo, the agents and protocols, and signing H1 |
| Sun Oct 4 | H2 to H4 | All day, into the evening | H2 to H4: EDA notes, signing D1 to D8, notebooks 03 and 04, ADRs, journals, submit |