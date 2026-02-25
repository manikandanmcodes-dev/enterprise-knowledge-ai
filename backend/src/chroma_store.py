from dotenv import load_dotenv
from backend.src.embed_chunks import (
    load,
    text_split,
    load_embeddings
)
from langchain_chroma import Chroma
from backend.config.settings import CHROMA_DIR
from pathlib import Path

load_dotenv()

def init_chroma():
    if Path(CHROMA_DIR).exists():
        print("✅ Chroma DB already exists. Skipping creation.")
        return

    print("⚙️ Creating Chroma DB...")

    documents = load()
    chunks = text_split(documents)
    embeddings = load_embeddings()

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR)
    )

    print("✅ Chroma DB created and persisted successfully.")