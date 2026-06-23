# SAFF Table Parsing

This section documents the technical approach to extracting tables from SAFF specification PDFs.

## Overview

The SAFF specifications (especially from GESB) contain complex tables with structured payroll data, field definitions, and validation rules. This section consolidates the technical approach for extracting and analyzing these tables using PyMuPDF.

## Documentation

### [PyMuPDF Patterns](./pymupdf-patterns.md)
**Reusable extraction patterns and techniques**

Documents the core patterns used for table extraction:
- Word-level extraction
- Spatial clustering
- Header detection
- Cell boundary inference
- Multi-row content handling

**Use this when**: Understanding how tables are extracted

---

### [Quality Issues & Mitigations](./quality-issues.md)
**Known challenges and solutions**

Catalogs known issues with their severity and workarounds:
- Layout & structure issues (merged cells, variable widths)
- Content extraction issues (multi-line, overlapping text)
- Table-specific issues (header identification, missing values)
- Performance considerations

**Use this when**: Debugging extraction problems or understanding limitations

---

### [Implementation Plan](./implementation-plan.md)
**Development roadmap and milestones**

Outlines the phased approach to building production-ready table parsing:
- Phase 1: Foundation (pattern extraction, documentation)
- Phase 2: Core Parser (unified implementation)
- Phase 3: Advanced Features (merged cells, optimization)
- Phase 4: Production Ready (comprehensive testing)

**Use this when**: Planning development work or understanding project status

---

## Key Files

| File | Purpose | Status |
|------|---------|--------|
| `src/contextbridge_parser/parsers/pdf/sources/gesb/saff.py` | Main SAFF parser | Active |
| `src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment.py` | Experimental code | Research |
| `src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment_walkthrough.ipynb` | Interactive walkthrough | Reference |

---

## Quick Start

### Understand the Approach
1. Read [PyMuPDF Patterns](./pymupdf-patterns.md) for core techniques
2. Review [Quality Issues](./quality-issues.md) for known challenges
3. Check [Implementation Plan](./implementation-plan.md) for development status

### Explore the Code
1. Run `pymupdf_table_experiment_walkthrough.ipynb` for interactive exploration
2. Review `pymupdf_table_experiment.py` for experimental techniques
3. Study `saff.py` for production implementation

### Debug Issues
1. Consult [Quality Issues](./quality-issues.md) for your specific problem
2. Use debugging techniques from that section
3. Check coordinate analysis and boundary validation

---

## Current State

### ✅ Completed
- Core patterns identified and documented
- Quality issues cataloged with severity
- Experimental code working with real SAFF PDFs
- Walkthrough notebook demonstrating techniques

### 🔄 In Progress
- Consolidating utilities from experimental code
- Creating unified pattern library
- Planning Phase 2 implementation

### 📋 Planned
- Build unified table parser from patterns
- Implement advanced features (merged cells, multi-level headers)
- Comprehensive testing and optimization

---

## Related Sections

- [Specifications](../1.%20Specifications/) - SAFF format details
- [Parser Logic](../parser-logic.md) - Architecture overview
- [Implementation Overview](../README.md) - Broader context
