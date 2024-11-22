#!/bin/sh

# Command line arguments and options
args=${1:-TEST}

while getopts pt OPT; do
  case $OPT in
     p) args="PRODUCT";;
     t) args="TEST";;
     *) args="TEST";;
  esac
done

# Activate the virtual environment
. .venv/bin/activate

# Run the Python script
python src/main.py "$args"

# Deactivate the virtual environment
deactivate
