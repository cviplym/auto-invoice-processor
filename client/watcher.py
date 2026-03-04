# client/watcher.py
# Watchdog 핸들러
from __future__ import annotations
import os
from watchdog.events import FileSystemEventHandler

from .stability import wait_until_stable
from .dedup import sha256_file, save_seen_hash
from .uploader import upload_document
from .writer import append_jsonl, append_csv

class NewFileHandler(FileSystemEventHandler):
    def __init__(
        self,
        *,
        server_url: str,
        doc_type: str,
        out_jsonl: str,
        out_csv: str,
        seen_hashes: set[str],
        seen_path: str,
        stable_checks: int = 3,
        stable_interval: float = 0.5,
    ):
        self.server_url = server_url
        self.doc_type = doc_type
        self.out_jsonl = out_jsonl
        self.out_csv = out_csv
        self.seen_hashes = seen_hashes
        self.seen_path = seen_path
        self.stable_checks = stable_checks
        self.stable_interval = stable_interval

    def on_created(self, event):
        if event.is_directory:
            return

        path = event.src_path
        print(f"📄 새 파일 감지: {path}")

        if not wait_until_stable(path, checks=self.stable_checks, interval_sec=self.stable_interval):
            print(f"⚠️ 파일 안정화 실패(복사 중일 수 있음): {path}")
            return

        try:
            h = sha256_file(path)
        except Exception as e:
            print(f"❌ 해시 계산 실패: {e}")
            return

        if h in self.seen_hashes:
            print(f"⏭️ 이미 처리한 파일(중복): {os.path.basename(path)}")
            return

        # 업로드
        try:
            result = upload_document(
                server_url=self.server_url,
                file_path=path,
                doc_type=self.doc_type,
            )
            print(f"✅ 처리 완료: {result}")
        except Exception as e:
            print(f"❌ 업로드/처리 실패: {e}")
            return

        # 저장 (source_file 포함)
        row = {"source_file": os.path.basename(path), **result}
        try:
            append_jsonl(self.out_jsonl, row)
            append_csv(self.out_csv, row)
        except Exception as e:
            print(f"❌ 결과 저장 실패: {e}")
            return

        # 중복 방지 기록
        self.seen_hashes.add(h)
        save_seen_hash(self.seen_path, h)