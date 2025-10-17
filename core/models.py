from typing import List, Optional
from pydantic import BaseModel, Field


class VerseReference(BaseModel):
    surah_number: int = Field(description="Surah number (1-114)")
    surah_name: str = Field(description="Name of Surah")
    verse_number: int = Field(description="Verse number within the Surah")
    arabic_text: str = Field(description="Arabic text of the verse")
    translation: str = Field(description="English translation of the verse")


class TafsirExplanation(BaseModel):
    content: str = Field(description="Tafsir explanation from Ibn Kathir")
    relevance_score: Optional[float] = Field(
        default=None, description="How relevant this tafsir is to the query"
    )


class VerseReccommendation(BaseModel):
    verse: VerseReference = Field(description="The recommended Quranic verse")
    tafsir: TafsirExplanation = Field(description="Tafsir explanation for the verse")
    why_recommended: str = Field(
        description="Explanation of why this verse answers the user's question"
    )


class VerseLLMResponse(BaseModel):
    query: str = Field(description="The users's original question")
    answer_summary: str = Field(description="Brief summary answer to the query")
    recommendations: List[VerseReccommendation] = Field(
        description="List of recommended verses with tafsir"
    )
    themes_identified: List[str] = Field(
        description="Islamic themes identified from the query"
    )
