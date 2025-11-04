# Makefile for melb_weather_data

VENV_DIR=venv

.PHONY: setup activate test clean

setup:
	@echo "🔧 Creating virtual environment..."
	python3 -m venv $(VENV_DIR)
	@echo "📦 Installing dependencies..."
	$(VENV_DIR)/bin/pip install --upgrade pip
	$(VENV_DIR)/bin/pip install -r requirements.txt
	@echo "✅ Setup complete."

activate:
	@echo "💡 To activate your environment, run:"
	@echo "source $(VENV_DIR)/bin/activate"

test:
	$(VENV_DIR)/bin/pytest tests/

clean:
	rm -rf $(VENV_DIR)

coverage:
	venv/bin/pytest --cov=src --cov-report=term-missing --cov-report=html tests/
