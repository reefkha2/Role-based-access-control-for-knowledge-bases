#!/usr/bin/env python3

import json
import sys
import os
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/lambda/query_processor'))

# Import the Lambda function
import index

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create a test event
test_event = {
    "body": json.dumps({
        "query": "What information do we have about sales?",
        "user_info": {
            "departments": ["sales"],
            "clearance_level": "confidential"
        },
        "knowledge_base_id": "test-kb-id"
    })
}

# Mock the Bedrock Agent Runtime client
class MockBedrockAgentRuntime:
    def retrieve(self, knowledgeBaseId, retrievalQuery, retrievalConfiguration):
        return {
            'retrievalResults': [
                {
                    'content': {'text': 'This is a test document. It has multiple paragraphs. Some of this content should be for sales.'},
                    'metadata': {'departments': ['sales'], 'sensitivity': 'internal'},
                    'location': {'type': 's3'},
                    'score': 0.95
                }
            ]
        }

# Mock the CloudWatch client
class MockCloudWatch:
    def put_metric_data(self, Namespace, MetricData):
        return {}

# Replace the clients with our mocks
index.bedrock_agent_runtime = MockBedrockAgentRuntime()
index.cloudwatch = MockCloudWatch()

# Call the handler
result = index.handler(test_event, {})

# Print the result
print(json.dumps(result, indent=2))
