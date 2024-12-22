
# Documentation for Using `uv` in Python Package Development

## Setup Steps

### 1. Initialize Repository
- Create a repository on GitHub.  
- Clone it locally.  
- Run `uv init --lib` to set up the Python package repository structure.

### 2. Python Version Management
- Install Python versions globally using `uv python install`.  
  Example: `uv python install 3.11`.  
- View globally installed Python versions with `uv python list`.

### 3. Add Dependencies
- Add development dependencies using `uv add --dev`.

### 4. Virtual Environment (venv) Management
- Check the active `venv` source using `which python` or `which python3`.  
- If your terminal signature indicates a version (e.g., `3.11.1`), you are in a virtual environment.  
- **Note:** The `deactivate` command works only for `venv` environments (Python's built-in virtual environment) and is not applicable to `uv`.  
- To deactivate a `venv` environment, use the `deactivate` command.

### 5. Local Package Installation
- Install the local package for testing with:  
  ```bash
  uv pip install -e .
  ```

