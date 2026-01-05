FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl gcc \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv==0.5.16

# Copy only API project files (context is services/api)
COPY pyproject.toml /app/pyproject.toml
RUN uv pip install --system -e /app

# Copy source
COPY . /app

EXPOSE 8000

