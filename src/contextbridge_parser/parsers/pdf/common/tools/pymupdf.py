"""PyMuPDF adapters for common PDF parsing structures."""

from __future__ import annotations

from typing import Any

from contextbridge_parser.parsers.pdf.common.word_layer import Word


def page_words(page: Any, *, sort: bool = True) -> list[Word]:
    """Extract PyMuPDF page words into the common word coordinate shape."""

    words: list[Word] = []
    for item in page.get_text("words", sort=sort):
        x0, y0, x1, y1, text, block_no, line_no, word_no = item
        words.append(
            {
                "x0": x0,
                "y0": y0,
                "x1": x1,
                "y1": y1,
                "text": text,
                "block_no": block_no,
                "line_no": line_no,
                "word_no": word_no,
            }
        )
    return words
