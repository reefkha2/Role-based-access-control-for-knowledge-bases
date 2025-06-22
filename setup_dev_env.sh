#!/bin/bash

# Setup development environment for SecureKB project
echo "Setting up development environment for SecureKB project..."

# Create project directory structure
mkdir -p src/lambda/document_processor
mkdir -p src/lambda/metadata_tagger
mkdir -p src/lambda/query_processor
mkdir -p src/cdk
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p sample_documents

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install required packages
pip install --upgrade pip
pip install boto3 aws-cdk-lib constructs pytest

# Create requirements.txt
cat > requirements.txt << EOL
boto3>=1.28.0
aws-cdk-lib>=2.80.0
constructs>=10.2.0
pytest>=7.3.1
EOL

echo "Development environment setup completed."
echo "To activate the virtual environment, run:"
echo "source .venv/bin/activate"
