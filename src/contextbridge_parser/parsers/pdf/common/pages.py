"""Common PDF page inspection helpers."""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

from pypdf import PdfReader


LineCleaner = Callable[[list[str]], list[str]]
SectionHeadingParser = Callable[[str], tuple[str, str] | None]


def read_pdf_pages(
    reader: PdfReader,
    *,
    clean_lines: LineCleaner,
    parse_section_heading: SectionHeadingParser,
) -> list[dict[str, Any]]:
    """Read page text and page-level characteristics from a PDF reader."""

    pages = []
    for index, page in enumerate(reader.pages, start=1):
        raw_text = page.extract_text() or ""
        lines = clean_lines(raw_text.splitlines())
        media_box = page.mediabox
        width = float(media_box.width)
        height = float(media_box.height)
        pages.append(
            {
                "page_number": index,
                "document_page_label": _document_page_label(lines),
                "width": width,
                "height": height,
                "orientation": "landscape" if width > height else "portrait",
                "rotation": int(page.get("/Rotate", 0)),
                "text_char_count": len(raw_text),
                "image_count": _image_count(page),
                "section_headings": _section_headings(lines, parse_section_heading),
                "text": "\n".join(lines),
                "lines": lines,
            }
        )
    return pages


def page_range(
    pages: list[dict[str, Any]],
    start_page: int,
    end_page: int,
) -> list[dict[str, Any]]:
    """Return pages whose 1-based page number is within the inclusive range."""

    return [
        page
        for page in pages
        if start_page <= page["page_number"] <= end_page
    ]


def _section_headings(
    lines: list[str],
    parse_section_heading: SectionHeadingParser,
) -> list[dict[str, str]]:
    headings = []
    for line in lines:
        parsed = parse_section_heading(line)
        if parsed:
            headings.append({"section_number": parsed[0], "section_title": parsed[1]})
    return headings


def _document_page_label(lines: list[str]) -> str | None:
    for line in lines:
        match = re.fullmatch(r"Page\s+\d+", line)
        if match:
            return line
    return None


def _image_count(page: Any) -> int:
    resources = page.get("/Resources") or {}
    xobjects = resources.get("/XObject") or {}
    count = 0
    for item in xobjects.values():
        try:
            obj = item.get_object()
        except Exception:
            continue
        if obj.get("/Subtype") == "/Image":
            count += 1
    return count
