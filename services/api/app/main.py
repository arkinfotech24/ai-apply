from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import setup_logging

from app.routers.health import router as health_router
from app.routers.jobs import router as jobs_router
from app.routers.runs import router as runs_router
from app.routers.agent import router as agent_router

setup_logging()
app = FastAPI(title=settings.app_name)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
app.include_router(runs_router, prefix="/runs", tags=["runs"])
app.include_router(agent_router, prefix="/agent", tags=["agent"])
