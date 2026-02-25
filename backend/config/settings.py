from pathlib import Path
import os

# /app/backend
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"

PROMPTS_DIR = BASE_DIR / "prompts"
PROMPT_TEMPLATE = PROMPTS_DIR / "prompt.py"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 500

LOG_LEVEL = "INFO"