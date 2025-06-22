# SecureKB: Deployment Guide

This guide provides instructions for deploying the SecureKB solution to your AWS environment.

## Prerequisites

Before deploying SecureKB, ensure you have the following:

1. **AWS Account**: An AWS account with permissions to create the required resources
2. **AWS CLI**: Installed and configured with appropriate credentials
3. **Node.js and npm**: Required for AWS CDK
4. **Python 3.9+**: Required for the Lambda functions and deployment scripts
5. **Git**: For cloning the repository

## Deployment Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd securekb
```

### 2. Set Up the Development Environment

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Deploy the Infrastructure

The deployment script will:
- Install required dependencies
- Deploy the CloudFormation stack using CDK
- Configure the necessary resources
- Save the stack outputs for integration testing

```bash
./deploy.sh
```

### 4. Upload Sample Documents

After deployment, you can upload sample documents to test the system:

```bash
# Get the document bucket name from the stack outputs
DOCUMENT_BUCKET=$(aws cloudformation describe-stacks --stack-name SecureKbStack --query "Stacks[0].Outputs[?OutputKey=='DocumentBucketName'].OutputValue" --output text)

# Upload sample documents
aws s3 cp sample_documents/ s3://$DOCUMENT_BUCKET/documents/ --recursive
```

### 5. Create Test Users

Create test users with different roles:

```bash
# Get the User Pool ID and Client ID from the stack outputs
USER_POOL_ID=$(aws cloudformation describe-stacks --stack-name SecureKbStack --query "Stacks[0].Outputs[?OutputKey=='UserPoolId'].OutputValue" --output text)
CLIENT_ID=$(aws cloudformation describe-stacks --stack-name SecureKbStack --query "Stacks[0].Outputs[?OutputKey=='UserPoolClientId'].OutputValue" --output text)

# Create test users
python scripts/create_test_users.py --user-pool-id $USER_POOL_ID --client-id $CLIENT_ID
```

### 6. Verify the Deployment

Run the integration tests to verify that the deployment was successful:

```bash
./run_integration_tests.sh
```

## Monitoring and Alerting

SecureKB includes the following monitoring and alerting capabilities:

1. **CloudWatch Metrics**: The Query Processor Lambda publishes metrics for:
   - Query count by department
   - Results count per query

2. **CloudWatch Logs**: All Lambda functions log their operations to CloudWatch Logs

3. **CloudWatch Alarms**: You can set up alarms for:
   - Error rates in Lambda functions
   - Unauthorized access attempts
   - High latency in query processing

## Troubleshooting

### Common Issues

1. **Deployment Failures**:
   - Check the CloudFormation events for detailed error messages
   - Ensure you have sufficient permissions to create all required resources

2. **Document Processing Issues**:
   - Check the Document Processor Lambda logs
   - Verify that documents are uploaded to the correct S3 bucket

3. **Query Processing Issues**:
   - Check the Query Processor Lambda logs
   - Verify that the user has the correct roles and permissions

### Logs and Diagnostics

To view logs for the Lambda functions:

```bash
# View Document Processor logs
aws logs filter-log-events --log-group-name /aws/lambda/SecureKbStack-DocumentProcessor

# View Metadata Tagger logs
aws logs filter-log-events --log-group-name /aws/lambda/SecureKbStack-MetadataTagger

# View Query Processor logs
aws logs filter-log-events --log-group-name /aws/lambda/SecureKbStack-QueryProcessor
```

## Cleanup

To remove all resources created by SecureKB:

```bash
cd src/cdk
cdk destroy
```

Note: This will delete all resources, including the S3 buckets and their contents. Make sure to back up any important data before running this command.
