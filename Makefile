.PHONY: help install install-dev test test-cov format lint clean run

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install the package in production mode
	pip install -e .

install-dev: ## Install the package with development dependencies
	pip install -e ".[dev]"
	pip install pre-commit
	pre-commit install

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage report
	pytest --cov=src --cov-report=html --cov-report=term-missing

format: ## Format code with black
	black src tests main.py

format-check: ## Check code formatting without making changes
	black --check src tests main.py

lint: ## Run flake8 linter
	flake8 src tests main.py

lint-fix: ## Run flake8 and show suggestions
	flake8 src tests main.py --show-source --statistics

clean: ## Clean build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

run: ## Run the application
	python3 main.py

check: format-check lint ## Run all checks (format and lint)

all: clean install-dev test ## Clean, install dev dependencies, and run tests
