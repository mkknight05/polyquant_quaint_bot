import sys
import types
import unittest
from unittest.mock import patch

from bot.adapters import PolymarketAdapter


class _FakeClient:
    def __init__(self, host: str, chain_id: int, key: str) -> None:
        self.host = host
        self.chain_id = chain_id
        self.key = key
        self.set_creds = None

    def set_api_creds(self, creds):
        self.set_creds = creds

    def create_or_derive_api_creds(self):
        return {'api_key': 'k', 'secret': 's', 'passphrase': 'p'}

    def get_last_trade_price(self, token_id: str):
        return {'price': '0.42', 'token_id': token_id}


class _FakeApiCreds:
    def __init__(self, api_key: str, api_secret: str, api_passphrase: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = api_passphrase


class PolymarketAdapterTests(unittest.TestCase):
    def test_fetch_tick_uses_live_client_when_synthetic_disabled(self) -> None:
        adapter = PolymarketAdapter(
            'POLY',
            token_id='123',
            host='https://clob.polymarket.com',
            chain_id=137,
            private_key='0xabc',
            api_key=None,
            api_secret=None,
            api_passphrase=None,
            use_synthetic=False,
        )
        with patch.object(adapter, '_ensure_client', return_value=_FakeClient('h', 137, 'k')):
            tick = adapter.fetch_tick(anchor_price=1.0)
        self.assertEqual('polymarket', tick.source)
        self.assertAlmostEqual(0.42, tick.price)

    def test_ensure_client_builds_and_derives_api_creds(self) -> None:
        fake_client_module = types.SimpleNamespace(ClobClient=_FakeClient)
        fake_types_module = types.SimpleNamespace(ApiCreds=_FakeApiCreds)

        with patch.dict(sys.modules, {
            'py_clob_client': types.ModuleType('py_clob_client'),
            'py_clob_client.client': fake_client_module,
            'py_clob_client.clob_types': fake_types_module,
        }):
            adapter = PolymarketAdapter(
                'POLY',
                token_id='123',
                host='https://clob.polymarket.com',
                chain_id=137,
                private_key='0xabc',
                api_key='k',
                api_secret='s',
                api_passphrase='p',
                use_synthetic=False,
            )
            client = adapter._ensure_client()

        self.assertIsInstance(client, _FakeClient)
        self.assertIsNotNone(client.set_creds)


if __name__ == '__main__':
    unittest.main()
