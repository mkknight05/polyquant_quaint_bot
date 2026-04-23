from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import DateTime, Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from bot.models import MarketTick, PaperFill


class Base(DeclarativeBase):
    pass


class TickRow(Base):
    __tablename__ = 'ticks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(40), index=True)
    instrument: Mapped[str] = mapped_column(String(40), index=True)
    price: Mapped[float] = mapped_column(Float)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class FillRow(Base):
    __tablename__ = 'paper_fills'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    instrument: Mapped[str] = mapped_column(String(40), index=True)
    side: Mapped[str] = mapped_column(String(8))
    qty: Mapped[float] = mapped_column(Float)
    price: Mapped[float] = mapped_column(Float)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class Store:
    def __init__(self, sqlite_path: str) -> None:
        Path(sqlite_path).parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f'sqlite:///{sqlite_path}', future=True)
        Base.metadata.create_all(self.engine)

    def add_tick(self, tick: MarketTick) -> None:
        with Session(self.engine) as session:
            session.add(TickRow(source=tick.source, instrument=tick.instrument, price=tick.price, ts=tick.ts))
            session.commit()

    def add_fill(self, fill: PaperFill) -> None:
        with Session(self.engine) as session:
            session.add(
                FillRow(
                    instrument=fill.instrument,
                    side=fill.side,
                    qty=fill.qty,
                    price=fill.price,
                    ts=fill.ts,
                )
            )
            session.commit()

    def latest_price(self, source: str, instrument: str) -> float | None:
        with Session(self.engine) as session:
            row = (
                session.query(TickRow)
                .filter(TickRow.source == source, TickRow.instrument == instrument)
                .order_by(TickRow.ts.desc())
                .first()
            )
            return None if row is None else row.price

    def summary(self) -> dict[str, float]:
        with Session(self.engine) as session:
            tick_count = session.query(TickRow).count()
            fill_count = session.query(FillRow).count()
        return {'ticks': float(tick_count), 'fills': float(fill_count), 'ts': datetime.now(timezone.utc).timestamp()}
