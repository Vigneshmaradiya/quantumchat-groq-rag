# app/main.py

import os
import uuid
import json
import streamlit as st
from dotenv import load_dotenv
from typing import cast


from app.config import SUPPORTED_MODELS
from app.session_memory import (
    init_session, get_session_messages,
    append_message, list_all_sessions,
    delete_session
)
from app.llm_router import chat_with_model
from app.rag_engine import (
    load_and_split_document,
    embed_and_store,
    retrieve_relevent_docs
)
from utils.token_utils import count_tokens


# Load environment variables
load_dotenv()


# ========================= UI CONFIG ==========================
st.set_page_config(page_icon="https://imgs.search.brave.com/v1gpZ0Uwe7VkfVDv0XjvKhTFyR7e4ZU10juG72T1aV0/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9jZG4t/aWNvbnMtcG5nLmZy/ZWVwaWsuY29tLzI1/Ni84NzA4Lzg3MDg3/NjkucG5nP3NlbXQ9/YWlzX2h5YnJpZA", page_title="Open Source ChatGPT", layout="wide")
st.title("💬 QuantumChat: Lightning-Fast AI with GROQ & RAG")

# Sidebar - session management
with st.sidebar:
    st.header("🧠 Sessions")
    sessions = list_all_sessions()
    
    # ensure upload folder exists
    os.makedirs("data/uploads", exist_ok=True)

    selected_session = st.selectbox("Select a session", sessions + ["+ New Session"])
    if selected_session is None:
        st.stop()  # or raise an error

    # Safeguard default selection
    # session_id: str


    # If new session, create one

    if selected_session == "+ New Session":
        session_id = str(uuid.uuid4())[:8]
        init_session(session_id)
        st.success(f"Created new session: {session_id}")
    else:
        session_id = selected_session
        init_session(session_id)

    messages = get_session_messages(session_id)
    st.download_button(
        label="⬇️ Download Chat History",
        data=json.dumps(messages, indent=2),
        file_name=f"chat_{session_id}.json",
        mime="application/json"
    )

    # Optional: delete session
    if st.button("🗑️ Delete Session"):
        delete_session(session_id)
        st.experimental_rerun()

    
    # Model selection
    model_key = cast(str,st.selectbox(
        "Choose a model", 
        list(SUPPORTED_MODELS.keys()), 
        index=0
    ))
    model_info = SUPPORTED_MODELS[model_key]
    model_name = model_info["name"]

    #Upload files
    st.markdown("---")
    uploaded_files = st.file_uploader("📄 Upload document for RAG", type=["pdf","docx","txt","md","html"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            file_path = f"data/uploads/{uploaded_file.name}"
            with open(file_path, "wb") as f:
                f.write(uploaded_file.read())
            chunks = load_and_split_document(file_path)
            embed_and_store(chunks, session_id=session_id)
            
        st.success("✅ Document embedded successfully!")


# ========================= CHAT UI ==========================
# Get current session messages
messages = get_session_messages(session_id)

# Display chat history
for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# Chat input
user_input = st.chat_input("Ask anything...")

if user_input:
    # Display user input
    with st.chat_message("user"):
        st.markdown(user_input)
    append_message(session_id, "user", user_input)

    # Retrieve RAG content
    retrieved_chunks = retrieve_relevent_docs(user_input, session_id=session_id, k=4)
    context = "\n".join(retrieved_chunks)

    # Compose messages with context
    chat_history = get_session_messages(session_id)
    prompt_with_context = [
        {"role": "system", "content": "You are a helpful assistant with access to relevent documents."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_input}"}
    ] + chat_history[-6:]  # Limit history for token efficiency

    # Stream assistant response
    with st.chat_message("assistant"):
        full_response = ""
        response_stream = chat_with_model(model=model_name, messages=prompt_with_context, stream=True)
        response_area = st.empty()
        for chunk in response_stream:
            full_response +=chunk
            response_area.markdown(full_response, unsafe_allow_html=True)
        append_message(session_id, "assistant", full_response)

        total_tokens = count_tokens(full_response, model=model_name)
        st.caption(f"🔢 Tokens used: {total_tokens}")
