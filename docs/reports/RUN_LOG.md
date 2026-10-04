# Run log

Only the repo-auditor writes this file. It appends one entry per change or escalation found in
the other agents' reports (and its own). Newest at the bottom. Joseph skims this at each
checkpoint. Earlier entries are never deleted or rewritten.

```text
#<n>  <date time CT>  <agent>  since <checkpoint>
Type:    BUILD (builder) | FIX (mechanical, notebook-runner) | RERUN | ESCALATION
What:    <one line>
Why:     <error text or check that failed>
Files:   <paths>
Change:  <before -> after, or "none, waiting for Joseph">
Rule:    <for ESCALATION: decision not recorded | unexplained mismatch | data handling change | interpretation text>
Commit:  <hash or "uncommitted">
```

(entries start below)
