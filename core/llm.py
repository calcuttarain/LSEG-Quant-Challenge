import ollama
import re
import json
from config.settings import BASE_SYSTEM_PROMPT, PROMPTS, MODEL_NAME

def generate_diagram_code(chat_history: list, persona_key: str):
    """
    Comunică cu LLM-ul local trimițând tot contextul, extrăgând apoi JSON-ul pentru noul graf.
    """
    full_system = f"{PROMPTS[persona_key]}\n{BASE_SYSTEM_PROMPT}"
    
    # Construim array-ul de mesaje pentru Ollama (incluzând prompt-ul de sistem)
    messages_for_llm = [{'role': 'system', 'content': full_system}]
    
    for msg in chat_history:
        # Convertim diagramele generate anterior în string JSON ca LLM-ul să le poată citi
        if msg["type"] == "graph":
            json_str = json.dumps(msg["content"], ensure_ascii=False)
            messages_for_llm.append({'role': msg["role"], 'content': f"```json\n{json_str}\n```"})
        else:
            messages_for_llm.append({'role': msg["role"], 'content': msg["content"]})
            
    try:
        response = ollama.chat(model=MODEL_NAME, messages=messages_for_llm)
        
        llm_output = response['message']['content']
        
        # Căutăm blocul de cod JSON (ignorăm thinking process-ul)
        match = re.search(r'```json\n(.*?)\n```', llm_output, re.DOTALL)
        
        if match:
            try:
                graph_data = json.loads(match.group(1).strip())
                if "nodes" not in graph_data: graph_data["nodes"] = []
                if "edges" not in graph_data: graph_data["edges"] = []
                return graph_data, llm_output, None
            except json.JSONDecodeError:
                return None, llm_output, "Eroare la parsarea JSON-ului generat."
        else:
            return None, llm_output, "Modelul nu a returnat un format JSON valid."
            
    except Exception as e:
        return None, None, f"Eroare de conexiune cu Ollama: {str(e)}"