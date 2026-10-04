# Agents: role matrix and conflict check

This file is documentation, not an agent (it has no frontmatter). Every agent reads it first.
The five agents plus the builder (the main Claude Code session) and Joseph each have one lane.
**Exactly one owner per file type and action.**

## Role matrix

| Actor | Owns (only this actor does it) | May edit or write | May read | Must never | Escalates when | Hands off to |
|---|---|---|---|---|---|---|
| **Joseph** | every decision (cards D1 to D8 and their reviews), every interpretation (his markdown cells, findings, before and after notes, ML use cell), ADRs, RCA notes, journals, proposal, README prose, `config.py` decision values, approve or correct ticks, sign offs, `H<n>-signed` tags, every push | anything | anything | edit `data/raw/` | n/a | agents, by prompt |
| **builder** (main Claude session) | creating NEW code cells, structural headings, empty placeholder cells `[Joseph writes here at H#]`, new function bodies in `src/stroke_prep/pipeline.py`, all from signed cards and specs | `notebooks/` (new code cells, headings, placeholders), `src/stroke_prep/pipeline.py` | repo | fill a placeholder, edit Joseph's text, cards, ADRs, journals, README, config values, tests, scripts, CI, requirements; commit; push | a needed decision is not on a signed card; a spec and a card disagree | notebook-runner (to run), Joseph (escalations) |
| **notebook-runner** | executing notebooks in the working copy; MECHANICAL fixes to code cells and `src/stroke_prep/pipeline.py`; saving executed notebooks; the data files those runs write | code cells, `src/stroke_prep/pipeline.py` (mechanical only), executed notebooks, `data/interim/`, `data/processed/`, `.nbrun/`, its own report | repo | markdown cells, cards, ADRs, journals, README, config, tests, scripts, CI, requirements, `.gitignore`, RUN_LOG, summary, other reports, `data/raw/`; change data handling; weaken a check; commit; push | decision not recorded; fix would change data handling; would touch interpretation text; failure not fixable after two tries | repo-auditor (log and commit), Joseph |
| **data-validator** | recomputing every number in Joseph's prose; running the cards' "how to test" checks (raw outputs); leakage and integrity checks | its own report only | repo | every other file; interpret; supply expected values | unexplained MISMATCH; notebook differs from signed card; a check needs a decision | notebook-runner (stale outputs), Joseph (text mismatches) |
| **work-verifier** | checking the OTHER agents' work: RUN_LOG entries and the git diff since the last sign off, against specs, decisions, this matrix, tests and VALIDATION_PROTOCOL, with its own spot checks | its own report only | repo, its clones in `scratch/clones/` | every other file; fix, revert, stage, commit, tag, push; judge Joseph's writing or decisions; trust other reports without rechecking | everything it flags goes to Joseph by design; `NOT VERIFIED` when a check cannot run | repo-auditor (its section is pasted verbatim into the summary) |
| **repo-auditor** | reproducibility audit (quick and full); `RUN_LOG.md`; `H<n>_SUMMARY.md`; local commits of agent work; `.gitignore` junk entries | its own report, `RUN_LOG.md`, `H<n>_SUMMARY.md`, `.gitignore` | repo, its clones in `scratch/clones/` | notebooks, `src/`, tests, scripts, config, CI, requirements, Joseph's files, other reports, `data/`; run `ruff --fix`; edit the verifier section; pre tick a box; push | clone fails for a non mechanical reason; secret, large file or reference material found; tests or scripts need a change | notebook-runner (code and lint in src or notebooks), data-validator (claims), Joseph (summary) |
| **tutor-reviewer** | explaining concepts; asking Joseph questions; reviewing his drafts for gaps | nothing (read only) | repo | write any file; decide; write conclusions or example sentences about this dataset | n/a | data-validator (is my number right), work-verifier (did an agent do something wrong) |

## Ownership by file type and action

| File type or action | Single owner | Everyone else |
|---|---|---|
| Decision cards, reviews, `config.py` decision values | Joseph | read |
| `docs/tracking/` (GATES sign off log, progress, checkpoints, PIOF, TRACEABILITY evidence, COMMIT_PLAN hashes) | Joseph | read |
| Kit templates (`docs/reports/README.md`, `CHECKPOINT_SUMMARY_TEMPLATE.md`, ADR and RCA templates), `CLAUDE.md`, `LAB_GUIDE.md`, `VALIDATION_PROTOCOL.md`, specs | Joseph (agents escalate) | read |
| Markdown cells with interpretation, journals, ADRs, RCA, proposal, README prose | Joseph | read |
| New notebook files, new code cells, headings, placeholders, new function bodies | builder | read (see known shared write below) |
| Mechanical fixes to existing code cells and `pipeline.py` | notebook-runner | read; report problems |
| Executing notebooks in the working copy, writing `data/interim` and `data/processed` | notebook-runner | auditor and verifier rerun only inside their clones in `scratch/clones/` |
| `tests/`, `scripts/`, `requirements.txt`, `pyproject.toml`, `.pre-commit-config.yaml`, `.github/`, `.claude/`, `.kiro/`, config facts | Joseph (agents escalate) | read |
| `docs/reports/<agent>/H<n>_<YYYYMMDD_HHMM>.md` (one folder per agent, so no report name can match a summary) | the agent named in the folder | read |
| `docs/reports/RUN_LOG.md` | repo-auditor | read |
| `docs/reports/H<n>_SUMMARY.md` (verifier section copied verbatim) | repo-auditor | read |
| `.gitignore` junk entries | repo-auditor | read |
| `.nbrun/` scratch in the working copy | notebook-runner | auditor and verifier use their clones |
| `scratch/clones/<agent>_H<n>_<YYYYMMDD_HHMM>/` (git ignored clone of HEAD inside the repo folder) | repo-auditor and work-verifier, each only its own clone folders | never write; nobody deletes clones except Joseph |
| `git commit` of agent work | repo-auditor | never commit |
| `git commit` of Joseph's work, `git push`, tags | Joseph | never |
| Approve or correct ticks, sign off | Joseph | never |
| `data/raw/` | nobody (read only) | read |

### Known shared write: `notebooks/` and `src/stroke_prep/pipeline.py`

The builder and the notebook-runner both need write access to these two paths. The split is by
ACTION (builder creates new cells and functions; runner makes mechanical fixes to existing ones),
and neither Claude Code nor Kiro can enforce a split by action: Kiro's documented `fs_write`
rules match paths only, with no "create new file only" option. Both tools therefore allow both
agents to write these paths. Enforcement is the work-verifier: at every checkpoint it compares
the git diff with RUN_LOG (BUILD entries for the builder, FIX entries for the runner) and flags
`OUT OF LANE` for a builder edit to an existing cell or a runner change that adds new analysis.

## Order at each checkpoint

```text
builder builds → notebook-runner runs and fixes → data-validator checks
  → work-verifier checks the agents → repo-auditor audits, logs, commits, writes H<n>_SUMMARY.md
  → Joseph approves or corrects, signs, tags H<n>-signed, pushes
```

## Conflict check (done when this kit was built, Oct 3, 2026; rechecked for v5.1 with the Kiro files)

Checked across the five agent files, this README, `CLAUDE.md`, `.claude/settings.json`, and for
v5.1 the six `.kiro/agents/*.json` files, their prompts in `.kiro/prompts/` and `.kiro/steering/`:

| # | Found | Fixed by |
|---|---|---|
| 1 | Three agents could append to `RUN_LOG.md` (shared write) | Only the repo-auditor writes it; the others record fixes and escalations in their own reports |
| 2 | Three agents could make local commits | Only the repo-auditor commits, and only agent work |
| 3 | repo-auditor could run `ruff --fix` on `src/`, overlapping notebook-runner code edits | Auditor reports lint; notebook-runner fixes `src/`; tests and scripts are escalated |
| 4 | Builder and notebook-runner both edit code cells | Split by action: builder creates new cells from cards; runner makes mechanical fixes only |
| 5 | Nobody owned `tests/`, `scripts/`, CI, requirements | Joseph owns them; every agent escalates; the verifier flags any change |
| 6 | Nobody owned writing the data files | notebook-runner, through notebook execution only |
| 7 | Auditor quick mode executed notebooks in the working copy, which rewrites data files the runner owns | Auditor and verifier rerun only inside their clones in `scratch/clones/`; read only agents run pytest with `-p no:cacheprovider` so they write nothing |
| 8 | Nobody checked the agents themselves | work-verifier added; its section goes verbatim into the summary |
| 9 | Placeholder cells: builder creates them, Joseph fills them | builder never fills one; verifier flags `INTERPRETATION TOUCHED` if an agent does |
| 10 | Escalation route unclear for read only agents | Validator and verifier escalate in their reports; the auditor carries every escalation to the summary |
| 11 | Commit hook allowed only gate tags G0 to G7 | Hook now accepts `[H1]` to `[H4]` |
| 12 | The builder writes no report, so its work had no RUN_LOG entry | The builder lists what it built in its reply; the repo-auditor logs a BUILD entry per notebook or function from the git diff; the verifier checks it |
| 13 | Nobody owned `docs/tracking/`, the kit templates and the guides | Joseph owns them; agents escalate |
| 14 | Read only lanes for the validator and verifier rely on the prompt (Claude Code cannot limit Write to one path) | Prompt rules plus deny rules in `.claude/settings.json` (Joseph's file types, the same list Kiro denies: cards, tracking, journals, ADRs, RCA, specs, `config.py`, tests, scripts, CI, requirements, guides, raw data, `.claude/`, `.kiro/`; zip reads; web search and fetch; push, tag, remotes, `gh`, `curl`, `wget`) and `blockReadsOutsideWorkingDirectories`, which keeps the file tools inside the repo folder wherever it sits; the verifier's diff check catches any write outside a lane |
| 15 | The old deny list named fixed home folders (`~/Downloads`, `~/Documents/...`), which blocked the agents whenever the repo itself sat in one of them | Rules are now relative to the repo (v5.1): Claude Code blocks reads outside the working folder; Kiro allows workspace reads and asks for anything outside |
| 16 | Kiro copy of the lanes (v5.1): Kiro passes the orchestrator's deny rules down to every subagent, so a builder lane deny would also block the runner and auditor | The `builder` agent carries only the denies that bind everyone (Joseph's files, raw data, push, tag, remote, web, zips); each subagent denies all writes outside its own lane; the builder's finer limits stay in steering and are checked by the work-verifier |
| 17 | Kiro shell commands are not path checked, so a script could write outside a lane | Steering forbids working around a denial; read only agents are denied git write commands; the verifier's diff check is the backstop |
| 18 | The pre-commit hook ran `ruff check --fix`, so a commit by the repo-auditor could change code in `src/` | Hook now reports only (`--no-fix`); the notebook-runner fixes lint in its lane |
| 19 | Report names like `H2_<agent>_*.md` in one folder could not be told apart by a path rule, and clones went to `/tmp`, outside the project folder | Each agent writes reports only in `docs/reports/<agent>/`; the verifier and auditor clone into `scratch/clones/` inside the repo (git ignored, never deleted); the builder and runner share `notebooks/` and `pipeline.py` by design (see Known shared write) |
