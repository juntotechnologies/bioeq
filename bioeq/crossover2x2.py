import polars as pl
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from typing import List


class Crossover2x2:
    """
    A class to analyze a 2x2 crossover study dataset and compute bioequivalence (BE) metrics.

    This class processes PK data collected from a 2x2 crossover design, a common structure for
    bioequivalence trials where each subject receives two different formulations in two separate periods.

    The class performs the following calculations:
    - AUC (Area Under the Curve): Estimates drug exposure over time using the trapezoidal rule.
    - Cmax (Maximum Concentration): Extracts the highest observed drug concentration.
    - Tmax (Time to Cmax): Determines the time at which Cmax occurs.

    In addition to the raw metrics, log-transformed values for AUC and Cmax are computed
    and added to the output dataframe. Tmax remains untransformed.

    Attributes:
        data (pl.DataFrame): The input dataset containing PK measurements.
        subject_col (str): Column name representing the subject identifier.
        seq_col (str): Column name representing the treatment sequence.
        period_col (str): Column name representing the study period.
        time_col (str): Column name representing time values.
        conc_col (str): Column name representing drug concentration values.
        form_col (str): Column name representing the drug formulation (Test/Reference).
        df_params (pl.DataFrame): A dataframe storing computed AUC, Cmax, Tmax, and the log-transformed values for AUC and Cmax.
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
        Initializes the Crossover2x2 class and computes bioequivalence metrics.

        This method validates the dataset, ensures required columns exist, and sequentially
        computes AUC, Cmax, and Tmax, along with log-transformed versions for AUC and Cmax.

        Args:
            data (pl.DataFrame): The dataset containing PK data.
            subject_col (str): Column name for the subject identifier.
            seq_col (str): Column name for the treatment sequence.
            period_col (str): Column name for the study period.
            time_col (str): Column name for time measurements.
            conc_col (str): Column name for drug concentration measurements.
            form_col (str): Column name for formulation labels (Test/Reference).

        Raises:
            TypeError: If `data` is not a Polars DataFrame.
            ValueError: If required columns are missing in `data`.
        """
        # Load external simulated dataset for reference (not used in calculations)
        url1 = "https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
        self.simdata: pl.DataFrame = pl.read_csv(source=url1)

        # Store dataset and column names
        self.data: pl.DataFrame = data
        self.subject_col = subject_col
        self.seq_col = seq_col
        self.period_col = period_col
        self.time_col = time_col
        self.conc_col = conc_col
        self.form_col = form_col

        # Validate input dataset structure and required columns
        self._validate_data()
        self._validate_colvals()

        # Compute BE metrics in sequence
        self.df_params = self._calculate_auc()
        self.df_params = self._calculate_cmax()
        self.df_params = self._calculate_tmax()

        # Compute log-transformed BE metrics for AUC and Cmax and add alongside raw metrics.
        self.df_params = self._calculate_log_transform()

        # Sort final dataframe by subject identifier, formulation, and period.
        self.df_params = self.df_params.sort(
            [self.subject_col, self.form_col, self.period_col]
        )

    def _validate_data(self) -> None:
        """
        Ensures the dataset is a Polars DataFrame.

        Raises:
            TypeError: If the provided dataset is not a Polars DataFrame.
        """
        if not isinstance(self.data, pl.DataFrame):
            raise TypeError("Data must be a Polars DataFrame")

    def _validate_colvals(self) -> None:
        """
        Ensures that all required columns exist in the dataset.

        Raises:
            ValueError: If one or more required columns are missing.
        """
        required_columns = [
            self.subject_col,
            self.seq_col,
            self.period_col,
            self.time_col,
            self.conc_col,
            self.form_col,
        ]
        missing_columns = [
            col for col in required_columns if col not in self.data.columns
        ]
        if missing_columns:
            raise ValueError(
                f"Required column(s) missing: {', '.join(missing_columns)}"
            )

    def _calculate_auc(self) -> pl.DataFrame:
        """
        Computes the Area Under the Curve (AUC) using the trapezoidal rule.

        AUC represents the total drug exposure over time. The trapezoidal rule is used
        because it does not assume a specific PK model and provides a simple, robust estimate.

        Returns:
            pl.DataFrame: A new dataframe with an additional 'AUC' column.
        """
        grouped_df = self.data.group_by(
            [self.subject_col, self.period_col, self.seq_col, self.form_col]
        ).agg(
            [
                pl.col(self.time_col),
                pl.col(self.conc_col),
            ]
        )
        auc_vals = [
            np.trapezoid(row[self.conc_col], row[self.time_col])
            for row in grouped_df.to_dicts()
        ]
        return grouped_df.with_columns(pl.Series("AUC", auc_vals))

    def _calculate_cmax(self) -> pl.DataFrame:
        """
        Computes Cmax, the maximum observed drug concentration.

        Cmax is a critical metric in bioequivalence since it indicates the peak drug exposure.

        Returns:
            pl.DataFrame: A dataframe with an additional 'Cmax' column.
        """
        cmax_df = self.data.group_by(
            [self.subject_col, self.period_col, self.form_col]
        ).agg(pl.col(self.conc_col).max().alias("Cmax"))
        return self.df_params.join(
            cmax_df, on=[self.subject_col, self.period_col, self.form_col]
        )

    def _calculate_tmax(self) -> pl.DataFrame:
        """
        Computes Tmax, the time at which Cmax occurs.

        Tmax represents the time when the drug reaches its peak concentration.
        If multiple time points have the same Cmax, the earliest occurrence is selected.

        Returns:
            pl.DataFrame: A dataframe with an additional 'Tmax' column.
        """
        tmax_df = (
            self.data.filter(
                pl.col(self.conc_col)
                == pl.col(self.conc_col)
                .max()
                .over([self.subject_col, self.period_col, self.form_col])
            )
            .group_by([self.subject_col, self.period_col, self.form_col])
            .agg(pl.col(self.time_col).min().alias("Tmax"))
        )
        return self.df_params.join(
            tmax_df, on=[self.subject_col, self.period_col, self.form_col]
        )

    def _calculate_log_transform(self) -> pl.DataFrame:
        """
        Computes log-transformed BE metrics for AUC and Cmax and adds them alongside the raw metrics.
        Tmax is not log-transformed.

        Returns:
            pl.DataFrame: A dataframe with additional columns 'log_AUC' and 'log_Cmax'.
        """
        return self.df_params.with_columns(
            [
                pl.col("AUC").log().alias("log_AUC"),
                pl.col("Cmax").log().alias("log_Cmax"),
            ]
        )

    def run_anova(self, metric: str) -> None:
        """
        Performs a classical ANOVA on the specified log-transformed metric (e.g., 'log_AUC' or 'log_Cmax').

        The model includes fixed effects for formulation, period, and sequence.

        Args:
            metric (str): The column name of the metric to analyze.
        """
        # Convert the aggregated dataframe to a pandas DataFrame for statsmodels compatibility.
        df = self.df_params.to_pandas()
        # Build the ANOVA model formula.
        formula = (
            f"{metric} ~ C({self.form_col}) + C({self.period_col}) + C({self.seq_col})"
        )
        # Fit the ordinary least squares model.
        model = smf.ols(formula, data=df).fit()
        # Generate the ANOVA table using Type II sums of squares.
        anova_table = sm.stats.anova_lm(model, typ=2)
        print("ANOVA Results for", metric)
        print(anova_table)

    def run_nlme(self, metric: str) -> None:
        """
        Performs a mixed-effects (NLME) analysis on the specified log-transformed metric (e.g., 'log_AUC' or 'log_Cmax').

        The model includes fixed effects for formulation, period, and sequence, and a random intercept for each subject.

        Args:
            metric (str): The column name of the metric to analyze.
        """
        # Convert the aggregated dataframe to a pandas DataFrame for statsmodels compatibility.
        df = self.df_params.to_pandas()
        # Build the mixed-effects model formula.
        formula = (
            f"{metric} ~ C({self.form_col}) + C({self.period_col}) + C({self.seq_col})"
        )
        # Fit the mixed-effects model with subject as the grouping factor.
        model = smf.mixedlm(formula, data=df, groups=df[self.subject_col])
        mdf = model.fit()
        print("Mixed Effects Model Results for", metric)
        print(mdf.summary())
