from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from vector_store import get_retriever
import os

def get_qa_response(query):
    connection_string = os.getenv("CONNECTION_STRING", "postgresql://user:pass@localhost:5432/hopjetairline_db")
    collection_name = os.getenv("COLLECTION_NAME", "airline_docs_pg")
    retriever = get_retriever(connection_string, collection_name)
    llm = ChatOllama(model="mistral")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=False)
    return qa_chain.invoke({"query": query})["result"]