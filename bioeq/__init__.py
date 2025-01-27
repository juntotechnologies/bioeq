"""
__init__ file for library
"""

from importlib import metadata

from .bioeq import BioEq
from .crossover2x2 import Crossover2x2

__all__ = ["BioEq", "Crossover2x2"]

__version__ = metadata.version("bioeq")


def hello() -> str:
    """
    Initial hello function
    """
    return "Hello from bioeq! This is a test for 0.1.0.1"
