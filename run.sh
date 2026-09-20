#!/bin/bash
# Change to the directory where this script is located
cd "$(dirname "$0")"

# Run the app using the project's native Apple Silicon virtual environment
exec ./.venv/bin/python run_app.py "$@"
