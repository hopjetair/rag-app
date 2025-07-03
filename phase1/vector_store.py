from langchain_community.vectorstores.pgvector import PGVector
from phase1.embeddings import get_embeddings
from sqlalchemy import create_engine

def get_vector_store(documents, embeddings, connection_string, collection_name):
    return PGVector.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=collection_name,
        connection_string=connection_string
    )

def get_retriever(connection_string, collection_name):
    embeddings = get_embeddings()
    # Create a SQLAlchemy engine for the connection
    engine = create_engine(connection_string)
    # Initialize PGVector with the engine
    vector_store = PGVector.from_existing_index(
        embedding=embeddings,
        collection_name=collection_name,
        connection_string=connection_string,
        pre_delete_collection=False  # Avoid deleting existing data
    )
    return vector_store.as_retriever()