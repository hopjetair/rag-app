# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code 
COPY phase1/ ./phase1/
COPY phase2/ ./phase2/


# Set environment variable
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl -f http://localhost:8080/health || exit 1

# Run the application
# Phase 1 ingestion (run once, e.g., via entrypoint script or manual trigger)
# Phase 2 API server
CMD ["uvicorn", "phase2.api:app", "--host", "0.0.0.0", "--port", "8080"]