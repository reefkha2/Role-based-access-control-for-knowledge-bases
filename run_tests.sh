#!/bin/bash

# Run unit tests for SecureKB

echo "Running unit tests for SecureKB..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Activated virtual environment"
fi

# Install test dependencies
pip install pytest pytest-cov

# Run tests with coverage
python -m pytest tests/unit -v --cov=src/lambda

# Print summary
echo "Unit tests completed"
