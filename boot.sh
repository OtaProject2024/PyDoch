#!/bin/sh

# Command line arguments
args=${1:-TEST}

# Activate the virtual environment
. .venv/bin/activate

# Run the Python script
python src/main.py "$args"

# Deactivate the virtual environment
deactivate
