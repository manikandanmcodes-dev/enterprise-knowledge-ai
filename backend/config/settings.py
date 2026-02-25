from pathlib import Path
import os

# backend/
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

DATA_DIR = os.path.join(BASE_DIR, "data")

PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
PROMPT_TEMPLATE = os.path.join(PROMPTS_DIR, "prompt.py")

CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 500

LOG_LEVEL = "INFO"