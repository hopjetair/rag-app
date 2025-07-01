FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY phase1/ ./phase1/
COPY phase2/ ./phase2/

ENV PYTHONPATH=/app

# Phase 1 ingestion (run once, e.g., via entrypoint script or manual trigger)
# Phase 2 API server
CMD ["uvicorn", "phase2.api:app", "--host", "0.0.0.0", "--port", "8003"]