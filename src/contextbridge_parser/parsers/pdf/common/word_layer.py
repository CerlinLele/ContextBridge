"""Common word coordinate structures for PDF parsing."""

from __future__ import annotations

from typing import TypedDict


class Word(TypedDict):
    """A single extracted PDF word with page coordinates."""

    x0: float
    y0: float
    x1: float
    y1: float
    text: str
    block_no: int
    line_no: int
    word_no: int

