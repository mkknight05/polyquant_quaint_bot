from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from bot.models import Signal


class SignalQueue:
    def __init__(self, queue_path: str) -> None:
        self.path = Path(queue_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.touch(exist_ok=True)

    def enqueue(self, signal: Signal) -> None:
        with self.path.open('a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(signal)) + '\n')

    def drain(self) -> list[Signal]:
        with self.path.open('r+', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
            f.seek(0)
            f.truncate()
        out: list[Signal] = []
        for line in lines:
            payload = json.loads(line)
            out.append(
                Signal(
                    instrument=payload['instrument'],
                    side=payload['side'],
                    qty=float(payload['qty']),
                    reason=payload.get('reason', ''),
                )
            )
        return out


class BrokerState:
    def __init__(self, state_path: str, starting_cash: float) -> None:
        self.path = Path(state_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.starting_cash = starting_cash

    def load(self) -> tuple[float, float]:
        if not self.path.exists():
            return self.starting_cash, 0.0
        payload = json.loads(self.path.read_text(encoding='utf-8'))
        return float(payload.get('cash', self.starting_cash)), float(payload.get('position', 0.0))

    def save(self, cash: float, position: float) -> None:
        payload = {'cash': cash, 'position': position}
        self.path.write_text(json.dumps(payload), encoding='utf-8')
