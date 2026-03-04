# client/uploader.py
# 서버로 업로드
from __future__ import annotations
import os
import mimetypes
import requests
from typing import Any, Dict, Optional

def guess_mime(path: str) -> str:
    mt, _ = mimetypes.guess_type(path)
    return mt or "application/octet-stream"

def upload_document(
    *,
    server_url: str,
    file_path: str,
    doc_type: str = "receipt",
    timeout_sec: int = 120,
) -> Dict[str, Any]:
    """
    FastAPI /process에 multipart로 업로드.
    server_url 예: http://localhost:8000
    """
    endpoint = server_url.rstrip("/") + "/process"

    mime = guess_mime(file_path)
    filename = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        files = {"file": (filename, f, mime)}
        data = {"doc_type": doc_type}

        r = requests.post(endpoint, files=files, data=data, timeout=timeout_sec)
        r.raise_for_status()
        return r.json()