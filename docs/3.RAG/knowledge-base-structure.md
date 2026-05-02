# Knowledge Base Structure

## Recommendation

It is appropriate for a RAG knowledge base to have a file directory.

`knowledge_base` does not have to mean only a database. It can also be the local workspace for RAG source files, processed text, chunks, indexes, and metadata.

## Suggested Structure

```text
knowledge_base/
  sources/        # Original files maintained manually or uploaded by users
  processed/      # Cleaned text, optional
  chunks/         # Split text chunks, optional
  indexes/        # Local vector indexes, such as FAISS or Chroma, optional
  metadata/       # Document and chunk metadata, optional
```

## Minimal V1 Structure

For the first version, keep it simple:

```text
knowledge_base/
  sources/
```

Only store original source files in `knowledge_base/sources/`. Chunks, embeddings, and indexes can be stored in a database or generated later.

## Git Tracking Guidance

Recommended to track in Git:

```text
knowledge_base/sources/
```

This is suitable when the files are:

- Small
- Non-sensitive
- Stable
- Intended to be part of the project knowledge base

Usually not recommended to track in Git:

```text
knowledge_base/indexes/
knowledge_base/processed/
knowledge_base/chunks/
```

These are often generated artifacts and may become large.

Suggested `.gitignore` entries:

```gitignore
knowledge_base/indexes/
knowledge_base/processed/
knowledge_base/chunks/
```

## Sensitive Data

Do not commit sensitive documents or user-uploaded private files directly into Git.

For sensitive or user-specific knowledge sources, use external storage, a private database, or an ignored local folder.

## Final Recommendation

Start with:

```text
knowledge_base/
  sources/
```

Then add `processed/`, `chunks/`, `indexes/`, and `metadata/` only when the RAG pipeline needs them.
