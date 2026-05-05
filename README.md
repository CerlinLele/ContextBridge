# ContextBridge

## Local Python Environment

Create a local virtual environment from the repository root.

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

If PowerShell blocks activation scripts, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Optional Parser Dependencies

The base install includes the required dependency for the current GESB SAFF PDF parser:

```text
pypdf
```

Install optional PDF table tooling when working on richer PDF extraction:

```powershell
python -m pip install -e ".[pdf]"
```

Install OCR tooling when screenshot or scanned PDF extraction is needed:

```powershell
python -m pip install -e ".[ocr]"
```

Install document AI tooling for parser experiments:

```powershell
python -m pip install -e ".[document-ai]"
```

Install development tooling:

```powershell
python -m pip install -e ".[dev]"
```

## Run the GESB SAFF PDF Parser

See `src/contextbridge_parser/parsers/README.md`.

## Verify the Setup

```powershell
python -c "import pypdf; print(pypdf.__version__)"
python -m compileall -q src
```
