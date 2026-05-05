"""Parser for the GESB SAFF payroll data specification PDF."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import platform
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pypdf import PdfReader

from contextbridge_parser.parsers.pdf.common.pages import read_pdf_pages
from contextbridge_parser.parsers.pdf.common.sections import parse_numbered_section_heading
from contextbridge_parser.parsers.pdf.common.text import (
    clean_text_lines,
    normalize_space as _normalize_space,
)


PARSER_NAME = "gesb-saff-pdf"
PARSER_VERSION = "0.1.0"
PARSER_PROFILE = "pdf-table-aware-specification"

DEFAULT_SOURCE_PATH = Path(
    "knowledge_base/sources/structured-business-file-formats/saff/"
    "specifications/gesb/superstream-payroll-data-specification.pdf"
)
DEFAULT_OUTPUT_DIR = Path(
    "knowledge_base/processed/structured-business-file-formats/saff/"
    "specifications/gesb"
)

TABLE_PAGE_START = 10
TABLE_PAGE_END = 27
SAMPLE_PAGE_START = 28
SAMPLE_PAGE_END = 34
SECTION_HEADING_PREFIXES = tuple(f"{section}." for section in range(1, 13))


@dataclass(frozen=True)
class ParseOutputs:
    parsed_json: Path
    dependency_trace_json: Path


def parse_gesb_saff_pdf(source_path: Path) -> dict[str, Any]:
    """Parse the GESB SAFF PDF into section chunks and field rows."""

    source_path = source_path.resolve()
    reader = PdfReader(str(source_path))
    metadata = _read_metadata(reader)
    pages = read_pdf_pages(
        reader,
        clean_lines=_clean_lines,
        parse_section_heading=_parse_section_heading,
    )
    field_rows = _extract_field_rows(pages)
    section_chunks = _extract_section_chunks(pages[:9])
    sample_pages = _extract_sample_page_notes(pages)

    return {
        "parser": {
            "name": PARSER_NAME,
            "version": PARSER_VERSION,
            "profile": PARSER_PROFILE,
        },
        "source": {
            "path": _display_path(source_path),
            "sha256": _sha256(source_path),
            "document_title": metadata.get("title"),
            "document_version": _detect_document_version(pages),
            "document_date": _detect_document_date(pages),
            "page_count": len(reader.pages),
            "encrypted": reader.is_encrypted,
            "metadata": metadata,
        },
        "page_characteristics": pages,
        "section_chunks": section_chunks,
        "field_rows": field_rows,
        "sample_pages": sample_pages,
        "quality_notes": _quality_notes(pages, field_rows),
    }


def write_parse_outputs(
    source_path: Path = DEFAULT_SOURCE_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> ParseOutputs:
    """Parse the source PDF and write parsed artifacts plus dependency trace."""

    output_dir.mkdir(parents=True, exist_ok=True)
    parsed = parse_gesb_saff_pdf(source_path)

    parsed_json = output_dir / "superstream-payroll-data-specification.parsed.json"
    dependency_trace_json = (
        output_dir / "superstream-payroll-data-specification.dependency-trace.json"
    )

    _write_json(parsed_json, parsed)
    trace = build_dependency_trace(source_path, [parsed_json, dependency_trace_json])
    _write_json(dependency_trace_json, trace)

    return ParseOutputs(
        parsed_json=parsed_json,
        dependency_trace_json=dependency_trace_json,
    )


def build_dependency_trace(source_path: Path, outputs: list[Path]) -> dict[str, Any]:
    """Build a machine-readable dependency trace for this parser run."""

    dependencies = [
        {
            "package": "pypdf",
            "module": "pypdf",
            "required": True,
            "role": "PDF metadata, page text, and image object inspection",
        },
        {
            "package": "pymupdf",
            "module": "fitz",
            "required": False,
            "role": "Recommended future table and coordinate-aware extraction",
        },
        {
            "package": "pdfplumber",
            "module": "pdfplumber",
            "required": False,
            "role": "Recommended future table debugging and visual inspection",
        },
        {
            "package": "docling",
            "module": "docling",
            "required": False,
            "role": "Optional higher-level document conversion benchmark",
        },
        {
            "package": "unstructured",
            "module": "unstructured",
            "required": False,
            "role": "Optional generic PDF partitioning and OCR fallback",
        },
        {
            "package": "pytesseract",
            "module": "pytesseract",
            "required": False,
            "role": "Optional OCR integration for screenshot-heavy pages",
        },
    ]

    return {
        "trace_schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": {
            "path": _display_path(source_path.resolve()),
            "sha256": _sha256(source_path),
        },
        "parser": {
            "name": PARSER_NAME,
            "version": PARSER_VERSION,
            "profile": PARSER_PROFILE,
            "module": "contextbridge_parser.parsers.pdf.sources.gesb.saff",
        },
        "runtime": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "platform": platform.platform(),
        },
        "dependencies": [_dependency_status(dep) for dep in dependencies],
        "outputs": [_display_path(path.resolve()) for path in outputs],
    }


def _read_metadata(reader: PdfReader) -> dict[str, Any]:
    metadata = reader.metadata or {}
    normalized = {}
    for key, value in metadata.items():
        normalized[str(key).lstrip("/").lower()] = str(value)
    return normalized


def _extract_section_chunks(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    chunks: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for page in pages:
        for line in page["lines"]:
            heading = _parse_section_heading(line)
            if heading:
                if current and current["text"].strip():
                    chunks.append(_finalize_section_chunk(current))
                current = {
                    "chunk_type": "section_summary",
                    "section_number": heading[0],
                    "section_title": heading[1],
                    "start_page": page["page_number"],
                    "end_page": page["page_number"],
                    "text": line,
                }
                continue

            if current:
                current["end_page"] = page["page_number"]
                current["text"] += "\n" + line

    if current and current["text"].strip():
        chunks.append(_finalize_section_chunk(current))

    return chunks


def _finalize_section_chunk(chunk: dict[str, Any]) -> dict[str, Any]:
    text = _normalize_space(chunk["text"])
    return {
        "chunk_type": chunk["chunk_type"],
        "section_number": chunk["section_number"],
        "section_title": chunk["section_title"],
        "start_page": chunk["start_page"],
        "end_page": chunk["end_page"],
        "text": text,
    }


def _extract_field_rows(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    current: dict[str, Any] | None = None
    current_section = {"section_number": None, "section_title": None}

    for page in pages:
        page_number = page["page_number"]
        if page_number < TABLE_PAGE_START or page_number > TABLE_PAGE_END:
            continue

        for line in page["lines"]:
            section_heading = _parse_section_heading(line)
            if section_heading:
                if current:
                    rows.append(_normalize_field_row(current))
                    current = None
                current_section = {
                    "section_number": section_heading[0],
                    "section_title": section_heading[1],
                }
                continue

            if _is_table_header_line(line):
                continue

            row_start = re.match(r"^(?P<column>\d{1,3})\s+(?P<body>.+)$", line)
            if row_start:
                column_number = int(row_start.group("column"))
                if column_number == 0 or _is_numbered_value_line(row_start.group("body")):
                    if current:
                        current["end_page"] = page_number
                        current["raw_lines"].append(line)
                    continue
                if current:
                    rows.append(_normalize_field_row(current))
                current = {
                    "chunk_type": "field_specification_row",
                    "page_number": page_number,
                    "start_page": page_number,
                    "end_page": page_number,
                    "section_number": current_section["section_number"],
                    "section_title": current_section["section_title"],
                    "column_number": column_number,
                    "raw_lines": [line],
                }
                continue

            if current and line:
                current["end_page"] = page_number
                current["raw_lines"].append(line)

    if current:
        rows.append(_normalize_field_row(current))

    return rows


def _normalize_field_row(row: dict[str, Any]) -> dict[str, Any]:
    raw_text = _normalize_space(" ".join(row["raw_lines"]))
    body = re.sub(r"^\d{1,3}\s+", "", raw_text, count=1)
    field_name, description = _split_field_name_and_description(body)
    requirements_text = _extract_requirements_text(body)

    return {
        "chunk_type": row["chunk_type"],
        "row_subtype": _row_subtype(row["section_number"]),
        "page_number": row["page_number"],
        "start_page": row["start_page"],
        "end_page": row["end_page"],
        "section_number": row["section_number"],
        "section_title": row["section_title"],
        "column_number": row["column_number"],
        "field_name": field_name,
        "description": description,
        "requirements_text": requirements_text,
        "mandatory": _extract_mandatory(body),
        "required_by_gesb": _extract_required_by_gesb(body),
        "data_type": _extract_labeled_value(body, "Data Type"),
        "length": _extract_labeled_value(body, "Length"),
        "format": _extract_labeled_value(body, "Format"),
        "values": _extract_labeled_value(body, "Value(s)"),
        "notes": _extract_labeled_value(body, "Notes"),
        "references": _extract_references(body),
        "raw_text": raw_text,
        "parser_profile": PARSER_PROFILE,
        "parser_version": PARSER_VERSION,
    }


def _extract_sample_page_notes(pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sample_pages = []
    for page in pages:
        page_number = page["page_number"]
        if SAMPLE_PAGE_START <= page_number <= SAMPLE_PAGE_END:
            sample_pages.append(
                {
                    "chunk_type": "sample_file_screenshot_note",
                    "page_number": page_number,
                    "text_char_count": page["text_char_count"],
                    "image_count": page["image_count"],
                    "note": (
                        "Sample SAFF content appears image-heavy in this PDF. "
                        "Prefer the ATO XLSX source for structured sample data."
                    ),
                    "text": page["text"],
                }
            )
    return sample_pages


def _split_field_name_and_description(body: str) -> tuple[str | None, str | None]:
    body = _normalize_space(body)
    requirement_start = _first_requirement_index(body)
    pre_requirement = body[:requirement_start].strip() if requirement_start else body
    split_markers = [
        r"\bHeading text\b",
        r"\bVersion number\b",
        r"\bLine ID column header\b",
        r"\bColumn header\b",
        r"\bIf used\b",
        r"\bIdentifies\b",
        r"\bIndicates\b",
        r"\bRegistered\b",
        r"\bFull name\b",
        r"\bContact details\b",
        r"\bDetails of\b",
        r"\bLink an\b",
        r"\bSuperannuation fund generated\b",
        r"\bUSI identifying\b",
        r"\bThis value\b",
        r"\bSpecifies\b",
        r"\bDate on\b",
        r"\bUnique\b",
        r"\bCode used\b",
        r"\bThe amount\b",
        r"\bThe number\b",
        r"\bThe Australian mobile\b",
        r"\bBSB of\b",
        r"\bAccount number\b",
        r"\bAccount name\b",
        r"\bIf the\b",
        r"\bA term\b",
        r"\bAwards\b",
        r"\bThe person's\b",
        r"\bThe name\b",
        r"\bThe biological\b",
        r"\bThe year\b",
        r"\bThe current\b",
        r"\bMember's\b",
        r"\bEmployment start\b",
        r"\bEmployment end\b",
        r"\bPayroll tax\b",
        r"\bPay period\b",
        r"\bContribution made\b",
        r"\bA contribution\b",
        r"\bSalary sacrificing\b",
        r"\bUsed to identify\b",
        r"\bAn indicator\b",
        r"\bDate the\b",
        r"\bHours\b",
        r"\bNot used\b",
    ]

    first_match: re.Match[str] | None = None
    for marker in split_markers:
        match = re.search(marker, pre_requirement)
        if (
            match
            and match.start() > 0
            and (first_match is None or match.start() < first_match.start())
        ):
            first_match = match

    if first_match:
        field_name = pre_requirement[: first_match.start()].strip()
        description = pre_requirement[first_match.start() :].strip()
    else:
        repeated = _split_repeated_phrase(pre_requirement)
        if repeated:
            field_name, description = repeated
        else:
            field_name = pre_requirement
            description = None

    field_name = _normalize_space(field_name) if field_name else None
    description = _strip_after_requirement_markers(description) if description else None
    return field_name or None, description or None


def _split_repeated_phrase(value: str) -> tuple[str, str] | None:
    words = value.split()
    if len(words) < 2 or len(words) % 2 != 0:
        return None
    middle = len(words) // 2
    first = words[:middle]
    second = words[middle:]
    if first == second:
        phrase = " ".join(first)
        return phrase, phrase
    return None


def _row_subtype(section_number: str | None) -> str:
    if section_number and section_number.startswith("11.4."):
        return "data_row_field"
    return "format_control_row"


def _extract_requirements_text(body: str) -> str | None:
    markers = ["Mandatory:", "Refer to MIG", "Not accepted by GESB", "Leave blank"]
    start_positions = [body.find(marker) for marker in markers if body.find(marker) >= 0]
    if not start_positions:
        return None
    return _normalize_space(body[min(start_positions) :])


def _extract_mandatory(body: str) -> str | None:
    match = re.search(
        r"Mandatory:\s*(?P<mandatory>.+?)\s+(?P<required>Yes|No)\s+(?=Sec\.|N/A)",
        body,
    )
    if match:
        return _normalize_space(match.group("mandatory"))

    match = re.search(r"Mandatory:\s*(?P<mandatory>.+?)(?=\s+Data Type:|\s+Length:|$)", body)
    if match:
        return _normalize_space(match.group("mandatory"))

    if "Not used" in body:
        return "Not used"

    return None


def _extract_required_by_gesb(body: str) -> str | None:
    mandatory = re.search(
        r"Mandatory:\s*.+?\s+(?P<required>Yes|No)\s+(?=Sec\.|N/A)",
        body,
    )
    if mandatory:
        return mandatory.group("required")

    refer = re.search(r"Refer to MIG\s+(?P<required>Yes|No)\s+(?=Sec\.|N/A)", body)
    if refer:
        return refer.group("required")

    not_used = re.search(r"(?:Not accepted by GESB|Leave blank)\s+(?P<required>Yes|No)\s+", body)
    if not_used:
        return not_used.group("required")

    return None


def _extract_labeled_value(body: str, label: str) -> str | None:
    labels = ["Data Type", "Length", "Format", "Value(s)", "Notes"]
    following_labels = [item for item in labels if item != label]
    lookahead = "|".join(re.escape(item) + r":" for item in following_labels)
    pattern = rf"{re.escape(label)}:\s*(?P<value>.*?)(?=\s+(?:{lookahead})|$)"
    match = re.search(pattern, body)
    if not match:
        return None
    value = _normalize_space(match.group("value"))
    return value or None


def _extract_references(body: str) -> dict[str, Any]:
    references = re.findall(r"(?:Sec\.|Seq\.|Id\.)\s*[\d.]+|N/A", body)
    return {
        "raw_references": references,
        "mig_reference": references[0] if references else None,
        "des_reference": references[-1] if len(references) > 1 else None,
    }


def _quality_notes(pages: list[dict[str, Any]], field_rows: list[dict[str, Any]]) -> list[str]:
    notes = []
    missing_names = [
        row["column_number"] for row in field_rows if not row.get("field_name")
    ]
    if missing_names:
        notes.append(
            "Some field names could not be normalized from pypdf text order: "
            + ", ".join(str(item) for item in missing_names)
        )

    sample_image_pages = [
        page["page_number"]
        for page in pages
        if page["page_number"] >= SAMPLE_PAGE_START and page["image_count"] > 0
    ]
    if sample_image_pages:
        notes.append(
            "Sample pages contain embedded images and may need OCR if screenshot "
            "content is required: "
            + ", ".join(str(item) for item in sample_image_pages)
        )

    return notes


def _clean_lines(lines: list[str]) -> list[str]:
    return clean_text_lines(lines, keep_line=_is_gesb_content_line)


def _is_gesb_content_line(line: str) -> bool:
    if line == "Government Employees Superannuation Board (GESB)":
        return False
    if re.fullmatch(r"Page\s+\d+", line):
        return False
    return True


def _parse_section_heading(line: str) -> tuple[str, str] | None:
    return parse_numbered_section_heading(
        line,
        allowed_prefixes=SECTION_HEADING_PREFIXES,
    )


def _is_table_header_line(line: str) -> bool:
    headers = {
        "Column Field Name Description Requirements Required",
        "Column Field Name Description Requirements Required by GESB?",
        "Column Field Name Description      Requirements Required",
        "by GESB?",
        "MIG 2.0",
        "Reference",
        "DES Spec",
        "DES Spec 5.8",
        "5.8",
        "Required",
        "etc",
    }
    return line in headers


def _is_numbered_value_line(body: str) -> bool:
    return body.lstrip().startswith(("-", "–", "—"))


def _detect_document_version(pages: list[dict[str, Any]]) -> str | None:
    text = pages[0]["text"] if pages else ""
    match = re.search(r"Version number:\s*([^\s]+)", text)
    return match.group(1) if match else None


def _detect_document_date(pages: list[dict[str, Any]]) -> str | None:
    text = pages[0]["text"] if pages else ""
    match = re.search(r"Date updated:\s*([0-9/]+)", text)
    return match.group(1) if match else None


def _first_requirement_index(body: str) -> int | None:
    markers = ["Mandatory:", "Refer to MIG", "Not accepted by GESB", "Leave blank", "Data Type:"]
    positions = [body.find(marker) for marker in markers if body.find(marker) >= 0]
    return min(positions) if positions else None


def _strip_after_requirement_markers(text: str | None) -> str | None:
    if not text:
        return None
    index = _first_requirement_index(text)
    value = text[:index].strip() if index else text.strip()
    return _normalize_space(value) or None


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def _dependency_status(dependency: dict[str, Any]) -> dict[str, Any]:
    module = dependency["module"]
    package = dependency["package"]
    available = importlib.util.find_spec(module) is not None
    version = None
    if available:
        try:
            version = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            version = "unknown"

    return {
        **dependency,
        "available": available,
        "version": version,
    }


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Parse the GESB SAFF PDF.")
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE_PATH,
        help="Path to the GESB SAFF PDF source file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for parsed artifacts.",
    )
    args = parser.parse_args(argv)

    outputs = write_parse_outputs(args.source, args.output_dir)
    print(f"Parsed JSON: {outputs.parsed_json}")
    print(f"Dependency trace: {outputs.dependency_trace_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
