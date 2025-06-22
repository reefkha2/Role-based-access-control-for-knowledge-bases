# SecureKB: Design and Architecture

This document outlines the design and architecture for SecureKB, a solution for implementing role-based access control in Amazon Bedrock Knowledge Bases.

## System Architecture

SecureKB consists of two main workflows:
1. Document ingestion with chunk-level classification
2. Query processing with role-based filtering

### Core Components

1. **Amazon Bedrock Knowledge Base**
   - Stores all document chunks with metadata tags
   - Provides vector search capabilities for RAG

2. **Amazon Cognito**
   - Handles user authentication
   - Stores user attributes including roles
   - Supports federation with enterprise identity providers

3. **Lambda Functions**
   - Document Processor: Handles document chunking and preprocessing
   - Metadata Tagger: Uses LLM to classify chunks and apply metadata
   - Query Processor: Applies role-based filters to queries

4. **API Gateway**
   - Provides secure API endpoints for the application
   - Handles authentication and request routing

5. **Amazon S3**
   - Stores original documents
   - Serves as intermediate storage during processing

## Architecture Diagrams

### Document Ingestion Flow

![Knowledge Base Ingestion with Chunk-Level Tagging](images/kb-ingestion-with-chunk-tagging.png.png)

During document ingestion:
1. Documents are uploaded to S3
2. Document processor Lambda is triggered
3. Documents are split into chunks
4. Each chunk is classified by an LLM
5. Appropriate metadata tags are applied
6. Tagged chunks are ingested into the Knowledge Base

### Query Processing Flow

![Role-Based Query Flow](images/kb-role-based-query-flow.png.png)

During query processing:
1. User authenticates through Cognito
2. User submits a query through the application
3. Query and user role information are sent to API Gateway
4. Query processor Lambda applies appropriate filters based on user role
5. Only chunks matching the user's role are included in the search
6. Filtered results are returned to the user

## Data Models

### Document Chunk Metadata

```json
{
  "departments": ["sales", "marketing"],
  "sensitivity": "internal",
  "created_at": "2025-06-20T14:30:00Z",
  "source_document": "s3://bucket/path/to/document.pdf",
  "chunk_id": "doc123-chunk7"
}
```

### User Role Information

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "departments": ["sales"],
  "clearance_level": "internal"
}
```

### Query Filter Expression

```json
{
  "andAll": [
    {
      "listContains": {
        "key": "departments",
        "value": "sales"
      }
    },
    {
      "in": {
        "key": "sensitivity",
        "value": ["public", "internal"]
      }
    }
  ]
}
```

## Component Details

### Document Processor Lambda

The Document Processor Lambda handles the initial processing of documents:
- Extracts text from various document formats
- Splits documents into appropriate chunks
- Maintains document context for classification
- Triggers the metadata tagging process

### Metadata Tagger Lambda

The Metadata Tagger Lambda classifies chunks and applies metadata:
- Sends chunk and document context to an LLM
- Prompts the LLM to classify the chunk by department and sensitivity
- Applies the resulting metadata tags to the chunk
- Handles classification failures with secure defaults
- Ingests tagged chunks into the Knowledge Base

### Query Processor Lambda

The Query Processor Lambda handles role-based filtering:
- Extracts user role information from authentication context
- Generates appropriate filter expressions based on roles
- Applies filters to Knowledge Base queries
- Processes and formats the filtered results
- Logs access for audit purposes

## Security Considerations

1. **Defense in Depth**
   - Multiple layers of security controls
   - Least privilege IAM policies
   - Input validation at all entry points

2. **Authentication and Authorization**
   - Token-based authentication
   - Role-based access control
   - Secure token handling

3. **Data Protection**
   - Encryption in transit and at rest
   - Secure handling of sensitive information
   - Proper logging and audit trails

4. **Compliance**
   - Support for audit requirements
   - Adherence to AWS security best practices
   - Regular security reviews

## Scalability Considerations

1. **Performance Optimization**
   - Efficient metadata filtering
   - Caching of frequently accessed data
   - Asynchronous processing where appropriate

2. **Resource Scaling**
   - Auto-scaling Lambda configurations
   - Appropriate provisioning of Knowledge Base resources
   - Monitoring and alerting for performance issues

## Monitoring and Observability

1. **Logging**
   - Comprehensive logging of all operations
   - Structured log format for easier analysis
   - Sensitive information handling in logs

2. **Metrics**
   - Performance metrics for all components
   - User access patterns and query metrics
   - Classification accuracy metrics

3. **Alerting**
   - Alerts for security violations
   - Performance degradation alerts
   - Error rate monitoring
