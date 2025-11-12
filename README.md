# Plande

Dynamic planning agent framework scaffold managed by `uv`.

## Prerequisites

- Python 3.11+
- [`uv`](https://github.com/astral-sh/uv) installed and on your `PATH`.

## Getting Started

```bash
# create a new environment managed by uv
uv venv

# activate the environment (Linux/macOS)
source .venv/bin/activate

# install project dependencies
uv pip install -e .

# install optional development dependencies
uv pip install -e ".[dev]"
```

## Project Structure

- `src/plande_agent/` – core package with planner, executor, retriever, and support modules.
- `tests/` – pytest suite with smoke tests validating the executor.
- `pyproject.toml` – uv/hatch project definition, linting, and type checking config.

## Common Tasks

```bash
# run the test suite
uv pip install -e ".[dev]"
pytest

# run Ruff linting
ruff check src tests

# run mypy type checking
mypy src
```

## Next Steps

1. Wire up a real embedding-backed `ToolRetriever` to replace the lexical stub.
2. Integrate your LLM provider inside `Planner` and `FinalResponder`.
3. Expand the `Supervisor` loop with error-aware replanning and telemetry.
