#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[Stage 1] Unit tests"
python -m unittest discover -s tests -v

echo "[Stage 2] Compile sanity"
python -m compileall bot run.py

echo "[Stage 3] Synthetic smoke run"
POLYMARKET_USE_SYNTHETIC=true python run.py --iterations 3 --sleep-seconds 0

if [[ -n "${POLYMARKET_TOKEN_ID:-}" && -n "${POLYMARKET_PRIVATE_KEY:-}" ]]; then
  echo "[Stage 4] Live Polymarket read-only smoke run"
  POLYMARKET_USE_SYNTHETIC=false python run.py --iterations 2 --sleep-seconds 0
else
  echo "[Stage 4] Skipped (set POLYMARKET_TOKEN_ID and POLYMARKET_PRIVATE_KEY to enable live check)"
fi
