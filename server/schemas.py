# server/schemas.py
from typing import Optional, Literal, Any, Dict
from pydantic import BaseModel, Field

DocType = Literal["invoice", "receipt", "document"]

class ExtractedDoc(BaseModel):
    """
    Provider/모델과 무관하게 서버가 반환하는 '공통' 응답 스키마.
    """
    vendor: Optional[str] = None
    date: Optional[str] = None          # ideally YYYY-MM-DD
    total_amount: Optional[float] = None
    currency: Optional[str] = None      # e.g., KRW, USD
    meta: Dict[str, Any] = Field(default_factory=dict)