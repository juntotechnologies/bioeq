"""
Scratch for initial tests, will be scrapped for more defined files later
"""

import polars as pl
from bioeq import BioEq


def test_load_sim_df():
    """
    Test data loading function
    """

    url = "https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
    df_simdata1 = pl.read_csv(url)

    bioeq = BioEq(number=5)



"""
Main bioeq code
"""

import polars as pl
import numpy as np
from scipy.stats import t
import pytest


class BioEq:
    """
    Main BioEq class
    """

    def __init__(self, number):
        self.number = number
        url = "https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
        self.simdata1 = pl.read_csv(url)

    def compute_auc(self, subject_col="Subject", time_col="Time", conc_col="Concentration"):
        """
        Compute Area Under the Curve (AUC) using trapezoidal rule
        """
        df = self.simdata1.clone()
        df = df.sort([subject_col, time_col])
        auc_df = (
            df.groupby(subject_col)
            .apply(
                lambda group: np.trapz(
                    group[conc_col].to_numpy(),
                    group[time_col].to_numpy(),
                )
            )
            .alias("AUC")
        )
        return auc_df

    def compute_ratio(self, group_col="Treatment", measure_col="AUC", test_label="Test", ref_label="Reference"):
        """
        Compute Test/Reference ratios of a chosen measure (e.g., AUC or Cmax)
        """
        df = self.simdata1.clone()
        auc_df = self.compute_auc()
        joined_df = df.join(auc_df, on="Subject", how="inner").unique(subset=["Subject", group_col])
        pivoted = joined_df.pivot(values=measure_col, index="Subject", columns=group_col)
        pivoted = pivoted.with_columns((pivoted[test_label] / pivoted[ref_label]).alias("ratio"))
        return pivoted

    def run_tost(self, group_col="Treatment", measure_col="AUC", test_label="Test", ref_label="Reference", alpha=0.10):
        """
        Perform Two One-Sided Tests (TOST) on log-transformed ratios.
        Confidence interval is 1 - alpha, typically 90% for bioequivalence.
        """
        ratio_df = self.compute_ratio(
            group_col=group_col, measure_col=measure_col,
            test_label=test_label, ref_label=ref_label
        )
        ratios = ratio_df.select("ratio").to_series().drop_nulls().to_numpy()
        log_ratios = np.log(ratios)

        n = len(log_ratios)
        mean_log_ratio = np.mean(log_ratios)
        se_log_ratio = np.std(log_ratios, ddof=1) / np.sqrt(n)
        t_val = t.ppf(1 - alpha/2, df=n - 1)
        ci_lower = mean_log_ratio - t_val * se_log_ratio
        ci_upper = mean_log_ratio + t_val * se_log_ratio
        lower_bound = np.exp(ci_lower)
        upper_bound = np.exp(ci_upper)
        lower_limit = 0.80
        upper_limit = 1.25

        return {
            "mean_ratio": np.exp(mean_log_ratio),
            "ci_lower": lower_bound,
            "ci_upper": upper_bound,
            "within_80_125": (lower_bound >= lower_limit) and (upper_bound <= upper_limit),
        }


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
