# RAG Implementation Plan

## Goal

Build a minimal but complete RAG pipeline:

```text
User question -> retrieve relevant knowledge -> compose context -> generate answer -> return answer with sources
```

The first version should focus on proving the core loop works:

- Ingest documents into a searchable knowledge base.
- Retrieve relevant chunks for a user query.
- Generate an answer grounded in retrieved context.
- Return citations or source references with the answer.

## Phase 1: Define Scope

Start with one clear knowledge source instead of supporting everything at once.

Possible sources:

- Local documents: PDF, Markdown, TXT, Word
- Internal project data: database records, APIs, logs, business records
- User-uploaded files
- Web pages

Recommended first version:

- Use a `docs/` folder as the initial knowledge source.
- Support Markdown first.
- Add PDF support after the core ingestion and query flow is stable.

## Phase 2: Document Ingestion

Create an ingestion pipeline with these steps:

1. Read source documents.
2. Extract and clean text.
3. Split text into chunks.
4. Generate embeddings for each chunk.
5. Store chunks, metadata, and embeddings in a vector store.

Recommended chunking strategy for v1:

- Chunk size: 500-1000 tokens
- Overlap: 100-200 tokens
- Preserve source metadata such as filename, title, page number, section, and chunk index.

Suggested chunk schema:

```text
id
source
title
chunk_text
chunk_index
embedding
metadata
created_at
```

## Phase 3: Choose Vector Storage

Options:

- Chroma: fastest for local development
- FAISS: lightweight local vector search
- pgvector: good if the project already uses PostgreSQL
- Qdrant, Weaviate, Pinecone: stronger options for production or hosted vector search

Recommendation:

- Use `pgvector` if the project already has PostgreSQL.
- Otherwise use `Chroma` for the first prototype.

## Phase 4: Build Retrieval

Create a retrieval service with this input:

```text
query
top_k
filters optional
```

Return:

```text
matched_chunks
score
source metadata
```

First version:

```text
query -> embedding -> vector search -> top_k chunks
```

Later improvements:

- Hybrid search: keyword search + vector search
- Reranking: reorder retrieved chunks before generation
- Metadata filters: filter by file, time, user, project, or document type
- Query rewriting: improve vague or conversational user questions before search

## Phase 5: Generate Answers

Compose a prompt using retrieved chunks as context.

Core behavior:

- The model should answer only from provided context.
- If the context does not contain the answer, it should say it does not know.
- The response should include source references.

Suggested output shape:

```json
{
  "answer": "...",
  "sources": [
    {
      "title": "...",
      "source": "...",
      "chunk_id": "..."
    }
  ]
}
```

## Phase 6: API Design

Minimum API surface:

```http
POST /rag/ingest
POST /rag/query
GET /rag/sources
DELETE /rag/sources/{id}
```

Optional frontend views:

- Upload or select documents.
- Show ingestion status.
- Ask questions against the knowledge base.
- Display answer sources.
- Click a source to inspect the original text chunk.

## Phase 7: Quality Evaluation

Do not only check whether the model returns an answer. Evaluate whether the answer is grounded and useful.

Key checks:

- Are citations correct?
- Does the answer avoid hallucination?
- Are chunks too small or too large?
- Is `top_k` retrieving enough useful context?
- Does the model say it does not know when context is missing?
- Are source snippets relevant to the final answer?

Create a small eval set:

- 10-20 fixed questions
- Expected source documents
- Expected answer points
- Cases where the correct behavior is "I do not know"

## Recommended Development Order

1. Create branch: `feature/rag-pipeline`
2. Implement document loader.
3. Implement text cleaner and chunker.
4. Connect embedding generation.
5. Connect vector storage.
6. Implement query retrieval.
7. Implement answer generation.
8. Add citations and source references.
9. Add focused tests and eval examples.
10. Add reranking, hybrid search, and permission filters after the v1 loop works.

## V1 Definition of Done

The first version is complete when:

- A batch of documents can be ingested.
- User questions retrieve relevant chunks.
- The system returns an answer based on retrieved context.
- The answer includes source references.
- Missing knowledge produces a clear "I do not know" style response instead of a hallucinated answer.
