.PHONY: install dev test lint format run clean

install:
	uv sync

dev:
	uv sync --all-groups

test:
	uv run pytest

lint:
	uv run ruff check src tests
	uv run mypy src

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

run:
	uv run python -m src.entrypoints.server

clean:
	rm -rf .venv .pytest_cache .mypy_cache .ruff_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
