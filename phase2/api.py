from fastapi import FastAPI
from retrieval import get_qa_response
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/query")
async def query_endpoint(query: str):
    response = get_qa_response(query)
    return {"question": query, "answer": response}