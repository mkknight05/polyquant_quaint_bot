from __future__ import annotations

import argparse
import time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from bot.config import settings
from bot.service_io import SignalQueue
from bot.storage import Store
from bot.strategy import SpreadStrategy


def run_strategy(iterations: int, sleep_seconds: float) -> None:
    store = Store(settings.sqlite_path)
    queue = SignalQueue(settings.signal_queue_path)
    strategy = SpreadStrategy(threshold=settings.spread_threshold, qty=settings.trade_qty)

    for step in range(iterations):
        cb = store.latest_price('coinbase', settings.symbol)
        pm = store.latest_price('polymarket', settings.symbol)
        if cb is None or pm is None:
            print(f'[strategy:{step}] waiting for data')
        else:
            signal = strategy.generate(settings.symbol, price_a=cb, price_b=pm)
            if signal is None:
                print(f'[strategy:{step}] HOLD cb={cb:.2f} pm={pm:.2f}')
            else:
                queue.enqueue(signal)
                print(f'[strategy:{step}] queued {signal.side} {signal.qty} ({signal.reason})')
        if step < iterations - 1:
            time.sleep(sleep_seconds)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Strategy service that emits execution intents')
    parser.add_argument('--iterations', type=int, default=5)
    parser.add_argument('--sleep-seconds', type=float, default=1.0)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run_strategy(iterations=args.iterations, sleep_seconds=args.sleep_seconds)
