# # app/rag_engine.py

import os
from langchain_community.document_loaders import (
    PyPDFLoader, UnstructuredFileLoader, Docx2txtLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.qdrant import Qdrant
from langchain_core.documents import Document

from app.config import (
    EMBEDDING_MODEL_NAME, QDRANT_API_KEY, QDRANT_URL, VECTOR_COLLECTION_NAME
)

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.models import PayloadSchemaType


# === 1. Load & Split ===
def load_and_split_document(file_path: str) -> list[Document]:
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".docx":
        loader = Docx2txtLoader(file_path)
    else:
        loader = UnstructuredFileLoader(file_path)

    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(docs)
    return chunks


# === 2. Embed & Store ===
def embed_and_store(chunks: list[Document], session_id: str):
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

    # Tag each chunk with session ID in metadata
    for doc in chunks:
        doc.metadata["session_id"] = session_id

    # Create collection if not exists
    existing_collections = client.get_collections().collections
    if VECTOR_COLLECTION_NAME not in [c.name for c in existing_collections]:
        client.create_collection(
            collection_name=VECTOR_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,  # For MiniLM
                distance=Distance.COSINE
            )
        )

    # Create index for 'session_id' metadata if not already present
    try:
        client.create_payload_index(
            collection_name=VECTOR_COLLECTION_NAME,
            field_name="session_id",
            field_schema=PayloadSchemaType.KEYWORD
        )
    except Exception as e:
        if "already exists" not in str(e):
            raise e

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
    )

    Qdrant.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=VECTOR_COLLECTION_NAME,
        location=QDRANT_URL,
        api_key=QDRANT_API_KEY,
    )


# === 3. Retrieve Relevant Chunks ===
def retrieve_relevent_docs(query: str, session_id: str, k: int = 5) -> list[str]:
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
    )

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        timeout=30  # seconds, increase if needed
    )

    vectorstore = Qdrant(
        client=client,
        collection_name=VECTOR_COLLECTION_NAME,
        embeddings=embeddings
    )

    # Search without filter
    all_docs = vectorstore.similarity_search(query, k=30)  # Fetch more to allow filtering

    # Manual filtering
    filtered_docs = [doc.page_content for doc in all_docs if doc.metadata.get("session_id") == session_id]

    return filtered_docs[:k]
