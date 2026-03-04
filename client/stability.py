# client/stability.py
# 파일이 "쓰기 완료"될 때까지 대기
import os
import time

def wait_until_stable(path: str, checks: int = 3, interval_sec: float = 0.5) -> bool:
    """
    watchdog on_created는 파일이 아직 복사/다운로드 중일 때도 발생할 수 있음.
    파일 크기가 연속으로 동일해질 때까지 기다려서 부분 업로드 방지.
    """
    prev = -1
    for _ in range(checks):
        try:
            cur = os.path.getsize(path)
        except FileNotFoundError:
            time.sleep(interval_sec)
            continue

        if cur == prev and cur > 0:
            return True
        prev = cur
        time.sleep(interval_sec)
    return False