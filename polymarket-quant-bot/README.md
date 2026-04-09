# polymarket-quant-bot (bootstrap)

This repo currently contains container/runtime scaffolding for the bot.

## First steps (macOS Bash 3.2 compatible)

These commands work in macOS Terminal when the prompt shows `bash-3.2$`.

```bash
cd /workspace/simple-website/polymarket-quant-bot
cp -n .env.example .env 2>/dev/null || touch .env
nano .env
```

After editing `.env`, save in nano with:
- `Ctrl + O`, then Enter
- `Ctrl + X`

### Required secret hygiene

```bash
echo ".env" >> .gitignore
echo "*.pem" >> .gitignore
chmod 600 /absolute/path/to/kalshi_private_key.pem
```

## Docker usage

```bash
docker compose up --build -d
```

View logs:

```bash
docker compose logs -f bot
```

Stop:

```bash
docker compose down
```

## Notes

- `docker-compose.yml` waits for Redis to pass health checks before booting the bot.
- Health check is intentionally generic so startup does not fail if the DB has not been created yet.
