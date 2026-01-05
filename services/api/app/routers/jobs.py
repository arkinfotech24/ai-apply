import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.job import Job
from ai_apply_schemas.job import JobImportRequest

router = APIRouter()

@router.post("/import")
def import_job(payload: JobImportRequest, user_id: str = "00000000-0000-0000-0000-000000000000", db: Session = Depends(get_db)):
    # NOTE: MVP uses a placeholder user_id; replace with real auth later.
    job = Job(
        user_id=uuid.UUID(user_id),
        apply_url=payload.url,
        description_raw=payload.pasted_description,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # TODO: enqueue Celery task jd_extract.run(job_id)
    return {"job_id": str(job.id), "message": "imported"}
