### On macOS and Linux.
 curl -LsSf https://astral.sh/uv/install.sh | sh
### With Homebrew.
 brew install uv

### Tutorial
[uv-tutorial](https://chandrakundu.github.io/posts/uv-tutorial-2/)

[uv-ci-cache](https://szeyusim.medium.com/optimizing-uv-in-github-actions-one-global-cache-to-rule-them-all-9c64b42aee7f)

### Setup
uv venv --python 3.13
source .venv/bin/activate

### Install dependencies
#### Using UV
uv add fastapi httpx sqlalchemy alembic rich setuptools uvicorn
uv add pytest --dev
uv remove sqlalchemy

uv export --no-hashes -o requirements.txt 

uv tree
uv sync

#### Using uv with pip
uv pip install requests
uv pip check
uv pip freeze > requirements.txt
uv pip install -r requirements.txt

uv pip list

### Makefile - simplify running multiple commands with one custom command in terminal
make create-pr

### Run application
uv run uvicorn main:app --port 8000 --reload

