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
    return BioEq(number=1,
                 subject_col = 'SubjectID',
                 conc_col = 'Concentration (ng/mL)',
                 time_col = 'Time (hr)')

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


def test_compute_auc_empty_data():
    bioeq_instance = BioEq(number=1, subject_col="SubjectID", conc_col="Concentration (ng/mL)", time_col="Time (hr)")
    bioeq_instance.simdata1 = pl.DataFrame()  # Empty DataFrame
    with pytest.raises(ValueError):
        bioeq_instance.compute_auc()
