import ollama
import re
import json
from config.settings import BASE_SYSTEM_PROMPT, PROMPTS, MODEL_NAME

def generate_diagram_code(user_prompt: str, persona_key: str):
    """
    Comunică cu LLM-ul local și extrage JSON-ul pentru graf.
    """
    # Construim prompt-ul complet
    full_system = f"{PROMPTS[persona_key]}\n{BASE_SYSTEM_PROMPT}"
    
    try:
        response = ollama.chat(model=MODEL_NAME, messages=[
            {'role': 'system', 'content': full_system},
            {'role': 'user', 'content': user_prompt}
        ])
        
        llm_output = response['message']['content']
        
        # Căutăm blocul de cod JSON (ignora gândirea modelului DeepSeek)
        match = re.search(r'```json\n(.*?)\n```', llm_output, re.DOTALL)
        
        if match:
            try:
                graph_data = json.loads(match.group(1).strip())
                # Curățare minimală: ne asigurăm că avem listele necesare
                if "nodes" not in graph_data: graph_data["nodes"] = []
                if "edges" not in graph_data: graph_data["edges"] = []
                return graph_data, llm_output, None
            except json.JSONDecodeError:
                return None, llm_output, "Eroare la parsarea JSON-ului generat."
        else:
            return None, llm_output, "Modelul nu a returnat un format JSON valid."
            
    except Exception as e:
        return None, None, f"Eroare de conexiune cu Ollama: {str(e)}"