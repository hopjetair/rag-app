import os
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama
from dotenv import load_dotenv

load_dotenv()

# === Connection Config ===
RDS_HOST = "database-rag.cta8wggyqhhv.ap-south-1.rds.amazonaws.com"
RDS_USER = "ppm"
RDS_PASSWORD = ""
RDS_PORT = "5432"
RDS_DBNAME = "ragdb"

CONNECTION_STRING = f"postgresql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DBNAME}"

# === Setup ===
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LOCAL_PDF_PATH = "/Users/preethupallavim/Desktop/RAG/Airline_Regulations_v1.0.pdf"
COLLECTION_NAME = "airline_docs_pg"

# === Streamlit UI ===
st.title("📄 RAG PDF Chat (Mistral + PGVector)")

# === Load and Split ===
if not os.path.exists(LOCAL_PDF_PATH):
    st.error(f"PDF file not found at path: {LOCAL_PDF_PATH}")
else:
    st.success(f"Using PDF: {LOCAL_PDF_PATH}")

    loader = PyMuPDFLoader(LOCAL_PDF_PATH)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    # === Embed & Store ===
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    vectordb = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING
    )

    retriever = vectordb.as_retriever()

    # === RAG Chain ===
    llm = ChatOllama(model="mistral")
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    # === Chat Interface ===
    query = st.text_input("Ask a question about the PDF:")
    if query:
        result = qa_chain.invoke({"query": query})
        st.markdown("### 🤖 Answer")
        st.write(result["result"])

        with st.expander("📚 Sources"):
            #for doc in result["source_documents"]:
            #    st.markdown(f"• {doc.metadata.get('source', 'Unknown')}")
            for i, doc in enumerate(result["source_documents"], 1):
                st.markdown(f"• {doc.page_content}")
