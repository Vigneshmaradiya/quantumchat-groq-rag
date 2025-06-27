# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# === Groq API (OpenAI-Compitible) ===
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_BASE = "https://api.groq.com/openai/v1"


# === Qdrant Vector DB Config === 
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_URL = os.getenv("QDRANT_URL")


# === Default Embedding Model === 
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


# === Supported Groq LLMs === 
SUPPORTED_MODELS = {
    "llama3_instant":{
        "name": "llama-3.1-8b-instant",
        "max_tokens": 131072
    },
    "llama3_versatile": {
        "name": "llama3-3.3-70b-versatile",
        "max_tokens": 32768
    },
    "gemma2_9b_it": {
        "name": "gemma2-9b-it",
        "max_tokens": 8192
    }
}

DEFAULT_MODEL = SUPPORTED_MODELS["llama3_instant"]["name"]


# === App Constants ===
UPLOAD_DIR = "data/uploads"
VECTOR_COLLECTION_NAME = "chatbot-documents"