"""
2x2 Crossover Design Code
"""

import polars as pl
import numpy as np
from scipy.stats import t

class Crossover2x2:
    """
    Main BioEq class
    """

    def __init__(self, subject_col, seq_col, period_col, time_col, conc_col):
            url = "https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv"
            self.simdata1 = pl.read_csv(url)
            self.subject_col = subject_col
            self.seq_col = seq_col
            self.period_col = period_col
            self.time_col = time_col
            self.conc_col = conc_col
        
    def _validate_colvals(self):
        assert self.simdata1.isinstance(pl.DataFrame)
