# server/parser.py
import json
import re
from typing import Any, Dict

_JSON_BLOCK_RE = re.compile(r"\{.*\}", flags=re.DOTALL)

def strip_code_fences(text: str) -> str:
    t = text.strip()
    t = re.sub(r"^\s*```(?:json)?\s*", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\s*```\s*$", "", t)
    return t.strip()

def extract_json_object(text: str) -> Dict[str, Any]:
    """
    모델 출력에서 JSON object만 안전하게 추출.
    """
    cleaned = strip_code_fences(text)
    m = _JSON_BLOCK_RE.search(cleaned)
    if not m:
        raise ValueError("No JSON object found in model output.")
    blob = m.group(0)
    try:
        return json.loads(blob)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned by model: {e}") from e