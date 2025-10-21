from sqlalchemy.orm import Session

from core.models import VerseHistory
from models.verse import QueryLog


class Verses:

    @classmethod
    def get_verses(cls, db: Session, session_id: str) -> VerseHistory:
        # get all verses from db
        verses = (
            db.query(QueryLog)
            .filter(QueryLog.session_id == session_id)
            .order_by(QueryLog.created_at.desc())
            .all()
        )

        return verses
