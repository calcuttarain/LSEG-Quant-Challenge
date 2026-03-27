# core/llm.py

import ollama
import re
from config.settings import SYSTEM_PROMPT, MODEL_NAME

def generate_diagram_code(user_prompt: str):
    """
    Comunică cu LLM-ul local și extrage codul Mermaid.
    Returnează: (mermaid_code, raw_output, error_message)
    """
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_prompt}
        ])
        
        llm_output = response['message']['content']
        
        # Căutăm blocul de cod Mermaid, ignorând tag-urile <think> ale modelului DeepSeek
        match = re.search(r'```mermaid\n(.*?)```', llm_output, re.DOTALL)
        
        if match:
            mermaid_code = match.group(1).strip()
            return mermaid_code, llm_output, None
        else:
            return None, llm_output, "Modelul nu a returnat un cod Mermaid valid."
            
    except Exception as e:
        return None, None, f"Eroare de conexiune cu Ollama: {str(e)}"