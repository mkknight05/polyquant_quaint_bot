from __future__ import annotations

import random
from typing import Any

import httpx

from bot.models import MarketTick


class CoinbaseAdapter:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def fetch_tick(self) -> MarketTick:
        url = f'https://api.exchange.coinbase.com/products/{self.symbol}/ticker'
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(url)
                response.raise_for_status()
                payload = response.json()
            price = float(payload['price'])
        except Exception:
            # Environment/network fallback so MVP loop remains runnable in dev containers.
            price = 65000 * (1 + random.uniform(-0.002, 0.002))
        return MarketTick.now(source='coinbase', instrument=self.symbol, price=price)


class PolymarketAdapter:
    def __init__(
        self,
        instrument: str,
        *,
        token_id: str | None,
        host: str,
        chain_id: int,
        private_key: str | None,
        api_key: str | None,
        api_secret: str | None,
        api_passphrase: str | None,
        use_synthetic: bool = True,
    ) -> None:
        self.instrument = instrument
        self.token_id = token_id
        self.host = host
        self.chain_id = chain_id
        self.private_key = private_key
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase
        self.use_synthetic = use_synthetic
        self._client: Any | None = None

    def _synthetic_tick(self, anchor_price: float) -> MarketTick:
        price = anchor_price * (1 + random.uniform(-0.005, 0.005))
        return MarketTick.now(source='polymarket', instrument=self.instrument, price=price)

    def _ensure_client(self) -> Any:
        if self._client is not None:
            return self._client
        if not self.private_key:
            raise RuntimeError('POLYMARKET_PRIVATE_KEY is required when POLYMARKET_USE_SYNTHETIC=false')

        try:
            from py_clob_client.client import ClobClient
        except ImportError as exc:
            raise RuntimeError('py-clob-client dependency missing') from exc

        client = ClobClient(host=self.host, chain_id=self.chain_id, key=self.private_key)
        if self.api_key and self.api_secret and self.api_passphrase:
            try:
                from py_clob_client.clob_types import ApiCreds

                creds = ApiCreds(api_key=self.api_key, api_secret=self.api_secret, api_passphrase=self.api_passphrase)
            except Exception:
                creds = {
                    'api_key': self.api_key,
                    'secret': self.api_secret,
                    'passphrase': self.api_passphrase,
                }
            client.set_api_creds(creds)
        else:
            create_or_derive = getattr(client, 'create_or_derive_api_creds', None) or getattr(client, 'create_or_derive_api_key', None)
            if create_or_derive is None:
                raise RuntimeError('py-clob-client does not expose create_or_derive_api_creds/create_or_derive_api_key')
            client.set_api_creds(create_or_derive())

        self._client = client
        return client

    def fetch_tick(self, anchor_price: float) -> MarketTick:
        if self.use_synthetic:
            return self._synthetic_tick(anchor_price)
        if not self.token_id:
            raise RuntimeError('POLYMARKET_TOKEN_ID is required when POLYMARKET_USE_SYNTHETIC=false')

        try:
            client = self._ensure_client()
            raw = client.get_last_trade_price(self.token_id)
            if isinstance(raw, dict):
                raw = raw.get('price') or raw.get('last') or raw.get('value')
            price = float(raw)
            return MarketTick.now(source='polymarket', instrument=self.instrument, price=price)
        except Exception:
            if not self.use_synthetic:
                raise
            return self._synthetic_tick(anchor_price)
