rag-app/
├── phase1/
│   ├── ingest.py         # Data ingestion and indexing
│   ├── embeddings.py     # Embedding generation
│   ├── vector_store.py   # Vector store management
│   └── __init__.py
├── phase2/
│   ├── api.py            # FastAPI application
│   ├── retrieval.py      # RAG retrieval logic
│   ├── vector_store.py   # Vector store querying
│   └── __init__.py
├── Dockerfile
├── task-definition.json
├── .github/workf
│   └── ci-cd.yml
├── requirements.txt
└── .env.example          # Example environment variables