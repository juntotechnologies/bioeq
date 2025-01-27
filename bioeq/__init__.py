"""
__init__ file for library
"""

from importlib import metadata
from bioeq.bioeq import BioEq  # noqa
from bioeq.crossover2x2 import Crossover2x2  # noqa

__version__ = metadata.version("bioeq")
__all__ = ["BioEq", "Crossover2x2"]
