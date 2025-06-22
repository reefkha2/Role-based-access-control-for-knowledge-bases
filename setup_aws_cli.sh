#!/bin/bash

# Setup AWS CLI configuration for SecureKB project
echo "Setting up AWS CLI configuration for SecureKB project..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "AWS CLI is not installed. Please install it first."
    exit 1
fi

# Set default region
DEFAULT_REGION="us-east-1"
read -p "Enter AWS region [$DEFAULT_REGION]: " REGION
REGION=${REGION:-$DEFAULT_REGION}

# Configure AWS CLI profile for the project
aws configure set region $REGION --profile securekb
aws configure set output json --profile securekb

echo "AWS CLI configuration completed with profile 'securekb' and region '$REGION'."
echo "To use this profile, add '--profile securekb' to your AWS CLI commands or set:"
echo "export AWS_PROFILE=securekb"
