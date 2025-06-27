# app/session_memory.py

import streamlit as st
from typing import List, Dict
import json
import os

SESSION_FILE = "data/chat_sessions.json"

def _load_sessions_from_file():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_sessions_to_file():
    with open(SESSION_FILE, "w") as f:
        json.dump(st.session_state.sessions, f, indent=2)

def init_session(session_id: str) -> None:
    if "sessions" not in st.session_state:
        st.session_state.sessions = _load_sessions_from_file()

    if session_id not in st.session_state.sessions:
        st.session_state.sessions[session_id] = []
        _save_sessions_to_file()

def get_session_messages(session_id: str) -> List[Dict[str, str]]:
    init_session(session_id)
    return st.session_state.sessions[session_id]

def append_message(session_id: str, role: str, content: str) -> None:
    init_session(session_id)
    st.session_state.sessions[session_id].append({
        "role": role,
        "content": content
    })
    _save_sessions_to_file()

def list_all_sessions() -> List[str]:
    if "sessions" not in st.session_state:
        st.session_state.sessions = _load_sessions_from_file()
    return list(st.session_state.sessions.keys())

def delete_session(session_id: str) -> None:
    if "sessions" in st.session_state and session_id in st.session_state.sessions:
        del st.session_state.sessions[session_id]
        _save_sessions_to_file()
