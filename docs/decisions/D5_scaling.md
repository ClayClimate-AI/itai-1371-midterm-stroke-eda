# D5: Which scaling and which normalization, on which columns?

**Decided at:** checkpoint H1, with all other cards in one sitting. **Reviewed at:** H3. **Feeds:** ADR 0005.
**Canvas P2:** "Scaling"
**Canvas P3:** "Normalization"

## The question

Canvas lists scaling and normalization as separate exercises, so your notebook shows both. You
decide which method goes into the final file, and which columns are scaled. Check how Modules 4
and 5 define "normalization": many courses mean min max scaling to 0 to 1, while scikit learn's
`Normalizer` rescales each ROW to length 1. Use your module's definition and cite it.

## Why it matters (plain words)

Columns measured in different units are like distances in inches next to distances in miles.
Any method that measures distance between rows treats a big number range as more important.
Scaling puts the number columns on a similar ruler.

## Options

| Option | What it does | Pros | Cons |
|---|---|---|---|
| A. `StandardScaler` | subtract the train mean, divide by the train standard deviation | Keeps the shape of the distribution | Sensitive to extreme values; no fixed range |
| B. `MinMaxScaler` | map the train min to 0 and the train max to 1 | Fixed, easy to read range | One extreme value squeezes the rest; test values can land outside 0 to 1 |
| C. `RobustScaler` | subtract the train median, divide by the interquartile range | Less affected by extreme values | Less familiar; no fixed range |
| D. Leave a column unscaled | nothing | Values stay in real units | Distance based steps weigh it by its raw range |

**Which columns:** you decide which columns are scaled, for example any of the numeric
measurement columns (`age`, `avg_glucose_level`, `bmi`), and whether 0/1 columns are scaled too.
Write why for each.

## How to test the choice on your own data

1. Show each numeric column before and after each method you try (histograms side by side, and
   `describe()`), on train.
2. After fitting on train, check the train result has the property the method promises (mean
   about 0 and standard deviation about 1 for A, min 0 and max 1 for B).
3. Transform test with the train fitted scaler and look at its range. Test values outside the
   train range are expected behavior, not an error.
4. Keep the fitted scaler so you can convert values back to real units (`inverse_transform`) for
   charts and range checks.

## My decision (Joseph fills this in at H1, in his own words)

* **Option I chose:** A, `StandardScaler` on age, avg_glucose_level and bmi. 0/1 and one hot columns are not scaled. MinMaxScaler is shown in the notebook as the normalization exercise (Canvas P3), but the final file uses StandardScaler.

* **Why, in my words:**
  The three number columns use very different rulers: age 0.08 to 82, glucose 55.12 to 267.76, bmi 11.3 to 97.6. SMOTE measures distance, so without scaling glucose would count the most just because its numbers are bigger. StandardScaler puts each one on mean 0 and standard deviation 1, learned from train only, and keeps the shape of each distribution. The 0/1 columns already sit between 0 and 1, so I leave them alone and they stay 0/1.

* **Source:** Canvas P2 and P3; D5 card; scikit-learn StandardScaler and MinMaxScaler documentation; number column summaries in notebooks/02_eda_train.ipynb

* **Evidence** (added at H3: notebook name and cell number, chart, report file):

* **What I will watch for:** Glucose's long right tail and bmi's extreme high value pull the mean and standard deviation. Scaled values are z scores, so I keep the fitted scaler to convert back to real units for charts and range checks. Test values outside the train range are expected, not an error.

* **Value set in `src/stroke_prep/config.py`:** `SCALER = "StandardScaler"`, `SCALE_COLUMNS = ["age", "avg_glucose_level", "bmi"]`

* **ADR:** `docs/adr/____-________.md`

* **Signed:** Joseph Clay, 10/04/2026 3:31PM (CT)

## Review at H3 (Joseph)

* [ ] Keep as decided   [ ] Amend (new option, and why, in my words):
* **What in the H3 evidence I looked at:**
* **Signed:** Joseph Clay, date and time (CT):
