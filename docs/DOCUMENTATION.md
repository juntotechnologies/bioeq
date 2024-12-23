# Documentation for Using uv in Python Package Development

## Setup Steps

### 1. Initialize Repository
- Create a repository on GitHub.  
- Clone it locally.  
- Run "uv init --lib" to set up the Python package repository structure.

### 2. Python Version Management
- Install Python versions globally using "uv python install".  
  Example: "uv python install 3.11".  
- View globally installed Python versions with "uv python list".

### 3. Add Dependencies
- Add development dependencies using "uv add --dev".

### 4. Virtual Environment (venv) Management
- Check the active venv source using "which python" or "which python3".  
- If your terminal signature indicates a version (e.g., 3.11.1), you are in a virtual environment.  
- **Note:** The "deactivate" command works only for venv environments (Python's built-in virtual environment) and is not applicable to uv.  
- To deactivate a venv environment, use the "deactivate" command.

### 5. Local Package Installation
- Install the local package for testing with:  
  "uv pip install -e ."

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

#### Suggested Workflow:
- **During Active Development**: Use pytest directly for speed and debugging.
- **For Reproducible Testing and CI**: Use tox to ensure consistency across environments and dependencies.

### 7. Formatting Code
- Use tox to check and fix code formatting:
  - Check formatting:  
    "tox -e format"
  - Automatically fix formatting:  
    "tox -e format-fix"
