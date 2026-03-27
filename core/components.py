import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

def apply_custom_css():
    """Stiluri pentru interfața Streamlit cu un look Financial/Premium."""
    st.markdown("""
       <style>
        /* Fundal Dark Blue cu degrade fin */
        .stApp {
            background: #7485ab;
            color: #f1f5f9;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Carduri și containere */
        [data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
        }

        /* Sidebar Glassmorphism */
        [data-testid="stSidebar"] {
            background-color: #c5d0e8;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }

        /* Butoane stilizate, proeminente */
        .stButton>button {
            background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
            border: 1px solid #60a5fa;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            font-size: 1rem;
            letter-spacing: 0.5px;
            padding: 0 .6rem 1.2rem;
            box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.4);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #60a5fa 0%, #2563eb 100%);
            box-shadow: 0 6px 20px rgba(37, 99, 235, 0.6);
            transform: translateY(-2px);
            border-color: #93c5fd;
        }
        </style>
    """, unsafe_allow_html=True)

def render_interactive_graph(graph_data):
    """Randează diagrama cu setări de fizică îmbunătățite și stil vizual premium."""
    if not graph_data or "nodes" not in graph_data:
        return

    nodes = []
    for n in graph_data.get("nodes", []):
        node_id = str(n.get("id", "unknown"))
        nodes.append(Node(
            id=node_id, 
            label=n.get("label", node_id), 
            size=n.get("size", 30), 
            color=n.get("color", "#3b82f6"),
            shape="box", # Acesta forțează textul să fie ÎN INTERIORUL nodului
            font={'color': '#ffffff', 'size': 16, 'face': 'Arial', 'multi': True},
            shadow={'enabled': True, 'color': 'rgba(0,0,0,0.5)', 'size': 10}
        ))
    
    edges = []
    for e in graph_data.get("edges", []):
        src = e.get("source")
        dst = e.get("target")
        if src and dst:
            edges.append(Edge(
                source=str(src), 
                target=str(dst), 
                label=e.get("label", ""),
                color="#64748b",
                width=2
            ))

    config = Config(
        width=1000,
        height=700,
        directed=True, 
        physics={
            "enabled": True,
            "stabilization": {"iterations": 200},
            "barnesHut": {
                "gravitationalConstant": -3000,
                "centralGravity": 0.3,
                "springLength": 180,
                "springConstant": 0.04
            }
        }, 
        nodeHighlightBehavior=True,
        highlightColor="#facc15",
        collapsible=False
    )

    return agraph(nodes=nodes, edges=edges, config=config)