from __future__ import annotations

import os

from dotenv import load_dotenv


def _run_signal_shadow_mode() -> int:
    from strategy_signals import generate_read_only_signal
    from telegram_notify import send_signal_to_telegram

    dry_run = os.getenv("SIGNAL_TELEGRAM_DRY_RUN", "true").strip().lower() in {"1", "true", "yes", "on"}

    signal = generate_read_only_signal()
    print("[INFO] Generated read-only strategy signal.", flush=True)

    sent = send_signal_to_telegram(signal, dry_run=dry_run)
    return 0 if sent else 1


def main() -> int:
    load_dotenv()

    from api_check import run_all_checks

    mode = os.getenv("BOT_MODE", "check").strip().lower()

    if mode == "live":
        print(
            "[WARN] Live trading mode is not enabled in this bootstrap yet. "
            "Run with BOT_MODE=check first."
        )
        return 2

    print("[INFO] Running API connectivity checks...", flush=True)
    checks_ok = run_all_checks()
    if not checks_ok:
        return 1

    if mode == "signal":
        print("[INFO] Running signal shadow-mode (read-only, no orders).", flush=True)
        return _run_signal_shadow_mode()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
