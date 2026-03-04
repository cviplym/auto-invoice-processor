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
