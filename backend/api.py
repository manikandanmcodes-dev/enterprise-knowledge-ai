from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from backend.src.rag_answer import answer_question
from backend.middleware.rate_limit import limiter
from backend.utils.logging_config import setup_logging
from backend.config import settings

# --------------------------------
# App & Logging
# --------------------------------
setup_logging(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(title="Enterprise Knowledge AI")

# --------------------------------
# Rate Limiting
# --------------------------------
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

# --------------------------------
# CORS (frontend access)
# --------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------
# Request / Response Models
# --------------------------------
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

# --------------------------------
# API Endpoints
# --------------------------------
@app.post("/query", response_model=QueryResponse)
@limiter.limit("10/minute")
def query_knowledge_base(
    request: Request,
    payload: QueryRequest
):
    logger.info(f"Received query: {payload.question}")
    response = answer_question(payload.question)
    return response


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "enterprise-knowledge-ai"
    }