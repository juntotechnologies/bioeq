import pytest
import polars as pl
import re
from bioeq.crossover2x2 import Crossover2x2


@pytest.fixture
def simdata1():
    return pl.read_csv(
        source="https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
    )


def test_column_not_found_error(simdata1):

    with pytest.raises(
        ValueError,
        match=re.escape(  # re.escape escapes all regex special chars in string, in this case parentheses and slashes
            "Required column(s) not found in dataset: period, Concentration (bg/mL)"
        ),
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


def test_missing_param_value(simdata1):

    with pytest.raises(
        TypeError,
        match=re.escape(
            "Crossover2x2.__init__() missing 7 required positional arguments: 'data', 'subject_col', 'seq_col', 'period_col', 'time_col', 'conc_col', and 'form_col'"
        ),
    ):
        Crossover2x2()
