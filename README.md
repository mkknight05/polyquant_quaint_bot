# Polymarket Quant Bot Workspace

This repository contains the infrastructure/bootstrap folder at:

- `polymarket-quant-bot/`

Inside that folder, use `.env.example` + `run.py` to validate API readiness for Coinbase, OKX, Polymarket, Kalshi, Gemini, and Telegram before enabling any live trading code.

See:

- `polymarket-quant-bot/README.md`

- `polymarket-quant-bot/STRATEGY_GUIDE.md` (websites/apps + predefined strategy templates + bot comparison rubric)


## Where Docker is used

- Docker config is in `polymarket-quant-bot/Dockerfile` and `polymarket-quant-bot/docker-compose.yml`.
- The containerized program is the Python bootstrap runner: `python run.py` (inside the `bot` service).
- Start it from repo root with: `docker compose -f polymarket-quant-bot/docker-compose.yml up --build`.


### Quick start from repository root

```bash
cp polymarket-quant-bot/.env.example polymarket-quant-bot/.env
docker compose -f polymarket-quant-bot/docker-compose.yml up --build --abort-on-container-exit bot
# in another terminal: docker compose -f polymarket-quant-bot/docker-compose.yml logs -f bot
```
