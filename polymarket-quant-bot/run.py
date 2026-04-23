from __future__ import annotations

import argparse
import time

from bot.adapters import CoinbaseAdapter, PolymarketAdapter
from bot.config import settings
from bot.paper import PaperBroker
from bot.storage import Store
from bot.strategy import SpreadStrategy


def run_loop(iterations: int, sleep_seconds: float) -> None:
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
    strategy = SpreadStrategy(threshold=settings.spread_threshold, qty=settings.trade_qty)
    broker = PaperBroker(starting_cash=settings.starting_cash)

    for step in range(iterations):
        cb_tick = coinbase.fetch_tick()
        pm_tick = polymarket.fetch_tick(anchor_price=cb_tick.price)
        store.add_tick(cb_tick)
        store.add_tick(pm_tick)

        signal = strategy.generate(settings.symbol, price_a=cb_tick.price, price_b=pm_tick.price)
        if signal is not None:
            fill = broker.execute(signal, price=pm_tick.price)
            store.add_fill(fill)
            equity = broker.mark_to_market(last_price=pm_tick.price)
            print(f'[{step}] {signal.side.upper()} {signal.qty} {signal.instrument} @ {pm_tick.price:.2f} | {signal.reason} | equity={equity:.2f}')
        else:
            print(f'[{step}] HOLD {settings.symbol} | cb={cb_tick.price:.2f} pm={pm_tick.price:.2f}')

        if step < iterations - 1:
            time.sleep(sleep_seconds)

    print('summary:', store.summary())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Polymarket MVP bot runner')
    parser.add_argument('--iterations', type=int, default=5, help='Number of ingest/decision cycles')
    parser.add_argument('--sleep-seconds', type=float, default=1.0, help='Delay between cycles')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run_loop(iterations=args.iterations, sleep_seconds=args.sleep_seconds)
