# Auto Invoice Processor (Gemini API + Folder Watcher)

A minimal end-to-end demo that watches an `inbox/` folder, uploads newly created files to a FastAPI server, extracts key fields via Gemini API, and stores results into `outbox/` as JSONL/CSV.

---

# Overview
![Pipeline](docs/pipeline.png)
This project demonstrates a simple **Document AI pipeline**.

Client → Server → LLM → Structured Data

Flow:

1. Client watches a folder (`./inbox`)
2. When a new file appears:
   - Wait until the file is fully written
   - Prevent duplicates (SHA256)
   - Upload file to the server
3. Server:
   - Sends the document to Gemini API
   - Extracts structured information
4. Client stores the result in:
   - `outbox/results.jsonl`
   - `outbox/results.csv`

---

# Repository Structure
```
auto-invoice-processor/

├── server/  
│   ├── app.py  
│   ├── config.py  
│   ├── schemas.py  
│   ├── parser.py  
│   └── providers/  
│       ├── base.py  
│       └── gemini.py  

├── client/  
│   ├── run.py  
│   ├── watcher.py  
│   ├── uploader.py  
│   ├── stability.py  
│   ├── writer.py  
│   └── dedup.py  

├── inbox/  
│   └── .gitkeep  

├── outbox/  
│   └── .gitkeep  

└── README.md  
```
---

# Requirements

Python **3.10+** recommended.

---

# Installation

## 1. Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
```

## 2. Install server dependencies

```bash
pip install -r server/requirements.txt
```

## 3. Install client dependencies

```bash
pip install -r client/requirements.txt
```

---

# Environment Variables

Configure Gemini API key.

Example:

```bash
export PROVIDER="gemini"
export GEMINI_API_KEY="YOUR_API_KEY"
export GEMINI_MODEL="gemini-2.5-flash"
```

Notes:

- `GEMINI_MODEL` must support `generateContent`
- Example valid models:
  - gemini-2.5-flash
  - gemini-2.5-pro

Check available models:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"
```

---

# Running the System

## Start the Server

From project root:

```bash
python -m uvicorn server.app:app --reload --host 0.0.0.0 --port 8000
```

Health check:

```
http://localhost:8000/health
```

Swagger UI:

```
http://localhost:8000/docs
```

---

## Start the Client

```bash
python -m client.run --inbox ./inbox --server http://localhost:8000 --doc-type receipt
```

---

## Test the Pipeline

Drop a document into:

```
./inbox
```

Supported examples:

- PDF invoices
- receipt images
- scanned documents

The client automatically uploads them.

Results are saved to:

```
./outbox/results.jsonl
./outbox/results.csv
```

---

# Example Output

Example JSON response from `/process`:

```json
{
  "vendor": "ABC Store",
  "date": "2026-03-04",
  "total_amount": 12345.0,
  "currency": "KRW",
  "meta": {}
}
```

---

# API

## POST /process

Upload document for processing.

Multipart form:

- file → document file
- doc_type → receipt | invoice | document

Example:

```bash
curl -X POST http://localhost:8000/process \
  -F "file=@invoice.pdf" \
  -F "doc_type=invoice"
```

---

# Troubleshooting

## Uvicorn using wrong Python version

If `uvicorn --version` shows Python 3.8:

```bash
python -m uvicorn server.app:app --reload
```

This ensures uvicorn uses the active Python environment.

---

## Gemini API returns 404

The model name is invalid.

List models:

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"
```

Then set:

```
GEMINI_MODEL=gemini-2.5-flash
```

---

## Rate limit (429)

Reduce request frequency or implement retry/backoff.

---

## JSON parsing failure

LLM may output non-JSON text.

Improve prompt constraints or add JSON extraction logic.

---

# Future Improvements

Possible extensions:

- Async job API
- Google Sheets integration
- Multiple LLM providers
- Local VLM backend (Qwen3-VL)
- Web UI for uploads