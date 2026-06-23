# Quick Start Guide

Get oriented with SAFF documentation in 5 minutes.

## 🎯 I want to...

### Understand what SAFF is
→ Start with [Main README](./README.md) **Overview** section (2 min)

### Learn about SAFF specifications
→ Go to [Specifications](./1.%20Specifications/README.md) section (3 min)

### Understand how we parse SAFF PDFs
→ Read [Implementation Overview](./2.%20Implementation/README.md) (3 min)  
→ Then explore [Table Parsing Guide](./2.%20Implementation/table-parsing/) (5 min)

### See extraction results
→ Check [Extraction Results](./3.%20Extraction%20Results/README.md) (2 min)

### Find external resources
→ Visit [Resources & References](./4.%20Resources/README.md) (5 min)

### Dive into source code
→ Read [Source Code Reference](./2.%20Implementation/source-code.md) (5 min)

---

## 🗂️ Documentation Map

```
docs/2. SAFF/
├── README.md                    ← START HERE for overview
├── Quick Start (this file)
│
├── 1. Specifications/           ← What is SAFF?
│   ├── README.md
│   ├── gesb-specification.md
│   ├── ato-saff-format.md
│   └── csc-pssap-extended.md
│
├── 2. Implementation/           ← How do we parse it?
│   ├── README.md
│   ├── parser-logic.md
│   ├── source-code.md
│   └── table-parsing/
│       ├── README.md
│       ├── pymupdf-patterns.md        ← Reusable patterns
│       ├── quality-issues.md          ← Known challenges
│       └── implementation-plan.md     ← Development roadmap
│
├── 3. Extraction Results/       ← What did we extract?
│   └── README.md                ← Points to JSON artifacts
│
└── 4. Resources/                ← Where can I learn more?
    └── README.md                ← External links & guides
```

---

## 📍 Find Content by Role

### If you're a **Developer**
1. [Implementation Overview](./2.%20Implementation/README.md)
2. [Source Code Reference](./2.%20Implementation/source-code.md)
3. [PyMuPDF Patterns](./2.%20Implementation/table-parsing/pymupdf-patterns.md)
4. [Quality Issues](./2.%20Implementation/table-parsing/quality-issues.md)

### If you're a **Compliance Officer**
1. [Resources](./4.%20Resources/README.md) → External Resources section
2. [Specifications](./1.%20Specifications/README.md)
3. [Resources](./4.%20Resources/README.md) → Domain Glossary

### If you're a **Data Analyst**
1. [Extraction Results](./3.%20Extraction%20Results/README.md)
2. [Specifications](./1.%20Specifications/README.md)
3. [Implementation](./2.%20Implementation/table-parsing/) → Quality & Limitations

### If you're a **Product Manager**
1. [Main README](./README.md) → Overview section
2. [Implementation Plan](./2.%20Implementation/table-parsing/implementation-plan.md)
3. [Quality Issues](./2.%20Implementation/table-parsing/quality-issues.md) → Severity Classification

### If you're **Onboarding**
1. [Main README](./README.md)
2. [Quick Start](./QUICK-START.md) (this file)
3. [Specifications Overview](./1.%20Specifications/README.md)
4. [Resources](./4.%20Resources/README.md)

---

## 🔍 Find Specific Information

| What | Where |
|------|-------|
| SAFF overview | [Main README](./README.md) |
| SAFF format details | [Specifications](./1.%20Specifications/README.md) |
| Parser architecture | [Implementation Overview](./2.%20Implementation/README.md) |
| How we extract tables | [Table Parsing](./2.%20Implementation/table-parsing/README.md) |
| Extraction patterns | [PyMuPDF Patterns](./2.%20Implementation/table-parsing/pymupdf-patterns.md) |
| Known issues | [Quality Issues](./2.%20Implementation/table-parsing/quality-issues.md) |
| What we extracted | [Extraction Results](./3.%20Extraction%20Results/README.md) |
| External resources | [Resources](./4.%20Resources/README.md) |
| Source code | [Source Code Reference](./2.%20Implementation/source-code.md) |
| Development roadmap | [Implementation Plan](./2.%20Implementation/table-parsing/implementation-plan.md) |

---

## 🚀 Common Tasks

### Parse a SAFF PDF
```python
from contextbridge_parser.parsers.pdf.sources.gesb.saff import SAFFParser

parser = SAFFParser()
result = parser.parse_file('saff-specification.pdf')
```
→ See [Source Code Reference](./2.%20Implementation/source-code.md)

### Understand table extraction
1. Read [PyMuPDF Patterns](./2.%20Implementation/table-parsing/pymupdf-patterns.md)
2. Run the [Interactive Walkthrough](./2.%20Implementation/table-parsing/pymupdf-patterns.md#integration-with-parser)
3. Review [Quality Issues](./2.%20Implementation/table-parsing/quality-issues.md)

### Debug extraction problems
1. Check [Quality Issues](./2.%20Implementation/table-parsing/quality-issues.md)
2. Use debugging techniques from that section
3. Review [Known Limitations](./3.%20Extraction%20Results/README.md#known-limitations)

### Implement new feature
1. Review [Implementation Plan](./2.%20Implementation/table-parsing/implementation-plan.md)
2. Check [Quality Issues](./2.%20Implementation/table-parsing/quality-issues.md) for related challenges
3. Follow development workflow in [Source Code Reference](./2.%20Implementation/source-code.md)

### Find official guidance
→ See [Resources](./4.%20Resources/README.md) → External Resources

---

## 📚 Key Concepts

### SAFF (SuperStream Alternative File Format)
File-based format for superannuation contribution submission. Used when standard XML channels aren't appropriate.

→ Full details in [Specifications](./1.%20Specifications/README.md)

### PyMuPDF Table Parsing
Extracting tables from SAFF specification PDFs using word-level extraction and layout analysis.

→ Full details in [Table Parsing](./2.%20Implementation/table-parsing/)

### Extraction Results
Processed outputs (JSON artifacts) from parsing SAFF specifications.

→ Full details in [Extraction Results](./3.%20Extraction%20Results/README.md)

---

## ❓ FAQ

**Q: What is this documentation about?**
A: This is comprehensive documentation about SAFF (SuperStream Alternative File Format) including specifications, parser implementation, extraction results, and external resources.

**Q: Where do I start?**
A: Start with [Main README](./README.md) for a 5-minute overview, then navigate to the section relevant to your role.

**Q: Where is the source code?**
A: See [Source Code Reference](./2.%20Implementation/source-code.md) for locations and descriptions of all SAFF-related code.

**Q: How do I parse a SAFF PDF?**
A: See [Source Code Reference](./2.%20Implementation/source-code.md) and run `SAFFParser().parse_file('file.pdf')`.

**Q: What are known issues?**
A: See [Quality Issues](./2.%20Implementation/table-parsing/quality-issues.md) for comprehensive list of challenges and workarounds.

**Q: Where are external resources?**
A: See [Resources](./4.%20Resources/README.md) for official specifications, operational guides, and reference materials.

**Q: Is SAFF parsing production-ready?**
A: Basic parsing is ready. Advanced features (merged cells, multi-level headers) planned for Phase 3. See [Implementation Plan](./2.%20Implementation/table-parsing/implementation-plan.md).

**Q: How do I contribute improvements?**
A: See development workflow in [Source Code Reference](./2.%20Implementation/source-code.md) and [Implementation Plan](./2.%20Implementation/table-parsing/implementation-plan.md).

---

## 🎓 Learning Path

**For Beginners** (30 minutes):
1. [Main README](./README.md) - Overview (5 min)
2. [Specifications Overview](./1.%20Specifications/README.md) - What is SAFF (5 min)
3. [Implementation Overview](./2.%20Implementation/README.md) - How we parse it (5 min)
4. [Resources](./4.%20Resources/README.md) - Where to learn more (5 min)
5. [Quick Start](./QUICK-START.md) - This file (5 min)

**For Developers** (1 hour):
1. All of "For Beginners" above
2. [Source Code Reference](./2.%20Implementation/source-code.md) - Code organization (10 min)
3. [Table Parsing Overview](./2.%20Implementation/table-parsing/README.md) (10 min)
4. [PyMuPDF Patterns](./2.%20Implementation/table-parsing/pymupdf-patterns.md) - Core techniques (20 min)

**For Deep Dive** (2-3 hours):
1. All of "For Developers" above
2. [Quality Issues](./2.%20Implementation/table-parsing/quality-issues.md) - Challenges (15 min)
3. [Implementation Plan](./2.%20Implementation/table-parsing/implementation-plan.md) - Roadmap (15 min)
4. Run [Interactive Walkthrough](./2.%20Implementation/table-parsing/pymupdf-patterns.md#integration-with-parser) (30 min)
5. Review [Source Code](./2.%20Implementation/source-code.md) in IDE (30 min)

---

## 🔗 Navigation Tips

- **Back to Main Hub**: [SAFF Documentation Home](./README.md)
- **Section Navigation**: Each section has "Related Documentation" links
- **Quick Links**: Check the navigation table above
- **Search**: Use Ctrl+F to find specific topics within documents

---

## 📞 Support

- **Technical Questions**: See [Quality Issues](./2.%20Implementation/table-parsing/quality-issues.md) debugging section
- **API Questions**: See [Source Code Reference](./2.%20Implementation/source-code.md)
- **Specification Questions**: See [Specifications](./1.%20Specifications/README.md) and [Resources](./4.%20Resources/README.md)
- **Implementation Questions**: See [Implementation Plan](./2.%20Implementation/table-parsing/implementation-plan.md)

---

Last Updated: 2026-06-24  
Documentation Version: 1.0
