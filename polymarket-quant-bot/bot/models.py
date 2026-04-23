from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(slots=True)
class MarketTick:
    source: str
    instrument: str
    price: float
    ts: datetime

    @classmethod
    def now(cls, source: str, instrument: str, price: float) -> "MarketTick":
        return cls(source=source, instrument=instrument, price=price, ts=datetime.now(timezone.utc))


@dataclass(slots=True)
class Signal:
    instrument: str
    side: str
    qty: float
    reason: str


@dataclass(slots=True)
class PaperFill:
    instrument: str
    side: str
    qty: float
    price: float
    ts: datetime
