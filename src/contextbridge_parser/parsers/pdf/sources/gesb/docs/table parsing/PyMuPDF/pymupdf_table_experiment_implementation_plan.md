# PyMuPDF Table Experiment Implementation Plan

This plan describes how to improve the current PyMuPDF-based GESB SAFF table
extraction experiment until it is reliable enough to consider for production
parser integration.

It is based on the current quality issues documented in:

```text
src/contextbridge_parser/parsers/pdf/sources/gesb/docs/
pymupdf_table_experiment_quality_issues.md
```

## Goal

Improve the current coordinate-based extraction so it can reliably recover the
GESB SAFF field table rows and columns.

The target output should:

```text
include all expected column numbers
avoid repeated table header contamination
avoid section heading contamination
keep right-side reference columns separate
write valid UTF-8 JSON
provide repeatable quality checks
```

## Current State

The current experiment output has useful structure but is not production ready.

Observed result:

```text
pages: 18
rows: 128
column number range: 1-133
```

Known problems:

```text
missing column numbers: 24, 25, 56, 67, 78, 79, 106, 107, 108, 127, 128, 129
duplicate column numbers: 1, 2, 3, 4, 5, 6
header text appears inside some rows
section text appears inside some rows
required_by_gesb contains polluted values
output JSON is not valid UTF-8 on Windows
```

## Phase 1: Add Quality Checks

Before changing parsing rules, add an automated quality check for the
experiment output.

### Tasks

Create a script or test helper that reads:

```text
knowledge_base/processed/structured-business-file-formats/saff/specifications/gesb/
superstream-payroll-data-specification.pymupdf-tables.json
```

The check should report:

```text
total page count
total row count
missing column numbers
duplicate column numbers
rows with empty key fields
invalid required_by_gesb values
rows containing repeated table header text
rows containing section heading contamination
UTF-8 read success/failure
```

### Suggested Checks

Expected column numbers:

```text
1-133
```

Allowed `required_by_gesb` values should initially include:

```text
Yes
No
No - Ignored by GESB
No – Ignored by GESB
```

Header contamination indicators:

```text
Field Name
Description
Requirements
Required by GESB?
MIG 2.0 Reference
DES Spec 5.8 Reference
```

Section contamination indicators:

```text
Section:
11.4.
LINE ID
```

### Acceptance Criteria

The check can be run repeatedly and gives a clear pass/fail style summary.

It should make parser rule changes measurable instead of relying on manual JSON
inspection.

## Phase 2: Fix Output Encoding

The current JSON file could not be read as UTF-8. This should be fixed before
the output is used by other tooling.

### Tasks

Update `write_experiment_output()` in:

```text
src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment.py
```

Change the writer to explicitly use UTF-8:

```python
output_path.write_text(
    json.dumps(output, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
```

### Acceptance Criteria

The generated JSON can be loaded with:

```python
json.loads(path.read_text(encoding="utf-8"))
```

without fallback encodings.

## Phase 3: Investigate Missing Column Numbers

The most important parser quality issue is missing field rows.

### Tasks

For each missing column number:

```text
24
25
56
67
78
79
106
107
108
127
128
129
```

inspect the PyMuPDF word layer on the relevant page and record:

```text
word text
x0/y0/x1/y1
nearby words in field_name range
nearby words in requirements range
nearby words in right-side reference ranges
which row-start condition failed
```

Likely failure points:

```text
the column number x0 is outside column_number range
field words are not on the same visual line
right-side words are absent near the start y
the row is close to a section heading or table header
fallback x_ranges are too inaccurate for that page
```

### Acceptance Criteria

Each missing column number has a known reason before rule changes are made.

After fixes, the quality check should report no missing column numbers.

## Phase 4: Improve Row Start Detection

Current row start detection depends heavily on same-line word alignment.

### Current Rule

`_looks_like_table_row_start()` checks:

```text
same visual line: abs(word.y0 - start_word.y0) <= 4
field words exist on that visual line
right-side or requirement words exist nearby
```

This can miss rows where the field name or right-side content is slightly lower
than the column number.

### Proposed Change

Use a small vertical window instead of a strict same-line check:

```text
start_word.y0 - 2 <= word.y0 <= start_word.y0 + 14
```

Apply this especially when checking:

```text
field_name words
requirements words
right-side reference words
```

Keep the rule conservative enough that ordinary numeric text is not treated as
a row start.

### Acceptance Criteria

Missing column numbers are recovered without introducing many false positive
rows.

The duplicate count should not increase unexpectedly.

## Phase 5: Filter Repeated Table Headers

Some rows contain repeated table header text. This means header words are being
included in row reconstruction.

### Tasks

Detect repeated table header lines on each page.

Candidate header words:

```text
Column
Field
Name
Description
Requirements
Required
by
GESB?
MIG
2.0
Reference
DES
Spec
5.8
```

Only filter them when they appear as part of a detected table header line. Do
not globally remove these words from all rows, because some may legitimately
appear in descriptions.

### Possible Implementation

Add a helper such as:

```text
_find_header_line_ys(words)
```

Then exclude words whose `y0` is close to those header-line y values during
row reconstruction.

### Acceptance Criteria

Rows should no longer contain:

```text
Required by GESB?
MIG 2.0 Reference
DES Spec 5.8 Reference
Field Name
```

inside business field values.

## Phase 6: Tighten Row Boundaries

Some row regions include nearby section headings or explanatory text.

### Tasks

Improve `_extract_rows_from_words()` and `_next_section_or_page_end()` so row
boundaries stop at more visual breakpoints.

Additional stop signals:

```text
next section heading
next repeated table header line
large vertical gap before non-row text
page header/footer area
```

Section heading examples:

```text
11.4.3.
Section:
LINE ID
```

### Acceptance Criteria

Rows should not include section heading text such as:

```text
Section:
LINE ID
11.4.
```

unless that text is genuinely part of the field definition.

## Phase 7: Improve Layout Reuse

Some pages fall back to `DEFAULT_X_RANGES`. Hard-coded fallback ranges are less
reliable than page-specific header-derived ranges.

### Tasks

When a page does not contain a detectable header, reuse the most recent
header-derived layout from a previous page.

Suggested layout source values:

```text
header_words
previous_page
fallback
```

Only use `fallback` when no previous header-derived layout exists.

### Acceptance Criteria

Pages currently marked as `fallback` should use `previous_page` where possible.

Missing rows and right-side column contamination should decrease on fallback
pages.

## Phase 8: Validate Right-Side Columns

`required_by_gesb` is a narrow controlled field. It should be validated and
cleaned more aggressively than free-text fields.

### Tasks

Add a validation helper for `required_by_gesb`.

Allowed values:

```text
Yes
No
No - Ignored by GESB
No – Ignored by GESB
```

Flag or clean values such as:

```text
No Required by GESB?
No Super processes, details to create/
```

Do not silently discard unexpected values without logging them in the quality
check output.

### Acceptance Criteria

The quality check should report zero invalid `required_by_gesb` values.

## Phase 9: Add Golden Examples

Once the main rule fixes are in place, add targeted examples for complex rows.

### Suggested Golden Cases

Include examples for:

```text
a clean heading row
a clean data row
a row with labelled requirements
a row with Refer to MIG
a row with Leave blank
a row with multi-line Value(s)
a row near a repeated table header
a row near a section heading
a previously missing column number
```

### Acceptance Criteria

The golden cases should assert:

```text
column_number
field_name
description
requirements_text
requirements
required_by_gesb
mig_reference
des_reference
```

These examples should catch regressions before the experiment logic is promoted
or reused.

## Phase 10: Consider Tool Comparison Only If Needed

Do not switch tools before fixing the measurable PyMuPDF issues.

If the PyMuPDF approach still misses rows after the previous phases, run a small
comparison with `pdfplumber` only on the problematic pages and missing column
numbers.

### Comparison Scope

Use the missing or contaminated cases:

```text
24
25
56
67
78
79
106
107
108
127
128
129
```

Evaluate whether `pdfplumber` gives better:

```text
word coordinates
line grouping
table boundary detection
column separation
```

### Acceptance Criteria

Only consider a tool migration if `pdfplumber` clearly reduces missing rows or
contamination with less source-specific rule complexity.

## Recommended Execution Order

1. Add quality check.
2. Fix UTF-8 output.
3. Investigate missing column numbers.
4. Improve row start detection.
5. Filter repeated table headers.
6. Tighten row boundaries.
7. Reuse previous page layout instead of fallback ranges.
8. Validate `required_by_gesb`.
9. Add golden examples.
10. Compare `pdfplumber` only if PyMuPDF still fails.

## Definition Of Done

The PyMuPDF experiment can be considered ready for production-parser evaluation
when:

```text
all expected column numbers are present
unexpected duplicates are understood or removed
no header text appears in business row fields
no section heading text appears in business row fields
required_by_gesb values are valid
MIG and DES references are populated and separated
output JSON is valid UTF-8
quality checks pass consistently
golden examples cover known difficult rows
```

