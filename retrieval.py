import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.runnables import RunnablePassthrough

from langchain_core.output_parsers import PydanticOutputParser
from core.models import VerseLLMResponse

from dotenv import load_dotenv

load_dotenv()


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def retrieval_call(query):
    print("retrieving :)")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    llm = ChatOpenAI(
        verbose=True,
        temperature=0,
        model="gpt-4o-mini",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    vectorstore = PineconeVectorStore(
        index_name=os.environ["INDEX_NAME"], embedding=embeddings
    )

    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)

    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(), combine_docs_chain=combine_docs_chain
    )

    result = retrieval_chain.invoke(input={"input": query})

    template = """You are a Quran verse recommender using Tafsir Ibn Kathir.

    Based on the users question, find an explanation from the text that relates to it. For example of the question is about "poverty", return the explanation
    and verse related to do with how to response to financial lack/worry. Then explain how this is relevant to the users question.

    Use ONLY the information provided in the context below. Do not add interpretations or explanations that are not in the text.

    Provide:
    1. The verse reference (Surah:Ayah)
    2. The verse text (if available in context)
    3. The explanation from Tafsir Ibn Kathir

    If the context doesn't contain relevant information, say "I couldn't find relevant verses in the provided tafsir for this situation."

    Keep your answer concise and faithful to the source text.
    Always end with "Allah knows best."

    Provide your answer in the following JSON format:
    {format_instructions}

    Context from Tafsir Ibn Kathir:
    {context}

    Question: {question}

    Answer (use only the context provided):"""

    query_response_parser = PydanticOutputParser(pydantic_object=VerseLLMResponse)

    custom_rag_prompt = PromptTemplate.from_template(
        template=template,
        partial_variables={
            "format_instructions": query_response_parser.get_format_instructions()
        },
    )

    rag_chain = (
        {
            "context": vectorstore.as_retriever() | format_docs,
            "question": RunnablePassthrough(),
        }
        | custom_rag_prompt
        | llm
        | query_response_parser
    )

    res = rag_chain.invoke(query)

    return res


if __name__ == "__main__":
    result = retrieval_call("I am feeling sad")
    print(result)
