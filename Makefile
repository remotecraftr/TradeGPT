.PHONY: help install dev test lint format clean run docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make dev          - Setup development environment"
	@echo "  make test         - Run tests with coverage"
	@echo "  make lint         - Run code quality checks"
	@echo "  make format       - Format code with black and isort"
	@echo "  make clean        - Remove generated files"
	@echo "  make run          - Run the application"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt

dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 isort mypy

test:
	pytest --cov=. --cov-report=html --cov-report=term-missing

lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	mypy . --ignore-missing-imports

format:
	black .
	isort .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

run:
	python main.py

docker-build:
	docker build -t remote-crafter:latest .

docker-run:
	docker run -p 8000:8000 remote-crafter:latest
