import os
import boto3
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embeddings import get_embeddings
from vector_store import get_vector_store

def ingest_data_from_s3(bucket_name, object_key, connection_string, collection_name):
    s3 = boto3.client('s3')
    local_path = f"/tmp/{object_key}"
    s3.download_file(bucket_name, object_key, local_path)
    loader = PyMuPDFLoader(local_path)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = get_embeddings()
    get_vector_store(chunks, embeddings, connection_string, collection_name)
    print(f"Indexed {len(chunks)} chunks into {collection_name}")

def ingest_data_local(pdf_path, connection_string, collection_name):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at {pdf_path}")
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
    use_s3 = os.getenv("USE_S3", "false").lower() == "true"
    connection_string = os.getenv("CONNECTION_STRING")
    collection_name = os.getenv("COLLECTION_NAME")
    if use_s3:
        bucket_name = os.getenv("BUCKET_NAME")
        object_key = os.getenv("OBJECT_KEY")
        ingest_data_from_s3(bucket_name, object_key, connection_string, collection_name)
    else:
        pdf_path = os.getenv("LOCAL_PDF_PATH")
        ingest_data_local(pdf_path, connection_string, collection_name)