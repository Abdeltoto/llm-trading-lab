"""Worker minimal : heartbeat et verrouillage (extension Celery possible)."""

import time

from app.config import get_settings


def main() -> None:
    settings = get_settings()
    print(f"Worker LLM Trading Lab — mode {settings.trading_mode.value}")
    while settings.worker_enabled:
        time.sleep(60)
        print("worker:alive")


if __name__ == "__main__":
    main()
