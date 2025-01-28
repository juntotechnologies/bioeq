"""
__init__ file for library
"""

from importlib import metadata

try:
    __version__ = metadata.version("bioeq")
except metadata.PackageNotFoundError:
    __version__ = "unknown"

# Direct imports
from .crossover2x2 import Crossover2x2
