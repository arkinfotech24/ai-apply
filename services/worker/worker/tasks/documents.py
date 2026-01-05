from worker.celery_app import celery_app

@celery_app.task(name="documents.generate")
def generate_documents(job_id: str, doc_type: str) -> dict:
    # TODO: call OpenAI to generate doc; persist and write artifact file
    return {"job_id": job_id, "doc_type": doc_type, "status": "queued_stub"}
