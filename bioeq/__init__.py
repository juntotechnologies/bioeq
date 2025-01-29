"""
__init__ file for library
"""

from importlib import metadata

try:
    __version__ = metadata.version("bioeq")
except metadata.PackageNotFoundError:
    __version__ = "unknown"

# relative imports
from bioeq.crossover2x2 import Crossover2x2

__all__ = ["Crossover2x2"]
