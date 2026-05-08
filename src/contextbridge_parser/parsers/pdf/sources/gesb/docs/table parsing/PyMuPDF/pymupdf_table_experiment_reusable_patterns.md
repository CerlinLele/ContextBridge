# PyMuPDF Table Experiment Reusable Patterns

This document records which parts of the current GESB SAFF PyMuPDF table
experiment are worth reusing for future knowledge-base document processing.

The current implementation is source-specific and not yet production quality,
but several processing patterns are strong enough to extract into reusable
components.

## Current Assessment

The PyMuPDF experiment output shows useful structure:

```text
pages: 18
rows: 128
layout sources:
  header_words: 10 pages
  fallback: 8 pages
find_tables summaries: 75 tables
column number range: 1-133
unique column numbers: 121
non-N/A MIG references: 77
non-N/A DES references: 34
```

The approach is promising, but not yet final:

```text
12 expected column numbers are missing
some header and section text is mixed into rows
some required_by_gesb values are polluted
output encoding should be normalized to UTF-8
```

Therefore, the reusable value is in the processing patterns and abstractions,
not in copying the complete GESB-specific script unchanged.

## Pattern 1: PyMuPDF Word Coordinate Layer

The strongest reusable foundation is the word coordinate layer created by
`_page_words()`.

It converts each page into words with:

```text
x0
y0
x1
y1
text
block_no
line_no
word_no
```

This is more useful than plain text extraction for specification tables because
it preserves visual location. Later logic can ask:

```text
which column is this word in?
which visual row is this word in?
is this word near the row start?
does this word belong to a nested label/value cell?
```

### Reuse Potential

This should be extracted into a common utility, for example:

```text
pdf/common/word_layer.py
```

Possible reusable API:

```python
def page_words(page) -> list[Word]:
    ...
```

where `Word` can be a typed dict or dataclass.

## Pattern 2: Header-Driven Layout Detection

The combination of `_find_header_words()` and `_detect_table_layout()` is a
valuable pattern.

Instead of relying only on fixed x coordinates, the script:

```text
finds the table header words
uses their x0 coordinates
derives x_ranges for each logical column
falls back only when header detection fails
```

This pattern works well for PDFs where each table page has stable visible
headers.

### Reuse Potential

This can become a profile-driven layout detector:

```python
TableHeaderProfile(
    required_words=["Column", "Field", "Description", "Requirements", "Required", "MIG", "DES"],
    anchor_word="Column",
    anchor_x_max=80.0,
    header_y_range=(40.0, 160.0),
    same_line_tolerance=5.0,
)
```

Then each source can define its own header words and offsets without rewriting
the layout algorithm.

## Pattern 3: Row Start Detection

The current experiment identifies business rows by looking for numeric words in
the first column.

The general pattern is:

```text
detect a row-start token
check that nearby words look like a table row
use the row start as a y boundary anchor
```

For GESB SAFF, the row-start token is a one-to-three digit column number:

```text
\d{1,3}
```

### Reuse Potential

This can be generalized as:

```python
RowStartProfile(
    column_name="column_number",
    token_pattern=r"\d{1,3}",
    min_y_from_layout=True,
    nearby_required_columns=["field_name"],
    nearby_optional_columns=["requirements_label", "requirements_value", "required_by_gesb"],
)
```

This is useful for specification tables where each row starts with:

```text
a field number
a field code
a sequence number
a stable identifier
```

## Pattern 4: Row Boundary Reconstruction

`_extract_rows_from_words()` uses row starts to reconstruct row regions:

```text
current row starts at current row_start.y0
current row ends at next row_start.y0
last row ends at next section heading or page end
```

This is effective when the source table has multi-line rows but reliable row
start anchors.

### Reuse Potential

This can become a common row segmenter:

```python
def segment_rows(words, row_starts, end_boundary_detector) -> list[RowRegion]:
    ...
```

The end-boundary detector should be profile-specific. For GESB it currently
uses section headings like:

```text
10.1.
10.2.3.
11.4.
11.4.3.
```

Other sources should provide their own section heading patterns.

## Pattern 5: Cell Assignment By X Range

`_build_row()` assigns words to cells by comparing each word's `x0` against
the layout `x_ranges`.

The general rule is:

```text
if min_x <= word.x0 < max_x:
    assign word to that cell
```

This is a simple but effective way to recover table columns from PDF word
coordinates.

### Reuse Potential

This should become a common helper:

```python
def assign_words_to_cells(words, x_ranges) -> dict[str, list[Word]]:
    ...
```

It should remain separate from source-specific output mapping so it can be
used across table profiles.

## Pattern 6: Nested Label/Value Cell Parsing

The most valuable business-specific extraction pattern is the `Requirements`
cell parser.

GESB `Requirements` visually contains a nested label/value structure:

```text
Mandatory:    Yes
Data Type:    String
Length:       7
Value(s):     VERSION
```

The script splits it into:

```text
requirements_label
requirements_value
```

Then it pairs label and value lines by y coordinate.

### Reuse Potential

This pattern is highly reusable for specification documents that embed
key-value data inside a table cell.

Possible generic profile:

```python
NestedKeyValueProfile(
    label_column="requirements_label",
    value_column="requirements_value",
    line_tolerance=3.0,
    label_map={
        "mandatory": "mandatory",
        "data type": "data_type",
        "length": "length",
        "format": "format",
        "value(s)": "values",
        "notes": "notes",
    },
)
```

This is the part most worth preserving for future structured knowledge-base
records.

## Pattern 7: `find_tables()` As Diagnostic Signal

The experiment uses PyMuPDF `find_tables()` through `_find_tables_summary()`,
but does not rely on it as the main extraction path.

This is a good pattern:

```text
use find_tables() to inspect what PyMuPDF sees
store bbox, row count, column count, preview rows
compare it against custom coordinate extraction
do not blindly trust it when it misses rows
```

### Reuse Potential

This should become a diagnostic helper:

```python
def summarize_detected_tables(page) -> list[TableSummary]:
    ...
```

It can help debug new document profiles quickly.

## Pattern 8: Quality Checks As A Parser Gate

The current quality issues show why parser quality checks are necessary.

Useful checks include:

```text
expected row identifiers are present
unexpected duplicate identifiers are reported
required fields are non-empty
controlled-value fields contain allowed values
header text is not mixed into business fields
section headings are not mixed into business fields
output JSON is valid UTF-8
```

### Reuse Potential

This should become a common validation layer:

```text
pdf/common/table_quality.py
```

Each source profile should define expected identifiers, allowed values, and
contamination markers.

## Recommended Reusable Structure

The long-term structure should separate common mechanics from source-specific
profiles.

Suggested layout:

```text
pdf/common/word_layer.py
pdf/common/layout.py
pdf/common/row_detection.py
pdf/common/row_segmentation.py
pdf/common/cell_assignment.py
pdf/common/nested_key_value.py
pdf/common/table_quality.py
pdf/profiles/gesb_saff.py
```

The GESB-specific profile would contain:

```text
page range
header words
header anchor constraints
x range offset rules
row start pattern
section heading pattern
requirements label map
required_by_gesb allowed values
expected column numbers
contamination markers
```

## Example Profile Shape

A future profile could look like:

```python
TableProfile(
    page_range=(10, 27),
    header_words=[
        "Column",
        "Field",
        "Description",
        "Requirements",
        "Required",
        "MIG",
        "DES",
    ],
    row_start_pattern=r"\d{1,3}",
    expected_identifiers=range(1, 134),
    nested_cells={
        "requirements": NestedKeyValueProfile(
            label_column="requirements_label",
            value_column="requirements_value",
            label_map={
                "mandatory": "mandatory",
                "data type": "data_type",
                "length": "length",
                "format": "format",
                "value(s)": "values",
                "notes": "notes",
            },
        )
    },
)
```

## Best Knowledge-Base Record Shape

For knowledge-base use, the best reusable output is one field row per record,
not one large page chunk.

Recommended record shape:

```text
column_number
field_name
description
requirements_text
requirements
required_by_gesb
mig_reference
des_reference
page_number
source_path
parser_profile
```

This supports precise retrieval for questions such as:

```text
Is Payroll Number Identifier mandatory?
Which fields are required by GESB?
What is the MIG reference for a field?
What value format is required for a field?
```

## What Not To Reuse Directly

Do not reuse the current script unchanged as a generic parser.

The following parts are GESB-specific:

```text
hard-coded page range
specific header words
specific x offset constants
section heading regex limited to 10.x and 11.x
requirements label map
required_by_gesb value assumptions
expected column numbers
```

These should move into source profiles or layout configs before being reused
across other documents.

## Conclusion

The current experiment has several strong reusable patterns:

```text
word coordinate layer
header-driven layout detection
row start detection
row boundary reconstruction
x-range cell assignment
nested label/value parsing
find_tables diagnostic summaries
quality checks
```

The next step should be to extract these mechanics into common modules and keep
GESB-specific values in a profile. That would make future specification PDFs
much cheaper to process without repeating the same exploratory work.

