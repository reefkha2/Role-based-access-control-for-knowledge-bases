#!/bin/bash

# Security testing script for SecureKB

echo "Running security tests for SecureKB..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Activated virtual environment"
fi

# Install security testing tools
pip install bandit safety

echo "=== Running Bandit (Python Security Linter) ==="
bandit -r src/ -f html -o security_report_bandit.html

echo "=== Checking for vulnerable dependencies ==="
safety check -r requirements.txt --output html > security_report_dependencies.html

echo "=== Running IAM policy analyzer ==="
# In a real implementation, we would use AWS Access Analyzer
# For this demo, we'll just check for overly permissive policies in our CDK code
grep -r "Effect\": \"Allow" src/cdk/ --include="*.py" > security_report_iam.txt

echo "=== Security tests completed ==="
echo "Reports generated:"
echo "- security_report_bandit.html"
echo "- security_report_dependencies.html"
echo "- security_report_iam.txt"
