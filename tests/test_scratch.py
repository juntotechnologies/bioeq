"""
Scratch for initial tests, will be scrapped for more defined files later
"""

import polars as pl
from bioeq import hello
from bioeq import BioEq


def test_scratch():
    """
    Test hello function
    """
    assert hello() == "Hello from bioeq!"


def test_load_sim_df():
    """
    Test data loading function
    """

    url = "https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
    df_simdata1 = pl.read_csv(url)

    bioeq = BioEq(number=5)
