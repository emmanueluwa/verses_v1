import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.verse import Verse
from schemas.verse import QueryRequest, VersesHistory

from core.verse_generator import VerseGenerator
from core.verses import Verses
from core.models import VerseLLMResponse

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
        result = VerseGenerator.query_verse(
            db=db, session_id=session_id, query=request.query
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")


@router.get("/query_responses", response_model=List[VersesHistory])
async def get_responses(
    response: Response,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db),
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    verses = Verses.get_verses(db=db, session_id=session_id)
    if not verses:
        raise HTTPException(
            status_code=404,
            detail=f"no verses found found",
        )

    return verses


@router.get("/query_response/{query_response_id}", response_model=VersesHistory)
async def get_response(
    response: Response,
    query_response_id: int,
    session_id: str = Depends(get_session_id),
    db: Session = Depends(get_db),
):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    verse = Verses.get_verse(
        db=db, session_id=session_id, query_response_id=query_response_id
    )
    if not verse:
        raise HTTPException(
            status_code=404,
            detail=f"query response with id: {query_response_id} not found",
        )

    return verse
