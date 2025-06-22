#!/usr/bin/env python3

import json
import requests
import os
import sys
import argparse

def query_kb(api_url, query, user_info, bucket_name):
    """Query the knowledge base with user role"""
    try:
        # Prepare the request
        payload = {
            "query": query,
            "user_info": user_info,
            "bucket_name": bucket_name
        }
        
        # Make the request
        print(f"Querying: {query}")
        print(f"User info: {json.dumps(user_info)}")
        response = requests.post(api_url + "/query", json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            return result
        else:
            print(f"Error: API returned status code {response.status_code}")
            print(response.text)
            return None
    
    except Exception as e:
        print(f"Error querying knowledge base: {e}")
        return None

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test SecureKB query functionality')
    parser.add_argument('--department', choices=['sales', 'hr', 'finance', 'executive', 'public'], 
                        default='sales', help='Department for the query')
    parser.add_argument('--clearance', choices=['public', 'internal', 'confidential', 'restricted'], 
                        default='internal', help='Clearance level for the query')
    parser.add_argument('--query', default='What are our sales numbers?', 
                        help='Query to send to the knowledge base')
    args = parser.parse_args()
    
    # Check if config file exists
    if not os.path.exists('securekb_config.json'):
        print("Error: securekb_config.json not found. Please run deploy_with_cli.sh first.")
        sys.exit(1)
    
    # Load configuration
    with open('securekb_config.json', 'r') as f:
        config = json.load(f)
    
    # Get API URL and bucket name
    api_url = config.get('api_url')
    bucket_name = config.get('processed_chunks_bucket')
    if not api_url:
        print("Error: api_url not found in configuration.")
        sys.exit(1)
    if not bucket_name:
        print("Error: processed_chunks_bucket not found in configuration.")
        sys.exit(1)
    
    # Prepare user info
    user_info = {
        "departments": [args.department],
        "clearance_level": args.clearance
    }
    
    # Query the knowledge base
    print(f"Querying knowledge base at: {api_url}")
    result = query_kb(api_url, args.query, user_info, bucket_name)
    
    if result:
        print("\nQuery Results:")
        print(json.dumps(result, indent=2))
    else:
        print("Query failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
