import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

def apply_custom_css():
    """Aplică stilurile globale pentru interfața Streamlit."""
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #f8fafc;
        }
        .stButton>button {
            background: linear-gradient(90deg, #3b82f6, #2563eb);
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        [data-testid="stSidebar"] {
            background-color: rgba(15, 23, 42, 0.8);
        }
        </style>
    """, unsafe_allow_html=True)

def render_interactive_graph(graph_data):
    """Randează diagrama interactivă cu măsuri de siguranță anti-KeyError."""
    if not graph_data or "nodes" not in graph_data:
        st.warning("Datele diagramei sunt incomplete.")
        return

    nodes = []
    for n in graph_data.get("nodes", []):
        node_id = str(n.get("id", "unknown"))
        nodes.append(Node(
            id=node_id, 
            label=n.get("label", node_id), 
            size=n.get("size", 25), 
            color=n.get("color", "#3b82f6")
        ))
    
    edges = []
    for e in graph_data.get("edges", []):
        # Protecție la KeyError: 'source' sau 'target'
        src = e.get("source")
        dst = e.get("target")
        
        if src and dst:
            edges.append(Edge(
                source=str(src), 
                target=str(dst), 
                label=e.get("label", "")
            ))

    config = Config(
        width=1000,
        height=600,
        directed=True, 
        physics=True, 
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A7",
        collapsible=False
    )

    return agraph(nodes=nodes, edges=edges, config=config)