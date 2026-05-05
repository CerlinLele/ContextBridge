"""Common PDF section parsing helpers."""

from __future__ import annotations

import re
from collections.abc import Sequence


def parse_numbered_section_heading(
    line: str,
    *,
    allowed_prefixes: Sequence[str] | None = None,
) -> tuple[str, str] | None:
    """Parse a numbered section heading from a cleaned PDF text line."""

    match = re.match(r"^(?P<number>\d+(?:\.\d+)*\.?)\s+(?P<title>.+)$", line)
    if not match:
        return None

    number = match.group("number")
    title = match.group("title").strip()
    if allowed_prefixes and not number.startswith(tuple(allowed_prefixes)):
        return None
    return number, title
