# Reports

The agents save their work here. You read only two kinds of file:

* `H1_SUMMARY.md` to `H4_SUMMARY.md`: one page per checkpoint, made from
  `CHECKPOINT_SUMMARY_TEMPLATE.md`, with an approve or correct list. Start here.
* `RUN_LOG.md`: every change the agents made on their own between checkpoints, and every
  escalation waiting for you, kept by the repo-auditor. Skim it at each checkpoint.

Full reports behind each summary, one file per run, in one folder per agent, named
`<agent>/H<n>_<YYYYMMDD_HHMM>.md` (for example `data-validator/H2_20261005_1930.md`). The
folders keep report names apart from the summaries:

* `notebook-runner`: every notebook ran top to bottom in a clean kernel; errors; output changes.
* `data-validator`: every number in your prose recomputed from the data files; leakage and
  integrity checks; raw outputs of the decision cards' "how to test" checks.
* `work-verifier`: checks the agents, not you: every change since your last sign off against
  the specs, your decisions, the role matrix and the tests, with its own spot checks.
* `repo-auditor`: quick mode (tests, hashes, junk) or full mode (fresh clone, new venv, all
  notebooks rerun, Canvas uploads). The auditor also keeps RUN_LOG.md and writes the checkpoint
  summary, with the verifier section pasted verbatim.

A summary with any open FAIL, MISMATCH or escalation is not approved yet. Never edit a report by
hand; ask for a rerun instead.
