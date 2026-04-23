import asyncio
import unittest

from bot.exchange_adapters.base import AdapterManager, ExchangeAdapter, OrderResult, RateLimiter
from bot.exchange_adapters.gemini import GeminiAdapter


class _FakeGeminiClient:
    async def fetch_ticker(self, symbol: str):
        return {'last': '123.45', 'symbol': symbol}

    async def create_order(self, symbol: str, type: str, side: str, amount: float):
        return {'id': 'ord-1', 'status': 'open', 'symbol': symbol, 'type': type, 'side': side, 'amount': amount}

    async def close(self):
        return None


class _FailAdapter(ExchangeAdapter):
    async def connect(self) -> None:
        return None

    async def fetch_price(self, symbol: str) -> float:
        raise RuntimeError('boom')

    async def place_order(self, symbol: str, side: str, qty: float, order_type: str = 'market') -> OrderResult:
        raise RuntimeError('boom')


class _PassAdapter(ExchangeAdapter):
    async def connect(self) -> None:
        return None

    async def fetch_price(self, symbol: str) -> float:
        return 42.0

    async def place_order(self, symbol: str, side: str, qty: float, order_type: str = 'market') -> OrderResult:
        return OrderResult(exchange=self.name, symbol=symbol, side=side, qty=qty, status='ok')


class GeminiAdapterTests(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_price_and_place_order(self) -> None:
        adapter = GeminiAdapter({}, client_factory=lambda _: _FakeGeminiClient())
        price = await adapter.fetch_price('BTC/USD')
        self.assertEqual(123.45, price)

        result = await adapter.place_order('BTC/USD', 'buy', 0.1)
        self.assertEqual('gemini', result.exchange)
        self.assertEqual('ord-1', result.order_id)

    async def test_adapter_manager_fallback(self) -> None:
        manager = AdapterManager([_FailAdapter('fail'), _PassAdapter('pass')])
        price, source = await manager.fetch_price_with_fallback('BTC/USD')
        self.assertEqual(42.0, price)
        self.assertEqual('pass', source)


class RateLimiterTests(unittest.IsolatedAsyncioTestCase):
    async def test_rate_limiter_waits(self) -> None:
        limiter = RateLimiter(per_second=100)
        await limiter.acquire()
        start = asyncio.get_event_loop().time()
        await limiter.acquire()
        elapsed = asyncio.get_event_loop().time() - start
        self.assertGreaterEqual(elapsed, 0.005)


if __name__ == '__main__':
    unittest.main()
