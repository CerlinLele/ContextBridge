# PDF Table Parsing Strategy

PDFs with tables should usually be parsed with a generic extraction layer plus a
source-specific interpretation layer.

PDF does not preserve table semantics in the same way as HTML or spreadsheets.
Most tables are reconstructed from text blocks, line positions, coordinates, and
visual layout. A generic parser can extract useful primitives, but it usually
cannot reliably infer source-specific business meaning.

## Recommended Architecture

```text
PDF generic layer
-> source/profile-specific parser
-> normalized domain schema
```

## Generic PDF Layer

The generic layer should handle reusable PDF concerns:

```text
metadata
page text
page dimensions
text blocks, spans, and coordinates
image counts
candidate table regions
raw table cells when available
OCR fallback signals
dependency trace
```

This layer should avoid embedding source-specific business rules.

## Source-Specific Parser Layer

The source-specific layer should handle document-specific and business-specific
interpretation:

```text
table page ranges
section heading rules
header and footer removal
cross-page row continuation
row and cell repair
business field mapping
mandatory, data type, length, format, value, and reference extraction
quality notes
```

For example, fields such as `Column`, `Field Name`, `Mandatory`,
`Required by GESB`, `Data Type`, `Length`, and `Format` belong in a
GESB SAFF-specific parser or profile, not in the generic PDF layer.

## Practical Boundary

A useful directory split is:

```text
pdf/common/
  metadata.py
  pages.py
  text.py
  tables.py

pdf/profiles/
  table_aware_specification.py

pdf/sources/gesb/
  saff.py
  parser_logic.md
```

## Rule of Thumb

Table extraction tooling can be generic. Table interpretation should be
customized per source or profile.

Keeping this boundary prevents one document's heuristics from leaking into
other parsers while still sharing low-level PDF processing utilities.
