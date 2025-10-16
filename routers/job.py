import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Cookie
from sqlalchemy.orm import Session

from db.database import get_db
from models.job import VerseJob
from schemas.job import VerseJobResponse


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}", response_model=VerseJobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):

    job = db.query(VerseJob).filter(VerseJob.job_id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return job
