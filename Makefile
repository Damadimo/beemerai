# AI Car Makefile
# Build and deployment commands for the AI car system

.PHONY: help install run test clean

help:
	@echo "Available commands:"
	@echo "  install    - Install Python dependencies"
	@echo "  run        - Run the AI car voice assistant"
	@echo "  test       - Run tests"
	@echo "  clean      - Clean build artifacts and temporary files"

install:
	pip install -r requirements.txt

run:
	python -m app.main

test:
	python -m pytest tests/ -v

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info/
	rm -f /tmp/ai_car_*.wav 2>/dev/null || true
