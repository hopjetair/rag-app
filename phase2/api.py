from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from phase2.retrieval import get_qa_response
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="RAG PDF API")

class QueryRequest(BaseModel):
    query: str

class AnswerResponse(BaseModel):
    answer: str
    sources: List[str]
    
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QueryRequest):
    try:
        print(f"request query {request.query}")
        response = get_qa_response(request.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
