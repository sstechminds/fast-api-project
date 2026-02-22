### On macOS and Linux.
 curl -LsSf https://astral.sh/uv/install.sh | sh
### With Homebrew.
 brew install uv

### Tutorial
[uv-tutorial](https://chandrakundu.github.io/posts/uv-tutorial-2/)

[uv-ci-cache](https://szeyusim.medium.com/optimizing-uv-in-github-actions-one-global-cache-to-rule-them-all-9c64b42aee7f)


### Setup
uv init --lib project-name

uv venv --python 3.13
source .venv/bin/activate


### Install dependencies
#### Using UV
uv add fastapi httpx sqlalchemy alembic rich setuptools uvicorn
uv add ruff --dev 
uv add pytest --dev
uv remove sqlalchemy

uv export --no-hashes -o requirements.txt 

uv tree
uv sync --group test
uv sync --all-groups


### Linting, formatting and import sorting. [Refer](https://medium.com/@abhinav.dobhal/boosting-python-development-productivity-with-uv-and-ruff-539494f6c443)
uv run ruff check --fix .
uv run ruff format .


#### Using uv with pip
uv pip install requests
uv pip check
uv pip freeze > requirements.txt
uv pip install -r requirements.txt

uv pip list


### Makefile - simplify running multiple commands with one custom command in terminal
make -i create-pr


### Run application
uv run uvicorn main:app --port 8000 --reload
##### OR Refer: `project.scripts` in pyproject.toml
uv run start

