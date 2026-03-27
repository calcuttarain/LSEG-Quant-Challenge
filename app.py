# app.py

import streamlit as st
import sys
import os

# --- HACK PENTRU MACOS: Forțăm Python să vadă folderele 'core' și 'config' ---
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.components import render_mermaid
from core.llm import generate_diagram_code
from config.settings import MODEL_NAME

# --- SETĂRI PAGINĂ ---
st.set_page_config(page_title="Generator Diagrame", page_icon="📊", layout="wide")
st.title("Generare Diagrame Logice Local 🧠 -> 📊")

# Inițializare memorie chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afișare istoric mesaje
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "mermaid":
            render_mermaid(msg["content"])
            with st.expander("Vezi codul Mermaid generat"):
                st.code(msg["content"], language="mermaid")

# --- FLUXUL PRINCIPAL ---
if prompt := st.chat_input("Descrie fluxul pe care vrei să-l transformi în diagramă..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Modelul {MODEL_NAME} gândește..."):
            
            # Apelăm funcția din backend
            mermaid_code, raw_output, error = generate_diagram_code(prompt)
            
            if error:
                st.error(error)
                if raw_output:
                    with st.expander("Vezi răspunsul brut (Debug / Thinking)"):
                        st.write(raw_output)
                st.session_state.messages.append({"role": "assistant", "content": error, "type": "text"})
            else:
                # Succes! Randăm diagrama
                render_mermaid(mermaid_code)
                with st.expander("Vezi codul Mermaid generat"):
                    st.code(mermaid_code, language="mermaid")
                
                # Salvăm în istoric
                st.session_state.messages.append({"role": "assistant", "content": mermaid_code, "type": "mermaid"})