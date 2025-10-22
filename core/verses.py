from sqlalchemy.orm import Session

from schemas.verse import VersesHistory
from models.verse import QueryLog


class Verses:

    @classmethod
    def get_verses(cls, db: Session, session_id: str) -> VersesHistory:
        # get all verses from db
        verses = (
            db.query(QueryLog)
            .filter(QueryLog.session_id == session_id)
            .order_by(QueryLog.created_at.desc())
            .all()
        )

        return verses

    @classmethod
    def get_verse(
        cls, db: Session, session_id: str, query_response_id: int
    ) -> VersesHistory:
        # get all verses from db
        verse = (
            db.query(QueryLog)
            .filter(QueryLog.id == query_response_id)
            .filter(QueryLog.session_id == session_id)
            .order_by(QueryLog.created_at.desc())
            .first()
        )

        print(f"verse from verses.py get_verse(): {verse}")

        return verse
