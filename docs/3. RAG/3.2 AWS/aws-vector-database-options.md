# AWS Vector Database Options for RAG

Last checked: 2026-05-03

## Short Recommendation

For the current custom RAG direction:

```text
S3 -> LlamaIndex parser -> selected embedding model -> vector database -> selected LLM
```

Start with one of these:

```text
OpenSearch Serverless
Aurora PostgreSQL / RDS PostgreSQL + pgvector
Qdrant
```

Use `OpenSearch Serverless` as the default AWS-native choice.

Use `Aurora PostgreSQL / RDS PostgreSQL + pgvector` if the product already uses PostgreSQL and wants vectors close to relational metadata.

Use `Qdrant` if the team wants a dedicated vector database with strong filtering and simple developer ergonomics. Qdrant works well with a custom LlamaIndex pipeline, but it is not a native Amazon Bedrock Knowledge Bases vector store.

## Compatibility Matrix

| Vector database | AWS deployment mode | Bedrock Knowledge Bases native support | Custom LlamaIndex pipeline | Best fit |
| --- | --- | --- | --- | --- |
| Amazon OpenSearch Serverless | AWS managed serverless | Yes | Yes | Default AWS-native RAG vector store, metadata filtering, hybrid search |
| Amazon OpenSearch Managed Cluster | AWS managed cluster | Yes | Yes | More cluster control than Serverless |
| Amazon Aurora PostgreSQL / RDS PostgreSQL + pgvector | AWS managed relational database | Yes, through `RDS` storage configuration | Yes | Apps already using PostgreSQL, relational metadata + vectors together |
| Amazon S3 Vectors | AWS managed object/vector storage | Yes | Yes, if direct query behavior fits | Lower-cost vector storage, infrequent retrieval, large-scale retention |
| Amazon Neptune Analytics | AWS managed graph analytics | Yes | Yes | GraphRAG and graph + vector traversal |
| Pinecone | External managed service / AWS Marketplace | Yes | Yes | Managed dedicated vector database without self-hosting |
| Redis Enterprise Cloud | External managed Redis service | Yes | Yes | Low-latency vector search with Redis ecosystem |
| MongoDB Atlas | External managed MongoDB service | Yes | Yes | MongoDB-compatible app data + vector search |
| Qdrant | Qdrant Cloud on AWS, AWS Marketplace, ECS/EKS/EC2 self-hosting | No | Yes | Dedicated vector database, payload filtering, flexible self-managed or managed deployment |
| Amazon MemoryDB | AWS managed Redis-compatible in-memory database | No | Yes | Ultra-low-latency retrieval and semantic cache workloads |
| Amazon DocumentDB | AWS managed MongoDB-compatible database | No | Yes | Existing DocumentDB/MongoDB-style workloads that need vector search |
| Amazon Kendra | AWS managed enterprise search | No, not a vector store for Bedrock KB | Possible as a retrieval service, not a normal vector DB | Enterprise search connectors and semantic retrieval |

## Bedrock Knowledge Bases Native Vector Stores

If using Amazon Bedrock Knowledge Bases managed ingestion and retrieval, the supported storage configuration types are:

```text
OPENSEARCH_SERVERLESS
OPENSEARCH_MANAGED_CLUSTER
RDS
S3_VECTORS
NEPTUNE_ANALYTICS
PINECONE
REDIS_ENTERPRISE_CLOUD
MONGO_DB_ATLAS
```

This path is convenient, but it gives less control over parser/chunking behavior than the custom LlamaIndex pipeline.

## Custom LlamaIndex Pipeline Options

With a custom pipeline, the application controls:

```text
parser profile
chunking strategy
embedding model
embedding dimension
metadata schema
vector database
retrieval strategy
LLM model
```

This makes more vector databases viable, including Qdrant, MemoryDB, DocumentDB, and any vector store supported by LlamaIndex or an internal adapter.

Recommended custom flow:

```text
S3 ObjectCreated
-> EventBridge / SQS
-> ingestion worker
-> LlamaIndex reader/parser
-> selected embedding provider
-> selected vector database
-> source registry update
```

Query flow:

```text
question
-> selected embedding model
-> matching vector index
-> optional reranker
-> selected LLM
-> answer with citations
```

Important rule:

The query embedding model must match the embedding model and vector dimension used by the target index.

## Option Notes

### OpenSearch Serverless

Best default for AWS-native RAG.

Use it when:

- Metadata filtering matters.
- Hybrid search may be needed.
- The team wants managed scaling without managing OpenSearch clusters.
- Retrieval tuning is likely to matter later.

### Aurora PostgreSQL / RDS PostgreSQL + pgvector

Best when PostgreSQL is already part of the product.

Use it when:

- Source metadata already lives in PostgreSQL.
- The app needs SQL filtering plus vector search.
- Simpler operational architecture matters.
- The vector scale is moderate enough for PostgreSQL.

### Qdrant

Works well for the custom LlamaIndex pipeline.

Use it when:

- The team wants a dedicated vector database.
- Payload filtering matters.
- The team wants local/dev parity with Docker.
- Managed Qdrant Cloud on AWS is acceptable, or the team is comfortable deploying Qdrant on ECS, EKS, or EC2.

Do not choose Qdrant if the plan is to rely on Bedrock Knowledge Bases managed ingestion, because Qdrant is not listed as a native Bedrock Knowledge Bases storage configuration type.

### S3 Vectors

Use it when:

- Cost-efficient vector storage matters.
- Retrieval can tolerate higher latency than hot vector databases.
- The workload has large-scale retention or infrequent retrieval.
- AWS-native storage simplicity matters more than advanced search controls.

### Neptune Analytics

Use it for GraphRAG.

Do not start here for ordinary document Q&A unless graph traversal is a core requirement.

### MemoryDB

Use it when ultra-low latency matters.

It is better for hot retrieval, semantic cache, or real-time workloads than for cheap long-term vector storage.

### DocumentDB / MongoDB Atlas

Use these when the app already uses MongoDB-style document data and wants vector search close to the document model.

For a greenfield RAG-only system, OpenSearch, pgvector, or Qdrant are usually cleaner first choices.

## Practical Recommendation for ContextBridge

For this project, prefer:

```text
Primary: OpenSearch Serverless
Alternative if PostgreSQL exists: Aurora PostgreSQL / RDS PostgreSQL + pgvector
Alternative dedicated vector DB: Qdrant Cloud on AWS
```

Keep the vector database behind an internal adapter so the rest of the RAG pipeline only depends on:

```text
upsert(nodes, embeddings, metadata)
query(vector, top_k, filters)
delete_by_source(source_id)
```

This keeps embedding model, LLM model, parser, and vector database choices independent.

## References

- AWS Prescriptive Guidance, Vector database options: https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-an-aws-vector-database-for-rag-use-cases/vector-db-options.html
- AWS Prescriptive Guidance, Vector database comparison: https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-an-aws-vector-database-for-rag-use-cases/vector-db-comparison.html
- Amazon Bedrock API, `StorageConfiguration`: https://docs.aws.amazon.com/bedrock/latest/APIReference/API_agent_StorageConfiguration.html
- Qdrant Cloud: https://qdrant.tech/cloud/
- Qdrant deployment documentation: https://qdrant.tech/documentation/deploy-intro/
- Qdrant on AWS Marketplace: https://aws.amazon.com/marketplace/pp/prodview-rtphb42tydtzg
