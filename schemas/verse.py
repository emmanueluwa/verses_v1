"""
Purpose: specifying type of data api should accept and return
- fast api(pydantic) will auto validate data
"""

from typing import Annotated, List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(min_length=3, description="User's question")
    max_results: Optional[int] = Field(
        Default=3, description="Number of verse recommendations"
    )


class VersesHistory(BaseModel):
    user_query: str
    answer_summary: str
    verses_returned: str
    themes: str
    created_at: datetime
    id: int

    class Config:
        from_attributes = True


# class SavedVerse(BaseModel):
#     id: int
#     verse_reference: str
#     surah_name: str
#     verse_number: int
#     arabic_text: str
#     translation: str
#     saved_at: datetime

#     class Config:
#         from_attributes = True


# class BookmarkRequest(BaseModel):
#     verse_reference: str


# class BookmarkListResponse(BaseModel):
#     bookmarks: List[SavedVerse]


class Bookmark(BaseModel):
    query_log_id: int
    dir: Annotated[int, Field(strict=True, le=1)]
