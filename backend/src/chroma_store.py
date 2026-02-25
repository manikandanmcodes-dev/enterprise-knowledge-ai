from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from pathlib import Path

from backend.src.embed_chunks import (
    load,
    text_split,
    load_embeddings
)
from backend.config.settings import CHROMA_DIR

load_dotenv()


def init_chroma():
    chroma_path = Path(CHROMA_DIR)
    chroma_path.mkdir(parents=True, exist_ok=True)

    documents = load()
    if not documents:
        print("⚠️ No documents found. Skipping Chroma init.")
        return

    chunks = text_split(documents)
    embeddings = load_embeddings()

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(chroma_path)
    )

    #vector_db.persist()

    print("✅ Chroma DB created successfully")

#if __name__ == "__main__":
    #init_chroma()