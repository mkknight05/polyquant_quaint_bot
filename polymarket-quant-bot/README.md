# polymarket-quant-bot (bootstrap + API readiness checks)

This project now includes a safe **pre-live API verification flow** for:

- OKX
- Coinbase
- Polymarket
- Telegram
- Kalshi
- Gemini

## Docker location + program name

Docker is used inside this folder:

- `Dockerfile` → defines the bot image
- `docker-compose.yml` → defines services (`bot`, `redis`)

The program that Docker runs for the bot is:

```bash
python run.py
```

(defined by `command: ["python", "run.py"]` in `docker-compose.yml`).

## 1) Add API keys (easy + repeatable)

```bash
cd /workspace/simple-website/polymarket-quant-bot
cp .env.example .env
nano .env
```

Fill in all required values, then save and exit.

### Secret hygiene

- Never commit `.env` or `*.pem`.
- Keep your Kalshi key file outside the repo and set:
  - `KALSHI_PRIVATE_KEY_PATH=/absolute/path/to/kalshi_private_key.pem`

## 2) Dry-run connectivity checks in Docker (no live trading)

```bash
docker compose up --build --abort-on-container-exit bot
```

Expected behavior:
- Container runs `python run.py`
- `run.py` executes API checks and prints PASS/FAIL lines
- Exit code `0` only when all checks pass


### Reduce waiting/lag during checks

The checker now prints progress in real time and runs checks concurrently.
If your network is slow, tune per-request timeout:

```bash
API_CHECK_TIMEOUT_SECONDS=3 python run.py
```

## 3) Move to live mode (next phase)

Live trading is intentionally blocked in this bootstrap until strategy/execution code is integrated.

To prepare for that phase:
1. keep `BOT_MODE=check` while validating infra
2. integrate trading engines
3. add authenticated order-placement smoke tests in paper/sandbox mode
4. then permit `BOT_MODE=live`

## 4) Replace GitHub repo cleanly (avoid naming/version drift)

If this folder is your canonical version, force-push it as the single source of truth:

```bash
# from repo root
cd /workspace/simple-website
git remote -v
# confirm origin is the intended GitHub repo

git add .
git commit -m "Unify scaffold and API readiness checks"
git push origin HEAD --force-with-lease
```

Use `--force-with-lease` only when you're certain old history can be replaced.

## Useful commands

```bash
# Follow bot logs
docker compose logs -f bot

# Stop all services
docker compose down
```


## 5) Strategy resources (new)

To help decision making and future benchmarking, use:

- `STRATEGY_GUIDE.md` for websites/apps, predefined strategy templates, a live-readiness scorecard, and a competitor-comparison rubric.

Use this guide in `BOT_MODE=check` and paper phases before enabling any live execution logic.
