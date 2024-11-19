#!/bin/sh

# Activate the virtual environment
. .venv/bin/activate

# Run the Python script
python src/main.py PROJECT

# Deactivate the virtual environment
deactivate
