import polars as pl
from bioeq.crossover2x2 import Crossover2x2


@pytest.fixture
def simdata1():
    return pl.read_csv(
        source="https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
    )


def test_validations(simdata1):

    print(simdata1)
