"""
frontend sends jobs
backend performs job

frontend ask if job is done
backend reports status of job

if job is done, backend sends story
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from db.database import Base


class VerseJob(Base):
    __tablename__ = "verse_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, unique=True)
    session_id = Column(String, index=True)
    theme = Column(String)
    status = Column(String)
    verse_id = Column(Integer, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_job = Column(DateTime(timezone=True), nullable=True)
