from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
from phase1.vector_store import get_retriever
import os

def get_qa_response(query):
    connection_string = os.getenv("CONNECTION_STRING")
    collection_name = os.getenv("COLLECTION_NAME")
    print(f"connection_name {collection_name}" )
    print(f"connection_string {connection_string}" )
    retriever = get_retriever(connection_string, collection_name)
    llm = ChatOllama(model="mistral")
    print(f"we are after mistral")
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    result = qa_chain.invoke({"query": query})
    return {"answer": result["result"], "sources": [doc.page_content for doc in result["source_documents"]]}