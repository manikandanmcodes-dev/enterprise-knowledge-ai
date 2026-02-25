from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from pathlib import Path

from backend.src.chroma_store import init_chroma
from backend.config.settings import (
    GROQ_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    LLM_MAX_TOKENS,
    CHROMA_DIR
)
from backend.prompts.prompt import get_rag_prompt

load_dotenv()

# --- RAG Answer ---
def answer_question(question: str) -> dict:
    # ✅ Lazy init (runs only when API is called)
    if not Path(CHROMA_DIR).exists():
        init_chroma()

    # --- Embeddings ---
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # --- Vector DB ---
    vector_db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings
    )

    # --- LLM ---
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        max_tokens=LLM_MAX_TOKENS
    )

    docs = vector_db.max_marginal_relevance_search(
        question,
        k=6,
        fetch_k=20
    )

    context = "\n\n".join(doc.page_content for doc in docs) if docs else ""
    sources = list({doc.metadata.get("source", "unknown") for doc in docs})

    prompt = get_rag_prompt(context, question)
    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": sources
    }