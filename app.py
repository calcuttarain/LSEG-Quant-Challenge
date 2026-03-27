import streamlit as st
import sys
import os

# HACK: Adăugăm folderele la path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from core.components import render_interactive_graph, apply_custom_css
from core.llm import generate_diagram_code
from config.settings import MODEL_NAME, PROMPTS

st.set_page_config(page_title="Graph Designer Pro", page_icon="🕸️", layout="wide")
apply_custom_css()

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Configurare")
    persona_choice = st.selectbox("Alege Expertul:", list(PROMPTS.keys()))
    st.divider()
    st.info(f"Model activ: {MODEL_NAME}")
    if st.button("🗑️ Șterge Istoric"):
        st.session_state.messages = []
        st.rerun()

st.title(f"Analiză AI: {persona_choice} ")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Redăm istoricul pe ecran
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["type"] == "text":
            st.write(msg["content"])
        elif msg["type"] == "graph":
            render_interactive_graph(msg["content"])

# --- INPUT ---
if prompt := st.chat_input("Descrie procesul sau cere o modificare la grafic..."):
    
    # Adăugăm inputul utilizatorului la memorie
    st.session_state.messages.append({"role": "user", "content": prompt, "type": "text"})
    
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner(f"Expertul '{persona_choice}' lucrează..."):
            
            # Trimitem TOT istoricul către funcție
            graph_data, raw_output, error = generate_diagram_code(st.session_state.messages, persona_choice)
            
            if error:
                st.error(error)
                with st.expander("Vezi Thinking Process / Răspuns Brut"):
                    st.write(raw_output)
            else:
                # Randăm diagrama
                render_interactive_graph(graph_data)
                
                with st.expander("Vezi structura JSON"):
                    st.json(graph_data)
                
                # Salvăm noul graf generat în memorie pentru viitoarele editări
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": graph_data, 
                    "type": "graph"
                })