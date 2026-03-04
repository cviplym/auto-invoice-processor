# server/providers/base.py
from abc import ABC, abstractmethod

class BaseProvider(ABC):
    """
    어떤 모델/벤더든 아래 인터페이스만 맞추면 app.py는 수정 없이 동작.
    - generate(...)는 모델의 raw text를 반환(그 raw text는 JSON을 포함해야 함)
    """
    @abstractmethod
    def generate(self, *, file_bytes: bytes, mime_type: str, prompt: str) -> str:
        raise NotImplementedError