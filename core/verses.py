from sqlalchemy.orm import Session

from core.models import VerseHistory
from models.verse import QueryLog


class Verses:

    @classmethod
    def get_verses(cls, db: Session, session_id: str) -> VerseHistory:
        # get all verses from db
        verses = db.query(QueryLog).all()

        return verses
