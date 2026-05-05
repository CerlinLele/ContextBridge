# ContextBridge Parsers

## Run the GESB SAFF PDF Parser

After activating `.venv` and installing the package:

```powershell
parse-gesb-saff-pdf
```

Or run the local script directly:

```powershell
python src\contextbridge_parser\parsers\scripts\parse_gesb_saff_pdf.py
```

The parser writes artifacts to:

```text
knowledge_base/processed/structured-business-file-formats/saff/specifications/gesb/
```

Expected outputs:

```text
superstream-payroll-data-specification.parsed.json
superstream-payroll-data-specification.dependency-trace.json
```
