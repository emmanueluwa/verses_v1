import os
from sqlalchemy.orm import Session
from core.config import settings

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

from core.prompts import VERSE_PROMPT
from models.verse import Verse
from core.models import VerseLLMResponse
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
        cls, db: Session, session_id: str, query: str = "I am feeling sad"
    ) -> Verse:
        llm = cls._get_llm()
        retrieval_call(query)
