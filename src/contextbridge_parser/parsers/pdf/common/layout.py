"""Common helpers for coordinate-based PDF table layouts."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from typing import Any

from contextbridge_parser.parsers.pdf.common.word_layer import Word

HeaderWords = dict[str, Word]
XRangeMap = dict[str, tuple[float, float]]
XRangeBuilder = Callable[[Mapping[str, Word]], XRangeMap]


def find_header_words(
    words: Sequence[Word],
    *,
    anchor_text: str,
    required_texts: Sequence[str],
    anchor_x_max: float | None = None,
    header_y_range: tuple[float, float] | None = None,
    same_line_tolerance: float = 5.0,
) -> HeaderWords | None:
    """Find a complete table header line from extracted PDF words."""

    anchor_candidates = [
        word
        for word in words
        if word["text"] == anchor_text
        and (anchor_x_max is None or word["x0"] < anchor_x_max)
        and (
            header_y_range is None
            or header_y_range[0] <= word["y0"] <= header_y_range[1]
        )
    ]

    for anchor_word in anchor_candidates:
        same_line = [
            word
            for word in words
            if abs(word["y0"] - anchor_word["y0"]) <= same_line_tolerance
        ]
        header: HeaderWords = {anchor_text: anchor_word}
        for text in required_texts:
            matches = [word for word in same_line if word["text"] == text]
            if matches:
                header[text] = matches[0]
        if all(text in header for text in required_texts):
            return header
    return None


def detect_table_layout(
    words: Sequence[Word],
    *,
    default_x_ranges: XRangeMap,
    default_table_data_y_min: float,
    anchor_text: str,
    required_texts: Sequence[str],
    x_range_builder: XRangeBuilder,
    anchor_x_max: float | None = None,
    header_y_range: tuple[float, float] | None = None,
    same_line_tolerance: float = 5.0,
    table_data_y_offset: float = 10.0,
    header_source: str = "header_words",
    fallback_source: str = "fallback",
) -> dict[str, Any]:
    """Detect a table layout from header words or return a fallback layout."""

    header = find_header_words(
        words,
        anchor_text=anchor_text,
        required_texts=required_texts,
        anchor_x_max=anchor_x_max,
        header_y_range=header_y_range,
        same_line_tolerance=same_line_tolerance,
    )
    if not header:
        return {
            "x_ranges": default_x_ranges,
            "table_data_y_min": default_table_data_y_min,
            "source": fallback_source,
        }

    return {
        "x_ranges": x_range_builder(header),
        "table_data_y_min": header[anchor_text]["y0"] + table_data_y_offset,
        "source": header_source,
    }

