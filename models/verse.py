# reference (Surah:Ayah)
# text
# explanation
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from db.database import Base


class Verse:
    __tablename__ = "verses"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, index=True)

    session_id = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    nodes = relationship("VerseNode", back_populates="verse")


class VerseNode:
    __tablename__ = "verse_nodes"

    id = Column(Integer, primary_key=True, index=True)
    verse_id = Column(Integer, ForeignKey("verses.id"), index=True)

    text = Column(String, index=True)
    explanation = Column(String, index=True)
    related_verses = Column(JSON, default=list)

    verse = relationship("Verse", back_populates="nodes")
