#!/usr/bin/env python3

import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/lambda/metadata_tagger'))

# Import the Lambda function
import index

# Create a test event
test_event = {
    "chunk_id": "documents-test-document.txt-chunk-0",
    "chunk_key": "chunks/documents-test-document.txt-chunk-0.json"
}

# Mock the S3 client
class MockS3Client:
    def get_object(self, Bucket, Key):
        return {
            'Body': MockBody()
        }
    
    def put_object(self, Bucket, Key, Body, ContentType=None):
        print(f"Putting object to {Bucket}/{Key}")
        print(f"Body: {Body}")
        return {}

class MockBody:
    def read(self):
        chunk_data = {
            "chunk_id": "documents-test-document.txt-chunk-0",
            "source_document": "s3://test-bucket/documents/test-document.txt",
            "content": "This is a test document.\n\nIt has multiple paragraphs.\n\nSome of this content should be for sales.\n\nSome should be for HR.\n\nAnd some should be confidential financial information."
        }
        return json.dumps(chunk_data).encode('utf-8')

# Replace the S3 client with our mock
index.s3 = MockS3Client()

# Mock the Bedrock client
class MockBedrockRuntime:
    def invoke_model(self, modelId, body):
        return {
            'body': MockResponseBody()
        }

class MockResponseBody:
    def read(self):
        response = {
            "content": [
                {
                    "text": json.dumps({
                        "departments": ["sales", "hr", "finance"],
                        "sensitivity": "confidential"
                    })
                }
            ]
        }
        return json.dumps(response).encode('utf-8')

# Replace the Bedrock client with our mock
index.bedrock_runtime = MockBedrockRuntime()

# Set the environment variable
os.environ['PROCESSED_CHUNKS_BUCKET'] = 'test-processed-bucket'

# Call the handler
result = index.handler(test_event, {})

# Print the result
print(json.dumps(result, indent=2))
