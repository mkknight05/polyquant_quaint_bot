"""Copy this file when adding a new exchange adapter.

Steps:
1. Rename class and filename.
2. Implement connect/fetch_price/place_order.
3. Add tests mirroring tests/test_gemini_adapter.py.
"""

from __future__ import annotations

from typing import Any

from bot.exchange_adapters.base import ExchangeAdapter, OrderResult


class TemplateExchangeAdapter(ExchangeAdapter):
    def __init__(self, config: dict[str, Any]) -> None:
        super().__init__('template', rate_limit_per_second=float(config.get('rate_limit_per_second', 5.0)))
        self.config = config

    async def connect(self) -> None:
        # Initialize SDK client here.
        return None

    async def fetch_price(self, symbol: str) -> float:
        await self.rate_limiter.acquire()
        await self.connect()
        raise NotImplementedError('implement fetch_price for your exchange')

    async def place_order(self, symbol: str, side: str, qty: float, order_type: str = 'market') -> OrderResult:
        await self.rate_limiter.acquire()
        await self.connect()
        raise NotImplementedError('implement place_order for your exchange')
