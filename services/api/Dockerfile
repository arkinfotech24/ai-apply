FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv==0.5.16

# Copy the full API source first (includes app/, alembic/, etc.)
COPY . /app

# Install editable after source is present
RUN uv pip install --system -e /app

EXPOSE 8000

