"""
2x2 crossover Design Code
"""

import polars as pl
import numpy as np
from scipy.stats import t


class Crossover2x2:
    """
    Crossover2x2 Class
    """

    def __init__(
        self,
        data,
        subject_col,
        seq_col,
        period_col,
        time_col,
        conc_col,
        form_col,
    ):
        url1 = "https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
        self.simdata = pl.read_csv(source=url1)
        self.data = data

        self.subject_col = subject_col
        self.seq_col = seq_col
        self.period_col = period_col
        self.time_col = time_col
        self.conc_col = conc_col
        self.form_col = form_col

        self._validate_data()
        self._validate_colvals()

    def _validate_data(self):
        # Check Polars DataFrame
        if not isinstance(self.data, pl.DataFrame):
            raise TypeError("Data must be a Polars DataFrame")

    def _validate_colvals(self):
        # Check that all columns are present
        list_defined_columns = [
            self.subject_col,
            self.seq_col,
            self.period_col,
            self.time_col,
            self.conc_col,
            self.form_col,
        ]

        missing_columns = [
            col_name
            for col_name in list_defined_columns
            if col_name not in self.data.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Required column(s) not found in dataset: {', '.join(missing_columns)}"
            )

    def _integrate_group(self, group_df: pl.DataFrame) -> pl.DataFrame:
        """
        Compute AUC using trapezoidal rule for a group.
        """
        group_df = group_df.sort(self.time_col)
        times = group_df[self.time_col].to_numpy()
        concentrations = group_df[self.conc_col].to_numpy()
        auc_val = np.trapz(concentrations, times)
        return pl.DataFrame(
            {
                self.subject_col: [group_df[self.subject_col][0]],
                self.period_col: [group_df[self.period_col][0]],
                self.form_col: [group_df[self.form_col][0]],
                "AUC": [auc_val],
            }
        )

    def calculate_auc(self):
        """
        Calculate area under the concentration-time curve (AUC) using the trapezoidal rule.
        AUC is computed for each subject in each period and for each formulation.
        """
        auc_df = self.data.groupby(
            [self.subject_col, self.period_col, self.form_col]
        ).apply(self._integrate_group)
        return auc_df
