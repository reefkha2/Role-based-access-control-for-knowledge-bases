#!/usr/bin/env python3

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/lambda/document_processor'))

# Import the Lambda function
import index

# Create a test event
test_event = {
    "bucket": "test-bucket",
    "key": "documents/test-document.txt"
}

# Mock the S3 client
class MockS3Client:
    def get_object(self, Bucket, Key):
        return {
            'Body': MockBody()
        }
    
    def put_object(self, Bucket, Key, Body, ContentType=None):
        print(f"Putting object to {Bucket}/{Key}")
        return {}

class MockBody:
    def read(self):
        return b"This is a test document.\n\nIt has multiple paragraphs.\n\nSome of this content should be for sales.\n\nSome should be for HR.\n\nAnd some should be confidential financial information."

# Replace the S3 client with our mock
index.s3 = MockS3Client()

# Set the environment variable
os.environ['PROCESSED_CHUNKS_BUCKET'] = 'test-processed-bucket'

# Call the handler
result = index.handler(test_event, {})

# Print the result
print(json.dumps(result, indent=2))
