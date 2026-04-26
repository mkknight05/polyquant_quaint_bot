from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import os


@dataclass(frozen=True)
class StrategySignal:
    strategy: str
    market: str
    action: str
    confidence: float
    rationale: str
    timestamp_utc: str

    def to_text(self) -> str:
        return (
            "[SIGNAL] "
            f"strategy={self.strategy} "
            f"market={self.market} "
            f"action={self.action} "
            f"confidence={self.confidence:.2f} "
            f"time={self.timestamp_utc}\n"
            f"rationale={self.rationale}"
        )


def generate_read_only_signal() -> StrategySignal:
    """Generate a deterministic starter signal for shadow-mode validation.

    This function intentionally avoids order placement and external side effects.
    """
    strategy = os.getenv("SIGNAL_STRATEGY_NAME", "mean_reversion_stub").strip() or "mean_reversion_stub"
    market = os.getenv("SIGNAL_DEFAULT_MARKET", "POLYMARKET:DEMO").strip() or "POLYMARKET:DEMO"

    return StrategySignal(
        strategy=strategy,
        market=market,
        action="observe",
        confidence=0.51,
        rationale="Bootstrap read-only signal for Telegram shadow-mode validation.",
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
    )
