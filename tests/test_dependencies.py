"""Infrastructure test (working at H1): every package imports at a usable version."""
import importlib

import pytest
from packaging.version import Version

MINIMUMS = {
    "pandas": "2.2",
    "numpy": "1.26",
    "sklearn": "1.5",
    "imblearn": "0.13",
    "matplotlib": "3.8",
    "jupyterlab": "4.0",
    "nbconvert": "7.0",
    "pytest": "8.0",
}


@pytest.mark.parametrize("module,minimum", MINIMUMS.items())
def test_import_and_minimum_version(module, minimum):
    mod = importlib.import_module(module)
    assert Version(mod.__version__) >= Version(minimum), f"{module} {mod.__version__} < {minimum}"


def test_smote_imports():
    from imblearn.over_sampling import SMOTE  # noqa: F401  Prof Rao, class, Oct 1, 2026
