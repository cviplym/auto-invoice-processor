# server/app.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from dotenv import load_dotenv

from .config import load_settings
from .schemas import DocType, ExtractedDoc
from .parser import extract_json_object
from .providers import get_provider

import traceback

load_dotenv()
app = FastAPI(title="Invoice Auto Processor API", version="0.1.0")

settings = load_settings()

def build_prompt(doc_type: DocType) -> str:
    # provider와 무관한 prompt (로컬 모델로 교체해도 동일하게 사용 가능)
    return (
        f"You are a document parser. Extract key fields from this {doc_type}. "
        "Return ONLY a valid JSON object with keys: vendor, date, total_amount, currency. "
        "Rules: "
        "1) If missing, set the value to null. "
        "2) date should be ISO format YYYY-MM-DD when possible. "
        "3) total_amount must be a number (no commas, no currency symbols). "
        "4) No markdown, no extra text."
    )

# provider init (lazy init보다 여기서 잡는 게 디버그가 쉬움)
try:
    provider = get_provider(settings)
    provider_ready = True
    provider_error = ""
except Exception as e:
    provider = None
    provider_ready = False
    provider_error = str(e)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "provider": settings.provider,
        "provider_ready": provider_ready,
        "provider_error": provider_error,
    }

@app.post("/process")
async def process_document(
    file: UploadFile = File(...),
    doc_type: DocType = Form("receipt"),
):
    if not provider_ready or provider is None:
        raise HTTPException(status_code=500, detail=f"Provider init failed: {provider_error}")

    file_bytes = await file.read()
    max_bytes = settings.max_file_mb * 1024 * 1024
    if len(file_bytes) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File too large (max {settings.max_file_mb}MB)")

    mime_type = file.content_type or "application/octet-stream"
    prompt = build_prompt(doc_type)

    try:
        raw = provider.generate(file_bytes=file_bytes, mime_type=mime_type, prompt=prompt)
    except Exception as e:
        # traceback.print_exc() # 자세한 에러 사항 알고 싶을 때
        raise HTTPException(status_code=502, detail=f"Upstream provider error: {str(e)}")

    try:
        payload = extract_json_object(raw)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model output parse failed: {str(e)}")

    # normalize to ExtractedDoc
    total = payload.get("total_amount", None)
    if isinstance(total, str):
        try:
            total = float(total.replace(",", "").strip())
        except Exception:
            total = None

    doc = ExtractedDoc(
        vendor=payload.get("vendor"),
        date=payload.get("date"),
        total_amount=total if isinstance(total, (int, float)) else None,
        currency=payload.get("currency"),
        meta={k: v for k, v in payload.items() if k not in {"vendor", "date", "total_amount", "currency"}},
    )
    return doc.model_dump()