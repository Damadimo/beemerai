# AI Car Makefile
# Build and deployment commands for the AI car system

.PHONY: help install test clean firmware demo

help:
	@echo "Available commands:"
	@echo "  install    - Install Python dependencies"
	@echo "  test       - Run tests"
	@echo "  clean      - Clean build artifacts"
	@echo "  firmware   - Build ESP32 firmware"
	@echo "  demo       - Run demo application"

install:
	pip install -r requirements.txt

test:
	python -m pytest tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/ dist/ *.egg-info/

firmware:
	cd firmware/esp32_car && pio run

demo:
	python demo/routes.py
