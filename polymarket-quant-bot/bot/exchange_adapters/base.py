from __future__ import annotations

import abc
import asyncio
import time
from dataclasses import dataclass


@dataclass(slots=True)
class OrderResult:
    exchange: str
    symbol: str
    side: str
    qty: float
    status: str
    order_id: str | None = None
    raw: dict | None = None


class RateLimiter:
    def __init__(self, per_second: float) -> None:
        if per_second <= 0:
            raise ValueError('per_second must be > 0')
        self._interval = 1.0 / per_second
        self._lock = asyncio.Lock()
        self._last = 0.0

    async def acquire(self) -> None:
        async with self._lock:
            now = time.monotonic()
            wait = self._interval - (now - self._last)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last = time.monotonic()


class ExchangeAdapter(abc.ABC):
    def __init__(self, name: str, rate_limit_per_second: float = 5.0) -> None:
        self.name = name
        self.rate_limiter = RateLimiter(rate_limit_per_second)

    @abc.abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def fetch_price(self, symbol: str) -> float:
        raise NotImplementedError

    @abc.abstractmethod
    async def place_order(self, symbol: str, side: str, qty: float, order_type: str = 'market') -> OrderResult:
        raise NotImplementedError

    async def close(self) -> None:
        return None


class AdapterManager:
    def __init__(self, adapters: list[ExchangeAdapter]) -> None:
        self.adapters = adapters

    async def fetch_price_with_fallback(self, symbol: str) -> tuple[float, str]:
        last_error: Exception | None = None
        for adapter in self.adapters:
            try:
                price = await adapter.fetch_price(symbol)
                return price, adapter.name
            except Exception as exc:  # noqa: BLE001
                last_error = exc
        raise RuntimeError(f'all adapters failed for {symbol}: {last_error}')
