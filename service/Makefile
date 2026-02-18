.PHONY: dev test lint fmt

dev:
	uvicorn main:app --reload --port 8000

test:
	pytest tests/ -v

lint:
	ruff check .

fmt:
	ruff format .
