# AWS RAG Implementation Plan

## Recommendation

Use Amazon Bedrock Knowledge Bases for the first version, then move to a more customized ingestion and retrieval pipeline only when more control is needed.

V1 should prioritize a complete managed RAG loop:

```text
S3 knowledge source
-> Bedrock Knowledge Base ingestion
-> embedding model
-> vector store
-> application API
-> Bedrock foundation model
-> answer with citations
```

Recommended V1 AWS services:

```text
Amazon S3                      # Original knowledge source storage
Amazon Bedrock Knowledge Bases # Managed RAG ingestion and retrieval
Amazon Titan Embeddings V2     # Embedding model
OpenSearch Serverless          # Vector store option
S3 Vectors                     # Alternative vector store option
Lambda / ECS / App Runner      # Application API runtime
CloudWatch                     # Logs and metrics
IAM + KMS                      # Permissions and encryption
```

References:

- Amazon Bedrock Knowledge Bases: https://docs.aws.amazon.com/en_us/bedrock/latest/userguide/knowledge-base.html
- Create a Knowledge Base: https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-create.html

## Phase 1: AWS Environment Planning

Define separate environments:

```text
dev
staging
prod
```

Choose the AWS Region based on:

- User location
- Bedrock model availability
- Knowledge Bases support
- Vector store support
- Data residency requirements

If the product is mainly used in Australia, start by checking `ap-southeast-2`, but confirm the selected embedding model, generation model, Knowledge Bases, and vector store are all supported in that Region.

Reference:

- Bedrock supported models and Regions: https://docs.aws.amazon.com/en_us/bedrock/latest/userguide/knowledge-base-supported.html

## Phase 2: Data Source Management with S3

Use S3 as the source-of-truth storage for production knowledge sources.

Recommended source bucket:

```text
s3://contextbridge-kb-sources-dev/
  raw/
    policies/
    faq/
    product/
  manifests/
    sources.json
```

Recommended artifact bucket for custom ingestion later:

```text
s3://contextbridge-kb-artifacts-dev/
  processed/
  chunks/
  failed/
```

Separate source and artifact buckets are useful because ingestion jobs may generate outputs. If an S3 event triggers a function that writes back to the same bucket, it can accidentally create an event loop.

References:

- S3 Event Notifications: https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html
- S3 with Lambda: https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html

## Phase 3: Vector Store Selection

Recommended V1 options:

```text
OpenSearch Serverless
S3 Vectors
```

Use OpenSearch Serverless when:

- Metadata filtering matters.
- Search behavior needs to be more configurable.
- Hybrid search may be needed later.
- The team wants a common RAG vector search setup.

Use S3 Vectors when:

- The system needs a lighter managed vector storage path.
- Cost and scale for vectors matter.
- Bedrock Knowledge Bases can manage the vector lifecycle.

AWS documentation describes S3 Vectors integration with Bedrock Knowledge Bases, where Bedrock reads source data, creates text blocks, generates embeddings, stores them in a vector index, and retrieves them during query time.

Reference:

- S3 Vectors with Bedrock Knowledge Bases: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-bedrock-kb.html

Alternative:

```text
Aurora PostgreSQL + pgvector
```

This is a good option if the project already uses PostgreSQL and wants vectors close to relational metadata.

Reference:

- Aurora PostgreSQL as a Bedrock Knowledge Base vector store: https://docs.aws.amazon.com/en_us/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html

## Phase 4: Embedding Strategy

Recommended first embedding model:

```text
Amazon Titan Text Embeddings V2
```

Reasons:

- AWS-native
- Works naturally with Bedrock
- Supports selectable vector dimensions

Important values to store:

```text
embedding_model
embedding_dimension
chunk_size
chunk_overlap
vector_store
index_name
ingestion_version
```

If the embedding model or vector dimension changes, the vector index should generally be rebuilt.

Reference:

- Bedrock supported embedding models: https://docs.aws.amazon.com/en_us/bedrock/latest/userguide/knowledge-base-supported.html

## Phase 5: Source Registry Design

For V1, use an S3 JSON registry:

```text
s3://contextbridge-kb-sources-dev/manifests/sources.json
```

For production, migrate to DynamoDB:

```text
rag_sources
rag_ingestion_runs
rag_documents
```

Suggested DynamoDB table:

```text
Table: rag_sources
PK: source_id
```

Suggested fields:

```text
source_id
source_path
s3_bucket
s3_key
source_type
content_hash
status
last_modified_at
ingested_at
chunk_count
embedding_model
embedding_dimension
knowledge_base_id
data_source_id
metadata
```

Suggested statuses:

```text
pending
active
failed
deleted
reindex_required
```

## Phase 6: Ingestion Flow

### V1 Managed Flow

Use Bedrock Knowledge Bases sync:

```text
Upload file to S3 raw/
-> update source registry
-> trigger Bedrock Knowledge Base sync
-> Bedrock parses document
-> Bedrock chunks content
-> Bedrock creates embeddings
-> Bedrock writes to vector store
```

Bedrock Knowledge Bases ingestion includes parsing, chunking, embedding, and writing to a vector index.

Reference:

- Turning data into a knowledge base: https://docs.aws.amazon.com/en_us/bedrock/latest/userguide/kb-how-data.html

### Later Custom Flow

Use a custom pipeline when chunking, metadata, permissions, or retry behavior needs more control:

```text
S3 ObjectCreated
-> EventBridge / SQS
-> Lambda or ECS worker
-> extract text
-> clean text
-> chunk
-> call Bedrock embedding model
-> write vectors to OpenSearch / Aurora / S3 Vectors
-> update DynamoDB registry
```

## Phase 7: Query API

Recommended application API:

```http
POST /rag/query
GET /rag/sources
POST /rag/sources/sync
DELETE /rag/sources/{source_id}
```

Example query request:

```json
{
  "question": "...",
  "top_k": 5,
  "filters": {
    "category": "policies"
  }
}
```

Example query response:

```json
{
  "answer": "...",
  "sources": [
    {
      "source_id": "...",
      "title": "...",
      "s3_key": "...",
      "chunk_id": "...",
      "score": 0.82
    }
  ]
}
```

With Bedrock Knowledge Bases, the application can either:

- Use retrieve-and-generate for the simplest path.
- Retrieve chunks first, then compose its own prompt and call a Bedrock foundation model for more control.

## Phase 8: Security and Permissions

Minimum requirements:

```text
S3 bucket encryption with KMS
IAM least privilege
Bedrock service role scoped to target buckets and vector stores
CloudWatch logs
No public S3 access
Separate dev/staging/prod environments
```

Suggested app role permissions:

```text
bedrock:Retrieve
bedrock:RetrieveAndGenerate
dynamodb:GetItem
dynamodb:Query
dynamodb:Scan
s3:GetObject for approved metadata or source access only
```

Suggested ingestion role permissions:

```text
s3:GetObject from source bucket
s3:PutObject to artifact bucket
bedrock:StartIngestionJob
dynamodb:PutItem
dynamodb:UpdateItem
vector store write permissions if using a custom pipeline
```

## Phase 9: Observability

Track these ingestion fields:

```text
ingestion_job_id
source_id
content_hash
chunk_count
embedding_model
duration
failure_reason
```

Track these query fields:

```text
query_latency
retrieval_scores
model_latency
token_usage
answer_source_count
```

Recommended AWS tools:

```text
CloudWatch Logs
CloudWatch Metrics
AWS X-Ray optional
CloudTrail for audit
```

## Phase 10: Evaluation

Create a fixed eval set:

```text
question
expected_sources
expected_answer_points
should_answer true/false
```

Run the eval set whenever changing:

- Chunking strategy
- Embedding model
- `top_k`
- Reranking
- Prompt
- Vector store

Important metrics:

```text
retrieval_hit_rate
citation_accuracy
answer_groundedness
unknown_handling
latency
cost_per_query
```

## Milestones

### Milestone 1: AWS RAG MVP

- Create S3 source bucket.
- Create Bedrock Knowledge Base.
- Choose OpenSearch Serverless or S3 Vectors.
- Select one embedding model.
- Run manual sync.
- Build simple query API.

### Milestone 2: Source Management

- Add source registry in S3 or DynamoDB.
- Track `content_hash`.
- Track ingestion status.
- Add source list API.

### Milestone 3: Automated Ingestion

- Add S3 events.
- Add EventBridge or SQS.
- Add Lambda or ECS worker.
- Trigger automatic sync or reindexing.

### Milestone 4: Production Hardening

- Apply IAM least privilege.
- Add KMS encryption.
- Add CloudWatch metrics.
- Add retry and dead-letter queue.
- Add eval set.
- Add cost tracking.

### Milestone 5: Quality Improvements

- Add metadata filters.
- Add reranking.
- Add hybrid search.
- Add permission-aware retrieval.
- Add multi-tenant separation if needed.

## Final Recommendation

Start with:

```text
S3 + Bedrock Knowledge Bases + OpenSearch Serverless or S3 Vectors
```

This gives the fastest path to a working RAG system on AWS.

Move to a custom ingestion and retrieval pipeline only when Bedrock's managed chunking, metadata handling, or retrieval controls become limiting.
