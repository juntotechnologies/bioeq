"""
__init__ file for library
"""

from importlib import metadata

__version__ = metadata.version("bioeq")

# Move these imports to module level
from .bioeq import BioEq
from .crossover2x2 import Crossover2x2

__all__ = ["BioEq", "Crossover2x2"]
