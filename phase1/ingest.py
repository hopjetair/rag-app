import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embeddings import get_embeddings
from vector_store import get_vector_store

def ingest_data(pdf_path, connection_string, collection_name):
    loader = PyMuPDFLoader(pdf_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = get_embeddings()
    get_vector_store(chunks, embeddings, connection_string, collection_name)
    print(f"Indexed {len(chunks)} chunks into {collection_name}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    pdf_path = os.getenv("LOCAL_PDF_PATH", "/path/to/Airline_Regulations_v1.0.pdf")
    connection_string = os.getenv("CONNECTION_STRING", "postgresql://user:pass@localhost:5432/hopjetairline_db")
    collection_name = os.getenv("COLLECTION_NAME", "airline_docs_pg")
    ingest_data(pdf_path, connection_string, collection_name)