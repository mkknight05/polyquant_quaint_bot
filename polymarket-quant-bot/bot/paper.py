from __future__ import annotations

from datetime import datetime, timezone

from bot.models import PaperFill, Signal


class PaperBroker:
    def __init__(self, starting_cash: float) -> None:
        self.cash = starting_cash
        self.position = 0.0

    def execute(self, signal: Signal, price: float) -> PaperFill:
        notional = signal.qty * price
        if signal.side == 'buy':
            self.cash -= notional
            self.position += signal.qty
        elif signal.side == 'sell':
            self.cash += notional
            self.position -= signal.qty
        else:
            raise ValueError(f'unsupported side: {signal.side}')
        return PaperFill(
            instrument=signal.instrument,
            side=signal.side,
            qty=signal.qty,
            price=price,
            ts=datetime.now(timezone.utc),
        )

    def mark_to_market(self, last_price: float) -> float:
        return self.cash + self.position * last_price
