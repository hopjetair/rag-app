from langchain_community.vectorstores.pgvector import PGVector
import os


def get_retriever(connection_string, collection_name):
    embeddings = get_embeddings()
    return PGVector(connection_string=connection_string, embedding=embeddings, collection_name=collection_name).as_retriever()