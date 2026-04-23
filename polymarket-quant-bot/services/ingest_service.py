from __future__ import annotations

import argparse
import time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from bot.adapters import CoinbaseAdapter, PolymarketAdapter
from bot.config import settings
from bot.storage import Store


def run_ingest(iterations: int, sleep_seconds: float) -> None:
    store = Store(settings.sqlite_path)
    coinbase = CoinbaseAdapter(settings.symbol)
    polymarket = PolymarketAdapter(
        settings.symbol,
        token_id=settings.polymarket_token_id,
        host=settings.polymarket_host,
        chain_id=settings.polymarket_chain_id,
        private_key=settings.polymarket_private_key,
        api_key=settings.polymarket_api_key,
        api_secret=settings.polymarket_api_secret,
        api_passphrase=settings.polymarket_api_passphrase,
        use_synthetic=settings.polymarket_use_synthetic,
    )

    for step in range(iterations):
        cb_tick = coinbase.fetch_tick()
        pm_tick = polymarket.fetch_tick(anchor_price=cb_tick.price)
        store.add_tick(cb_tick)
        store.add_tick(pm_tick)
        print(f'[ingest:{step}] cb={cb_tick.price:.2f} pm={pm_tick.price:.2f}')
        if step < iterations - 1:
            time.sleep(sleep_seconds)

    print('ingest summary:', store.summary())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Ingest service for market data collection')
    parser.add_argument('--iterations', type=int, default=5)
    parser.add_argument('--sleep-seconds', type=float, default=1.0)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run_ingest(iterations=args.iterations, sleep_seconds=args.sleep_seconds)
