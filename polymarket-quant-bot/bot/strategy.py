from __future__ import annotations

from bot.models import Signal


class SpreadStrategy:
    def __init__(self, threshold: float, qty: float) -> None:
        self.threshold = threshold
        self.qty = qty

    def generate(self, instrument: str, price_a: float, price_b: float) -> Signal | None:
        spread = (price_b - price_a) / price_a
        if spread >= self.threshold:
            return Signal(instrument=instrument, side='buy', qty=self.qty, reason=f'spread={spread:.4f} >= {self.threshold}')
        if spread <= -self.threshold:
            return Signal(instrument=instrument, side='sell', qty=self.qty, reason=f'spread={spread:.4f} <= -{self.threshold}')
        return None
