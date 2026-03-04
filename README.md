# Auto Invoice Processor

A simple **Document AI pipeline** that watches an `inbox` folder, uploads documents to a FastAPI server, extracts structured data using Gemini API, and stores results as JSON/CSV.

---

## Architecture

![Pipeline](docs/pipeline.png)

See detailed architecture:  
➡ [Architecture](docs/architecture.md)

---

## Environment Settings

### 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
```

### 2. Install server dependencies

```bash
pip install -r server/requirements.txt
```

### 3. Install client dependencies

```bash
pip install -r client/requirements.txt
```
### 4. Environment Variables

Configure Gemini API key.

Example:

```bash
export PROVIDER="gemini"
export GEMINI_API_KEY="YOUR_API_KEY"
export GEMINI_MODEL="gemini-3.1-flash-lite-preview"
```
[More Gemini Models](docs/models-gemini.md)

## Quick Start

### Run Server

```bash
python -m uvicorn server.app:app --reload --host 0.0.0.0 --port 8000
```

### Run Client

```bash
python -m client.run --inbox ./inbox --server http://localhost:8000 --doc-type receipt # receipt, invoice, document
```

---

## Example Output

```json
{
  "vendor": "ABC Store",
  "date": "2026-03-04",
  "total_amount": 12345.0,
  "currency": "KRW"
}
```

---

## Documentation

More details:

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Gemini Models](docs/models-gemini.md)
- [TroubleShooting](docs/troubleshooting.md)