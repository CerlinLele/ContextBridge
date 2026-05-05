# Page Reading

This document explains the common PDF page reading logic in `pdf/common/pages.py`.

## Purpose

`read_pdf_pages()` converts a `pypdf.PdfReader` into a list of page dictionaries
with consistent page-level metadata and extracted text.

It is the first parsing layer for PDF sources:

```text
PdfReader
-> page text extraction
-> source-specific line cleaning
-> page-level metadata collection
-> image counting
-> source-specific section heading detection
-> list[page]
```

The function does not perform source-specific field extraction, table parsing, or
OCR. Those responsibilities belong to parser profiles or source-specific parsers.

## API

```python
read_pdf_pages(
    reader,
    clean_lines=...,
    parse_section_heading=...,
)
```

Arguments:

```text
reader
  A pypdf.PdfReader instance.

clean_lines
  A source-specific callback that receives raw text lines and returns cleaned
  lines.

parse_section_heading
  A source-specific callback that receives a cleaned line and returns
  (section_number, section_title) when the line is a heading, otherwise None.
```

The callbacks keep `common/pages.py` generic. For example, GESB-specific rules
such as removing the repeated GESB line or accepting only sections `1.` through
`12.` stay in the GESB parser.

## Output Shape

Each page dictionary contains:

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

Example:

```json
{
  "page_number": 10,
  "document_page_label": null,
  "width": 841.92,
  "height": 595.32,
  "orientation": "landscape",
  "rotation": 0,
  "text_char_count": 1007,
  "image_count": 0,
  "section_headings": [
    {
      "section_number": "11.1.",
      "section_title": "Header Row"
    }
  ],
  "text": "11.1. Header Row\nColumn Field Name Description ...",
  "lines": [
    "11.1. Header Row",
    "Column Field Name Description Requirements Required by GESB?",
    "1 Version Version number Mandatory: Yes No Sec. ..."
  ]
}
```

## Field Meanings

`page_number`

The 1-based page index in the PDF.

`document_page_label`

The detected `Page N` label if it remains after line cleaning.

`width` and `height`

The PDF page media box dimensions.

`orientation`

`landscape` when width is greater than height, otherwise `portrait`.

`rotation`

The page `/Rotate` value.

`text_char_count`

The character count from the raw `pypdf` extracted text before line cleaning.

`image_count`

The number of image XObjects found in the page resources.

`section_headings`

Headings detected by the caller-provided `parse_section_heading` callback.

`text`

The cleaned lines joined with newline characters.

`lines`

The cleaned page lines used by later parsing stages.

## Important Limitations

`read_pdf_pages()` uses:

```python
page.extract_text()
```

That means it depends on `pypdf` text order. It does not preserve:

```text
text coordinates
table cells
column boundaries
reading-order confidence
OCR text
```

For dense specification tables, later parsing logic should use this output as a
baseline only. Table-aware extraction should eventually use coordinate-aware
tools such as PyMuPDF or pdfplumber.
