# Decision cards

Every method choice in this project is yours. Each card below asks one question, lists options
with neutral pros and cons, and shows how to test the choice on YOUR training data. Nothing on a
card tells you which option to pick or what result to expect.

## Fixed by the assignment or the instructor (not decisions)

* Canvas S3: "In jupyter notebook use python to split dataset: training 70%, testing 30%; Python loads training data into memory; do not split manually or in excel"
* Canvas S4: "EDA performed only on training data; testing data untouched"
* Canvas GL4: "NEVER EVER change the dataset manually. If you do this you have failed the exam. All changes to be done via Python code in Jupyter lab."
* Prof Rao's guidance: the dataset was approved on the condition that work_type is balanced, and in class on Oct 1, 2026 Prof Rao said to balance work_type with SMOTE. Cite it as "Prof Rao, in class, Oct 1, 2026".
* Leakage rule (general ML practice, used in Modules 4 and 5): anything learned from data is learned from train only, and the test set is transformed with what train learned. The test set is never balanced.

## The cards

| Card | Question | Reviewed at | ADR it feeds |
|---|---|---|---|
| [D1](D1_split.md) | How exactly do I split 70/30 (stratify? on what? which seed?) | H2 | 0001 |
| [D2](D2_rows_and_columns.md) | Which rows or columns do I remove or recode (rare categories, the id column)? | H3 | 0002 |
| [D3](D3_missing_values.md) | How do I fill missing values, and do I add a missing flag? | H3 | 0003 |
| [D4](D4_encoding.md) | How do I turn text categories into numbers? | H3 | 0004 |
| [D5](D5_scaling.md) | Which scaling and which normalization, on which columns? | H3 | 0005 |
| [D6](D6_order_around_smote.md) | In what order do encoding, scaling and SMOTE run? | H3 | 0006 |
| [D7](D7_smote_setup.md) | How do I set up SMOTE (variant, k_neighbors, seed, strategy, columns, dtypes)? | H3 | 0007 |
| [D8](D8_after_smote.md) | How do I repair and check synthetic rows, and what goes in the final file? | H3 | 0008 |

## How to use the cards (all at once, at checkpoint H1)

1. In one sitting at H1, read every card. Ask the tutor-reviewer to explain anything unclear.
2. Fill "My decision" on every card in your own words: the option, why, and your source
   (module, lecture, library documentation, Prof Rao with date). Set the matching values in
   `src/stroke_prep/config.py`. Sign each card. This is what lets the agents work on their own
   until the next checkpoint: they only carry out what is written here.
3. After the split, the agents run each card's "How to test" checks on TRAIN and put the raw
   outputs in your H2 or H3 summary. They do not interpret them.
4. At H2 (card D1) and H3 (cards D2 to D8), fill "Review": keep or amend, and why. An amendment
   is your decision, written by you; the agents stop and wait for it.
5. Write the ADR for each card from the card (`docs/adr/TEMPLATE.md`), at its review checkpoint.
6. A different choice from someone else is not wrong. A choice with no reason or no source is
   incomplete. Changing your mind after looking at train data is fine when you write down why;
   looking at test data to decide is not.
