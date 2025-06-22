#!/bin/bash

# Run integration tests for SecureKB

echo "Running integration tests for SecureKB..."

# Check if configuration file exists
if [ ! -f "integration_test_config.json" ]; then
    echo "Error: integration_test_config.json not found."
    echo "Please create this file based on the template:"
    echo "cp integration_test_config.json.template integration_test_config.json"
    echo "Then update the values with your deployed resources."
    exit 1
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Activated virtual environment"
fi

# Install test dependencies
pip install pytest boto3

# Run integration tests
python -m pytest tests/integration -v

# Print summary
echo "Integration tests completed"
