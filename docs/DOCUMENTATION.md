

#### Setup Steps

- Created repo on GitHub
- Cloned locally
- Ran `uv init --lib` to initialize the python package repo structure
- Can install python versions using `uv python install`
  - To install a specific Python version, can do , e.g., `uv python install 3.11`
- To view installed python versions, can do `uv python list`
- To add a development dependency, use `uv add --dev`
- If there's a venv active, to check where it's coming from use `which python` or `which python3`
- If there is a virtual env indicated by a .e.g., 3.11.1, in the terminal signature, and it gets deactivated when you run `deactivate` command, it means you were in a `venv` virtual env, which is Python's built-in virtual env