# Parser Implementation Reference

This document provides a reference to the SAFF parser implementation across the codebase.

## Main Parser Module

### File: `src/contextbridge_parser/parsers/pdf/sources/gesb/saff.py`

**Purpose**: Production SAFF parser implementation

**Key Components**:
- `SAFFParser` class - Main parser interface
- `SAFFSpecificationExtractor` - Specification extraction
- `FieldDefinitionExtractor` - Field definition parsing
- `ValidationRuleExtractor` - Validation rule parsing

**Responsibilities**:
- Parse SAFF specification PDFs
- Extract field definitions
- Extract validation rules
- Generate structured output
- Handle errors gracefully

**Usage**:
```python
from contextbridge_parser.parsers.pdf.sources.gesb.saff import SAFFParser

parser = SAFFParser()
result = parser.parse_file('saff-specification.pdf')
```

**Status**: Active, production-ready for basic extraction

---

## Experimental & Research Code

### File: `src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment.py`

**Purpose**: Experimental table parsing implementation

**Key Functions**:
- `extract_words_from_page()` - Word-level extraction
- `detect_column_boundaries()` - Column boundary detection
- `detect_row_boundaries()` - Row boundary detection
- `reconstruct_table_cells()` - Cell reconstruction
- `group_content_in_cells()` - Multi-line content handling

**Features**:
- PyMuPDF word-layer extraction
- Coordinate-based layout analysis
- Table structure inference
- Content grouping algorithms

**Status**: Research/experimental, patterns documented for production use

---

## Interactive Walkthrough

### File: `src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment_walkthrough.ipynb`

**Purpose**: Interactive exploration and documentation of table parsing techniques

**Sections**:
1. PDF loading and PyMuPDF integration
2. Page analysis and word extraction
3. Coordinate system and layout analysis
4. Column and row boundary detection
5. Table structure reconstruction
6. Content extraction and validation
7. Results visualization

**Run Notebook**:
```bash
jupyter notebook src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment_walkthrough.ipynb
```

**Status**: Reference implementation, excellent for learning the approach

---

## Documentation Structure

### Parser Logic Architecture

**File**: `src/contextbridge_parser/parsers/pdf/sources/gesb/docs/parser_logic.md`

Documents the overall architecture, design decisions, and pipeline stages. Link to this for:
- Architecture overview
- Pipeline stages
- Design rationale
- Integration points

### Table Parsing Tools Reference

**File**: `src/contextbridge_parser/parsers/pdf/sources/gesb/docs/table parsing/table_parsing_tools.md`

Reference for available tools and techniques. Use this for:
- Tool availability
- Technique descriptions
- Usage examples
- Limitations and considerations

### PyMuPDF Table Parsing Documentation

**Directory**: `src/contextbridge_parser/parsers/pdf/sources/gesb/docs/table parsing/PyMuPDF/`

Detailed documentation on PyMuPDF-specific approaches:
- `pymupdf_table_experiment_logic.md` - Logic and algorithms
- `pymupdf_table_experiment_quality_issues.md` - Quality issues
- `pymupdf_table_experiment_reusable_patterns.md` - Reusable patterns
- `pymupdf_table_experiment_implementation_plan.md` - Implementation roadmap

---

## Code Organization

```
src/contextbridge_parser/
└── parsers/
    └── pdf/
        └── sources/
            └── gesb/
                ├── saff.py                                    # Main production module
                ├── pymupdf_table_experiment.py               # Experimental code
                ├── pymupdf_table_experiment_walkthrough.ipynb # Interactive walkthrough
                ├── __init__.py
                └── docs/
                    ├── parser_logic.md                       # Architecture
                    ├── table parsing/
                    │   ├── table_parsing_tools.md
                    │   └── PyMuPDF/
                    │       ├── pymupdf_table_experiment_logic.md
                    │       ├── pymupdf_table_experiment_quality_issues.md
                    │       ├── pymupdf_table_experiment_reusable_patterns.md
                    │       └── pymupdf_table_experiment_implementation_plan.md
```

---

## Implementation Status

### ✅ Completed Components

1. **Basic PDF Loading** - PyMuPDF integration
2. **Word Extraction** - Word-level content from PDFs
3. **Layout Analysis** - Coordinate-based position analysis
4. **Boundary Detection** - Column and row boundary inference
5. **Cell Reconstruction** - Basic table structure building
6. **Pattern Documentation** - Reusable extraction patterns

### 🔄 In Progress

1. **Unified Parser** - Consolidating patterns into production parser
2. **Error Handling** - Comprehensive error recovery
3. **Quality Metrics** - Confidence scoring and diagnostics

### 📋 Planned

1. **Merged Cell Handling** - Advanced cell reconstruction
2. **Multi-Level Headers** - Complex header structures
3. **Performance Optimization** - Speed and memory improvements
4. **Advanced Features** - Additional extraction capabilities

---

## Key Dependencies

### Python Packages
- `fitz` (PyMuPDF) - PDF analysis and word extraction
- `json` - JSON output format
- `logging` - Diagnostics and debugging

### Internal Dependencies
- `contextbridge_parser.parsers.pdf` - PDF parser framework
- Specification files from knowledge_base

---

## Development Workflow

### Adding New Features

1. **Prototype** in `pymupdf_table_experiment.py`
2. **Document** patterns in implementation guide
3. **Test** with real SAFF specifications
4. **Integrate** into `saff.py`
5. **Update** documentation

### Testing

```bash
# Run unit tests
pytest src/contextbridge_parser/parsers/pdf/sources/gesb/

# Run walkthrough notebook
jupyter notebook src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment_walkthrough.ipynb

# Test with specific PDF
python -c "from contextbridge_parser.parsers.pdf.sources.gesb.saff import SAFFParser; SAFFParser().parse_file('spec.pdf')"
```

### Debugging

Enable verbose logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Use diagnostic output:
```python
from contextbridge_parser.parsers.pdf.sources.gesb.pymupdf_table_experiment import visualize_extraction
visualize_extraction(pdf_page, show_coordinates=True, show_boundaries=True)
```

---

## Integration Points

### RAG Context Integration
- [Extraction Results](../../3.%20Extraction%20Results/) for indexed content
- Parsed SAFF specs available for retrieval

### Parser Pipeline
- Integrates with `contextbridge_parser` framework
- Follows standard PDF parser interface
- Supports streaming and batch processing

### Knowledge Base
- Source files: `knowledge_base/sources/structured-business-file-formats/saff/`
- Processed results: `knowledge_base/processed/structured-business-file-formats/saff/`

---

## Performance Characteristics

### Current Performance (Baseline)
- **Typical spec** (~25 pages): ~15-20 seconds
- **Memory usage**: ~100-200 MB
- **Table extraction accuracy**: ~85-90%

### Performance Goals (Phase 3)
- **Typical spec**: <10 seconds
- **Memory usage**: <100 MB
- **Table extraction accuracy**: >95%

---

## Contributing to Parser

### Code Style
- Follow PEP 8 conventions
- Use type hints where practical
- Add docstrings to public functions
- Keep functions focused and testable

### Adding Patterns
1. Document pattern in `pymupdf_table_experiment.py`
2. Add to [PyMuPDF Patterns](../../2.%20Implementation/table-parsing/pymupdf-patterns.md)
3. Create tests
4. Integrate into production parser

### Documentation
- Update relevant documentation when making changes
- Link new components to existing docs
- Add examples for new features
- Keep implementation plan in sync

---

## Related Documentation

- [Implementation Overview](../README.md) - Broader context
- [Table Parsing Guide](../table-parsing/) - Specific techniques
- [PyMuPDF Patterns](../table-parsing/pymupdf-patterns.md) - Core patterns
- [Quality Issues](../table-parsing/quality-issues.md) - Known challenges
- [Implementation Plan](../table-parsing/implementation-plan.md) - Development roadmap
