# LAB GUIDE v5.1: ITAI 1371 Midterm, Stroke Dataset EDA

Joseph Clay, individual work. This guide tells you WHAT to do and HOW to check it. It never tells
you what you will find. Every number, decision and conclusion in your repo comes from your own
run.

## 0. The idea in plain words

You have a big table of patients. You will:

1. Cut it into a practice pile (train, 70%) and a locked test pile (test, 30%).
2. Look closely at the practice pile only, with charts, and write down what you notice.
3. Clean the practice pile: deal with odd rows, blanks, and words that a computer cannot do math on.
4. Even out the `work_type` groups with SMOTE (Prof Rao's guidance), which makes new pretend rows
   that look like real ones. You decide (card D8) whether a column marks which rows are pretend.
5. Save the clean file and write up what you did and why.

In real terms: a 70/30 split in Python, EDA on train only, imputation, encoding, scaling and
normalization, then SMOTE oversampling of `work_type` on train only, with before and after charts.

## 1. Who writes what

* **You:** every decision card (all at H1), every markdown cell that explains an output, every ADR,
  the journals, the proposal, the README prose. You approve or correct at each checkpoint, and you
  push.
* **The AI (Claude Code or Kiro CLI) and the agents:** Python code built from your signed cards, running, checking and
  fixing mechanical problems on their own between checkpoints, and a one page summary for you at
  each checkpoint. They never write a result or a conclusion and never pick a method for you.
* **Subagents** (in `.claude/agents/` for Claude Code and `.kiro/agents/` for Kiro):
  `notebook-runner`, `data-validator`, `repo-auditor`, `work-verifier`, `tutor-reviewer`. Who
  owns what is in `.claude/agents/README.md` (Kiro copy: `.kiro/steering/03-role-matrix.md`);
  the `work-verifier` checks the other agents, not you.

## 2. The flow

```text
H1 Kickoff (you): approve setup, sign ALL cards D1..D8, push
 │
 │  agents: notebook 01 (split) + notebook 02 (EDA charts)
 │          run, check, fix, log
 ▼
H2 After EDA (you): read one page, approve or correct,
 │                  write your EDA observations, review D1
 │
 │  agents: notebook 03 (clean, encode, scale) + notebook 04 (SMOTE)
 │          final files, run, check, fix, log
 ▼
H3 After prep and SMOTE (you): read one page, approve or correct,
 │                             write before and after notes, ADRs
 │
 │  agents: check every number you wrote, fresh clone audit
 ▼
H4 Final (you): journals, proposal, README, definition of done, submit
```

Four checkpoints. At each one you read `docs/reports/H#_SUMMARY.md` (one page, with a verifier
section that checks the agents) and skim `docs/reports/RUN_LOG.md`. Green tests alone never count
as done.

## 3. When the agents stop and ask you

Between checkpoints the agents fix mechanical problems on their own (errors, paths, formatting,
test failures caused by code) and log each change. They stop and wait for you only when:

1. a decision is needed that is not on a signed card,
2. the validator finds a mismatch they cannot explain,
3. a fix would change how the data is handled,
4. something touches your writing.

You will see these under "Waiting for you" in the summary, and as ESCALATION in the run log.

Writing rules for your markdown and documents:

* Every number you type must be visible in a cell output above it. Name the cell: "cell [7]".
* Say what you see first, then what you think it means, then how sure you are.
* Short sentences. No dashes or hyphens in prose.
* If a number changes after a rerun, the validator flags it; update your text.

## 4. Claude Code or Kiro CLI: start and pick a helper

Both tools use the same rules, the same five helpers and the same checkpoints. Pick one per
session. Your project folder is `itai-1371-midterm-stroke-eda` in Downloads (the same name as
the GitHub repo), open in the Kiro IDE with File, Open Folder. The IDE terminal starts in the
repo root, so every command and path in this guide is relative to that folder; no `cd` needed.
In each new terminal, run `source .venv/bin/activate` first.

**Claude Code** reads `CLAUDE.md` and `.claude/agents/`:

```bash
source .venv/bin/activate
claude
```

Ask for a helper by name ("Use the `data-validator` subagent for H2") or with `@agent-` and its
name.

**Kiro CLI** reads `.kiro/steering/` (the house rules) and `.kiro/agents/` (six agents: the five
helpers plus `builder`, which plays the main Claude session). Commands from the Kiro docs:

```bash
source .venv/bin/activate
kiro-cli --version                       # if "command not found", see below
kiro-cli agent list                      # should list builder and the five helpers
kiro-cli chat --v3 --agent builder       # start the builder with the V3 engine
```

* No `kiro-cli` yet? The Kiro IDE does not include it. Install it once yourself, before you
  start any helper, with the line from the Kiro docs:
  `curl -fsSL https://cli.kiro.dev/install | bash`. Open a new terminal, activate `.venv`, and
  run `kiro-cli` to sign in. The helpers are never allowed to run `curl`; this is for you only.
* What Kiro enforces: in V3 each helper's file tools are limited to its own lane. The builder's
  lane and all shell commands are not enforced by Kiro; the `work-verifier` checks them at
  every checkpoint.

* First start: Kiro asks whether you trust the workspace. Choose trust, or it loads no agents
  and no rules.
* Type `/model` once and pick Claude Opus 5.5, then `/model set-current-as-default`. The agents
  keep your choice. Opus 5.5 has a 2.0x credit multiplier (Pro plan or higher).
* In the Kiro IDE: Terminal, New Terminal opens in the project folder; run the `kiro-cli`
  commands there. That is the main path. If you use the IDE chat panel instead: trust the
  workspace, pick `builder` in the agent picker (or type `/builder`), pick Claude Opus 5.5 in
  the model picker, and use Supervised mode, not Autopilot. Only the `permissions` rules apply
  there, helper handoffs may run in the background as Workflows, and `/model`,
  `/model set-current-as-default`, `/agent swap` and Ctrl+G are CLI only.
* Hand work to a helper from the builder chat: "Use the `data-validator` agent to check notebook
  02 for H2." The builder may run them one after another in the checkpoint order.
* Or switch the chat itself: `/agent swap tutor-reviewer`, and back with `/agent swap builder`.
  `/agent list` shows them all. Start one directly with
  `kiro-cli chat --v3 --agent tutor-reviewer`. In V3 the helpers run in the background and the
  docs say the monitor was simplified, so Ctrl+G may show little; ask the builder which helpers
  are running.
* Approve a Kiro prompt only when the file is in that helper's lane. Say no to anything outside
  the project folder; the helpers' test clones go in `scratch/clones/`, inside it. A "denied"
  message means the rules stopped a helper leaving its lane.
* In the prompts below, "subagent" works the same in Kiro: write "Use the `work-verifier` agent".
  Where a prompt says "the escalation reasons in CLAUDE.md", Kiro has the same list in
  `.kiro/steering/02-checkpoints-and-escalation.md`.

## 5. Checkpoint by checkpoint

### H1 Kickoff (about 2 hours)

1. Setup in the IDE terminal, which starts in the repo root (your Mac has Python 3.14; the kit
   is tested on 3.14 and 3.13):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name stroke-eda --display-name "stroke-eda"
python scripts/setup_gate.py
python scripts/check_raw_hash.py
python -m pytest -q
```

2. Make commit 1, connect your GitHub repo (it already exists and is empty), push, and check
   that CI runs (GitHub, Actions tab). You push and tag yourself; the agents never do. Before
   the first commit: if macOS offers the Xcode Command Line Tools, install them. Check
   `git config --global user.name` and `git config --global user.email`; if either is blank,
   set it with `git config --global user.name "Joseph Clay"` (and your GitHub email). The
   first push asks for a password: use a GitHub Personal Access Token with Contents and
   Workflows set to read and write for this repo, or run `gh auth login` first if you have
   `gh`.

```bash
git init
pre-commit install --hook-type pre-commit --hook-type commit-msg
git add .
git commit -m "chore: scaffold repo from starter kit v5.1"
git branch -M main
git remote add origin https://github.com/ClayClimate-AI/itai-1371-midterm-stroke-eda.git
git push -u origin main
```

3. Decisions, in one sitting. Read `docs/decisions/README.md`, then every card D1 to D8. For each,
   fill "My decision": the option, why in your words, and your source (module, lecture, library
   documentation, Prof Rao with date). Sign. Then copy each value into its slot in
   `src/stroke_prep/config.py`: D1 (`SPLIT_SEED`, `STRATIFY_ON`), D3 (`IMPUTE_STRATEGY`,
   `ADD_MISSING_FLAG`), D4 (`ONEHOT_DROP_FIRST`), D5 (`SCALER`, `SCALE_COLUMNS`), D7
   (`SMOTE_VARIANT`, `SMOTE_K_NEIGHBORS`, `SMOTE_SAMPLING_STRATEGY`, `SMOTE_RANDOM_STATE`), D8
   (`REPAIR_RULE`, `NUMERIC_CHECK`, `FINAL_NUMERIC_UNITS`, `FLAG_SYNTHETIC`). Every slot starts
   as `None`; the tests in `tests/test_decision_slots.py` skip a blank slot and name its card. If you want a
   concept explained:
   > Use the tutor-reviewer subagent to explain the options on card D5 simply, then ask me
   > questions. Do not recommend one.
4. Ask for the setup report:
   > Use the data-validator on docs/dataset_url.md and my signed cards, then the work-verifier,
   > then the repo-auditor in full mode for H1 to write H1_SUMMARY.md.
5. Read the one page. Tick approve or write a correction. Sign H1 in `docs/tracking/GATES.md`.
   Commit, then `git tag H1-signed`, then `git push --tags` and `git push`.

### Between H1 and H2 (agents)

Start the run:
> Build notebooks 01 and 02 from the specs in docs/specs and my signed cards. Leave a
> placeholder markdown cell wherever I need to write. Then loop notebook-runner and
> data-validator until clean, then run the work-verifier, then the repo-auditor in quick mode to
> log, commit agent work and write H2_SUMMARY.md. Stop only for the escalation reasons in CLAUDE.md.

What notebook 02 must cover is in `docs/specs/nb02_eda_train.md`. If you want specific charts,
say so in the prompt. The chart menu:

Chart menu (pick what answers your questions; each chart needs a title and labeled axes):

| Chart | Good for |
|---|---|
| Bar chart of missing values per column | where blanks are |
| Bar chart of counts per category | size of each group, rare groups |
| Bar chart of the target rate per category | comparing groups on the target |
| Histogram | shape of one numeric column |
| Box plot, overall or by group | spread and unusual values |
| Scatter plot | two numeric columns together |
| Correlation heatmap | numeric relationships at a glance |

### H2 After EDA (about 2 to 3 hours, mostly your writing)

1. Read `docs/reports/H2_SUMMARY.md` and skim the run log. Approve or correct each line. Answer
   any escalation.
2. Open notebook 02 in Jupyter. Under each chart, in the placeholder cell, write what you see
   (with numbers from the printed output), what it might mean, and what you are not sure about.
   Fill the findings cell: each data problem you found and which card (D2 to D8) handles it.
3. Card D1: fill "Review at H2" (keep or amend, and why). Write ADR 0001.
4. Ask:
   > Run data-validator on my notebook 02 markdown, then the repo-auditor to update H2_SUMMARY.md.
   Fix any MISMATCH in your text. Sign H2. Commit, `git tag H2-signed`, push with tags.

### Between H2 and H3 (agents)

> Build notebooks 03 and 04 from the specs and my signed cards D2 to D8. Fit on train only,
> transform test only, never balance test. Show before and after outputs and charts. Save the
> final file and the transformed test file. Leave placeholders for my writing. Loop
> notebook-runner and data-validator until clean, then work-verifier, then repo-auditor to write
> H3_SUMMARY.md.

### H3 After prep and SMOTE (about 2 to 3 hours, mostly your writing)

1. Read `docs/reports/H3_SUMMARY.md`: before and after tables, reconciliation, integrity checks
   after SMOTE, the card check outputs. Approve or correct each line.
2. Cards D2 to D8: fill "Review at H3". Any amendment means the agents rebuild and you get a new
   summary.
3. In notebooks 03 and 04, write your notes in the placeholders. Compare each column before and
   after each step; describe what you see and why. Last cell of notebook 04: how you would use
   this dataset for an ML problem in the Final.
4. Write ADRs 0002 to 0008. Ask for a validator pass on your text. Sign H3. Commit,
   `git tag H3-signed`, push with tags.

### H4 Final (about 2 to 3 hours)

1. Write the one page proposal (`docs/journals/proposal_outline.md` then PDF), the reflection
   journal, the contribution journal (edit the AI use note in your own words), the README summary
   and working method. Export PDFs with the exact names in the README table.
2. Ask:
   > Use the tutor-reviewer subagent to review my proposal and journals for missing parts and
   > unclear claims. Do not rewrite them.

   > Run data-validator on README, docs and journals for H4, then the work-verifier, then the
   > repo-auditor in full mode to write H4_SUMMARY.md.
3. Read the page, fix every MISMATCH in your text, tick the definition of done (section 7), sign
   H4, `git tag H4-signed`, push with tags, paste the Canvas line.

## 6. Troubleshooting (general)

| Message or symptom | What it usually means | What to do |
|---|---|---|
| `ModuleNotFoundError` | the notebook kernel is not your venv | pick the `stroke-eda` kernel |
| `FileNotFoundError` for a data file | an earlier notebook has not run, or the path is wrong | run notebooks in order; use paths from `config.py` |
| `could not convert string to float` | a text column reached a step that needs numbers | check the order in card D6 |
| SMOTE says `n_neighbors` is larger than the samples | a class has fewer rows than k plus one | look at your own counts, revisit card D7 |
| Kiro lists no agents, or ignores the rules | the workspace is not trusted, or Kiro started outside the project folder | start Kiro inside the project folder and choose trust |
| Kiro says a write or command is denied | a helper tried to leave its lane | expected; read its ESCALATION and decide |
| raw hash check FAILS | the raw CSV changed | `git checkout data/raw/` and never edit it |
| a test FAILS | an invariant broke | agents fix code causes; a decision cause comes to you as an escalation |
| validator says MISMATCH | your text and your data disagree | fix your text, or answer the escalation if the code is wrong |
| auditor says outputs differ on rerun | something is not repeatable | the agents check seeds and cell order; if a seed is missing, it is a decision for you (D1, D7) |

## 7. Definition of done (Canvas mapping)

| Canvas | Done when |
|---|---|
| S1 dataset URL | `docs/dataset_url.md` committed |
| S2 one page proposal PDF | PDF in `docs/`, one page, your words |
| S3 split in Python | notebook 01 ran, split invariant tests pass, D1 signed and reviewed |
| S4 EDA on train only | notebook 02 never names the test file, findings in your words |
| S5 before and after notebooks | notebooks 03 and 04 show before and after outputs and charts |
| S6 the .ipynb files | all four committed with outputs, run top to bottom |
| S7 journals | both PDFs committed, your words, AI use disclosed |
| S8 final clean dataset | `data/processed/stroke_clean_final.csv`, invariant tests pass |
| S9 GitHub URL | pushed, H4 summary approved, URL pasted in Canvas |
| S10 raw untouched | raw hash check passes |

Checklist with commands: `VALIDATION_PROTOCOL.md`.
