import os
import asyncio
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv

load_dotenv()


async def load_documents():

    file_path = "data/tafsir_quran_1.pdf"

    loader = PyPDFLoader(file_path)
    pages = []

    async for page in loader.alazy_load():
        pages.append(page)

    return pages


async def main():
    print("getting started")

    pages = await load_documents()

    print("splitting :)")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    texts = text_splitter.split_documents(pages)

    print(f"created {len(texts)} chunks")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    print("ingesting :)")
    PineconeVectorStore.from_documents(
        texts, embeddings, index_name=os.environ["INDEX_NAME"]
    )


if __name__ == "__main__":
    asyncio.run(main())
