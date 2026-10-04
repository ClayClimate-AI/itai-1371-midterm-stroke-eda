# Commit plan
**[Engineering extra, not graded]**

The `commit-msg` hook checks `type(scope): subject  [H#]` (subject 72 characters or fewer; the tag
is optional). Only the repo-auditor commits agent work, locally, with scope `agent`, logged in
`docs/reports/RUN_LOG.md`; no agent pushes. Everything you write is committed by you, with your
own scope. After each sign off: `git tag H<n>-signed` and push with `--tags`. Fill in your own details; never write a result you have not seen.

| # | Checkpoint | Who | Suggested message | Hash |
|---|---|---|---|---|
| 1 | H1 | Joseph | `chore: scaffold repo from starter kit v5.1` | |
| 2 | H1 | Joseph | `docs(decisions): record decisions D1 to D8  [H1]` | |
| 3 | H1 | Joseph | `docs(reports): H1 summary approved  [H1]` | |
| 4 | H2 | agents | `feat(agent): notebook 01 load and split per D1  [H2]` | |
| 5 | H2 | agents | `feat(agent): notebook 02 charts on train  [H2]` | |
| 6 | H2 | agents | `docs(agent): H2 reports and summary  [H2]` | |
| 7 | H2 | Joseph | `docs(nb02): my EDA observations and findings  [H2]` | |
| 8 | H2 | Joseph | `docs(adr): ADR 0001 and D1 review  [H2]` | |
| 9 | H3 | agents | `feat(agent): notebook 03 prep per D2 to D6  [H3]` | |
| 10 | H3 | agents | `feat(agent): notebook 04 SMOTE and repair per D7, D8  [H3]` | |
| 11 | H3 | agents | `data(agent): final dataset and transformed test set  [H3]` | |
| 12 | H3 | agents | `docs(agent): H3 reports and summary  [H3]` | |
| 13 | H3 | Joseph | `docs(nb04): my before and after notes  [H3]` | |
| 14 | H3 | Joseph | `docs(adr): ADRs 0002 to 0008 and card reviews  [H3]` | |
| 15 | H4 | Joseph | `docs(journal): proposal and journals  [H4]` | |
| 16 | H4 | Joseph | `docs(readme): summary and working method  [H4]` | |
| 17 | H4 | agents | `docs(agent): H4 full audit and summary  [H4]` | |
| 18 | H4 | Joseph | `chore: final submission  [H4]` | |

Fix commits between checkpoints (made by the repo-auditor): `fix(agent): <what>  [H#]` plus a
RUN_LOG entry.
