# PyMuPDF Table Experiment Quality Issues

This document records issues found in the current PyMuPDF experiment output:

```text
knowledge_base/processed/structured-business-file-formats/saff/specifications/gesb/
superstream-payroll-data-specification.pymupdf-tables.json
```

The output shows that the PyMuPDF coordinate-based approach is promising, but
the current extraction rules are not yet good enough to use as the final parser.

## Summary

The result contains:

```text
pages: 18
rows: 128
page range: 10-27
```

The main row fields are populated:

```text
column_number
field_name
description
requirements_text
required_by_gesb
mig_reference
des_reference
```

However, the result has three important quality problems:

```text
missing column numbers
header / section text contamination
some right-side column contamination
```

There is also an output encoding issue on Windows.

## Missing Column Numbers

The PyMuPDF output starts at column number `1` and ends at `133`, but the
following column numbers are missing:

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

This is the most important issue. A specification parser cannot silently lose
field definitions.

The existing `parsed.json` output contains these column numbers, so the missing
rows are not absent from the source document. They were missed by the current
PyMuPDF row-start detection / row-boundary rules.

## Duplicate Column Numbers

The PyMuPDF output contains duplicate column numbers:

```text
1
2
3
4
5
6
```

Some duplication is expected because the document has repeated introductory
header-like fields and line ID sections. However, duplicates still need to be
reviewed so the parser can distinguish real repeated field definitions from
rows polluted by headings or table headers.

Observed duplicate counts in the PyMuPDF result:

```text
1: 3
2: 2
3: 2
4: 2
5: 2
6: 2
```

## Header And Section Text Contamination

Some extracted rows include section headings or repeated table headers inside
business fields.

Example from page 11:

```text
column_number: 1
field_name: LINE ID 3 - Column header exist in the SAFF Field Name
description: Line ID column header row file but will be ignored. Description
requirements_text: Refer to MIG Requirements
required_by_gesb: No Required by GESB?
mig_reference: N/A MIG 2.0 Reference
des_reference: N/A DES Spec 5.8 Reference
```

This row has multiple contamination signals:

```text
field_name includes section/header prose
description includes the literal word Description from the table header
requirements_text includes Requirements
required_by_gesb includes Required by GESB?
mig_reference includes MIG 2.0 Reference
des_reference includes DES Spec 5.8 Reference
```

Example from page 12:

```text
column_number: 5
field_name: ElectronicErrorMessaging 11.4.3. Section: Sender Field Name
description: Indicates the sender's capability of handling the receipt of Member
Registration Outcome Response messages. details Description
requirements_text: Refer to MIG Requirements
required_by_gesb: No Required by GESB?
mig_reference: Sec. 4.1 MIG 2.0 Reference
des_reference: N/A DES Spec 5.8 Reference
```

This indicates that the row reconstruction can extend too far upward or include
nearby non-row text when section headings and table headers appear close to the
field row.

## Right-Side Column Contamination

Most `required_by_gesb` values look reasonable, but some are clearly polluted.

Observed values include:

```text
No
Yes
No - Ignored by GESB
No Required by GESB?
No Super processes, details to create/
```

The problematic values are:

```text
No Required by GESB?
No Super processes, details to create/
```

`No Required by GESB?` means the repeated table header was included in the row.

`No Super processes, details to create/` means nearby description or note text
was assigned to the `required_by_gesb` column, likely because the visual row
boundary was too broad or because text crossed into the right-side x range.

## Requirements Coverage

Many rows do not map cleanly into the normalized `requirements` dictionary.

Empty normalized requirement counts:

```text
mandatory: 89
data_type: 89
length: 91
format: 117
values: 107
notes: 125
```

This is not automatically wrong. Many rows say only `Refer to MIG`, `Leave
blank`, or `Not accepted by GESB`, so they do not have labels such as
`Mandatory`, `Data Type`, or `Length`.

The important check is whether labelled requirement blocks are correctly split
into:

```text
requirements_lines
requirements
```

Rows with `Mandatory`, `Data Type`, `Length`, `Format`, `Value(s)`, or `Notes`
should be validated with targeted golden examples.

## Output Encoding Issue

The JSON file could not be read as UTF-8 by Python:

```text
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x95
```

It was readable with `cp1252`.

This likely happens because `write_experiment_output()` uses:

```python
output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
```

without explicitly passing an encoding. On Windows, `Path.write_text()` can use
the platform default encoding.

The output writer should specify UTF-8:

```python
output_path.write_text(
    json.dumps(output, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
```

## Positive Signals

The approach still has strong signals:

```text
it produced structured rows across all table pages
main fields are mostly populated
MIG and DES reference columns are separated better than the pypdf parser
Requirements key-value cells are recoverable when the layout is clean
```

Compared with the current `parsed.json`, the PyMuPDF output gives better access
to visual table columns, especially:

```text
required_by_gesb
mig_reference
des_reference
```

## Recommended Fix Order

1. Fix output encoding to always write UTF-8.
2. Add a quality check that asserts expected column numbers are present.
3. Investigate and fix the 12 missing column numbers.
4. Filter repeated table headers from reconstructed rows.
5. Tighten row boundaries around section headings.
6. Add validation for `required_by_gesb` allowed values.
7. Add golden examples for complex `Requirements` rows.

## Current Assessment

The current PyMuPDF result is useful for evaluating the approach, but it is not
yet production quality.

The coordinate-based method is worth continuing. The next step should be
targeted rule fixes and quality checks, not a broad tool change.

