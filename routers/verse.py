import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.verse import Verse
from schemas.verse import VerseLLMResponse, BookmarkRequest, QueryRequest
from services.verse_service import get_verse_recommendation, get_verse_by_reference

router = APIRouter(prefix="/verses", tags=["verses"])


def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())

    return session_id


@router.post("/query", response_model=VerseLLMResponse)
async def query_verses(
    request: QueryRequest,
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db),
):
    # identifying users based on web browser instance instead of auth
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    try:
        result = await get_verse_recommendations(request.question, request.max_results)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.post("/bookmarks/save")
async def save_bookmark(
    request: BookmarkRequest,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db),
):
    existing = db.query(Verse).filter(
        Verse.session_id == session_id,
        Verse.verse_reference == request.verse_reference,
    )
    if existing:
        raise HTTPException(status_Code=400, detail="Verse already bookmarked")

    verse_data = get_verse_by_reference(request.verse_reference)
