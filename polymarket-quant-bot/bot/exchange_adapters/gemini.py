from __future__ import annotations

from typing import Any, Callable

from bot.exchange_adapters.base import ExchangeAdapter, OrderResult


class GeminiAdapter(ExchangeAdapter):
    def __init__(
        self,
        config: dict[str, Any],
        *,
        client_factory: Callable[[dict[str, Any]], Any] | None = None,
    ) -> None:
        super().__init__('gemini', rate_limit_per_second=float(config.get('rate_limit_per_second', 5.0)))
        self.config = config
        self._factory = client_factory
        self.client: Any | None = None

    async def connect(self) -> None:
        if self.client is not None:
            return
        if self._factory is not None:
            self.client = self._factory(self.config)
            return
        try:
            import ccxt.async_support as ccxt  # type: ignore
        except ImportError as exc:  # pragma: no cover - exercised in runtime only
            raise RuntimeError('ccxt is required for GeminiAdapter live usage') from exc
        self.client = ccxt.gemini(
            {
                'apiKey': self.config.get('api_key'),
                'secret': self.config.get('api_secret'),
                'enableRateLimit': True,
            }
        )

    async def fetch_price(self, symbol: str) -> float:
        await self.rate_limiter.acquire()
        await self.connect()
        assert self.client is not None
        ticker = await self.client.fetch_ticker(symbol)
        return float(ticker['last'])

    async def place_order(self, symbol: str, side: str, qty: float, order_type: str = 'market') -> OrderResult:
        await self.rate_limiter.acquire()
        await self.connect()
        assert self.client is not None
        raw = await self.client.create_order(symbol=symbol, type=order_type, side=side, amount=qty)
        return OrderResult(
            exchange=self.name,
            symbol=symbol,
            side=side,
            qty=qty,
            status=str(raw.get('status', 'submitted')),
            order_id=None if raw.get('id') is None else str(raw.get('id')),
            raw=raw,
        )

    async def close(self) -> None:
        if self.client is not None and hasattr(self.client, 'close'):
            await self.client.close()
