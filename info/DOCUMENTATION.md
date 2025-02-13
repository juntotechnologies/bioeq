# Documentation for Using `poetry` in Python Package Development

###### Actually, `poetry` is much better for python package development since it can seamlessly publish to test.pypi and pypi using actions

## Setup Steps

### 1. Initialize Repository

- Create a repository on GitHub.
- Clone it locally.
- Run "poetry init" to set up the Python package repository structure.

### 2. Python Version Management

- Install Python versions globally using "brew install python@x.11".
  Example: "brew install python@3.10".
- View globally installed Python versions with "brew list".

### 3. Add Dependencies

- Add development dependencies using "poetry add --group dev <deps>".
  Example: "poetry add --group dev black"

### 4. Virtual Environment (venv) Management

- Check the active venv source using "which python" or "which python3".
- If your terminal signature indicates a version (e.g., 3.11.1), you are in a virtual environment.
- **Note:** The "deactivate" command works only for venv environments (Python's built-in virtual environment) and is not applicable to uv.
- To deactivate a venv environment, use the "deactivate" command.

### 5. Local Package Installation

- Install the local package for testing with:
  "poetry install"

### 6. Running Tests

#### With tox

- Use tox for testing whenever possible, as it ensures:
  - Clean and isolated environments.
  - Consistent execution of tests across Python versions.
  - Easier automation in CI/CD pipelines.
- To run tests with tox, use:
  "tox"
  - Run all environments (e.g., tests and formatting): "tox".
  - Run a specific environment: "tox -e py311".

#### With pytest Directly

- Use pytest directly for rapid test iteration or debugging during development.
- Example:
  "pytest tests/test_example.py"
  - Faster for debugging specific tests as it skips tox's environment setup.
  - Ideal for interactive development workflows.

#### Suggested Workflow

- **During Active Development**: Use pytest directly for speed and debugging (`poetry run pytest`) in repo root
- **For Reproducible Testing and CI**: Use tox to ensure consistency across environments and dependencies.

### 7. Formatting Code

- Use tox to check and fix code formatting:
  - Check formatting:
    "tox -e format"
  - Automatically fix formatting:
    "tox -e format-fix"

---

## If trying to use poetry to test package locally on jupyter notebook, read below

#### Setting Up a Poetry Environment with Jupyter Notebook Integration

Follow these steps to create a new Poetry environment, install it as a Jupyter kernel, and test your package.

## 1. Create a New Poetry Environment

1. Initialize a new Poetry environment:

    `poetry init`

    Follow the prompts to set up your `pyproject.toml`.

2. If you already have an existing `pyproject.toml`, install dependencies:

    `poetry install`

---

## 2. Add Required Dependencies

Install Jupyter and any additional dependencies required for development:

`poetry add notebook ipykernel --group dev`

---

## 3. Install the Poetry Environment as a Jupyter Kernel

Run the following command to add the Poetry environment to Jupyter as a kernel:

`poetry run python -m ipykernel install --user --name="$(poetry run python -c 'import sys, tomllib; print(tomllib.load(sys.stdin.buffer)["tool"]["poetry"]["name"])' < pyproject.toml)-py$(python --version | cut -d' ' -f2 | cut -d. -f1-2)" --display-name "Python ($(poetry run python -c 'import sys, tomllib; print(tomllib.load(sys.stdin.buffer)["tool"]["poetry"]["name"])' < pyproject.toml), Python $(python --version | cut -d' ' -f2 | cut -d. -f1-2))"`

This ensures the Poetry environment is installed as a Jupyter kernel with a clean name.

## - If you'd like to uninstall a previously created kernel, use this following command

`poetry run jupyter kernelspec uninstall <Jupyter Kernel Name>`

## - If you'd like to show the current kernels

`poetry run jupyter kernelspec list`

---

## 4. Verify Installation

Check if the kernel is successfully installed:

`poetry run jupyter kernelspec list`

You should see an entry similar to:

`bioeq /Users/your-username/Library/Jupyter/kernels/bioeq`

---

## 6. Run Jupyter Notebook

Run Jupyter Notebook within the Poetry environment:

`poetry run jupyter notebook`

In the notebook interface, select the kernel matching the name you created (e.g., Python (your-env-name)).

---

## 7. Test the Installed Package

Inside a notebook cell, verify the package and its version:

`from bioeq import **version**`

`print(**version**)`

This should display the version defined in your `pyproject.toml`.

---
