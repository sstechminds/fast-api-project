### On macOS and Linux.
 curl -LsSf https://astral.sh/uv/install.sh | sh
### With Homebrew.
 brew install uv

### Tutorial
[uv-tutorial](https://chandrakundu.github.io/posts/uv-tutorial-2/)

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

### Run application
uv run uvicorn main:app --port 8000 --reload