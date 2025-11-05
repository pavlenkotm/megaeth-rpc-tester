.PHONY: help install test lint format clean build docker run-example

help:
	@echo "MegaETH RPC Tester - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install dependencies"
	@echo "  make install-dev      Install with dev dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make format           Format code with black and isort"
	@echo "  make lint             Run linters (flake8, mypy)"
	@echo "  make test             Run tests"
	@echo "  make test-cov         Run tests with coverage report"
	@echo "  make test-integration Run integration tests only"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     Build Docker image"
	@echo "  make docker-run       Run Docker container"
	@echo "  make docker-test      Test Docker image"
	@echo ""
	@echo "Examples:"
	@echo "  make run-basic        Run basic example"
	@echo "  make run-compare      Run comparison example"
	@echo "  make run-health       Run health monitoring example"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean            Clean build artifacts"
	@echo "  make build            Build package"
	@echo "  make security-check   Run security scans"

# Setup targets
install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e .
	pip install black isort flake8 mypy pytest pytest-asyncio pytest-cov bandit safety

# Development targets
format:
	@echo "Formatting code with black..."
	black rpc_tester/ tests/ examples/
	@echo "Sorting imports with isort..."
	isort rpc_tester/ tests/ examples/
	@echo "Done!"

lint:
	@echo "Running flake8..."
	flake8 rpc_tester/ tests/ --max-line-length=127 --exclude=__pycache__
	@echo "Running mypy..."
	mypy rpc_tester/ --ignore-missing-imports
	@echo "Linting complete!"

test:
	@echo "Running tests..."
	pytest tests/ -v

test-cov:
	@echo "Running tests with coverage..."
	pytest tests/ --cov=rpc_tester --cov-report=html --cov-report=term
	@echo "Coverage report generated in htmlcov/"

test-integration:
	@echo "Running integration tests..."
	pytest tests/test_integration.py -v

test-watch:
	@echo "Running tests in watch mode..."
	pytest-watch tests/

# Docker targets
docker-build:
	@echo "Building Docker image..."
	docker build -t megaeth-rpc-tester:latest .

docker-run:
	@echo "Running Docker container..."
	docker run --rm megaeth-rpc-tester:latest --help

docker-test:
	@echo "Testing Docker image..."
	docker build -t megaeth-rpc-tester:test .
	docker run --rm megaeth-rpc-tester:test --version
	@echo "Docker image test passed!"

docker-compose-up:
	@echo "Starting services with docker-compose..."
	docker-compose up

docker-compose-down:
	@echo "Stopping services..."
	docker-compose down

# Example targets
run-basic:
	@echo "Running basic example..."
	python examples/basic_usage.py

run-compare:
	@echo "Running comparison example..."
	python examples/compare_endpoints.py

run-health:
	@echo "Running health monitoring example..."
	python examples/health_monitoring.py

run-cache:
	@echo "Running caching example..."
	python examples/with_caching.py

run-prometheus:
	@echo "Running Prometheus integration example..."
	python examples/prometheus_integration.py

# Security
security-check:
	@echo "Running security checks..."
	@echo "Checking dependencies with safety..."
	safety check || true
	@echo "Scanning code with bandit..."
	bandit -r rpc_tester/ -f screen || true
	@echo "Security scan complete!"

# Build and packaging
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "Clean complete!"

build: clean
	@echo "Building package..."
	python -m build
	@echo "Build complete! Artifacts in dist/"

# Quality checks (all-in-one)
check: format lint test
	@echo "All quality checks passed!"

# Quick test (fast subset for development)
quick-test:
	@echo "Running quick tests..."
	pytest tests/test_core.py tests/test_config.py -v

# Generate config example
gen-config:
	@echo "Generating example configuration..."
	python -m rpc_tester --generate-config example_config.yaml
	@echo "Config generated: example_config.yaml"

# Documentation
docs-serve:
	@echo "Serving documentation..."
	mkdocs serve

docs-build:
	@echo "Building documentation..."
	mkdocs build
	@echo "Documentation built in site/"

# Development server (if needed)
dev:
	@echo "Starting development mode with auto-reload..."
	watchmedo auto-restart --directory=./rpc_tester --pattern=*.py --recursive -- python -m rpc_tester

# Release helpers
version:
	@echo "Current version:"
	@grep "version" setup.py | head -1

bump-patch:
	@echo "Bumping patch version..."
	bumpversion patch

bump-minor:
	@echo "Bumping minor version..."
	bumpversion minor

bump-major:
	@echo "Bumping major version..."
	bumpversion major
