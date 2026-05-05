"""Common PDF text normalization helpers."""

from __future__ import annotations

import re
from collections.abc import Callable


LinePredicate = Callable[[str], bool]


def clean_text_lines(
    lines: list[str],
    *,
    keep_line: LinePredicate | None = None,
) -> list[str]:
    """Normalize PDF text lines, remove blanks, and apply optional filtering."""

    cleaned = []
    for line in lines:
        value = normalize_space(line)
        if not value:
            continue
        if keep_line and not keep_line(value):
            continue
        cleaned.append(value)
    return cleaned


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()
