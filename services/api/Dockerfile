FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv==0.5.16

COPY pyproject.toml ./
# Optional: COPY uv.lock ./

# Install dependencies (editable)
RUN uv pip install --system -e .

# Shared schemas (editable mount in compose is recommended; copy for container build robustness)
COPY ../../packages/schemas /packages/schemas
RUN uv pip install --system -e /packages/schemas

COPY . /app

EXPOSE 8000
