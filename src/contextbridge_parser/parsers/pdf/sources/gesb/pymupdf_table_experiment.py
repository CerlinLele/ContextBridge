"""PyMuPDF experiment for GESB SAFF table extraction.

This script is intentionally separate from the production parser. It tests
whether PyMuPDF coordinates can reconstruct SAFF field table rows more reliably
than text-order-only parsing.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import fitz

from contextbridge_parser.parsers.pdf.sources.gesb.saff import (
    DEFAULT_OUTPUT_DIR,
    DEFAULT_SOURCE_PATH,
    TABLE_PAGE_END,
    TABLE_PAGE_START,
)


DEFAULT_OUTPUT_PATH = (
    DEFAULT_OUTPUT_DIR / "superstream-payroll-data-specification.pymupdf-tables.json"
)

DEFAULT_X_RANGES = {
    "column_number": (45.0, 92.0),
    "field_name": (92.0, 205.0),
    "description": (205.0, 347.0),
    "requirements_label": (347.0, 411.0),
    "requirements_value": (411.0, 510.0),
    "required_by_gesb": (510.0, 563.0),
    "mig_reference": (563.0, 617.0),
    "des_reference": (617.0, 676.0),
}

DEFAULT_TABLE_DATA_Y_MIN = 100.0


def extract_pymupdf_tables(source_path: Path) -> dict[str, Any]:
    source_path = source_path.resolve()
    doc = fitz.open(source_path)
    pages = []
    rows = []

    for page_index in range(TABLE_PAGE_START - 1, min(TABLE_PAGE_END, len(doc))):
        page = doc[page_index]
        page_number = page_index + 1
        words = _page_words(page)
        layout = _detect_table_layout(words)
        row_starts = _find_row_starts(words, layout)
        finder_tables = _find_tables_summary(page)
        page_rows = _extract_rows_from_words(page_number, words, row_starts, layout)

        pages.append(
            {
                "page_number": page_number,
                "size": {
                    "width": page.rect.width,
                    "height": page.rect.height,
                },
                "pymupdf_find_tables": finder_tables,
                "detected_layout": layout,
                "word_row_start_count": len(row_starts),
                "word_row_count": len(page_rows),
            }
        )
        rows.extend(page_rows)

    return {
        "experiment": {
            "name": "gesb-saff-pymupdf-table-experiment",
            "tool": "PyMuPDF",
            "pymupdf_version": fitz.VersionBind,
            "source_path": _display_path(source_path),
            "page_range": {
                "start": TABLE_PAGE_START,
                "end": TABLE_PAGE_END,
            },
            "default_x_ranges": DEFAULT_X_RANGES,
        },
        "pages": pages,
        "rows": rows,
    }


def _page_words(page: fitz.Page) -> list[dict[str, Any]]:
    words = []
    for item in page.get_text("words", sort=True):
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


def _detect_table_layout(words: list[dict[str, Any]]) -> dict[str, Any]:
    header = _find_header_words(words)
    if not header:
        return {
            "x_ranges": DEFAULT_X_RANGES,
            "table_data_y_min": DEFAULT_TABLE_DATA_Y_MIN,
            "source": "fallback",
        }

    column_x = header["Column"]["x0"]
    field_x = header["Field"]["x0"]
    description_x = header["Description"]["x0"]
    requirements_x = header["Requirements"]["x0"]
    required_x = header["Required"]["x0"]
    mig_x = header["MIG"]["x0"]
    des_x = header["DES"]["x0"]

    x_ranges = {
        "column_number": (max(0.0, column_x - 12.0), field_x - 5.0),
        "field_name": (field_x - 5.0, description_x - 5.0),
        "description": (description_x - 5.0, requirements_x - 5.0),
        "requirements_label": (requirements_x - 5.0, requirements_x + 58.0),
        "requirements_value": (requirements_x + 58.0, required_x - 8.0),
        "required_by_gesb": (required_x - 5.0, mig_x - 2.0),
        "mig_reference": (mig_x - 2.0, des_x - 2.0),
        "des_reference": (des_x - 2.0, des_x + 80.0),
    }
    return {
        "x_ranges": x_ranges,
        "table_data_y_min": header["Column"]["y0"] + 10.0,
        "source": "header_words",
    }


def _find_header_words(words: list[dict[str, Any]]) -> dict[str, dict[str, Any]] | None:
    column_candidates = [
        word
        for word in words
        if word["text"] == "Column" and word["x0"] < 80.0 and 40.0 <= word["y0"] <= 160.0
    ]
    for column_word in column_candidates:
        same_line = [
            word for word in words if abs(word["y0"] - column_word["y0"]) <= 5.0
        ]
        header = {"Column": column_word}
        for text in ("Field", "Description", "Requirements", "Required", "MIG", "DES"):
            matches = [word for word in same_line if word["text"] == text]
            if matches:
                header[text] = matches[0]
        if all(text in header for text in ("Field", "Description", "Requirements", "Required", "MIG", "DES")):
            return header
    return None


def _find_row_starts(
    words: list[dict[str, Any]],
    layout: dict[str, Any],
) -> list[dict[str, Any]]:
    starts = []
    x_ranges = layout["x_ranges"]
    min_x, max_x = x_ranges["column_number"]
    for word in words:
        if word["y0"] < layout["table_data_y_min"]:
            continue
        if min_x <= word["x0"] < max_x and re.fullmatch(r"\d{1,3}", word["text"]):
            if _looks_like_table_row_start(word, words, x_ranges):
                starts.append(word)
    return starts


def _looks_like_table_row_start(
    start_word: dict[str, Any],
    words: list[dict[str, Any]],
    x_ranges: dict[str, tuple[float, float]],
) -> bool:
    same_visual_line = [
        word for word in words if abs(word["y0"] - start_word["y0"]) <= 4.0
    ]
    field_words = [
        word
        for word in same_visual_line
        if x_ranges["field_name"][0] <= word["x0"] < x_ranges["field_name"][1]
    ]
    right_side_words = [
        word
        for word in same_visual_line
        if x_ranges["required_by_gesb"][0] <= word["x0"] < x_ranges["des_reference"][1]
    ]
    requirement_words = [
        word
        for word in words
        if start_word["y0"] - 1.0 <= word["y0"] <= start_word["y0"] + 10.0
        and x_ranges["requirements_label"][0] <= word["x0"] < x_ranges["requirements_value"][1]
    ]
    return bool(field_words and (right_side_words or requirement_words))


def _find_tables_summary(page: fitz.Page) -> list[dict[str, Any]]:
    tables = []
    for table_index, table in enumerate(page.find_tables().tables):
        extracted = table.extract()
        tables.append(
            {
                "table_index": table_index,
                "bbox": _round_rect(table.bbox),
                "row_count": table.row_count,
                "col_count": table.col_count,
                "preview_rows": extracted[:6],
            }
        )
    return tables


def _extract_rows_from_words(
    page_number: int,
    words: list[dict[str, Any]],
    row_starts: list[dict[str, Any]],
    layout: dict[str, Any],
) -> list[dict[str, Any]]:
    rows = []
    for index, row_start in enumerate(row_starts):
        next_y = (
            row_starts[index + 1]["y0"]
            if index + 1 < len(row_starts)
            else _next_section_or_page_end(words, row_start["y0"])
        )
        row_words = [
            word for word in words if row_start["y0"] - 1 <= word["y0"] < next_y - 0.5
        ]
        row = _build_row(page_number, row_start, next_y, row_words, layout["x_ranges"])
        rows.append(row)
    return rows


def _next_section_or_page_end(words: list[dict[str, Any]], start_y: float) -> float:
    candidates = []
    for word in words:
        if word["y0"] <= start_y:
            continue
        if word["x0"] < 80 and re.fullmatch(r"1[01]\.\d+(?:\.\d+)?\.", word["text"]):
            candidates.append(word["y0"])
    return min(candidates) if candidates else 9999.0


def _build_row(
    page_number: int,
    row_start: dict[str, Any],
    next_y: float,
    row_words: list[dict[str, Any]],
    x_ranges: dict[str, tuple[float, float]],
) -> dict[str, Any]:
    cells: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for word in row_words:
        cell_name = _cell_name_for_x(word["x0"], x_ranges)
        if cell_name:
            cells[cell_name].append(word)

    requirement_lines = _requirements_lines(
        cells["requirements_label"], cells["requirements_value"]
    )

    return {
        "page_number": page_number,
        "bbox": _round_rect(
            (
                min((word["x0"] for word in row_words), default=row_start["x0"]),
                row_start["y0"],
                max((word["x1"] for word in row_words), default=row_start["x1"]),
                next_y,
            )
        ),
        "column_number": _first_int(_join_words(cells["column_number"])),
        "field_name": _join_words(cells["field_name"]),
        "description": _join_words(cells["description"]),
        "requirements_text": _join_requirement_lines(requirement_lines),
        "requirements_lines": requirement_lines,
        "requirements": _requirements_dict(requirement_lines),
        "required_by_gesb": _join_words(cells["required_by_gesb"]),
        "mig_reference": _join_words(cells["mig_reference"]),
        "des_reference": _join_words(cells["des_reference"]),
        "raw_text": _join_words(row_words),
    }


def _cell_name_for_x(x: float, x_ranges: dict[str, tuple[float, float]]) -> str | None:
    for name, (min_x, max_x) in x_ranges.items():
        if min_x <= x < max_x:
            return name
    return None


def _requirements_lines(
    label_words: list[dict[str, Any]],
    value_words: list[dict[str, Any]],
) -> list[dict[str, str]]:
    label_lines = _words_by_line(label_words)
    value_lines = _words_by_line(value_words)
    lines = []
    used_value_keys: set[float] = set()

    for label_y, label_text in label_lines:
        value_key, value_text = _nearest_line(label_y, value_lines)
        if value_key is not None:
            used_value_keys.add(value_key)
        lines.append(
            {
                "label": label_text,
                "value": value_text or "",
            }
        )

    # Multi-line values often continue directly below the labelled value line.
    if lines:
        for value_y, value_text in value_lines:
            if value_y not in used_value_keys:
                lines[-1]["value"] = _normalize_space(
                    f"{lines[-1]['value']} {value_text}"
                )

    return lines


def _words_by_line(words: list[dict[str, Any]]) -> list[tuple[float, str]]:
    groups: dict[float, list[dict[str, Any]]] = defaultdict(list)
    for word in words:
        key = round(word["y0"], 1)
        groups[key].append(word)
    return [
        (key, _join_words(sorted(group, key=lambda word: word["x0"])))
        for key, group in sorted(groups.items())
    ]


def _nearest_line(
    label_y: float,
    value_lines: list[tuple[float, str]],
    tolerance: float = 3.0,
) -> tuple[float | None, str | None]:
    candidates = [
        (abs(value_y - label_y), value_y, value_text)
        for value_y, value_text in value_lines
        if abs(value_y - label_y) <= tolerance
    ]
    if not candidates:
        return None, None
    _, value_y, value_text = min(candidates)
    return value_y, value_text


def _requirements_dict(requirement_lines: list[dict[str, str]]) -> dict[str, str | None]:
    mapped = {
        "mandatory": None,
        "data_type": None,
        "length": None,
        "format": None,
        "values": None,
        "notes": None,
    }
    label_map = {
        "mandatory": "mandatory",
        "data type": "data_type",
        "length": "length",
        "format": "format",
        "value(s)": "values",
        "notes": "notes",
    }
    for line in requirement_lines:
        label = line["label"].strip().rstrip(":").lower()
        key = label_map.get(label)
        if key:
            mapped[key] = line["value"] or None
    return mapped


def _join_requirement_lines(requirement_lines: list[dict[str, str]]) -> str:
    return _normalize_space(
        " ".join(
            f"{line['label']} {line['value']}".strip() for line in requirement_lines
        )
    )


def _join_words(words: list[dict[str, Any]]) -> str:
    return _normalize_space(
        " ".join(word["text"] for word in sorted(words, key=lambda word: (word["y0"], word["x0"])))
    )


def _normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _first_int(value: str) -> int | None:
    match = re.search(r"\d{1,3}", value)
    return int(match.group(0)) if match else None


def _round_rect(rect: tuple[float, float, float, float]) -> list[float]:
    return [round(value, 3) for value in rect]


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(Path.cwd()).as_posix()
    except ValueError:
        return path.as_posix()


def write_experiment_output(
    source_path: Path = DEFAULT_SOURCE_PATH,
    output_path: Path = DEFAULT_OUTPUT_PATH,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output = extract_pymupdf_tables(source_path)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    return output_path


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the GESB SAFF PyMuPDF table experiment.")
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE_PATH,
        help="Source GESB SAFF PDF.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Output JSON path for the PyMuPDF experiment.",
    )
    args = parser.parse_args(argv)
    output_path = write_experiment_output(args.source, args.output)
    print(f"PyMuPDF experiment JSON: {output_path}")


if __name__ == "__main__":
    main()
