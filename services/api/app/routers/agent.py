import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.run import Run, RunEvent, RunArtifact
from ai_apply_schemas.run import (
    AgentRegisterRequest, AgentHeartbeatRequest, AgentPollResponse,
    RunPayload, RunCompleteRequest, RunEventIn, ArtifactRef
)

router = APIRouter()

# In MVP we store agents in-memory; production should persist in DB.
AGENTS: dict[str, dict] = {}

@router.post("/register")
def register_agent(payload: AgentRegisterRequest):
    AGENTS[payload.agent_id] = payload.model_dump()
    return {"status": "registered", "agent": payload.model_dump()}

@router.post("/heartbeat")
def heartbeat(payload: AgentHeartbeatRequest):
    agent = AGENTS.get(payload.agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not registered")
    agent["last_seen"] = datetime.now(timezone.utc).isoformat()
    return {"status": "ok"}

@router.post("/poll", response_model=AgentPollResponse)
def poll(agent_id: str, db: Session = Depends(get_db)):
    agent = AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not registered")

    # Find next run not assigned; simplistic FIFO by created_at.
    run = (
        db.query(Run)
        .filter(Run.status == "CREATED")
        .order_by(Run.created_at.asc())
        .first()
    )
    if not run:
        return AgentPollResponse(run=None)

    run.status = "ASSIGNED"
    run.assigned_agent_id = agent_id
    db.add(run)
    db.commit()
    db.refresh(run)

    payload = RunPayload(
        run_id=str(run.id),
        user_id=str(run.user_id),
        apply_url=run.apply_url or "",
        platform_hint=run.platform_hint,
        mode=run.mode,
        field_payload=(run.payload_json or {}).get("field_payload", {}) if run.payload_json else {},
        answers=(run.payload_json or {}).get("answers", {}) if run.payload_json else {},
        documents=[
            ArtifactRef(**d) for d in (run.payload_json or {}).get("documents", [])
        ] if run.payload_json else [],
    )
    return AgentPollResponse(run=payload)

@router.post("/runs/{run_id}/events")
def ingest_events(run_id: str, events: list[RunEventIn], db: Session = Depends(get_db)):
    run = db.get(Run, uuid.UUID(run_id))
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    for e in events:
        ts = datetime.fromisoformat(e.ts.replace("Z", "+00:00"))
        db.add(RunEvent(
            run_id=run.id,
            ts=ts,
            event_type=e.event_type,
            step_id=e.step_id,
            message=e.message,
            data=e.data,
        ))
    db.commit()
    return {"status": "ok", "count": len(events)}

@router.post("/runs/{run_id}/complete")
def complete_run(run_id: str, payload: RunCompleteRequest, db: Session = Depends(get_db)):
    run = db.get(Run, uuid.UUID(run_id))
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    # Save events in payload (optional)
    if payload.events:
        for e in payload.events:
            ts = datetime.fromisoformat(e.ts.replace("Z", "+00:00"))
            db.add(RunEvent(
                run_id=run.id,
                ts=ts,
                event_type=e.event_type,
                step_id=e.step_id,
                message=e.message,
                data=e.data,
            ))

    # Save artifacts references
    for a in payload.artifacts:
        db.add(RunArtifact(
            run_id=run.id,
            kind=a.kind,
            path=a.path,
            content_type=a.content_type,
        ))

    run.status = payload.status.value
    run.result_json = {
        "receipt": payload.receipt.model_dump() if payload.receipt else None,
        "errors": payload.errors,
    }
    db.add(run)
    db.commit()
    db.refresh(run)

    return {"status": run.status, "run_id": str(run.id)}
