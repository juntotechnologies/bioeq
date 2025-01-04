"""
Scratch for initial tests, will be scrapped for more defined files later
"""

import polars as pl
from bioeq import BioEq
import numpy as np
from scipy.stats import t
import pytest

@pytest.fixture
def bioeq_instance():
    return BioEq(number=1)

def test_compute_auc(bioeq_instance):
    auc_df = bioeq_instance.compute_auc()
    assert not auc_df.is_empty()


def test_compute_ratio(bioeq_instance):
    ratio_df = bioeq_instance.compute_ratio()
    assert "ratio" in ratio_df.columns
    assert not ratio_df.is_empty()


def test_run_tost(bioeq_instance):
    results = bioeq_instance.run_tost()
    assert "mean_ratio" in results
    assert "ci_lower" in results
    assert "ci_upper" in results
    assert "within_80_125" in results
