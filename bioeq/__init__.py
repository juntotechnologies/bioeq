"""
__init__ file for library
"""

from importlib import metadata

from bioeq.bioeq import BioEq
from bioeq.crossover2x2 import Crossover2x2


__version__ = metadata.version("bioeq")
