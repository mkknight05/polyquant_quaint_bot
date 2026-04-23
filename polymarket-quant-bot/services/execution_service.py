from __future__ import annotations

import argparse
import time
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

from bot.config import settings
from bot.paper import PaperBroker
from bot.service_io import BrokerState, SignalQueue
from bot.storage import Store


def run_execution(iterations: int, sleep_seconds: float) -> None:
    store = Store(settings.sqlite_path)
    queue = SignalQueue(settings.signal_queue_path)
    state = BrokerState(settings.broker_state_path, starting_cash=settings.starting_cash)

    cash, position = state.load()
    broker = PaperBroker(starting_cash=cash)
    broker.position = position

    for step in range(iterations):
        signals = queue.drain()
        if not signals:
            print(f'[execution:{step}] no queued signals')
        for signal in signals:
            last_price = store.latest_price('polymarket', signal.instrument)
            if last_price is None:
                print(f'[execution:{step}] missing price for {signal.instrument}; skipping')
                continue
            fill = broker.execute(signal, price=last_price)
            store.add_fill(fill)
            equity = broker.mark_to_market(last_price=last_price)
            print(f'[execution:{step}] {signal.side.upper()} {signal.qty} @ {last_price:.2f} | equity={equity:.2f}')

        state.save(cash=broker.cash, position=broker.position)
        if step < iterations - 1:
            time.sleep(sleep_seconds)

    print('execution summary:', store.summary())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Execution service for queued strategy signals')
    parser.add_argument('--iterations', type=int, default=5)
    parser.add_argument('--sleep-seconds', type=float, default=1.0)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    run_execution(iterations=args.iterations, sleep_seconds=args.sleep_seconds)
