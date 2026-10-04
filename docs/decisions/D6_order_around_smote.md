# D6: In what order do encoding, scaling and SMOTE run?

**Decided at:** checkpoint H1, with all other cards in one sitting. **Reviewed at:** H3. **Feeds:** ADR 0006.
**Canvas P4:** "Class Balancing the dataset"
**Prof Rao (in class, Oct 1, 2026):** balance work_type with SMOTE.

## The question

SMOTE makes a new row by picking a real row, picking one of its nearest neighbors in the same
work_type group, and placing a new point between them. That raises an order question: which
steps happen before SMOTE (so SMOTE sees their output) and which happen after?

## Why it matters (plain words)

SMOTE finds "nearest neighbors" by measuring distance. What it measures depends on what the
columns look like when it runs: text it cannot measure at all, missing values it refuses, and
columns with big number ranges count more than columns with small ones.

## Facts to check yourself (library behavior, not results)

* Read the `imblearn.over_sampling.SMOTE` documentation page for your installed version: which
  input types it accepts, and how it handles missing values and text. Then confirm by trying it
  on a tiny made up frame in a scratch cell.
* Read the `SMOTENC` documentation page too, because it is a SMOTE variant built for a mix of
  number and category columns. Decide whether a variant fits Prof Rao's guidance; if unsure,
  ask Prof Rao and record the answer and its date.

## Options

| Option | Order | Pros | Cons |
|---|---|---|---|
| A. Fill, encode and scale, then plain SMOTE | SMOTE sees only numbers on a common scale | Plain SMOTE can run; every column counts in the distance on a similar ruler | One hot and 0/1 columns come out as in between values that need repair (D8); the scaler describes real train rows only |
| B. Fill and encode, plain SMOTE, then scale | SMOTE sees numbers in real units | Scaler is fit on the balanced data that the Final will train on | Columns with big ranges dominate the neighbor search; same repair need as A |
| C. Fill, scale numbers, SMOTENC with the text columns as categories | category columns stay categories | Synthetic category values are always real categories | A variant: check it fits Prof Rao's guidance; encoding happens after |
| D. Another order you can justify | | | Explain it in the ADR |

In every option the fill values, encoders and scalers are fit on train only, and SMOTE runs on
train only.

## How to test the choice on your own data

1. On a small sample of train, try the orders you consider in a scratch notebook and print the
   error (if any) each order produces.
2. For the orders that run, print a few synthetic rows and look at the 0/1 and one hot columns
   and the numeric columns (in real units, using `inverse_transform`).
3. Compare numeric distributions of real and synthetic rows for each order. Describe what you
   see; there is no target result.

## My decision (Joseph fills this in at H1, in his own words)

* **Option I chose:** A, fill, encode and scale, then plain SMOTE.

* **Why, in my words:**
  Plain SMOTE needs every column to be a number with no blanks, and it picks neighbors by distance. So bmi has to be filled, the text columns encoded, and the three number columns scaled before SMOTE runs, which puts every column on a similar ruler. This follows Prof Rao's Oct 1 guidance to balance work_type with SMOTE. Every fill value, encoder and scaler is fit on train only, and SMOTE runs on train only.

* **Source:** Prof Rao in class, Oct 1, 2026; Canvas P4; D6 card; imbalanced-learn SMOTE documentation

* **Evidence** (added at H3: notebook name and cell number, chart, report file):

* **What I will watch for:** SMOTE will create in between values in the 0/1 and one hot columns (like 0.4 for hypertension), which D8 repairs. The scaler describes real train rows only, because it is fit before SMOTE. Test goes through the same train fitted steps and is never balanced.

* **Value set in `src/stroke_prep/config.py`:** none (D6 has no slot)

* **ADR:** `docs/adr/____-________.md`

* **Signed:** Joseph Clay, 10/04/2026 3:32PM (CT)

## Review at H3 (Joseph)

* [ ] Keep as decided   [ ] Amend (new option, and why, in my words):
* **What in the H3 evidence I looked at:**
* **Signed:** Joseph Clay, date and time (CT):
