# polymarket-quant-bot MVP

This directory now contains a **7-day MVP skeleton** for a prediction-market trading system.

## What is implemented now

- Coinbase market-data ingestion (public ticker endpoint).
- Polymarket adapter with real CLOB client wiring and optional synthetic fallback.
- Unified tick + paper-fill persistence in SQLite.
- Simple spread strategy.
- Paper execution engine and mark-to-market equity output.
- Service-oriented entrypoints that replace multi-agent orchestration:
  - `services/ingest_service.py`
  - `services/strategy_service.py`
  - `services/execution_service.py`
- Exchange integration framework:
  - `bot/exchange_adapters/base.py`
  - `bot/exchange_adapters/gemini.py`
  - `bot/exchange_adapters/_template.py`

## Quick start

```bash
cd /workspace/simple-website/polymarket-quant-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp -n .env.example .env
python run.py --iterations 5 --sleep-seconds 1
```

## Environment variables used by MVP

```bash
SQLITE_PATH=data/mvp.db
SYMBOL=BTC-USD
TRADE_QTY=0.01
SPREAD_THRESHOLD=0.01
STARTING_CASH=10000
POLYMARKET_USE_SYNTHETIC=true
POLYMARKET_HOST=https://clob.polymarket.com
POLYMARKET_CHAIN_ID=137
POLYMARKET_TOKEN_ID=
POLYMARKET_PRIVATE_KEY=
POLYMARKET_API_KEY=
POLYMARKET_API_SECRET=
POLYMARKET_API_PASSPHRASE=
SIGNAL_QUEUE_PATH=data/signals.jsonl
BROKER_STATE_PATH=data/broker_state.json
```

## Current limitations

- Set `POLYMARKET_USE_SYNTHETIC=false` plus `POLYMARKET_TOKEN_ID` and `POLYMARKET_PRIVATE_KEY` to use live last-trade prices.
- This version reads live prices but still does not place live orders.
- This version is paper-only and intentionally minimal.

## Exchange integration framework

Use the adapter framework to add new exchanges quickly:

```bash
cp bot/exchange_adapters/_template.py bot/exchange_adapters/kraken.py
```

Then implement `connect`, `fetch_price`, and `place_order`.

Reference docs:
- `EXCHANGE_INTEGRATION.md`
- `EXCHANGE_INTEGRATION_CHECKLIST.md`

## Service-mode flow (replaces agent concept)

The project now supports a deterministic 3-service flow:

1. **Ingest service** collects ticks from Coinbase + Polymarket and writes to SQLite.
2. **Strategy service** reads latest ticks and queues signal intents.
3. **Execution service** drains queued signals and paper-executes fills.

Run locally in order:

```bash
python services/ingest_service.py --iterations 3 --sleep-seconds 0
python services/strategy_service.py --iterations 1 --sleep-seconds 0
python services/execution_service.py --iterations 1 --sleep-seconds 0
```

## Staged test plan (recommended validation flow)

Run validation in four stages so we can isolate failures quickly:

1. **Stage 1: fast unit checks (no network)**
   - `python -m unittest discover -s tests -v`
2. **Stage 2: compile/import sanity**
   - `python -m compileall bot run.py`
3. **Stage 3: synthetic integration smoke (deterministic dev path)**
   - `POLYMARKET_USE_SYNTHETIC=true python run.py --iterations 3 --sleep-seconds 0`
4. **Stage 4: optional live Polymarket read-only check**
   - Set: `POLYMARKET_USE_SYNTHETIC=false`, `POLYMARKET_TOKEN_ID`, `POLYMARKET_PRIVATE_KEY`
   - Run: `python run.py --iterations 2 --sleep-seconds 0`

You can run stages 1–3 (and conditionally stage 4) with:

```bash
bash scripts/staged_test_plan.sh
```
