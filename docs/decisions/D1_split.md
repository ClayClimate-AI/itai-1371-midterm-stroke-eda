# D1: How exactly do I split 70/30?

**Decided at:** checkpoint H1, with all other cards in one sitting. **Reviewed at:** H2. **Feeds:** ADR 0001.
**Canvas S3:** "In jupyter notebook use python to split dataset: training 70%, testing 30%; Python loads training data into memory; do not split manually or in excel"

## The question

Canvas fixes the ratio (70/30) and the tool (Python in a notebook). You still decide whether the
split is stratified, on which column, and which random seed makes it repeatable.

## Why it matters (plain words)

Splitting is like dealing a deck into two piles. If some card types are rare, a plain shuffle
can put noticeably more of them in one pile than the other by chance. Stratifying deals each
card type into the two piles in the same proportion. The seed is the shuffle's starting point:
the same seed gives the same deal every time.

## Options

| Option | What it is | Pros | Cons |
|---|---|---|---|
| A. Plain random split | `train_test_split(..., test_size=0.30, random_state=seed)` | Simplest; no assumption about which column matters | Shares of rare values can differ between the parts by chance |
| B. Stratify on the target `stroke` | add `stratify=df["stroke"]` | Target share stays about the same in both parts, which helps later evaluation | Does not control the shares of other columns |
| C. Stratify on `work_type` | add `stratify=df["work_type"]` | Every work_type group appears in both parts in similar shares (work_type is the column you balance) | Target share is not directly controlled |
| D. Stratify on both together | stratify on a combined label such as `stroke` plus `work_type` | Controls both shares at once | Combinations with very few rows can make the split fail or be unstable; harder to explain |

**Seed:** any fixed integer makes the split repeatable. Record it once and do not change it after
you have seen results, because trying seeds until results look nicer is a form of cherry picking.

## How to test the choice on your own data

Do this before any EDA, and look only at shares, not at relationships between columns.

1. For each option you are considering, split and print a small table: rows in each part, the
   share of each `stroke` value, and the share of each `work_type` value, in train and in test.
2. Check that the smallest group you care about exists in both parts.
3. Re run with the same seed and confirm the same ids land in train.
4. Pick one option and keep that split. Save it once (notebook 01) and never split again.

## My decision (Joseph fills this in at H1, in his own words)

* **Option I chose:** A

* **Why, in my words:**
  Canvas S3 asks for a 70/30 split in Python and nothing more, so a plain random split (option A) meets it as written. A random split is a shuffle made by a formula, and the seed (`random_state`) is that formula's starting number. When I set a fixed seed, the same rows land in train and test every run. If I leave it unset, the starting number changes each time, so the split changes and can't be reproduced. The seed alone isn't enough, though. Reproducibility needs the same data, the same code, and the same seed, which is why the repo pins all three. The number I pick doesn't affect quality. I set it once and won't change it after seeing results, because trying seeds until results look better is cherry picking.

* **Source:** Canvas S3 (70/30 split in Python); D1 card; tutor-reviewer explanation, Oct 4, 2026; scikit-learn train_test_split documentation (random_state)

* **Evidence** (added at H2: notebook name and cell number, chart, report file):

* **What I will watch for:** If I ever changed the seed after seeing results, that would be cherry picking. I'll keep it fixed.

* **Value set in `src/stroke_prep/config.py`:** `SPLIT_SEED = 33`, `STRATIFY_ON = None`

* **ADR:** `docs/adr/____-________.md`

* **Signed:** Joseph Clay, 10/04/2026 9:49 AM (CT)

## Review at H2 (Joseph)

* [ ] Keep as decided   [ ] Amend (new option, and why, in my words):
* **What in the H2 evidence I looked at:**
* **Signed:** Joseph Clay, date and time (CT):
