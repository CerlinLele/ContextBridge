"""Local entry point for parsing the GESB SAFF PDF."""

from __future__ import annotations

import sys
from pathlib import Path


SRC = Path(__file__).resolve().parents[3]
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from contextbridge_parser.parsers.pdf.gesb_saff import main


if __name__ == "__main__":
    raise SystemExit(main())
