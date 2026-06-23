#!/bin/sh
set -e

python -m app.rag.ingest || echo "RAG ingest failed at startup; app will try lazy ingest on first retrieval."

python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

python -m streamlit run app/frontend.py \
  --server.address 0.0.0.0 \
  --server.port "${PORT:-7860}" \
  --server.headless true
