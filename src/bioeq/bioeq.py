"""
Main bioeq code
"""

import pandas as pd

def asdf():
    """
    asdf
    """

    print("kshjfoweifjoi")


def sdfg():
    """
    asdf
    """

    print("asdfasdfrtherg")


class BioEq:
    """
    Main BioEq class
    """

    def __init__(self, number):
        self.number = number

        url = 'https://raw.githubusercontent.com/shaunporwal/bioeq/refs/heads/main/simdata/bioeq_simdata_1.csv'
        self.simdata1 = pd.read_csv(url)
