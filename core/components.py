# core/components.py

import streamlit.components.v1 as components

def render_mermaid(code: str):
    """Încarcă librăria JS și randează codul Mermaid primit."""
    components.html(
        f"""
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
        </script>
        <div class="mermaid" style="display: flex; justify-content: center; background-color: white; padding: 20px; border-radius: 10px;">
            {code}
        </div>
        """,
        height=600,
        scrolling=True
    )