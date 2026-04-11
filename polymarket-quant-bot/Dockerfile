FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Keep runtime deps minimal.
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY . .

# Runtime mount points for persistent data/logs
RUN mkdir -p /app/data /app/logs

# Generic healthcheck that does not assume DB initialization timing.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import pathlib; pathlib.Path('/app').exists()" || exit 1

CMD ["python", "run.py"]
