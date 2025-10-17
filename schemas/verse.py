"""
specifying type of data api should accept and return
- fast api(pydantic) will auto validate data
"""

from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=3, description="User's question")
    max_results: Optional[int] = Field(
        Default=3, description="Number of verse recommendations"
    )


class BookmarkRequest(BaseModel):
    verse_reference: str


class VerseReference(BaseModel):
    surah_number: int
    surah_name: str
    verse_number: int
    arabic_text: str
    translation: str
    recitation_url: Optional[str] = None

    class Config:
        from_attributes = True


class TafsirExplanation(BaseModel):
    """Tafsir explanation from Ibn Kathir"""

    content: str
    source: str = "Tafsir Ibn Kathir"


class VerseRecommendation(BaseModel):
    verse: VerseReference
    tafsir: TafsirExplanation
    why_recommended: str = Field(description="Why this verse answers the question")


class VerseLLMResponse(BaseModel):
    query: str
    answer_summary: str
    recommendations: List[VerseRecommendation]
    themes_identitfied: List[str]
    timestamp: datetime


class SavedVerse(BaseModel):
    id: int
    verse_reference: set
    surah_name: str
    verse_number: int
    arabic_text: str
    translation: str
    saved_at: datetime

    class Config:
        from_attributes = True


class BookmarkListResponse(BaseModel):
    bookmarks: List[SavedVerse]
