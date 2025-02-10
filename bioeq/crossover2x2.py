import polars as pl
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf


class Crossover2x2:
    """
    Analyze a 2x2 crossover study to compute Area Under the Curve (AUC), Maximum Concentration (Cmax), Time to Cmax (Tmax) (and logAUC, logCmax):
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
        Initialize with dataset and column names, validate input, and compute BE metrics.
        """
        # Load external simulated dataset (unused in calculations)
        url1 = "https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
        self.simdata: pl.DataFrame = pl.read_csv(source=url1)

        self.data = data
        self.subject_col = subject_col
        self.seq_col = seq_col
        self.period_col = period_col
        self.time_col = time_col
        self.conc_col = conc_col
        self.form_col = form_col

        self._validate_data()
        self._validate_colvals()

        self.df_params = self._calculate_auc()
        self.df_params = self._calculate_cmax()
        self.df_params = self._calculate_tmax()
        self.df_params = self._calculate_log_transform()

        self.df_params = self.df_params.sort(
            [self.subject_col, self.form_col, self.period_col]
        )

    def _validate_data(self) -> None:
        """Check that data is a Polars DataFrame."""
        if not isinstance(self.data, pl.DataFrame):
            raise TypeError("Data must be a Polars DataFrame")

    def _validate_colvals(self) -> None:
        """Ensure all required columns exist in the dataset."""
        required = [
            self.subject_col,
            self.seq_col,
            self.period_col,
            self.time_col,
            self.conc_col,
            self.form_col,
        ]
        missing = [col for col in required if col not in self.data.columns]
        if missing:
            raise ValueError(f"Missing required column(s): {', '.join(missing)}")

    def _calculate_auc(self) -> pl.DataFrame:
        """Compute AUC (Area Under the Curve) using the trapezoidal rule."""
        grouped_df = self.data.group_by(
            [self.subject_col, self.period_col, self.seq_col, self.form_col]
        ).agg([pl.col(self.time_col), pl.col(self.conc_col)])
        auc_vals = [
            np.trapezoid(row[self.conc_col], row[self.time_col])
            for row in grouped_df.to_dicts()
        ]
        return grouped_df.with_columns(pl.Series("AUC", auc_vals))

    def _calculate_cmax(self) -> pl.DataFrame:
        """Compute Cmax (maximum concentration)."""
        cmax_df = self.data.group_by(
            [self.subject_col, self.period_col, self.form_col]
        ).agg(pl.col(self.conc_col).max().alias("Cmax"))
        return self.df_params.join(
            cmax_df, on=[self.subject_col, self.period_col, self.form_col]
        )

    def _calculate_tmax(self) -> pl.DataFrame:
        """Compute Tmax (time when Cmax occurs)."""
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
        """Compute log-transformed AUC and Cmax."""
        return self.df_params.with_columns(
            [
                pl.col("AUC").log().alias("log_AUC"),
                pl.col("Cmax").log().alias("log_Cmax"),
            ]
        )

    def run_anova(self, metric: str) -> None:
        """
        Perform ANOVA for the specified metric.
        Displays unique levels for formulation, period, and sequence before printing ANOVA results.
        """
        df = self.df_params.to_pandas()
        unique_form = df[self.form_col].unique()
        unique_period = df[self.period_col].unique()
        unique_seq = df[self.seq_col].unique()

        print("Formulation levels:", unique_form)
        print("Period levels:", unique_period)
        print("Sequence levels:", unique_seq)

        if len(unique_form) < 2:
            print(
                "Error: Formulation is constant. Provide data with ≥2 formulation levels."
            )
            return
        if len(unique_period) < 2:
            print("Error: Period is constant. Provide data with ≥2 period levels.")
            return
        if len(unique_seq) < 2:
            print(
                "Error: Sequence is confounded. Provide data with ≥2 sequence levels."
            )
            return

        formula = (
            f"{metric} ~ C({self.form_col}) + C({self.period_col}) + C({self.seq_col})"
        )
        model = smf.ols(formula, data=df).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        print("ANOVA Results for", metric)
        print(anova_table)

    def run_nlme(self, metric: str) -> None:
        """
        Perform a mixed effects model analysis for the specified metric.
        Displays unique levels for formulation, period, and sequence before printing model summary.
        """
        df = self.df_params.to_pandas()
        unique_form = df[self.form_col].unique()
        unique_period = df[self.period_col].unique()
        unique_seq = df[self.seq_col].unique()

        print("Formulation levels:", unique_form)
        print("Period levels:", unique_period)
        print("Sequence levels:", unique_seq)

        if len(unique_form) < 2:
            print(
                "Error: Formulation is constant. Provide data with ≥2 formulation levels."
            )
            return
        if len(unique_period) < 2:
            print("Error: Period is constant. Provide data with ≥2 period levels.")
            return
        if len(unique_seq) < 2:
            print(
                "Error: Sequence is confounded. Provide data with ≥2 sequence levels."
            )
            return

        formula = (
            f"{metric} ~ C({self.form_col}) + C({self.period_col}) + C({self.seq_col})"
        )
        model = smf.mixedlm(formula, data=df, groups=df[self.subject_col])
        mdf = model.fit()
        print("Mixed Effects Model Results for", metric)
        print(mdf.summary())
