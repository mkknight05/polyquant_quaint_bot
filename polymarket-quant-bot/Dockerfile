FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps kept minimal; add build-essential only if future deps need compilation
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Ensure persistent dirs exist
RUN mkdir -p /app/data /app/logs

# Healthcheck assumes app emits an alive marker file (optional).
# You can replace this with an HTTP endpoint check later.
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD test -f /app/data/bot.db || exit 1

CMD ["python", "run.py"]
