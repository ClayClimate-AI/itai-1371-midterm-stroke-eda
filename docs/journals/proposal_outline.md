# One page proposal outline (Canvas item 2)

> OUTLINE AND PROMPTS ONLY. Write the proposal yourself, keep it to ONE page, and export to
> `docs/MT_JosephClay_ITAI1371_Proposal.pdf`. Write each section only after the notebook that
> supports it has run. The tutor-reviewer may review length and clarity only.

**Canvas S2:** "Upload pdf describing dataset and proposal, not more than a page"
**Canvas GL8:** "Discuss how you would use this dataset to solve an ML problem"

1. **Title line:** ITAI 1371 Midterm: Stroke Dataset EDA, Preprocessing and SMOTE. Joseph Clay, Oct
   4, 2026.
2. **Dataset (3 to 4 sentences):** Kaggle stroke prediction data (docs/dataset_url.md), 5110 rows
   by 12 columns, target stroke.
3. **What my EDA found (bullets):** bmi missing in 138 train rows and not at random, 1 gender Other
   row, only 13 Never_worked train rows, and stroke at 4.7% positive.
4. **What I did about each problem (bullets, in order):** plain random 70/30 split with seed 33;
   dropped the Other row and id; median fill for bmi plus a bmi_missing flag; full one hot encoding
   with handle_unknown ignore; StandardScaler on age, glucose and bmi; fill, encode, scale, then
   SMOTE on train only; plain SMOTE on work_type (k 5, seed 33, float first); repair, range check
   and an is_synthetic flag.
5. **Balancing:** per Prof Rao (Oct 1, 2026), I balanced on work_type. Every group went to 2040
   rows (nb04 cell 9), 6624 synthetic rows added.
6. **ML problem (2 to 3 sentences):** a stroke risk classifier, judged on the untouched test file
   with recall on stroke cases.
7. **Deliverables:** see the README table.
