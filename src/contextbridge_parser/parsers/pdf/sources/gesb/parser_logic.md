# GESB SAFF PDF Parser Logic

This document explains the parsing logic in `saff.py`.

The current parser is a `pypdf` text extraction parser with GESB SAFF-specific
rules. It is not a generic PDF parser and does not preserve real table cell
coordinates.

## Overall Flow

`parse_gesb_saff_pdf()` runs the main parsing flow:

```text
PDF
-> read metadata
-> read every page as text lines
-> extract section chunks
-> extract field rows
-> extract sample page notes
-> emit parsed JSON
```

The parsed JSON contains:

```text
parser
source
page_characteristics
section_chunks
field_rows
sample_pages
quality_notes
```

## Page Reading

`read_pdf_pages()` from `pdf/common/pages.py` uses `pypdf.PdfReader` to inspect
every page. The GESB parser passes in its own line cleaner and section heading
parser so source-specific rules stay in `saff.py`.

For each page, it records:

```text
page_number
document_page_label
width
height
orientation
rotation
text_char_count
image_count
section_headings
text
lines
```

The text extraction comes from:

```python
page.extract_text()
```

The parser then normalizes whitespace, removes empty lines, removes the repeated
GESB footer/header line, and removes `Page N` lines.

This means the parser works from `pypdf` text order, not from PDF coordinates or
true table cells.

## Section Chunk Extraction

`_extract_section_chunks()` extracts section summaries from the body summary
pages, excluding the change history, key references, and table of contents:

```python
section_chunks = _extract_section_chunks(
    _page_range(pages, SECTION_SUMMARY_PAGE_START, SECTION_SUMMARY_PAGE_END)
)
```

The logic is:

```text
when a section heading is found:
  finalize the previous section chunk
  start a new section chunk

otherwise:
  append the line to the current section chunk
```

Section headings are detected by `_parse_section_heading()`, which matches
numbered headings such as:

```text
1. Introduction
11.4. Employee details
```

Only headings beginning with sections `1.` through `12.` are accepted.

## Field Row Extraction

`_extract_field_rows()` extracts table rows from pages 10 through 27:

```python
TABLE_PAGE_START = 10
TABLE_PAGE_END = 27
```

The parser scans lines in those pages and applies this flow:

```text
if line is a section heading:
  save the current row
  update the current section

if line is a table header:
  skip it

if line starts with a 1-3 digit number:
  treat it as the start of a new field row

otherwise:
  append the line to the current field row
```

New rows are detected with:

```regex
^(?P<column>\d{1,3})\s+(?P<body>.+)$
```

For example:

```text
1 Version ...
42 Member Given Name ...
133 Employee Location Identifier End Date ...
```

The parser keeps track of the current section heading and adds it to each row.

Rows with column number `0`, or numbered value lines that begin with a dash, are
treated as continuations of the current row rather than new field rows.

## Field Row Normalization

Each raw field row is normalized by `_normalize_field_row()`.

The normalized row includes:

```text
chunk_type
row_subtype
page_number
start_page
end_page
section_number
section_title
column_number
field_name
description
requirements_text
mandatory
required_by_gesb
data_type
length
format
values
notes
references
raw_text
parser_profile
parser_version
```

The row body is parsed with targeted regex helpers:

```text
_split_field_name_and_description()
_extract_requirements_text()
_extract_mandatory()
_extract_required_by_gesb()
_extract_labeled_value()
_extract_references()
```

## Field Name and Description Splitting

`_split_field_name_and_description()` is the most heuristic part of the parser.

It first removes the requirements section from consideration by looking for
markers such as:

```text
Mandatory:
Refer to MIG
Not accepted by GESB
Leave blank
Data Type:
```

It then splits the remaining text using a hardcoded list of description-start
markers, such as:

```text
Heading text
Version number
Identifies
Indicates
Full name
The amount
Pay period
Not used
```

The assumption is:

```text
field name = text before the first marker
description = text from the marker onward
```

If no marker is found, the parser checks for duplicated text patterns and then
falls back to treating the whole pre-requirement text as the field name.

This works for the current GESB SAFF PDF, but it is brittle because it depends on
`pypdf` text order and exact wording in the source document.

## Row Subtypes

`_row_subtype()` classifies rows by section number:

```text
sections starting with 11.4. -> data_row_field
all other rows              -> format_control_row
```

This separates actual data row fields from format/header/control rows.

## Sample Page Handling

`_extract_sample_page_notes()` handles pages 28 through 34:

```python
SAMPLE_PAGE_START = 28
SAMPLE_PAGE_END = 34
```

The parser does not try to parse sample SAFF content from these pages. It emits a
note explaining that the pages appear image-heavy and that the ATO XLSX source is
preferred for structured sample data.

## Dependency Trace

`build_dependency_trace()` records the parser runtime and dependency status.

It marks `pypdf` as required and records several optional tools for future parser
improvements:

```text
pymupdf
pdfplumber
docling
unstructured
pytesseract
```

The trace also includes:

```text
generated_at
source path and sha256
parser name/version/profile
Python runtime
output paths
```

## Current Output Characteristics

For the current GESB SAFF PDF, the existing parsed artifact contains:

```text
section_chunks: 11
field_rows: 141
sample_pages: 7
```

The quality notes report that sample pages 28 through 34 contain embedded images
and may need OCR if screenshot content is required.

## Known Limitations

The parser is useful for the first structured artifact, but it has important
limitations:

1. `pypdf.extract_text()` text order can be unstable for dense tables.
2. Field name and description splitting depends on hardcoded English markers.
3. Table and sample page ranges are hardcoded.
4. `document_page_label` is likely unavailable because `Page N` lines are removed
   during cleaning before label detection.
5. `_is_numbered_value_line()` contains encoded dash artifacts (`â€“`, `â€”`) that
   should be cleaned up.
6. `page_characteristics` stores full page text, which is useful for debugging
   but may be too large for retrieval-oriented artifacts.

## Recommended Next Step

Keep this parser as the first deterministic GESB SAFF parser, but move table
extraction toward a table-aware implementation:

```text
PyMuPDF for page structure, coordinates, images, and table detection
pdfplumber for table extraction experiments and visual debugging
pypdf for metadata, encryption checks, page counts, and lightweight smoke tests
OCR only as a fallback for screenshot-heavy sample pages
```
