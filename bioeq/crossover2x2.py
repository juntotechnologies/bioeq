"""
2x2 crossover Design Code
"""

import polars as pl
import numpy as np
from scipy.stats import t
from typing import List


class Crossover2x2:
    """
    A class to perform operations on a 2x2 crossover design dataset.

    Attributes:
        data (pl.DataFrame): The input dataset.
        subject_col (str): Column name representing the subject identifier.
        seq_col (str): Column name representing the sequence.
        period_col (str): Column name representing the period.
        time_col (str): Column name representing time values.
        conc_col (str): Column name representing concentration values.
        form_col (str): Column name representing the formulation.
        simdata (pl.DataFrame): A reference dataset loaded from a remote CSV.
    """

    def __init__(
        self,
        data: pl.DataFrame,
        subject_col: str,
        seq_col: str,
        period_col: str,
        time_col: str,
        conc_col: str,
        form_col: str,
    ) -> None:
        """
        Initialize the Crossover2x2 object.

        Loads a reference CSV into simdata, sets dataset and column attributes,
        and validates the input data.

        Args:
            data (pl.DataFrame): Input dataset.
            subject_col (str): Column name for the subject identifier.
            seq_col (str): Column name for the sequence.
            period_col (str): Column name for the period.
            time_col (str): Column name for time values.
            conc_col (str): Column name for concentration values.
            form_col (str): Column name for the formulation.
        """
        url1: str = (
            "https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
        )
        self.simdata: pl.DataFrame = pl.read_csv(source=url1)
        self.data: pl.DataFrame = data

        self.subject_col: str = subject_col
        self.seq_col: str = seq_col
        self.period_col: str = period_col
        self.time_col: str = time_col
        self.conc_col: str = conc_col
        self.form_col: str = form_col

        self._validate_data()
        self._validate_colvals()

    def _validate_data(self) -> None:
        """
        Validate that the provided data is a Polars DataFrame.

        Raises:
            TypeError: If data is not an instance of pl.DataFrame.
        """
        if not isinstance(self.data, pl.DataFrame):
            raise TypeError("Data must be a Polars DataFrame")

    def _validate_colvals(self) -> None:
        """
        Validate that all required columns are present in the dataset.

        Raises:
            ValueError: If one or more required columns are missing.
        """
        list_defined_columns: List[str] = [
            self.subject_col,
            self.seq_col,
            self.period_col,
            self.time_col,
            self.conc_col,
            self.form_col,
        ]

        missing_columns: List[str] = [
            col_name
            for col_name in list_defined_columns
            if col_name not in self.data.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Required column(s) not found in dataset: {', '.join(missing_columns)}"
            )

    def calculate_auc(self) -> pl.DataFrame:
        """
        Calculate the Area Under the Curve (AUC) for concentration over time.

        The method groups the data by subject, period, and formulation, aggregates
        the time and concentration columns, computes the AUC for each group using the
        trapezoidal rule, adds the computed AUC as a new column, and sorts the results.

        Returns:
            pl.DataFrame: A DataFrame with an additional 'AUC' column.
        """
        grouped_df: pl.DataFrame = self.data.group_by(
            [self.subject_col, self.period_col, self.form_col]
        ).agg(
            [
                pl.col(self.time_col),
                pl.col(self.conc_col),
            ]
        )

        auc_vals: List[float] = [
            np.trapezoid(row[self.conc_col], row[self.time_col])
            for row in grouped_df.to_dicts()
        ]

        grouped_df = grouped_df.with_columns(pl.Series("AUC", auc_vals)).sort(
            [pl.col(self.subject_col), pl.col(self.period_col), pl.col(self.form_col)]
        )

        return grouped_df
