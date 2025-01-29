import pytest
import polars as pl
from bioeq.crossover2x2 import Crossover2x2


@pytest.fixture
def simdata1():
    return pl.read_csv(
        source="https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
    )


def test_validations(simdata1):

    with pytest.raises(
        ValueError,
        match="Required column(s) not found in dataset: period, Concentration (bg/mL)",
    ):
        Crossover2x2(
            data=simdata1,
            conc_col="Concentration (bg/mL)",
            period_col="period",
            seq_col="Sequence",
            time_col="Time (hr)",
            subject_col="SubjectID",
            form_col="Formulation",
        )
