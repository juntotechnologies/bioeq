
[2024-01-07]

I was able to set up a nice workflow dynamically develop this package. Can use on other packages as well. First you should make sure that there are no other venvs being used, or weren't any venvs being used previously for the project. If there were, they may impact poetry commands. You want to delete those.

Next, assuming poetry has been installed, run a `poetry init` in the root of the repo the package is housed in. Next, make sure to create an `__init__.py` file in the package dir, as well as the main package code file, which will be called `<your-package-name>.py`. Now, I like to have the following functions there to test that the notebook we'll be developing in is getting the most updated version of the local package.

```{bash}
"""
__init__ file for library
"""

import tomli  # TOML parser for Python <3.11
from pathlib import Path


from .bioeq import BioEq


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

__version__ = get_version()
```

With this set up, we want to immediately create the notebook so that we can begin working things out there and adding tested code to the package.

Create a dir in the root named `notebooks` and create a `test.ipynb` in there using `touch`.

From there, assuming you're working on `vs-code`/`positron`, you have to create a kernel from a venv that `positron` can detect. First, add the necessary deps (e.g. `poetry add pathlib jupyter ipykernel notebook tomli`). Next, run `poetry install`, and make the poetry env visible to jupyter notebooks as a kernel. To do that, run the following command in a terminal, making sure to sub in your package information where necessary:

`poetry run python -m ipykernel install --user --name="bioeq-py$(python --version | cut -d' ' -f2 | cut -d. -f1-2)" --display-name "Python (bioeq, Python $(python --version | cut -d' ' -f2 | cut -d. -f1-2))"`

The command above will make the kernel available to the notebook, and you can go ahead and select it with the notebook open. Usually there will be a button on the top right that will allow you to scroll through the detected environments and pick one you generated for the package you're working on.

Once you've done the above, open up the test notebook you generated, and in the first cell you can import your package (e.g. `import bioeq`) and test out its contents in subsequent ones.
