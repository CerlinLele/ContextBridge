# Source Registry

## What It Is

A source registry is the inventory of knowledge sources used by the RAG system.

It records which sources exist, where they are stored, their current status, their content hash, when they were ingested, and which processing settings were used.

The registry allows ingestion to be incremental instead of rebuilding the entire knowledge base every time.

## Why It Matters

A source registry helps answer these questions:

- Has this source changed?
- Is this a new source?
- Was this source deleted?
- How many chunks were generated from this source?
- Which embedding model was used?
- Which chunking strategy was used?
- Does this source need to be re-indexed?

## Recommended Location

For a simple file-based setup:

```text
knowledge_base/
  manifests/
    sources.json
```

In a larger system, the same concept can later move into database tables such as:

```text
rag_sources
rag_chunks
rag_ingestion_runs
```

## Minimal Example

```json
{
  "sources": [
    {
      "source_id": "refund-policy",
      "source_path": "knowledge_base/sources/policies/refund-policy.md",
      "content_hash": "sha256:8b8f1c...",
      "status": "active",
      "ingested_at": "2026-05-03T10:25:00+10:00"
    }
  ]
}
```

## Fuller Example

```json
{
  "version": 1,
  "sources": [
    {
      "source_id": "policy-refund-v1",
      "source_path": "knowledge_base/sources/policies/refund-policy.md",
      "source_type": "markdown",
      "title": "Refund Policy",
      "category": "policies",
      "content_hash": "sha256:8b8f1c...",
      "status": "active",
      "last_modified_at": "2026-05-03T10:20:00+10:00",
      "ingested_at": "2026-05-03T10:25:00+10:00",
      "chunk_count": 12,
      "embedding_model": "text-embedding-3-small",
      "chunking": {
        "strategy": "recursive_text_splitter",
        "chunk_size": 800,
        "chunk_overlap": 150
      },
      "metadata": {
        "owner": "product",
        "visibility": "internal",
        "language": "en"
      }
    }
  ]
}
```

## Important Fields

Recommended core fields:

```text
source_id
source_path
content_hash
status
ingested_at
chunk_count
embedding_model
```

Optional but useful fields:

```text
source_type
title
category
last_modified_at
chunking
metadata
```

## Status Values

Suggested source statuses:

```text
active
deleted
failed
pending
```

Meanings:

- `active`: source is available and has been ingested.
- `deleted`: source was removed and related chunks or embeddings should be deleted.
- `failed`: ingestion failed and should be retried or inspected.
- `pending`: source was discovered but has not been ingested yet.

## How Ingestion Uses It

During ingestion:

1. Scan `knowledge_base/sources/`.
2. Calculate a `content_hash` for each source.
3. Compare the current scan with `sources.json`.
4. Skip unchanged sources.
5. Ingest new sources.
6. Re-ingest changed sources.
7. Delete chunks and embeddings for removed sources.
8. Update the registry after a successful run.

## Recommendation

Start with a simple `knowledge_base/manifests/sources.json` file.

Keep the first version small and include only:

```text
source_id
source_path
content_hash
status
ingested_at
chunk_count
embedding_model
```

Add richer metadata only when the RAG pipeline needs filtering, permissions, categories, or operational tracking.
