import os
from datetime import datetime
from sqlalchemy.orm import Session
from core.config import settings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from models.verse import QueryLog, Verse
from core.models import VerseLLMResponse, VerseReference
from retrieval import retrieval_call


class VerseGenerator:

    @classmethod
    def _get_llm(cls):
        return ChatOpenAI(
            verbose=True,
            temperature=0,
            model="gpt-4o-mini",
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

    @classmethod
    def query_verse(
        cls,
        db: Session,
        session_id: str,
        query: str,
    ) -> VerseLLMResponse:
        llm = cls._get_llm()
        raw_response = retrieval_call(query)

        verse_references = ",".join(
            [
                f"{rec.verse.surah_name}:{rec.verse.verse_number}"
                for rec in raw_response.recommendations
            ]
        )

        query_log = QueryLog(
            session_id=session_id,
            user_query=query,
            answer_summary=raw_response.answer_summary,
            verses_returned=verse_references,
            themes=",".join(raw_response.themes_identified),
        )

        db.add(query_log)
        db.commit()

        return raw_response
