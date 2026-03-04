# Auto Invoice Processor

A simple **Document AI pipeline** that watches an `inbox` folder, uploads documents to a FastAPI server, extracts structured data using Gemini API, and stores results as JSON/CSV.

---

## Architecture

![Pipeline](docs/pipeline.png)

See detailed architecture:  
➡ [Architecture](docs/architecture.md)

---

## Quick Start

### Install

```bash
pip install -r server/requirements.txt
pip install -r client/requirements.txt
```

### Run Server

```bash
python -m uvicorn server.app:app --reload
```

### Run Client

```bash
python -m client.run --inbox ./inbox --server http://localhost:8000
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