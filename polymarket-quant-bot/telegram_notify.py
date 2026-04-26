from __future__ import annotations

import os

import httpx

from strategy_signals import StrategySignal


TELEGRAM_TIMEOUT_SECONDS = float(os.getenv("TELEGRAM_TIMEOUT_SECONDS", "5"))


def send_signal_to_telegram(signal: StrategySignal, dry_run: bool = True) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    message = signal.to_text()

    if dry_run:
        print(f"[DRY-RUN] Telegram message preview:\n{message}", flush=True)
        return True

    if not token or not chat_id:
        print("[FAIL] Telegram dispatch skipped: missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID", flush=True)
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "disable_web_page_preview": True,
    }

    try:
        with httpx.Client(timeout=TELEGRAM_TIMEOUT_SECONDS) as client:
            resp = client.post(url, json=payload)
        if resp.status_code != 200:
            print(f"[FAIL] Telegram dispatch failed: HTTP {resp.status_code}", flush=True)
            return False
        data = resp.json()
        if not data.get("ok"):
            print(f"[FAIL] Telegram dispatch failed: {data}", flush=True)
            return False
        print("[PASS] Telegram dispatch succeeded.", flush=True)
        return True
    except Exception as exc:  # pragma: no cover
        print(f"[FAIL] Telegram dispatch failed: {exc}", flush=True)
        return False
