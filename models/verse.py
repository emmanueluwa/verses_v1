# reference (Surah:Ayah)
# text
# explanation
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class Verse(Base):
    """Tack verses users save/bookmark"""

    __tablename__ = "verses"

    session_id = Column(String, index=True)
    query_log_id = Column(
        Integer, ForeignKey("query_logs.id", ondelete="CASCADE"), primary_key=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class QueryLog(Base):
    """Track what users are asking"""

    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_query = Column(String, index=True)
    answer_summary = Column(Text)
    themes = Column(String)
    verses_returned = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
