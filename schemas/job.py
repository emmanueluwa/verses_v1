from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class VerseJobBase(BaseModel):
    theme: str


class VerseJobResponse(BaseModel):
    job_id: int
    status: str
    created_at: datetime
    verse_id: Optional[int] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    class Config:
        from_attributes = True


class VerseJobCreate(VerseJobBase):
    pass
