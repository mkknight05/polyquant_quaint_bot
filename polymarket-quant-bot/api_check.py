from __future__ import annotations

import os
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import httpx

TIMEOUT_SECONDS = float(os.getenv("API_CHECK_TIMEOUT_SECONDS", "4.0"))


@dataclass
class CheckResult:
    name: str
    ok: bool
    message: str


def _public_get(name: str, url: str) -> CheckResult:
    try:
        with httpx.Client(timeout=TIMEOUT_SECONDS, follow_redirects=True) as client:
            resp = client.get(url)
        if 200 <= resp.status_code < 300:
            return CheckResult(name=name, ok=True, message=f"reachable ({resp.status_code})")
        return CheckResult(name=name, ok=False, message=f"HTTP {resp.status_code}")
    except Exception as exc:  # pragma: no cover
        return CheckResult(name=name, ok=False, message=f"request failed: {exc}")


def _env_present(name: str, required: list[str]) -> CheckResult:
    missing = [k for k in required if not os.getenv(k)]
    if missing:
        return CheckResult(name=name, ok=False, message=f"missing env vars: {', '.join(missing)}")
    return CheckResult(name=name, ok=True, message="required env vars present")


def _kalshi_key_path_check() -> CheckResult:
    key_path = os.getenv("KALSHI_PRIVATE_KEY_PATH", "").strip()
    if not key_path:
        return CheckResult(name="Kalshi key path", ok=False, message="KALSHI_PRIVATE_KEY_PATH is empty")
    p = Path(key_path)
    if not p.exists():
        return CheckResult(name="Kalshi key path", ok=False, message=f"file not found: {p}")
    return CheckResult(name="Kalshi key path", ok=True, message=f"found {p}")


def _telegram_auth_check() -> CheckResult:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return CheckResult(name="Telegram", ok=False, message="missing TELEGRAM_BOT_TOKEN")

    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        with httpx.Client(timeout=TIMEOUT_SECONDS) as client:
            resp = client.get(url)
        if resp.status_code != 200:
            return CheckResult(name="Telegram", ok=False, message=f"HTTP {resp.status_code}")
        data = resp.json()
        if data.get("ok"):
            bot_user = data.get("result", {}).get("username", "unknown")
            return CheckResult(name="Telegram", ok=True, message=f"bot authenticated (@{bot_user})")
        return CheckResult(name="Telegram", ok=False, message=f"auth failed: {data}")
    except Exception as exc:  # pragma: no cover
        return CheckResult(name="Telegram", ok=False, message=f"request failed: {exc}")


def _run_check(task: tuple[str, Callable[[], CheckResult]]) -> CheckResult:
    name, fn = task
    print(f"[INFO] Checking {name}...", flush=True)
    started = time.perf_counter()
    result = fn()
    elapsed = time.perf_counter() - started
    status = "PASS" if result.ok else "FAIL"
    print(f"[{status}] {result.name}: {result.message} ({elapsed:.2f}s)", flush=True)
    return result


def run_all_checks() -> bool:
    checks: list[tuple[str, Callable[[], CheckResult]]] = [
        (
            "Coinbase public API",
            lambda: _public_get("Coinbase public API", os.getenv("COINBASE_BASE_URL", "https://api.coinbase.com") + "/v2/time"),
        ),
        ("Coinbase credentials", lambda: _env_present("Coinbase credentials", ["COINBASE_API_KEY", "COINBASE_API_SECRET"])),
        (
            "OKX public API",
            lambda: _public_get("OKX public API", os.getenv("OKX_BASE_URL", "https://www.okx.com") + "/api/v5/public/time"),
        ),
        ("OKX credentials", lambda: _env_present("OKX credentials", ["OKX_API_KEY", "OKX_API_SECRET", "OKX_PASSPHRASE"])),
        (
            "Polymarket public API",
            lambda: _public_get(
                "Polymarket public API", os.getenv("POLYMARKET_BASE_URL", "https://gamma-api.polymarket.com") + "/events?limit=1"
            ),
        ),
        (
            "Polymarket credentials",
            lambda: _env_present("Polymarket credentials", ["POLYMARKET_API_KEY", "POLYMARKET_API_SECRET", "POLYMARKET_PASSPHRASE"]),
        ),
        (
            "Kalshi public API",
            lambda: _public_get(
                "Kalshi public API", os.getenv("KALSHI_BASE_URL", "https://api.elections.kalshi.com") + "/trade-api/v2/exchange/status"
            ),
        ),
        ("Kalshi credentials", lambda: _env_present("Kalshi credentials", ["KALSHI_API_KEY_ID", "KALSHI_PRIVATE_KEY_PATH"])),
        ("Kalshi key path", _kalshi_key_path_check),
        (
            "Gemini public API",
            lambda: _public_get("Gemini public API", os.getenv("GEMINI_BASE_URL", "https://api.gemini.com") + "/v1/heartbeat"),
        ),
        ("Gemini credentials", lambda: _env_present("Gemini credentials", ["GEMINI_API_KEY", "GEMINI_API_SECRET"])),
        ("Telegram", _telegram_auth_check),
    ]

    print(f"\n=== API Check Report (timeout={TIMEOUT_SECONDS:.1f}s per network call) ===", flush=True)

    with ThreadPoolExecutor(max_workers=min(8, len(checks))) as pool:
        results = list(pool.map(_run_check, checks))

    failures = sum(1 for item in results if not item.ok)
    print(f"\nSummary: {len(results) - failures}/{len(results)} checks passed.", flush=True)
    return failures == 0
