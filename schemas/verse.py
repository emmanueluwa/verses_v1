"""
specifying type of data api should accept and return
- fast api(pydantic) will auto validate data
"""

from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel


class VerseThemeSchema(BaseModel):
    text: str
    node_id: Optional[int] = None


class VerseNodeBase(BaseModel):
    content: str
    reference: str


class CompleteVerseNodeResponse(VerseNodeBase):
    id: int
    theme: List[VerseThemeSchema] = []

    class Config:
        from_attributes = True


class VerseBase(BaseModel):
    reference: str
    session_id: Optional[str] = None

    class Config:
        from_attributes = True


class CreateVerseRequest(BaseModel):
    theme: str


class CompleteVerseResponse(VerseBase):
    id: int
    created_at: datetime
    root_node: CompleteVerseNodeResponse
    all_nodes: Dict[int, CompleteVerseNodeResponse]

    class Config:
        from_attributes = True
