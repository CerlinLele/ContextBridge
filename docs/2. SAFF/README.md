# SuperStream Alternative File Format (SAFF) - Consolidated Documentation

This directory consolidates all SAFF-related documentation, specifications, implementations, and extraction results for the ContextBridge project.

## Directory Structure

```
docs/2. SAFF/
├── README.md                           # This file - navigation hub
├── 1. Specifications/                  # Official SAFF file format specifications
├── 2. Implementation/                  # Parser and extraction implementation
├── 3. Extraction Results/              # Processed/parsed data artifacts
└── 4. Resources/                       # Links and reference materials
```

## Quick Navigation

### 📋 Specifications
- [GESB SAFF Specification](./1.%20Specifications/gesb-specification.md)
- [CSC PSSAP Extended Data Requirements](./1.%20Specifications/csc-pssap-extended-requirements.md)
- [ATO Official SAFF Format](./1.%20Specifications/ato-saff-format.md)

### 🔧 Implementation
- [Parser Logic & Architecture](./2.%20Implementation/parser-logic.md)
- [PDF Table Parsing Approach](./2.%20Implementation/table-parsing/)
  - [PyMuPDF Table Parsing Patterns](./2.%20Implementation/table-parsing/pymupdf-patterns.md)
  - [Quality Issues & Mitigations](./2.%20Implementation/table-parsing/quality-issues.md)
  - [Implementation Plan](./2.%20Implementation/table-parsing/implementation-plan.md)
- [Source Code Reference](./2.%20Implementation/source-code.md)

### 📊 Extraction Results
- [GESB Specification - Dependency Trace](./3.%20Extraction%20Results/gesb-dependency-trace.json)
- [GESB Specification - PyMuPDF Table Analysis](./3.%20Extraction%20Results/gesb-pymupdf-tables.json)
- [GESB Specification - Full Parse](./3.%20Extraction%20Results/gesb-parsed.json)

### 📚 Resources
- [External Resources & Links](./4.%20Resources/external-links.md)
- [SAFF Operational Guides](./4.%20Resources/operational-guides.md)

---

## What is SAFF?

**SuperStream Alternative File Format (SAFF)** is an alternative file format for superannuation contribution data submission in Australia. It's used when standard SuperStream XML submission channels are not appropriate.

Key characteristics:
- File-based contribution submission format
- Used by employers and super funds
- Contains payroll and super contribution data
- Subject to field-level validation rules
- Typically provided as PDF specifications with tables and structured data

## Project Context

In ContextBridge, SAFF is used as:
1. **Test case** for complex PDF table parsing with PyMuPDF
2. **RAG demo context** for superannuation domain knowledge
3. **Reference implementation** for structured data extraction from specification PDFs

## Key Files Across the Project

### Knowledge Base
- **Sources**: `knowledge_base/sources/structured-business-file-formats/saff/`
  - Raw PDFs and documents
  - Mercer operator guides
  - CSC PSSAP specifications
  
- **Processed**: `knowledge_base/processed/structured-business-file-formats/saff/`
  - Extracted JSON and parse results
  - Dependency traces
  - Table analyses

### Parser Implementation
- **Main module**: `src/contextbridge_parser/parsers/pdf/sources/gesb/saff.py`
- **Experiments**: `src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment.py`
- **Notebooks**: `src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment_walkthrough.ipynb`

### Documentation
- **Parser Logic**: `src/contextbridge_parser/parsers/pdf/sources/gesb/docs/parser_logic.md`
- **Table Parsing Tools**: `src/contextbridge_parser/parsers/pdf/sources/gesb/docs/table parsing/table_parsing_tools.md`
- **PyMuPDF Experiments**: `src/contextbridge_parser/parsers/pdf/sources/gesb/docs/table parsing/PyMuPDF/`

---

## Recent Work

**Latest commits** (from `feature/rag-pipeline` branch):
- Extract PDF table layout detection helpers
- Extract PyMuPDF word layer adapter
- Capture reusable PyMuPDF table parsing patterns
- Move PyMuPDF quality notes under table parsing
- Add GESB PyMuPDF extraction notebook

**Current focus**: Consolidating scattered PyMuPDF table parsing documentation and making patterns reusable.

---

## Next Steps

1. **Review** each section to understand the current state
2. **Link** documentation together with cross-references
3. **Consolidate** parser logic documentation
4. **Update** implementation status as work progresses

---

## Questions?

- For **specification details**: See [1. Specifications](./1.%20Specifications/)
- For **parser implementation**: See [2. Implementation](./2.%20Implementation/)
- For **extraction results**: See [3. Extraction%20Results](./3.%20Extraction%20Results/)
- For **external references**: See [4. Resources](./4.%20Resources/)
