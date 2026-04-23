# Copilot workspace instructions for `simple-website/polymarket-quant-bot`

## Project purpose
This project is a lightweight MVP for a prediction/crypto quant bot focused on:
- ingesting market data,
- generating strategy signals,
- simulating execution in paper mode,
- and storing tick/fill history for backtesting and diagnostics.

## Architecture conventions
Prefer deterministic, modular services over opaque "agents":
1. `services/ingest_service.py` collects market data and writes ticks.
2. `services/strategy_service.py` reads ticks and emits signal intents.
3. `services/execution_service.py` consumes intents and writes paper fills.

Shared modules live in `polymarket-quant-bot/bot/`.

## Development style
- Python 3.10+.
- Keep logic config-driven via environment variables in `bot/config.py`.
- Avoid embedding secrets in code or committed files.
- Keep external API access behind adapters.
- Write tests for new behavior in `polymarket-quant-bot/tests/`.

## Run/test workflow
From `polymarket-quant-bot/`:
- Full staged validation: `bash scripts/staged_test_plan.sh`
- Unit tests only: `python -m unittest discover -s tests -v`

Service-oriented local smoke sequence:
1. `python services/ingest_service.py --iterations 3 --sleep-seconds 0`
2. `python services/strategy_service.py --iterations 1 --sleep-seconds 0`
3. `python services/execution_service.py --iterations 1 --sleep-seconds 0`

## Implementation guardrails
- Do not break existing `run.py`; it remains the all-in-one fast loop.
- New features should be added to both module docs and `.env.example` if configurable.
- Keep synthetic fallback paths available for non-network environments.

## Exchange integration conventions
- Adapter framework lives in `polymarket-quant-bot/bot/exchange_adapters/`.
- Base abstractions are in `base.py`; new connectors should start from `_template.py`.
- Keep adapters async and rate-limited via `RateLimiter`.
- Add tests under `polymarket-quant-bot/tests/` (see `test_gemini_adapter.py`).
