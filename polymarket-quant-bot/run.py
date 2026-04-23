from __future__ import annotations

import os

from api_check import run_all_checks


def main() -> int:
    mode = os.getenv("BOT_MODE", "check").strip().lower()

    if mode == "live":
        print(
            "[WARN] Live trading mode is not enabled in this bootstrap yet. "
            "Run with BOT_MODE=check first."
        )
        return 2

    print("[INFO] Running API connectivity checks...", flush=True)
    ok = run_all_checks()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
