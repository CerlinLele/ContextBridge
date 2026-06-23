# PDF Common Module Structure

This document describes how `src/contextbridge_parser/parsers/pdf/common` should
be organized as reusable PDF parsing utilities grow.

## Recommendation

Do not organize `pdf/common` primarily by PDF tool.

Instead, organize common code by parsing capability, and keep tool-specific code
in thin adapter modules.

Recommended shape:

```text
src/contextbridge_parser/parsers/pdf/common/
  text.py
  pages.py
  sections.py
  word_layer.py
  layout.py
  row_detection.py
  row_segmentation.py
  cell_assignment.py
  nested_key_value.py
  table_quality.py
  tools/
    pymupdf.py
    pdfplumber.py
    pypdf.py
```

## Why Not Organize Primarily By Tool

A tool-first layout would look like:

```text
common/pymupdf/
common/pdfplumber/
common/pypdf/
```

That is not the best default because the reusable value is usually not the tool
itself. The reusable value is the parsing logic:

```text
word coordinate layer
layout detection
row start detection
row segmentation
cell assignment
nested key-value parsing
quality checks
```

Those capabilities may be fed by PyMuPDF today and pdfplumber later. If the
business logic lives under tool-specific folders, a future migration is more
likely to duplicate logic across tools.

## Preferred Separation

Use this separation:

```text
tool adapter layer:
  convert a library-specific page object into common data structures

common parsing layer:
  parse common data structures into rows, cells, nested values, and checks

source profile layer:
  define source-specific page ranges, headers, offsets, patterns, and expected values
```

In short:

```text
tools convert
common parses
profiles configure
```

## Suggested Module Responsibilities

### `word_layer.py`

Defines common word structures and helpers.

Responsibilities:

```text
Word typed dict or dataclass
coordinate normalization
word sorting
line grouping helpers
```

### `layout.py`

Handles table layout detection from common word data.

Responsibilities:

```text
header word detection
x range generation
layout profile definitions
fallback layout handling
```

### `row_detection.py`

Finds row start anchors.

Responsibilities:

```text
row start token matching
nearby-cell checks
row start validation
```

### `row_segmentation.py`

Segments a page into row regions.

Responsibilities:

```text
use row starts as y boundaries
find end boundary for last row
support source-specific section/page-end rules
```

### `cell_assignment.py`

Assigns words to cells by x range.

Responsibilities:

```text
cell_name_for_x
assign_words_to_cells
cell text joining
```

### `nested_key_value.py`

Parses nested label/value structures inside table cells.

Responsibilities:

```text
group words by visual line
pair label lines with nearest value lines
append continuation value lines
map labels to normalized field names
```

### `table_quality.py`

Provides reusable parser quality checks.

Responsibilities:

```text
missing identifier checks
duplicate identifier checks
empty field checks
allowed value checks
header contamination checks
section contamination checks
UTF-8 output validation
```

### `tools/pymupdf.py`

Thin adapter for PyMuPDF.

Responsibilities:

```text
fitz.Page -> common Word list
PyMuPDF find_tables summary
PyMuPDF version reporting
```

This is where functions like these should eventually live:

```text
page_words()
summarize_detected_tables()
```

### `tools/pdfplumber.py`

Thin adapter for pdfplumber.

Responsibilities:

```text
pdfplumber.Page -> common Word list
pdfplumber table/debug extraction helpers
```

This should only be added when there is a real use case.

### `tools/pypdf.py`

Thin adapter for pypdf-specific helpers if needed.

Current `pages.py` already uses `pypdf.PdfReader` for page text extraction.
Do not move it just to create symmetry; only split a pypdf adapter if the module
starts mixing generic page logic with library-specific details.

## What Should Stay In Source Profiles

Source-specific values should not move into `pdf/common`.

For GESB SAFF, these should stay in the GESB parser/profile:

```text
TABLE_PAGE_START / TABLE_PAGE_END
GESB-specific header words
GESB-specific x offset constants
required_by_gesb allowed values
MIG / DES field names
expected column numbers 1-133
section heading regex for 10.x and 11.x
requirements label map
```

The common modules should provide mechanics. Source profiles should provide
document-specific configuration.

## First Extraction Candidates

The safest first common helpers to extract from the PyMuPDF experiment are:

```text
common/tools/pymupdf.py
  page_words()
  summarize_detected_tables()

common/cell_assignment.py
  cell_name_for_x()
  assign_words_to_cells()

common/nested_key_value.py
  words_by_line()
  nearest_line()
  key_value_lines()
```

These are relatively low-coupling and clearly reusable.

Avoid extracting the full GESB parser too early. The following logic still needs
to mature before becoming common:

```text
GESB row start heuristics
GESB fallback x ranges
GESB section-heading end boundary
GESB required_by_gesb cleanup
```

## Migration Principle

Future tool migration should be adapter-level, not parser-level.

If PyMuPDF is replaced or supplemented by pdfplumber, the intended change should
look like:

```text
pdfplumber page
-> common Word list
-> same layout / row / cell / quality logic
```

not:

```text
rewrite the parser under common/pdfplumber
```

This keeps the expensive parsing logic reusable across tools.

## Summary

Use capability-first modules for `pdf/common`.

Use `common/tools` only for thin adapters around external PDF libraries.

Keep source-specific document rules in source parsers or profiles.

