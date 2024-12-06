#!/bin/sh

# Command line arguments and options
args=${1:-DEMO}

while getopts ptd OPT; do
  case $OPT in
     p) args="PRODUCT";;
     t) args="TEST";;
     d) args="DEMO";;
     *) args="DEMO";;
  esac
done

# Activate the virtual environment
. .venv/bin/activate

# Run the Python script
python src/main.py "$args"

# Deactivate the virtual environment
deactivate
