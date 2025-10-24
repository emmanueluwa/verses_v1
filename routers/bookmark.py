import uuid
from typing import Optional, List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Cookie,
    Response,
    status,
    BackgroundTasks,
)
from sqlalchemy.orm import Session

from db.database import get_db, SessionLocal
from models.verse import QueryLog, Verse
from schemas.verse import Bookmark, VersesHistory
from core.verse_generator import VerseGenerator
from core.models import VerseLLMResponse

router = APIRouter(prefix="/bookmark", tags=["bookmark"])


def get_session_id(session_id: Optional[str] = Cookie(None)):
    if not session_id:
        session_id = str(uuid.uuid4())

    return session_id


@router.post("/", status_code=status.HTTP_201_CREATED)
def bookmark(
    bookmark: Bookmark,
    db: Session = Depends(get_db),
    session_id=Depends(get_session_id),
):
    query_response = (
        db.query(QueryLog).filter(QueryLog.id == bookmark.query_log_id).first()
    )
    print(f"verse from bookmark router: {query_response}")
    if not query_response:
        raise HTTPException(
            status_code=404,
            detail=f"query response with id: {bookmark.query_log_id} does not exist",
        )

    bookmark_query = db.query(Verse).filter(
        Verse.query_log_id == bookmark.query_log_id, Verse.session_id == session_id
    )
    bookmarked_verse = bookmark_query.first()

    if bookmark.dir == 1:
        if bookmarked_verse:
            raise HTTPException(status_code=409, detail="verse already bookmarked")

        new_bookmark = Verse(query_log_id=bookmark.query_log_id, session_id=session_id)

        db.add(new_bookmark)
        db.commit()

        return {"message": "successfully added bookmark"}
    else:
        if not bookmarked_verse:
            raise HTTPException(status_code=404, detail="bookmark does not exist")

        bookmark_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "successfully deleted bookmark"}


@router.get(
    "/saved",
    status_code=status.HTTP_200_OK,
)
def bookmark(
    db: Session = Depends(get_db),
    session_id=Depends(get_session_id),
):
    bookmarked_responses = db.query(Verse).filter(Verse.session_id == session_id).all()
    if not bookmarked_responses:
        raise HTTPException(
            status_code=404,
            detail=f"bookmarked verses for id: {session_id} do not exist",
        )

    return bookmarked_responses
