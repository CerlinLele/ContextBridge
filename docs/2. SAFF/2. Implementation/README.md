# SAFF Implementation

This section documents the parser implementation, table extraction strategies, and technical approaches used in ContextBridge to process SAFF specifications and extract structured data.

## Architecture Overview

```
Parser Pipeline
├── PDF Input (SAFF Specification)
├── Page Analysis (Layout Detection)
├── Table Detection & Extraction (PyMuPDF)
├── Content Processing
└── Structured Output (JSON/Parsed Format)
```

## Main Components

### 1. Parser Logic & Architecture
**File**: `src/contextbridge_parser/parsers/pdf/sources/gesb/parser_logic.md`

Covers:
- Overall parser design
- Module structure
- Processing pipeline stages
- Integration points

**Related Code**: `src/contextbridge_parser/parsers/pdf/sources/gesb/saff.py`

---

### 2. Table Parsing Strategy
**Documentation**: `table-parsing/` subdirectory

The GESB SAFF specification contains complex tables with:
- Multi-row headers
- Merged cells
- Nested structures
- Variable column widths
- Mixed content types

**Approach**: PyMuPDF word layer extraction with layout analysis

**Key Documents**:
- [`pymupdf-patterns.md`](./table-parsing/pymupdf-patterns.md) - Reusable extraction patterns
- [`quality-issues.md`](./table-parsing/quality-issues.md) - Known issues and mitigations
- [`implementation-plan.md`](./table-parsing/implementation-plan.md) - Development roadmap

**Key Files**:
- `src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment.py` - Experimentation code
- `src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment_walkthrough.ipynb` - Walkthrough notebook

---

### 3. PyMuPDF Word Layer Adapter
**Extracted From**: `pymupdf_table_experiment_walkthrough.ipynb`

Provides:
- Word-level extraction helpers
- Layout detection utilities
- Coordinate-based table analysis
- Content grouping algorithms

**Status**: Patterns extracted and documented, ready for reuse

---

## Implementation Files Reference

| File | Purpose | Status |
|------|---------|--------|
| `saff.py` | Main SAFF parser module | Active |
| `pymupdf_table_experiment.py` | Table parsing experimentation | Research |
| `pymupdf_table_experiment_walkthrough.ipynb` | Interactive exploration notebook | Reference |
| `parser_logic.md` | Architecture documentation | Active |
| `table_parsing_tools.md` | Tool reference | Active |

---

## Table Parsing Tools & Techniques

**Reference**: `src/contextbridge_parser/parsers/pdf/sources/gesb/docs/table parsing/table_parsing_tools.md`

Available techniques:
- PyMuPDF word extraction
- Layout analysis
- Column detection
- Row grouping
- Cell boundary inference

---

## Experimental Notebook

**File**: `src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment_walkthrough.ipynb`

**Purpose**: Interactive walkthrough of SAFF table parsing

**Covers**:
- GESB specification loading
- PyMuPDF extraction techniques
- Table analysis step-by-step
- Result visualization
- Pattern identification

**Run**: 
```bash
jupyter notebook src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment_walkthrough.ipynb
```

---

## Current State

### ✅ Completed
- PDF layout detection helpers extracted
- PyMuPDF word layer adapter documented
- Reusable table parsing patterns captured
- Quality issues documented and categorized
- Implementation approach defined

### 🔄 In Progress
- Consolidating pattern library
- Creating reusable extraction utilities
- Documenting edge cases

### 📋 Next Steps
- Build unified table parser from patterns
- Add comprehensive error handling
- Create test suite for table extraction
- Document performance characteristics

---

## Key Insights

1. **Layout Detection**: SAFF tables have consistent structure that can be analyzed programmatically
2. **Word-Level Extraction**: PyMuPDF word layer provides better accuracy than line-based extraction
3. **Quality Challenges**: Some tables have formatting that challenges automatic extraction
4. **Reusable Patterns**: Many parsing operations can be abstracted into helper functions

---

## Related Documentation

- [Specifications](../1.%20Specifications/) - SAFF format details
- [Extraction Results](../3.%20Extraction%20Results/) - Output from parser
- [PyMuPDF Patterns](./table-parsing/pymupdf-patterns.md) - Specific techniques
- [Quality Issues](./table-parsing/quality-issues.md) - Known limitations
- [Implementation Plan](./table-parsing/implementation-plan.md) - Development roadmap

---

## Debugging & Development

### Enable Verbose Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Table Extraction
```bash
python -m contextbridge_parser.parsers.pdf.sources.gesb.pymupdf_table_experiment
```

### Run Walkthrough
```bash
jupyter notebook pymupdf_table_experiment_walkthrough.ipynb
```

---

## Questions?

- **How does table parsing work?** → See [PyMuPDF Patterns](./table-parsing/pymupdf-patterns.md)
- **What are known issues?** → See [Quality Issues](./table-parsing/quality-issues.md)
- **What's the development plan?** → See [Implementation Plan](./table-parsing/implementation-plan.md)
- **How do I extend parsing?** → See [Parser Logic](./parser-logic.md)
