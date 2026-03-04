# client/dedup.py
# 중복 처리 방지: 파일 해시
import hashlib
from pathlib import Path

def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_seen_hashes(seen_path: str) -> set[str]:
    p = Path(seen_path)
    if not p.exists():
        return set()
    return set(x.strip() for x in p.read_text(encoding="utf-8").splitlines() if x.strip())

def save_seen_hash(seen_path: str, file_hash: str) -> None:
    p = Path(seen_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(file_hash + "\n")