## **Graph Designer PRO 2000**

## Overview
Graph Designer Pro is an interactive, AI-powered web application designed to generate, visualize, and dynamically modify network diagrams and flowcharts using natural language. By leveraging local Large Language Models (LLMs) via Ollama, the system translates textual descriptions of processes, architectures, or conceptual maps into structured JSON data. This data is subsequently rendered as an interactive, physics-enabled network graph.

## Key Features

* **Iterative Graph Generation:** Users can construct and refine diagrams through a conversational interface. The application maintains session history, allowing the AI to understand the current graph state and apply incremental modifications based on user feedback.
* **Dynamic Visual Rendering:** Powered by `streamlit_agraph`, the application displays fully interactive graphs. Features include node dragging, automated physics-based layout stabilization, and highlight behaviors upon selection.
* **Specialized AI Personas:** The application utilizes tailored system prompts to adjust the logic, styling, and hierarchy of the generated graphs. Users can toggle between:
    * **Rigorous Architect (Logical):** Prioritizes continuous process flow and logical consistency, outputting a uniform, neutral aesthetic.
    * **Hierarchical (Importance-based):** Scales node sizes and applies distinct colors based on the critical nature or weight of the node (e.g., major databases vs. standard processes).
    * **Minimalist (Rapid):** Bypasses complex styling for quick, foundational structural generation.
* **Local Processing:** Relies on local LLM execution via Ollama (configured by default for `deepseek-r1:14b`), ensuring data privacy and offline capability.
* **Premium User Interface:** Custom CSS implementation provides a modern, dark-themed interface optimized for data visualization and professional environments.

## Architecture and Technology Stack

* **Frontend / Framework:** Streamlit
* **Graph Visualization:** `streamlit_agraph`
* **AI / LLM Backend:** Ollama (Local LLM Execution)
* **Default Model:** `deepseek-r1:14b` (Configurable)
* **Data Structure:** Strict JSON schema parsing for node and edge generation.

## Prerequisites

Before running the application, ensure you have the following installed on your system:
1. Python 3.8 or higher.
2. [Ollama](https://ollama.com/) installed and running locally.
3. The specific LLM pulled via Ollama. You can do this by running the following command in your terminal:
   `ollama run deepseek-r1:14b`

## Installation and Setup

1. **Clone the repository:**
   Ensure you have the project files downloaded and navigate to the root directory of the project.

2. **Install Python dependencies:**
   It is recommended to use a virtual environment. Install the required packages using pip:
   ```bash
   pip install streamlit streamlit-agraph ollama

2. **Run Main Script:**
   ```bash
   python3 -m streamlit run ./app.py

