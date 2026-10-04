# Builder loop PIOF log
**[Engineering extra, not graded]**

Optional. Use a PIOF block when you direct Claude or Kiro to build something specific (a chart you want,
a fix you asked for): Problem, Input, Output, Fix/verify. The "Fix/verify" line names a CHECK (an
assert or a printed property), never an expected number. Agent work between checkpoints is logged
in `docs/reports/RUN_LOG.md` instead.

```text
PIOF  checkpoint H#  notebook cell [n]
Problem:     (what is missing, in your words)
Input:       (file or frame going in)
Output:      (what the cell must print or draw)
Fix/verify:  (the check that proves it worked, for example "parts add up to the raw row count")
Result:      PASS / FAIL (date)
```

## H1 Kickoff
## H2 After EDA (notebooks 01 and 02)
## H3 After prep and SMOTE (notebooks 03 and 04)
## H4 Final
