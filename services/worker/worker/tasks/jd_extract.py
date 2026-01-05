from worker.celery_app import celery_app

@celery_app.task(name="jd_extract.run")
def extract_job_description(job_id: str) -> dict:
    # TODO: fetch job description from DB, call OpenAI structured extract, store result
    return {"job_id": job_id, "status": "queued_stub"}
