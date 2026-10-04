---
inclusion: always
---

# Role matrix (binding for the builder and all five agents)

Copied from `.claude/agents/README.md`, which stays the master copy. The five agents plus the
builder and Joseph each have one lane. **Exactly one owner per file type and action.**
In Kiro the builder is the `builder` agent (the main session); in Claude Code it is the main
session.

## Role matrix

| Actor | Owns (only this actor does it) | May edit or write | May read | Must never | Escalates when | Hands off to |
|---|---|---|---|---|---|---|
| **Joseph** | every decision (cards D1 to D8 and their reviews), every interpretation (his markdown cells, findings, before and after notes, ML use cell), ADRs, RCA notes, journals, proposal, README prose, `config.py` decision values, approve or correct ticks, sign offs, `H<n>-signed` tags, every push | anything | anything | edit `data/raw/` | n/a | agents, by prompt |
| **builder** (main session: the `builder` agent in Kiro) | creating NEW code cells, structural headings, empty placeholder cells `[Joseph writes here at H#]`, new function bodies in `src/stroke_prep/pipeline.py`, all from signed cards and specs | `notebooks/` (new code cells, headings, placeholders), `src/stroke_prep/pipeline.py` | repo | fill a placeholder, edit Joseph's text, cards, ADRs, journals, README, config values, tests, scripts, CI, requirements; commit; push | a needed decision is not on a signed card; a spec and a card disagree | notebook-runner (to run), Joseph (escalations) |
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

## How Kiro enforces the lanes

| Agent | Config | Write paths allowed | Enforcement |
|---|---|---|---|
| `builder` | `.kiro/agents/builder.json` | `notebooks/**`, `src/stroke_prep/pipeline.py` | allow rule for its lane only (no lane deny, because subagents inherit the builder's denies); shares `notebooks/` and `pipeline.py` with the runner (known shared write, checked by the work-verifier) |
| `notebook-runner` | `.kiro/agents/notebook-runner.json` | `notebooks/**`, `src/stroke_prep/pipeline.py`, `data/interim/**`, `data/processed/**`, `.nbrun/**`, `docs/reports/notebook-runner/**` | fs_write denied everywhere except its lane (V3); V2 deniedPaths list |
| `data-validator` | `.kiro/agents/data-validator.json` | `docs/reports/data-validator/**` | fs_write denied everywhere except its lane (V3); V2 deniedPaths list |
| `work-verifier` | `.kiro/agents/work-verifier.json` | `docs/reports/work-verifier/**` | fs_write denied everywhere except its lane (V3); V2 deniedPaths list |
| `repo-auditor` | `.kiro/agents/repo-auditor.json` | `docs/reports/repo-auditor/**`, `docs/reports/RUN_LOG.md`, `docs/reports/H*_SUMMARY.md`, `.gitignore` | fs_write denied everywhere except its lane (V3); V2 deniedPaths list |
| `tutor-reviewer` | `.kiro/agents/tutor-reviewer.json` | nothing | no write or shell tool; fs_write and shell denied |

Every agent, including the builder, also has these deny rules: writes to `data/raw/` and to
every file type Joseph owns (cards, tracking, journals, ADR, RCA, specs, tests, scripts, CI,
`.kiro/`, `.claude/`, requirements, `config.py`, README, guides); reading zip files; `git push`, `git tag`, `git remote`, `gh`, `curl`, `wget`; web
fetch and web search. The data-validator and work-verifier (read only except their own report
files in `docs/reports/<agent>/`) and the notebook-runner are also denied `git add`, `git commit` and other git write commands. Only the repo-auditor may run
`git add` and `git commit`.

Kiro passes the builder's deny rules down to every agent it starts (deny wins), so the builder
holds only the rules that bind everyone. The rest of the builder's lane (never fill a
placeholder, never edit Joseph's files, never commit) is a rule in this steering, checked by the
work-verifier at every checkpoint.

What Kiro enforces and what it does not: in V3 the file tools are limited per helper by the
rules above. The builder's lane is only partly enforced (allow rule, shared denies), and shell
commands are not path checked by Kiro, so a script could still write anywhere. Both are checked
by the work-verifier from the git diff, not enforced.
