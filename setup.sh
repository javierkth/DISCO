#!/bin/bash

# Path to your virtual environment
VENV_DIR=".venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    python -m venv $VENV_DIR
fi

# Activate the virtual environment (Linux/macOS)
source $VENV_DIR/bin/activate

# Activate the virtual environment (Windows)
# source $VENV_DIR/Scripts/activate

# Install project dependencies
pip install -r requirements.txt
