# Makefile for Kasparro

.PHONY: help install run test clean lint

help:
	@echo "Kasparro - Agentic Facebook Ads Analyst"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run analysis (provide QUERY='your query')"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Clean generated files"
	@echo "  make lint       - Run linting"

install:
	pip install -r requirements.txt

run:
	python run.py "$(QUERY)"

test:
	python -m pytest tests/ -v

clean:
	rm -rf reports/*.md reports/*.json logs/*.json
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	python -m pylint src/
