import os
import asyncio
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

from dotenv import load_dotenv

load_dotenv()


def load_documents():

    file_path = "data/tafsir_quran_1.pdf"

    loader = PyPDFLoader(file_path)

    pages = loader.load()

    return pages


def main():
    print("getting started with loading..")

    pages = load_documents()

    print("\n")
    print("splitting :)")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=150, separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_documents(pages)
    print(f"Created {len(chunks)} chunks")

    print("----- Check chunk quality before uploading -----")
    print("\n--- Sample Chunk (first one) ---")
    print(chunks[0].page_content[:500])
    print("\n--- Sample Chunk (middle) ---")
    print(chunks[len(chunks) // 2].page_content[:500])

    print("\n")
    print("Creating embeddings and uploading to pinecone...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    batch_size = 100

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i : i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(chunks) + batch_size - 1) // batch_size

        print(f"Uploading batch {batch_num}/{total_batches} ({len(batch)} chunks)...")

        if i == 0:
            vectorestore = PineconeVectorStore.from_documents(
                batch, embeddings, index_name=os.environ["INDEX_NAME"]
            )
        else:
            vectorestore.add_documents(batch)

    print(f"✓ Successfully ingested {len(chunks)} chunks to Pinecone!")


if __name__ == "__main__":
    main()
