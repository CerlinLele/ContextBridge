# GESB SAFF Table Parsing Tools

## Problem

The current `field_rows` extraction is not accurate enough for the SAFF field
specification tables.

The table layout is not a simple flat row structure. Each outer row has the
main columns:

```text
Column
Field Name
Description
Requirements
Required by GESB?
MIG 2.0 Reference
DES Spec 5.8 Reference
```

The `Requirements` cell also behaves like a small nested key-value table:

```text
Mandatory:  Yes
Data Type:  String
Length:     7
Value(s):   VERSION
```

Text-only extraction flattens this into one stream, for example:

```text
Mandatory: Yes No N/A N/A Data Type: String Length: 7 Value(s): VERSION
```

That loses column boundaries and can mix the `Required by GESB?`, `MIG`, and
`DES` columns into the requirements text.

## Recommended Approach

Use coordinate-aware table extraction first, then apply a GESB SAFF-specific
interpretation layer.

```text
PDF page primitives
-> table regions and cell coordinates
-> outer SAFF row reconstruction
-> nested Requirements parsing
-> normalized field_rows
```

The generic PDF layer should extract layout primitives. The GESB layer should
understand the business meaning of fields such as `Mandatory`, `Data Type`,
`Length`, `Required by GESB?`, `MIG Reference`, and `DES Reference`.

## Tool Options

### PyMuPDF

Use this as the first local implementation candidate.

PyMuPDF provides page text, blocks, drawings, coordinates, and table detection
through `page.find_tables()`. This is a good fit for the SAFF pages because the
tables have visible horizontal rules and stable column positions.

Expected role:

```text
primary page structure and table candidate extraction
```

### pdfplumber

Use this as the main debugging and visual inspection tool.

pdfplumber exposes characters, lines, rectangles, curves, words, table settings,
and visual debugging helpers. It is useful for tuning row and column boundaries
when PyMuPDF output is ambiguous.

Expected role:

```text
table boundary debugging and fallback cell extraction experiments
```

### Docling

Use this as a later comparison option for broader RAG ingestion.

Docling can produce a structured document model with text, tables, bounding
boxes, section context, and provenance. It is heavier than PyMuPDF plus
pdfplumber, but useful if the parser must generalize across many document
families.

Expected role:

```text
benchmark parser for richer document structure
```

### Camelot or Tabula

Use these only as quick extraction benchmarks.

They can work well for simple lattice or stream PDF tables, but complex
multi-line cells and nested key-value content usually still require custom
repair logic.

Expected role:

```text
quick CSV/JSON comparison output, not the main parser
```

### Cloud OCR and Document AI Services

Azure Document Intelligence, AWS Textract, and Google Document AI are better
reserved for scanned PDFs, image-heavy files, or documents where local text and
line extraction is insufficient.

Expected role:

```text
fallback for scanned or highly irregular PDFs
```

## Target Output Shape

`requirements_text` should still be preserved for debugging, but the parser
should also expose structured requirement fields.

Example:

```json
{
  "column_number": 1,
  "field_name": "Version",
  "description": "Heading text",
  "requirements_text": "Mandatory: Yes Data Type: String Length: 7 Value(s): VERSION",
  "requirements": {
    "mandatory": "Yes",
    "data_type": "String",
    "length": "7",
    "format": null,
    "values": "VERSION",
    "notes": null
  },
  "required_by_gesb": "No",
  "references": {
    "mig_reference": "N/A",
    "des_reference": "N/A"
  }
}
```

## Implementation Notes

1. Detect the outer table columns by coordinates, not by text order alone.
2. Treat each `Column` number as the start of an outer field row.
3. Use row boundary coordinates to collect all text belonging to that row.
4. Parse the `Requirements` cell separately from the right-side reference cells.
5. Inside the `Requirements` cell, parse label/value pairs by y-position and
   known labels: `Mandatory`, `Data Type`, `Length`, `Format`, `Value(s)`, and
   `Notes`.
6. Preserve raw text, page number, row bounding box, and cell bounding boxes for
   debugging and re-normalization.

## Preferred Next Step

Build a small experiment for pages 10-27:

```text
1. Run PyMuPDF `find_tables()` on each page.
2. Save raw table cells with bounding boxes.
3. Compare page 10 output against the visible table.
4. Use pdfplumber visual debugging to tune boundaries if needed.
5. Replace the current text-line-only `field_rows` parser with a coordinate
   aware implementation once row and cell boundaries are stable.
```
