import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.run import Run
from app.models.job import Job
from ai_apply_schemas.run import RunCreateRequest

router = APIRouter()

@router.post("")
def create_run(payload: RunCreateRequest, user_id: str = "00000000-0000-0000-0000-000000000000", db: Session = Depends(get_db)):
    job = db.get(Job, uuid.UUID(payload.job_id))
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    run = Run(
        user_id=uuid.UUID(user_id),
        job_id=job.id,
        status="CREATED",
        mode=payload.mode,
        apply_url=job.apply_url,
        platform_hint=None,
        payload_json=None,
        result_json=None,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return {"run_id": str(run.id), "status": run.status}

@router.get("/{run_id}")
def get_run(run_id: str, db: Session = Depends(get_db)):
    run = db.get(Run, uuid.UUID(run_id))
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {
        "run_id": str(run.id),
        "status": run.status,
        "mode": run.mode,
        "apply_url": run.apply_url,
        "platform_hint": run.platform_hint,
        "assigned_agent_id": run.assigned_agent_id,
        "result_json": run.result_json,
        "created_at": run.created_at,
        "updated_at": run.updated_at,
    }
