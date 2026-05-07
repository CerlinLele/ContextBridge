# PyMuPDF Table Experiment Notes

## Context

The existing GESB SAFF parser extracts `field_rows` from pypdf text lines and
then uses regular expressions to infer table rows and field attributes.

That approach is fragile for the SAFF field specification tables because the
PDF table has two levels of structure:

1. An outer field row with columns such as `Column`, `Field Name`,
   `Description`, `Requirements`, `Required by GESB?`, `MIG 2.0 Reference`,
   and `DES Spec 5.8 Reference`.
2. A nested key-value structure inside the `Requirements` cell, with labels
   such as `Mandatory`, `Data Type`, `Length`, `Format`, `Value(s)`, and
   `Notes`.

The text-only parser can flatten this into one sequence such as:

```text
Mandatory: Yes No N/A N/A Data Type: String Length: 7 Value(s): VERSION
```

This loses the visual boundary between the `Requirements` cell and the right
side reference columns.

## Environment

The experiment was run from the project virtual environment.

Activate `.venv` first:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project and optional PDF dependencies inside `.venv`:

```powershell
.venv\Scripts\python -m pip install -e ".[pdf]"
```

The virtual environment dependency check returned:

```text
fitz 1.27.2.3
pypdf 6.10.2
pdfplumber 0.11.9
```

## First PyMuPDF `find_tables()` Trial

The first experiment opened page 10 of the GESB SAFF PDF with PyMuPDF and ran
the default table finder:

```python
import fitz

pdf = "knowledge_base/sources/structured-business-file-formats/saff/specifications/gesb/superstream-payroll-data-specification.pdf"
doc = fitz.open(pdf)
page = doc[9]
tables = list(page.find_tables().tables)
```

Result:

```text
PyMuPDF 1.27.2.3
page 10 size Rect(0.0, 0.0, 842.0399780273438, 595.3200073242188)
tables 3
```

The three detected tables represented rows 1, 3, and 5. Each detected table had
5 rows and 9 columns.

Example output for row 1:

```text
['1', 'Version', 'Heading text', '', 'Mandatory:', 'Yes', 'No', 'N/A', 'N/A']
['', '', '', '', 'Data Type:', 'String', '', '', '']
[None, None, None, None, 'Length:', '7', None, None, None]
[None, None, None, None, 'Value(s):', 'VERSION', None, None, None]
```

### Result

This was useful because PyMuPDF correctly split the nested `Requirements`
content into label/value cells and kept `Required by GESB?`, `MIG`, and `DES`
separate.

### Problem

Default `find_tables()` only detected rows 1, 3, and 5 on page 10. It missed
rows 2, 4, and 6 because those rows did not form the same complete line-bounded
table regions as the grey-highlighted rows.

This does not mean PyMuPDF can only recognize one row color. The default table
finder is not primarily color-based. It infers tables from layout signals such
as lines, borders, rectangles, intersections, and text alignment. Rows 1, 3, and
5 happen to be grey-highlighted, but the likely reason they were detected is
that they also form clearer line-bounded or rectangle-like regions. The white
rows between them were visible in the PDF text layer, but default
`find_tables()` did not classify them as complete table regions.

This means default `find_tables()` alone is not enough to replace the current
parser.

## Strategy Comparison

Several `find_tables()` strategy combinations were tested:

```python
page.find_tables(vertical_strategy="lines", horizontal_strategy="lines")
page.find_tables(vertical_strategy="text", horizontal_strategy="text")
page.find_tables(vertical_strategy="lines", horizontal_strategy="text")
page.find_tables(vertical_strategy="text", horizontal_strategy="lines")
page.find_tables(vertical_strategy="lines_strict", horizontal_strategy="lines_strict")
```

### `lines` / `lines`

Result:

```text
tables 3
```

This produced clean nested `Requirements` cells, but only for rows 1, 3, and 5.

### `text` / `text`

Result:

```text
tables 1
rows 58
cols 9
```

This included much more text, but it also pulled in page headers and surrounding
body text. It was too noisy for direct row extraction.

### `lines` / `text`

Result:

```text
tables 3
```

This still detected only the same broad table regions, with extra blank rows.
It did not solve the missing even-numbered rows.

### `text` / `lines`

Result:

```text
tables 1
rows 27
cols 8
```

This covered more content but merged headers and table cells in ways that would
still require substantial repair logic.

### `lines_strict` / `lines_strict`

Result:

```text
tables 3
rows 1
cols 2
```

This collapsed each detected region into two broad cells and lost the useful
nested `Requirements` split.

### Conclusion

The best raw `find_tables()` mode was still the default `lines` / `lines`, but
it should be treated as a diagnostic signal rather than the complete parser.

## Word Coordinate Trial

The next experiment used PyMuPDF word coordinates:

```python
page.get_text("words", sort=True)
```

For page 10, the words showed stable x/y positions:

```text
56.4 154.6 1
97.5 154.6 Version
210.6 154.6 Heading
360.2 157.6 Mandatory:
417.6 157.6 Yes
516.1 154.6 No
567.9 154.6 N/A
621.8 154.6 N/A
```

Rows 2, 4, and 6 were present in the word coordinate output even though default
`find_tables()` missed them.

Example for row 2:

```text
56.4 204.8 2
97.5 204.8 Version
127.0 204.8 data
210.6 204.8 Version
240.1 204.8 number
360.2 207.7 Mandatory:
417.6 207.7 Yes
516.1 204.8 No
567.9 204.8 N/A
621.8 204.8 N/A
```

### Result

This showed that PyMuPDF word coordinates can recover all visible rows on page
10. The coordinate data is a better base for a deterministic parser than
text-order-only extraction.

## Experiment Script

A dedicated experiment script was added:

```text
src/contextbridge_parser/parsers/pdf/sources/gesb/pymupdf_table_experiment.py
```

It is intentionally separate from the production parser. It does not replace
`field_rows` yet.

Run command:

```powershell
.venv\Scripts\python -m contextbridge_parser.parsers.pdf.sources.gesb.pymupdf_table_experiment
```

Output:

```text
knowledge_base/processed/structured-business-file-formats/saff/specifications/gesb/superstream-payroll-data-specification.pymupdf-tables.json
```

The output includes:

```text
experiment metadata
per-page PyMuPDF find_tables summaries
per-page detected layout
word-coordinate reconstructed rows
structured requirements fields
raw row text
```

## First Script Version

The first script version used fixed x ranges based on page 10:

```python
PAGE_X_RANGES = {
    "column_number": (45.0, 92.0),
    "field_name": (92.0, 205.0),
    "description": (205.0, 347.0),
    "requirements_label": (347.0, 411.0),
    "requirements_value": (411.0, 510.0),
    "required_by_gesb": (510.0, 563.0),
    "mig_reference": (563.0, 617.0),
    "des_reference": (617.0, 676.0),
}
```

It identified a row start when a word in the left `Column` x range matched:

```text
\d{1,3}
```

### Result

For page 10, the output was good:

```text
1 Version
2 Version data
3 Negatives Supported
4 Negatives Supported data
5 File Id
6 File Id data
```

It also correctly normalized page 10 requirements:

```json
{
  "mandatory": "Yes",
  "data_type": "String",
  "length": "7",
  "format": null,
  "values": "VERSION",
  "notes": null
}
```

### Problem

The fixed row-start rule was too loose. It misread non-row text such as section
headings and table headers as field rows.

Examples of bad extracted rows included:

```text
ID Column 4 onwards 11.4.1. Section: Name Description
ElectronicErrorMessaging 11.4.3. Section: Field Name
Employee Location Identifier 11.4.11. Section: Field Name
```

## Row-Start Rule Improvement

The row-start rule was tightened. A candidate row number now has to satisfy more
than just being a number in the left column.

The improved rule checks:

1. The candidate word is in the `Column` x range.
2. The candidate word is a 1-3 digit number.
3. The same visual line has words in the `Field Name` x range.
4. The same visual line has either right-side reference words or nearby
   `Requirements` words.

This reduced false positives from random numbered text.

### Result

The experiment output improved, but some false positives remained where section
headers appeared directly inside the table flow.

## Dynamic Per-Page Column Detection

The fixed page 10 x ranges were not stable enough across all pages.

For example, table headers shifted by page:

```text
page 10 Requirements x ~= 352.5, Required x ~= 518.3
page 11 Requirements x ~= 319.9, Required x ~= 461.7
page 12 Requirements x ~= 353.8, Required x ~= 468.8
page 14 Requirements x ~= 353.8, Required x ~= 522.2
```

The script was changed to detect table header words on each page:

```text
Column
Field
Description
Requirements
Required
MIG
DES
```

It then derives x ranges from those header positions.

### Result

Dynamic per-page layout detection separated right-side columns better across
pages and recovered more rows.

The generated output summary after this change:

```text
pages: 18
word rows total: 128
page 10 word rows: 6
PyMuPDF version: 1.27.2.3
```

## Boundary Adjustment

After dynamic x-range detection, page 10 initially lost the `No` value in
`Required by GESB?` because the `No` word sat slightly left of the derived
`Required` column boundary.

The right-side boundary was adjusted:

```python
"requirements_value": (requirements_x + 58.0, required_x - 8.0)
"required_by_gesb": (required_x - 5.0, mig_x - 2.0)
```

### Result

Page 10 rows now preserve the right-side values:

```text
[(1, 'No', 'N/A', 'N/A'),
 (2, 'No', 'N/A', 'N/A'),
 (3, 'No', 'N/A', 'N/A'),
 (4, 'No', 'N/A', 'N/A'),
 (5, 'No', 'N/A', 'N/A'),
 (6, 'No', 'N/A', 'N/A')]
```

## Current Results

The current experiment output contains:

```text
rows: 128
pages: 18
word rows page 10: 6
word rows total: 128
```

Useful examples:

```text
column 1
field_name: Version
requirements:
  mandatory: Yes
  data_type: String
  length: 7
  values: VERSION
required_by_gesb: No
mig_reference: N/A
des_reference: N/A
```

```text
column 31
field_name: Location ID
requirements:
  mandatory: No
  data_type: String
  length: 20
required_by_gesb: Yes
mig_reference: N/A
des_reference: Sec. 2.3 Id. 37
```

```text
column 75
field_name: %FTE (Repurposed Weekly Hours Worked Number field)
requirements:
  mandatory: Yes
  data_type: Numeric
  length: 3
  format: 999
required_by_gesb: Yes
mig_reference: N/A (Originall y Sec. 4.3.4 Seq. 19)
des_reference: Sec. 2.3 Id. 28
```

## Remaining Problems

The experiment is promising but not production-ready.

### 1. `find_tables()` Is Incomplete

Default PyMuPDF `find_tables()` detects the nested `Requirements` table well
when it finds a row region, but it misses some visible rows.

So `find_tables()` should not be the only extraction mechanism.

### 2. Section Headers Can Be Mixed Into Rows

Some pages contain section headings very close to the table body. The current
word-coordinate row reconstruction can still absorb section header text into the
previous or next row.

Examples:

```text
11.4.3. Section: Sender details
11.4.11. Section: Defined benefit registration details
```

### 3. Some Multi-Line Rows Still Need Repair

Column 29 is still problematic. It mixes explanatory note text across columns:

```text
Account Name Text regulated fund details by the Employer through itself...
```

This row likely needs source-specific handling for long notes and row
continuation boundaries.

### 4. Some Pages Fall Back to Default X Ranges

Not every page had a table header detected cleanly. Those pages use fallback x
ranges, which are less reliable.

Current page layout sources include both:

```text
header_words
fallback
```

Fallback pages should be inspected and improved before replacing the production
parser.

### 5. Row Count Is Lower Than the Full Logical Range

The experiment currently extracts 128 rows. The SAFF table includes logical
columns through 133, but not every column is necessarily present as an accepted
field row in the same way. Missing or skipped columns need to be reconciled
against the source document and current `field_rows` output before changing the
production parser.

## Recommended Next Improvements

1. Keep using PyMuPDF word coordinates as the main extraction base.
2. Use `find_tables()` as a helper signal for row/cell boundaries where it works.
3. Add explicit section heading detection to stop rows before a new section
   heading begins.
4. Add row validation rules:
   - `column_number` must be plausible for the current section.
   - `field_name` must not contain table header text.
   - `raw_text` should not contain a following section heading unless the row is
     explicitly marked as suspect.
5. Add per-page layout diagnostics for fallback pages.
6. Add tests or snapshot checks for representative rows:
   - page 10 columns 1-6
   - column 19 USI
   - column 29 Account Name Text
   - column 31 Location ID
   - column 75 %FTE
   - column 76 Occupation Description
7. Once stable, move the coordinate-aware logic into the production GESB parser
   and keep the old text parser as a fallback or comparison mode.

## Practical Conclusion

PyMuPDF is useful for this document, but the best path is not a direct
`find_tables()` replacement.

The better design is:

```text
PyMuPDF words and table candidates
-> dynamic per-page column layout
-> row boundary reconstruction
-> nested Requirements parsing
-> source-specific row validation and repair
-> production field_rows
```

This should produce more accurate `field_rows` than the current text-only
regular-expression parser while staying deterministic and local.
