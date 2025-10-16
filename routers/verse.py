import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.verse import Verse, VerseNode
from models.job import VerseJob
from schemas.verse import (
    CompleteVerseResponse,
    CompleteVerseNodeResponse,
    CreateVerseRequest,
)
from schemas.job import VerseJobResponse

router = APIRouter(prefix="/verses", tags=["verses"])


def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())

    return session_id


@router.post("/create", response_model=VerseJobResponse)
def create_story(
    request: CreateVerseRequest,
    background_tasks: BackgroundTasks,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db),
):
    # identifying users based on web browser instance instead of auth
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    # job triggers background task to call llm
    job_id = str(uuid.uuid4())

    job = VerseJob(
        job_id=job_id, session_id=session_id, theme=request.theme, status="pending"
    )

    db.add(job)
    db.commit()

    # add background taks. generate verse
    background_tasks.add_task(
        generate_verse_task, job_id=job_id, theme=request.theme, session_id=session_id
    )

    return job


def generate_verse_task(job_id: str, theme: str, session_id: str):
    # new db instance, seperate session started to avoid hanging -> threading and async operations
    db = SessionLocal()

    try:
        job = db.query(VerseJob).filter(VerseJob.job_id == job_id).first()

        if not job:
            return

        try:
            job.status = "processing"
            db.commit()

            verse = {}  # TODO: generate story

            job.verse_id = 1  # TODO: update story id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()

        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()

    finally:
        db.close()
