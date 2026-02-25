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
    try:
        chroma_path = Path(CHROMA_DIR)

        # Rebuild DB if missing OR empty
        if not chroma_path.exists() or not any(chroma_path.iterdir()):
            init_chroma()

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vector_db = Chroma(
            persist_directory=str(chroma_path),
            embedding_function=embeddings
        )

        docs = vector_db.max_marginal_relevance_search(
            question,
            k=6,
            fetch_k=20
        )

        context = "\n\n".join(doc.page_content for doc in docs) if docs else ""
        sources = list({doc.metadata.get("source", "unknown") for doc in docs})

        llm = ChatGroq(
            api_key=GROQ_API_KEY,
            model=LLM_MODEL,
            temperature=LLM_TEMPERATURE,
            max_tokens=LLM_MAX_TOKENS
        )

        prompt = get_rag_prompt(context, question)
        response = llm.invoke(prompt)

        return {
            "answer": response.content,
            "sources": sources
        }

    except Exception as e:
        return {
            "error": "Query failed",
            "detail": str(e)
        }