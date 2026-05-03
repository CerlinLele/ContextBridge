# AWS RAG Implementation Plan

## Recommendation

Use a custom RAG pipeline on AWS with LlamaIndex for ingestion and parsing.

The main reason is flexibility: the application should be able to choose the embedding model and LLM model from configuration instead of being locked into one managed Bedrock Knowledge Base setup.

Recommended V1 architecture:

```text
S3 knowledge source
-> ingestion worker
-> LlamaIndex reader/parser
-> LlamaIndex node/chunk pipeline
-> selected embedding model
-> vector store
-> retrieval API
-> selected LLM model
-> answer with citations
```

Recommended V1 AWS services:

```text
Amazon S3                 # Original knowledge source storage
Lambda / ECS / App Runner # Ingestion worker and application API runtime
DynamoDB                  # Source registry, ingestion runs, model profiles
OpenSearch Serverless     # Primary vector store option
Aurora PostgreSQL pgvector # Alternative if PostgreSQL is already used
SQS / EventBridge         # Async ingestion trigger
CloudWatch                # Logs and metrics
IAM + KMS                 # Permissions and encryption
```

Recommended framework components:

```text
LlamaIndex readers              # Load files into Documents
LlamaIndex NodeParser           # Parse Documents into Nodes
LlamaIndex IngestionPipeline    # Compose parsing, metadata, and embedding steps
Provider adapters               # Bedrock / OpenAI / local model providers
```

Use Amazon Bedrock Knowledge Bases only as an optional managed path when speed matters more than parser, chunking, and model-control flexibility.

References:

- LlamaIndex Ingestion Pipeline: https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline/
- LlamaIndex Documents and Nodes: https://developers.llamaindex.ai/python/framework/module_guides/loading/documents_and_nodes/
- LlamaIndex Transformations: https://developers.llamaindex.ai/python/framework/module_guides/loading/ingestion_pipeline/transformations/
- Amazon Bedrock supported models and Regions: https://docs.aws.amazon.com/en_us/bedrock/latest/userguide/knowledge-base-supported.html

## Phase 1: AWS Environment Planning

Define separate environments:

```text
dev
staging
prod
```

Choose the AWS Region based on:

- User location
- Bedrock model availability, if using Bedrock-hosted models
- Vector store support
- Data residency requirements
- Latency to model providers and users

If the product is mainly used in Australia, start by checking `ap-southeast-2`, but confirm the selected embedding model, selected LLM model, and vector store are all supported in that Region.

The system should not assume all models are available everywhere. Store model-provider and region compatibility in configuration.

## Phase 2: Model Selection Strategy

The RAG system should support selectable model profiles.

Separate these choices:

```text
embedding model
generation LLM
optional reranker model
optional parser mode
```

Example model profile:

```json
{
  "profile_id": "dev-bedrock-titan-claude",
  "embedding": {
    "provider": "bedrock",
    "model_id": "amazon.titan-embed-text-v2:0",
    "dimension": 1024,
    "region": "ap-southeast-2"
  },
  "llm": {
    "provider": "bedrock",
    "model_id": "anthropic.claude-3-5-sonnet-20241022-v2:0",
    "region": "ap-southeast-2",
    "temperature": 0.2,
    "max_tokens": 1200
  },
  "parser": {
    "framework": "llamaindex",
    "node_parser": "SentenceSplitter",
    "chunk_size": 800,
    "chunk_overlap": 120
  },
  "retrieval": {
    "top_k": 5
  }
}
```

The exact model IDs should be environment-specific. Do not hard-code them in ingestion or query business logic.

Supported provider options can include:

```text
Bedrock embeddings + Bedrock LLM
OpenAI embeddings + OpenAI LLM
Cohere embeddings/reranker + Bedrock LLM
Local embedding model + Bedrock/OpenAI LLM
```

Implementation rule:

- Store `embedding_model`, `embedding_dimension`, and `embedding_provider` with every vector index.
- Store `llm_model`, `llm_provider`, and prompt version with every answer trace.
- Rebuild the vector index when the embedding model or embedding dimension changes.
- Re-run evaluation when the LLM, prompt, parser, chunking, reranker, or retrieval settings change.

## Phase 3: Data Source Management with S3

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

Recommended artifact bucket:

```text
s3://contextbridge-kb-artifacts-dev/
  parsed/
  nodes/
  chunks/
  failed/
  reports/
```

Separate source and artifact buckets are useful because ingestion jobs may generate outputs. If an S3 event triggers a function that writes back to the same bucket, it can accidentally create an event loop.

References:

- S3 Event Notifications: https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html
- S3 with Lambda: https://docs.aws.amazon.com/lambda/latest/dg/with-s3.html

## Phase 4: Vector Store Selection

Recommended V1 options:

```text
OpenSearch Serverless
Aurora PostgreSQL + pgvector
```

Use OpenSearch Serverless when:

- Metadata filtering matters.
- Search behavior needs to be configurable.
- Hybrid search may be needed later.
- The team wants a common AWS-native RAG vector search setup.

Use Aurora PostgreSQL + pgvector when:

- The product already uses PostgreSQL.
- Source metadata and relational app data need to live close together.
- Operational simplicity matters more than specialized search features.

Optional:

```text
S3 Vectors
```

Use S3 Vectors only if its query/filtering behavior fits the application and the team wants lighter managed vector storage. It is a better fit for simpler retrieval workflows than for highly customized ranking and filtering.

References:

- S3 Vectors with Bedrock Knowledge Bases: https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-vectors-bedrock-kb.html
- Aurora PostgreSQL as a Bedrock Knowledge Base vector store: https://docs.aws.amazon.com/en_us/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.VectorDB.html

## Phase 5: LlamaIndex Parser and Ingestion Design

Use LlamaIndex for parsing and node creation instead of relying on Bedrock Knowledge Bases parsing.

Core concepts:

```text
source file
-> LlamaIndex Document
-> LlamaIndex NodeParser
-> Nodes with metadata
-> embeddings
-> vector records
```

Default parser profile:

```text
framework: llamaindex
node_parser: SentenceSplitter
chunk_size: 800
chunk_overlap: 120
include_metadata: true
```

Use parser profiles so the team can experiment safely:

```json
{
  "parser_profile_id": "sentence-800-120-v1",
  "framework": "llamaindex",
  "reader": "file-type-specific",
  "node_parser": "SentenceSplitter",
  "chunk_size": 800,
  "chunk_overlap": 120,
  "metadata_extractors": ["title", "source_path"],
  "version": 1
}
```

Parser options to support later:

```text
SentenceSplitter             # Good default for normal text
TokenTextSplitter            # More predictable token budgets
HierarchicalNodeParser       # Parent/child retrieval
SemanticSplitterNodeParser   # Semantic chunk boundaries
custom parser                # Domain-specific parsing rules
```

Store these fields for every generated node:

```text
node_id
source_id
source_uri
source_type
content_hash
parser_profile_id
parser_version
chunk_index
chunk_text
metadata
created_at
```

If parser settings change, mark affected sources as `reindex_required`.

## Phase 6: Embedding Strategy

Do not pick a single fixed embedding model in the plan.

Instead, define allowed embedding providers and model profiles:

```text
Bedrock Titan embeddings
OpenAI text embeddings
Cohere embeddings
Local sentence-transformer style embeddings
```

Important values to store:

```text
embedding_provider
embedding_model
embedding_dimension
embedding_profile_id
chunk_size
chunk_overlap
parser_profile_id
vector_store
index_name
ingestion_version
```

The vector index is tied to one embedding profile. If a source needs to be indexed by multiple embedding models, create separate indexes or separate vector namespaces.

Recommended naming:

```text
rag-{env}-{embedding_provider}-{embedding_model_slug}-{dimension}
```

Example:

```text
rag-dev-bedrock-titan-v2-1024
rag-dev-openai-text-embedding-3-large-3072
```

## Phase 7: Source Registry Design

For V1, use DynamoDB if possible. Use an S3 JSON registry only for the smallest prototype.

Suggested DynamoDB tables:

```text
rag_sources
rag_ingestion_runs
rag_documents
rag_model_profiles
rag_parser_profiles
```

Suggested `rag_sources` fields:

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
parser_profile_id
embedding_profile_id
vector_index_name
metadata
```

Suggested `rag_model_profiles` fields:

```text
profile_id
environment
embedding_provider
embedding_model
embedding_dimension
llm_provider
llm_model
llm_region
temperature
max_tokens
is_default
status
created_at
```

Suggested statuses:

```text
pending
active
failed
deleted
reindex_required
disabled
```

## Phase 8: Ingestion Flow

Use an async custom ingestion flow.

```text
Upload file to S3 raw/
-> S3 ObjectCreated event
-> EventBridge / SQS
-> ingestion worker
-> read source registry
-> load active parser profile
-> load active embedding profile
-> parse with LlamaIndex
-> generate embeddings with selected provider
-> write vectors to OpenSearch / Aurora pgvector
-> write artifacts and ingestion report
-> update DynamoDB registry
```

The ingestion worker should be idempotent:

- Calculate a source `content_hash`.
- Skip ingestion if the source hash and ingestion profile hash have not changed.
- Mark the source as `reindex_required` if parser or embedding profile changes.
- Write failed files to `failed/` with error details.

Suggested ingestion profile hash input:

```text
source content hash
parser profile id + version
embedding profile id + model + dimension
metadata extraction version
```

LlamaIndex ingestion can be modeled as:

```python
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter

parser = SentenceSplitter(
    chunk_size=parser_config.chunk_size,
    chunk_overlap=parser_config.chunk_overlap,
)

pipeline = IngestionPipeline(
    transformations=[
        parser,
        embedding_model,
    ]
)

nodes = pipeline.run(documents=documents)
```

Keep this as an architectural sketch. The production implementation should wrap provider-specific embedding clients behind an internal interface.

## Phase 9: Query API

Recommended application API:

```http
POST /rag/query
GET /rag/sources
POST /rag/sources/sync
POST /rag/sources/reindex
GET /rag/model-profiles
PUT /rag/model-profiles/default
GET /rag/parser-profiles
PUT /rag/parser-profiles/default
DELETE /rag/sources/{source_id}
```

Example query request:

```json
{
  "question": "...",
  "model_profile_id": "prod-bedrock-titan-claude",
  "retrieval": {
    "top_k": 5
  },
  "filters": {
    "category": "policies"
  }
}
```

Example query response:

```json
{
  "answer": "...",
  "model_profile_id": "prod-bedrock-titan-claude",
  "sources": [
    {
      "source_id": "...",
      "title": "...",
      "s3_key": "...",
      "node_id": "...",
      "score": 0.82
    }
  ]
}
```

Query flow:

```text
question
-> load model profile
-> embed query with selected embedding model
-> vector search in matching index
-> optional reranking
-> compose prompt
-> call selected LLM
-> return answer and citations
```

Important rule:

The query embedding model must match the embedding model used by the target vector index.

## Phase 10: LLM Strategy

The generation LLM should be selected at query time through a model profile.

Supported LLM provider options can include:

```text
Bedrock Anthropic Claude
Bedrock Amazon Nova
OpenAI models
local or private hosted models
```

Store these values per query:

```text
query_id
model_profile_id
llm_provider
llm_model
prompt_version
retrieval_profile_id
top_k
latency
token_usage
answer_source_count
```

Prompt rules:

- The model should answer only from retrieved context.
- The model should cite source nodes.
- The model should say it does not know when context is insufficient.
- The model should not expose internal source paths unless the application allows it.

## Phase 11: Security and Permissions

Minimum requirements:

```text
S3 bucket encryption with KMS
IAM least privilege
CloudWatch logs
No public S3 access
Separate dev/staging/prod environments
Provider API keys stored in Secrets Manager
Bedrock permissions scoped to selected models
Vector store access scoped by environment and index
```

Suggested app role permissions:

```text
bedrock:InvokeModel for approved Bedrock models
dynamodb:GetItem
dynamodb:Query
dynamodb:Scan
s3:GetObject for approved metadata or source access only
vector store read permissions
secretsmanager:GetSecretValue for approved external provider keys
```

Suggested ingestion role permissions:

```text
s3:GetObject from source bucket
s3:PutObject to artifact bucket
bedrock:InvokeModel for approved embedding models
dynamodb:PutItem
dynamodb:UpdateItem
vector store write permissions
secretsmanager:GetSecretValue for approved external provider keys
```

## Phase 12: Observability

Track these ingestion fields:

```text
ingestion_run_id
source_id
content_hash
parser_profile_id
embedding_profile_id
chunk_count
duration
failure_reason
```

Track these query fields:

```text
query_latency
retrieval_scores
embedding_model_latency
llm_model_latency
token_usage
answer_source_count
model_profile_id
```

Recommended AWS tools:

```text
CloudWatch Logs
CloudWatch Metrics
AWS X-Ray optional
CloudTrail for audit
```

## Phase 13: Evaluation

Create a fixed eval set:

```text
question
expected_sources
expected_answer_points
should_answer true/false
```

Run the eval set whenever changing:

- Parser profile
- Chunking strategy
- Embedding model
- LLM model
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

Compare model profiles with the same eval set before changing production defaults.

## Milestones

### Milestone 1: Flexible RAG MVP

- Create S3 source bucket.
- Create artifact bucket.
- Create DynamoDB source registry.
- Define one parser profile.
- Define one embedding profile.
- Define one LLM profile.
- Build LlamaIndex ingestion worker.
- Store vectors in OpenSearch Serverless or Aurora pgvector.
- Build simple query API.

### Milestone 2: Model and Parser Profiles

- Add model profile CRUD.
- Add parser profile CRUD.
- Add default profile selection per environment.
- Track profile IDs in ingestion and query traces.
- Add validation so query embedding model matches the vector index.

### Milestone 3: Automated Ingestion

- Add S3 events.
- Add EventBridge or SQS.
- Add Lambda or ECS worker.
- Add idempotent ingestion based on content hash and profile hash.
- Add reindex flow.

### Milestone 4: Production Hardening

- Apply IAM least privilege.
- Add KMS encryption.
- Add Secrets Manager for external provider keys.
- Add CloudWatch metrics.
- Add retry and dead-letter queue.
- Add eval set.
- Add cost tracking.

### Milestone 5: Quality Improvements

- Add metadata filters.
- Add reranking.
- Add hybrid search.
- Add parent/child retrieval.
- Add permission-aware retrieval.
- Add multi-tenant separation if needed.

## Final Recommendation

Start with:

```text
S3 + DynamoDB + LlamaIndex ingestion/parser + OpenSearch Serverless or Aurora pgvector
```

Use model profiles to choose the embedding model and LLM model.

Use parser profiles to choose the LlamaIndex parser and chunking strategy.

This gives the project a flexible RAG foundation while still staying AWS-friendly for storage, security, observability, and deployment.
