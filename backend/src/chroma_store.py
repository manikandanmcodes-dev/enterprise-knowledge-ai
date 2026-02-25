from dotenv import load_dotenv
from backend.src.embed_chunks import (
    load,
    text_split,
    load_embeddings
)
import os
from langchain_chroma import Chroma
from backend.config.settings import CHROMA_DIR
from pathlib import Path


load_dotenv()

documents = load()

chunks = text_split(documents)

embeddings = load_embeddings()

vector_db = Chroma.from_documents(
    documents = chunks,
    embedding=embeddings,
    persist_directory=str(CHROMA_DIR)
)

print("Chroma DB created and persisted successfully.")