"""
Main bioeq code
"""

import polars as pl
import numpy as np
from scipy.stats import t

class BioEq:
    """
    Main BioEq class
    """

    def __init__(self, number, subject_col, time_col, conc_col):
        self.number = number
        url = "https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
        self.simdata1 = pl.read_csv(url)
        self.subject_col = subject_col
        self.time_col = time_col
        self.conc_col = conc_col

    def compute_auc(self):
        """
        Compute Area Under the Curve (AUC) using trapezoidal rule.
        """
        # Validate required columns
        required_cols = [self.subject_col, self.time_col, self.conc_col]
        if not all(col in self.simdata1.columns for col in required_cols):
            raise ValueError(f"Dataset is missing required columns: {required_cols}")
        
        df = self.simdata1.clone()
        df = df.sort([self.subject_col, self.time_col])

        # Compute AUC for each group
        auc_df = (
            df.group_by(self.subject_col).agg(
                pl.struct([self.time_col, self.conc_col]).apply(
                    lambda rows: np.trapz(
                        [row[self.conc_col] for row in rows],
                        [row[self.time_col] for row in rows],
                    )
                ).alias("AUC")
            )
        )
        return auc_df


    def compute_ratio(self, group_col="Treatment", measure_col="AUC", test_label="Test", ref_label="Reference"):
        """
        Compute Test/Reference ratios of a chosen measure (e.g., AUC or Cmax)
        """

        df = self.simdata1.clone()
        auc_df = self.compute_auc()
        # Join AUC back onto original data by Subject
        joined_df = df.join(auc_df, on="Subject", how="inner").unique(subset=["Subject", group_col])
        # Pivot wide to compare test_label vs ref_label
        pivoted = joined_df.pivot(
            values=measure_col,
            index="Subject",
            columns=group_col
        )
        pivoted = pivoted.with_columns(
            (pivoted[test_label] / pivoted[ref_label]).alias("ratio")
        )
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

        # Critical value for two-tailed T at (1 - alpha) confidence
        # For TOST, alpha is split, so we use 1 - alpha/2
        t_val = t.ppf(1 - alpha/2, df=n - 1)

        ci_lower = mean_log_ratio - t_val * se_log_ratio
        ci_upper = mean_log_ratio + t_val * se_log_ratio

        # Convert back from log scale
        lower_bound = np.exp(ci_lower)
        upper_bound = np.exp(ci_upper)

        # Typical bioequivalence limits of 80%-125%
        lower_limit = 0.80
        upper_limit = 1.25

        results = {
            "mean_ratio": np.exp(mean_log_ratio),
            "ci_lower": lower_bound,
            "ci_upper": upper_bound,
            "within_80_125": (lower_bound >= lower_limit) and (upper_bound <= upper_limit),
        }
        return results
