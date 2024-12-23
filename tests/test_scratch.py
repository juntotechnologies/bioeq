"""
Scratch for initial tests, will be scrapped for more defined files later
"""

import pandas as pd
from bioeq import hello
from bioeq.load_test_data import load_sim_df


def test_scratch():
    """
    Test hello function
    """
    assert hello() == "Hello from bioeq!"


def test_load_sim_df():
    """
    Test data loading function
    """

    df = load_sim_df()

    assert isinstance(df, pd.DataFrame)
