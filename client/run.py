# client/run.py
# 실행 엔트리 포인트
from __future__ import annotations
import argparse
import time
from pathlib import Path

from watchdog.observers import Observer

from .watcher import NewFileHandler
from .dedup import load_seen_hashes

def parse_args():
    p = argparse.ArgumentParser(description="Inbox watcher → server upload → outbox save")
    p.add_argument("--inbox", type=str, default="./inbox", help="folder to watch")
    p.add_argument("--server", type=str, default="http://localhost:8000", help="FastAPI server URL")
    p.add_argument("--doc-type", type=str, default="receipt", choices=["receipt", "invoice", "document"])
    p.add_argument("--out-jsonl", type=str, default="./outbox/results.jsonl")
    p.add_argument("--out-csv", type=str, default="./outbox/results.csv")
    p.add_argument("--seen", type=str, default="./outbox/seen_hashes.txt")
    p.add_argument("--stable-checks", type=int, default=3)
    p.add_argument("--stable-interval", type=float, default=0.5)
    return p.parse_args()

def main():
    args = parse_args()

    Path(args.inbox).mkdir(parents=True, exist_ok=True)
    Path("./outbox").mkdir(parents=True, exist_ok=True)

    seen_hashes = load_seen_hashes(args.seen)

    event_handler = NewFileHandler(
        server_url=args.server,
        doc_type=args.doc_type,
        out_jsonl=args.out_jsonl,
        out_csv=args.out_csv,
        seen_hashes=seen_hashes,
        seen_path=args.seen,
        stable_checks=args.stable_checks,
        stable_interval=args.stable_interval,
    )

    observer = Observer()
    observer.schedule(event_handler, args.inbox, recursive=False)

    print(f"🚀 inbox 감시 시작: {args.inbox}")
    print(f"   server: {args.server}")
    print(f"   doc_type: {args.doc_type}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 종료")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()