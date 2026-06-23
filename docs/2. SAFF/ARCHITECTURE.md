# SAFF Documentation Architecture

This document provides a visual and conceptual overview of how all SAFF documentation, code, and knowledge base artifacts fit together.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAFF Documentation Hub                        │
│                  docs/2. SAFF/README.md                          │
│  (Central navigation, overview, and cross-linking point)         │
└──────────────────────┬──────────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼              ▼
    ┌─────────┐  ┌──────────────┐  ┌──────────┐  ┌────────────┐
    │  Quick  │  │ Specifi-     │  │Implement-│  │ Extraction │
    │  Start  │  │  cations     │  │ ation    │  │  Results   │
    │ Guide   │  │              │  │          │  │            │
    └─────────┘  └──────────────┘  └──────────┘  └────────────┘
         │             │                 │              │
         │             │                 ▼              │
         │             │        ┌──────────────────┐   │
         │             │        │ Table Parsing    │   │
         │             │        │ (PyMuPDF)        │   │
         │             │        └──────────────────┘   │
         │             │                               │
         └─────────────┴───────────────────────────────┘
                       │
         ┌─────────────┴─────────────┐
         │                           │
         ▼                           ▼
    ┌──────────────┐         ┌────────────────┐
    │   Resources  │         │  External      │
    │  & Reference │         │  References    │
    └──────────────┘         └────────────────┘
```

## Data Flow: From Source to Usage

```
SAFF Specification PDFs
│
├─ GESB Specification
│   └─ superstream-payroll-data-specification.pdf
│
├─ Mercer Operator Guide
│   └─ saff-support-guide-employer-portal.pdf
│
└─ CSC PSSAP Requirements
    └─ pssap-saff-extended-data-requirements.pdf
            │
            ▼
     ┌─────────────────────────────────────────┐
     │  Parser Implementation Layer            │
     ├─────────────────────────────────────────┤
     │  saff.py (Production)                   │
     │  pymupdf_table_experiment.py (Research) │
     │  PyMuPDF word layer + Layout Analysis   │
     └────────────┬────────────────────────────┘
                  │
      ┌───────────┼───────────┐
      │           │           │
      ▼           ▼           ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│Dependency│ │ PyMuPDF  │ │  Parsed  │
│  Trace   │ │  Tables  │ │ Content  │
└──────────┘ └──────────┘ └──────────┘
      │           │           │
      └───────────┼───────────┘
                  │
                  ▼
     ┌────────────────────────────────┐
     │  Usage Layers                  │
     ├────────────────────────────────┤
     │  • RAG Context Retrieval       │
     │  • Field Mapping Reference     │
     │  • Validation Rule Extraction  │
     │  • Testing & Validation        │
     └────────────────────────────────┘
```

## Documentation Layers

```
Layer 1: Navigation & Orientation
├─ README.md (Main Hub)
├─ QUICK-START.md (Role-based paths)
└─ INDEX.md (This architecture doc)

Layer 2: Conceptual Understanding
├─ Specifications/ (What is SAFF?)
├─ Resources/ (Where to learn more?)
└─ Implementation/README.md (How does it work?)

Layer 3: Technical Implementation
├─ Implementation/source-code.md (Code organization)
├─ Table Parsing/ (PyMuPDF techniques)
└─ Implementation/parser-logic.md (Architecture)

Layer 4: Detailed Reference
├─ PyMuPDF Patterns (Reusable techniques)
├─ Quality Issues (Known challenges)
├─ Implementation Plan (Development roadmap)
└─ Extraction Results (Output artifacts)

Layer 5: Source & Integration
├─ src/contextbridge_parser/ (Production code)
├─ knowledge_base/sources/ (Raw PDFs)
├─ knowledge_base/processed/ (Extracted data)
└─ External Resources (Official documentation)
```

## Information Organization by Audience

```
Developer Path
└─ Quick Start
   └─ Implementation Overview
      ├─ Table Parsing Guide
      │  ├─ PyMuPDF Patterns
      │  ├─ Quality Issues
      │  └─ Implementation Plan
      └─ Source Code Reference
         └─ Review actual code

Compliance/Manager Path
└─ Quick Start
   └─ Specifications
      └─ Resources & External Links
         ├─ Official Guidance
         └─ Regulatory Context

Analyst Path
└─ Quick Start
   └─ Extraction Results
      ├─ Specification Details
      └─ Resources (Field Reference)

New Hire Path
└─ Quick Start
   ├─ Overview
   └─ Choose role-based path above
```

## Cross-Reference Map

```
README.md (Hub)
├─ Specifications ──┐
├─ Implementation   ├─ All cross-linked
├─ Results    ──────┤
└─ Resources ───────┘
    │
    ├─ Table Parsing ──→ PyMuPDF Patterns ──→ Quality Issues
    │                        │                      │
    │                        └──→ Implementation Plan ──→ Source Code
    │
    ├─ Extraction Results ──→ Specifications ──→ Resources
    │
    └─ Source Code ──→ Links back to all sections
```

## Knowledge Base Integration

```
Knowledge Base Structure
│
├─ sources/ (Raw Input)
│  └─ structured-business-file-formats/saff/
│     ├─ official/ato/
│     ├─ specifications/
│     │  ├─ gesb/
│     │  └─ csc-pssap/
│     └─ operational-guides/mercer/
│
├─ processed/ (Extracted Output)
│  └─ structured-business-file-formats/saff/
│     └─ specifications/gesb/
│        ├─ dependency-trace.json
│        ├─ pymupdf-tables.json
│        └─ parsed.json
│
└─ Documented in: docs/2. SAFF/
   ├─ 1. Specifications/ (References sources)
   ├─ 3. Extraction Results/ (Indexes processed)
   └─ 4. Resources/ (Links to materials)
```

## Implementation Phases & Documentation

```
Phase 1: Foundation (Current)
├─ ✅ Patterns extracted
├─ ✅ Documented in PyMuPDF Patterns
├─ ✅ Quality issues cataloged
└─ ✅ Initial implementation plan
    Docs: pyrmupdfl-patterns.md, quality-issues.md, implementation-plan.md

Phase 2: Core Parser
├─ 🔄 Unified parser implementation
├─ 📋 Integration testing
├─ 📋 Performance baseline
└─ 📋 Documentation updates
    Docs: Update Implementation Overview & Plan

Phase 3: Advanced Features
├─ 📋 Merged cell handling
├─ 📋 Multi-level headers
├─ 📋 Performance optimization
└─ 📋 Advanced features doc
    Docs: Add advanced techniques documentation

Phase 4: Production Ready
├─ 📋 Comprehensive testing
├─ 📋 Production validation
├─ 📋 Documentation complete
└─ 📋 Deployment preparation
    Docs: Production guide, monitoring guide
```

## Search & Discovery

### By Question

| Question | Answer Location |
|----------|-----------------|
| What is SAFF? | Specifications/README.md |
| How do we parse SAFF? | Implementation/README.md |
| What are known issues? | table-parsing/quality-issues.md |
| Where's the source code? | Implementation/source-code.md |
| What did we extract? | Extraction Results/README.md |
| Where are external specs? | Resources/README.md |
| How do I get started? | QUICK-START.md |
| What's the development plan? | table-parsing/implementation-plan.md |

### By Topic

| Topic | Primary Location | Secondary Locations |
|-------|-----------------|-------------------|
| Specifications | 1. Specifications/ | 4. Resources/ |
| Implementation | 2. Implementation/ | Source Code, notebook |
| Table Parsing | 2.Implementation/table-parsing/ | Code experiments |
| Extraction | 3. Extraction Results/ | Knowledge base/processed |
| External Resources | 4. Resources/ | Specifications (links) |
| Development Status | table-parsing/implementation-plan.md | README files |

## File Relationship Diagram

```
docs/2. SAFF/
│
├─ README.md (Hub)
│  └─ References all sections
│
├─ QUICK-START.md (Entry)
│  └─ Role-based navigation
│
├─ INDEX.md (This doc)
│  └─ Architecture overview
│
├─ 1. Specifications/
│  └─ README.md
│     └─ Links to: Resources, Implementation
│
├─ 2. Implementation/
│  ├─ README.md
│  │  └─ Links to: Specifications, Table Parsing, Source Code
│  │
│  ├─ source-code.md
│  │  └─ Links to: Implementation files, code organization
│  │
│  ├─ parser-logic.md
│  │  └─ [File at src/.../docs/parser_logic.md - linked]
│  │
│  └─ table-parsing/
│     ├─ README.md
│     │  └─ Overview and structure
│     │
│     ├─ pymupdf-patterns.md
│     │  └─ Core techniques
│     │
│     ├─ quality-issues.md
│     │  └─ Known challenges
│     │
│     └─ implementation-plan.md
│        └─ Development roadmap
│
├─ 3. Extraction Results/
│  └─ README.md
│     └─ Indexes JSON artifacts
│
└─ 4. Resources/
   └─ README.md
      └─ External links & guides
```

## Content Completeness Matrix

| Section | Content | Links | Status |
|---------|---------|-------|--------|
| Specifications | ✅ 3 specs | ✅ All linked | Complete |
| Implementation | ✅ Overview | ✅ All linked | Complete |
| Table Parsing | ✅ 4 docs | ✅ Cross-linked | Complete |
| Extraction | ✅ 3 artifacts | ✅ Indexed | Complete |
| Resources | ✅ 10+ links | ✅ Categorized | Complete |
| Quick Start | ✅ Complete | ✅ All paths | Complete |

## Navigation Recommendations

### For First Time
1. README.md (2 min)
2. QUICK-START.md (3 min)
3. Role-based section (10-20 min)

### For Implementation Work
1. source-code.md (5 min)
2. table-parsing/README.md (3 min)
3. Specific patterns or issues as needed

### For Onboarding New Dev
1. QUICK-START.md (5 min)
2. Specifications/README.md (5 min)
3. Implementation/README.md (5 min)
4. Assign role-based learning path

## Maintenance Schedule

### Weekly
- Monitor for broken links
- Track implementation progress

### Monthly
- Review quality issues for new entries
- Update implementation plan with progress
- Check external resource links

### Quarterly
- Major documentation review
- Archive completed phases
- Plan next phase documentation

---

## Related Documents

- [Main README](./README.md) - Hub and overview
- [Quick Start](./QUICK-START.md) - Getting oriented
- [Consolidation Summary](./INDEX.md) - What was organized
