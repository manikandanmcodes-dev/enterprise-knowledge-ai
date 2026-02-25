FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/tmp/huggingface
ENV TRANSFORMERS_CACHE=/tmp/huggingface

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 👇 COPY BACKEND CODE
COPY backend /app/backend

# 👇 ENSURE THESE EXIST (CRITICAL)
RUN mkdir -p /app/backend/data /app/backend/chroma_db

EXPOSE 8000

CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]