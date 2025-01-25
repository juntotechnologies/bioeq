"""
__init__ file for library
"""

import tomli  # TOML parser for Python <3.11
from pathlib import Path

from .bioeq import BioEq

from .crossover2x2 import Crossover2x2


# Dynamically extract version from pyproject.toml
def get_version():
    """
    Reads the version of the package from pyproject.toml.

    Returns:
        str: The version specified in the pyproject.toml file.
    """
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        pyproject_data = tomli.load(f)
    return pyproject_data["tool"]["poetry"]["version"]


# test function
def hello() -> str:
    """
    Initial hello function
    """
    return "Hello from bioeq! This is a test for 0.1.0.1"


__version__ = get_version()
