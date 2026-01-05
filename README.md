# AI Apply

Local-first AI job application assistant:
- FastAPI API (orchestrator)
- Celery worker (async tasks)
- Postgres + Redis (docker-compose)
- Shared schemas package
- Agent control-plane endpoints (for a local Playwright agent)

## Quickstart (local dev)

1) Create env file
```bash
cp .env.example .env
# set OPENAI_API_KEY
```

2) Start stack
```bash
docker compose up -d --build
```

3) Verify API health
- http://localhost:8000/health

## Notes
- Alembic migrations run on API container start (local dev).
- Generated artifacts are stored in a shared docker volume at `/data/artifacts`.
