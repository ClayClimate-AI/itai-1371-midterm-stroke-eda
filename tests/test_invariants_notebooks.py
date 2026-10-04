"""Notebook invariants. Skip until the notebooks exist."""
import json
import re

import pytest
from conftest import ROOT

NB = ROOT / "notebooks"


def _code(nb_path):
    cells = json.loads(nb_path.read_text(encoding="utf-8"))["cells"]
    return "\n".join("".join(c["source"]) for c in cells if c["cell_type"] == "code")


def _notebooks():
    found = sorted(NB.glob("0*.ipynb"))
    if not found:
        pytest.skip("no notebooks yet (notebook 01 is created at H2)")
    return found


def test_eda_notebook_reads_train_only():
    # Canvas S4: "EDA performed only on training data; testing data untouched"
    path = NB / "02_eda_train.ipynb"
    if not path.exists():
        pytest.skip("notebooks/02_eda_train.ipynb does not exist yet (H2)")
    code = _code(path)
    assert "test_raw" not in code and "TEST_RAW" not in code


def test_no_notebook_writes_into_data_raw():
    # Canvas GL4 and S10: never change the dataset manually; all changes in Python, elsewhere.
    for nb in _notebooks():
        code = _code(nb)
        for line in code.splitlines():
            if re.search(r"to_csv|open\(.+['\"]w|write_text|write_bytes", line):
                assert "data/raw" not in line and "RAW_PATH" not in line, f"{nb.name}: {line}"


def test_committed_notebooks_were_run_top_to_bottom():
    # Restart and Run All leaves execution counts 1, 2, 3 ... with no gaps.
    for nb in _notebooks():
        cells = json.loads(nb.read_text(encoding="utf-8"))["cells"]
        counts = [c.get("execution_count") for c in cells
                  if c["cell_type"] == "code" and "".join(c["source"]).strip()]
        if not counts or all(n is None for n in counts):
            pytest.skip(f"{nb.name} has not been executed yet")
        assert counts == list(range(1, len(counts) + 1)), f"{nb.name}: counts {counts}"
